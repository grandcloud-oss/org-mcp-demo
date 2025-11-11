"""Integration tests for airplane client repositories."""

import pytest
from airplane_client import (
    Neo4jConnection,
    AircraftRepository,
    AirportRepository,
    FlightRepository,
    SystemRepository,
    MaintenanceEventRepository,
    Aircraft,
    Airport,
    Flight,
    System,
    MaintenanceEvent,
)


class TestAircraftRepository:
    """Tests for AircraftRepository."""
    
    def test_create_aircraft(self, neo4j_connection):
        """Test creating an aircraft."""
        repo = AircraftRepository(neo4j_connection)
        aircraft = Aircraft(
            aircraft_id="AC001",
            tail_number="N12345",
            icao24="ABC123",
            model="Boeing 737",
            operator="Test Airlines",
            manufacturer="Boeing"
        )
        
        created = repo.create(aircraft)
        assert created.aircraft_id == "AC001"
        assert created.tail_number == "N12345"
    
    def test_find_aircraft_by_id(self, neo4j_connection):
        """Test finding an aircraft by ID."""
        repo = AircraftRepository(neo4j_connection)
        aircraft = Aircraft(
            aircraft_id="AC002",
            tail_number="N54321",
            icao24="XYZ789",
            model="Airbus A320",
            operator="Test Airlines",
            manufacturer="Airbus"
        )
        repo.create(aircraft)
        
        found = repo.find_by_id("AC002")
        assert found is not None
        assert found.aircraft_id == "AC002"
        assert found.model == "Airbus A320"
    
    def test_find_aircraft_not_found(self, neo4j_connection):
        """Test finding a non-existent aircraft."""
        repo = AircraftRepository(neo4j_connection)
        found = repo.find_by_id("NONEXISTENT")
        assert found is None
    
    def test_find_all_aircraft(self, neo4j_connection):
        """Test finding all aircraft."""
        repo = AircraftRepository(neo4j_connection)
        
        # Create multiple aircraft
        for i in range(3):
            aircraft = Aircraft(
                aircraft_id=f"AC{i:03d}",
                tail_number=f"N{i:05d}",
                icao24=f"ICO{i:03d}",
                model=f"Model {i}",
                operator="Test Airlines",
                manufacturer="Test Manufacturer"
            )
            repo.create(aircraft)
        
        all_aircraft = repo.find_all(limit=10)
        assert len(all_aircraft) >= 3
    
    def test_delete_aircraft(self, neo4j_connection):
        """Test deleting an aircraft."""
        repo = AircraftRepository(neo4j_connection)
        aircraft = Aircraft(
            aircraft_id="AC999",
            tail_number="N99999",
            icao24="DEL999",
            model="Test Model",
            operator="Test Airlines",
            manufacturer="Test Manufacturer"
        )
        repo.create(aircraft)
        
        # Delete and verify
        deleted = repo.delete("AC999")
        assert deleted is True
        
        # Verify it's gone
        found = repo.find_by_id("AC999")
        assert found is None


