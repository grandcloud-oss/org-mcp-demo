"""Repository pattern for accessing airplane database entities."""

from typing import List, Optional
from neo4j import Session
from .models import (
    Aircraft, Airport, Flight, Delay, System, Component,
    Sensor, MaintenanceEvent, Reading
)
from .exceptions import QueryError, NotFoundError


class AircraftRepository:
    """Repository for Aircraft entities."""
    
    def __init__(self, session: Session):
        """Initialize repository with a Neo4j session."""
        self.session = session
    
    def create(self, aircraft: Aircraft) -> Aircraft:
        """Create a new aircraft.
        
        Args:
            aircraft: Aircraft model instance
            
        Returns:
            Created aircraft
        """
        query = """
        MERGE (a:Aircraft {aircraft_id: $aircraft_id})
        SET a.tail_number = $tail_number,
            a.icao24 = $icao24,
            a.model = $model,
            a.manufacturer = $manufacturer,
            a.operator = $operator
        RETURN a
        """
        try:
            result = self.session.run(query, **aircraft.model_dump())
            record = result.single()
            if record:
                return aircraft
            raise QueryError("Failed to create aircraft")
        except Exception as e:
            raise QueryError(f"Error creating aircraft: {str(e)}")
    
    def find_by_id(self, aircraft_id: str) -> Optional[Aircraft]:
        """Find aircraft by ID.
        
        Args:
            aircraft_id: Aircraft ID
            
        Returns:
            Aircraft if found, None otherwise
        """
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})
        RETURN a
        """
        try:
            result = self.session.run(query, aircraft_id=aircraft_id)
            record = result.single()
            if record:
                data = dict(record["a"])
                return Aircraft(**data)
            return None
        except Exception as e:
            raise QueryError(f"Error finding aircraft: {str(e)}")
    
    def find_by_tail_number(self, tail_number: str) -> Optional[Aircraft]:
        """Find aircraft by tail number.
        
        Args:
            tail_number: Aircraft tail number
            
        Returns:
            Aircraft if found, None otherwise
        """
        query = """
        MATCH (a:Aircraft {tail_number: $tail_number})
        RETURN a
        """
        try:
            result = self.session.run(query, tail_number=tail_number)
            record = result.single()
            if record:
                data = dict(record["a"])
                return Aircraft(**data)
            return None
        except Exception as e:
            raise QueryError(f"Error finding aircraft: {str(e)}")
    
    def find_all(self, limit: int = 100) -> List[Aircraft]:
        """Find all aircraft.
        
        Args:
            limit: Maximum number of results (default: 100)
            
        Returns:
            List of aircraft
        """
        query = """
        MATCH (a:Aircraft)
        RETURN a
        LIMIT $limit
        """
        try:
            result = self.session.run(query, limit=limit)
            aircraft_list = []
            for record in result:
                data = dict(record["a"])
                aircraft_list.append(Aircraft(**data))
            return aircraft_list
        except Exception as e:
            raise QueryError(f"Error finding aircraft: {str(e)}")
    
    def find_by_operator(self, operator: str) -> List[Aircraft]:
        """Find aircraft by operator.
        
        Args:
            operator: Operator name
            
        Returns:
            List of aircraft
        """
        query = """
        MATCH (a:Aircraft {operator: $operator})
        RETURN a
        """
        try:
            result = self.session.run(query, operator=operator)
            aircraft_list = []
            for record in result:
                data = dict(record["a"])
                aircraft_list.append(Aircraft(**data))
            return aircraft_list
        except Exception as e:
            raise QueryError(f"Error finding aircraft by operator: {str(e)}")
    
    def delete(self, aircraft_id: str) -> bool:
        """Delete aircraft by ID.
        
        Args:
            aircraft_id: Aircraft ID
            
        Returns:
            True if deleted, False if not found
        """
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})
        DELETE a
        RETURN count(a) as deleted
        """
        try:
            result = self.session.run(query, aircraft_id=aircraft_id)
            record = result.single()
            return record["deleted"] > 0 if record else False
        except Exception as e:
            raise QueryError(f"Error deleting aircraft: {str(e)}")


