"""Integration tests for repository classes."""

import pytest
from neo4j_client.models import Aircraft, Airport, Flight, Delay, MaintenanceEvent
from neo4j_client.repository import (
    AircraftRepository,
    AirportRepository,
    FlightRepository,
    DelayRepository,
    MaintenanceEventRepository,
)
from neo4j_client.exceptions import QueryError, NotFoundError


class TestAircraftRepository:
    """Tests for AircraftRepository."""
    
    def test_create_aircraft(self, session):
        """Test creating an aircraft."""
        repo = AircraftRepository(session)
        aircraft = Aircraft(
            aircraft_id="AC001",
            tail_number="N12345",
            icao24="ABC123",
            model="Boeing 737-800",
            manufacturer="Boeing",
            operator="Test Airlines"
        )
        
        result = repo.create(aircraft)
        assert result.aircraft_id == "AC001"
        assert result.tail_number == "N12345"
    
    def test_find_by_id(self, session):
        """Test finding aircraft by ID."""
        repo = AircraftRepository(session)
        aircraft = Aircraft(
            aircraft_id="AC002",
            tail_number="N54321",
            icao24="DEF456",
            model="Airbus A320",
            manufacturer="Airbus",
            operator="Test Airlines"
        )
        repo.create(aircraft)
        
        found = repo.find_by_id("AC002")
        assert found is not None
        assert found.aircraft_id == "AC002"
        assert found.model == "Airbus A320"
    
    def test_find_by_id_not_found(self, session):
        """Test finding non-existent aircraft."""
        repo = AircraftRepository(session)
        found = repo.find_by_id("NONEXISTENT")
        assert found is None
    
    def test_find_by_tail_number(self, session):
        """Test finding aircraft by tail number."""
        repo = AircraftRepository(session)
        aircraft = Aircraft(
            aircraft_id="AC003",
            tail_number="N99999",
            model="Boeing 777",
            manufacturer="Boeing",
            operator="Test Airlines"
        )
        repo.create(aircraft)
        
        found = repo.find_by_tail_number("N99999")
        assert found is not None
        assert found.aircraft_id == "AC003"
    
    def test_find_all(self, session):
        """Test finding all aircraft."""
        repo = AircraftRepository(session)
        
        aircraft1 = Aircraft(
            aircraft_id="AC010",
            tail_number="N10001",
            model="Boeing 737",
            manufacturer="Boeing",
            operator="Airline A"
        )
        aircraft2 = Aircraft(
            aircraft_id="AC011",
            tail_number="N10002",
            model="Airbus A320",
            manufacturer="Airbus",
            operator="Airline B"
        )
        
        repo.create(aircraft1)
        repo.create(aircraft2)
        
        all_aircraft = repo.find_all()
        assert len(all_aircraft) >= 2
    
    def test_find_by_operator(self, session):
        """Test finding aircraft by operator."""
        repo = AircraftRepository(session)
        
        aircraft = Aircraft(
            aircraft_id="AC020",
            tail_number="N20001",
            model="Boeing 747",
            manufacturer="Boeing",
            operator="United Airlines"
        )
        repo.create(aircraft)
        
        found = repo.find_by_operator("United Airlines")
        assert len(found) >= 1
        assert any(a.aircraft_id == "AC020" for a in found)
    
    def test_delete_aircraft(self, session):
        """Test deleting an aircraft."""
        repo = AircraftRepository(session)
        
        aircraft = Aircraft(
            aircraft_id="AC030",
            tail_number="N30001",
            model="Boeing 787",
            manufacturer="Boeing",
            operator="Test Airlines"
        )
        repo.create(aircraft)
        
        deleted = repo.delete("AC030")
        assert deleted is True
        
        found = repo.find_by_id("AC030")
        assert found is None


class TestAirportRepository:
    """Tests for AirportRepository."""
    
    def test_create_airport(self, session):
        """Test creating an airport."""
        repo = AirportRepository(session)
        airport = Airport(
            airport_id="APT001",
            name="Test International Airport",
            iata="TST",
            icao="KTST",
            city="Test City",
            country="Test Country",
            lat=40.7128,
            lon=-74.0060
        )
        
        result = repo.create(airport)
        assert result.airport_id == "APT001"
        assert result.iata == "TST"
    
    def test_find_by_iata(self, session):
        """Test finding airport by IATA code."""
        repo = AirportRepository(session)
        airport = Airport(
            airport_id="APT002",
            name="JFK International",
            iata="JFK",
            icao="KJFK",
            city="New York",
            country="USA",
            lat=40.6413,
            lon=-73.7781
        )
        repo.create(airport)
        
        found = repo.find_by_iata("JFK")
        assert found is not None
        assert found.name == "JFK International"
    
    def test_find_by_country(self, session):
        """Test finding airports by country."""
        repo = AirportRepository(session)
        
        airport1 = Airport(
            airport_id="APT010",
            name="Airport One",
            iata="AP1",
            icao="KAP1",
            city="City One",
            country="TestLand",
            lat=40.0,
            lon=-70.0
        )
        airport2 = Airport(
            airport_id="APT011",
            name="Airport Two",
            iata="AP2",
            icao="KAP2",
            city="City Two",
            country="TestLand",
            lat=41.0,
            lon=-71.0
        )
        
        repo.create(airport1)
        repo.create(airport2)
        
        found = repo.find_by_country("TestLand")
        assert len(found) >= 2


