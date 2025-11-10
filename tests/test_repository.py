"""Tests for repository classes."""

import pytest
from neo4j_client import (
    Aircraft,
    Airport,
    Flight,
    MaintenanceEvent,
    System,
    Delay,
    AircraftRepository,
    AirportRepository,
    FlightRepository,
    MaintenanceEventRepository,
    SystemRepository,
    DelayRepository,
)


class TestAircraftRepository:
    """Test cases for AircraftRepository."""
    
    def test_create_aircraft(self, neo4j_session):
        """Test creating a new aircraft."""
        repo = AircraftRepository(neo4j_session)
        aircraft = Aircraft(
            aircraft_id="AC001",
            tail_number="N12345",
            icao24="ABC123",
            model="B737-800",
            operator="TestAir",
            manufacturer="Boeing"
        )
        
        result = repo.create(aircraft)
        assert result.aircraft_id == "AC001"
        assert result.tail_number == "N12345"
    
    def test_find_by_id(self, neo4j_session):
        """Test finding aircraft by ID."""
        repo = AircraftRepository(neo4j_session)
        aircraft = Aircraft(
            aircraft_id="AC002",
            tail_number="N67890",
            icao24="DEF456",
            model="A320-200",
            operator="SkyAir",
            manufacturer="Airbus"
        )
        repo.create(aircraft)
        
        found = repo.find_by_id("AC002")
        assert found is not None
        assert found.aircraft_id == "AC002"
        assert found.model == "A320-200"
    
    def test_find_by_id_not_found(self, neo4j_session):
        """Test finding non-existent aircraft returns None."""
        repo = AircraftRepository(neo4j_session)
        found = repo.find_by_id("NONEXISTENT")
        assert found is None
    
    def test_find_by_tail_number(self, neo4j_session):
        """Test finding aircraft by tail number."""
        repo = AircraftRepository(neo4j_session)
        aircraft = Aircraft(
            aircraft_id="AC003",
            tail_number="N99999",
            icao24="GHI789",
            model="B787-9",
            operator="GlobalAir",
            manufacturer="Boeing"
        )
        repo.create(aircraft)
        
        found = repo.find_by_tail_number("N99999")
        assert found is not None
        assert found.aircraft_id == "AC003"
    
    def test_find_by_operator(self, neo4j_session):
        """Test finding all aircraft for an operator."""
        repo = AircraftRepository(neo4j_session)
        
        aircraft1 = Aircraft(
            aircraft_id="AC004",
            tail_number="N11111",
            icao24="JKL012",
            model="B737-800",
            operator="TestOp",
            manufacturer="Boeing"
        )
        aircraft2 = Aircraft(
            aircraft_id="AC005",
            tail_number="N22222",
            icao24="MNO345",
            model="B737-900",
            operator="TestOp",
            manufacturer="Boeing"
        )
        repo.create(aircraft1)
        repo.create(aircraft2)
        
        results = repo.find_by_operator("TestOp")
        assert len(results) == 2
        assert all(a.operator == "TestOp" for a in results)
    
    def test_find_all(self, neo4j_session):
        """Test finding all aircraft."""
        repo = AircraftRepository(neo4j_session)
        
        for i in range(3):
            aircraft = Aircraft(
                aircraft_id=f"AC{100+i}",
                tail_number=f"N{1000+i}",
                icao24=f"TEST{i}",
                model="B737-800",
                operator="TestAir",
                manufacturer="Boeing"
            )
            repo.create(aircraft)
        
        results = repo.find_all(limit=10)
        assert len(results) >= 3
    
    def test_delete_aircraft(self, neo4j_session):
        """Test deleting an aircraft."""
        repo = AircraftRepository(neo4j_session)
        aircraft = Aircraft(
            aircraft_id="AC999",
            tail_number="N99999",
            icao24="DEL999",
            model="B737-800",
            operator="DeleteAir",
            manufacturer="Boeing"
        )
        repo.create(aircraft)
        
        # Verify it exists
        found = repo.find_by_id("AC999")
        assert found is not None
        
        # Delete it
        deleted = repo.delete("AC999")
        assert deleted is True
        
        # Verify it's gone
        found = repo.find_by_id("AC999")
        assert found is None


