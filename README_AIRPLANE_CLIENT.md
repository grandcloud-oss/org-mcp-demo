# Airplane Information Reader - Neo4j Client

A Python client for reading airplane information and parts from a Neo4j database using the Model Context Protocol (MCP) server.

## Overview

This client demonstrates how to query airplane data from a Neo4j graph database through the Neo4j MCP server. The database contains information about:
- **Aircraft**: Fleet of 60 aircraft with details like tail number, model, manufacturer
- **Systems**: 240 systems installed on aircraft (engines, avionics, hydraulics, etc.)
- **Components**: 960 individual parts/components that make up the systems
- **Sensors**: 480 sensors monitoring system performance
- **Maintenance Events**: 900 maintenance and repair records
- **Flights**: 2,400 flight operations
- **Airports**: 36 airports for flight operations

## Database Schema

### Node Types

1. **Aircraft**
   - Properties: `aircraft_id`, `tail_number`, `icao24`, `model`, `operator`, `manufacturer`
   - Example: Boeing 737-800, Airbus A320-200

2. **System**
   - Properties: `system_id`, `name`, `type`, `aircraft_id`
   - Examples: CFM56-7B engines, APU systems, hydraulic systems

3. **Component**
   - Properties: `component_id`, `name`, `type`, `system_id`
   - Examples: Fan modules, compressor stages, fuel pumps

4. **Sensor**
   - Properties: `sensor_id`, `name`, `type`, `unit`, `system_id`
   - Monitors temperature, pressure, vibration, etc.

5. **MaintenanceEvent**
   - Properties: `event_id`, `fault`, `severity`, `corrective_action`, `reported_at`

6. **Flight**
   - Properties: `flight_id`, `flight_number`, `origin`, `destination`, `operator`

7. **Airport**
   - Properties: `airport_id`, `iata`, `icao`, `name`, `city`, `country`

### Relationships

```
Aircraft -[:HAS_SYSTEM]-> System
System -[:HAS_COMPONENT]-> Component
System -[:HAS_SENSOR]-> Sensor
Component -[:HAS_EVENT]-> MaintenanceEvent
MaintenanceEvent -[:AFFECTS_AIRCRAFT]-> Aircraft
MaintenanceEvent -[:AFFECTS_SYSTEM]-> System
Aircraft -[:OPERATES_FLIGHT]-> Flight
Flight -[:DEPARTS_FROM]-> Airport
Flight -[:ARRIVES_AT]-> Airport
```

## MCP Server Configuration

### Environment Variables Required

The Neo4j MCP server requires the following environment variables to be configured:

```bash
COPILOT_MCP_NEO4J_URI=neo4j://your-server:7687
COPILOT_MCP_NEO4J_USERNAME=neo4j
COPILOT_MCP_NEO4J_PASSWORD=your-password
COPILOT_MCP_NEO4J_DATABASE=neo4j
```

### MCP Server Tools Available

The following tools are available through the Neo4j MCP server:

1. **get_neo4j_schema** - Retrieve database schema information
2. **read_neo4j_cypher** - Execute read-only Cypher queries
3. **write_neo4j_cypher** - Execute write Cypher queries

### Connection Verification

During development, the MCP server connection was successfully verified with the following results:

- ✅ MCP Server: `neo4j-python-neo4j-python`
- ✅ Schema Discovery: Successfully retrieved schema for 13 node/relationship types
- ✅ Read Queries: Successfully executed sample queries
- ✅ Database Access: Confirmed access to airplane database with 60 aircraft

## Usage

### Running the Client

```bash
python3 airplane_client.py
```

This will display:
1. Database schema information
2. Usage demonstration with example queries
3. Complete query guide

### Using the Client in Your Code

```python
from airplane_client import AirplaneClient

# Create client instance
client = AirplaneClient()

# Get query for listing all aircraft
query = client.list_all_aircraft()
# Execute via MCP server: read_neo4j_cypher(query=query)

# Get query for specific aircraft details
query = client.get_aircraft_info("AC1001")
# Execute via MCP server: read_neo4j_cypher(query=query, params={'aircraft_id': 'AC1001'})

# Get all parts for an aircraft
query = client.get_all_aircraft_parts("AC1001")
# Execute via MCP server: read_neo4j_cypher(query=query, params={'aircraft_id': 'AC1001'})
```

## Example Queries

### 1. List All Aircraft

```cypher
MATCH (a:Aircraft)
RETURN a.aircraft_id as aircraft_id,
       a.tail_number as tail_number,
       a.model as model,
       a.operator as operator,
       a.manufacturer as manufacturer
ORDER BY a.aircraft_id
```

**Sample Results:**
```json
[
  {
    "aircraft_id": "AC1001",
    "tail_number": "N95040A",
    "model": "B737-800",
    "operator": "ExampleAir",
    "manufacturer": "Boeing"
  },
  {
    "aircraft_id": "AC1002",
    "tail_number": "N30268B",
    "model": "A320-200",
    "operator": "SkyWays",
    "manufacturer": "Airbus"
  }
]
```

