#!/usr/bin/env python3
"""
Simple Example: Using Neo4j Airplane Client

This script demonstrates the most common use cases for querying
airplane information and parts from the Neo4j database.

Before running, update the connection parameters below.
"""

import os
from neo4j_airplane_client import Neo4jAirplaneClient


def simple_example():
    """Simple example showing common queries"""
    
    # Connection parameters - UPDATE THESE
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    username = os.getenv("NEO4J_USERNAME", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "your-password-here")
    database = os.getenv("NEO4J_DATABASE", "neo4j")
    
    print("Connecting to Neo4j database...")
    print(f"URI: {uri}")
    print(f"Database: {database}")
    print()
    
    # Use context manager for automatic cleanup
    with Neo4jAirplaneClient(uri, username, password, database) as client:
        
        # 1. Get a count of all aircraft
        print("=" * 60)
        print("All Aircraft in Database")
        print("=" * 60)
        all_aircraft = client.list_all_aircraft()
        print(f"Total aircraft: {len(all_aircraft)}\n")
        
        # Show first few
        for aircraft in all_aircraft[:10]:
            print(f"  {aircraft.tail_number:12} | {aircraft.manufacturer:10} | {aircraft.model:15} | {aircraft.operator}")
        
        if len(all_aircraft) > 10:
            print(f"  ... and {len(all_aircraft) - 10} more")
        print()
        
        # 2. Get details for a specific aircraft
        print("=" * 60)
        print("Detailed View: Single Aircraft")
        print("=" * 60)
        if all_aircraft:
            first_aircraft = all_aircraft[0]
            print(f"Aircraft: {first_aircraft.tail_number}")
            print(f"  Model: {first_aircraft.manufacturer} {first_aircraft.model}")
            print(f"  Operator: {first_aircraft.operator}")
            print(f"  ICAO24: {first_aircraft.icao24}")
            print()
            
            # 3. Get all systems for this aircraft
            print(f"Systems on {first_aircraft.tail_number}:")
            systems = client.get_aircraft_systems(first_aircraft.aircraft_id)
            for i, system in enumerate(systems, 1):
                print(f"  {i}. {system.name} ({system.type})")
            print()
            
            # 4. Get components for the first system
            if systems:
                first_system = systems[0]
                print(f"Components in '{first_system.name}':")
                components = client.get_system_components(first_system.system_id)
                for i, component in enumerate(components, 1):
                    print(f"  {i}. {component.name} - Type: {component.type}")
                print()
        
        # 5. Group aircraft by manufacturer
        print("=" * 60)
        print("Aircraft by Manufacturer")
        print("=" * 60)
        manufacturers = {}
        for aircraft in all_aircraft:
            if aircraft.manufacturer not in manufacturers:
                manufacturers[aircraft.manufacturer] = []
            manufacturers[aircraft.manufacturer].append(aircraft)
        
        for manufacturer, aircraft_list in sorted(manufacturers.items()):
            print(f"{manufacturer}: {len(aircraft_list)} aircraft")
            for aircraft in aircraft_list[:3]:  # Show up to 3
                print(f"  - {aircraft.tail_number} ({aircraft.model})")
            if len(aircraft_list) > 3:
                print(f"  ... and {len(aircraft_list) - 3} more")
        print()
        
        # 6. Search for specific component types
        print("=" * 60)
        print("Component Search: Find all 'Turbine' components")
        print("=" * 60)
        turbines = client.search_components_by_type("Turbine")
        print(f"Found {len(turbines)} turbine components\n")
        
        # Group by aircraft
        turbines_by_aircraft = {}
        for turbine in turbines:
            tail = turbine['aircraft_tail']
            if tail not in turbines_by_aircraft:
                turbines_by_aircraft[tail] = []
            turbines_by_aircraft[tail].append(turbine)
        
        for tail, components in sorted(turbines_by_aircraft.items())[:5]:
            print(f"{tail}:")
            for comp in components:
                print(f"  - {comp['system_name']}: {comp['component_name']}")
        
        if len(turbines_by_aircraft) > 5:
            print(f"... and {len(turbines_by_aircraft) - 5} more aircraft")
        print()
        
        # 7. Complete hierarchy for one aircraft
        print("=" * 60)
        print("Complete Aircraft Hierarchy (First Aircraft)")
        print("=" * 60)
        if all_aircraft:
            aircraft_with_parts = client.get_aircraft_with_all_parts(all_aircraft[0].aircraft_id)
            if aircraft_with_parts:
                print(f"Aircraft: {aircraft_with_parts.aircraft.tail_number}")
                print(f"Model: {aircraft_with_parts.aircraft.manufacturer} {aircraft_with_parts.aircraft.model}")
                print(f"Total Systems: {len(aircraft_with_parts.systems)}\n")
                
                for system in aircraft_with_parts.systems[:3]:  # Show first 3 systems
                    print(f"  ├─ {system['name']} ({system['type']})")
                    print(f"  │  └─ {len(system['components'])} components")
                    for comp in system['components'][:5]:  # Show first 5 components
                        print(f"  │     • {comp['name']} ({comp['type']})")
                    if len(system['components']) > 5:
                        print(f"  │     • ... and {len(system['components']) - 5} more")
                    print()
                
                if len(aircraft_with_parts.systems) > 3:
                    print(f"  ... and {len(aircraft_with_parts.systems) - 3} more systems")
        
        print("\n" + "=" * 60)
        print("Example Complete!")
        print("=" * 60)


if __name__ == "__main__":
    try:
        simple_example()
    except Exception as e:
        print(f"\nError: {e}")
        print("\nPlease ensure:")
        print("1. Neo4j database is running")
        print("2. Connection parameters are correct")
        print("3. Database contains the aviation schema")
        print("\nSet environment variables or update connection parameters in the script:")
        print("  NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, NEO4J_DATABASE")
