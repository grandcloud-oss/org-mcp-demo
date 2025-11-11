# Neo4j Airplane Database Python Client

A Python client library for the Neo4j airplane database, providing a clean and type-safe interface for working with aviation data including aircraft, flights, airports, maintenance events, and more.

## Features

- ✅ **Type-safe models** using Pydantic for all entities
- ✅ **Repository pattern** for clean query organization  
- ✅ **Parameterized Cypher queries** to prevent injection attacks
- ✅ **Connection management** with context manager support
- ✅ **Comprehensive test suite** using pytest and testcontainers
- ✅ **Modern Python packaging** with pyproject.toml

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
from neo4j_client import Neo4jConnection, AircraftRepository, FlightRepository

# Connect to database
with Neo4jConnection(
    uri="bolt://localhost:7687",
    username="neo4j",
    password="password"
) as conn:
    # Get a session
    session = conn.get_session()
    
    # Create repository
    aircraft_repo = AircraftRepository(session)
    
    # Find all aircraft
    aircraft_list = aircraft_repo.find_all(limit=10)
    for aircraft in aircraft_list:
        print(f"{aircraft.tail_number}: {aircraft.model}")
    
    session.close()
```

### Working with Aircraft

```python
from neo4j_client import Neo4jConnection, AircraftRepository, Aircraft

with Neo4jConnection(uri="bolt://localhost:7687", username="neo4j", password="password") as conn:
    session = conn.get_session()
    repo = AircraftRepository(session)
    
    # Create a new aircraft
    aircraft = Aircraft(
        aircraft_id="AC001",
        tail_number="N12345",
        icao24="ABC123",
        model="Boeing 737-800",
        manufacturer="Boeing",
        operator="United Airlines"
    )
    repo.create(aircraft)
    
    # Find by tail number
    found = repo.find_by_tail_number("N12345")
    print(f"Found: {found.model}")
    
    # Find by operator
    united_aircraft = repo.find_by_operator("United Airlines")
    print(f"United has {len(united_aircraft)} aircraft")
    
    session.close()
```

### Working with Flights

```python
from neo4j_client import FlightRepository, Flight

with Neo4jConnection(uri="bolt://localhost:7687", username="neo4j", password="password") as conn:
    session = conn.get_session()
    repo = FlightRepository(session)
    
    # Find flights by route
    flights = repo.find_by_route("JFK", "LAX")
    for flight in flights:
        print(f"Flight {flight.flight_number}: {flight.scheduled_departure}")
    
    # Get flight with delays
    flight_data = repo.get_flight_with_delays("FL12345")
    print(f"Flight: {flight_data['flight'].flight_number}")
    print(f"Delays: {len(flight_data['delays'])}")
    for delay in flight_data['delays']:
        print(f"  - {delay.cause}: {delay.minutes} minutes")
    
    session.close()
```

### Working with Airports

```python
from neo4j_client import AirportRepository

with Neo4jConnection(uri="bolt://localhost:7687", username="neo4j", password="password") as conn:
    session = conn.get_session()
    repo = AirportRepository(session)
    
    # Find by IATA code
    jfk = repo.find_by_iata("JFK")
    if jfk:
        print(f"{jfk.name} ({jfk.iata})")
        print(f"Location: {jfk.city}, {jfk.country}")
        print(f"Coordinates: {jfk.lat}, {jfk.lon}")
    
    # Find all airports in a country
    usa_airports = repo.find_by_country("USA")
    print(f"USA has {len(usa_airports)} airports")
    
    session.close()
```

### Working with Maintenance Events

```python
from neo4j_client import MaintenanceEventRepository

with Neo4jConnection(uri="bolt://localhost:7687", username="neo4j", password="password") as conn:
    session = conn.get_session()
    repo = MaintenanceEventRepository(session)
    
    # Find events for an aircraft
    events = repo.find_by_aircraft("AC001")
    for event in events:
        print(f"{event.reported_at}: {event.fault} ({event.severity})")
        print(f"  Action: {event.corrective_action}")
    
    # Find critical events
    critical = repo.find_by_severity("Critical")
    print(f"Found {len(critical)} critical maintenance events")
    
    session.close()
