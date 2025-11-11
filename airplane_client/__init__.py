"""Airplane Database Client - Python client for Neo4j airplane database."""

from .models import (
    Aircraft,
    Airport,
    Flight,
    System,
    Component,
    Sensor,
    MaintenanceEvent,
    Delay,
    Reading,
)
from .connection import Neo4jConnection
from .repository import (
    AircraftRepository,
    AirportRepository,
    FlightRepository,
    SystemRepository,
    MaintenanceEventRepository,
)
from .exceptions import (
    AirplaneClientError,
    ConnectionError,
    QueryError,
    NotFoundError,
)

__version__ = "0.1.0"

__all__ = [
    # Models
    "Aircraft",
    "Airport",
    "Flight",
    "System",
    "Component",
    "Sensor",
    "MaintenanceEvent",
    "Delay",
    "Reading",
    # Connection
    "Neo4jConnection",
    # Repositories
    "AircraftRepository",
    "AirportRepository",
    "FlightRepository",
    "SystemRepository",
    "MaintenanceEventRepository",
    # Exceptions
    "AirplaneClientError",
    "ConnectionError",
    "QueryError",
    "NotFoundError",
]