class AirportRepository:
    """Repository for Airport entities."""
    
    def __init__(self, session: Session):
        """Initialize repository with a Neo4j session."""
        self.session = session
    
    def create(self, airport: Airport) -> Airport:
        """Create a new airport.
        
        Args:
            airport: Airport model instance
            
        Returns:
            Created airport
        """
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
            result = self.session.run(query, **airport.model_dump())
            record = result.single()
            if record:
                return airport
            raise QueryError("Failed to create airport")
        except Exception as e:
            raise QueryError(f"Error creating airport: {str(e)}")
    
    def find_by_id(self, airport_id: str) -> Optional[Airport]:
        """Find airport by ID.
        
        Args:
            airport_id: Airport ID
            
        Returns:
            Airport if found, None otherwise
        """
        query = """
        MATCH (a:Airport {airport_id: $airport_id})
        RETURN a
        """
        try:
            result = self.session.run(query, airport_id=airport_id)
            record = result.single()
            if record:
                data = dict(record["a"])
                return Airport(**data)
            return None
        except Exception as e:
            raise QueryError(f"Error finding airport: {str(e)}")
    
    def find_by_iata(self, iata: str) -> Optional[Airport]:
        """Find airport by IATA code.
        
        Args:
            iata: IATA airport code
            
        Returns:
            Airport if found, None otherwise
        """
        query = """
        MATCH (a:Airport {iata: $iata})
        RETURN a
        """
        try:
            result = self.session.run(query, iata=iata)
            record = result.single()
            if record:
                data = dict(record["a"])
                return Airport(**data)
            return None
        except Exception as e:
            raise QueryError(f"Error finding airport: {str(e)}")
    
    def find_all(self, limit: int = 100) -> List[Airport]:
        """Find all airports.
        
        Args:
            limit: Maximum number of results (default: 100)
            
        Returns:
            List of airports
        """
        query = """
        MATCH (a:Airport)
        RETURN a
        LIMIT $limit
        """
        try:
            result = self.session.run(query, limit=limit)
            airports = []
            for record in result:
                data = dict(record["a"])
                airports.append(Airport(**data))
            return airports
        except Exception as e:
            raise QueryError(f"Error finding airports: {str(e)}")
    
    def find_by_country(self, country: str) -> List[Airport]:
        """Find airports by country.
        
        Args:
            country: Country name
            
        Returns:
            List of airports
        """
        query = """
        MATCH (a:Airport {country: $country})
        RETURN a
        """
        try:
            result = self.session.run(query, country=country)
            airports = []
            for record in result:
                data = dict(record["a"])
                airports.append(Airport(**data))
            return airports
        except Exception as e:
            raise QueryError(f"Error finding airports by country: {str(e)}")


