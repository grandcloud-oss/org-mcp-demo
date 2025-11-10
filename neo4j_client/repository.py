"""Repository classes for airplane data CRUD operations."""

from typing import List, Optional
from neo4j import Session
from .models import (
    Aircraft, Airport, Flight, System, Component,
    MaintenanceEvent, Delay, Sensor, Reading
)
from .exceptions import QueryError, NotFoundError


class AircraftRepository:
    """Repository for Aircraft entity operations."""
    
    def __init__(self, session: Session):
        """Initialize repository with Neo4j session.
        
        Args:
            session: Active Neo4j session
        """
        self.session = session
    
    def create(self, aircraft: Aircraft) -> Aircraft:
        """Create a new aircraft in the database.
        
        Args:
            aircraft: Aircraft object to create
            
        Returns:
            Created aircraft object
            
        Raises:
            QueryError: If creation fails
        """
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
            result = self.session.run(query, **aircraft.model_dump())
            return aircraft
        except Exception as e:
            raise QueryError(f"Failed to create aircraft: {str(e)}") from e
    
    def find_by_id(self, aircraft_id: str) -> Optional[Aircraft]:
        """Find aircraft by ID.
        
        Args:
            aircraft_id: Unique aircraft identifier
            
        Returns:
            Aircraft object if found, None otherwise
        """
        query = "MATCH (a:Aircraft {aircraft_id: $aircraft_id}) RETURN a"
        result = self.session.run(query, aircraft_id=aircraft_id)
        record = result.single()
        if record:
            return Aircraft(**record["a"])
        return None
    
    def find_by_tail_number(self, tail_number: str) -> Optional[Aircraft]:
        """Find aircraft by tail number.
        
        Args:
            tail_number: Aircraft registration number
            
        Returns:
            Aircraft object if found, None otherwise
        """
        query = "MATCH (a:Aircraft {tail_number: $tail_number}) RETURN a"
        result = self.session.run(query, tail_number=tail_number)
        record = result.single()
        if record:
            return Aircraft(**record["a"])
        return None
    
    def find_by_operator(self, operator: str) -> List[Aircraft]:
        """Find all aircraft for a given operator.
        
        Args:
            operator: Operator/airline name
            
        Returns:
            List of aircraft objects
        """
        query = "MATCH (a:Aircraft {operator: $operator}) RETURN a"
        result = self.session.run(query, operator=operator)
        return [Aircraft(**record["a"]) for record in result]
    
    def find_all(self, limit: int = 100) -> List[Aircraft]:
        """Find all aircraft.
        
        Args:
            limit: Maximum number of records to return (default: 100)
            
        Returns:
            List of aircraft objects
        """
        query = "MATCH (a:Aircraft) RETURN a LIMIT $limit"
        result = self.session.run(query, limit=limit)
        return [Aircraft(**record["a"]) for record in result]
    
    def delete(self, aircraft_id: str) -> bool:
        """Delete aircraft by ID.
        
        Args:
            aircraft_id: Unique aircraft identifier
            
        Returns:
            True if aircraft was deleted, False if not found
        """
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})
        DELETE a
        RETURN count(a) as deleted
        """
        result = self.session.run(query, aircraft_id=aircraft_id)
        record = result.single()
        return record["deleted"] > 0 if record else False


class AirportRepository:
    """Repository for Airport entity operations."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, airport: Airport) -> Airport:
        """Create a new airport in the database.
        
        Args:
            airport: Airport object to create
            
        Returns:
            Created airport object
        """
        query = """
        MERGE (ap:Airport {airport_id: $airport_id})
        SET ap.iata = $iata,
            ap.icao = $icao,
            ap.name = $name,
            ap.city = $city,
            ap.country = $country,
            ap.lat = $lat,
            ap.lon = $lon
        RETURN ap
        """
        try:
            result = self.session.run(query, **airport.model_dump())
            return airport
        except Exception as e:
            raise QueryError(f"Failed to create airport: {str(e)}") from e
    
    def find_by_iata(self, iata: str) -> Optional[Airport]:
        """Find airport by IATA code.
        
        Args:
            iata: IATA airport code (e.g., JFK)
            
        Returns:
            Airport object if found, None otherwise
        """
        query = "MATCH (ap:Airport {iata: $iata}) RETURN ap"
        result = self.session.run(query, iata=iata)
        record = result.single()
        if record:
            return Airport(**record["ap"])
        return None
    
    def find_by_country(self, country: str) -> List[Airport]:
        """Find all airports in a given country.
        
        Args:
            country: Country name
            
        Returns:
            List of airport objects
        """
        query = "MATCH (ap:Airport {country: $country}) RETURN ap"
        result = self.session.run(query, country=country)
        return [Airport(**record["ap"]) for record in result]
    
    def find_all(self, limit: int = 100) -> List[Airport]:
        """Find all airports.
        
        Args:
            limit: Maximum number of records to return
            
        Returns:
            List of airport objects
        """
        query = "MATCH (ap:Airport) RETURN ap LIMIT $limit"
        result = self.session.run(query, limit=limit)
        return [Airport(**record["ap"]) for record in result]


