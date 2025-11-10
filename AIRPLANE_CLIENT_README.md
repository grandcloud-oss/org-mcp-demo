# Neo4j Airplane Information Client

A Python client library for querying airplane information and parts from a Neo4j graph database.

## Overview

This project provides a comprehensive Python client (`neo4j_airplane_client.py`) that demonstrates how to interact with a Neo4j database containing aviation data, including aircraft, systems, components, and related information.

## Database Schema

The Neo4j database contains an aviation data model with the following structure:

### Node Types
- **Aircraft** (60 nodes): Basic aircraft information
- **System** (240 nodes): Aircraft systems (engines, hydraulics, avionics, etc.)
- **Component** (960 nodes): Parts that make up each system
- **Sensor** (480 nodes): Monitoring sensors
- **MaintenanceEvent** (900 nodes): Maintenance history
- **Flight** (2,400 nodes): Flight operations
- **Airport** (36 nodes): Airport information
- **Delay** (1,542 nodes): Flight delay data
- **Reading** (1,036,800 nodes): Sensor readings

### Key Relationships
- `Aircraft -[:HAS_SYSTEM]-> System`
- `System -[:HAS_COMPONENT]-> Component`
- `System -[:HAS_SENSOR]-> Sensor`
- `Aircraft -[:OPERATES_FLIGHT]-> Flight`
- `Component -[:HAS_EVENT]-> MaintenanceEvent`

See [NEO4J_DIAGNOSTIC_REPORT.md](NEO4J_DIAGNOSTIC_REPORT.md) for complete schema details.

## Installation

### Prerequisites
- Python 3.7 or higher
- Access to a Neo4j database (local or cloud)
- Neo4j Python driver

### Install Dependencies

```bash
pip install neo4j
```

## Configuration

Update the connection parameters in the `main()` function of `neo4j_airplane_client.py`:

```python
NEO4J_URI = "bolt://localhost:7687"  # Your Neo4j URI
NEO4J_USERNAME = "neo4j"              # Your username
NEO4J_PASSWORD = "your-password"      # Your password
NEO4J_DATABASE = "neo4j"              # Database name
```

### Environment Variables (Alternative)

You can also use environment variables:

```bash
export NEO4J_URI="bolt://localhost:7687"
export NEO4J_USERNAME="neo4j"
export NEO4J_PASSWORD="your-password"
export NEO4J_DATABASE="neo4j"
```

Then modify the client initialization:

```python
import os

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")
```

## Usage

### Running the Example

```bash
python neo4j_airplane_client.py
```

This will run all the example queries and display results.

### Using as a Library

```python
from neo4j_airplane_client import Neo4jAirplaneClient

# Initialize client (with context manager for automatic cleanup)
with Neo4jAirplaneClient(uri, username, password, database) as client:
    
    # Get all aircraft
    aircraft_list = client.list_all_aircraft()
    for aircraft in aircraft_list:
        print(f"{aircraft.tail_number}: {aircraft.model}")
    
    # Get specific aircraft by tail number
    aircraft = client.get_aircraft_by_tail_number("N95040A")
    print(f"Found: {aircraft.manufacturer} {aircraft.model}")
    
    # Get all systems for an aircraft
    systems = client.get_aircraft_systems(aircraft.aircraft_id)
    for system in systems:
        print(f"System: {system.name} ({system.type})")
    
    # Get components for a specific system
    components = client.get_system_components(systems[0].system_id)
    for component in components:
        print(f"Component: {component.name} ({component.type})")
```

## API Reference

### Class: `Neo4jAirplaneClient`

#### Methods

##### `__init__(uri, username, password, database="neo4j")`
Initialize the client with database connection parameters.

##### `list_all_aircraft() -> List[Aircraft]`
Retrieve all aircraft from the database.

**Returns:** List of `Aircraft` objects

**Example:**
```python
aircraft_list = client.list_all_aircraft()
```

##### `get_aircraft_by_tail_number(tail_number: str) -> Optional[Aircraft]`
Get aircraft information by tail number.

**Parameters:**
- `tail_number`: Aircraft tail number (e.g., 'N95040A')

**Returns:** `Aircraft` object if found, `None` otherwise

**Example:**
```python
aircraft = client.get_aircraft_by_tail_number("N95040A")
```

##### `get_aircraft_systems(aircraft_id: str) -> List[System]`
Get all systems for a specific aircraft.

**Parameters:**
- `aircraft_id`: Aircraft ID (e.g., 'AC1001')

**Returns:** List of `System` objects

**Example:**
```python
systems = client.get_aircraft_systems("AC1001")
```

##### `get_system_components(system_id: str) -> List[Component]`
Get all components for a specific system.

**Parameters:**
- `system_id`: System ID

**Returns:** List of `Component` objects

**Example:**
```python
components = client.get_system_components("SYS_AC1001_001")
```

##### `get_aircraft_with_all_parts(aircraft_id: str) -> Optional[AircraftWithParts]`
Get complete aircraft information including all systems and their components.

**Parameters:**
- `aircraft_id`: Aircraft ID (e.g., 'AC1001')

**Returns:** `AircraftWithParts` object with complete hierarchy

