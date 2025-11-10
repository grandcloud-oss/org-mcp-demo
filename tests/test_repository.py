"""Tests for repository operations."""

import pytest
from neo4j_client import (
    Aircraft,
    Airport,
    Flight,
    MaintenanceEvent,
    System,
    AircraftRepository,
    AirportRepository,
    FlightRepository,
    MaintenanceEventRepository,
    SystemRepository,
    NotFoundError,
)


class TestAircraftRepository:
    """Test cases for AircraftRepository."""
    
    def test_create_aircraft(self, connection):
        """Test creating an aircraft."""
        with connection.get_session() as session:
            repo = AircraftRepository(session)
            
            aircraft = Aircraft(
                aircraft_id="AC001",
                tail_number="N12345",
                icao24="ABC123",
                model="B737-800",
                operator="TestAir",
                manufacturer="Boeing"
            )
            
            created = repo.create(aircraft)
            assert created.aircraft_id == aircraft.aircraft_id
            assert created.tail_number == aircraft.tail_number
    
    def test_find_by_id(self, connection):
        """Test finding aircraft by ID."""
        with connection.get_session() as session:
            repo = AircraftRepository(session)
            
            aircraft = Aircraft(
                aircraft_id="AC002",
                tail_number="N67890",
                icao24="DEF456",
                model="A320-200",
                operator="SkyTest",
                manufacturer="Airbus"
            )
            
            repo.create(aircraft)
            found = repo.find_by_id("AC002")
            
            assert found is not None
            assert found.aircraft_id == "AC002"
            assert found.model == "A320-200"
    
    def test_find_by_id_not_found(self, connection):
        """Test finding non-existent aircraft."""
        with connection.get_session() as session:
            repo = AircraftRepository(session)
            found = repo.find_by_id("NONEXISTENT")
            assert found is None
    
    def test_find_by_tail_number(self, connection):
        """Test finding aircraft by tail number."""
        with connection.get_session() as session:
            repo = AircraftRepository(session)
            
            aircraft = Aircraft(
                aircraft_id="AC003",
                tail_number="N11111",
                icao24="GHI789",
                model="B787-9",
                operator="WorldAir",
                manufacturer="Boeing"
            )
            
            repo.create(aircraft)
            found = repo.find_by_tail_number("N11111")
            
            assert found is not None
            assert found.aircraft_id == "AC003"
    
    def test_find_by_operator(self, connection):
        """Test finding aircraft by operator."""
        with connection.get_session() as session:
            repo = AircraftRepository(session)
            
            aircraft1 = Aircraft(
                aircraft_id="AC004",
                tail_number="N22222",
                icao24="JKL012",
                model="B737-800",
                operator="TestOp",
                manufacturer="Boeing"
            )
            
            aircraft2 = Aircraft(
                aircraft_id="AC005",
                tail_number="N33333",
                icao24="MNO345",
                model="A320-200",
                operator="TestOp",
                manufacturer="Airbus"
            )
            
            repo.create(aircraft1)
            repo.create(aircraft2)
            
            found = repo.find_by_operator("TestOp")
            assert len(found) == 2
    
    def test_find_all(self, connection):
        """Test finding all aircraft."""
        with connection.get_session() as session:
            repo = AircraftRepository(session)
            
            aircraft1 = Aircraft(
                aircraft_id="AC006",
                tail_number="N44444",
                icao24="PQR678",
                model="B777-300ER",
                operator="GlobalAir",
                manufacturer="Boeing"
            )
            
            aircraft2 = Aircraft(
                aircraft_id="AC007",
                tail_number="N55555",
                icao24="STU901",
                model="A350-900",
                operator="IntlAir",
                manufacturer="Airbus"
            )
            
            repo.create(aircraft1)
            repo.create(aircraft2)
            
            all_aircraft = repo.find_all()
            assert len(all_aircraft) >= 2
    
    def test_update_aircraft(self, connection):
        """Test updating an aircraft."""
        with connection.get_session() as session:
            repo = AircraftRepository(session)
            
            aircraft = Aircraft(
                aircraft_id="AC008",
                tail_number="N66666",
                icao24="VWX234",
                model="B737-800",
                operator="OldOp",
                manufacturer="Boeing"
            )
            
            repo.create(aircraft)
            
            aircraft.operator = "NewOp"
            updated = repo.update(aircraft)
            
            assert updated.operator == "NewOp"
            assert updated.aircraft_id == "AC008"
    
    def test_update_nonexistent_aircraft(self, connection):
        """Test updating a non-existent aircraft."""
        with connection.get_session() as session:
            repo = AircraftRepository(session)
            
            aircraft = Aircraft(
                aircraft_id="NONEXISTENT",
                tail_number="N99999",
                icao24="ZZZ999",
                model="B747-8",
                operator="NoOp",
                manufacturer="Boeing"
            )
            
            with pytest.raises(NotFoundError):
                repo.update(aircraft)
    
    def test_delete_aircraft(self, connection):
        """Test deleting an aircraft."""
        with connection.get_session() as session:
            repo = AircraftRepository(session)
            
            aircraft = Aircraft(
                aircraft_id="AC009",
                tail_number="N77777",
                icao24="YZA567",
                model="A380-800",
                operator="MegaAir",
                manufacturer="Airbus"
            )
            
            repo.create(aircraft)
            deleted = repo.delete("AC009")
            
            assert deleted is True
            assert repo.find_by_id("AC009") is None
    
    def test_delete_nonexistent_aircraft(self, connection):
        """Test deleting a non-existent aircraft."""
        with connection.get_session() as session:
            repo = AircraftRepository(session)
            deleted = repo.delete("NONEXISTENT")
            assert deleted is False