class FlightRepository:
    """Repository for Flight entities."""
    
    def __init__(self, session: Session):
        """Initialize repository with a Neo4j session."""
        self.session = session
    
    def create(self, flight: Flight) -> Flight:
        """Create a new flight.
        
        Args:
            flight: Flight model instance
            
        Returns:
            Created flight
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
            record = result.single()
            if record:
                return flight
            raise QueryError("Failed to create flight")
        except Exception as e:
            raise QueryError(f"Error creating flight: {str(e)}")
    
    def find_by_id(self, flight_id: str) -> Optional[Flight]:
        """Find flight by ID.
        
        Args:
            flight_id: Flight ID
            
        Returns:
            Flight if found, None otherwise
        """
        query = """
        MATCH (f:Flight {flight_id: $flight_id})
        RETURN f
        """
        try:
            result = self.session.run(query, flight_id=flight_id)
            record = result.single()
            if record:
                data = dict(record["f"])
                return Flight(**data)
            return None
        except Exception as e:
            raise QueryError(f"Error finding flight: {str(e)}")
    
    def find_by_flight_number(self, flight_number: str) -> List[Flight]:
        """Find flights by flight number.
        
        Args:
            flight_number: Flight number
            
        Returns:
            List of flights
        """
        query = """
        MATCH (f:Flight {flight_number: $flight_number})
        RETURN f
        """
        try:
            result = self.session.run(query, flight_number=flight_number)
            flights = []
            for record in result:
                data = dict(record["f"])
                flights.append(Flight(**data))
            return flights
        except Exception as e:
            raise QueryError(f"Error finding flights: {str(e)}")
    
    def find_all(self, limit: int = 100) -> List[Flight]:
        """Find all flights.
        
        Args:
            limit: Maximum number of results (default: 100)
            
        Returns:
            List of flights
        """
        query = """
        MATCH (f:Flight)
        RETURN f
        LIMIT $limit
        """
        try:
            result = self.session.run(query, limit=limit)
            flights = []
            for record in result:
                data = dict(record["f"])
                flights.append(Flight(**data))
            return flights
        except Exception as e:
            raise QueryError(f"Error finding flights: {str(e)}")
    
    def find_by_route(self, origin: str, destination: str) -> List[Flight]:
        """Find flights by route.
        
        Args:
            origin: Origin airport code
            destination: Destination airport code
            
        Returns:
            List of flights
        """
        query = """
        MATCH (f:Flight {origin: $origin, destination: $destination})
        RETURN f
        """
        try:
            result = self.session.run(query, origin=origin, destination=destination)
            flights = []
            for record in result:
                data = dict(record["f"])
                flights.append(Flight(**data))
            return flights
        except Exception as e:
            raise QueryError(f"Error finding flights by route: {str(e)}")
    
    def get_flight_with_delays(self, flight_id: str) -> dict:
        """Get flight with associated delays.
        
        Args:
            flight_id: Flight ID
            
        Returns:
            Dictionary with flight and delays
        """
        query = """
        MATCH (f:Flight {flight_id: $flight_id})
        OPTIONAL MATCH (f)-[:HAS_DELAY]->(d:Delay)
        RETURN f, collect(d) as delays
        """
        try:
            result = self.session.run(query, flight_id=flight_id)
            record = result.single()
            if record:
                flight_data = dict(record["f"])
                flight = Flight(**flight_data)
                delays = []
                for delay_node in record["delays"]:
                    if delay_node:
                        delay_data = dict(delay_node)
                        delays.append(Delay(**delay_data))
                return {"flight": flight, "delays": delays}
            raise NotFoundError(f"Flight {flight_id} not found")
        except NotFoundError:
            raise
        except Exception as e:
            raise QueryError(f"Error getting flight with delays: {str(e)}")


class MaintenanceEventRepository:
    """Repository for MaintenanceEvent entities."""
    
    def __init__(self, session: Session):
        """Initialize repository with a Neo4j session."""
        self.session = session
    
    def create(self, event: MaintenanceEvent) -> MaintenanceEvent:
        """Create a new maintenance event.
        
        Args:
            event: MaintenanceEvent model instance
            
        Returns:
            Created maintenance event
        """
        query = """
        MERGE (m:MaintenanceEvent {event_id: $event_id})
        SET m.aircraft_id = $aircraft_id,
            m.component_id = $component_id,
            m.system_id = $system_id,
            m.fault = $fault,
            m.severity = $severity,
            m.corrective_action = $corrective_action,
            m.reported_at = $reported_at
        RETURN m
        """
        try:
            result = self.session.run(query, **event.model_dump())
            record = result.single()
            if record:
                return event
            raise QueryError("Failed to create maintenance event")
        except Exception as e:
            raise QueryError(f"Error creating maintenance event: {str(e)}")
    
    def find_by_id(self, event_id: str) -> Optional[MaintenanceEvent]:
        """Find maintenance event by ID.
        
        Args:
            event_id: Event ID
            
        Returns:
            MaintenanceEvent if found, None otherwise
        """
        query = """
        MATCH (m:MaintenanceEvent {event_id: $event_id})
        RETURN m
        """
        try:
            result = self.session.run(query, event_id=event_id)
            record = result.single()
            if record:
                data = dict(record["m"])
                return MaintenanceEvent(**data)
            return None
        except Exception as e:
            raise QueryError(f"Error finding maintenance event: {str(e)}")
    
    def find_by_aircraft(self, aircraft_id: str) -> List[MaintenanceEvent]:
        """Find maintenance events for an aircraft.
        
        Args:
            aircraft_id: Aircraft ID
            
        Returns:
            List of maintenance events
        """
        query = """
        MATCH (m:MaintenanceEvent {aircraft_id: $aircraft_id})
        RETURN m
        ORDER BY m.reported_at DESC
        """
        try:
            result = self.session.run(query, aircraft_id=aircraft_id)
            events = []
            for record in result:
                data = dict(record["m"])
                events.append(MaintenanceEvent(**data))
            return events
        except Exception as e:
            raise QueryError(f"Error finding maintenance events: {str(e)}")
    
    def find_by_severity(self, severity: str) -> List[MaintenanceEvent]:
        """Find maintenance events by severity.
        
        Args:
            severity: Severity level
            
        Returns:
            List of maintenance events
        """
        query = """
        MATCH (m:MaintenanceEvent {severity: $severity})
        RETURN m
        ORDER BY m.reported_at DESC
        """
        try:
            result = self.session.run(query, severity=severity)
            events = []
            for record in result:
                data = dict(record["m"])
                events.append(MaintenanceEvent(**data))
            return events
        except Exception as e:
            raise QueryError(f"Error finding maintenance events by severity: {str(e)}")
    
    def find_all(self, limit: int = 100) -> List[MaintenanceEvent]:
        """Find all maintenance events.
        
        Args:
            limit: Maximum number of results (default: 100)
            
        Returns:
            List of maintenance events
        """
        query = """
        MATCH (m:MaintenanceEvent)
        RETURN m
        ORDER BY m.reported_at DESC
        LIMIT $limit
        """
        try:
            result = self.session.run(query, limit=limit)
            events = []
            for record in result:
                data = dict(record["m"])
                events.append(MaintenanceEvent(**data))
            return events
        except Exception as e:
            raise QueryError(f"Error finding maintenance events: {str(e)}")


class DelayRepository:
    """Repository for Delay entities."""
    
    def __init__(self, session: Session):
        """Initialize repository with a Neo4j session."""
        self.session = session
    
    def create(self, delay: Delay) -> Delay:
        """Create a new delay.
        
        Args:
            delay: Delay model instance
            
        Returns:
            Created delay
        """
        query = """
        MERGE (d:Delay {delay_id: $delay_id})
        SET d.flight_id = $flight_id,
            d.cause = $cause,
            d.minutes = $minutes
        RETURN d
        """
        try:
            result = self.session.run(query, **delay.model_dump())
            record = result.single()
            if record:
                return delay
            raise QueryError("Failed to create delay")
        except Exception as e:
            raise QueryError(f"Error creating delay: {str(e)}")
    
    def find_by_id(self, delay_id: str) -> Optional[Delay]:
        """Find delay by ID.
        
        Args:
            delay_id: Delay ID
            
        Returns:
            Delay if found, None otherwise
        """
        query = """
        MATCH (d:Delay {delay_id: $delay_id})
        RETURN d
        """
        try:
            result = self.session.run(query, delay_id=delay_id)
            record = result.single()
            if record:
                data = dict(record["d"])
                return Delay(**data)
            return None
        except Exception as e:
            raise QueryError(f"Error finding delay: {str(e)}")
    
    def find_by_flight(self, flight_id: str) -> List[Delay]:
        """Find delays for a flight.
        
        Args:
            flight_id: Flight ID
            
        Returns:
            List of delays
        """
        query = """
        MATCH (d:Delay {flight_id: $flight_id})
        RETURN d
        """
        try:
            result = self.session.run(query, flight_id=flight_id)
            delays = []
            for record in result:
                data = dict(record["d"])
                delays.append(Delay(**data))
            return delays
        except Exception as e:
            raise QueryError(f"Error finding delays: {str(e)}")
    
    def find_by_cause(self, cause: str) -> List[Delay]:
        """Find delays by cause.
        
        Args:
            cause: Delay cause
            
        Returns:
            List of delays
        """
        query = """
        MATCH (d:Delay {cause: $cause})
        RETURN d
        """
        try:
            result = self.session.run(query, cause=cause)
            delays = []
            for record in result:
                data = dict(record["d"])
                delays.append(Delay(**data))
            return delays
        except Exception as e:
            raise QueryError(f"Error finding delays by cause: {str(e)}")
    
    def find_all(self, limit: int = 100) -> List[Delay]:
        """Find all delays.
        
        Args:
            limit: Maximum number of results (default: 100)
            
        Returns:
            List of delays
        """
        query = """
        MATCH (d:Delay)
        RETURN d
        LIMIT $limit
        """
        try:
            result = self.session.run(query, limit=limit)
            delays = []
            for record in result:
                data = dict(record["d"])
                delays.append(Delay(**data))
            return delays
        except Exception as e:
            raise QueryError(f"Error finding delays: {str(e)}")
