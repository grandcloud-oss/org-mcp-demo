#!/usr/bin/env python3
"""
Airplane Information and Parts Client for Neo4j Database

This client demonstrates how to read airplane information and parts data
from a Neo4j database using the MCP (Model Context Protocol) server.

The database contains aircraft data with the following structure:
- Aircraft nodes: Information about airplanes (tail number, model, manufacturer, operator)
- System nodes: Aircraft systems (engines, hydraulics, etc.)
- Component nodes: Parts/components within each system

Usage:
    python airplane_client.py

Requirements:
    - mcp-neo4j-cypher (installed via pip)
    - Neo4j database connection configured via MCP server

Note: This client is designed to work with the GitHub Copilot MCP integration
and reads data through the neo4j-python MCP server tools.
"""

import json
from typing import List, Dict, Any


class AirplaneClient:
    """
    Client for reading airplane and parts information from Neo4j database.
    
    This client provides methods to query aircraft, systems, and components
    from the Neo4j graph database through the MCP server interface.
    """
    
    def __init__(self):
        """Initialize the airplane client."""
        self.schema = None
    
    def get_database_schema(self) -> Dict[str, Any]:
        """
        Get the Neo4j database schema.
        
        Returns:
            Dictionary containing node types, relationships, and properties
        
        Note: This method demonstrates the expected structure. In practice,
        this would be called via the MCP server's get_neo4j_schema tool.
        """
        # This is a placeholder - in actual use, this would be called via MCP
        # Example: neo4j-python-neo4j-python-get_neo4j_schema
        return {
            "message": "Use neo4j-python-neo4j-python-get_neo4j_schema MCP tool to get schema",
            "expected_nodes": ["Aircraft", "System", "Component", "MaintenanceEvent", 
                             "Flight", "Airport", "Sensor", "Reading", "Delay"],
            "key_relationships": {
                "Aircraft->System": "HAS_SYSTEM",
                "System->Component": "HAS_COMPONENT",
                "Aircraft->Flight": "OPERATES_FLIGHT"
            }
        }
    
    def get_all_aircraft(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Query to retrieve all aircraft in the database.
        
        Args:
            limit: Maximum number of aircraft to return
            
        Returns:
            List of aircraft dictionaries with properties
            
        Cypher Query:
            MATCH (a:Aircraft)
            RETURN a.aircraft_id, a.tail_number, a.model, 
                   a.manufacturer, a.operator, a.icao24
            LIMIT {limit}
        """
        return {
            "query": """
                MATCH (a:Aircraft)
                RETURN a.aircraft_id as aircraft_id, 
                       a.tail_number as tail_number, 
                       a.model as model,
                       a.manufacturer as manufacturer, 
                       a.operator as operator, 
                       a.icao24 as icao24
                LIMIT $limit
            """,
            "params": {"limit": limit},
            "description": "Retrieves basic information about all aircraft"
        }
    
    def get_aircraft_with_systems(self, aircraft_id: str = None, limit: int = 20) -> Dict[str, Any]:
        """
        Query to retrieve aircraft along with their systems.
        
        Args:
            aircraft_id: Specific aircraft ID to query (optional)
            limit: Maximum number of results to return
            
        Returns:
            Dictionary containing the query and parameters
            
        Cypher Query:
            MATCH (a:Aircraft)-[:HAS_SYSTEM]->(s:System)
            WHERE a.aircraft_id = {aircraft_id} OR {aircraft_id} IS NULL
            RETURN a.aircraft_id, a.tail_number, a.model, a.manufacturer,
                   s.system_id, s.name, s.type
            LIMIT {limit}
        """
        if aircraft_id:
            return {
                "query": """
                    MATCH (a:Aircraft)-[:HAS_SYSTEM]->(s:System)
                    WHERE a.aircraft_id = $aircraft_id
                    RETURN a.aircraft_id as aircraft_id, 
                           a.tail_number as tail_number, 
                           a.model as model,
                           a.manufacturer as manufacturer,
                           a.operator as operator,
                           s.system_id as system_id, 
                           s.name as system_name, 
                           s.type as system_type
                    LIMIT $limit
                """,
                "params": {"aircraft_id": aircraft_id, "limit": limit},
                "description": f"Retrieves aircraft {aircraft_id} with all its systems"
            }
        else:
            return {
                "query": """
                    MATCH (a:Aircraft)-[:HAS_SYSTEM]->(s:System)
                    RETURN a.aircraft_id as aircraft_id, 
                           a.tail_number as tail_number, 
                           a.model as model,
                           a.manufacturer as manufacturer,
                           a.operator as operator,
                           s.system_id as system_id, 
                           s.name as system_name, 
                           s.type as system_type
                    LIMIT $limit
                """,
                "params": {"limit": limit},
                "description": "Retrieves all aircraft with their systems"
            }
    
    def get_aircraft_parts(self, aircraft_id: str = None, system_type: str = None, 
                          limit: int = 50) -> Dict[str, Any]:
        """
        Query to retrieve aircraft parts/components.
        
        Args:
            aircraft_id: Specific aircraft ID to query (optional)
            system_type: Filter by system type (e.g., 'Engine', 'Hydraulic') (optional)
            limit: Maximum number of results to return
            
        Returns:
            Dictionary containing the query and parameters
            
        Cypher Query:
            MATCH (a:Aircraft)-[:HAS_SYSTEM]->(s:System)-[:HAS_COMPONENT]->(c:Component)
            WHERE (a.aircraft_id = {aircraft_id} OR {aircraft_id} IS NULL)
              AND (s.type = {system_type} OR {system_type} IS NULL)
            RETURN a.aircraft_id, a.tail_number, a.model,
                   s.system_id, s.name, s.type,
                   c.component_id, c.name, c.type
            LIMIT {limit}
        """
        conditions = []
        params = {"limit": limit}
        
        if aircraft_id:
            conditions.append("a.aircraft_id = $aircraft_id")
            params["aircraft_id"] = aircraft_id
        
        if system_type:
            conditions.append("s.type = $system_type")
            params["system_type"] = system_type
        
        where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""
        
        return {
            "query": f"""
                MATCH (a:Aircraft)-[:HAS_SYSTEM]->(s:System)-[:HAS_COMPONENT]->(c:Component)
                {where_clause}
                RETURN a.aircraft_id as aircraft_id, 
                       a.tail_number as tail_number, 
                       a.model as model,
                       a.manufacturer as manufacturer,
                       s.system_id as system_id, 
                       s.name as system_name, 
                       s.type as system_type,
                       c.component_id as component_id, 
                       c.name as component_name, 
                       c.type as component_type
                LIMIT $limit
            """,
            "params": params,
            "description": f"Retrieves aircraft parts/components" + 
                          (f" for aircraft {aircraft_id}" if aircraft_id else "") +
                          (f" in {system_type} systems" if system_type else "")
        }
    
    def get_component_details(self, component_id: str) -> Dict[str, Any]:
        """
        Query to retrieve detailed information about a specific component.
        
        Args:
            component_id: The unique component identifier
            
        Returns:
            Dictionary containing the query and parameters
            
        Cypher Query:
            MATCH (c:Component {component_id: {component_id}})
            OPTIONAL MATCH (c)<-[:HAS_COMPONENT]-(s:System)<-[:HAS_SYSTEM]-(a:Aircraft)
            OPTIONAL MATCH (c)-[:HAS_EVENT]->(m:MaintenanceEvent)
            RETURN c.component_id, c.name, c.type,
                   s.system_id, s.name, s.type,
                   a.aircraft_id, a.tail_number,
                   collect(m.event_id) as maintenance_events
        """
        return {
            "query": """
                MATCH (c:Component {component_id: $component_id})
                OPTIONAL MATCH (c)<-[:HAS_COMPONENT]-(s:System)<-[:HAS_SYSTEM]-(a:Aircraft)
                OPTIONAL MATCH (c)-[:HAS_EVENT]->(m:MaintenanceEvent)
                RETURN c.component_id as component_id, 
                       c.name as component_name, 
                       c.type as component_type,
                       s.system_id as system_id, 
                       s.name as system_name, 
                       s.type as system_type,
                       a.aircraft_id as aircraft_id, 
                       a.tail_number as tail_number,
                       collect(m.event_id) as maintenance_events
            """,
            "params": {"component_id": component_id},
            "description": f"Retrieves detailed information about component {component_id}"
        }
    
    def get_aircraft_by_manufacturer(self, manufacturer: str, limit: int = 10) -> Dict[str, Any]:
        """
        Query to retrieve aircraft by manufacturer.
        
        Args:
            manufacturer: Aircraft manufacturer (e.g., 'Boeing', 'Airbus')
            limit: Maximum number of results to return
            
        Returns:
            Dictionary containing the query and parameters
            
        Cypher Query:
            MATCH (a:Aircraft {manufacturer: {manufacturer}})
            RETURN a.aircraft_id, a.tail_number, a.model, a.operator
            LIMIT {limit}
        """
        return {
            "query": """
                MATCH (a:Aircraft {manufacturer: $manufacturer})
                RETURN a.aircraft_id as aircraft_id, 
                       a.tail_number as tail_number, 
                       a.model as model, 
                       a.operator as operator,
                       a.icao24 as icao24
                LIMIT $limit
            """,
            "params": {"manufacturer": manufacturer, "limit": limit},
            "description": f"Retrieves aircraft manufactured by {manufacturer}"
        }
    
    def get_system_components_count(self) -> Dict[str, Any]:
        """
        Query to get a count of components per system type.
        
        Returns:
            Dictionary containing the query
            
        Cypher Query:
            MATCH (s:System)-[:HAS_COMPONENT]->(c:Component)
            RETURN s.type as system_type, count(c) as component_count
            ORDER BY component_count DESC
        """
        return {
            "query": """
                MATCH (s:System)-[:HAS_COMPONENT]->(c:Component)
                RETURN s.type as system_type, 
                       count(c) as component_count
                ORDER BY component_count DESC
            """,
            "params": {},
            "description": "Returns count of components per system type"
        }
    
    def print_query_info(self, query_dict: Dict[str, Any]) -> None:
        """
        Print formatted query information.
        
        Args:
            query_dict: Dictionary containing query, params, and description
        """
        print("\n" + "="*70)
        print(f"Description: {query_dict['description']}")
        print("="*70)
        print("\nCypher Query:")
        print(query_dict['query'].strip())
        if query_dict['params']:
            print(f"\nParameters: {json.dumps(query_dict['params'], indent=2)}")
        print("="*70 + "\n")


def main():
    """
    Main function demonstrating the airplane client usage.
    
    This function shows example queries that can be executed against
    the Neo4j database using the MCP server.
    """
    print("="*70)
    print("Airplane Information and Parts Client - Neo4j MCP Demo")
    print("="*70)
    
    client = AirplaneClient()
    
    print("\n" + "="*70)
    print("DATABASE SCHEMA INFORMATION")
    print("="*70)
    schema_info = client.get_database_schema()
    print(json.dumps(schema_info, indent=2))
    
    print("\n" + "="*70)
    print("EXAMPLE QUERIES")
    print("="*70)
    
    # Example 1: Get all aircraft
    print("\n1. Get All Aircraft (Limited to 10)")
    query1 = client.get_all_aircraft(limit=10)
    client.print_query_info(query1)
    print("To execute via MCP: neo4j-python-neo4j-python-read_neo4j_cypher")
    
    # Example 2: Get aircraft with systems
    print("\n2. Get Aircraft with Systems")
    query2 = client.get_aircraft_with_systems(limit=20)
    client.print_query_info(query2)
    print("To execute via MCP: neo4j-python-neo4j-python-read_neo4j_cypher")
    
    # Example 3: Get specific aircraft with systems
    print("\n3. Get Specific Aircraft with Systems (AC1001)")
    query3 = client.get_aircraft_with_systems(aircraft_id="AC1001", limit=20)
    client.print_query_info(query3)
    print("To execute via MCP: neo4j-python-neo4j-python-read_neo4j_cypher")
    
    # Example 4: Get all aircraft parts
    print("\n4. Get All Aircraft Parts/Components")
    query4 = client.get_aircraft_parts(limit=50)
    client.print_query_info(query4)
    print("To execute via MCP: neo4j-python-neo4j-python-read_neo4j_cypher")
    
    # Example 5: Get parts for specific aircraft
    print("\n5. Get Parts for Specific Aircraft (AC1001)")
    query5 = client.get_aircraft_parts(aircraft_id="AC1001", limit=50)
    client.print_query_info(query5)
    print("To execute via MCP: neo4j-python-neo4j-python-read_neo4j_cypher")
    
    # Example 6: Get engine parts only
    print("\n6. Get Engine Parts Only")
    query6 = client.get_aircraft_parts(system_type="Engine", limit=50)
    client.print_query_info(query6)
    print("To execute via MCP: neo4j-python-neo4j-python-read_neo4j_cypher")
    
    # Example 7: Get component details
    print("\n7. Get Component Details (AC1001-S01-C01)")
    query7 = client.get_component_details(component_id="AC1001-S01-C01")
    client.print_query_info(query7)
    print("To execute via MCP: neo4j-python-neo4j-python-read_neo4j_cypher")
    
    # Example 8: Get Boeing aircraft
    print("\n8. Get Boeing Aircraft")
    query8 = client.get_aircraft_by_manufacturer(manufacturer="Boeing", limit=10)
    client.print_query_info(query8)
    print("To execute via MCP: neo4j-python-neo4j-python-read_neo4j_cypher")
    
    # Example 9: Get component counts by system type
    print("\n9. Get Component Counts by System Type")
    query9 = client.get_system_components_count()
    client.print_query_info(query9)
    print("To execute via MCP: neo4j-python-neo4j-python-read_neo4j_cypher")
    
    print("\n" + "="*70)
    print("USAGE NOTES")
    print("="*70)
    print("""
This client demonstrates queries for reading airplane and parts data.
In a GitHub Copilot environment with MCP server integration:

1. The queries shown above can be executed using the MCP tools:
   - neo4j-python-neo4j-python-read_neo4j_cypher
   - neo4j-python-neo4j-python-write_neo4j_cypher (for writes)
   - neo4j-python-neo4j-python-get_neo4j_schema

2. To execute a query, use the tool with the query and params from above.

3. Example MCP tool invocation structure:
   {
     "query": "<cypher query from above>",
     "params": {<parameters from above>}
   }

4. The database contains:
   - Aircraft nodes: 60 airplanes with details
   - System nodes: 240 aircraft systems  
   - Component nodes: 960 parts/components
   - Plus maintenance events, flights, sensors, etc.
    """)
    
    print("="*70)


if __name__ == "__main__":
    main()
