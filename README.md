# Neo4j Python Client for Airplane Data

A simple, high-quality Python client library for working with airplane data in Neo4j. This library provides a clean, type-safe interface using Pydantic models and the repository pattern.

## Features

✅ **Type-safe models** - Pydantic models for all entities (Aircraft, Flight, Airport, etc.)  
✅ **Repository pattern** - Clean CRUD operations for each entity type  
✅ **Parameterized queries** - All Cypher queries use parameters to prevent injection  
✅ **Connection management** - Context manager support for automatic cleanup  
✅ **Well-tested** - Integration tests using testcontainers  
✅ **Modern Python** - Type hints throughout, Python 3.9+ compatible  

## Entities

The client supports the following airplane data entities:

- **Aircraft** - Aircraft information (tail number, model, manufacturer, operator)
- **Airport** - Airport data (IATA/ICAO codes, location, city, country)
- **Flight** - Flight records (flight number, route, schedule)
- **System** - Aircraft systems (engines, hydraulics, avionics)
- **Component** - System components
- **MaintenanceEvent** - Maintenance and fault records
- **Delay** - Flight delay records with cause
- **Sensor** - Sensor information
- **Reading** - Sensor telemetry data

## Installation

```bash
# Install the package
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"
```

## Quick Start

### Basic Connection

```python
from neo4j_client import Neo4jConnection

# Create connection
conn = Neo4jConnection(
    uri="bolt://localhost:7687",
    username="neo4j",
    password="your_password"
)

# Use with context manager (recommended)
with Neo4jConnection("bolt://localhost:7687", "neo4j", "password") as conn:
    with conn.session() as session:
        # Use session here
        pass
```

### Working with Aircraft

```python
from neo4j_client import Neo4jConnection, AircraftRepository, Aircraft

# Connect to database
with Neo4jConnection("bolt://localhost:7687", "neo4j", "password") as conn:
    with conn.session() as session:
        # Create repository
        aircraft_repo = AircraftRepository(session)
        
        # Create a new aircraft
        aircraft = Aircraft(
            aircraft_id="AC1001",
            tail_number="N95040A",
            icao24="448367",
            model="B737-800",
            operator="ExampleAir",
            manufacturer="Boeing"
        )
        aircraft_repo.create(aircraft)
        
        # Find aircraft by ID
        found = aircraft_repo.find_by_id("AC1001")
        print(f"Found: {found.tail_number} - {found.model}")
        
        # Find all aircraft for an operator
        operator_fleet = aircraft_repo.find_by_operator("ExampleAir")
        print(f"Fleet size: {len(operator_fleet)}")
        
        # Find by tail number
        by_tail = aircraft_repo.find_by_tail_number("N95040A")
        
        # Get all aircraft
        all_aircraft = aircraft_repo.find_all(limit=100)
```

### Working with Flights

```python
from neo4j_client import FlightRepository, Flight

with Neo4jConnection("bolt://localhost:7687", "neo4j", "password") as conn:
    with conn.session() as session:
        flight_repo = FlightRepository(session)
        
        # Create a flight
        flight = Flight(
            flight_id="FL00001",
            flight_number="EX370",
            aircraft_id="AC1013",
            operator="ExampleAir",
            origin="PHX",
            destination="SEA",
            scheduled_departure="2024-09-27T22:00:00",
            scheduled_arrival="2024-09-28T03:24:00"
        )
        flight_repo.create(flight)
        
        # Find flights by route
        route_flights = flight_repo.find_by_route("PHX", "SEA")
        
        # Find flights for an aircraft
        aircraft_flights = flight_repo.find_by_aircraft("AC1013")
        
        # Find by flight number
        by_number = flight_repo.find_by_flight_number("EX370")
```

### Working with Airports

```python
from neo4j_client import AirportRepository, Airport

with Neo4jConnection("bolt://localhost:7687", "neo4j", "password") as conn:
    with conn.session() as session:
        airport_repo = AirportRepository(session)
        
        # Create an airport
        airport = Airport(
            airport_id="JFK",
            iata="JFK",
            icao="KJFK",
            name="John F. Kennedy International",
            city="New York",
            country="USA",
            lat=40.6413,
            lon=-73.7781
        )
        airport_repo.create(airport)
        
        # Find by IATA code
        jfk = airport_repo.find_by_iata("JFK")
        print(f"{jfk.name} in {jfk.city}")
        
        # Find all airports in a country
        us_airports = airport_repo.find_by_country("USA")
```

