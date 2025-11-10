"""Pytest fixtures for Neo4j client tests."""

import os
import pytest
from testcontainers.neo4j import Neo4jContainer
from neo4j_client import Neo4jConnection


@pytest.fixture(scope="session")
def neo4j_container():
    """Provide a Neo4j testcontainer for the test session.
    
    Yields:
        Neo4jContainer instance with running Neo4j database
    """
    with Neo4jContainer("neo4j:5.13.0") as container:
        yield container


@pytest.fixture(scope="session")
def neo4j_uri(neo4j_container):
    """Get Neo4j connection URI from container.
    
    Args:
        neo4j_container: Neo4j container fixture
        
    Returns:
        Connection URI string
    """
    return neo4j_container.get_connection_url()


@pytest.fixture(scope="session")
def neo4j_credentials():
    """Get Neo4j credentials.
    
    Returns:
        Tuple of (username, password)
    """
    return ("neo4j", "password")


@pytest.fixture
def neo4j_connection(neo4j_uri, neo4j_credentials):
    """Provide a Neo4j connection for each test.
    
    Args:
        neo4j_uri: Connection URI from container
        neo4j_credentials: Username and password tuple
        
    Yields:
        Neo4jConnection instance
    """
    username, password = neo4j_credentials
    connection = Neo4jConnection(neo4j_uri, username, password)
    yield connection
    connection.close()


@pytest.fixture
def neo4j_session(neo4j_connection):
    """Provide a Neo4j session for each test.
    
    Args:
        neo4j_connection: Neo4j connection fixture
        
    Yields:
        Neo4j session instance
    """
    with neo4j_connection.session() as session:
        # Clean up any existing data before test
        session.run("MATCH (n) DETACH DELETE n")
        yield session
        # Clean up after test
        session.run("MATCH (n) DETACH DELETE n")
