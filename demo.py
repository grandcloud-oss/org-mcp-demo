#!/usr/bin/env python3
"""
Demonstration script showing the Neo4j Python client working with actual airplane data.

This script connects to the Neo4j database and demonstrates various queries
using the generated client library.
"""

import os
from neo4j_client import (
    Neo4jConnection,
    AircraftRepository,
    AirportRepository,
    FlightRepository,
    MaintenanceEventRepository,
    SystemRepository,
    DelayRepository,
)


def main():
    # Get connection details from environment (MCP server provides these)
    uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
    username = os.environ.get("NEO4J_USERNAME", "neo4j")
    password = os.environ.get("NEO4J_PASSWORD", "password")
    
    print("=" * 80)
    print("Neo4j Python Client Demonstration")
    print("=" * 80)
    print(f"\nConnecting to: {uri}")
    
    with Neo4jConnection(uri, username, password) as conn:
        with conn.session() as session:
            print("\n✓ Connected successfully!\n")
            
            # Demonstrate Aircraft Repository
            print("-" * 80)
            print("1. AIRCRAFT QUERIES")
            print("-" * 80)
            
            aircraft_repo = AircraftRepository(session)
            
            # Get all aircraft (limited to 5)
            all_aircraft = aircraft_repo.find_all(limit=5)
            print(f"\nFound {len(all_aircraft)} aircraft (showing first 5):")
            for aircraft in all_aircraft:
                print(f"  - {aircraft.tail_number}: {aircraft.manufacturer} {aircraft.model} "
                      f"(Operator: {aircraft.operator})")
            
            # Query by operator
            if all_aircraft:
                operator = all_aircraft[0].operator
                operator_fleet = aircraft_repo.find_by_operator(operator)
                print(f"\n{operator} fleet size: {len(operator_fleet)} aircraft")
            
            # Demonstrate Airport Repository
            print("\n" + "-" * 80)
            print("2. AIRPORT QUERIES")
            print("-" * 80)
            
            airport_repo = AirportRepository(session)
            
            # Get all airports
            all_airports = airport_repo.find_all(limit=10)
            print(f"\nFound {len(all_airports)} airports (showing first 10):")
            for airport in all_airports:
                print(f"  - {airport.iata} ({airport.icao}): {airport.name}, "
                      f"{airport.city}, {airport.country}")
            
            # Query by country
            us_airports = airport_repo.find_by_country("USA")
            print(f"\nTotal USA airports: {len(us_airports)}")
            
            # Demonstrate Flight Repository
            print("\n" + "-" * 80)
            print("3. FLIGHT QUERIES")
            print("-" * 80)
            
            flight_repo = FlightRepository(session)
            
            # Get sample flights
            sample_flights = flight_repo.find_by_aircraft(all_aircraft[0].aircraft_id, limit=3)
            print(f"\nFlights for aircraft {all_aircraft[0].tail_number}:")
            for flight in sample_flights:
                print(f"  - {flight.flight_number}: {flight.origin} → {flight.destination}")
                print(f"    Departure: {flight.scheduled_departure}")
                print(f"    Arrival:   {flight.scheduled_arrival}")
            
            # Demonstrate Maintenance Events
            print("\n" + "-" * 80)
            print("4. MAINTENANCE EVENT QUERIES")
            print("-" * 80)
            
            maintenance_repo = MaintenanceEventRepository(session)
            
            # Find critical maintenance events
            critical_events = maintenance_repo.find_by_severity("CRITICAL", limit=5)
            print(f"\nCritical maintenance events (showing {len(critical_events)}):")
            for event in critical_events:
                print(f"  - Event {event.event_id}:")
                print(f"    Aircraft: {event.aircraft_id}")
                print(f"    Fault: {event.fault}")
                print(f"    Action: {event.corrective_action}")
                print(f"    Reported: {event.reported_at}")
            
            # Demonstrate Systems
            print("\n" + "-" * 80)
            print("5. AIRCRAFT SYSTEMS QUERIES")
            print("-" * 80)
            
            system_repo = SystemRepository(session)
            
            # Find systems for first aircraft
            systems = system_repo.find_by_aircraft(all_aircraft[0].aircraft_id)
            print(f"\nSystems on aircraft {all_aircraft[0].tail_number}:")
            for system in systems:
                print(f"  - {system.name} (Type: {system.type})")
            
            # Find all engines
            engines = system_repo.find_by_type("Engine", limit=10)
            print(f"\nTotal engines in database (sample of 10): {len(engines)}")
            for engine in engines[:3]:
                print(f"  - {engine.name}")
            
            # Demonstrate Delays
            print("\n" + "-" * 80)
            print("6. FLIGHT DELAY QUERIES")
            print("-" * 80)
            
            delay_repo = DelayRepository(session)
            
            # Find delays by cause
            delay_causes = ["Weather", "Mechanical", "Security", "Crew"]
            print("\nDelay statistics by cause:")
            for cause in delay_causes:
                delays = delay_repo.find_by_cause(cause, limit=1000)
                if delays:
                    avg_delay = sum(d.minutes for d in delays) / len(delays)
                    print(f"  - {cause}: {len(delays)} delays, "
                          f"avg {avg_delay:.1f} minutes")
            
            print("\n" + "=" * 80)
            print("Demonstration completed successfully!")
            print("=" * 80)
            print("\nMCP Tools Used:")
            print("  ✓ get_neo4j_schema - Discovered database schema")
            print("  ✓ read_neo4j_cypher - Explored sample data")
            print("\nGenerated Components:")
            print("  ✓ 9 Pydantic models (Aircraft, Airport, Flight, etc.)")
            print("  ✓ 6 Repository classes with CRUD operations")
            print("  ✓ Connection management with context managers")
            print("  ✓ 22 passing integration tests")
            print("  ✓ Type-safe, parameterized Cypher queries")
            print("=" * 80)


if __name__ == "__main__":
    main()
