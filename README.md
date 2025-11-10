# Neo4j Airplane Data Client

A simple, type-safe Python client library for working with airplane data stored in a Neo4j database. This client provides Pydantic-based models and repository pattern implementations for easy data access.

## Features

- ✅ **Type-safe models** using Pydantic for all entities
- ✅ **Repository pattern** for clean data access
- ✅ **Parameterized Cypher queries** for security
- ✅ **Comprehensive test coverage** with pytest and testcontainers
- ✅ **Simple API** - easy to understand and extend
- ✅ **Context manager support** for connection management

## Supported Entities

Based on the Neo4j database schema, this client supports the following entities:

- **Aircraft** - Aircraft information (tail number, model, manufacturer, operator)
- **Flight** - Flight schedules and operations
- **Airport** - Airport details with IATA/ICAO codes and coordinates
- **MaintenanceEvent** - Aircraft maintenance records
- **System** - Aircraft systems
- **Component** - System components
- **Sensor** - Monitoring sensors
- **Delay** - Flight delays with causes
- **Reading** - Sensor readings (1M+ records)

## Database Schema Overview

The database contains:
- 60 Aircraft nodes
- 2,400 Flight nodes
- 36 Airport nodes
- 900 MaintenanceEvent nodes
- 240 System nodes
- 960 Component nodes
- 480 Sensor nodes
- 1,542 Delay nodes
- 1,036,800+ Reading nodes

## Installation

```bash
# Install the package
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"
```

## Quick Start

### Basic Usage

```python
from neo4j_client import Neo4jConnection, AircraftRepository

# Connect to Neo4j
with Neo4jConnection(
    uri="bolt://localhost:7687",
    username="neo4j",
    password="your_password"
) as conn:
    # Create a session
    session = conn.get_session()
    
    # Use a repository
    aircraft_repo = AircraftRepository(session)
    
    # Find all aircraft
    aircraft_list = aircraft_repo.find_all()
    for aircraft in aircraft_list:
        print(f"{aircraft.tail_number}: {aircraft.model}")
    
    session.close()
```

### Working with Aircraft

```python
from neo4j_client import Neo4jConnection, AircraftRepository, Aircraft

with Neo4jConnection(
    uri="bolt://localhost:7687",
    username="neo4j",
    password="your_password"
) as conn:
    session = conn.get_session()
    aircraft_repo = AircraftRepository(session)
    
    # Find a specific aircraft
    aircraft = aircraft_repo.find_by_tail_number("N95040A")
    if aircraft:
        print(f"Found: {aircraft.model} operated by {aircraft.operator}")
    
    # Find aircraft by operator
    skyways_aircraft = aircraft_repo.find_by_operator("SkyWays")
    print(f"SkyWays has {len(skyways_aircraft)} aircraft")
    
    # Create a new aircraft
    new_aircraft = Aircraft(
        aircraft_id="AC9999",
        tail_number="N12345",
        icao24="abc123",
        model="B737-800",
        operator="TestAir",
        manufacturer="Boeing"
    )
    created = aircraft_repo.create(new_aircraft)
    
    session.close()
```

### Working with Flights

```python
from neo4j_client import FlightRepository

with Neo4jConnection(
    uri="bolt://localhost:7687",
    username="neo4j",
    password="your_password"
) as conn:
    session = conn.get_session()
    flight_repo = FlightRepository(session)
    
    # Find flights on a route
    jfk_to_lax = flight_repo.find_by_route("JFK", "LAX")
    print(f"Found {len(jfk_to_lax)} flights from JFK to LAX")
    
    # Find flights for an aircraft
    aircraft_flights = flight_repo.find_by_aircraft("AC1001")
    for flight in aircraft_flights:
        print(f"{flight.flight_number}: {flight.origin} → {flight.destination}")
    
    session.close()
```

### Working with Airports

```python
from neo4j_client import AirportRepository

with Neo4jConnection(
    uri="bolt://localhost:7687",
    username="neo4j",
    password="your_password"
) as conn:
    session = conn.get_session()
    airport_repo = AirportRepository(session)
    
    # Find airport by IATA code
    jfk = airport_repo.find_by_iata("JFK")
    if jfk:
        print(f"{jfk.name} in {jfk.city}, {jfk.country}")
        print(f"Coordinates: {jfk.lat}, {jfk.lon}")
    
    # Find all US airports
    us_airports = airport_repo.find_by_country("USA")
    print(f"Found {len(us_airports)} airports in USA")
    
    session.close()
```

### Working with Maintenance Events

```python
from neo4j_client import MaintenanceEventRepository

with Neo4jConnection(
    uri="bolt://localhost:7687",
    username="neo4j",
    password="your_password"
) as conn:
    session = conn.get_session()
    maint_repo = MaintenanceEventRepository(session)
    
    # Find maintenance events for an aircraft
    events = maint_repo.find_by_aircraft("AC1001")
    for event in events:
        print(f"{event.severity}: {event.fault}")
        print(f"Action: {event.corrective_action}")
    
    # Find critical events
    critical = maint_repo.find_by_severity("CRITICAL")
    print(f"Found {len(critical)} critical maintenance events")
    
    session.close()
```

### Working with Systems and Delays

```python
from neo4j_client import SystemRepository, DelayRepository

with Neo4jConnection(
    uri="bolt://localhost:7687",
    username="neo4j",
    password="your_password"
) as conn:
    session = conn.get_session()
    
    # Aircraft systems
    system_repo = SystemRepository(session)
    systems = system_repo.find_by_aircraft("AC1001")
    for system in systems:
        print(f"System: {system.name} ({system.type})")
    
    # Flight delays
    delay_repo = DelayRepository(session)
    weather_delays = delay_repo.find_by_cause("weather")
    total_minutes = sum(d.minutes for d in weather_delays)
    print(f"Weather caused {len(weather_delays)} delays totaling {total_minutes} minutes")
    
    session.close()
```

