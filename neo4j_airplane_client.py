"""
Neo4j Airplane Information Client

This Python client demonstrates how to read airplane information and parts
from a Neo4j database. It uses the neo4j Python driver to connect and query
the aviation data model.

The database schema includes:
- Aircraft: Basic aircraft information (tail number, model, manufacturer, operator)
- Systems: Aircraft systems (engines, hydraulics, avionics, etc.)
- Components: Parts that make up each system
- Sensors: Monitoring sensors attached to systems
- MaintenanceEvent: Maintenance history for aircraft and components
- Flight: Flight operations data
- Airport: Airport information
"""

from neo4j import GraphDatabase
import json
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict


@dataclass
class Aircraft:
    """Represents an aircraft in the database"""
    aircraft_id: str
    tail_number: str
    icao24: str
    model: str
    operator: str
    manufacturer: str


@dataclass
class System:
    """Represents a system on an aircraft"""
    system_id: str
    name: str
    type: str
    aircraft_id: str


@dataclass
class Component:
    """Represents a component/part within a system"""
    component_id: str
    name: str
    type: str
    system_id: str


@dataclass
class AircraftWithParts:
    """Complete aircraft information including all systems and components"""
    aircraft: Aircraft
    systems: List[Dict]  # List of systems with their components


class Neo4jAirplaneClient:
    """
    Client for querying airplane information and parts from Neo4j database.
    
    This client provides methods to:
    - List all aircraft
    - Get detailed information about a specific aircraft
    - Query aircraft parts and components
    - Retrieve system information
    """
    
    def __init__(self, uri: str, username: str, password: str, database: str = "neo4j"):
        """
        Initialize the Neo4j client.
        
        Args:
            uri: Neo4j connection URI (e.g., 'bolt://localhost:7687')
            username: Database username
            password: Database password
            database: Database name (default: 'neo4j')
        """
        self.driver = GraphDatabase.driver(uri, auth=(username, password))
        self.database = database
    
    def close(self):
        """Close the database connection"""
        self.driver.close()
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
    
    def list_all_aircraft(self) -> List[Aircraft]:
        """
        Retrieve all aircraft from the database.
        
        Returns:
            List of Aircraft objects
        """
        query = """
        MATCH (aircraft:Aircraft)
        RETURN aircraft
        ORDER BY aircraft.tail_number
        """
        
        with self.driver.session(database=self.database) as session:
            result = session.run(query)
            aircraft_list = []
            for record in result:
                aircraft_data = record["aircraft"]
                aircraft_list.append(Aircraft(
                    aircraft_id=aircraft_data.get("aircraft_id", ""),
                    tail_number=aircraft_data.get("tail_number", ""),
                    icao24=aircraft_data.get("icao24", ""),
                    model=aircraft_data.get("model", ""),
                    operator=aircraft_data.get("operator", ""),
                    manufacturer=aircraft_data.get("manufacturer", "")
                ))
            return aircraft_list
    
    def get_aircraft_by_tail_number(self, tail_number: str) -> Optional[Aircraft]:
        """
        Get aircraft information by tail number.
        
        Args:
            tail_number: Aircraft tail number (e.g., 'N95040A')
        
        Returns:
            Aircraft object if found, None otherwise
        """
        query = """
        MATCH (aircraft:Aircraft {tail_number: $tail_number})
        RETURN aircraft
        """
        
        with self.driver.session(database=self.database) as session:
            result = session.run(query, tail_number=tail_number)
            record = result.single()
            if record:
                aircraft_data = record["aircraft"]
                return Aircraft(
                    aircraft_id=aircraft_data.get("aircraft_id", ""),
                    tail_number=aircraft_data.get("tail_number", ""),
                    icao24=aircraft_data.get("icao24", ""),
                    model=aircraft_data.get("model", ""),
                    operator=aircraft_data.get("operator", ""),
                    manufacturer=aircraft_data.get("manufacturer", "")
                )
            return None
    
    def get_aircraft_systems(self, aircraft_id: str) -> List[System]:
        """
        Get all systems for a specific aircraft.
        
        Args:
            aircraft_id: Aircraft ID (e.g., 'AC1001')
        
        Returns:
            List of System objects
        """
        query = """
        MATCH (aircraft:Aircraft {aircraft_id: $aircraft_id})-[:HAS_SYSTEM]->(system:System)
        RETURN system
        ORDER BY system.name
        """
        
        with self.driver.session(database=self.database) as session:
            result = session.run(query, aircraft_id=aircraft_id)
            systems = []
            for record in result:
                system_data = record["system"]
                systems.append(System(
                    system_id=system_data.get("system_id", ""),
                    name=system_data.get("name", ""),
                    type=system_data.get("type", ""),
                    aircraft_id=system_data.get("aircraft_id", "")
                ))
            return systems
    
    def get_system_components(self, system_id: str) -> List[Component]:
        """
        Get all components for a specific system.
        
        Args:
            system_id: System ID
        
        Returns:
            List of Component objects
        """
        query = """
        MATCH (system:System {system_id: $system_id})-[:HAS_COMPONENT]->(component:Component)
        RETURN component
        ORDER BY component.name
        """
        
        with self.driver.session(database=self.database) as session:
            result = session.run(query, system_id=system_id)
            components = []
            for record in result:
                component_data = record["component"]
                components.append(Component(
                    component_id=component_data.get("component_id", ""),
                    name=component_data.get("name", ""),
                    type=component_data.get("type", ""),
                    system_id=component_data.get("system_id", "")
                ))
            return components
    
    def get_aircraft_with_all_parts(self, aircraft_id: str) -> Optional[AircraftWithParts]:
        """
        Get complete aircraft information including all systems and their components.
        
        Args:
            aircraft_id: Aircraft ID (e.g., 'AC1001')
        
        Returns:
            AircraftWithParts object with complete hierarchy
        """
        query = """
        MATCH (aircraft:Aircraft {aircraft_id: $aircraft_id})
        OPTIONAL MATCH (aircraft)-[:HAS_SYSTEM]->(system:System)
        OPTIONAL MATCH (system)-[:HAS_COMPONENT]->(component:Component)
        RETURN aircraft,
               collect(DISTINCT system) AS systems,
               collect(DISTINCT {
                   system_id: system.system_id,
                   component: component
               }) AS components
        """
        
        with self.driver.session(database=self.database) as session:
            result = session.run(query, aircraft_id=aircraft_id)
            record = result.single()
            
            if not record:
                return None
            
            # Parse aircraft
            aircraft_data = record["aircraft"]
            aircraft = Aircraft(
                aircraft_id=aircraft_data.get("aircraft_id", ""),
                tail_number=aircraft_data.get("tail_number", ""),
                icao24=aircraft_data.get("icao24", ""),
                model=aircraft_data.get("model", ""),
                operator=aircraft_data.get("operator", ""),
                manufacturer=aircraft_data.get("manufacturer", "")
            )
            
            # Parse systems and components
            systems_dict = {}
            for system_node in record["systems"]:
                if system_node:
                    system_id = system_node.get("system_id", "")
                    systems_dict[system_id] = {
                        "system_id": system_id,
                        "name": system_node.get("name", ""),
                        "type": system_node.get("type", ""),
                        "aircraft_id": system_node.get("aircraft_id", ""),
                        "components": []
                    }
            
            # Add components to their systems
            for comp_data in record["components"]:
                if comp_data["component"]:
                    system_id = comp_data["system_id"]
                    if system_id in systems_dict:
                        component = comp_data["component"]
                        systems_dict[system_id]["components"].append({
                            "component_id": component.get("component_id", ""),
                            "name": component.get("name", ""),
                            "type": component.get("type", ""),
                            "system_id": component.get("system_id", "")
                        })
            
            return AircraftWithParts(
                aircraft=aircraft,
                systems=list(systems_dict.values())
            )
    
    def get_aircraft_by_manufacturer(self, manufacturer: str) -> List[Aircraft]:
        """
        Get all aircraft from a specific manufacturer.
        
        Args:
            manufacturer: Manufacturer name (e.g., 'Boeing', 'Airbus')
        
        Returns:
            List of Aircraft objects
        """
        query = """
        MATCH (aircraft:Aircraft {manufacturer: $manufacturer})
        RETURN aircraft
        ORDER BY aircraft.model, aircraft.tail_number
        """
        
        with self.driver.session(database=self.database) as session:
            result = session.run(query, manufacturer=manufacturer)
            aircraft_list = []
            for record in result:
                aircraft_data = record["aircraft"]
                aircraft_list.append(Aircraft(
                    aircraft_id=aircraft_data.get("aircraft_id", ""),
                    tail_number=aircraft_data.get("tail_number", ""),
                    icao24=aircraft_data.get("icao24", ""),
                    model=aircraft_data.get("model", ""),
                    operator=aircraft_data.get("operator", ""),
                    manufacturer=aircraft_data.get("manufacturer", "")
                ))
            return aircraft_list
    
    def search_components_by_type(self, component_type: str) -> List[Dict]:
        """
        Search for components by type across all aircraft.
        
        Args:
            component_type: Component type (e.g., 'Fan', 'Turbine', 'Compressor')
        
        Returns:
            List of dictionaries with component and associated aircraft info
        """
        query = """
        MATCH (aircraft:Aircraft)-[:HAS_SYSTEM]->(system:System)-[:HAS_COMPONENT]->(component:Component {type: $component_type})
        RETURN aircraft.tail_number AS aircraft_tail,
               aircraft.model AS aircraft_model,
               system.name AS system_name,
               component.name AS component_name,
               component.component_id AS component_id
        ORDER BY aircraft.tail_number, system.name
        LIMIT 100
        """
        
        with self.driver.session(database=self.database) as session:
            result = session.run(query, component_type=component_type)
            components = []
            for record in result:
                components.append({
                    "aircraft_tail": record["aircraft_tail"],
                    "aircraft_model": record["aircraft_model"],
                    "system_name": record["system_name"],
                    "component_name": record["component_name"],
                    "component_id": record["component_id"]
                })
            return components


