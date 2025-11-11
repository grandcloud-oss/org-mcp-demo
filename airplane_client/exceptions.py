"""Custom exceptions for the airplane client."""


class AirplaneClientError(Exception):
    """Base exception for all airplane client errors."""
    pass


class ConnectionError(AirplaneClientError):
    """Raised when there's a connection error to Neo4j."""
    pass


class QueryError(AirplaneClientError):
    """Raised when a query fails to execute."""
    pass


class NotFoundError(AirplaneClientError):
    """Raised when a requested entity is not found."""
    pass
