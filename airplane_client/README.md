# Airplane Database Client

A simple, well-structured Python client library for interacting with a Neo4j airplane database. This client provides Pydantic models, repository patterns, and parameterized Cypher queries for type-safe, secure database operations.

## Features

- ✅ **Pydantic Models** - Type-safe data classes for all entities
- ✅ **Repository Pattern** - Clean, organized query methods
- ✅ **Parameterized Queries** - Secure Cypher queries to prevent injection
- ✅ **Context Managers** - Proper connection lifecycle management
- ✅ **Integration Tests** - Working pytest tests with testcontainers
- ✅ **Type Hints** - Full type annotations throughout

## Installation

### From Source

```bash
pip install -e .
```

### With Development Dependencies

```bash
pip install -e ".[dev]"
```

## Quick Start

### Basic Usage

```python
from airplane_client import (
    Neo4jConnection,
    AircraftRepository,
    Aircraft
)

# Connect to Neo4j
connection = Neo4jConnection(
    uri="bolt://localhost:7687",
    username="neo4j",
    password="your_password",
    database="neo4j"
)

# Use context manager for automatic cleanup
with connection:
    # Create repository
    aircraft_repo = AircraftRepository(connection)
    
    # Create an aircraft
    aircraft = Aircraft(
        aircraft_id="AC001",
        tail_number="N12345",
        icao24="ABC123",
        model="Boeing 737",
        operator="Example Airlines",
        manufacturer="Boeing"
    )
    created = aircraft_repo.create(aircraft)
    
    # Find aircraft by ID
    found = aircraft_repo.find_by_id("AC001")
    print(f"Found: {found.tail_number} - {found.model}")
    
    # Find all aircraft (with limit)
    all_aircraft = aircraft_repo.find_all(limit=10)
    for ac in all_aircraft:
        print(f"{ac.tail_number}: {ac.model}")
```

### Working with Airports

```python
from airplane_client import AirportRepository, Airport

with connection:
    airport_repo = AirportRepository(connection)
    
    # Create an airport
    airport = Airport(
        airport_id="AP001",
        name="John F. Kennedy International Airport",
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
    print(f"{jfk.name} in {jfk.city}, {jfk.country}")
```

### Working with Flights

```python
from airplane_client import FlightRepository, Flight

with connection:
    flight_repo = FlightRepository(connection)
    
    # Create a flight
    flight = Flight(
        flight_id="FL001",
        flight_number="AA100",
        aircraft_id="AC001",
        operator="Example Airlines",
        origin="JFK",
        destination="LAX",
        scheduled_departure="2024-01-01T10:00:00",
        scheduled_arrival="2024-01-01T13:00:00"
    )
    flight_repo.create(flight)
    
    # Find all flights for a specific aircraft
    flights = flight_repo.find_by_aircraft("AC001", limit=50)
    for f in flights:
        print(f"{f.flight_number}: {f.origin} → {f.destination}")
```

### Working with Maintenance Events

```python
from airplane_client import MaintenanceEventRepository, MaintenanceEvent

with connection:
    maintenance_repo = MaintenanceEventRepository(connection)
    
    # Create a maintenance event
    event = MaintenanceEvent(
        event_id="ME001",
        aircraft_id="AC001",
        system_id="SYS001",
        component_id="COMP001",
        fault="Hydraulic pressure low",
        severity="High",
        reported_at="2024-01-01T14:30:00",
        corrective_action="Replace hydraulic pump"
    )
    maintenance_repo.create(event)
    
    # Find all high-severity events
    critical_events = maintenance_repo.find_by_severity("High", limit=20)
    
    # Find all events for a specific aircraft
    aircraft_events = maintenance_repo.find_by_aircraft("AC001", limit=50)
```

### Working with Systems

```python
from airplane_client import SystemRepository, System

with connection:
    system_repo = SystemRepository(connection)
    
    # Create a system
    system = System(
        system_id="SYS001",
        aircraft_id="AC001",
        name="Hydraulic System A",
        type="Hydraulic"
    )
    system_repo.create(system)
    
    # Find all systems for an aircraft
    systems = system_repo.find_by_aircraft("AC001")
    for sys in systems:
        print(f"{sys.name} ({sys.type})")
```

