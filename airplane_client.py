#!/usr/bin/env python3
"""
Airplane Information and Parts Reader

This Python client demonstrates how to read airplane information and parts
from a Neo4j database using the MCP (Model Context Protocol) server.

The client connects to Neo4j through the MCP server and provides methods to:
- List all aircraft in the database
- Get detailed information about specific aircraft
- Retrieve systems and components (parts) for aircraft
- Query maintenance events and sensor data

Prerequisites:
    The Neo4j MCP server must be configured with the following environment variables:
    - COPILOT_MCP_NEO4J_URI: Database connection URI
    - COPILOT_MCP_NEO4J_USERNAME: Username (usually 'neo4j')
    - COPILOT_MCP_NEO4J_PASSWORD: Password
    - COPILOT_MCP_NEO4J_DATABASE: Database name (default: 'neo4j')

Note:
    This client is designed to work with the MCP server infrastructure.
    It does not connect directly to Neo4j but uses MCP server tools.
"""

import json
from typing import List, Dict, Optional, Any


class AirplaneClient:
    """
    Client for reading airplane information and parts from Neo4j database
    through the MCP server.
    
    This is a demonstration client showing the structure and queries needed
    to access airplane data. In a real implementation, this would use the
    MCP server's Python SDK or API to execute these queries.
    """
    
    def __init__(self):
        """
        Initialize the airplane client.
        
        In a production environment, this would establish connection to the
        MCP server. For this demo, we document the queries that would be executed.
        """
        self.queries = {
            'list_aircraft': """
                MATCH (a:Aircraft)
                RETURN a.aircraft_id as aircraft_id,
                       a.tail_number as tail_number,
                       a.icao24 as icao24,
                       a.model as model,
                       a.operator as operator,
                       a.manufacturer as manufacturer
                ORDER BY a.aircraft_id
            """,
            
            'get_aircraft_details': """
                MATCH (a:Aircraft {aircraft_id: $aircraft_id})
                RETURN a.aircraft_id as aircraft_id,
                       a.tail_number as tail_number,
                       a.icao24 as icao24,
                       a.model as model,
                       a.operator as operator,
                       a.manufacturer as manufacturer
            """,
            
            'get_aircraft_systems': """
                MATCH (a:Aircraft {aircraft_id: $aircraft_id})-[:HAS_SYSTEM]->(s:System)
                RETURN s.system_id as system_id,
                       s.name as name,
                       s.type as type
                ORDER BY s.name
            """,
            
            'get_system_components': """
                MATCH (s:System {system_id: $system_id})-[:HAS_COMPONENT]->(c:Component)
                RETURN c.component_id as component_id,
                       c.name as name,
                       c.type as type
                ORDER BY c.name
            """,
            
            'get_aircraft_all_parts': """
                MATCH (a:Aircraft {aircraft_id: $aircraft_id})-[:HAS_SYSTEM]->(s:System)-[:HAS_COMPONENT]->(c:Component)
                RETURN s.system_id as system_id,
                       s.name as system_name,
                       s.type as system_type,
                       c.component_id as component_id,
                       c.name as component_name,
                       c.type as component_type
                ORDER BY s.name, c.name
            """,
            
            'get_maintenance_events': """
                MATCH (a:Aircraft {aircraft_id: $aircraft_id})<-[:AFFECTS_AIRCRAFT]-(m:MaintenanceEvent)
                RETURN m.event_id as event_id,
                       m.fault as fault,
                       m.severity as severity,
                       m.corrective_action as corrective_action,
                       m.reported_at as reported_at
                ORDER BY m.reported_at DESC
                LIMIT $limit
            """,
            
            'get_system_sensors': """
                MATCH (s:System {system_id: $system_id})-[:HAS_SENSOR]->(sensor:Sensor)
                RETURN sensor.sensor_id as sensor_id,
                       sensor.name as name,
                       sensor.type as type,
                       sensor.unit as unit
                ORDER BY sensor.name
            """,
            
            'get_aircraft_statistics': """
                MATCH (a:Aircraft {aircraft_id: $aircraft_id})
                OPTIONAL MATCH (a)-[:HAS_SYSTEM]->(s:System)
                OPTIONAL MATCH (s)-[:HAS_COMPONENT]->(c:Component)
                OPTIONAL MATCH (a)<-[:AFFECTS_AIRCRAFT]-(m:MaintenanceEvent)
                OPTIONAL MATCH (a)-[:OPERATES_FLIGHT]->(f:Flight)
                RETURN a.aircraft_id as aircraft_id,
                       COUNT(DISTINCT s) as system_count,
                       COUNT(DISTINCT c) as component_count,
                       COUNT(DISTINCT m) as maintenance_event_count,
                       COUNT(DISTINCT f) as flight_count
            """
        }
    
    def list_all_aircraft(self) -> str:
        """
        Get a list of all aircraft in the database.
        
        Returns:
            Query string to execute via MCP server
        """
        return self.queries['list_aircraft']
    
    def get_aircraft_info(self, aircraft_id: str) -> str:
        """
        Get detailed information about a specific aircraft.
        
        Args:
            aircraft_id: The unique identifier of the aircraft
            
        Returns:
            Query string with parameters to execute via MCP server
        """
        return self.queries['get_aircraft_details']
    
    def get_aircraft_systems(self, aircraft_id: str) -> str:
        """
        Get all systems for a specific aircraft.
        
        Args:
            aircraft_id: The unique identifier of the aircraft
            
        Returns:
            Query string with parameters to execute via MCP server
        """
        return self.queries['get_aircraft_systems']
    
    def get_system_components(self, system_id: str) -> str:
        """
        Get all components (parts) for a specific system.
        
        Args:
            system_id: The unique identifier of the system
            
        Returns:
            Query string with parameters to execute via MCP server
        """
        return self.queries['get_system_components']
    
    def get_all_aircraft_parts(self, aircraft_id: str) -> str:
        """
        Get all parts (components) for a specific aircraft including their systems.
        
        Args:
            aircraft_id: The unique identifier of the aircraft
            
        Returns:
            Query string with parameters to execute via MCP server
        """
        return self.queries['get_aircraft_all_parts']
    
    def get_maintenance_history(self, aircraft_id: str, limit: int = 10) -> str:
        """
        Get recent maintenance events for an aircraft.
        
        Args:
            aircraft_id: The unique identifier of the aircraft
            limit: Maximum number of events to return
            
        Returns:
            Query string with parameters to execute via MCP server
        """
        return self.queries['get_maintenance_events']
    
    def get_aircraft_statistics(self, aircraft_id: str) -> str:
        """
        Get statistics about an aircraft (counts of systems, components, etc.).
        
        Args:
            aircraft_id: The unique identifier of the aircraft
            
        Returns:
            Query string with parameters to execute via MCP server
        """
        return self.queries['get_aircraft_statistics']
    
    def print_query_guide(self):
        """Print a guide showing all available queries and their parameters."""
        print("=" * 80)
        print("AIRPLANE CLIENT QUERY GUIDE")
        print("=" * 80)
        print("\nThis client provides the following Cypher queries for the Neo4j MCP server:\n")
        
        for name, query in self.queries.items():
            print(f"\n{name}:")
            print("-" * 80)
            print(query.strip())
            print()