class TestAirportRepository:
    """Test cases for AirportRepository."""
    
    def test_create_airport(self, neo4j_session):
        """Test creating a new airport."""
        repo = AirportRepository(neo4j_session)
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
        
        result = repo.create(airport)
        assert result.airport_id == "JFK"
        assert result.iata == "JFK"
    
    def test_find_by_iata(self, neo4j_session):
        """Test finding airport by IATA code."""
        repo = AirportRepository(neo4j_session)
        airport = Airport(
            airport_id="LAX",
            iata="LAX",
            icao="KLAX",
            name="Los Angeles International",
            city="Los Angeles",
            country="USA",
            lat=33.9416,
            lon=-118.4085
        )
        repo.create(airport)
        
        found = repo.find_by_iata("LAX")
        assert found is not None
        assert found.city == "Los Angeles"
    
    def test_find_by_country(self, neo4j_session):
        """Test finding airports by country."""
        repo = AirportRepository(neo4j_session)
        
        airport1 = Airport(
            airport_id="ORD",
            iata="ORD",
            icao="KORD",
            name="O'Hare International",
            city="Chicago",
            country="USA",
            lat=41.9742,
            lon=-87.9073
        )
        airport2 = Airport(
            airport_id="ATL",
            iata="ATL",
            icao="KATL",
            name="Hartsfield-Jackson Atlanta",
            city="Atlanta",
            country="USA",
            lat=33.6407,
            lon=-84.4277
        )
        repo.create(airport1)
        repo.create(airport2)
        
        results = repo.find_by_country("USA")
        assert len(results) >= 2


class TestFlightRepository:
    """Test cases for FlightRepository."""
    
    def test_create_flight(self, neo4j_session):
        """Test creating a new flight."""
        repo = FlightRepository(neo4j_session)
        flight = Flight(
            flight_id="FL001",
            flight_number="EX100",
            aircraft_id="AC001",
            operator="TestAir",
            origin="JFK",
            destination="LAX",
            scheduled_departure="2024-01-01T10:00:00",
            scheduled_arrival="2024-01-01T13:00:00"
        )
        
        result = repo.create(flight)
        assert result.flight_id == "FL001"
        assert result.flight_number == "EX100"
    
    def test_find_by_id(self, neo4j_session):
        """Test finding flight by ID."""
        repo = FlightRepository(neo4j_session)
        flight = Flight(
            flight_id="FL002",
            flight_number="EX200",
            aircraft_id="AC002",
            operator="TestAir",
            origin="ORD",
            destination="SFO",
            scheduled_departure="2024-01-02T09:00:00",
            scheduled_arrival="2024-01-02T11:00:00"
        )
        repo.create(flight)
        
        found = repo.find_by_id("FL002")
        assert found is not None
        assert found.origin == "ORD"
        assert found.destination == "SFO"
    
    def test_find_by_aircraft(self, neo4j_session):
        """Test finding flights by aircraft."""
        repo = FlightRepository(neo4j_session)
        
        flight1 = Flight(
            flight_id="FL003",
            flight_number="EX300",
            aircraft_id="AC100",
            operator="TestAir",
            origin="JFK",
            destination="LAX",
            scheduled_departure="2024-01-03T10:00:00",
            scheduled_arrival="2024-01-03T13:00:00"
        )
        flight2 = Flight(
            flight_id="FL004",
            flight_number="EX400",
            aircraft_id="AC100",
            operator="TestAir",
            origin="LAX",
            destination="JFK",
            scheduled_departure="2024-01-04T14:00:00",
            scheduled_arrival="2024-01-04T22:00:00"
        )
        repo.create(flight1)
        repo.create(flight2)
        
        results = repo.find_by_aircraft("AC100")
        assert len(results) == 2
    
    def test_find_by_route(self, neo4j_session):
        """Test finding flights by route."""
        repo = FlightRepository(neo4j_session)
        
        flight = Flight(
            flight_id="FL005",
            flight_number="EX500",
            aircraft_id="AC200",
            operator="TestAir",
            origin="ATL",
            destination="MIA",
            scheduled_departure="2024-01-05T08:00:00",
            scheduled_arrival="2024-01-05T10:00:00"
        )
        repo.create(flight)
        
        results = repo.find_by_route("ATL", "MIA")
        assert len(results) >= 1
        assert results[0].origin == "ATL"
        assert results[0].destination == "MIA"


