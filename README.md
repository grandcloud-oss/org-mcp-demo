# org-mcp-demo

A demonstration repository for using Neo4j with the Model Context Protocol (MCP) server in GitHub Copilot.

## Contents

- **airplane_client.py** - Python client for reading airplane and parts data from Neo4j
- **example_queries.py** - Example queries with sample results
- **AIRPLANE_DATA_README.md** - Comprehensive documentation including:
  - Database schema details
  - MCP server diagnostic information
  - Usage examples and troubleshooting

## Quick Start

```bash
# Run the airplane client to see available queries
python3 airplane_client.py

# View example queries with sample results
python3 example_queries.py
```

## Database Overview

The Neo4j database contains aircraft fleet data:
- **60 Aircraft** with manufacturer, model, and operator details
- **240 Systems** including engines, hydraulics, avionics
- **960 Components** - individual parts within each system
- Plus maintenance events, flights, sensors, and more

## MCP Server

This repository uses the `mcp-neo4j-cypher` MCP server for database access. See [AIRPLANE_DATA_README.md](AIRPLANE_DATA_README.md) for full details.
