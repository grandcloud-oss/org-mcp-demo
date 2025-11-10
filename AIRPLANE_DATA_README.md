# Neo4j MCP Server - Airplane Data Client

## Overview

This repository contains a Python client for reading airplane information and parts data from a Neo4j graph database using the Model Context Protocol (MCP) server integration.

## MCP Server Diagnostic Information

### Connection Details

**MCP Server**: `neo4j-python` MCP server  
**Tools Available**:
- `neo4j-python-neo4j-python-get_neo4j_schema` - Get database schema
- `neo4j-python-neo4j-python-read_neo4j_cypher` - Execute read-only Cypher queries
- `neo4j-python-neo4j-python-write_neo4j_cypher` - Execute write Cypher queries

### Environment Configuration

The MCP server requires the following environment variables (configured in GitHub Copilot settings):

```
COPILOT_MCP_NEO4J_URI - Database connection URI
COPILOT_MCP_NEO4J_USERNAME - Database username (typically 'neo4j')
COPILOT_MCP_NEO4J_PASSWORD - Database password
COPILOT_MCP_NEO4J_DATABASE - Database name (default: 'neo4j')
```

### Installation

The MCP server is installed via the GitHub Actions workflow defined in `.github/workflows/copilot-setup-steps.yml`:

```yaml
- name: Install mcp-neo4j-cypher with pip
  run: |
    python3 -m pip install --upgrade pip
    python3 -m pip install mcp-neo4j-cypher
```

## Database Schema

The Neo4j database contains aircraft-related data with the following structure:

### Node Types

1. **Aircraft** (60 nodes)
   - Properties: `aircraft_id`, `tail_number`, `model`, `manufacturer`, `operator`, `icao24`
   - Represents individual airplanes in the fleet

2. **System** (240 nodes)
   - Properties: `system_id`, `name`, `type`, `aircraft_id`
   - Represents aircraft systems (engines, hydraulics, avionics, etc.)

3. **Component** (960 nodes)
   - Properties: `component_id`, `name`, `type`, `system_id`
   - Represents parts/components within systems

4. **MaintenanceEvent** (900 nodes)
   - Properties: `event_id`, `aircraft_id`, `component_id`, `system_id`, `fault`, `severity`, `corrective_action`, `reported_at`
   - Tracks maintenance events and issues

5. **Flight** (2,400 nodes)
   - Properties: `flight_id`, `flight_number`, `aircraft_id`, `origin`, `destination`, `operator`, `scheduled_departure`, `scheduled_arrival`
   - Represents flight operations

6. **Airport** (36 nodes)
   - Properties: `airport_id`, `name`, `iata`, `icao`, `city`, `country`, `lat`, `lon`
   - Airport information

7. **Sensor** (480 nodes)
   - Properties: `sensor_id`, `name`, `type`, `unit`, `system_id`
   - Sensors monitoring aircraft systems

8. **Reading** (1,036,800 nodes)
   - Properties: `reading_id`, `sensor_id`, `timestamp`, `value`
   - Sensor readings over time

9. **Delay** (1,542 nodes)
   - Properties: `delay_id`, `flight_id`, `cause`, `minutes`
   - Flight delay information

### Relationships

- `AFFECTS_AIRCRAFT` - MaintenanceEvent → Aircraft (4,200 relationships)
- `AFFECTS_SYSTEM` - MaintenanceEvent → System (4,200 relationships)
- `ARRIVES_AT` - Flight → Airport (11,200 relationships)
- `DEPARTS_FROM` - Flight → Airport (11,200 relationships)
- `HAS_COMPONENT` - System → Component (4,480 relationships)
- `HAS_DELAY` - Flight → Delay (7,196 relationships)
- `HAS_EVENT` - Component → MaintenanceEvent (4,200 relationships)
- `HAS_SENSOR` - System → Sensor (2,240 relationships)
- `HAS_SYSTEM` - Aircraft → System (1,120 relationships)
- `OPERATES_FLIGHT` - Aircraft → Flight (11,200 relationships)

## Sample Data

### Aircraft Examples

```json
{
  "aircraft_id": "AC1001",
  "tail_number": "N95040A",
  "model": "B737-800",
  "manufacturer": "Boeing",
  "operator": "ExampleAir"
}
```

### System Examples

```json
{
  "system_id": "AC1001-S01",
  "name": "CFM56-7B #1",
  "type": "Engine",
  "aircraft_id": "AC1001"
}
```

### Component Examples

```json
[
  {
    "component_id": "AC1001-S01-C01",
    "name": "Fan Module",
    "type": "Fan",
    "system_id": "AC1001-S01"
  },
  {
    "component_id": "AC1001-S01-C02",
    "name": "Compressor Stage",
    "type": "Compressor",
    "system_id": "AC1001-S01"
  },
  {
    "component_id": "AC1001-S01-C03",
    "name": "High-Pressure Turbine",
    "type": "Turbine",
    "system_id": "AC1001-S01"
  },
  {
    "component_id": "AC1001-S01-C04",
    "name": "Main Fuel Pump",
    "type": "FuelPump",
    "system_id": "AC1001-S01"
  },
  {
    "component_id": "AC1001-S01-C05",
    "name": "Thrust Bearing",
    "type": "Bearing",
    "system_id": "AC1001-S01"
  }
]
```

## Usage

### Running the Python Client

```bash
python airplane_client.py
```

This will display:
1. Database schema information
2. Example Cypher queries for various use cases
3. Query parameters
4. Usage instructions

### Example Queries

#### 1. Get All Aircraft

