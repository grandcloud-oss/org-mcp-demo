"""Neo4j Python client for airplane database."""

from .connection import Neo4jConnection
from .models import (
    Aircraft,
    Airport,
    Flight,
    Delay,
    System,
    Component,
    Sensor,
    MaintenanceEvent,
    Reading,
)
from .repository import (
    AircraftRepository,
    AirportRepository,
    FlightRepository,
    DelayRepository,
    MaintenanceEventRepository,
)
from .exceptions import (
    Neo4jClientError,
    ConnectionError,
    QueryError,
    NotFoundError,
)

__version__ = "0.1.0"

__all__ = [
    # Connection
    "Neo4jConnection",
    # Models
    "Aircraft",
    "Airport",
    "Flight",
    "Delay",
    "System",
    "Component",
    "Sensor",
    "MaintenanceEvent",
    "Reading",
    # Repositories
    "AircraftRepository",
    "AirportRepository",
    "FlightRepository",
    "DelayRepository",
    "MaintenanceEventRepository",
    # Exceptions
    "Neo4jClientError",
    "ConnectionError",
    "QueryError",
    "NotFoundError",
]
