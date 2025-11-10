"""Pytest configuration and fixtures."""

import os
import pytest
from testcontainers.neo4j import Neo4jContainer
from neo4j_client import Neo4jConnection


@pytest.fixture(scope="session")
def neo4j_container():
    """Provide a Neo4j container for testing."""
    container = Neo4jContainer("neo4j:5.15")
    container.start()
    
    # Wait for Neo4j to be ready
    container.get_driver().verify_connectivity()
    
    yield container
    
    container.stop()


@pytest.fixture(scope="session")
def neo4j_uri(neo4j_container):
    """Get Neo4j connection URI."""
    return neo4j_container.get_connection_url()


@pytest.fixture(scope="session")
def neo4j_username():
    """Get Neo4j username."""
    return "neo4j"


@pytest.fixture(scope="session")
def neo4j_password(neo4j_container):
    """Get Neo4j password."""
    return neo4j_container.password


@pytest.fixture
def connection(neo4j_uri, neo4j_username, neo4j_password):
    """Provide a Neo4j connection for testing."""
    conn = Neo4jConnection(
        uri=neo4j_uri,
        username=neo4j_username,
        password=neo4j_password,
        database="neo4j"
    )
    conn.connect()
    
    yield conn
    
    # Clean up database after each test
    with conn.get_session() as session:
        session.run("MATCH (n) DETACH DELETE n")
    
    conn.close()