class FlightRepository:
    """Repository for Flight entity operations."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, flight: Flight) -> Flight:
        """Create a new flight in the database.
        
        Args:
            flight: Flight object to create
            
        Returns:
            Created flight object
        """
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
            result = self.session.run(query, **flight.model_dump())
            return flight
        except Exception as e:
            raise QueryError(f"Failed to create flight: {str(e)}") from e
    
    def find_by_id(self, flight_id: str) -> Optional[Flight]:
        """Find flight by ID.
        
        Args:
            flight_id: Unique flight identifier
            
        Returns:
            Flight object if found, None otherwise
        """
        query = "MATCH (f:Flight {flight_id: $flight_id}) RETURN f"
        result = self.session.run(query, flight_id=flight_id)
        record = result.single()
        if record:
            return Flight(**record["f"])
        return None
    
    def find_by_flight_number(self, flight_number: str) -> List[Flight]:
        """Find flights by flight number.
        
        Args:
            flight_number: Flight number (e.g., EX370)
            
        Returns:
            List of flight objects
        """
        query = "MATCH (f:Flight {flight_number: $flight_number}) RETURN f"
        result = self.session.run(query, flight_number=flight_number)
        return [Flight(**record["f"]) for record in result]
    
    def find_by_aircraft(self, aircraft_id: str, limit: int = 100) -> List[Flight]:
        """Find flights for a given aircraft.
        
        Args:
            aircraft_id: Aircraft identifier
            limit: Maximum number of records to return
            
        Returns:
            List of flight objects
        """
        query = """
        MATCH (f:Flight {aircraft_id: $aircraft_id})
        RETURN f
        ORDER BY f.scheduled_departure DESC
        LIMIT $limit
        """
        result = self.session.run(query, aircraft_id=aircraft_id, limit=limit)
        return [Flight(**record["f"]) for record in result]
    
    def find_by_route(self, origin: str, destination: str, limit: int = 100) -> List[Flight]:
        """Find flights by route.
        
        Args:
            origin: Origin airport IATA code
            destination: Destination airport IATA code
            limit: Maximum number of records to return
            
        Returns:
            List of flight objects
        """
        query = """
        MATCH (f:Flight {origin: $origin, destination: $destination})
        RETURN f
        LIMIT $limit
        """
        result = self.session.run(query, origin=origin, destination=destination, limit=limit)
        return [Flight(**record["f"]) for record in result]


class MaintenanceEventRepository:
    """Repository for MaintenanceEvent entity operations."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, event: MaintenanceEvent) -> MaintenanceEvent:
        """Create a new maintenance event.
        
        Args:
            event: MaintenanceEvent object to create
            
        Returns:
            Created maintenance event object
        """
        query = """
        MERGE (me:MaintenanceEvent {event_id: $event_id})
        SET me.aircraft_id = $aircraft_id,
            me.system_id = $system_id,
            me.component_id = $component_id,
            me.fault = $fault,
            me.severity = $severity,
            me.reported_at = $reported_at,
            me.corrective_action = $corrective_action
        RETURN me
        """
        try:
            result = self.session.run(query, **event.model_dump())
            return event
        except Exception as e:
            raise QueryError(f"Failed to create maintenance event: {str(e)}") from e
    
    def find_by_aircraft(self, aircraft_id: str, limit: int = 100) -> List[MaintenanceEvent]:
        """Find maintenance events for an aircraft.
        
        Args:
            aircraft_id: Aircraft identifier
            limit: Maximum number of records to return
            
        Returns:
            List of maintenance event objects
        """
        query = """
        MATCH (me:MaintenanceEvent {aircraft_id: $aircraft_id})
        RETURN me
        ORDER BY me.reported_at DESC
        LIMIT $limit
        """
        result = self.session.run(query, aircraft_id=aircraft_id, limit=limit)
        return [MaintenanceEvent(**record["me"]) for record in result]
    
    def find_by_severity(self, severity: str, limit: int = 100) -> List[MaintenanceEvent]:
        """Find maintenance events by severity level.
        
        Args:
            severity: Severity level (e.g., CRITICAL, MINOR)
            limit: Maximum number of records to return
            
        Returns:
            List of maintenance event objects
        """
        query = """
        MATCH (me:MaintenanceEvent {severity: $severity})
        RETURN me
        ORDER BY me.reported_at DESC
        LIMIT $limit
        """
        result = self.session.run(query, severity=severity, limit=limit)
        return [MaintenanceEvent(**record["me"]) for record in result]


