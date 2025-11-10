# org-mcp-demo

Demo repository for testing Model Context Protocol (MCP) servers with GitHub Copilot.

## Airplane Information Client

This repository contains a Python client for reading airplane information and parts from a Neo4j database using the Neo4j MCP server.

### Quick Start

```bash
# Run the main client (shows all available queries)
python3 airplane_client.py

# Run the example usage (shows how to use with MCP server)
python3 example_usage.py
```

### Features

The airplane client provides queries to:
- List all aircraft in the database (60 aircraft)
- Get detailed information about specific aircraft
- Retrieve systems installed on aircraft (engines, avionics, hydraulics, etc.)
- Query components (parts) for each system
- Access maintenance history and sensor data
- Get flight operations and airport information

### Database Schema

The Neo4j database contains:
- **Aircraft**: 60 nodes (Boeing 737, Airbus A320, Embraer E190, etc.)
- **Systems**: 240 nodes (engines, hydraulic systems, avionics)
- **Components**: 960 nodes (fan modules, pumps, turbines, etc.)
- **Sensors**: 480 nodes (temperature, pressure, vibration monitors)
- **MaintenanceEvents**: 900 nodes (repairs, inspections, replacements)
- **Flights**: 2,400 nodes (flight operations)
- **Airports**: 36 nodes (departure/arrival locations)

### Neo4j MCP Server

The client uses the Neo4j MCP server (`mcp-neo4j-cypher`) which provides:
- `get_neo4j_schema` - Retrieve database schema information
- `read_neo4j_cypher` - Execute read-only Cypher queries
- `write_neo4j_cypher` - Execute write Cypher queries

### Documentation

- **[README_AIRPLANE_CLIENT.md](README_AIRPLANE_CLIENT.md)** - Complete documentation with examples and schema details
- **[airplane_client.py](airplane_client.py)** - Main Python client with all query methods
- **[example_usage.py](example_usage.py)** - Examples showing how to use the client with MCP server

### MCP Server Configuration

The Neo4j MCP server requires the following environment variables:
- `COPILOT_MCP_NEO4J_URI` - Database connection URI
- `COPILOT_MCP_NEO4J_USERNAME` - Username (usually 'neo4j')
- `COPILOT_MCP_NEO4J_PASSWORD` - Password
- `COPILOT_MCP_NEO4J_DATABASE` - Database name (default: 'neo4j')

### Connection Status

✅ **MCP Server**: Successfully connected to `neo4j-python-neo4j-python`  
✅ **Schema Discovery**: Retrieved complete database schema  
✅ **Read Queries**: Successfully queried aircraft and parts data  
✅ **Database Access**: Verified access to airplane database with 60 aircraft

### Installation

The Neo4j MCP server is installed via the GitHub Actions workflow:

```yaml
# .github/workflows/copilot-setup-steps.yml
- name: Install mcp-neo4j-cypher with pip
  run: |
    python3 -m pip install --upgrade pip
    python3 -m pip install mcp-neo4j-cypher
```
