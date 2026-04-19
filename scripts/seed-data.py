"""
Seed data for SkyMechanics Platform.
Creates sample entities for testing.
"""
import sys
sys.path.insert(0, '/app')

from db import db_client
from models import CustomerCreateRequest, JobCreateRequest, MechanicCreateRequest


def seed_sample_data():
    """Seed the database with sample data."""
    try:
        db_client.connect()
        graph = db_client.get_graph()
        
        # Create sample customers
        customers = [
            {"name": "John Smith", "email": "john.smith@example.com", "phone": "555-0101"},
            {"name": "Jane Doe", "email": "jane.doe@example.com", "phone": "555-0102"},
            {"name": "Bob Johnson", "email": "bob.johnson@example.com", "phone": "555-0103"},
        ]
        
        customer_ids = []
        for customer_data in customers:
            # Check if customer already exists
            check_query = "MATCH (c:Customer {email: $email}) RETURN c"
            check_result = graph.query(check_query, params={"email": customer_data["email"]})
            
            if not check_result.result_set:
                create_query = (
                    "CREATE (c:Customer {"
                    "name: $name, email: $email, phone: $phone"
                    "}) RETURN c"
                )
                result = graph.query(create_query, params=customer_data)
                customer_id = result.result_set[0][0].id
                customer_ids.append(customer_id)
                print(f"✅ Created customer: {customer_data['name']} (ID: {customer_id})")
            else:
                customer_id = check_result.result_set[0][0].id
                customer_ids.append(customer_id)
                print(f"⏭️  Customer already exists: {customer_data['name']} (ID: {customer_id})")
        
        # Create sample mechanics
        mechanics = [
            {"name": "Alice Williams", "email": "alice.williams@example.com", "phone": "555-0201", "specialties": ["engine", "transmission"]},
            {"name": "Charlie Brown", "email": "charlie.brown@example.com", "phone": "555-0202", "specialties": ["brakes", "suspension"]},
            {"name": "Diana Prince", "email": "diana.prince@example.com", "phone": "555-0203", "specialties": ["electrical", "diagnostics"]},
        ]
        
        mechanic_ids = []
        for mechanic_data in mechanics:
            # Check if mechanic already exists
            check_query = "MATCH (m:Mechanic {email: $email}) RETURN m"
            check_result = graph.query(check_query, params={"email": mechanic_data["email"]})
            
            if not check_result.result_set:
                create_query = (
                    "CREATE (m:Mechanic {"
                    "name: $name, email: $email, phone: $phone, specialties: $specialties"
                    "}) RETURN m"
                )
                result = graph.query(create_query, params=mechanic_data)
                mechanic_id = result.result_set[0][0].id
                mechanic_ids.append(mechanic_id)
                print(f"✅ Created mechanic: {mechanic_data['name']} (ID: {mechanic_id})")
            else:
                mechanic_id = check_result.result_set[0][0].id
                mechanic_ids.append(mechanic_id)
                print(f"⏭️  Mechanic already exists: {mechanic_data['name']} (ID: {mechanic_id})")
        
        # Create sample jobs
        jobs = [
            {"customer_id": customer_ids[0], "title": "Engine Repair", "description": "Engine performance issues", "status": "pending", "priority": 2},
            {"customer_id": customer_ids[1], "title": "Brake Replacement", "description": "Front and rear brakes", "status": "in-progress", "priority": 1},
            {"customer_id": customer_ids[2], "title": "Diagnostic Check", "description": "Check engine light on", "status": "pending", "priority": 3},
        ]
        
        for job_data in jobs:
            # Verify customer exists
            check_query = "MATCH (c:Customer) WHERE id(c) = $customer_id RETURN c"
            check_result = graph.query(check_query, params={"customer_id": job_data["customer_id"]})
            
            if check_result.result_set:
                # Check if job already exists
                job_check_query = (
                    "MATCH (c:Customer)-[:OWNS]->(j:Job {title: $title}) "
                    "RETURN j"
                )
                job_check_result = graph.query(job_check_query, params={"title": job_data["title"]})
                
                if not job_check_result.result_set:
                    create_query = (
                        "MATCH (c:Customer) WHERE id(c) = $customer_id "
                        "CREATE (j:Job {"
                        "title: $title, description: $description, status: $status, priority: $priority"
                        "}) "
                        "CREATE (c)-[:OWNS]->(j) "
                        "RETURN j"
                    )
                    result = graph.query(create_query, params=job_data)
                    job_id = result.result_set[0][0].id
                    print(f"✅ Created job: {job_data['title']} (ID: {job_id})")
                else:
                    print(f"⏭️  Job already exists: {job_data['title']}")
        
        # Create relationships between mechanics and jobs
        # Alice Williams (mechanic_ids[0]) -> Engine Repair (jobs[0])
        # Charlie Brown (mechanic_ids[1]) -> Brake Replacement (jobs[1])
        
        assign_query = (
            "MATCH (m:Mechanic), (j:Job) "
            "WHERE id(m) = $mechanic_id AND id(j) = $job_id "
            "CREATE (m)-[:WORKS_ON {assigned_at: datetime()}]->(j)"
        )
        
        # Assign first mechanic to first job
        graph.query(assign_query, params={"mechanic_id": mechanic_ids[0], "job_id": 0})  # 0 is first job node ID
        print("✅ Assigned mechanic to job")
        
        print("\n📊 Seed data completed!")
        print(f"   Customers: {len(customers)}")
        print(f"   Mechanics: {len(mechanics)}")
        print(f"   Jobs: {len(jobs)}")
        
    except Exception as e:
        print(f"❌ Error seeding data: {e}")
    finally:
        db_client.close()


if __name__ == "__main__":
    seed_sample_data()