class SystemRepository:
    """Repository for System entity operations."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, system: System) -> System:
        """Create a new system.
        
        Args:
            system: System object to create
            
        Returns:
            Created system object
        """
        query = """
        MERGE (s:System {system_id: $system_id})
        SET s.aircraft_id = $aircraft_id,
            s.name = $name,
            s.type = $type
        RETURN s
        """
        try:
            result = self.session.run(query, **system.model_dump())
            return system
        except Exception as e:
            raise QueryError(f"Failed to create system: {str(e)}") from e
    
    def find_by_aircraft(self, aircraft_id: str) -> List[System]:
        """Find systems for an aircraft.
        
        Args:
            aircraft_id: Aircraft identifier
            
        Returns:
            List of system objects
        """
        query = "MATCH (s:System {aircraft_id: $aircraft_id}) RETURN s"
        result = self.session.run(query, aircraft_id=aircraft_id)
        return [System(**record["s"]) for record in result]
    
    def find_by_type(self, system_type: str, limit: int = 100) -> List[System]:
        """Find systems by type.
        
        Args:
            system_type: System type (e.g., Engine, Hydraulics)
            limit: Maximum number of records to return
            
        Returns:
            List of system objects
        """
        query = "MATCH (s:System {type: $system_type}) RETURN s LIMIT $limit"
        result = self.session.run(query, system_type=system_type, limit=limit)
        return [System(**record["s"]) for record in result]


class DelayRepository:
    """Repository for Delay entity operations."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def find_by_flight(self, flight_id: str) -> List[Delay]:
        """Find delays for a flight.
        
        Args:
            flight_id: Flight identifier
            
        Returns:
            List of delay objects
        """
        query = "MATCH (d:Delay {flight_id: $flight_id}) RETURN d"
        result = self.session.run(query, flight_id=flight_id)
        return [Delay(**record["d"]) for record in result]
    
    def find_by_cause(self, cause: str, limit: int = 100) -> List[Delay]:
        """Find delays by cause.
        
        Args:
            cause: Delay cause (e.g., Weather, Security)
            limit: Maximum number of records to return
            
        Returns:
            List of delay objects
        """
        query = "MATCH (d:Delay {cause: $cause}) RETURN d LIMIT $limit"
        result = self.session.run(query, cause=cause, limit=limit)
        return [Delay(**record["d"]) for record in result]
