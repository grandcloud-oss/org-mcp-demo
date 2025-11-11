"""Repository pattern for querying airplane database entities."""

from typing import List, Optional
from neo4j import Session
from .models import (
    Aircraft, Airport, Flight, System, Component, 
    Sensor, MaintenanceEvent, Delay, Reading
)
from .connection import Neo4jConnection
from .exceptions import QueryError, NotFoundError


class AircraftRepository:
    """Repository for Aircraft entities."""
    
    def __init__(self, connection: Neo4jConnection):
        self.connection = connection
    
    def create(self, aircraft: Aircraft) -> Aircraft:
        """Create a new aircraft."""
        query = """
        MERGE (a:Aircraft {aircraft_id: $aircraft_id})
        SET a.tail_number = $tail_number,
            a.icao24 = $icao24,
            a.model = $model,
            a.operator = $operator,
            a.manufacturer = $manufacturer
        RETURN a
        """
        try:
            with self.connection.get_session() as session:
                result = session.run(query, **aircraft.model_dump())
                record = result.single()
                if record:
                    return Aircraft(**record["a"])
                raise QueryError("Failed to create aircraft")
        except Exception as e:
            raise QueryError(f"Failed to create aircraft: {e}")
    
    def find_by_id(self, aircraft_id: str) -> Optional[Aircraft]:
        """Find aircraft by ID."""
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})
        RETURN a
        """
        try:
            with self.connection.get_session() as session:
                result = session.run(query, aircraft_id=aircraft_id)
                record = result.single()
                if record:
                    return Aircraft(**record["a"])
                return None
        except Exception as e:
            raise QueryError(f"Failed to find aircraft: {e}")
    
    def find_all(self, limit: int = 100) -> List[Aircraft]:
        """Find all aircraft with optional limit."""
        query = """
        MATCH (a:Aircraft)
        RETURN a
        LIMIT $limit
        """
        try:
            with self.connection.get_session() as session:
                result = session.run(query, limit=limit)
                return [Aircraft(**record["a"]) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to find aircraft: {e}")
    
    def delete(self, aircraft_id: str) -> bool:
        """Delete an aircraft by ID."""
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})
        DELETE a
        RETURN count(a) as deleted
        """
        try:
            with self.connection.get_session() as session:
                result = session.run(query, aircraft_id=aircraft_id)
                record = result.single()
                return record["deleted"] > 0 if record else False
        except Exception as e:
            raise QueryError(f"Failed to delete aircraft: {e}")


