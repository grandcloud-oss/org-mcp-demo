"""Tests for repository implementations."""

import pytest
from neo4j_client import (
    Aircraft,
    Flight,
    Airport,
    MaintenanceEvent,
    AircraftRepository,
    FlightRepository,
    AirportRepository,
    MaintenanceEventRepository,
)


class TestAircraftRepository:
    """Tests for AircraftRepository."""

    def test_create_aircraft(self, neo4j_session):
        """Test creating an aircraft."""
        repo = AircraftRepository(neo4j_session)
        aircraft = Aircraft(
            aircraft_id="AC001",
            tail_number="N12345",
            icao24="abc123",
            model="B737-800",
            operator="TestAir",
            manufacturer="Boeing"
        )
        
        created = repo.create(aircraft)
        
        assert created.aircraft_id == aircraft.aircraft_id
        assert created.tail_number == aircraft.tail_number
        assert created.model == aircraft.model

    def test_find_aircraft_by_id(self, neo4j_session):
        """Test finding aircraft by ID."""
        repo = AircraftRepository(neo4j_session)
        aircraft = Aircraft(
            aircraft_id="AC002",
            tail_number="N54321",
            icao24="def456",
            model="A320",
            operator="TestAir",
            manufacturer="Airbus"
        )
        repo.create(aircraft)
        
        found = repo.find_by_id("AC002")
        
        assert found is not None
        assert found.aircraft_id == "AC002"
        assert found.tail_number == "N54321"

    def test_find_aircraft_by_id_not_found(self, neo4j_session):
        """Test finding non-existent aircraft."""
        repo = AircraftRepository(neo4j_session)
        
        found = repo.find_by_id("NONEXISTENT")
        
        assert found is None

    def test_find_aircraft_by_tail_number(self, neo4j_session):
        """Test finding aircraft by tail number."""
        repo = AircraftRepository(neo4j_session)
        aircraft = Aircraft(
            aircraft_id="AC003",
            tail_number="N99999",
            icao24="ghi789",
            model="B777",
            operator="TestAir",
            manufacturer="Boeing"
        )
        repo.create(aircraft)
        
        found = repo.find_by_tail_number("N99999")
        
        assert found is not None
        assert found.aircraft_id == "AC003"

    def test_find_all_aircraft(self, neo4j_session):
        """Test finding all aircraft."""
        repo = AircraftRepository(neo4j_session)
        
        aircraft1 = Aircraft(
            aircraft_id="AC004",
            tail_number="N11111",
            icao24="jkl012",
            model="B737",
            operator="TestAir",
            manufacturer="Boeing"
        )
        aircraft2 = Aircraft(
            aircraft_id="AC005",
            tail_number="N22222",
            icao24="mno345",
            model="A320",
            operator="TestAir",
            manufacturer="Airbus"
        )
        
        repo.create(aircraft1)
        repo.create(aircraft2)
        
        all_aircraft = repo.find_all()
        
        assert len(all_aircraft) == 2

    def test_find_aircraft_by_operator(self, neo4j_session):
        """Test finding aircraft by operator."""
        repo = AircraftRepository(neo4j_session)
        
        aircraft1 = Aircraft(
            aircraft_id="AC006",
            tail_number="N33333",
            icao24="pqr678",
            model="B737",
            operator="SkyAir",
            manufacturer="Boeing"
        )
        aircraft2 = Aircraft(
            aircraft_id="AC007",
            tail_number="N44444",
            icao24="stu901",
            model="A320",
            operator="JetAir",
            manufacturer="Airbus"
        )
        
        repo.create(aircraft1)
        repo.create(aircraft2)
        
        sky_aircraft = repo.find_by_operator("SkyAir")
        
        assert len(sky_aircraft) == 1
        assert sky_aircraft[0].operator == "SkyAir"

    def test_update_aircraft(self, neo4j_session):
        """Test updating an aircraft."""
        repo = AircraftRepository(neo4j_session)
        
        aircraft = Aircraft(
            aircraft_id="AC008",
            tail_number="N55555",
            icao24="vwx234",
            model="B737",
            operator="OldAir",
            manufacturer="Boeing"
        )
        repo.create(aircraft)
        
        aircraft.operator = "NewAir"
        updated = repo.update(aircraft)
        
        assert updated.operator == "NewAir"
        
        # Verify the update persisted
        found = repo.find_by_id("AC008")
        assert found.operator == "NewAir"

    def test_delete_aircraft(self, neo4j_session):
        """Test deleting an aircraft."""
        repo = AircraftRepository(neo4j_session)
        
        aircraft = Aircraft(
            aircraft_id="AC009",
            tail_number="N66666",
            icao24="yzx567",
            model="B737",
            operator="TestAir",
            manufacturer="Boeing"
        )
        repo.create(aircraft)
        
        deleted = repo.delete("AC009")
        
        assert deleted is True
        
        # Verify deletion
        found = repo.find_by_id("AC009")
        assert found is None


