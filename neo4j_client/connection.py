"""Connection management for Neo4j database."""

from typing import Optional
from neo4j import GraphDatabase, Driver, Session
from .exceptions import ConnectionError as ClientConnectionError


class Neo4jConnection:
    """Manages connection to Neo4j database."""
    
    def __init__(
        self,
        uri: str,
        username: str,
        password: str,
        database: str = "neo4j"
    ):
        """Initialize Neo4j connection.
        
        Args:
            uri: Neo4j database URI (e.g., 'bolt://localhost:7687')
            username: Database username
            password: Database password
            database: Database name (default: 'neo4j')
        """
        self.uri = uri
        self.username = username
        self.password = password
        self.database = database
        self._driver: Optional[Driver] = None
        
    def connect(self) -> Driver:
        """Establish connection to Neo4j database.
        
        Returns:
            Neo4j driver instance
            
        Raises:
            ClientConnectionError: If connection fails
        """
        try:
            self._driver = GraphDatabase.driver(
                self.uri,
                auth=(self.username, self.password)
            )
            # Test connection
            self._driver.verify_connectivity()
            return self._driver
        except Exception as e:
            raise ClientConnectionError(f"Failed to connect to Neo4j: {e}")
    
    def close(self) -> None:
        """Close connection to Neo4j database."""
        if self._driver:
            self._driver.close()
            self._driver = None
    
    def get_session(self) -> Session:
        """Get a new session from the driver.
        
        Returns:
            Neo4j session instance
            
        Raises:
            ClientConnectionError: If driver is not initialized
        """
        if not self._driver:
            raise ClientConnectionError("Driver not initialized. Call connect() first.")
        return self._driver.session(database=self.database)
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
