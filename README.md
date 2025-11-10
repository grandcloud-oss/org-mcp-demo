# Neo4j Airplane Data Client

A simple, well-structured Python client library for working with airplane data in Neo4j databases. This client provides a clean starting point with Python best practices, type safety, and repository pattern for managing aircraft, flights, airports, maintenance events, and systems.

## Features

✅ **Type-safe models** - Pydantic models for all entities with full type hints  
✅ **Repository pattern** - Clean CRUD operations for each entity type  
✅ **Parameterized queries** - All Cypher queries use parameters to prevent injection  
✅ **Connection management** - Context manager support for safe resource handling  
✅ **Comprehensive tests** - Integration tests using testcontainers  
✅ **Modern Python** - Follows PEP 621 packaging standards

## Installation

### From source

```bash
# Clone the repository
git clone https://github.com/grandcloud-oss/org-mcp-demo.git
cd org-mcp-demo

# Install the package
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"
```

### Requirements

- Python 3.9 or higher
- Neo4j 5.x database

## Quick Start

### Basic Usage

```python
from neo4j_client import Neo4jConnection, AircraftRepository, Aircraft

# Create connection
connection = Neo4jConnection(
    uri="bolt://localhost:7687",
    username="neo4j",
    password="your_password",
    database="neo4j"
)

# Use context manager for automatic cleanup
with connection:
    with connection.get_session() as session:
        # Create repository
        aircraft_repo = AircraftRepository(session)
        
        # Create a new aircraft
        aircraft = Aircraft(
            aircraft_id="AC001",
            tail_number="N12345",
            icao24="ABC123",
            model="B737-800",
            operator="ExampleAir",
            manufacturer="Boeing"
        )
        
        created = aircraft_repo.create(aircraft)
        print(f"Created aircraft: {created.tail_number}")
        
        # Find aircraft by ID
        found = aircraft_repo.find_by_id("AC001")
        if found:
            print(f"Found: {found.model}")
        
        # Find all aircraft by operator
        fleet = aircraft_repo.find_by_operator("ExampleAir")
        print(f"Fleet size: {len(fleet)}")
```

### Working with Flights

```python
from neo4j_client import FlightRepository, Flight

with connection:
    with connection.get_session() as session:
        flight_repo = FlightRepository(session)
        
        # Create a flight
        flight = Flight(
            flight_id="FL001",
            flight_number="EX100",
            aircraft_id="AC001",
            operator="ExampleAir",
            origin="JFK",
            destination="LAX",
            scheduled_departure="2024-01-15T10:00:00",
            scheduled_arrival="2024-01-15T13:30:00"
        )
        
        flight_repo.create(flight)
        
        # Find flights by route
        jfk_to_lax = flight_repo.find_by_route("JFK", "LAX")
        print(f"Flights on route: {len(jfk_to_lax)}")
        
        # Find all flights for an aircraft
        aircraft_flights = flight_repo.find_by_aircraft("AC001")
        for f in aircraft_flights:
            print(f"{f.flight_number}: {f.origin} → {f.destination}")
```

### Working with Airports

```python
from neo4j_client import AirportRepository, Airport

with connection:
    with connection.get_session() as session:
        airport_repo = AirportRepository(session)
        
        # Create an airport
        airport = Airport(
            airport_id="JFK",
            name="John F. Kennedy International",
            iata="JFK",
            icao="KJFK",
            city="New York",
            country="USA",
            lat=40.6413,
            lon=-73.7781
        )
        
        airport_repo.create(airport)
        
        # Find by IATA code
        jfk = airport_repo.find_by_iata("JFK")
        print(f"{jfk.name} - {jfk.city}, {jfk.country}")
        
        # Find all airports in a country
        us_airports = airport_repo.find_by_country("USA")
        print(f"US airports: {len(us_airports)}")
```

### Working with Maintenance Events

```python
from neo4j_client import MaintenanceEventRepository, MaintenanceEvent

with connection:
    with connection.get_session() as session:
        maint_repo = MaintenanceEventRepository(session)
        
        # Create maintenance event
        event = MaintenanceEvent(
            event_id="ME001",
            aircraft_id="AC001",
            system_id="SYS001",
            component_id="COMP001",
            fault="Hydraulic leak detected",
            severity="High",
            corrective_action="Replace hydraulic line",
            reported_at="2024-01-15T14:30:00"
        )
        
        maint_repo.create(event)
        
        # Find all events for an aircraft
        aircraft_events = maint_repo.find_by_aircraft("AC001")
        for e in aircraft_events:
            print(f"{e.reported_at}: {e.fault} [{e.severity}]")
        
        # Find critical events
        critical = maint_repo.find_by_severity("Critical")
        print(f"Critical events: {len(critical)}")
```

### Working with Systems