class TestAirportRepository:
    """Test cases for AirportRepository."""
    
    def test_create_airport(self, connection):
        """Test creating an airport."""
        with connection.get_session() as session:
            repo = AirportRepository(session)
            
            airport = Airport(
                airport_id="JFK",
                name="John F. Kennedy International",
                iata="JFK",
                icao="KJFK",
                city="New York",
                country="USA",
                lat=40.6413,
                lon=-73.7781
            )
            
            created = repo.create(airport)
            assert created.airport_id == "JFK"
            assert created.name == "John F. Kennedy International"
    
    def test_find_by_iata(self, connection):
        """Test finding airport by IATA code."""
        with connection.get_session() as session:
            repo = AirportRepository(session)
            
            airport = Airport(
                airport_id="LAX",
                name="Los Angeles International",
                iata="LAX",
                icao="KLAX",
                city="Los Angeles",
                country="USA",
                lat=33.9416,
                lon=-118.4085
            )
            
            repo.create(airport)
            found = repo.find_by_iata("LAX")
            
            assert found is not None
            assert found.airport_id == "LAX"
    
    def test_find_by_country(self, connection):
        """Test finding airports by country."""
        with connection.get_session() as session:
            repo = AirportRepository(session)
            
            airport1 = Airport(
                airport_id="ORD",
                name="O'Hare International",
                iata="ORD",
                icao="KORD",
                city="Chicago",
                country="USA",
                lat=41.9742,
                lon=-87.9073
            )
            
            airport2 = Airport(
                airport_id="ATL",
                name="Hartsfield-Jackson Atlanta International",
                iata="ATL",
                icao="KATL",
                city="Atlanta",
                country="USA",
                lat=33.6407,
                lon=-84.4277
            )
            
            repo.create(airport1)
            repo.create(airport2)
            
            found = repo.find_by_country("USA")
            assert len(found) >= 2