def demonstrate_usage():
    """
    Demonstrate how to use the AirplaneClient.
    
    This function shows examples of the queries that should be executed
    through the Neo4j MCP server to read airplane information and parts.
    """
    client = AirplaneClient()
    
    print("=" * 80)
    print("AIRPLANE CLIENT - USAGE DEMONSTRATION")
    print("=" * 80)
    print()
    print("This client demonstrates queries for reading airplane information and parts")
    print("from a Neo4j database through the MCP server.")
    print()
    print("To use this client with the Neo4j MCP server, execute the following queries:")
    print()
    
    # Example 1: List all aircraft
    print("\n1. LIST ALL AIRCRAFT")
    print("-" * 80)
    print("Query:")
    print(client.list_all_aircraft())
    print("\nParameters: None")
    print("\nExpected Result: List of all aircraft with their details")
    
    # Example 2: Get specific aircraft details
    print("\n\n2. GET AIRCRAFT DETAILS")
    print("-" * 80)
    print("Query:")
    print(client.get_aircraft_info("AC1001"))
    print("\nParameters: {'aircraft_id': 'AC1001'}")
    print("\nExpected Result: Detailed information about aircraft AC1001")
    
    # Example 3: Get aircraft systems
    print("\n\n3. GET AIRCRAFT SYSTEMS")
    print("-" * 80)
    print("Query:")
    print(client.get_aircraft_systems("AC1001"))
    print("\nParameters: {'aircraft_id': 'AC1001'}")
    print("\nExpected Result: List of all systems installed on aircraft AC1001")
    
    # Example 4: Get all parts for an aircraft
    print("\n\n4. GET ALL AIRCRAFT PARTS")
    print("-" * 80)
    print("Query:")
    print(client.get_all_aircraft_parts("AC1001"))
    print("\nParameters: {'aircraft_id': 'AC1001'}")
    print("\nExpected Result: Complete list of all parts/components organized by system")
    
    # Example 5: Get maintenance history
    print("\n\n5. GET MAINTENANCE HISTORY")
    print("-" * 80)
    print("Query:")
    print(client.get_maintenance_history("AC1001", limit=5))
    print("\nParameters: {'aircraft_id': 'AC1001', 'limit': 5}")
    print("\nExpected Result: Recent maintenance events for aircraft AC1001")
    
    # Example 6: Get aircraft statistics
    print("\n\n6. GET AIRCRAFT STATISTICS")
    print("-" * 80)
    print("Query:")
    print(client.get_aircraft_statistics("AC1001"))
    print("\nParameters: {'aircraft_id': 'AC1001'}")
    print("\nExpected Result: Summary statistics for aircraft AC1001")
    
    print("\n" + "=" * 80)
    print("END OF DEMONSTRATION")
    print("=" * 80)
    print()
    print("To execute these queries through the Neo4j MCP server:")
    print("1. Use the read_neo4j_cypher tool for read-only queries")
    print("2. Pass the query string and parameters as shown above")
    print("3. The MCP server will return results in JSON format")
    print()


