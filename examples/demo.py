"""
Example script demonstrating the Neo4j airplane data client.

This script shows how to use the client to interact with airplane data in Neo4j.
It assumes you have a Neo4j instance running with airplane data.

Usage:
    python examples/demo.py

Environment Variables:
    NEO4J_URI - Neo4j connection URI (default: bolt://localhost:7687)
    NEO4J_USERNAME - Neo4j username (default: neo4j)
    NEO4J_PASSWORD - Neo4j password (required)
    NEO4J_DATABASE - Neo4j database name (default: neo4j)
"""

import os
from neo4j_client import (
    Neo4jConnection,
    AircraftRepository,
    FlightRepository,
    AirportRepository,
    MaintenanceEventRepository,
    SystemRepository,
)


def main():
    """Main demonstration function."""
    
    # Get connection details from environment
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    username = os.getenv("NEO4J_USERNAME", "neo4j")
    password = os.getenv("NEO4J_PASSWORD")
    database = os.getenv("NEO4J_DATABASE", "neo4j")
    
    if not password:
        print("Error: NEO4J_PASSWORD environment variable is required")
        return
    
    print("=" * 60)
    print("Neo4j Airplane Data Client - Demo")
    print("=" * 60)
    print(f"Connecting to: {uri}")
    print(f"Database: {database}")
    print()
    
    # Create connection using context manager
    with Neo4jConnection(uri, username, password, database) as connection:
        with connection.get_session() as session:
            # Example 1: Query aircraft
            print("Example 1: Finding all aircraft")
            print("-" * 60)
            aircraft_repo = AircraftRepository(session)
            aircraft_list = aircraft_repo.find_all()
            
            print(f"Total aircraft in database: {len(aircraft_list)}")
            if aircraft_list:
                for i, aircraft in enumerate(aircraft_list[:5], 1):
                    print(f"{i}. {aircraft.tail_number} - {aircraft.model} ({aircraft.operator})")
                if len(aircraft_list) > 5:
                    print(f"... and {len(aircraft_list) - 5} more")
            print()
            
            # Example 2: Find aircraft by operator
            if aircraft_list:
                first_operator = aircraft_list[0].operator
                print(f"Example 2: Finding aircraft for operator '{first_operator}'")
                print("-" * 60)
                operator_fleet = aircraft_repo.find_by_operator(first_operator)
                print(f"Fleet size: {len(operator_fleet)}")
                for aircraft in operator_fleet[:3]:
                    print(f"  - {aircraft.tail_number} ({aircraft.model})")
                print()
            
            # Example 3: Query airports
            print("Example 3: Finding all airports")
            print("-" * 60)
            airport_repo = AirportRepository(session)
            airports = airport_repo.find_all()
            
            print(f"Total airports: {len(airports)}")
            if airports:
                for i, airport in enumerate(airports[:5], 1):
                    print(f"{i}. {airport.iata} - {airport.name} ({airport.city}, {airport.country})")
                if len(airports) > 5:
                    print(f"... and {len(airports) - 5} more")
            print()
            
            # Example 4: Find flights
            print("Example 4: Finding flights")
            print("-" * 60)
            flight_repo = FlightRepository(session)
            flights = flight_repo.find_all()
            
            print(f"Total flights: {len(flights)}")
            if flights:
                for i, flight in enumerate(flights[:5], 1):
                    print(f"{i}. {flight.flight_number}: {flight.origin} → {flight.destination}")
                if len(flights) > 5:
                    print(f"... and {len(flights) - 5} more")
            print()
            
            # Example 5: Find flights by route
            if airports and len(airports) >= 2:
                origin = airports[0].iata
                destination = airports[1].iata
                print(f"Example 5: Finding flights from {origin} to {destination}")
                print("-" * 60)
                route_flights = flight_repo.find_by_route(origin, destination)
                print(f"Flights on this route: {len(route_flights)}")
                for flight in route_flights[:3]:
                    print(f"  - {flight.flight_number} ({flight.operator})")
                print()
            
            # Example 6: Find maintenance events
            print("Example 6: Finding maintenance events")
            print("-" * 60)
            maint_repo = MaintenanceEventRepository(session)
            events = maint_repo.find_all()
            
            print(f"Total maintenance events: {len(events)}")
            if events:
                for i, event in enumerate(events[:5], 1):
                    print(f"{i}. [{event.severity}] {event.fault[:50]}...")
                if len(events) > 5:
                    print(f"... and {len(events) - 5} more")
            print()
            
            # Example 7: Find high severity maintenance events
            print("Example 7: Finding high severity maintenance events")
            print("-" * 60)
            high_severity = maint_repo.find_by_severity("High")
            print(f"High severity events: {len(high_severity)}")
            for event in high_severity[:3]:
                print(f"  - {event.fault[:60]}...")
            print()
            
            # Example 8: Find aircraft systems
            if aircraft_list:
                first_aircraft = aircraft_list[0].aircraft_id
                print(f"Example 8: Finding systems for aircraft {aircraft_list[0].tail_number}")
                print("-" * 60)
                system_repo = SystemRepository(session)
                systems = system_repo.find_by_aircraft(first_aircraft)
                print(f"Systems: {len(systems)}")
                for system in systems[:5]:
                    print(f"  - {system.name} ({system.type})")
                print()
    
    print("=" * 60)
    print("Demo completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
