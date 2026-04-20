#!/bin/bash
# monitor-resources.sh - Monitor memory pressure and protect host system

set -e

echo "=== Resource Monitor for SkyMechanics ==="

# Memory threshold (percentage)
MEMORY_THRESHOLD=85

# Check current memory usage
check_memory() {
    local mem_info=$(cat /proc/meminfo | grep MemAvailable)
    local mem_total=$(cat /proc/meminfo | grep MemTotal | awk '{print $2}')
    local mem_available=$(cat /proc/meminfo | grep MemAvailable | awk '{print $2}')
    local mem_used=$((mem_total - mem_available))
    local mem_percent=$((mem_used * 100 / mem_total))
    
    echo "Memory Usage: ${mem_percent}% (${mem_used} KiB / ${mem_total} KiB)"
    
    if [ $mem_percent -gt $MEMORY_THRESHOLD ]; then
        echo "⚠️  HIGH MEMORY PRESSURE DETECTED!"
        echo "Protecting host system..."
        
        # Send alert (Telegram notification)
        if command -v openclaw &> /dev/null; then
            openclaw telegram sendMessage \
                --chat-id 5824139677 \
                --text "⚠️ MEMORY PRESSURE ALERT: ${mem_percent}% used on ${HOSTNAME}"
        fi
        
        # Log to file
        echo "$(date): Memory pressure at ${mem_percent}%" >> /var/log/skymechanics-resource-alerts.log
        
        return 1
    fi
    
    return 0
}

# Get container resource usage
get_container_stats() {
    echo "=== Current Container Resource Usage ==="
    docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}"
}

# Check FalkorDB memory (critical service)
check_falkordb_memory() {
    local falkordb_mem=$(docker stats --no-stream --format "{{.MemPerc}}" gb10-falkordb 2>/dev/null | tr -d '%')
    
    if [ -n "$falkordb_mem" ]; then
        echo "FalkorDB Memory: ${falkordb_mem}%"
        if [ "$falkordb_mem" -gt 30 ]; then
            echo "⚠️ FalkorDB memory usage is high (>30%)"
        fi
    fi
}

# Get K8s pod resource usage
get_k8s_pod_stats() {
    if command -v kubectl &> /dev/null && kubectl cluster-info &> /dev/null; then
        echo "=== K8s Pod Resource Usage ==="
        kubectl top pods --all-namespaces 2>/dev/null || echo "Metrics server not available or no pods running"
    fi
}

# Main monitoring loop
monitor_loop() {
    echo "Starting resource monitor..."
    echo "Memory threshold: ${MEMORY_THRESHOLD}%"
    echo "Press Ctrl+C to stop"
    
    while true; do
        clear
        check_memory
        echo ""
        get_container_stats
        echo ""
        get_k8s_pod_stats
        
        # Check every 5 seconds
        sleep 5
    done
}

# One-time check
one_time_check() {
    check_memory
    echo ""
    get_container_stats
    echo ""
    get_k8s_pod_stats
}

# Alert script for system monitoring
generate_alert_script() {
    cat << 'EOF' > /usr/local/bin/skymemalert
#!/bin/bash
# Auto-generated memory alert script

THRESHOLD=${1:-85}

while true; do
    mem_total=$(cat /proc/meminfo | grep MemTotal | awk '{print $2}')
    mem_available=$(cat /proc/meminfo | grep MemAvailable | awk '{print $2}')
    mem_used=$((mem_total - mem_available))
    mem_percent=$((mem_used * 100 / mem_total))
    
    if [ $mem_percent -gt $THRESHOLD ]; then
        echo "$(date): Memory at ${mem_percent}% - triggering alert"
        # Log to system log
        logger -t skymemalert "Memory pressure at ${mem_percent}% - protecting host"
        
        # Optional: Send to OpenClaw
        if command -v openclaw &> /dev/null; then
            openclaw telegram sendMessage \
                --chat-id 5824139677 \
                --text "⚠️ MEMORY CRITICAL: ${mem_percent}% on ${HOSTNAME}" 2>/dev/null || true
        fi
    fi
    
    sleep 10
done
EOF
    chmod +x /usr/local/bin/skymemalert
    echo "Alert script created at /usr/local/bin/skymemalert"
}

# Parse arguments
case "${1:-check}" in
    check)
        one_time_check
        ;;
    monitor)
        monitor_loop
        ;;
    alert-script)
        generate_alert_script
        ;;
    help|*)
        echo "Usage: $0 [check|monitor|alert-script|help]"
        echo ""
        echo "Commands:"
        echo "  check        - One-time memory check"
        echo "  monitor      - Continuous monitoring loop"
        echo "  alert-script - Generate system alert script"
        echo "  help         - Show this help"
        ;;
esac