class TestFlightRepository:
    """Tests for FlightRepository."""

    def test_create_flight(self, neo4j_session):
        """Test creating a flight."""
        repo = FlightRepository(neo4j_session)
        
        flight = Flight(
            flight_id="FL001",
            flight_number="TA123",
            aircraft_id="AC001",
            operator="TestAir",
            origin="JFK",
            destination="LAX",
            scheduled_departure="2024-01-01T10:00:00",
            scheduled_arrival="2024-01-01T13:00:00"
        )
        
        created = repo.create(flight)
        
        assert created.flight_id == flight.flight_id
        assert created.flight_number == flight.flight_number

    def test_find_flight_by_id(self, neo4j_session):
        """Test finding flight by ID."""
        repo = FlightRepository(neo4j_session)
        
        flight = Flight(
            flight_id="FL002",
            flight_number="TA456",
            aircraft_id="AC002",
            operator="TestAir",
            origin="LAX",
            destination="SFO",
            scheduled_departure="2024-01-02T10:00:00",
            scheduled_arrival="2024-01-02T11:00:00"
        )
        repo.create(flight)
        
        found = repo.find_by_id("FL002")
        
        assert found is not None
        assert found.flight_number == "TA456"

    def test_find_flights_by_aircraft(self, neo4j_session):
        """Test finding flights by aircraft."""
        repo = FlightRepository(neo4j_session)
        
        flight1 = Flight(
            flight_id="FL003",
            flight_number="TA100",
            aircraft_id="AC100",
            operator="TestAir",
            origin="JFK",
            destination="LAX",
            scheduled_departure="2024-01-01T10:00:00",
            scheduled_arrival="2024-01-01T13:00:00"
        )
        flight2 = Flight(
            flight_id="FL004",
            flight_number="TA101",
            aircraft_id="AC100",
            operator="TestAir",
            origin="LAX",
            destination="SFO",
            scheduled_departure="2024-01-02T10:00:00",
            scheduled_arrival="2024-01-02T11:00:00"
        )
        
        repo.create(flight1)
        repo.create(flight2)
        
        flights = repo.find_by_aircraft("AC100")
        
        assert len(flights) == 2

    def test_find_flights_by_route(self, neo4j_session):
        """Test finding flights by route."""
        repo = FlightRepository(neo4j_session)
        
        flight = Flight(
            flight_id="FL005",
            flight_number="TA200",
            aircraft_id="AC200",
            operator="TestAir",
            origin="JFK",
            destination="LAX",
            scheduled_departure="2024-01-01T10:00:00",
            scheduled_arrival="2024-01-01T13:00:00"
        )
        repo.create(flight)
        
        flights = repo.find_by_route("JFK", "LAX")
        
        assert len(flights) >= 1
        assert all(f.origin == "JFK" and f.destination == "LAX" for f in flights)