class AirportRepository:
    """Repository for Airport entities."""
    
    def __init__(self, connection: Neo4jConnection):
        self.connection = connection
    
    def create(self, airport: Airport) -> Airport:
        """Create a new airport."""
        query = """
        MERGE (a:Airport {airport_id: $airport_id})
        SET a.name = $name,
            a.iata = $iata,
            a.icao = $icao,
            a.city = $city,
            a.country = $country,
            a.lat = $lat,
            a.lon = $lon
        RETURN a
        """
        try:
            with self.connection.get_session() as session:
                result = session.run(query, **airport.model_dump())
                record = result.single()
                if record:
                    return Airport(**record["a"])
                raise QueryError("Failed to create airport")
        except Exception as e:
            raise QueryError(f"Failed to create airport: {e}")
    
    def find_by_id(self, airport_id: str) -> Optional[Airport]:
        """Find airport by ID."""
        query = """
        MATCH (a:Airport {airport_id: $airport_id})
        RETURN a
        """
        try:
            with self.connection.get_session() as session:
                result = session.run(query, airport_id=airport_id)
                record = result.single()
                if record:
                    return Airport(**record["a"])
                return None
        except Exception as e:
            raise QueryError(f"Failed to find airport: {e}")
    
    def find_by_iata(self, iata: str) -> Optional[Airport]:
        """Find airport by IATA code."""
        query = """
        MATCH (a:Airport {iata: $iata})
        RETURN a
        """
        try:
            with self.connection.get_session() as session:
                result = session.run(query, iata=iata)
                record = result.single()
                if record:
                    return Airport(**record["a"])
                return None
        except Exception as e:
            raise QueryError(f"Failed to find airport: {e}")
    
    def find_all(self, limit: int = 100) -> List[Airport]:
        """Find all airports with optional limit."""
        query = """
        MATCH (a:Airport)
        RETURN a
        LIMIT $limit
        """
        try:
            with self.connection.get_session() as session:
                result = session.run(query, limit=limit)
                return [Airport(**record["a"]) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to find airports: {e}")


class FlightRepository:
    """Repository for Flight entities."""
    
    def __init__(self, connection: Neo4jConnection):
        self.connection = connection
    
    def create(self, flight: Flight) -> Flight:
        """Create a new flight."""
        query = """
        MERGE (f:Flight {flight_id: $flight_id})
        SET f.flight_number = $flight_number,
            f.aircraft_id = $aircraft_id,
            f.operator = $operator,
            f.origin = $origin,
            f.destination = $destination,
            f.scheduled_departure = $scheduled_departure,
            f.scheduled_arrival = $scheduled_arrival
        RETURN f
        """
        try:
            with self.connection.get_session() as session:
                result = session.run(query, **flight.model_dump())
                record = result.single()
                if record:
                    return Flight(**record["f"])
                raise QueryError("Failed to create flight")
        except Exception as e:
            raise QueryError(f"Failed to create flight: {e}")
    
    def find_by_id(self, flight_id: str) -> Optional[Flight]:
        """Find flight by ID."""
        query = """
        MATCH (f:Flight {flight_id: $flight_id})
        RETURN f
        """
        try:
            with self.connection.get_session() as session:
                result = session.run(query, flight_id=flight_id)
                record = result.single()
                if record:
                    return Flight(**record["f"])
                return None
        except Exception as e:
            raise QueryError(f"Failed to find flight: {e}")
    
    def find_by_aircraft(self, aircraft_id: str, limit: int = 100) -> List[Flight]:
        """Find flights by aircraft ID."""
        query = """
        MATCH (f:Flight {aircraft_id: $aircraft_id})
        RETURN f
        LIMIT $limit
        """
        try:
            with self.connection.get_session() as session:
                result = session.run(query, aircraft_id=aircraft_id, limit=limit)
                return [Flight(**record["f"]) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to find flights: {e}")
    
    def find_all(self, limit: int = 100) -> List[Flight]:
        """Find all flights with optional limit."""
        query = """
        MATCH (f:Flight)
        RETURN f
        LIMIT $limit
        """
        try:
            with self.connection.get_session() as session:
                result = session.run(query, limit=limit)
                return [Flight(**record["f"]) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to find flights: {e}")


class SystemRepository:
    """Repository for System entities."""
    
    def __init__(self, connection: Neo4jConnection):
        self.connection = connection
    
    def create(self, system: System) -> System:
        """Create a new system."""
        query = """
        MERGE (s:System {system_id: $system_id})
        SET s.aircraft_id = $aircraft_id,
            s.name = $name,
            s.type = $type
        RETURN s
        """
        try:
            with self.connection.get_session() as session:
                result = session.run(query, **system.model_dump())
                record = result.single()
                if record:
                    return System(**record["s"])
                raise QueryError("Failed to create system")
        except Exception as e:
            raise QueryError(f"Failed to create system: {e}")
    
    def find_by_id(self, system_id: str) -> Optional[System]:
        """Find system by ID."""
        query = """
        MATCH (s:System {system_id: $system_id})
        RETURN s
        """
        try:
            with self.connection.get_session() as session:
                result = session.run(query, system_id=system_id)
                record = result.single()
                if record:
                    return System(**record["s"])
                return None
        except Exception as e:
            raise QueryError(f"Failed to find system: {e}")
    
    def find_by_aircraft(self, aircraft_id: str) -> List[System]:
        """Find systems by aircraft ID."""
        query = """
        MATCH (s:System {aircraft_id: $aircraft_id})
        RETURN s
        """
        try:
            with self.connection.get_session() as session:
                result = session.run(query, aircraft_id=aircraft_id)
                return [System(**record["s"]) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to find systems: {e}")


class MaintenanceEventRepository:
    """Repository for MaintenanceEvent entities."""
    
    def __init__(self, connection: Neo4jConnection):
        self.connection = connection
    
    def create(self, event: MaintenanceEvent) -> MaintenanceEvent:
        """Create a new maintenance event."""
        query = """
        MERGE (e:MaintenanceEvent {event_id: $event_id})
        SET e.aircraft_id = $aircraft_id,
            e.system_id = $system_id,
            e.component_id = $component_id,
            e.fault = $fault,
            e.severity = $severity,
            e.reported_at = $reported_at,
            e.corrective_action = $corrective_action
        RETURN e
        """
        try:
            with self.connection.get_session() as session:
                result = session.run(query, **event.model_dump())
                record = result.single()
                if record:
                    return MaintenanceEvent(**record["e"])
                raise QueryError("Failed to create maintenance event")
        except Exception as e:
            raise QueryError(f"Failed to create maintenance event: {e}")
    
    def find_by_id(self, event_id: str) -> Optional[MaintenanceEvent]:
        """Find maintenance event by ID."""
        query = """
        MATCH (e:MaintenanceEvent {event_id: $event_id})
        RETURN e
        """
        try:
            with self.connection.get_session() as session:
                result = session.run(query, event_id=event_id)
                record = result.single()
                if record:
                    return MaintenanceEvent(**record["e"])
                return None
        except Exception as e:
            raise QueryError(f"Failed to find maintenance event: {e}")
    
    def find_by_aircraft(self, aircraft_id: str, limit: int = 100) -> List[MaintenanceEvent]:
        """Find maintenance events by aircraft ID."""
        query = """
        MATCH (e:MaintenanceEvent {aircraft_id: $aircraft_id})
        RETURN e
        ORDER BY e.reported_at DESC
        LIMIT $limit
        """
        try:
            with self.connection.get_session() as session:
                result = session.run(query, aircraft_id=aircraft_id, limit=limit)
                return [MaintenanceEvent(**record["e"]) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to find maintenance events: {e}")
    
    def find_by_severity(self, severity: str, limit: int = 100) -> List[MaintenanceEvent]:
        """Find maintenance events by severity."""
        query = """
        MATCH (e:MaintenanceEvent {severity: $severity})
        RETURN e
        ORDER BY e.reported_at DESC
        LIMIT $limit
        """
        try:
            with self.connection.get_session() as session:
                result = session.run(query, severity=severity, limit=limit)
                return [MaintenanceEvent(**record["e"]) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to find maintenance events: {e}")
