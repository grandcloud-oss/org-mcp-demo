"""Pytest configuration and fixtures."""

import os
import pytest
from testcontainers.neo4j import Neo4jContainer
from neo4j_client import Neo4jConnection


@pytest.fixture(scope="session")
def neo4j_container():
    """Provide a Neo4j container for testing."""
    # Create container with password
    container = Neo4jContainer("neo4j:5.15", password="test12345678")
    container.start()
    yield container
    container.stop()


@pytest.fixture(scope="session")
def neo4j_uri(neo4j_container):
    """Get Neo4j URI from container."""
    return neo4j_container.get_connection_url()


@pytest.fixture(scope="session")
def neo4j_credentials():
    """Get Neo4j credentials."""
    return {
        "username": "neo4j",
        "password": "test12345678",
    }


@pytest.fixture
def connection(neo4j_uri, neo4j_credentials):
    """Provide a Neo4j connection for testing."""
    conn = Neo4jConnection(
        uri=neo4j_uri,
        username=neo4j_credentials["username"],
        password=neo4j_credentials["password"],
    )
    conn.connect()
    yield conn
    
    # Cleanup: delete all nodes and relationships
    with conn.get_session() as session:
        session.run("MATCH (n) DETACH DELETE n")
    
    conn.close()


@pytest.fixture
def session(connection):
    """Provide a Neo4j session for testing."""
    session = connection.get_session()
    yield session
    session.close()