class TestFlightRepository:
    """Test cases for FlightRepository."""
    
    def test_create_flight(self, connection):
        """Test creating a flight."""
        with connection.get_session() as session:
            repo = FlightRepository(session)
            
            flight = Flight(
                flight_id="FL001",
                flight_number="AA100",
                aircraft_id="AC001",
                operator="American Airlines",
                origin="JFK",
                destination="LAX",
                scheduled_departure="2024-01-01T10:00:00",
                scheduled_arrival="2024-01-01T13:30:00"
            )
            
            created = repo.create(flight)
            assert created.flight_id == "FL001"
            assert created.flight_number == "AA100"
    
    def test_find_by_aircraft(self, connection):
        """Test finding flights by aircraft."""
        with connection.get_session() as session:
            repo = FlightRepository(session)
            
            flight1 = Flight(
                flight_id="FL002",
                flight_number="UA200",
                aircraft_id="AC002",
                operator="United Airlines",
                origin="SFO",
                destination="ORD",
                scheduled_departure="2024-01-02T08:00:00",
                scheduled_arrival="2024-01-02T14:00:00"
            )
            
            flight2 = Flight(
                flight_id="FL003",
                flight_number="UA201",
                aircraft_id="AC002",
                operator="United Airlines",
                origin="ORD",
                destination="SFO",
                scheduled_departure="2024-01-02T16:00:00",
                scheduled_arrival="2024-01-02T19:00:00"
            )
            
            repo.create(flight1)
            repo.create(flight2)
            
            found = repo.find_by_aircraft("AC002")
            assert len(found) == 2
    
    def test_find_by_route(self, connection):
        """Test finding flights by route."""
        with connection.get_session() as session:
            repo = FlightRepository(session)
            
            flight = Flight(
                flight_id="FL004",
                flight_number="DL300",
                aircraft_id="AC003",
                operator="Delta Airlines",
                origin="ATL",
                destination="SEA",
                scheduled_departure="2024-01-03T09:00:00",
                scheduled_arrival="2024-01-03T12:00:00"
            )
            
            repo.create(flight)
            
            found = repo.find_by_route("ATL", "SEA")
            assert len(found) >= 1


class TestMaintenanceEventRepository:
    """Test cases for MaintenanceEventRepository."""
    
    def test_create_maintenance_event(self, connection):
        """Test creating a maintenance event."""
        with connection.get_session() as session:
            repo = MaintenanceEventRepository(session)
            
            event = MaintenanceEvent(
                event_id="ME001",
                aircraft_id="AC001",
                system_id="SYS001",
                component_id="COMP001",
                fault="Hydraulic leak",
                severity="High",
                corrective_action="Replace hydraulic line",
                reported_at="2024-01-01T15:30:00"
            )
            
            created = repo.create(event)
            assert created.event_id == "ME001"
            assert created.severity == "High"
    
    def test_find_by_aircraft(self, connection):
        """Test finding maintenance events by aircraft."""
        with connection.get_session() as session:
            repo = MaintenanceEventRepository(session)
            
            event1 = MaintenanceEvent(
                event_id="ME002",
                aircraft_id="AC002",
                system_id="SYS002",
                component_id="COMP002",
                fault="Engine oil pressure low",
                severity="Medium",
                corrective_action="Oil system inspection",
                reported_at="2024-01-02T10:00:00"
            )
            
            event2 = MaintenanceEvent(
                event_id="ME003",
                aircraft_id="AC002",
                system_id="SYS003",
                component_id="COMP003",
                fault="Tire wear",
                severity="Low",
                corrective_action="Replace tire",
                reported_at="2024-01-02T14:00:00"
            )
            
            repo.create(event1)
            repo.create(event2)
            
            found = repo.find_by_aircraft("AC002")
            assert len(found) == 2
    
    def test_find_by_severity(self, connection):
        """Test finding maintenance events by severity."""
        with connection.get_session() as session:
            repo = MaintenanceEventRepository(session)
            
            event = MaintenanceEvent(
                event_id="ME004",
                aircraft_id="AC003",
                system_id="SYS004",
                component_id="COMP004",
                fault="Critical system failure",
                severity="Critical",
                corrective_action="Emergency maintenance",
                reported_at="2024-01-03T16:00:00"
            )
            
            repo.create(event)
            
            found = repo.find_by_severity("Critical")
            assert len(found) >= 1


class TestSystemRepository:
    """Test cases for SystemRepository."""
    
    def test_create_system(self, connection):
        """Test creating a system."""
        with connection.get_session() as session:
            repo = SystemRepository(session)
            
            system = System(
                system_id="SYS001",
                aircraft_id="AC001",
                name="Hydraulic System",
                type="Hydraulic"
            )
            
            created = repo.create(system)
            assert created.system_id == "SYS001"
            assert created.name == "Hydraulic System"
    
    def test_find_by_aircraft(self, connection):
        """Test finding systems by aircraft."""
        with connection.get_session() as session:
            repo = SystemRepository(session)
            
            system1 = System(
                system_id="SYS002",
                aircraft_id="AC002",
                name="Engine System",
                type="Propulsion"
            )
            
            system2 = System(
                system_id="SYS003",
                aircraft_id="AC002",
                name="Navigation System",
                type="Avionics"
            )
            
            repo.create(system1)
            repo.create(system2)
            
            found = repo.find_by_aircraft("AC002")
            assert len(found) == 2
