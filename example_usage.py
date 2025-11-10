#!/usr/bin/env python3
"""
Example script demonstrating the Neo4j Airplane Data Client.

This script connects to the Neo4j database and performs various queries
to showcase the client's capabilities.
"""

import os
from neo4j_client import (
    Neo4jConnection,
    AircraftRepository,
    FlightRepository,
    AirportRepository,
    MaintenanceEventRepository,
    SystemRepository,
    DelayRepository,
)


def main():
    """Main function demonstrating client usage."""
    # Get connection details from environment
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    username = os.getenv("NEO4J_USERNAME", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")
    
    print("=" * 60)
    print("Neo4j Airplane Data Client - Example")
    print("=" * 60)
    print(f"\nConnecting to: {uri}")
    
    # Connect to Neo4j
    with Neo4jConnection(uri, username, password) as conn:
        session = conn.get_session()
        
        # 1. Query Aircraft
        print("\n" + "=" * 60)
        print("1. Aircraft Query Examples")
        print("=" * 60)
        
        aircraft_repo = AircraftRepository(session)
        all_aircraft = aircraft_repo.find_all(limit=5)
        print(f"\nFound {len(all_aircraft)} aircraft (showing first 5):")
        for aircraft in all_aircraft:
            print(f"  • {aircraft.tail_number}: {aircraft.manufacturer} {aircraft.model}")
            print(f"    Operator: {aircraft.operator}")
        
        # Find specific aircraft
        if all_aircraft:
            sample_tail = all_aircraft[0].tail_number
            print(f"\nSearching for aircraft with tail number: {sample_tail}")
            found = aircraft_repo.find_by_tail_number(sample_tail)
            if found:
                print(f"  ✓ Found: {found.model} (ICAO24: {found.icao24})")
        
        # 2. Query Flights
        print("\n" + "=" * 60)
        print("2. Flight Query Examples")
        print("=" * 60)
        
        flight_repo = FlightRepository(session)
        all_flights = flight_repo.find_all(limit=5)
        print(f"\nFound {len(all_flights)} flights (showing first 5):")
        for flight in all_flights:
            print(f"  • {flight.flight_number}: {flight.origin} → {flight.destination}")
            print(f"    Operator: {flight.operator}")
            print(f"    Departure: {flight.scheduled_departure}")
        
        # 3. Query Airports
        print("\n" + "=" * 60)
        print("3. Airport Query Examples")
        print("=" * 60)
        
        airport_repo = AirportRepository(session)
        all_airports = airport_repo.find_all()
        print(f"\nFound {len(all_airports)} airports total")
        
        # Find US airports
        us_airports = airport_repo.find_by_country("USA")
        print(f"\nUS Airports ({len(us_airports)} total, showing first 5):")
        for airport in us_airports[:5]:
            print(f"  • {airport.iata} - {airport.name}")
            print(f"    Location: {airport.city}, {airport.country}")
            print(f"    Coordinates: {airport.lat}, {airport.lon}")
        
        # 4. Query Maintenance Events
        print("\n" + "=" * 60)
        print("4. Maintenance Event Query Examples")
        print("=" * 60)
        
        maint_repo = MaintenanceEventRepository(session)
        
        # Find events by severity
        for severity in ["CRITICAL", "HIGH", "MEDIUM"]:
            events = maint_repo.find_by_severity(severity)
            print(f"\n{severity} maintenance events: {len(events)}")
            if events:
                sample = events[0]
                print(f"  Example: {sample.fault}")
                print(f"  Action: {sample.corrective_action}")
        
        # 5. Query Systems
        print("\n" + "=" * 60)
        print("5. Aircraft Systems Query Examples")
        print("=" * 60)
        
        system_repo = SystemRepository(session)
        if all_aircraft:
            sample_aircraft_id = all_aircraft[0].aircraft_id
            systems = system_repo.find_by_aircraft(sample_aircraft_id)
            print(f"\nSystems for aircraft {sample_aircraft_id}: {len(systems)}")
            for system in systems[:5]:
                print(f"  • {system.name} ({system.type})")
        
        # 6. Query Delays
        print("\n" + "=" * 60)
        print("6. Flight Delay Query Examples")
        print("=" * 60)
        
        delay_repo = DelayRepository(session)
        
        # Find delays by cause
        delay_causes = ["weather", "mechanical", "crew", "air_traffic"]
        for cause in delay_causes:
            delays = delay_repo.find_by_cause(cause)
            if delays:
                total_minutes = sum(d.minutes for d in delays)
                avg_minutes = total_minutes / len(delays) if delays else 0
                print(f"\n{cause.upper()} delays:")
                print(f"  Count: {len(delays)}")
                print(f"  Total time: {total_minutes} minutes")
                print(f"  Average: {avg_minutes:.1f} minutes")
        
        session.close()
    
    print("\n" + "=" * 60)
    print("Demo completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