## Environment Configuration

Set these environment variables for your Neo4j connection:

```bash
export NEO4J_URI="bolt://localhost:7687"
export NEO4J_USERNAME="neo4j"
export NEO4J_PASSWORD="your_password"
export NEO4J_DATABASE="neo4j"
```

Or use them in your code:

```python
import os
from neo4j_client import Neo4jConnection

conn = Neo4jConnection(
    uri=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD"),
    database=os.getenv("NEO4J_DATABASE", "neo4j")
)
```

## Testing

The client includes comprehensive integration tests using testcontainers:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=neo4j_client

# Run specific test file
pytest tests/test_repository.py

# Run specific test
pytest tests/test_repository.py::TestAircraftRepository::test_create_aircraft
```

## Project Structure

```
neo4j_client/
├── __init__.py          # Package exports
├── models.py            # Pydantic data models
├── repository.py        # Repository pattern implementations
├── connection.py        # Connection management
└── exceptions.py        # Custom exception classes

tests/
├── __init__.py
├── conftest.py          # pytest fixtures with testcontainers
└── test_repository.py   # Integration tests

pyproject.toml           # Project configuration
README.md                # This file
MCP_DIAGNOSTIC_REPORT.md # MCP tools usage report
```

## API Reference

### Models

All models are Pydantic `BaseModel` instances with type hints:

- `Aircraft` - aircraft_id, tail_number, icao24, model, operator, manufacturer
- `Flight` - flight_id, flight_number, aircraft_id, operator, origin, destination, scheduled_departure, scheduled_arrival
- `Airport` - airport_id, name, city, country, iata, icao, lat, lon
- `MaintenanceEvent` - event_id, aircraft_id, system_id, component_id, fault, severity, corrective_action, reported_at
- `System` - system_id, aircraft_id, name, type
- `Component` - component_id, system_id, name, type
- `Sensor` - sensor_id, system_id, name, type, unit
- `Delay` - delay_id, flight_id, cause, minutes
- `Reading` - reading_id, sensor_id, timestamp, value

### Repositories

Each repository provides CRUD operations:

**AircraftRepository**
- `create(aircraft)` - Create or update aircraft
- `find_by_id(aircraft_id)` - Find by ID
- `find_by_tail_number(tail_number)` - Find by tail number
- `find_by_operator(operator)` - Find all aircraft for operator
- `find_all(limit=100)` - Find all aircraft
- `update(aircraft)` - Update aircraft
- `delete(aircraft_id)` - Delete aircraft

**FlightRepository**
- `create(flight)` - Create or update flight
- `find_by_id(flight_id)` - Find by ID
- `find_by_flight_number(flight_number)` - Find by flight number
- `find_by_aircraft(aircraft_id)` - Find flights for aircraft
- `find_by_route(origin, destination)` - Find flights on route
- `find_all(limit=100)` - Find all flights

**AirportRepository**
- `create(airport)` - Create or update airport
- `find_by_id(airport_id)` - Find by ID
- `find_by_iata(iata)` - Find by IATA code
- `find_by_country(country)` - Find airports in country
- `find_all()` - Find all airports

**MaintenanceEventRepository**
- `create(event)` - Create or update maintenance event
- `find_by_id(event_id)` - Find by ID
- `find_by_aircraft(aircraft_id)` - Find events for aircraft
- `find_by_severity(severity)` - Find events by severity

**SystemRepository**
- `find_by_aircraft(aircraft_id)` - Find systems for aircraft
- `find_by_id(system_id)` - Find by ID

**DelayRepository**
- `find_by_flight(flight_id)` - Find delays for flight
- `find_by_cause(cause)` - Find delays by cause

### Exceptions

- `Neo4jClientError` - Base exception
- `ConnectionError` - Connection failures
- `QueryError` - Query execution errors
- `NotFoundError` - Entity not found

## Security Best Practices

This client follows Neo4j security best practices:

1. **Parameterized queries** - All Cypher queries use parameters, never string interpolation
2. **MERGE over CREATE** - Uses MERGE to prevent duplicate nodes
3. **Input validation** - Pydantic models validate all data before queries
4. **Error handling** - All database errors are caught and wrapped in typed exceptions

## Next Steps

This client provides a solid foundation. Here are some ideas for extension:

1. **Add relationship methods** - Query related entities (e.g., aircraft → flights → airports)
2. **Add aggregation queries** - Count, sum, average operations
3. **Add date filtering** - Filter flights by date range
4. **Add bulk operations** - Batch create/update methods
5. **Add async support** - Use neo4j async driver for high-concurrency scenarios
6. **Add caching** - Cache frequently accessed data
7. **Add pagination** - Implement cursor-based pagination for large result sets
8. **Add transaction support** - Wrap multiple operations in transactions
9. **Add monitoring** - Add logging and metrics
10. **Add CLI tool** - Command-line interface for common operations

## Requirements

- Python 3.9+
- Neo4j 5.0+
- Dependencies: `neo4j>=5.0.0`, `pydantic>=2.0.0`
- Dev dependencies: `pytest>=7.0.0`, `testcontainers[neo4j]>=3.7.0`

## License

This is a demo project created for learning and development purposes.

## Contributing

This is a starting point client. Feel free to extend and customize for your needs!

## MCP Tools Used

This client was generated by inspecting a live Neo4j database using MCP (Model Context Protocol) server tools. See `MCP_DIAGNOSTIC_REPORT.md` for details on the tools used and the generation process.
