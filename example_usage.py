"""Example usage of the Neo4j airplane database client.

This script demonstrates how to use the client library to interact
with the airplane database.
"""

import os
from neo4j_client import (
    Neo4jConnection,
    AircraftRepository,
    AirportRepository,
    FlightRepository,
    MaintenanceEventRepository,
    DelayRepository,
    Aircraft,
    Flight,
)


def main():
    """Demonstrate client usage."""
    # Get connection details from environment variables
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    username = os.getenv("NEO4J_USERNAME", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")
    database = os.getenv("NEO4J_DATABASE", "neo4j")
    
    print(f"Connecting to Neo4j at {uri}...")
    
    # Use connection as a context manager for automatic cleanup
    with Neo4jConnection(uri, username, password, database) as conn:
        session = conn.get_session()
        
        # Example 1: Query Aircraft
        print("\n=== Aircraft in Fleet ===")
        aircraft_repo = AircraftRepository(session)
        aircraft_list = aircraft_repo.find_all(limit=5)
        for aircraft in aircraft_list:
            print(f"  {aircraft.tail_number}: {aircraft.manufacturer} {aircraft.model}")
            print(f"    Operator: {aircraft.operator}")
        
        # Example 2: Query Airports
        print("\n=== Airports ===")
        airport_repo = AirportRepository(session)
        airports = airport_repo.find_all(limit=5)
        for airport in airports:
            print(f"  {airport.iata} ({airport.icao}): {airport.name}")
            print(f"    Location: {airport.city}, {airport.country}")
            print(f"    Coordinates: {airport.lat}, {airport.lon}")
        
        # Example 3: Query Flights
        print("\n=== Recent Flights ===")
        flight_repo = FlightRepository(session)
        flights = flight_repo.find_all(limit=5)
        for flight in flights:
            print(f"  {flight.flight_number}: {flight.origin} → {flight.destination}")
            print(f"    Operator: {flight.operator}")
            print(f"    Departure: {flight.scheduled_departure}")
        
        # Example 4: Query Flights with Delays
        if flights:
            print("\n=== Flight Details with Delays ===")
            flight_id = flights[0].flight_id
            try:
                flight_data = flight_repo.get_flight_with_delays(flight_id)
                flight = flight_data["flight"]
                delays = flight_data["delays"]
                print(f"  Flight: {flight.flight_number}")
                print(f"  Delays: {len(delays)}")
                for delay in delays:
                    print(f"    - {delay.cause}: {delay.minutes} minutes")
            except Exception as e:
                print(f"  No delays found for flight {flight_id}")
        
        # Example 5: Query Maintenance Events
        print("\n=== Recent Maintenance Events ===")
        maintenance_repo = MaintenanceEventRepository(session)
        events = maintenance_repo.find_all(limit=5)
        for event in events:
            print(f"  Aircraft: {event.aircraft_id}")
            print(f"    Fault: {event.fault} (Severity: {event.severity})")
            print(f"    Action: {event.corrective_action}")
            print(f"    Reported: {event.reported_at}")
        
        # Example 6: Find aircraft by operator
        if aircraft_list:
            print(f"\n=== Aircraft operated by {aircraft_list[0].operator} ===")
            operator_aircraft = aircraft_repo.find_by_operator(aircraft_list[0].operator)
            print(f"  Found {len(operator_aircraft)} aircraft")
            for aircraft in operator_aircraft[:3]:
                print(f"    - {aircraft.tail_number}: {aircraft.model}")
        
        # Example 7: Find airports by country
        if airports:
            print(f"\n=== Airports in {airports[0].country} ===")
            country_airports = airport_repo.find_by_country(airports[0].country)
            print(f"  Found {len(country_airports)} airports")
            for airport in country_airports[:3]:
                print(f"    - {airport.iata}: {airport.name}")
        
        session.close()
    
    print("\n✅ Example completed successfully!")


if __name__ == "__main__":
    main()
