"""Pytest configuration and fixtures."""

import os
import pytest
from testcontainers.neo4j import Neo4jContainer
from neo4j_client import Neo4jConnection


@pytest.fixture(scope="session")
def neo4j_container():
    """Provide a Neo4j testcontainer for integration tests."""
    with Neo4jContainer("neo4j:5.12", password="testpassword") as container:
        yield container


@pytest.fixture(scope="session")
def neo4j_connection(neo4j_container):
    """Provide a Neo4j connection using testcontainer."""
    connection = Neo4jConnection(
        uri=neo4j_container.get_connection_url(),
        username="neo4j",
        password="testpassword"
    )
    connection.connect()
    yield connection
    connection.close()


@pytest.fixture
def neo4j_session(neo4j_connection):
    """Provide a fresh Neo4j session for each test."""
    session = neo4j_connection.get_session()
    yield session
    # Cleanup: Clear all data after each test
    session.run("MATCH (n) DETACH DELETE n")
    session.close()
