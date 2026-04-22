"""Generate OpenAPI spec for all SkyMechanics services."""

import json
import sys
from pathlib import Path

# Add the backend directory to the path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))
sys.path.insert(0, str(backend_dir / "services"))

from auth_service.main import app as auth_app
from mechanics_service.main import app as mechanics_app
from jobs_service.main import app as jobs_app
from aircraft_service.main import app as aircraft_app


def generate_openapi_specs():
    """Generate OpenAPI specs for all services."""
    specs = {}
    
    services = [
        ("auth", auth_app, "/api/v1"),
        ("mechanics", mechanics_app, "/api/v1"),
        ("jobs", jobs_app, "/api/v1"),
        ("aircraft", aircraft_app, "/api/v1"),
    ]
    
    for name, app, prefix in services:
        spec = app.openapi()
        # Adjust paths to remove prefix for cleaner spec
        paths = {}
        for path, methods in spec.get("paths", {}).items():
            if path.startswith(prefix):
                paths[path[len(prefix):]] = methods
            else:
                paths[path] = methods
        
        specs[name] = {
            "info": spec.get("info", {}),
            "paths": paths,
            "components": spec.get("components", {}),
            "servers": [{"url": f"http://localhost:820{services.index((name, app, prefix))}"}],
        }
    
    return specs


def save_specs(specs: dict, output_dir: Path):
    """Save OpenAPI specs to JSON files."""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for name, spec in specs.items():
        output_file = output_dir / f"{name}_api.json"
        with open(output_file, "w") as f:
            json.dump(spec, f, indent=2)
        print(f"Generated: {output_file}")


if __name__ == "__main__":
    specs = generate_openapi_specs()
    output_dir = Path(__file__).parent / "openapi_specs"
    save_specs(specs, output_dir)
