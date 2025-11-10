"""Repository pattern implementations for Neo4j entities."""

from typing import List, Optional
from neo4j import Session
from .models import (
    Aircraft, Flight, Airport, MaintenanceEvent,
    System, Component, Sensor, Delay, Reading
)
from .exceptions import QueryError, NotFoundError


class AircraftRepository:
    """Repository for Aircraft entities."""

    def __init__(self, session: Session):
        """
        Initialize repository with Neo4j session.

        Args:
            session: Active Neo4j session
        """
        self.session = session

    def create(self, aircraft: Aircraft) -> Aircraft:
        """
        Create a new aircraft.

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
            a.operator = $operator,
            a.manufacturer = $manufacturer
        RETURN a
        """
        try:
            result = self.session.run(query, **aircraft.model_dump())
            record = result.single()
            if record:
                return Aircraft(**record["a"])
            raise QueryError("Failed to create aircraft")
        except Exception as e:
            raise QueryError(f"Error creating aircraft: {e}")

    def find_by_id(self, aircraft_id: str) -> Optional[Aircraft]:
        """
        Find aircraft by ID.

        Args:
            aircraft_id: Aircraft identifier

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
            return Aircraft(**record["a"]) if record else None
        except Exception as e:
            raise QueryError(f"Error finding aircraft: {e}")

    def find_by_tail_number(self, tail_number: str) -> Optional[Aircraft]:
        """
        Find aircraft by tail number.

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
            return Aircraft(**record["a"]) if record else None
        except Exception as e:
            raise QueryError(f"Error finding aircraft: {e}")

    def find_all(self, limit: int = 100) -> List[Aircraft]:
        """
        Find all aircraft.

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
            return [Aircraft(**record["a"]) for record in result]
        except Exception as e:
            raise QueryError(f"Error finding aircraft: {e}")

    def find_by_operator(self, operator: str) -> List[Aircraft]:
        """
        Find aircraft by operator.

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
            return [Aircraft(**record["a"]) for record in result]
        except Exception as e:
            raise QueryError(f"Error finding aircraft: {e}")

    def update(self, aircraft: Aircraft) -> Aircraft:
        """
        Update an aircraft.

        Args:
            aircraft: Aircraft model instance with updated data

        Returns:
            Updated aircraft
        """
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})
        SET a.tail_number = $tail_number,
            a.icao24 = $icao24,
            a.model = $model,
            a.operator = $operator,
            a.manufacturer = $manufacturer
        RETURN a
        """
        try:
            result = self.session.run(query, **aircraft.model_dump())
            record = result.single()
            if record:
                return Aircraft(**record["a"])
            raise NotFoundError(f"Aircraft not found: {aircraft.aircraft_id}")
        except NotFoundError:
            raise
        except Exception as e:
            raise QueryError(f"Error updating aircraft: {e}")

    def delete(self, aircraft_id: str) -> bool:
        """
        Delete an aircraft.

        Args:
            aircraft_id: Aircraft identifier

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
            raise QueryError(f"Error deleting aircraft: {e}")


