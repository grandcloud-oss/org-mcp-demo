#!/usr/bin/env python
"""Example script demonstrating the airplane client usage."""

import os
from airplane_client import (
    Neo4jConnection,
    AircraftRepository,
    AirportRepository,
    FlightRepository,
    SystemRepository,
    MaintenanceEventRepository,
)


def main():
    """Main example function."""
    # Get connection details from environment variables
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    username = os.getenv("NEO4J_USERNAME", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")
    database = os.getenv("NEO4J_DATABASE", "neo4j")
    
    # Create connection
    connection = Neo4jConnection(uri, username, password, database)
    
    # Use context manager for automatic cleanup
    with connection:
        print("=== Airplane Database Client Example ===\n")
        
        # Example 1: Query Aircraft
        print("1. Querying Aircraft...")
        aircraft_repo = AircraftRepository(connection)
        aircraft_list = aircraft_repo.find_all(limit=5)
        print(f"   Found {len(aircraft_list)} aircraft:")
        for aircraft in aircraft_list:
            print(f"   - {aircraft.tail_number}: {aircraft.manufacturer} {aircraft.model}")
        print()
        
        # Example 2: Query Airports
        print("2. Querying Airports...")
        airport_repo = AirportRepository(connection)
        airports = airport_repo.find_all(limit=5)
        print(f"   Found {len(airports)} airports:")
        for airport in airports:
            print(f"   - {airport.iata} ({airport.icao}): {airport.name}, {airport.city}, {airport.country}")
        print()
        
        # Example 3: Query Flights
        print("3. Querying Flights...")
        flight_repo = FlightRepository(connection)
        flights = flight_repo.find_all(limit=5)
        print(f"   Found {len(flights)} flights:")
        for flight in flights:
            print(f"   - {flight.flight_number}: {flight.origin} → {flight.destination}")
        print()
        
        # Example 4: Query Aircraft Systems
        if aircraft_list:
            first_aircraft = aircraft_list[0]
            print(f"4. Querying Systems for Aircraft {first_aircraft.tail_number}...")
            system_repo = SystemRepository(connection)
            systems = system_repo.find_by_aircraft(first_aircraft.aircraft_id)
            print(f"   Found {len(systems)} systems:")
            for system in systems:
                print(f"   - {system.name} ({system.type})")
            print()
        
        # Example 5: Query Maintenance Events
        print("5. Querying Recent Maintenance Events...")
        maintenance_repo = MaintenanceEventRepository(connection)
        events = maintenance_repo.find_by_severity("High", limit=3)
        print(f"   Found {len(events)} high-severity events:")
        for event in events:
            print(f"   - {event.reported_at}: {event.fault}")
            print(f"     Corrective Action: {event.corrective_action}")
        print()
        
        print("=== Example Complete ===")


if __name__ == "__main__":
    main()
