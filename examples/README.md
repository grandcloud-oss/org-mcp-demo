# Examples

This directory contains example scripts demonstrating how to use the Neo4j airplane data client.

## demo.py

A comprehensive demonstration script that shows how to:

- Connect to a Neo4j database
- Query aircraft by various criteria
- Find airports and flights
- Search for maintenance events
- Retrieve aircraft systems

### Running the Demo

1. Set the required environment variables:

```bash
export NEO4J_URI="bolt://localhost:7687"
export NEO4J_USERNAME="neo4j"
export NEO4J_PASSWORD="your_password"
export NEO4J_DATABASE="neo4j"
```

2. Run the demo:

```bash
python examples/demo.py
```

### Expected Output

The demo will display:
- Total aircraft count with sample listings
- Fleet information by operator
- Airport listings
- Flight information and routes
- Maintenance events by severity
- Aircraft system information

## Additional Examples

You can create your own scripts by following this pattern:

```python
import os
from neo4j_client import Neo4jConnection, AircraftRepository

# Get credentials from environment
uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
username = os.getenv("NEO4J_USERNAME", "neo4j")
password = os.getenv("NEO4J_PASSWORD")
database = os.getenv("NEO4J_DATABASE", "neo4j")

# Use connection context manager
with Neo4jConnection(uri, username, password, database) as connection:
    with connection.get_session() as session:
        # Create repository and query data
        repo = AircraftRepository(session)
        aircraft = repo.find_all()
        
        for a in aircraft:
            print(f"{a.tail_number} - {a.model}")
```
