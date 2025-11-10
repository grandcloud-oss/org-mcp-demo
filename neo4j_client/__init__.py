"""Neo4j Python Client for Airplane Data.

This package provides a simple, type-safe Python client for working with
airplane data stored in a Neo4j database.
"""

from .connection import Neo4jConnection
from .models import (
    Aircraft,
    Flight,
    Airport,
    MaintenanceEvent,
    System,
    Component,
    Sensor,
    Delay,
    Reading,
)
from .repository import (
    AircraftRepository,
    FlightRepository,
    AirportRepository,
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
    "Flight",
    "Airport",
    "MaintenanceEvent",
    "System",
    "Component",
    "Sensor",
    "Delay",
    "Reading",
    # Repositories
    "AircraftRepository",
    "FlightRepository",
    "AirportRepository",
    "MaintenanceEventRepository",
    "SystemRepository",
    "DelayRepository",
    # Exceptions
    "Neo4jClientError",
    "ConnectionError",
    "QueryError",
    "NotFoundError",
]