class FlightRepository:
    """Repository for Flight entities."""

    def __init__(self, session: Session):
        """
        Initialize repository with Neo4j session.

        Args:
            session: Active Neo4j session
        """
        self.session = session

    def create(self, flight: Flight) -> Flight:
        """
        Create a new flight.

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
                return Flight(**record["f"])
            raise QueryError("Failed to create flight")
        except Exception as e:
            raise QueryError(f"Error creating flight: {e}")

    def find_by_id(self, flight_id: str) -> Optional[Flight]:
        """
        Find flight by ID.

        Args:
            flight_id: Flight identifier

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
            return Flight(**record["f"]) if record else None
        except Exception as e:
            raise QueryError(f"Error finding flight: {e}")

    def find_by_flight_number(self, flight_number: str) -> List[Flight]:
        """
        Find flights by flight number.

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
            return [Flight(**record["f"]) for record in result]
        except Exception as e:
            raise QueryError(f"Error finding flights: {e}")

    def find_by_aircraft(self, aircraft_id: str) -> List[Flight]:
        """
        Find flights by aircraft.

        Args:
            aircraft_id: Aircraft identifier

        Returns:
            List of flights
        """
        query = """
        MATCH (f:Flight {aircraft_id: $aircraft_id})
        RETURN f
        """
        try:
            result = self.session.run(query, aircraft_id=aircraft_id)
            return [Flight(**record["f"]) for record in result]
        except Exception as e:
            raise QueryError(f"Error finding flights: {e}")

    def find_by_route(self, origin: str, destination: str) -> List[Flight]:
        """
        Find flights by route.

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
            return [Flight(**record["f"]) for record in result]
        except Exception as e:
            raise QueryError(f"Error finding flights: {e}")

    def find_all(self, limit: int = 100) -> List[Flight]:
        """
        Find all flights.

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
            return [Flight(**record["f"]) for record in result]
        except Exception as e:
            raise QueryError(f"Error finding flights: {e}")


class AirportRepository:
    """Repository for Airport entities."""

    def __init__(self, session: Session):
        """
        Initialize repository with Neo4j session.

        Args:
            session: Active Neo4j session
        """
        self.session = session

    def create(self, airport: Airport) -> Airport:
        """
        Create a new airport.

        Args:
            airport: Airport model instance

        Returns:
            Created airport
        """
        query = """
        MERGE (ap:Airport {airport_id: $airport_id})
        SET ap.name = $name,
            ap.city = $city,
            ap.country = $country,
            ap.iata = $iata,
            ap.icao = $icao,
            ap.lat = $lat,
            ap.lon = $lon
        RETURN ap
        """
        try:
            result = self.session.run(query, **airport.model_dump())
            record = result.single()
            if record:
                return Airport(**record["ap"])
            raise QueryError("Failed to create airport")
        except Exception as e:
            raise QueryError(f"Error creating airport: {e}")

    def find_by_id(self, airport_id: str) -> Optional[Airport]:
        """
        Find airport by ID.

        Args:
            airport_id: Airport identifier

        Returns:
            Airport if found, None otherwise
        """
        query = """
        MATCH (ap:Airport {airport_id: $airport_id})
        RETURN ap
        """
        try:
            result = self.session.run(query, airport_id=airport_id)
            record = result.single()
            return Airport(**record["ap"]) if record else None
        except Exception as e:
            raise QueryError(f"Error finding airport: {e}")

    def find_by_iata(self, iata: str) -> Optional[Airport]:
        """
        Find airport by IATA code.

        Args:
            iata: IATA airport code

        Returns:
            Airport if found, None otherwise
        """
        query = """
        MATCH (ap:Airport {iata: $iata})
        RETURN ap
        """
        try:
            result = self.session.run(query, iata=iata)
            record = result.single()
            return Airport(**record["ap"]) if record else None
        except Exception as e:
            raise QueryError(f"Error finding airport: {e}")

    def find_by_country(self, country: str) -> List[Airport]:
        """
        Find airports by country.

        Args:
            country: Country name

        Returns:
            List of airports
        """
        query = """
        MATCH (ap:Airport {country: $country})
        RETURN ap
        """
        try:
            result = self.session.run(query, country=country)
            return [Airport(**record["ap"]) for record in result]
        except Exception as e:
            raise QueryError(f"Error finding airports: {e}")

    def find_all(self) -> List[Airport]:
        """
        Find all airports.

        Returns:
            List of airports
        """
        query = """
        MATCH (ap:Airport)
        RETURN ap
        """
        try:
            result = self.session.run(query)
            return [Airport(**record["ap"]) for record in result]
        except Exception as e:
            raise QueryError(f"Error finding airports: {e}")


class MaintenanceEventRepository:
    """Repository for MaintenanceEvent entities."""

    def __init__(self, session: Session):
        """
        Initialize repository with Neo4j session.

        Args:
            session: Active Neo4j session
        """
        self.session = session

    def create(self, event: MaintenanceEvent) -> MaintenanceEvent:
        """
        Create a new maintenance event.

        Args:
            event: MaintenanceEvent model instance

        Returns:
            Created maintenance event
        """
        query = """
        MERGE (me:MaintenanceEvent {event_id: $event_id})
        SET me.aircraft_id = $aircraft_id,
            me.system_id = $system_id,
            me.component_id = $component_id,
            me.fault = $fault,
            me.severity = $severity,
            me.corrective_action = $corrective_action,
            me.reported_at = $reported_at
        RETURN me
        """
        try:
            result = self.session.run(query, **event.model_dump())
            record = result.single()
            if record:
                return MaintenanceEvent(**record["me"])
            raise QueryError("Failed to create maintenance event")
        except Exception as e:
            raise QueryError(f"Error creating maintenance event: {e}")

    def find_by_id(self, event_id: str) -> Optional[MaintenanceEvent]:
        """
        Find maintenance event by ID.

        Args:
            event_id: Event identifier

        Returns:
            MaintenanceEvent if found, None otherwise
        """
        query = """
        MATCH (me:MaintenanceEvent {event_id: $event_id})
        RETURN me
        """
        try:
            result = self.session.run(query, event_id=event_id)
            record = result.single()
            return MaintenanceEvent(**record["me"]) if record else None
        except Exception as e:
            raise QueryError(f"Error finding maintenance event: {e}")

    def find_by_aircraft(self, aircraft_id: str) -> List[MaintenanceEvent]:
        """
        Find maintenance events by aircraft.

        Args:
            aircraft_id: Aircraft identifier

        Returns:
            List of maintenance events
        """
        query = """
        MATCH (me:MaintenanceEvent {aircraft_id: $aircraft_id})
        RETURN me
        ORDER BY me.reported_at DESC
        """
        try:
            result = self.session.run(query, aircraft_id=aircraft_id)
            return [MaintenanceEvent(**record["me"]) for record in result]
        except Exception as e:
            raise QueryError(f"Error finding maintenance events: {e}")

    def find_by_severity(self, severity: str) -> List[MaintenanceEvent]:
        """
        Find maintenance events by severity.

        Args:
            severity: Severity level

        Returns:
            List of maintenance events
        """
        query = """
        MATCH (me:MaintenanceEvent {severity: $severity})
        RETURN me
        ORDER BY me.reported_at DESC
        """
        try:
            result = self.session.run(query, severity=severity)
            return [MaintenanceEvent(**record["me"]) for record in result]
        except Exception as e:
            raise QueryError(f"Error finding maintenance events: {e}")


class SystemRepository:
    """Repository for System entities."""

    def __init__(self, session: Session):
        """
        Initialize repository with Neo4j session.

        Args:
            session: Active Neo4j session
        """
        self.session = session

    def find_by_aircraft(self, aircraft_id: str) -> List[System]:
        """
        Find systems by aircraft.

        Args:
            aircraft_id: Aircraft identifier

        Returns:
            List of systems
        """
        query = """
        MATCH (s:System {aircraft_id: $aircraft_id})
        RETURN s
        """
        try:
            result = self.session.run(query, aircraft_id=aircraft_id)
            return [System(**record["s"]) for record in result]
        except Exception as e:
            raise QueryError(f"Error finding systems: {e}")

    def find_by_id(self, system_id: str) -> Optional[System]:
        """
        Find system by ID.

        Args:
            system_id: System identifier

        Returns:
            System if found, None otherwise
        """
        query = """
        MATCH (s:System {system_id: $system_id})
        RETURN s
        """
        try:
            result = self.session.run(query, system_id=system_id)
            record = result.single()
            return System(**record["s"]) if record else None
        except Exception as e:
            raise QueryError(f"Error finding system: {e}")


class DelayRepository:
    """Repository for Delay entities."""

    def __init__(self, session: Session):
        """
        Initialize repository with Neo4j session.

        Args:
            session: Active Neo4j session
        """
        self.session = session

    def find_by_flight(self, flight_id: str) -> List[Delay]:
        """
        Find delays by flight.

        Args:
            flight_id: Flight identifier

        Returns:
            List of delays
        """
        query = """
        MATCH (d:Delay {flight_id: $flight_id})
        RETURN d
        """
        try:
            result = self.session.run(query, flight_id=flight_id)
            return [Delay(**record["d"]) for record in result]
        except Exception as e:
            raise QueryError(f"Error finding delays: {e}")

    def find_by_cause(self, cause: str) -> List[Delay]:
        """
        Find delays by cause.

        Args:
            cause: Delay cause

        Returns:
            List of delays
        """
        query = """
        MATCH (d:Delay {cause: $cause})
        RETURN d
        ORDER BY d.minutes DESC
        """
        try:
            result = self.session.run(query, cause=cause)
            return [Delay(**record["d"]) for record in result]
        except Exception as e:
            raise QueryError(f"Error finding delays: {e}")
