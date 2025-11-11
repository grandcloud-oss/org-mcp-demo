"""Pytest fixtures for airplane client tests."""

import os
import pytest
from testcontainers.neo4j import Neo4jContainer
from airplane_client import Neo4jConnection


@pytest.fixture(scope="session")
def neo4j_container():
    """Session-scoped Neo4j container fixture."""
    with Neo4jContainer("neo4j:5.13", password="testpassword") as container:
        yield container


@pytest.fixture(scope="session")
def neo4j_uri(neo4j_container):
    """Get Neo4j URI from container."""
    return neo4j_container.get_connection_url()


@pytest.fixture
def neo4j_connection(neo4j_container):
    """Function-scoped Neo4j connection fixture."""
    uri = neo4j_container.get_connection_url()
    username = "neo4j"
    password = "testpassword"
    
    connection = Neo4jConnection(uri, username, password)
    connection.connect()
    
    yield connection
    
    # Cleanup: delete all nodes and relationships
    with connection.get_session() as session:
        session.run("MATCH (n) DETACH DELETE n")
    
    connection.close()