def main():
    """
    Example usage of the Neo4jAirplaneClient.
    
    Note: Update the connection parameters before running.
    """
    # Connection parameters - UPDATE THESE VALUES
    NEO4J_URI = "bolt://localhost:7687"
    NEO4J_USERNAME = "neo4j"
    NEO4J_PASSWORD = "your-password-here"
    NEO4J_DATABASE = "neo4j"
    
    # Use context manager for automatic connection cleanup
    with Neo4jAirplaneClient(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, NEO4J_DATABASE) as client:
        
        # Example 1: List all aircraft
        print("=" * 80)
        print("Example 1: List all aircraft")
        print("=" * 80)
        aircraft_list = client.list_all_aircraft()
        print(f"Found {len(aircraft_list)} aircraft:")
        for aircraft in aircraft_list[:5]:  # Show first 5
            print(f"  - {aircraft.tail_number}: {aircraft.manufacturer} {aircraft.model} (Operator: {aircraft.operator})")
        print()
        
        # Example 2: Get specific aircraft by tail number
        print("=" * 80)
        print("Example 2: Get aircraft by tail number")
        print("=" * 80)
        aircraft = client.get_aircraft_by_tail_number("N95040A")
        if aircraft:
            print(f"Found aircraft: {json.dumps(asdict(aircraft), indent=2)}")
        print()
        
        # Example 3: Get aircraft systems
        print("=" * 80)
        print("Example 3: Get aircraft systems")
        print("=" * 80)
        if aircraft:
            systems = client.get_aircraft_systems(aircraft.aircraft_id)
            print(f"Aircraft {aircraft.tail_number} has {len(systems)} systems:")
            for system in systems[:5]:  # Show first 5
                print(f"  - {system.name} ({system.type})")
        print()
        
        # Example 4: Get system components
        print("=" * 80)
        print("Example 4: Get system components")
        print("=" * 80)
        if systems:
            first_system = systems[0]
            components = client.get_system_components(first_system.system_id)
            print(f"System '{first_system.name}' has {len(components)} components:")
            for component in components:
                print(f"  - {component.name} ({component.type})")
        print()
        
        # Example 5: Get complete aircraft hierarchy
        print("=" * 80)
        print("Example 5: Get complete aircraft with all parts")
        print("=" * 80)
        if aircraft:
            aircraft_with_parts = client.get_aircraft_with_all_parts(aircraft.aircraft_id)
            if aircraft_with_parts:
                print(f"Aircraft: {aircraft_with_parts.aircraft.tail_number}")
                print(f"Systems: {len(aircraft_with_parts.systems)}")
                for system in aircraft_with_parts.systems[:2]:  # Show first 2 systems
                    print(f"\n  System: {system['name']} ({system['type']})")
                    print(f"  Components: {len(system['components'])}")
                    for component in system['components'][:3]:  # Show first 3 components
                        print(f"    - {component['name']} ({component['type']})")
        print()
        
        # Example 6: Search by manufacturer
        print("=" * 80)
        print("Example 6: Get Boeing aircraft")
        print("=" * 80)
        boeing_aircraft = client.get_aircraft_by_manufacturer("Boeing")
        print(f"Found {len(boeing_aircraft)} Boeing aircraft:")
        for aircraft in boeing_aircraft[:5]:  # Show first 5
            print(f"  - {aircraft.tail_number}: {aircraft.model}")
        print()
        
        # Example 7: Search components by type
        print("=" * 80)
        print("Example 7: Search for Fan components")
        print("=" * 80)
        fan_components = client.search_components_by_type("Fan")
        print(f"Found {len(fan_components)} Fan components:")
        for comp in fan_components[:5]:  # Show first 5
            print(f"  - {comp['aircraft_tail']} ({comp['aircraft_model']}): {comp['system_name']} -> {comp['component_name']}")
        print()


if __name__ == "__main__":
    main()