### Working with Maintenance Events

```python
from neo4j_client import MaintenanceEventRepository, MaintenanceEvent

with Neo4jConnection("bolt://localhost:7687", "neo4j", "password") as conn:
    with conn.session() as session:
        maintenance_repo = MaintenanceEventRepository(session)
        
        # Create a maintenance event
        event = MaintenanceEvent(
            event_id="ME0001",
            aircraft_id="AC1002",
            system_id="AC1002-S04",
            component_id="AC1002-S04-C02",
            fault="Contamination",
            severity="CRITICAL",
            reported_at="2024-08-27T12:00:00",
            corrective_action="Adjusted tolerance"
        )
        maintenance_repo.create(event)
        
        # Find all maintenance events for an aircraft
        aircraft_events = maintenance_repo.find_by_aircraft("AC1002")
        
        # Find critical events
        critical_events = maintenance_repo.find_by_severity("CRITICAL")
        for event in critical_events:
            print(f"{event.fault} - {event.corrective_action}")
```

### Working with Systems and Delays

```python
from neo4j_client import SystemRepository, DelayRepository

with Neo4jConnection("bolt://localhost:7687", "neo4j", "password") as conn:
    with conn.session() as session:
        # Systems
        system_repo = SystemRepository(session)
        
        # Find all systems for an aircraft
        systems = system_repo.find_by_aircraft("AC1001")
        
        # Find engines
        engines = system_repo.find_by_type("Engine")
        
        # Delays
        delay_repo = DelayRepository(session)
        
        # Find delays for a flight
        flight_delays = delay_repo.find_by_flight("FL00001")
        
        # Find delays by cause
        weather_delays = delay_repo.find_by_cause("Weather")
```

## Error Handling

The library provides custom exceptions for better error handling:

```python
from neo4j_client import (
    Neo4jClientError,
    ConnectionError,
    QueryError,
    NotFoundError
)

try:
    conn = Neo4jConnection("bolt://localhost:7687", "neo4j", "password")
except ConnectionError as e:
    print(f"Failed to connect: {e}")

try:
    aircraft = aircraft_repo.create(invalid_aircraft)
except QueryError as e:
    print(f"Query failed: {e}")
```

## Testing

The library includes comprehensive tests using pytest and testcontainers:

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with verbose output
pytest -v

# Run specific test file
pytest tests/test_repository.py

# Run specific test
pytest tests/test_repository.py::TestAircraftRepository::test_create_aircraft
```

## Development

### Project Structure

```
neo4j_client/
├── __init__.py          # Package exports
├── models.py            # Pydantic data models
├── repository.py        # Repository classes for CRUD
├── connection.py        # Connection management
└── exceptions.py        # Custom exceptions