```

## Database Schema

The airplane database contains the following entities:

### Node Types

- **Aircraft** (60 nodes) - Aircraft in the fleet
  - `aircraft_id`, `tail_number`, `icao24`, `model`, `manufacturer`, `operator`
  
- **Airport** (36 nodes) - Airports
  - `airport_id`, `name`, `iata`, `icao`, `city`, `country`, `lat`, `lon`
  
- **Flight** (2,400 nodes) - Flight operations
  - `flight_id`, `flight_number`, `aircraft_id`, `operator`, `origin`, `destination`, `scheduled_departure`, `scheduled_arrival`
  
- **Delay** (1,542 nodes) - Flight delays
  - `delay_id`, `flight_id`, `cause`, `minutes`
  
- **System** (240 nodes) - Aircraft systems (hydraulic, electrical, etc.)
  - `system_id`, `aircraft_id`, `name`, `type`
  
- **Component** (960 nodes) - System components
  - `component_id`, `system_id`, `name`, `type`
  
- **Sensor** (480 nodes) - Sensors monitoring systems
  - `sensor_id`, `system_id`, `name`, `type`, `unit`
  
- **MaintenanceEvent** (900 nodes) - Maintenance records
  - `event_id`, `aircraft_id`, `component_id`, `system_id`, `fault`, `severity`, `corrective_action`, `reported_at`
  
- **Reading** (1M+ nodes) - Sensor readings
  - `reading_id`, `sensor_id`, `timestamp`, `value`

### Relationships

- `HAS_SYSTEM` - Aircraft to System
- `HAS_COMPONENT` - System to Component
- `HAS_SENSOR` - System to Sensor
- `OPERATES_FLIGHT` - Aircraft to Flight
- `DEPARTS_FROM` - Flight to Airport
- `ARRIVES_AT` - Flight to Airport
- `HAS_DELAY` - Flight to Delay
- `HAS_EVENT` - Component to MaintenanceEvent
- `AFFECTS_SYSTEM` - MaintenanceEvent to System
- `AFFECTS_AIRCRAFT` - MaintenanceEvent to Aircraft

## Available Repositories

### AircraftRepository
- `create(aircraft)` - Create or update aircraft
- `find_by_id(aircraft_id)` - Find by ID
- `find_by_tail_number(tail_number)` - Find by tail number
- `find_by_operator(operator)` - Find all aircraft for operator
- `find_all(limit=100)` - Find all aircraft
- `delete(aircraft_id)` - Delete aircraft

### AirportRepository
- `create(airport)` - Create or update airport
- `find_by_id(airport_id)` - Find by ID
- `find_by_iata(iata)` - Find by IATA code
- `find_by_country(country)` - Find all airports in country
- `find_all(limit=100)` - Find all airports

### FlightRepository
- `create(flight)` - Create or update flight
- `find_by_id(flight_id)` - Find by ID
- `find_by_flight_number(flight_number)` - Find by flight number
- `find_by_route(origin, destination)` - Find by route
- `find_all(limit=100)` - Find all flights
- `get_flight_with_delays(flight_id)` - Get flight with associated delays

### DelayRepository
- `create(delay)` - Create or update delay
- `find_by_id(delay_id)` - Find by ID
- `find_by_flight(flight_id)` - Find delays for flight
- `find_by_cause(cause)` - Find by delay cause
- `find_all(limit=100)` - Find all delays

### MaintenanceEventRepository
- `create(event)` - Create or update maintenance event
- `find_by_id(event_id)` - Find by ID
- `find_by_aircraft(aircraft_id)` - Find events for aircraft
- `find_by_severity(severity)` - Find by severity level
- `find_all(limit=100)` - Find all events

## Testing

The library includes a comprehensive test suite using pytest and testcontainers.

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

## Environment Configuration

The client requires connection to a Neo4j database. You can configure using environment variables:

```bash
export NEO4J_URI="bolt://localhost:7687"
export NEO4J_USERNAME="neo4j"
export NEO4J_PASSWORD="your-password"
export NEO4J_DATABASE="neo4j"
```

Or pass directly to `Neo4jConnection`:

```python
conn = Neo4jConnection(
    uri="bolt://localhost:7687",
    username="neo4j",
    password="your-password",
    database="neo4j"
)
```

## Security Best Practices

This library follows Neo4j security best practices:

1. **Parameterized queries** - All Cypher queries use named parameters to prevent injection attacks
2. **MERGE over CREATE** - Uses `MERGE` to safely handle duplicate prevention
3. **Input validation** - Pydantic models validate all data before queries
4. **Error handling** - Custom exceptions wrap Neo4j driver errors
5. **Connection management** - Context managers ensure proper cleanup

## What's Included

✅ Pydantic models for type safety  
✅ Repository pattern for query organization  
✅ Parameterized Cypher queries  
✅ Connection management with context managers  
✅ Custom exception hierarchy  
✅ Comprehensive test suite  
✅ Modern Python packaging  

## What's NOT Included (Future Extensions)

This is a starting point client. Consider adding:

- ❌ Async/await support
- ❌ ORM-like relationship mapping
- ❌ Advanced transaction management
- ❌ Query result caching
- ❌ Retry logic and circuit breakers
- ❌ Logging and observability
- ❌ CLI tools
- ❌ Migration utilities

## Next Steps

To extend this client:

1. **Add relationship management** - Methods to create/query relationships between entities
2. **Add aggregation queries** - Statistics and analytics queries
3. **Add bulk operations** - Batch create/update methods
4. **Add async support** - Use `neo4j.AsyncGraphDatabase` for async operations
5. **Add caching** - Cache frequently accessed data
6. **Add custom queries** - Domain-specific query methods
7. **Add monitoring** - Log queries and performance metrics

## License

MIT License

## Contributing

This library was generated as a starting point. Feel free to extend and customize for your needs.