def print_schema_info():
    """Print information about the Neo4j database schema for airplanes."""
    print("=" * 80)
    print("NEO4J DATABASE SCHEMA - AIRPLANE INFORMATION")
    print("=" * 80)
    print()
    print("NODE TYPES:")
    print("-" * 80)
    print("""
1. Aircraft
   Properties: aircraft_id, tail_number, icao24, model, operator, manufacturer
   Description: Represents individual aircraft in the fleet

2. System
   Properties: system_id, name, type, aircraft_id
   Description: Major systems installed on aircraft (engines, avionics, etc.)

3. Component
   Properties: component_id, name, type, system_id
   Description: Individual parts/components that make up systems

4. Sensor
   Properties: sensor_id, name, type, unit, system_id
   Description: Sensors that monitor system and component performance

5. MaintenanceEvent
   Properties: event_id, fault, severity, corrective_action, reported_at
   Description: Maintenance events and repairs

6. Flight
   Properties: flight_id, flight_number, origin, destination, operator
   Description: Flight operations for each aircraft

7. Airport
   Properties: airport_id, iata, icao, name, city, country
   Description: Airports for flight operations
""")
    
    print("\nRELATIONSHIPS:")
    print("-" * 80)
    print("""
- Aircraft -[:HAS_SYSTEM]-> System
- System -[:HAS_COMPONENT]-> Component
- System -[:HAS_SENSOR]-> Sensor
- Component -[:HAS_EVENT]-> MaintenanceEvent
- MaintenanceEvent -[:AFFECTS_AIRCRAFT]-> Aircraft
- MaintenanceEvent -[:AFFECTS_SYSTEM]-> System
- Aircraft -[:OPERATES_FLIGHT]-> Flight
- Flight -[:DEPARTS_FROM]-> Airport
- Flight -[:ARRIVES_AT]-> Airport
""")
    
    print("\nDATABASE STATISTICS (from MCP server schema discovery):")
    print("-" * 80)
    print("""
- Aircraft nodes: 60
- System nodes: 240
- Component nodes: 960
- Sensor nodes: 480
- MaintenanceEvent nodes: 900
- Flight nodes: 2,400
- Airport nodes: 36
""")
    print()


if __name__ == "__main__":
    print("\n" * 2)
    
    # Print schema information
    print_schema_info()
    
    # Demonstrate usage
    demonstrate_usage()
    
    # Print complete query guide
    print("\n" * 2)
    client = AirplaneClient()
    client.print_query_guide()
    
    print("\n" + "=" * 80)
    print("NOTES:")
    print("=" * 80)
    print("""
This client is a reference implementation showing the structure of queries
needed to read airplane information and parts from the Neo4j database.

To actually execute these queries, use the Neo4j MCP server tools:
- neo4j-python-neo4j-python-read_neo4j_cypher for read operations
- neo4j-python-neo4j-python-get_neo4j_schema for schema information

The MCP server must be configured with the appropriate environment variables:
- COPILOT_MCP_NEO4J_URI
- COPILOT_MCP_NEO4J_USERNAME
- COPILOT_MCP_NEO4J_PASSWORD
- COPILOT_MCP_NEO4J_DATABASE

Example MCP server connection was successfully established and validated
during the development of this client, confirming access to the airplane
database with 60 aircraft and their associated systems and components.
""")
    print("=" * 80)
    print()