tests/
├── __init__.py
├── conftest.py          # pytest fixtures
└── test_repository.py   # Repository tests
```

### Code Quality

- All code uses type hints
- Pydantic models for data validation
- Parameterized Cypher queries (no SQL injection risk)
- Repository pattern for clean separation
- Context managers for resource management

## Next Steps

This is a starting point library. You can extend it with:

- **Additional query methods** - Add more specialized queries to repositories
- **Relationship methods** - Add methods to query relationships between entities
- **Batch operations** - Add bulk create/update methods
- **Transaction support** - Add explicit transaction management
- **Async support** - Add async/await support for concurrent operations
- **Query builders** - Add fluent query builders for complex queries
- **Caching** - Add caching layer for frequently accessed data
- **Monitoring** - Add logging and metrics collection

## License

Generated by Neo4j Python Client Agent

## MCP Tools Diagnostic Report

This client library was generated using the **Neo4j MCP (Model Context Protocol) Server** tools. Below is a complete report of the MCP tools and capabilities used during generation:

### MCP Server Information

**Server**: Neo4j MCP Server (local instance)  
**Purpose**: Schema introspection and data exploration for Neo4j databases  

### Tools Used

#### 1. `get_neo4j_schema`
**Purpose**: Retrieve complete database schema including node labels, properties, relationships, and cardinalities  
**Usage**: Called at the beginning to understand the airplane data model structure  
**Sample Size**: 1000 nodes (default)  
**Output**: Discovered 10 node types, 10 relationship types, and all property schemas

**Discovered Entities**:
- Aircraft (60 nodes) - 6 properties
- Airport (36 nodes) - 8 properties  
- Flight (2,400 nodes) - 8 properties
- System (240 nodes) - 4 properties
- Component (960 nodes) - 4 properties
- MaintenanceEvent (900 nodes) - 8 properties
- Delay (1,542 nodes) - 4 properties
- Sensor (480 nodes) - 5 properties
- Reading (1,036,800 nodes) - 4 properties

**Discovered Relationships**:
- OPERATES_FLIGHT (Aircraft → Flight)
- DEPARTS_FROM (Flight → Airport)
- ARRIVES_AT (Flight → Airport)
- HAS_DELAY (Flight → Delay)
- HAS_SYSTEM (Aircraft → System)
- HAS_COMPONENT (System → Component)
- HAS_SENSOR (System → Sensor)
- AFFECTS_AIRCRAFT (MaintenanceEvent → Aircraft)
- AFFECTS_SYSTEM (MaintenanceEvent → System)
- HAS_EVENT (Component → MaintenanceEvent)

#### 2. `read_neo4j_cypher`
**Purpose**: Execute read-only Cypher queries to explore sample data  
**Usage**: Called multiple times to inspect actual data values and understand data patterns  

**Queries Executed**:
1. `MATCH (a:Aircraft) RETURN a LIMIT 3` - Explored aircraft records
2. `MATCH (f:Flight) RETURN f LIMIT 3` - Explored flight records
3. `MATCH (ap:Airport) RETURN ap LIMIT 3` - Explored airport records
4. `MATCH (s:System) RETURN s LIMIT 2` - Explored system records
5. `MATCH (me:MaintenanceEvent) RETURN me LIMIT 2` - Explored maintenance records
6. `MATCH (d:Delay) RETURN d LIMIT 2` - Explored delay records

**Value**: Understanding actual data helped:
- Identify property data types (strings, integers, floats)
- Understand naming conventions (e.g., IATA codes, ISO timestamps)
- Discover domain-specific values (severity levels, delay causes)
- Inform example data in tests and documentation

### Generation Process

1. **Schema Discovery** (using `get_neo4j_schema`)
   - Retrieved complete graph schema
   - Identified all node labels and relationship types
   - Discovered property names and types
   - Understood cardinalities and data distribution

2. **Data Exploration** (using `read_neo4j_cypher`)
   - Sampled real data from each entity type
   - Validated property types and formats
   - Understood data patterns and conventions
   - Collected realistic example values

3. **Model Generation**
   - Created Pydantic models for each entity type
   - Added appropriate type hints based on discovered types
   - Included comprehensive docstrings
   - Used realistic field names from actual schema

4. **Repository Implementation**
   - Designed CRUD methods for each entity
   - Implemented parameterized Cypher queries
   - Added specialized query methods (e.g., find by operator, find by route)
   - Used MERGE for idempotent creates

5. **Test Creation**
   - Built tests with realistic data based on samples
   - Covered CRUD operations for all repositories
   - Used testcontainers for integration testing
   - Validated query correctness

### Benefits of MCP-Assisted Generation

✅ **Accuracy** - Models exactly match actual database schema  
✅ **Completeness** - All entities and relationships discovered automatically  
✅ **Type Safety** - Correct Python types inferred from Neo4j property types  
✅ **Realistic Examples** - Documentation uses actual data patterns  
✅ **No Manual Inspection** - Avoided error-prone manual schema exploration  
✅ **Up-to-date** - Reflects current database state, not outdated documentation  

### MCP vs Manual Approach

| Aspect | MCP-Assisted | Manual Approach |
|--------|--------------|----------------|
| Schema Discovery | Automatic via `get_neo4j_schema` | Manual Cypher queries |
| Accuracy | 100% match to database | Risk of human error |
| Time to Complete | Minutes | Hours |
| Completeness | All entities discovered | May miss entities |
| Type Inference | Automatic from samples | Manual inference |
| Maintenance | Re-run tools | Manual re-inspection |

### Conclusion

The Neo4j MCP Server tools enabled rapid, accurate generation of this Python client library by providing programmatic access to schema metadata and data exploration capabilities. The combination of `get_neo4j_schema` for structure discovery and `read_neo4j_cypher` for data validation created a foundation for generating type-safe, production-ready client code.