class TestMaintenanceEventRepository:
    """Test cases for MaintenanceEventRepository."""
    
    def test_create_maintenance_event(self, neo4j_session):
        """Test creating a maintenance event."""
        repo = MaintenanceEventRepository(neo4j_session)
        event = MaintenanceEvent(
            event_id="ME001",
            aircraft_id="AC001",
            system_id="SYS001",
            component_id="COMP001",
            fault="Oil leak detected",
            severity="CRITICAL",
            reported_at="2024-01-01T10:00:00",
            corrective_action="Replaced seal"
        )
        
        result = repo.create(event)
        assert result.event_id == "ME001"
        assert result.severity == "CRITICAL"
    
    def test_find_by_aircraft(self, neo4j_session):
        """Test finding maintenance events by aircraft."""
        repo = MaintenanceEventRepository(neo4j_session)
        
        event1 = MaintenanceEvent(
            event_id="ME002",
            aircraft_id="AC500",
            system_id="SYS002",
            component_id="COMP002",
            fault="Sensor malfunction",
            severity="MINOR",
            reported_at="2024-01-02T10:00:00",
            corrective_action="Recalibrated sensor"
        )
        event2 = MaintenanceEvent(
            event_id="ME003",
            aircraft_id="AC500",
            system_id="SYS003",
            component_id="COMP003",
            fault="Hydraulic pressure low",
            severity="MAJOR",
            reported_at="2024-01-03T10:00:00",
            corrective_action="Replaced hydraulic pump"
        )
        repo.create(event1)
        repo.create(event2)
        
        results = repo.find_by_aircraft("AC500")
        assert len(results) == 2
    
    def test_find_by_severity(self, neo4j_session):
        """Test finding maintenance events by severity."""
        repo = MaintenanceEventRepository(neo4j_session)
        
        event = MaintenanceEvent(
            event_id="ME004",
            aircraft_id="AC600",
            system_id="SYS004",
            component_id="COMP004",
            fault="Critical failure",
            severity="CRITICAL",
            reported_at="2024-01-04T10:00:00",
            corrective_action="Emergency repair"
        )
        repo.create(event)
        
        results = repo.find_by_severity("CRITICAL")
        assert len(results) >= 1
        assert all(e.severity == "CRITICAL" for e in results)


class TestSystemRepository:
    """Test cases for SystemRepository."""
    
    def test_create_system(self, neo4j_session):
        """Test creating a system."""
        repo = SystemRepository(neo4j_session)
        system = System(
            system_id="SYS001",
            aircraft_id="AC001",
            name="Engine #1",
            type="Engine"
        )
        
        result = repo.create(system)
        assert result.system_id == "SYS001"
        assert result.type == "Engine"
    
    def test_find_by_aircraft(self, neo4j_session):
        """Test finding systems by aircraft."""
        repo = SystemRepository(neo4j_session)
        
        system1 = System(
            system_id="SYS100",
            aircraft_id="AC700",
            name="Engine #1",
            type="Engine"
        )
        system2 = System(
            system_id="SYS101",
            aircraft_id="AC700",
            name="Hydraulics",
            type="Hydraulics"
        )
        repo.create(system1)
        repo.create(system2)
        
        results = repo.find_by_aircraft("AC700")
        assert len(results) == 2
    
    def test_find_by_type(self, neo4j_session):
        """Test finding systems by type."""
        repo = SystemRepository(neo4j_session)
        
        system = System(
            system_id="SYS200",
            aircraft_id="AC800",
            name="Avionics Suite",
            type="Avionics"
        )
        repo.create(system)
        
        results = repo.find_by_type("Avionics")
        assert len(results) >= 1
        assert all(s.type == "Avionics" for s in results)


class TestDelayRepository:
    """Test cases for DelayRepository."""
    
    def test_find_by_flight(self, neo4j_session):
        """Test finding delays by flight."""
        repo = DelayRepository(neo4j_session)
        
        # Create delay directly in database
        neo4j_session.run(
            """
            CREATE (d:Delay {
                delay_id: $delay_id,
                flight_id: $flight_id,
                minutes: $minutes,
                cause: $cause
            })
            """,
            delay_id="DLY001",
            flight_id="FL100",
            minutes=30,
            cause="Weather"
        )
        
        results = repo.find_by_flight("FL100")
        assert len(results) == 1
        assert results[0].minutes == 30
    
    def test_find_by_cause(self, neo4j_session):
        """Test finding delays by cause."""
        repo = DelayRepository(neo4j_session)
        
        # Create delay directly in database
        neo4j_session.run(
            """
            CREATE (d:Delay {
                delay_id: $delay_id,
                flight_id: $flight_id,
                minutes: $minutes,
                cause: $cause
            })
            """,
            delay_id="DLY002",
            flight_id="FL200",
            minutes=45,
            cause="Mechanical"
        )
        
        results = repo.find_by_cause("Mechanical")
        assert len(results) >= 1
        assert all(d.cause == "Mechanical" for d in results)