```python
from neo4j_client import SystemRepository, System

with connection:
    with connection.get_session() as session:
        system_repo = SystemRepository(session)
        
        # Create system
        system = System(
            system_id="SYS001",
            aircraft_id="AC001",
            name="Hydraulic System",
            type="Hydraulic"
        )
        
        system_repo.create(system)
        
        # Find all systems for an aircraft
        aircraft_systems = system_repo.find_by_aircraft("AC001")
        for s in aircraft_systems:
            print(f"{s.name} ({s.type})")
```

## Data Models

The client includes Pydantic models for the following entities:

### Core Entities (with repositories)

- **Aircraft** - Fleet aircraft with tail numbers, models, and operators
- **Airport** - Airport locations with IATA/ICAO codes and coordinates
- **Flight** - Flight operations with routes and schedules
- **MaintenanceEvent** - Maintenance and fault records
- **System** - Aircraft system components

### Additional Models

- **Component** - System components
- **Sensor** - Sensors within systems
- **Delay** - Flight delay records
- **Reading** - Sensor readings

## Testing

The project includes comprehensive integration tests using pytest and testcontainers.

### Run Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_repository.py

# Run specific test class
pytest tests/test_repository.py::TestAircraftRepository
```

### Test Coverage

Tests cover:
- ✅ CRUD operations for all repository types
- ✅ Query filtering (by ID, operator, route, severity, etc.)
- ✅ Edge cases (not found, duplicates)
- ✅ Error handling (NotFoundError for updates)
- ✅ Connection management

## Schema Overview

The client is designed to work with the following Neo4j schema:

```
Aircraft
├─ HAS_SYSTEM → System
├─ OPERATES_FLIGHT → Flight
└─ AFFECTS_AIRCRAFT ← MaintenanceEvent

Flight
├─ DEPARTS_FROM → Airport
├─ ARRIVES_AT → Airport
└─ HAS_DELAY → Delay

System
├─ HAS_COMPONENT → Component
├─ HAS_SENSOR → Sensor
└─ AFFECTS_SYSTEM ← MaintenanceEvent

Component
└─ HAS_EVENT → MaintenanceEvent

Sensor
└─ (captures) → Reading
```

## Project Structure

```
neo4j_client/
├── __init__.py          # Package exports
├── models.py            # Pydantic data models
├── repository.py        # Repository pattern implementations
├── connection.py        # Connection management
└── exceptions.py        # Custom exceptions

tests/
├── __init__.py
├── conftest.py          # pytest fixtures with testcontainers
└── test_repository.py   # Integration tests

pyproject.toml           # Project configuration (PEP 621)
README.md                # This file
```

## Error Handling

The client provides custom exceptions for different error scenarios:

```python
from neo4j_client import NotFoundError, QueryError, ConnectionError

try:
    aircraft = aircraft_repo.find_by_id("INVALID")
except NotFoundError:
    print("Aircraft not found")
except QueryError as e:
    print(f"Query failed: {e}")
except ConnectionError as e:
    print(f"Connection failed: {e}")
```

## Security Best Practices

✅ **Parameterized queries** - All Cypher queries use named parameters  
✅ **MERGE operations** - Prevents duplicate node creation  
✅ **Input validation** - Pydantic models validate all data  
✅ **No string interpolation** - Eliminates injection risks  
✅ **Context managers** - Ensures proper resource cleanup

## Next Steps

This is a starting point for working with airplane data in Neo4j. Consider extending with:

- **Relationship management** - Methods to create/query relationships between entities
- **Advanced queries** - Complex analytical queries (e.g., flight patterns, maintenance trends)
- **Async support** - Async/await for concurrent operations
- **Caching** - Add caching layer for frequently accessed data
- **Batch operations** - Bulk insert/update capabilities
- **Transaction management** - Explicit transaction control
- **Additional repositories** - Component, Sensor, Delay, and Reading repositories
- **Query builders** - Fluent API for complex queries
- **Monitoring** - Logging and metrics collection

## Environment Variables

For convenience, you can use environment variables:

```bash
export NEO4J_URI="bolt://localhost:7687"
export NEO4J_USERNAME="neo4j"
export NEO4J_PASSWORD="your_password"
export NEO4J_DATABASE="neo4j"
```

Then in your code:

```python
import os
from neo4j_client import Neo4jConnection

connection = Neo4jConnection(
    uri=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD"),
    database=os.getenv("NEO4J_DATABASE", "neo4j")
)
```

## Contributing

This is a basic client designed as a starting point. Feel free to extend it based on your needs:

1. Add new repository methods for your use cases
2. Extend models with additional validation
3. Implement relationship management
4. Add more sophisticated error handling
5. Contribute improvements back to the project

## License

MIT

## Support

For issues or questions, please open an issue on the GitHub repository.