**Example:**
```python
aircraft_with_parts = client.get_aircraft_with_all_parts("AC1001")
print(f"Aircraft has {len(aircraft_with_parts.systems)} systems")
```

##### `get_aircraft_by_manufacturer(manufacturer: str) -> List[Aircraft]`
Get all aircraft from a specific manufacturer.

**Parameters:**
- `manufacturer`: Manufacturer name (e.g., 'Boeing', 'Airbus')

**Returns:** List of `Aircraft` objects

**Example:**
```python
boeing_aircraft = client.get_aircraft_by_manufacturer("Boeing")
```

##### `search_components_by_type(component_type: str) -> List[Dict]`
Search for components by type across all aircraft.

**Parameters:**
- `component_type`: Component type (e.g., 'Fan', 'Turbine', 'Compressor')

**Returns:** List of dictionaries with component and associated aircraft info

**Example:**
```python
fans = client.search_components_by_type("Fan")
```

### Data Classes

#### `Aircraft`
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

#### `System`
```python
@dataclass
class System:
    system_id: str
    name: str
    type: str
    aircraft_id: str
```

#### `Component`
```python
@dataclass
class Component:
    component_id: str
    name: str
    type: str
    system_id: str
```

#### `AircraftWithParts`
```python
@dataclass
class AircraftWithParts:
    aircraft: Aircraft
    systems: List[Dict]  # List of systems with their components
```

## Example Queries

### 1. List All Aircraft

```python
aircraft_list = client.list_all_aircraft()
for aircraft in aircraft_list:
    print(f"{aircraft.tail_number}: {aircraft.manufacturer} {aircraft.model}")
```

**Output:**
```
N95040A: Boeing B737-800
N30268B: Airbus A320-200
N54980C: Airbus A321neo
...
```

### 2. Get Aircraft Details with All Parts

```python
aircraft_with_parts = client.get_aircraft_with_all_parts("AC1001")
print(f"Aircraft: {aircraft_with_parts.aircraft.tail_number}")
print(f"Model: {aircraft_with_parts.aircraft.model}")
print(f"Number of systems: {len(aircraft_with_parts.systems)}")

for system in aircraft_with_parts.systems:
    print(f"\nSystem: {system['name']}")
    print(f"Components: {len(system['components'])}")
    for component in system['components']:
        print(f"  - {component['name']} ({component['type']})")
```

**Output:**
```
Aircraft: N95040A
Model: B737-800
Number of systems: 4

System: CFM56-7B #1
Components: 8
  - Fan Module (Fan)
  - Compressor Stage (Compressor)
  - High-Pressure Turbine (Turbine)
  - Main Fuel Pump (FuelPump)
  ...
```

### 3. Search for Specific Component Types

```python
turbines = client.search_components_by_type("Turbine")
print(f"Found {len(turbines)} turbine components:")
for turbine in turbines:
    print(f"{turbine['aircraft_tail']} - {turbine['system_name']}: {turbine['component_name']}")
```

### 4. Filter Aircraft by Manufacturer

```python
airbus_aircraft = client.get_aircraft_by_manufacturer("Airbus")
boeing_aircraft = client.get_aircraft_by_manufacturer("Boeing")

print(f"Airbus: {len(airbus_aircraft)} aircraft")
print(f"Boeing: {len(boeing_aircraft)} aircraft")
```

## MCP Server Integration

This project was developed using the Neo4j MCP (Model Context Protocol) server integration. The diagnostic report in [NEO4J_DIAGNOSTIC_REPORT.md](NEO4J_DIAGNOSTIC_REPORT.md) shows how the schema was discovered using MCP tools.

### MCP Tools Used
- `neo4j-local-neo4j-local-get_neo4j_schema`: Retrieve database schema
- `neo4j-local-neo4j-local-read_neo4j_cypher`: Execute read queries
- `neo4j-local-neo4j-local-write_neo4j_cypher`: Execute write queries

## Error Handling

The client includes basic error handling. For production use, consider adding:

```python
try:
    aircraft = client.get_aircraft_by_tail_number("N95040A")
    if aircraft:
        print(f"Found: {aircraft.model}")
    else:
        print("Aircraft not found")
except Exception as e:
    print(f"Error querying database: {e}")
```

## Testing

To verify the client is working:

1. Ensure Neo4j is running and accessible
2. Update connection parameters
3. Run the example script:
   ```bash
   python neo4j_airplane_client.py
   ```

## Limitations

- The client currently supports read operations only
- Limited error handling for production use
- No connection pooling or retry logic
- Examples use a simplified data model

## Contributing

Feel free to extend this client with additional functionality:
- Add write operations (create/update aircraft)
- Implement maintenance event queries
- Add sensor data retrieval
- Include flight operations queries
- Add aggregation and analytics methods

## License

This is a demonstration project for educational purposes.

## Additional Resources

- [Neo4j Python Driver Documentation](https://neo4j.com/docs/python-manual/current/)
- [Cypher Query Language Reference](https://neo4j.com/docs/cypher-manual/current/)
- [Neo4j Graph Database Documentation](https://neo4j.com/docs/)