class TestFlightRepository:
    """Tests for FlightRepository."""
    
    def test_create_flight(self, session):
        """Test creating a flight."""
        repo = FlightRepository(session)
        flight = Flight(
            flight_id="FL001",
            flight_number="TS123",
            aircraft_id="AC001",
            operator="Test Airlines",
            origin="JFK",
            destination="LAX",
            scheduled_departure="2024-01-01T08:00:00Z",
            scheduled_arrival="2024-01-01T14:00:00Z"
        )
        
        result = repo.create(flight)
        assert result.flight_id == "FL001"
        assert result.flight_number == "TS123"
    
    def test_find_by_flight_number(self, session):
        """Test finding flights by flight number."""
        repo = FlightRepository(session)
        flight = Flight(
            flight_id="FL002",
            flight_number="TS456",
            aircraft_id="AC002",
            operator="Test Airlines",
            origin="LAX",
            destination="JFK",
            scheduled_departure="2024-01-02T10:00:00Z",
            scheduled_arrival="2024-01-02T18:00:00Z"
        )
        repo.create(flight)
        
        found = repo.find_by_flight_number("TS456")
        assert len(found) >= 1
        assert any(f.flight_id == "FL002" for f in found)
    
    def test_find_by_route(self, session):
        """Test finding flights by route."""
        repo = FlightRepository(session)
        flight = Flight(
            flight_id="FL010",
            flight_number="TS789",
            aircraft_id="AC010",
            operator="Test Airlines",
            origin="ORD",
            destination="DFW",
            scheduled_departure="2024-01-03T09:00:00Z",
            scheduled_arrival="2024-01-03T13:00:00Z"
        )
        repo.create(flight)
        
        found = repo.find_by_route("ORD", "DFW")
        assert len(found) >= 1
        assert any(f.flight_id == "FL010" for f in found)
    
    def test_get_flight_with_delays(self, session):
        """Test getting flight with associated delays."""
        # Create flight
        flight_repo = FlightRepository(session)
        flight = Flight(
            flight_id="FL020",
            flight_number="TS999",
            aircraft_id="AC020",
            operator="Test Airlines",
            origin="ATL",
            destination="MIA",
            scheduled_departure="2024-01-04T07:00:00Z",
            scheduled_arrival="2024-01-04T10:00:00Z"
        )
        flight_repo.create(flight)
        
        # Create delays and link to flight
        delay_repo = DelayRepository(session)
        delay1 = Delay(
            delay_id="DLY001",
            flight_id="FL020",
            cause="Weather",
            minutes=30
        )
        delay2 = Delay(
            delay_id="DLY002",
            flight_id="FL020",
            cause="Maintenance",
            minutes=15
        )
        delay_repo.create(delay1)
        delay_repo.create(delay2)
        
        # Link delays to flight
        session.run("""
            MATCH (f:Flight {flight_id: $flight_id})
            MATCH (d:Delay {flight_id: $flight_id})
            MERGE (f)-[:HAS_DELAY]->(d)
        """, flight_id="FL020")
        
        # Get flight with delays
        result = flight_repo.get_flight_with_delays("FL020")
        assert result["flight"].flight_id == "FL020"
        assert len(result["delays"]) == 2


class TestDelayRepository:
    """Tests for DelayRepository."""
    
    def test_create_delay(self, session):
        """Test creating a delay."""
        repo = DelayRepository(session)
        delay = Delay(
            delay_id="DLY010",
            flight_id="FL010",
            cause="Weather",
            minutes=45
        )
        
        result = repo.create(delay)
        assert result.delay_id == "DLY010"
        assert result.minutes == 45
    
    def test_find_by_cause(self, session):
        """Test finding delays by cause."""
        repo = DelayRepository(session)
        delay = Delay(
            delay_id="DLY020",
            flight_id="FL020",
            cause="Mechanical",
            minutes=60
        )
        repo.create(delay)
        
        found = repo.find_by_cause("Mechanical")
        assert len(found) >= 1
        assert any(d.delay_id == "DLY020" for d in found)


class TestMaintenanceEventRepository:
    """Tests for MaintenanceEventRepository."""
    
    def test_create_maintenance_event(self, session):
        """Test creating a maintenance event."""
        repo = MaintenanceEventRepository(session)
        event = MaintenanceEvent(
            event_id="ME001",
            aircraft_id="AC001",
            component_id="COMP001",
            system_id="SYS001",
            fault="Hydraulic leak",
            severity="High",
            corrective_action="Replaced hydraulic pump",
            reported_at="2024-01-01T10:00:00Z"
        )
        
        result = repo.create(event)
        assert result.event_id == "ME001"
        assert result.severity == "High"
    
    def test_find_by_aircraft(self, session):
        """Test finding maintenance events for an aircraft."""
        repo = MaintenanceEventRepository(session)
        event = MaintenanceEvent(
            event_id="ME010",
            aircraft_id="AC010",
            component_id="COMP010",
            system_id="SYS010",
            fault="Engine warning light",
            severity="Medium",
            corrective_action="Replaced sensor",
            reported_at="2024-01-02T14:00:00Z"
        )
        repo.create(event)
        
        found = repo.find_by_aircraft("AC010")
        assert len(found) >= 1
        assert any(e.event_id == "ME010" for e in found)
    
    def test_find_by_severity(self, session):
        """Test finding maintenance events by severity."""
        repo = MaintenanceEventRepository(session)
        event = MaintenanceEvent(
            event_id="ME020",
            aircraft_id="AC020",
            component_id="COMP020",
            system_id="SYS020",
            fault="Critical system failure",
            severity="Critical",
            corrective_action="Emergency repair",
            reported_at="2024-01-03T16:00:00Z"
        )
        repo.create(event)
        
        found = repo.find_by_severity("Critical")
        assert len(found) >= 1
        assert any(e.event_id == "ME020" for e in found)