class TestAirportRepository:
    """Tests for AirportRepository."""

    def test_create_airport(self, neo4j_session):
        """Test creating an airport."""
        repo = AirportRepository(neo4j_session)
        
        airport = Airport(
            airport_id="JFK",
            name="John F. Kennedy International",
            city="New York",
            country="USA",
            iata="JFK",
            icao="KJFK",
            lat=40.6413,
            lon=-73.7781
        )
        
        created = repo.create(airport)
        
        assert created.airport_id == airport.airport_id
        assert created.name == airport.name

    def test_find_airport_by_iata(self, neo4j_session):
        """Test finding airport by IATA code."""
        repo = AirportRepository(neo4j_session)
        
        airport = Airport(
            airport_id="LAX",
            name="Los Angeles International",
            city="Los Angeles",
            country="USA",
            iata="LAX",
            icao="KLAX",
            lat=33.9416,
            lon=-118.4085
        )
        repo.create(airport)
        
        found = repo.find_by_iata("LAX")
        
        assert found is not None
        assert found.city == "Los Angeles"

    def test_find_airports_by_country(self, neo4j_session):
        """Test finding airports by country."""
        repo = AirportRepository(neo4j_session)
        
        airport1 = Airport(
            airport_id="JFK2",
            name="John F. Kennedy International",
            city="New York",
            country="USA",
            iata="JFK",
            icao="KJFK",
            lat=40.6413,
            lon=-73.7781
        )
        airport2 = Airport(
            airport_id="LAX2",
            name="Los Angeles International",
            city="Los Angeles",
            country="USA",
            iata="LAX",
            icao="KLAX",
            lat=33.9416,
            lon=-118.4085
        )
        
        repo.create(airport1)
        repo.create(airport2)
        
        us_airports = repo.find_by_country("USA")
        
        assert len(us_airports) == 2


class TestMaintenanceEventRepository:
    """Tests for MaintenanceEventRepository."""

    def test_create_maintenance_event(self, neo4j_session):
        """Test creating a maintenance event."""
        repo = MaintenanceEventRepository(neo4j_session)
        
        event = MaintenanceEvent(
            event_id="ME001",
            aircraft_id="AC001",
            system_id="SYS001",
            component_id="COMP001",
            fault="Engine vibration",
            severity="HIGH",
            corrective_action="Replace bearings",
            reported_at="2024-01-01T10:00:00"
        )
        
        created = repo.create(event)
        
        assert created.event_id == event.event_id
        assert created.fault == event.fault

    def test_find_maintenance_events_by_aircraft(self, neo4j_session):
        """Test finding maintenance events by aircraft."""
        repo = MaintenanceEventRepository(neo4j_session)
        
        event1 = MaintenanceEvent(
            event_id="ME002",
            aircraft_id="AC999",
            system_id="SYS001",
            component_id="COMP001",
            fault="Hydraulic leak",
            severity="MEDIUM",
            corrective_action="Replace seal",
            reported_at="2024-01-01T10:00:00"
        )
        event2 = MaintenanceEvent(
            event_id="ME003",
            aircraft_id="AC999",
            system_id="SYS002",
            component_id="COMP002",
            fault="Avionics fault",
            severity="LOW",
            corrective_action="Software update",
            reported_at="2024-01-02T10:00:00"
        )
        
        repo.create(event1)
        repo.create(event2)
        
        events = repo.find_by_aircraft("AC999")
        
        assert len(events) == 2

    def test_find_maintenance_events_by_severity(self, neo4j_session):
        """Test finding maintenance events by severity."""
        repo = MaintenanceEventRepository(neo4j_session)
        
        event = MaintenanceEvent(
            event_id="ME004",
            aircraft_id="AC888",
            system_id="SYS001",
            component_id="COMP001",
            fault="Critical failure",
            severity="CRITICAL",
            corrective_action="Emergency repair",
            reported_at="2024-01-01T10:00:00"
        )
        repo.create(event)
        
        critical_events = repo.find_by_severity("CRITICAL")
        
        assert len(critical_events) >= 1
        assert all(e.severity == "CRITICAL" for e in critical_events)
