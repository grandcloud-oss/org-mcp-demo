# Quick Reference Guide

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Configuration

### Option 1: Environment Variables (Recommended)
```bash
export NEO4J_URI="bolt://localhost:7687"
export NEO4J_USERNAME="neo4j"
export NEO4J_PASSWORD="your-password"
export NEO4J_DATABASE="neo4j"
```

### Option 2: Direct Configuration
Edit the connection parameters in your Python script:
```python
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "your-password"
NEO4J_DATABASE = "neo4j"
```

## Quick Start

```python
from neo4j_airplane_client import Neo4jAirplaneClient

# Initialize client
with Neo4jAirplaneClient(uri, username, password, database) as client:
    # Get all aircraft
    aircraft = client.list_all_aircraft()
    print(f"Total aircraft: {len(aircraft)}")
```

## Common Operations

### List All Aircraft
```python
aircraft_list = client.list_all_aircraft()
for aircraft in aircraft_list:
    print(f"{aircraft.tail_number}: {aircraft.model}")
```

### Get Aircraft by Tail Number
```python
aircraft = client.get_aircraft_by_tail_number("N95040A")
if aircraft:
    print(f"Model: {aircraft.manufacturer} {aircraft.model}")
```

### Get Aircraft Systems
```python
systems = client.get_aircraft_systems("AC1001")
for system in systems:
    print(f"{system.name} ({system.type})")
```

### Get System Components
```python
components = client.get_system_components("SYS_AC1001_001")
for component in components:
    print(f"{component.name} - {component.type}")
```

### Get Complete Aircraft Hierarchy
```python
aircraft_with_parts = client.get_aircraft_with_all_parts("AC1001")
print(f"Systems: {len(aircraft_with_parts.systems)}")
for system in aircraft_with_parts.systems:
    print(f"  {system['name']}: {len(system['components'])} components")
```

### Filter by Manufacturer
```python
boeing_aircraft = client.get_aircraft_by_manufacturer("Boeing")
print(f"Boeing aircraft: {len(boeing_aircraft)}")
```

### Search Components
```python
turbines = client.search_components_by_type("Turbine")
for turbine in turbines:
    print(f"{turbine['aircraft_tail']}: {turbine['component_name']}")
```

## Data Classes

### Aircraft
```python
@dataclass
class Aircraft:
    aircraft_id: str
    tail_number: str
    icao24: str
    model: str
    operator: str
    manufacturer: str
```

### System
```python
@dataclass
class System:
    system_id: str
    name: str
    type: str
    aircraft_id: str
```

### Component
```python
@dataclass
class Component:
    component_id: str
    name: str
    type: str
    system_id: str
```

## Example Output

```
N95040A: Boeing B737-800 (ExampleAir)
├─ CFM56-7B #1 (Engine)
│  ├─ Fan Module (Fan)
│  ├─ Compressor Stage (Compressor)
│  └─ High-Pressure Turbine (Turbine)
└─ Hydraulic System A (Hydraulics)
   ├─ Hydraulic Pump (Pump)
   └─ Reservoir (Tank)
```

## Running Examples

### Simple Example
```bash
python simple_example.py
```

### Full Example (in neo4j_airplane_client.py)
```bash
python neo4j_airplane_client.py
```

## Troubleshooting

### Connection Error
```
Error: Failed to connect to Neo4j
```
**Solution**: Check NEO4J_URI, username, and password

### Authentication Error
```
Error: The client is unauthorized
```
**Solution**: Verify NEO4J_USERNAME and NEO4J_PASSWORD

### Database Not Found
```
Error: Database does not exist
```
**Solution**: Check NEO4J_DATABASE name

### No Data Returned
```
Found 0 aircraft
```
**Solution**: Ensure database contains the aviation schema

## Documentation Files

- **README.md** - Project overview
- **AIRPLANE_CLIENT_README.md** - Complete API documentation
- **NEO4J_DIAGNOSTIC_REPORT.md** - Schema and diagnostics
- **SCHEMA_VISUALIZATION.md** - Visual schema guide
- **MCP_SERVER_SUMMARY.md** - MCP connection details
- **QUICK_REFERENCE.md** - This file

## Database Statistics

- Aircraft: 60
- Systems: 240  
- Components: 960
- Sensors: 480
- Flights: 2,400
- Airports: 36
- Maintenance Events: 900

## Support

For issues or questions:
1. Check NEO4J_DIAGNOSTIC_REPORT.md for schema details
2. Review AIRPLANE_CLIENT_README.md for API documentation
3. Verify database connection and credentials
4. Ensure Neo4j database is running
