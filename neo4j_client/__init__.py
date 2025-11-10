"""Neo4j Python client for airplane data."""

from .models import (
    Aircraft,
    Airport,
    Flight,
    MaintenanceEvent,
    System,
    Component,
    Sensor,
    Delay,
    Reading,
)
from .repository import (
    AircraftRepository,
    AirportRepository,
    FlightRepository,
    MaintenanceEventRepository,
    SystemRepository,
)
from .connection import Neo4jConnection
from .exceptions import (
    Neo4jClientError,
    ConnectionError,
    QueryError,
    NotFoundError,
)

__all__ = [
    # Models
    "Aircraft",
    "Airport",
    "Flight",
    "MaintenanceEvent",
    "System",
    "Component",
    "Sensor",
    "Delay",
    "Reading",
    # Repositories
    "AircraftRepository",
    "AirportRepository",
    "FlightRepository",
    "MaintenanceEventRepository",
    "SystemRepository",
    # Connection
    "Neo4jConnection",
    # Exceptions
    "Neo4jClientError",
    "ConnectionError",
    "QueryError",
    "NotFoundError",
]