### 2. Get Aircraft Systems

```cypher
MATCH (a:Aircraft {aircraft_id: $aircraft_id})-[:HAS_SYSTEM]->(s:System)
RETURN s.system_id as system_id,
       s.name as name,
       s.type as type
ORDER BY s.name
```

**Parameters:** `{'aircraft_id': 'AC1001'}`

### 3. Get All Aircraft Parts

```cypher
MATCH (a:Aircraft {aircraft_id: $aircraft_id})-[:HAS_SYSTEM]->(s:System)-[:HAS_COMPONENT]->(c:Component)
RETURN s.name as system_name,
       c.name as component_name,
       c.type as component_type
ORDER BY s.name, c.name
```

**Parameters:** `{'aircraft_id': 'AC1001'}`

**Sample Results:**
```json
[
  {
    "system_name": "CFM56-7B #1",
    "component_name": "Fan Module",
    "component_type": "Fan"
  },
  {
    "system_name": "CFM56-7B #1",
    "component_name": "Compressor Stage",
    "component_type": "Compressor"
  },
  {
    "system_name": "CFM56-7B #1",
    "component_name": "High-Pressure Turbine",
    "component_type": "Turbine"
  }
]
```

### 4. Get Maintenance History

```cypher
MATCH (a:Aircraft {aircraft_id: $aircraft_id})<-[:AFFECTS_AIRCRAFT]-(m:MaintenanceEvent)
RETURN m.event_id as event_id,
       m.fault as fault,
       m.severity as severity,
       m.corrective_action as corrective_action,
       m.reported_at as reported_at
ORDER BY m.reported_at DESC
LIMIT $limit
```

**Parameters:** `{'aircraft_id': 'AC1001', 'limit': 5}`

### 5. Get Aircraft Statistics

```cypher
MATCH (a:Aircraft {aircraft_id: $aircraft_id})
OPTIONAL MATCH (a)-[:HAS_SYSTEM]->(s:System)
OPTIONAL MATCH (s)-[:HAS_COMPONENT]->(c:Component)
OPTIONAL MATCH (a)<-[:AFFECTS_AIRCRAFT]-(m:MaintenanceEvent)
RETURN a.aircraft_id as aircraft_id,
       COUNT(DISTINCT s) as system_count,
       COUNT(DISTINCT c) as component_count,
       COUNT(DISTINCT m) as maintenance_event_count
```

**Parameters:** `{'aircraft_id': 'AC1001'}`

## Integration with MCP Server

To execute these queries through the Neo4j MCP server, use the provided tools:

```python
# Using the MCP server read tool
result = read_neo4j_cypher(
    query=client.list_all_aircraft()
)

# With parameters
result = read_neo4j_cypher(
    query=client.get_aircraft_info("AC1001"),
    params={'aircraft_id': 'AC1001'}
)
```

## Diagnostic Information

### MCP Server Details

- **MCP Server Name**: `neo4j-python-neo4j-python`
- **Available Tools**:
  - `neo4j-python-neo4j-python-get_neo4j_schema`
  - `neo4j-python-neo4j-python-read_neo4j_cypher`
  - `neo4j-python-neo4j-python-write_neo4j_cypher`

### Installation

The Neo4j MCP server is installed via the GitHub Actions workflow defined in `.github/workflows/copilot-setup-steps.yml`:

```yaml
- name: Install mcp-neo4j-cypher with pip
  run: |
    python3 -m pip install --upgrade pip
    python3 -m pip install mcp-neo4j-cypher
```

### Connection Status

✅ **Connection Successful** - The MCP server successfully connected to the Neo4j database and retrieved:
- Complete schema with 13 entity types
- Sample aircraft data (60 aircraft)
- Hierarchical data (systems → components)
- Maintenance and operational data

### Troubleshooting

If you encounter MCP server errors:

1. **Verify Environment Variables**: Ensure all required environment variables are set
2. **Check MCP Server Installation**: Verify `mcp-neo4j-cypher` is installed
3. **Test Connection**: Use `get_neo4j_schema` tool to verify database access
4. **Review Logs**: Check GitHub Actions logs for any connection errors

## Files

- `airplane_client.py` - Main Python client with query methods and documentation
- `README_AIRPLANE_CLIENT.md` - This documentation file
- `.github/workflows/copilot-setup-steps.yml` - MCP server installation workflow

## License

This is a demonstration project for testing Neo4j MCP server connectivity.

## Notes

- This client is designed as a reference implementation showing the structure of queries needed to access airplane data
- All queries are read-only and safe to execute
- The client does not connect directly to Neo4j but uses the MCP server infrastructure
- Sample data was successfully verified during development

## Sample Aircraft in Database

The database contains various aircraft models including:
- Boeing 737-800
- Airbus A320-200
- Airbus A321neo
- Embraer E190

Each aircraft has complete system hierarchies with engines, hydraulics, avionics, and other critical systems, along with their constituent components and sensors.
