"""Neo4j Python Client for Airplane Data.

A simple, high-quality client library for working with airplane data in Neo4j.
"""

from .connection import Neo4jConnection
from .models import (
    Aircraft,
    Airport,
    Flight,
    System,
    Component,
    MaintenanceEvent,
    Delay,
    Sensor,
    Reading,
)
from .repository import (
    AircraftRepository,
    AirportRepository,
    FlightRepository,
    MaintenanceEventRepository,
    SystemRepository,
    DelayRepository,
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
    "System",
    "Component",
    "MaintenanceEvent",
    "Delay",
    "Sensor",
    "Reading",
    # Repositories
    "AircraftRepository",
    "AirportRepository",
    "FlightRepository",
    "MaintenanceEventRepository",
    "SystemRepository",
    "DelayRepository",
    # Exceptions
    "Neo4jClientError",
    "ConnectionError",
    "QueryError",
    "NotFoundError",
]