```cypher
MATCH (a:Aircraft)
RETURN a.aircraft_id as aircraft_id, 
       a.tail_number as tail_number, 
       a.model as model,
       a.manufacturer as manufacturer, 
       a.operator as operator, 
       a.icao24 as icao24
LIMIT 10
```

#### 2. Get Aircraft with Systems

```cypher
MATCH (a:Aircraft)-[:HAS_SYSTEM]->(s:System)
RETURN a.aircraft_id as aircraft_id, 
       a.tail_number as tail_number, 
       a.model as model,
       a.manufacturer as manufacturer,
       a.operator as operator,
       s.system_id as system_id, 
       s.name as system_name, 
       s.type as system_type
LIMIT 20
```

#### 3. Get Aircraft Parts/Components

```cypher
MATCH (a:Aircraft)-[:HAS_SYSTEM]->(s:System)-[:HAS_COMPONENT]->(c:Component)
RETURN a.aircraft_id as aircraft_id, 
       a.tail_number as tail_number, 
       a.model as model,
       a.manufacturer as manufacturer,
       s.system_id as system_id, 
       s.name as system_name, 
       s.type as system_type,
       c.component_id as component_id, 
       c.name as component_name, 
       c.type as component_type
LIMIT 50
```

#### 4. Get Specific Aircraft Parts

```cypher
MATCH (a:Aircraft)-[:HAS_SYSTEM]->(s:System)-[:HAS_COMPONENT]->(c:Component)
WHERE a.aircraft_id = 'AC1001'
RETURN a.aircraft_id as aircraft_id, 
       a.tail_number as tail_number, 
       s.system_id as system_id, 
       s.name as system_name,
       c.component_id as component_id, 
       c.name as component_name, 
       c.type as component_type
LIMIT 50
```

#### 5. Get Engine Parts Only

```cypher
MATCH (a:Aircraft)-[:HAS_SYSTEM]->(s:System)-[:HAS_COMPONENT]->(c:Component)
WHERE s.type = 'Engine'
RETURN a.aircraft_id as aircraft_id, 
       a.tail_number as tail_number,
       s.system_id as system_id, 
       s.name as system_name,
       c.component_id as component_id, 
       c.name as component_name, 
       c.type as component_type
LIMIT 50
```

### Using with MCP Tools

The client demonstrates query structures that can be executed using the MCP tools:

```python
# Example: Get schema
neo4j-python-neo4j-python-get_neo4j_schema(sample_size=1000)

# Example: Execute read query
neo4j-python-neo4j-python-read_neo4j_cypher(
    query="MATCH (a:Aircraft) RETURN a LIMIT 10",
    params={}
)
```

## Python Client API

The `AirplaneClient` class provides the following methods:

### `get_database_schema()`
Returns information about the database schema structure.

### `get_all_aircraft(limit=10)`
Retrieves basic information about all aircraft.

### `get_aircraft_with_systems(aircraft_id=None, limit=20)`
Retrieves aircraft along with their systems. Optionally filter by aircraft_id.

### `get_aircraft_parts(aircraft_id=None, system_type=None, limit=50)`
Retrieves aircraft parts/components with optional filtering by aircraft and system type.

### `get_component_details(component_id)`
Retrieves detailed information about a specific component including maintenance history.

### `get_aircraft_by_manufacturer(manufacturer, limit=10)`
Retrieves aircraft filtered by manufacturer (e.g., 'Boeing', 'Airbus').

### `get_system_components_count()`
Returns a count of components per system type.

## MCP Server Verification

The Neo4j MCP server was successfully verified with the following checks:

✅ **Schema Discovery**: Successfully retrieved database schema using `get_neo4j_schema`  
✅ **Read Queries**: Successfully executed Cypher read queries  
✅ **Data Retrieval**: Successfully retrieved airplane and parts data  
✅ **Relationship Traversal**: Successfully navigated Aircraft → System → Component relationships

## Troubleshooting

### If MCP Server Connection Fails

1. Verify environment variables are set in GitHub Copilot settings:
   - `COPILOT_MCP_NEO4J_URI`
   - `COPILOT_MCP_NEO4J_USERNAME`
   - `COPILOT_MCP_NEO4J_PASSWORD`
   - `COPILOT_MCP_NEO4J_DATABASE`

2. Check that `mcp-neo4j-cypher` is installed:
   ```bash
   pip list | grep mcp-neo4j-cypher
   ```

3. Verify the workflow ran successfully in `.github/workflows/copilot-setup-steps.yml`

4. Test MCP tools are available:
   - Try calling `neo4j-python-neo4j-python-get_neo4j_schema`
   - Check for any error messages in the response

### Common Issues

- **Connection timeout**: Check Neo4j database is running and accessible
- **Authentication errors**: Verify username and password are correct
- **Schema not found**: Ensure database contains data and is not empty
- **Query errors**: Validate Cypher syntax and parameter types

## Development

### Requirements

- Python 3.11+
- `mcp-neo4j-cypher` package
- Access to Neo4j database via MCP server configuration

### Project Structure

```
org-mcp-demo/
├── .github/
│   └── workflows/
│       └── copilot-setup-steps.yml  # MCP server installation
├── airplane_client.py                # Python client implementation
├── AIRPLANE_DATA_README.md          # This documentation
└── README.md                         # Repository readme
```

## License

This is a demo project for testing Neo4j MCP server integration with GitHub Copilot.

## Support

For issues with:
- **MCP Server**: Check GitHub Copilot MCP documentation
- **Neo4j Database**: Refer to Neo4j documentation
- **This Client**: Review this documentation and example queries
