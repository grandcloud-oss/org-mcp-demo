# org-mcp-demo

Demo repository for MCP (Model Context Protocol) server integration with Neo4j.

## Neo4j Airplane Information Client

This repository contains a Python client for querying airplane information and parts from a Neo4j graph database.

### Features

- **Complete Python Client**: Query aircraft, systems, and components from Neo4j
- **MCP Server Integration**: Developed using Neo4j MCP server tools
- **Sample Data**: Aviation data model with 60 aircraft, 240 systems, and 960 components
- **Easy to Use**: Simple API with examples and documentation

### Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Connection**
   
   Set environment variables:
   ```bash
   export NEO4J_URI="bolt://localhost:7687"
   export NEO4J_USERNAME="neo4j"
   export NEO4J_PASSWORD="your-password"
   export NEO4J_DATABASE="neo4j"
   ```

3. **Run Examples**
   ```bash
   python simple_example.py
   ```

### Documentation

- **[AIRPLANE_CLIENT_README.md](AIRPLANE_CLIENT_README.md)** - Complete API documentation and usage examples
- **[NEO4J_DIAGNOSTIC_REPORT.md](NEO4J_DIAGNOSTIC_REPORT.md)** - Database schema and MCP server diagnostic information

### Files

- `neo4j_airplane_client.py` - Main Python client library
- `simple_example.py` - Quick start example with common queries
- `requirements.txt` - Python dependencies
- `NEO4J_DIAGNOSTIC_REPORT.md` - Schema discovery and diagnostic report
- `AIRPLANE_CLIENT_README.md` - Detailed documentation

### Database Schema

The Neo4j database contains:
- **Aircraft**: 60 nodes with manufacturer, model, operator details
- **Systems**: 240 nodes representing aircraft systems (engines, hydraulics, etc.)
- **Components**: 960 nodes representing parts within systems
- **Plus**: Sensors, maintenance events, flights, airports, and more

### Example Usage

```python
from neo4j_airplane_client import Neo4jAirplaneClient

with Neo4jAirplaneClient(uri, username, password, database) as client:
    # Get all aircraft
    aircraft = client.list_all_aircraft()
    
    # Get aircraft with all parts
    details = client.get_aircraft_with_all_parts("AC1001")
    
    # Search for specific components
    turbines = client.search_components_by_type("Turbine")
```

See [AIRPLANE_CLIENT_README.md](AIRPLANE_CLIENT_README.md) for complete documentation.

### MCP Server

This project demonstrates the use of Neo4j MCP (Model Context Protocol) server integration. The schema was discovered and validated using MCP tools without direct database access. See [NEO4J_DIAGNOSTIC_REPORT.md](NEO4J_DIAGNOSTIC_REPORT.md) for details.