## Database Schema

The client supports the following entities:

### Core Entities

- **Aircraft** - Aircraft in the fleet (tail number, model, operator, etc.)
- **Airport** - Airports (IATA/ICAO codes, location, etc.)
- **Flight** - Flight records (flight number, origin, destination, schedule)
- **System** - Aircraft systems (hydraulic, electrical, etc.)
- **Component** - Components within systems
- **Sensor** - Sensors monitoring systems
- **MaintenanceEvent** - Maintenance and fault events
- **Delay** - Flight delay records
- **Reading** - Sensor readings (time-series data)

### Relationships

- Aircraft → System (HAS_SYSTEM)
- System → Component (HAS_COMPONENT)
- System → Sensor (HAS_SENSOR)
- Aircraft → Flight (OPERATES_FLIGHT)
- Flight → Airport (DEPARTS_FROM, ARRIVES_AT)
- Flight → Delay (HAS_DELAY)
- MaintenanceEvent → Aircraft (AFFECTS_AIRCRAFT)
- MaintenanceEvent → System (AFFECTS_SYSTEM)
- Component → MaintenanceEvent (HAS_EVENT)

## Testing

The client includes comprehensive integration tests using testcontainers.

### Run All Tests

```bash
pytest
```

### Run Specific Test Class

```bash
pytest tests/test_repository.py::TestAircraftRepository
```

### Run with Verbose Output

```bash
pytest -v
```

## Included Repositories

Currently implemented repositories:

- **AircraftRepository** - CRUD operations for aircraft
- **AirportRepository** - CRUD operations for airports (including IATA lookup)
- **FlightRepository** - CRUD operations for flights (including aircraft lookup)
- **SystemRepository** - CRUD operations for systems (including aircraft lookup)
- **MaintenanceEventRepository** - CRUD for maintenance events (with severity and aircraft filters)

## Security

All Cypher queries use parameterization to prevent injection attacks:

```python
# ✅ Good - Parameterized
query = "MATCH (a:Aircraft {aircraft_id: $aircraft_id}) RETURN a"
session.run(query, aircraft_id=aircraft_id)

# ❌ Bad - String interpolation (never do this!)
query = f"MATCH (a:Aircraft {{aircraft_id: '{aircraft_id}'}}) RETURN a"
```

## Error Handling

The client provides custom exceptions:

- `AirplaneClientError` - Base exception for all errors
- `ConnectionError` - Connection failures
- `QueryError` - Query execution failures
- `NotFoundError` - Entity not found

```python
from airplane_client import QueryError, NotFoundError

try:
    aircraft = aircraft_repo.find_by_id("AC001")
    if aircraft is None:
        raise NotFoundError("Aircraft not found")
except QueryError as e:
    print(f"Database query failed: {e}")
```

## Next Steps

This is a **starting point** for working with the airplane database. Consider extending it with:

1. **Additional Repositories** - Component, Sensor, Delay, Reading repositories
2. **Relationship Management** - Methods to create/query relationships between entities
3. **Advanced Queries** - Complex queries involving multiple entities
4. **Async Support** - Add async/await support for better performance
5. **Caching** - Add caching layer for frequently accessed data
6. **Logging** - Add structured logging for debugging
7. **Retry Logic** - Add retry mechanisms for transient failures
8. **Batch Operations** - Support for bulk creates/updates
9. **Schema Validation** - Validate data against Neo4j constraints
10. **Query Builders** - Fluent API for building complex queries

## Requirements

- Python 3.9+
- Neo4j 5.0+
- Dependencies:
  - `neo4j>=5.13.0` - Neo4j Python driver
  - `pydantic>=2.0.0` - Data validation and settings management
  - `pytest>=7.4.0` (dev) - Testing framework
  - `testcontainers[neo4j]>=3.7.0` (dev) - Integration testing with Docker

## License

This project is provided as-is for demonstration purposes.

## Contributing

This is a basic starting point. Feel free to extend and customize it for your specific needs!
