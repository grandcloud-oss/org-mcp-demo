---
name: neo4j-demo
description: A basic demo agent for testing Neo4j graph database integration with Python MCP server
tools: ['read', 'edit', 'search', 'shell', 'neo4j-python/*']
mcp-servers:
  neo4j-python:
    type: 'local'
    command: 'mcp-neo4j-cypher'
    args: ['--transport', 'stdio', '--namespace', 'neo4j-python']
    env:
      NEO4J_URI: '${COPILOT_MCP_NEO4J_URI}'
      NEO4J_USERNAME: '${COPILOT_MCP_NEO4J_USERNAME}'
      NEO4J_PASSWORD: '${COPILOT_MCP_NEO4J_PASSWORD}'
      NEO4J_DATABASE: '${COPILOT_MCP_NEO4J_DATABASE}'
    tools: ["*"]
---

# Neo4j Demo Agent

A simple agent for testing Neo4j database connectivity and basic Cypher queries.

## What This Agent Does

- Connects to Neo4j databases using a Python-based MCP server
- Helps write and execute basic Cypher queries
- Explores graph database schemas
- Tests database connectivity

## Available Tools

**From MCP Server:**
- `get_neo4j_schema` - Get database schema information
- `read_neo4j_cypher` - Execute read-only Cypher queries
- `write_neo4j_cypher` - Execute write Cypher queries

## Basic Usage

### Check Schema
```cypher
CALL db.labels()
```

### Simple Query
```cypher
MATCH (n)
RETURN n
LIMIT 10
```

### Create Data
```cypher
MERGE (p:Person {name: 'Alice'})
RETURN p
```

## Environment Setup

Configure these variables in GitHub Copilot settings:
- `COPILOT_MCP_NEO4J_URI` - Database connection URI
- `COPILOT_MCP_NEO4J_USERNAME` - Username (usually `neo4j`)
- `COPILOT_MCP_NEO4J_PASSWORD` - Password
- `COPILOT_MCP_NEO4J_DATABASE` - Database name (default: `neo4j`)

## Notes

This is a basic demo agent for testing purposes. The Python MCP server is installed via the workflow in `.github/workflows/copilot-setup-steps.yml`.
