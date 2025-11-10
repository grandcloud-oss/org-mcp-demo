"""Repository pattern implementation for airplane data entities."""

from typing import List, Optional
from neo4j import Session
from .models import Aircraft, Airport, Flight, MaintenanceEvent, System
from .exceptions import QueryError, NotFoundError


class AircraftRepository:
    """Repository for Aircraft entity operations."""
    
    def __init__(self, session: Session):
        """Initialize repository with Neo4j session.
        
        Args:
            session: Neo4j database session
        """
        self.session = session
    
    def create(self, aircraft: Aircraft) -> Aircraft:
        """Create a new aircraft.
        
        Args:
            aircraft: Aircraft model to create
            
        Returns:
            Created aircraft
            
        Raises:
            QueryError: If query execution fails
        """
        try:
            query = """
            MERGE (a:Aircraft {aircraft_id: $aircraft_id})
            SET a.tail_number = $tail_number,
                a.icao24 = $icao24,
                a.model = $model,
                a.operator = $operator,
                a.manufacturer = $manufacturer
            RETURN a
            """
            result = self.session.run(query, **aircraft.model_dump())
            record = result.single()
            if not record:
                raise QueryError("Failed to create aircraft")
            return Aircraft(**record["a"])
        except Exception as e:
            raise QueryError(f"Failed to create aircraft: {e}")
    
    def find_by_id(self, aircraft_id: str) -> Optional[Aircraft]:
        """Find aircraft by ID.
        
        Args:
            aircraft_id: Aircraft identifier
            
        Returns:
            Aircraft if found, None otherwise
        """
        try:
            query = "MATCH (a:Aircraft {aircraft_id: $aircraft_id}) RETURN a"
            result = self.session.run(query, aircraft_id=aircraft_id)
            record = result.single()
            if record:
                return Aircraft(**record["a"])
            return None
        except Exception as e:
            raise QueryError(f"Failed to find aircraft: {e}")
    
    def find_by_tail_number(self, tail_number: str) -> Optional[Aircraft]:
        """Find aircraft by tail number.
        
        Args:
            tail_number: Aircraft tail number
            
        Returns:
            Aircraft if found, None otherwise
        """
        try:
            query = "MATCH (a:Aircraft {tail_number: $tail_number}) RETURN a"
            result = self.session.run(query, tail_number=tail_number)
            record = result.single()
            if record:
                return Aircraft(**record["a"])
            return None
        except Exception as e:
            raise QueryError(f"Failed to find aircraft: {e}")
    
    def find_all(self) -> List[Aircraft]:
        """Find all aircraft.
        
        Returns:
            List of all aircraft
        """
        try:
            query = "MATCH (a:Aircraft) RETURN a"
            result = self.session.run(query)
            return [Aircraft(**record["a"]) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to find aircraft: {e}")
    
    def find_by_operator(self, operator: str) -> List[Aircraft]:
        """Find aircraft by operator.
        
        Args:
            operator: Operator/airline name
            
        Returns:
            List of aircraft for the operator
        """
        try:
            query = "MATCH (a:Aircraft {operator: $operator}) RETURN a"
            result = self.session.run(query, operator=operator)
            return [Aircraft(**record["a"]) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to find aircraft by operator: {e}")
    
    def update(self, aircraft: Aircraft) -> Aircraft:
        """Update an existing aircraft.
        
        Args:
            aircraft: Aircraft model with updated data
            
        Returns:
            Updated aircraft
            
        Raises:
            NotFoundError: If aircraft doesn't exist
        """
        try:
            query = """
            MATCH (a:Aircraft {aircraft_id: $aircraft_id})
            SET a.tail_number = $tail_number,
                a.icao24 = $icao24,
                a.model = $model,
                a.operator = $operator,
                a.manufacturer = $manufacturer
            RETURN a
            """
            result = self.session.run(query, **aircraft.model_dump())
            record = result.single()
            if not record:
                raise NotFoundError(f"Aircraft not found: {aircraft.aircraft_id}")
            return Aircraft(**record["a"])
        except NotFoundError:
            raise
        except Exception as e:
            raise QueryError(f"Failed to update aircraft: {e}")
    
    def delete(self, aircraft_id: str) -> bool:
        """Delete an aircraft.
        
        Args:
            aircraft_id: Aircraft identifier
            
        Returns:
            True if deleted, False if not found
        """
        try:
            query = """
            MATCH (a:Aircraft {aircraft_id: $aircraft_id})
            DETACH DELETE a
            RETURN count(a) as deleted
            """
            result = self.session.run(query, aircraft_id=aircraft_id)
            record = result.single()
            return record["deleted"] > 0 if record else False
        except Exception as e:
            raise QueryError(f"Failed to delete aircraft: {e}")


class AirportRepository:
    """Repository for Airport entity operations."""
    
    def __init__(self, session: Session):
        """Initialize repository with Neo4j session.
        
        Args:
            session: Neo4j database session
        """
        self.session = session
    
    def create(self, airport: Airport) -> Airport:
        """Create a new airport.
        
        Args:
            airport: Airport model to create
            
        Returns:
            Created airport
        """
        try:
            query = """
            MERGE (ap:Airport {airport_id: $airport_id})
            SET ap.name = $name,
                ap.iata = $iata,
                ap.icao = $icao,
                ap.city = $city,
                ap.country = $country,
                ap.lat = $lat,
                ap.lon = $lon
            RETURN ap
            """
            result = self.session.run(query, **airport.model_dump())
            record = result.single()
            if not record:
                raise QueryError("Failed to create airport")
            return Airport(**record["ap"])
        except Exception as e:
            raise QueryError(f"Failed to create airport: {e}")
    
    def find_by_id(self, airport_id: str) -> Optional[Airport]:
        """Find airport by ID.
        
        Args:
            airport_id: Airport identifier
            
        Returns:
            Airport if found, None otherwise
        """
        try:
            query = "MATCH (ap:Airport {airport_id: $airport_id}) RETURN ap"
            result = self.session.run(query, airport_id=airport_id)
            record = result.single()
            if record:
                return Airport(**record["ap"])
            return None
        except Exception as e:
            raise QueryError(f"Failed to find airport: {e}")
    
    def find_by_iata(self, iata: str) -> Optional[Airport]:
        """Find airport by IATA code.
        
        Args:
            iata: IATA airport code
            
        Returns:
            Airport if found, None otherwise
        """
        try:
            query = "MATCH (ap:Airport {iata: $iata}) RETURN ap"
            result = self.session.run(query, iata=iata)
            record = result.single()
            if record:
                return Airport(**record["ap"])
            return None
        except Exception as e:
            raise QueryError(f"Failed to find airport: {e}")
    
    def find_all(self) -> List[Airport]:
        """Find all airports.
        
        Returns:
            List of all airports
        """
        try:
            query = "MATCH (ap:Airport) RETURN ap"
            result = self.session.run(query)
            return [Airport(**record["ap"]) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to find airports: {e}")
    
    def find_by_country(self, country: str) -> List[Airport]:
        """Find airports by country.
        
        Args:
            country: Country name
            
        Returns:
            List of airports in the country
        """
        try:
            query = "MATCH (ap:Airport {country: $country}) RETURN ap"
            result = self.session.run(query, country=country)
            return [Airport(**record["ap"]) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to find airports by country: {e}")


class FlightRepository:
    """Repository for Flight entity operations."""
    
    def __init__(self, session: Session):
        """Initialize repository with Neo4j session.
        
        Args:
            session: Neo4j database session
        """
        self.session = session
    
    def create(self, flight: Flight) -> Flight:
        """Create a new flight.
        
        Args:
            flight: Flight model to create
            
        Returns:
            Created flight
        """
        try:
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
            result = self.session.run(query, **flight.model_dump())
            record = result.single()
            if not record:
                raise QueryError("Failed to create flight")
            return Flight(**record["f"])
        except Exception as e:
            raise QueryError(f"Failed to create flight: {e}")
    
    def find_by_id(self, flight_id: str) -> Optional[Flight]:
        """Find flight by ID.
        
        Args:
            flight_id: Flight identifier
            
        Returns:
            Flight if found, None otherwise
        """
        try:
            query = "MATCH (f:Flight {flight_id: $flight_id}) RETURN f"
            result = self.session.run(query, flight_id=flight_id)
            record = result.single()
            if record:
                return Flight(**record["f"])
            return None
        except Exception as e:
            raise QueryError(f"Failed to find flight: {e}")
    
    def find_by_flight_number(self, flight_number: str) -> List[Flight]:
        """Find flights by flight number.
        
        Args:
            flight_number: Flight number
            
        Returns:
            List of flights with this number
        """
        try:
            query = "MATCH (f:Flight {flight_number: $flight_number}) RETURN f"
            result = self.session.run(query, flight_number=flight_number)
            return [Flight(**record["f"]) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to find flights: {e}")
    
    def find_by_aircraft(self, aircraft_id: str) -> List[Flight]:
        """Find flights by aircraft.
        
        Args:
            aircraft_id: Aircraft identifier
            
        Returns:
            List of flights operated by this aircraft
        """
        try:
            query = "MATCH (f:Flight {aircraft_id: $aircraft_id}) RETURN f"
            result = self.session.run(query, aircraft_id=aircraft_id)
            return [Flight(**record["f"]) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to find flights by aircraft: {e}")
    
    def find_by_route(self, origin: str, destination: str) -> List[Flight]:
        """Find flights by origin and destination.
        
        Args:
            origin: Origin airport IATA code
            destination: Destination airport IATA code
            
        Returns:
            List of flights on this route
        """
        try:
            query = """
            MATCH (f:Flight {origin: $origin, destination: $destination})
            RETURN f
            """
            result = self.session.run(query, origin=origin, destination=destination)
            return [Flight(**record["f"]) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to find flights by route: {e}")
    
    def find_all(self) -> List[Flight]:
        """Find all flights.
        
        Returns:
            List of all flights
        """
        try:
            query = "MATCH (f:Flight) RETURN f"
            result = self.session.run(query)
            return [Flight(**record["f"]) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to find flights: {e}")


class MaintenanceEventRepository:
    """Repository for MaintenanceEvent entity operations."""
    
    def __init__(self, session: Session):
        """Initialize repository with Neo4j session.
        
        Args:
            session: Neo4j database session
        """
        self.session = session
    
    def create(self, event: MaintenanceEvent) -> MaintenanceEvent:
        """Create a new maintenance event.
        
        Args:
            event: MaintenanceEvent model to create
            
        Returns:
            Created maintenance event
        """
        try:
            query = """
            MERGE (e:MaintenanceEvent {event_id: $event_id})
            SET e.aircraft_id = $aircraft_id,
                e.system_id = $system_id,
                e.component_id = $component_id,
                e.fault = $fault,
                e.severity = $severity,
                e.corrective_action = $corrective_action,
                e.reported_at = $reported_at
            RETURN e
            """
            result = self.session.run(query, **event.model_dump())
            record = result.single()
            if not record:
                raise QueryError("Failed to create maintenance event")
            return MaintenanceEvent(**record["e"])
        except Exception as e:
            raise QueryError(f"Failed to create maintenance event: {e}")
    
    def find_by_id(self, event_id: str) -> Optional[MaintenanceEvent]:
        """Find maintenance event by ID.
        
        Args:
            event_id: Event identifier
            
        Returns:
            MaintenanceEvent if found, None otherwise
        """
        try:
            query = "MATCH (e:MaintenanceEvent {event_id: $event_id}) RETURN e"
            result = self.session.run(query, event_id=event_id)
            record = result.single()
            if record:
                return MaintenanceEvent(**record["e"])
            return None
        except Exception as e:
            raise QueryError(f"Failed to find maintenance event: {e}")
    
    def find_by_aircraft(self, aircraft_id: str) -> List[MaintenanceEvent]:
        """Find maintenance events by aircraft.
        
        Args:
            aircraft_id: Aircraft identifier
            
        Returns:
            List of maintenance events for this aircraft
        """
        try:
            query = "MATCH (e:MaintenanceEvent {aircraft_id: $aircraft_id}) RETURN e"
            result = self.session.run(query, aircraft_id=aircraft_id)
            return [MaintenanceEvent(**record["e"]) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to find maintenance events: {e}")
    
    def find_by_severity(self, severity: str) -> List[MaintenanceEvent]:
        """Find maintenance events by severity.
        
        Args:
            severity: Event severity level
            
        Returns:
            List of maintenance events with this severity
        """
        try:
            query = "MATCH (e:MaintenanceEvent {severity: $severity}) RETURN e"
            result = self.session.run(query, severity=severity)
            return [MaintenanceEvent(**record["e"]) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to find maintenance events by severity: {e}")
    
    def find_all(self) -> List[MaintenanceEvent]:
        """Find all maintenance events.
        
        Returns:
            List of all maintenance events
        """
        try:
            query = "MATCH (e:MaintenanceEvent) RETURN e"
            result = self.session.run(query)
            return [MaintenanceEvent(**record["e"]) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to find maintenance events: {e}")


class SystemRepository:
    """Repository for System entity operations."""
    
    def __init__(self, session: Session):
        """Initialize repository with Neo4j session.
        
        Args:
            session: Neo4j database session
        """
        self.session = session
    
    def create(self, system: System) -> System:
        """Create a new system.
        
        Args:
            system: System model to create
            
        Returns:
            Created system
        """
        try:
            query = """
            MERGE (s:System {system_id: $system_id})
            SET s.aircraft_id = $aircraft_id,
                s.name = $name,
                s.type = $type
            RETURN s
            """
            result = self.session.run(query, **system.model_dump())
            record = result.single()
            if not record:
                raise QueryError("Failed to create system")
            return System(**record["s"])
        except Exception as e:
            raise QueryError(f"Failed to create system: {e}")
    
    def find_by_id(self, system_id: str) -> Optional[System]:
        """Find system by ID.
        
        Args:
            system_id: System identifier
            
        Returns:
            System if found, None otherwise
        """
        try:
            query = "MATCH (s:System {system_id: $system_id}) RETURN s"
            result = self.session.run(query, system_id=system_id)
            record = result.single()
            if record:
                return System(**record["s"])
            return None
        except Exception as e:
            raise QueryError(f"Failed to find system: {e}")
    
    def find_by_aircraft(self, aircraft_id: str) -> List[System]:
        """Find systems by aircraft.
        
        Args:
            aircraft_id: Aircraft identifier
            
        Returns:
            List of systems for this aircraft
        """
        try:
            query = "MATCH (s:System {aircraft_id: $aircraft_id}) RETURN s"
            result = self.session.run(query, aircraft_id=aircraft_id)
            return [System(**record["s"]) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to find systems by aircraft: {e}")
    
    def find_all(self) -> List[System]:
        """Find all systems.
        
        Returns:
            List of all systems
        """
        try:
            query = "MATCH (s:System) RETURN s"
            result = self.session.run(query)
            return [System(**record["s"]) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to find systems: {e}")