class TestAirportRepository:
    """Tests for AirportRepository."""
    
    def test_create_airport(self, neo4j_connection):
        """Test creating an airport."""
        repo = AirportRepository(neo4j_connection)
        airport = Airport(
            airport_id="AP001",
            name="Test Airport",
            iata="TST",
            icao="KTST",
            city="Test City",
            country="Test Country",
            lat=40.7128,
            lon=-74.0060
        )
        
        created = repo.create(airport)
        assert created.airport_id == "AP001"
        assert created.iata == "TST"
    
    def test_find_airport_by_id(self, neo4j_connection):
        """Test finding an airport by ID."""
        repo = AirportRepository(neo4j_connection)
        airport = Airport(
            airport_id="AP002",
            name="Second Test Airport",
            iata="ST2",
            icao="KST2",
            city="Test City 2",
            country="Test Country",
            lat=41.0,
            lon=-75.0
        )
        repo.create(airport)
        
        found = repo.find_by_id("AP002")
        assert found is not None
        assert found.iata == "ST2"
    
    def test_find_airport_by_iata(self, neo4j_connection):
        """Test finding an airport by IATA code."""
        repo = AirportRepository(neo4j_connection)
        airport = Airport(
            airport_id="AP003",
            name="Third Test Airport",
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
        assert found.airport_id == "AP003"


class TestFlightRepository:
    """Tests for FlightRepository."""
    
    def test_create_flight(self, neo4j_connection):
        """Test creating a flight."""
        repo = FlightRepository(neo4j_connection)
        flight = Flight(
            flight_id="FL001",
            flight_number="AA100",
            aircraft_id="AC001",
            operator="Test Airlines",
            origin="JFK",
            destination="LAX",
            scheduled_departure="2024-01-01T10:00:00",
            scheduled_arrival="2024-01-01T13:00:00"
        )
        
        created = repo.create(flight)
        assert created.flight_id == "FL001"
        assert created.flight_number == "AA100"
    
    def test_find_flights_by_aircraft(self, neo4j_connection):
        """Test finding flights by aircraft ID."""
        repo = FlightRepository(neo4j_connection)
        
        # Create multiple flights for the same aircraft
        for i in range(3):
            flight = Flight(
                flight_id=f"FL{i:03d}",
                flight_number=f"AA{i:03d}",
                aircraft_id="AC999",
                operator="Test Airlines",
                origin="JFK",
                destination="LAX",
                scheduled_departure=f"2024-01-{i+1:02d}T10:00:00",
                scheduled_arrival=f"2024-01-{i+1:02d}T13:00:00"
            )
            repo.create(flight)
        
        flights = repo.find_by_aircraft("AC999")
        assert len(flights) == 3


class TestSystemRepository:
    """Tests for SystemRepository."""
    
    def test_create_system(self, neo4j_connection):
        """Test creating a system."""
        repo = SystemRepository(neo4j_connection)
        system = System(
            system_id="SYS001",
            aircraft_id="AC001",
            name="Hydraulic System",
            type="Hydraulic"
        )
        
        created = repo.create(system)
        assert created.system_id == "SYS001"
        assert created.name == "Hydraulic System"
    
    def test_find_systems_by_aircraft(self, neo4j_connection):
        """Test finding systems by aircraft ID."""
        repo = SystemRepository(neo4j_connection)
        
        # Create multiple systems for the same aircraft
        for i in range(2):
            system = System(
                system_id=f"SYS{i:03d}",
                aircraft_id="AC777",
                name=f"System {i}",
                type=f"Type {i}"
            )
            repo.create(system)
        
        systems = repo.find_by_aircraft("AC777")
        assert len(systems) == 2


class TestMaintenanceEventRepository:
    """Tests for MaintenanceEventRepository."""
    
    def test_create_maintenance_event(self, neo4j_connection):
        """Test creating a maintenance event."""
        repo = MaintenanceEventRepository(neo4j_connection)
        event = MaintenanceEvent(
            event_id="ME001",
            aircraft_id="AC001",
            system_id="SYS001",
            component_id="COMP001",
            fault="Hydraulic leak",
            severity="High",
            reported_at="2024-01-01T12:00:00",
            corrective_action="Replace hydraulic line"
        )
        
        created = repo.create(event)
        assert created.event_id == "ME001"
        assert created.severity == "High"
    
    def test_find_events_by_aircraft(self, neo4j_connection):
        """Test finding maintenance events by aircraft ID."""
        repo = MaintenanceEventRepository(neo4j_connection)
        
        # Create multiple events for the same aircraft
        for i in range(3):
            event = MaintenanceEvent(
                event_id=f"ME{i:03d}",
                aircraft_id="AC555",
                system_id=f"SYS{i:03d}",
                component_id=f"COMP{i:03d}",
                fault=f"Fault {i}",
                severity="Medium",
                reported_at=f"2024-01-{i+1:02d}T12:00:00",
                corrective_action=f"Action {i}"
            )
            repo.create(event)
        
        events = repo.find_by_aircraft("AC555")
        assert len(events) == 3
    
    def test_find_events_by_severity(self, neo4j_connection):
        """Test finding maintenance events by severity."""
        repo = MaintenanceEventRepository(neo4j_connection)
        
        # Create events with different severities
        event1 = MaintenanceEvent(
            event_id="ME100",
            aircraft_id="AC100",
            system_id="SYS100",
            component_id="COMP100",
            fault="Critical fault",
            severity="Critical",
            reported_at="2024-01-01T12:00:00",
            corrective_action="Immediate repair"
        )
        event2 = MaintenanceEvent(
            event_id="ME101",
            aircraft_id="AC101",
            system_id="SYS101",
            component_id="COMP101",
            fault="Minor fault",
            severity="Low",
            reported_at="2024-01-02T12:00:00",
            corrective_action="Scheduled maintenance"
        )
        repo.create(event1)
        repo.create(event2)
        
        critical_events = repo.find_by_severity("Critical")
        assert len(critical_events) >= 1
        assert all(e.severity == "Critical" for e in critical_events)
