"""Connection management for Neo4j database."""

from typing import Optional
from neo4j import GraphDatabase, Driver, Session
from .exceptions import ConnectionError


class Neo4jConnection:
    """Manages connection to Neo4j database.
    
    Provides connection lifecycle management and session creation.
    Supports context manager pattern for automatic resource cleanup.
    
    Example:
        >>> conn = Neo4jConnection("bolt://localhost:7687", "neo4j", "password")
        >>> with conn.session() as session:
        ...     result = session.run("MATCH (n) RETURN n LIMIT 1")
        >>> conn.close()
        
        Or using context manager:
        >>> with Neo4jConnection("bolt://localhost:7687", "neo4j", "password") as conn:
        ...     with conn.session() as session:
        ...         result = session.run("MATCH (n) RETURN n LIMIT 1")
    """
    
    def __init__(
        self,
        uri: str,
        username: str,
        password: str,
        database: str = "neo4j"
    ):
        """Initialize connection to Neo4j.
        
        Args:
            uri: Neo4j connection URI (e.g., bolt://localhost:7687)
            username: Database username
            password: Database password
            database: Database name (default: neo4j)
            
        Raises:
            ConnectionError: If connection to database fails
        """
        self.uri = uri
        self.username = username
        self.database = database
        
        try:
            self._driver: Driver = GraphDatabase.driver(
                uri,
                auth=(username, password)
            )
            # Verify connectivity
            self._driver.verify_connectivity()
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Neo4j: {str(e)}") from e
    
    def session(self) -> Session:
        """Create a new database session.
        
        Returns:
            Neo4j session object
        """
        return self._driver.session(database=self.database)
    
    def close(self) -> None:
        """Close the database connection."""
        if self._driver:
            self._driver.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - ensures connection is closed."""
        self.close()
