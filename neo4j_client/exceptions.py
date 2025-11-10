"""Custom exceptions for Neo4j client."""


class Neo4jClientError(Exception):
    """Base exception for Neo4j client errors."""
    pass


class ConnectionError(Neo4jClientError):
    """Exception raised for connection errors."""
    pass


class QueryError(Neo4jClientError):
    """Exception raised for query execution errors."""
    pass


class NotFoundError(Neo4jClientError):
    """Exception raised when a resource is not found."""
    pass
