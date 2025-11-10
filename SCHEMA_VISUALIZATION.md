# Neo4j Aviation Database Schema Visualization

## Entity Relationship Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         AVIATION DATABASE SCHEMA                         │
└─────────────────────────────────────────────────────────────────────────┘

                              ┌──────────────┐
                              │   Aircraft   │
                              │  (60 nodes)  │
                              └──────┬───────┘
                                     │
                    ┌────────────────┼────────────────┐
                    │                │                │
                    ▼                ▼                ▼
         ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
         │    System    │  │    Flight    │  │  Maintenance │
         │ (240 nodes)  │  │ (2400 nodes) │  │    Event     │
         └──────┬───────┘  └──────┬───────┘  │  (900 nodes) │
                │                 │           └──────────────┘
       ┌────────┼────────┐        │
       │        │        │        │
       ▼        ▼        ▼        ▼
  ┌────────┐ ┌────────┐ ┌────────┐
  │Component│ │ Sensor │ │ Airport│
  │(960)   │ │ (480)  │ │  (36)  │
  └────┬───┘ └────────┘ └────────┘
       │
       ▼
  ┌────────────┐
  │Maintenance │
  │   Event    │
  └────────────┘
```

## Node Types and Properties

### Aircraft (60 nodes)
**Properties:**
- aircraft_id (String) - Unique identifier
- tail_number (String) - Registration number
- icao24 (String) - ICAO 24-bit address
- model (String) - Aircraft model (e.g., "B737-800", "A320-200")
- operator (String) - Operating airline
- manufacturer (String) - Aircraft manufacturer (Boeing, Airbus)

**Outgoing Relationships:**
- HAS_SYSTEM → System
- OPERATES_FLIGHT → Flight

**Incoming Relationships:**
- AFFECTS_AIRCRAFT ← MaintenanceEvent

### System (240 nodes)
**Properties:**
- system_id (String) - Unique identifier
- name (String) - System name (e.g., "CFM56-7B #1")
- type (String) - System type (Engine, Hydraulics, Avionics, etc.)
- aircraft_id (String) - Parent aircraft reference

**Outgoing Relationships:**
- HAS_COMPONENT → Component
- HAS_SENSOR → Sensor

**Incoming Relationships:**
- HAS_SYSTEM ← Aircraft
- AFFECTS_SYSTEM ← MaintenanceEvent

### Component (960 nodes)
**Properties:**
- component_id (String) - Unique identifier
- name (String) - Component name
- type (String) - Component type (Fan, Compressor, Turbine, FuelPump, etc.)
- system_id (String) - Parent system reference

**Outgoing Relationships:**
- HAS_EVENT → MaintenanceEvent

**Incoming Relationships:**
- HAS_COMPONENT ← System

### Sensor (480 nodes)
**Properties:**
- sensor_id (String) - Unique identifier
- name (String) - Sensor name
- type (String) - Sensor type
- unit (String) - Measurement unit
- system_id (String) - Parent system reference

**Incoming Relationships:**
- HAS_SENSOR ← System

### MaintenanceEvent (900 nodes)
**Properties:**
- event_id (String) - Unique identifier
- aircraft_id (String) - Aircraft reference
- component_id (String) - Component reference
- system_id (String) - System reference
- fault (String) - Fault description
- severity (String) - Severity level
- reported_at (String) - Timestamp
- corrective_action (String) - Action taken

**Outgoing Relationships:**
- AFFECTS_AIRCRAFT → Aircraft
- AFFECTS_SYSTEM → System

**Incoming Relationships:**
- HAS_EVENT ← Component

### Flight (2,400 nodes)
**Properties:**
- flight_id (String) - Unique identifier
- flight_number (String) - Flight number
- aircraft_id (String) - Aircraft reference
- operator (String) - Operating airline
- origin (String) - Origin airport code
- destination (String) - Destination airport code
- scheduled_departure (String) - Scheduled departure time
- scheduled_arrival (String) - Scheduled arrival time

**Outgoing Relationships:**
- DEPARTS_FROM → Airport
- ARRIVES_AT → Airport
- HAS_DELAY → Delay

**Incoming Relationships:**
- OPERATES_FLIGHT ← Aircraft

### Airport (36 nodes)
**Properties:**
- airport_id (String) - Unique identifier
- iata (String) - IATA code (3-letter)
- icao (String) - ICAO code (4-letter)
- name (String) - Airport name
- city (String) - City name
- country (String) - Country name
- lat (Float) - Latitude
- lon (Float) - Longitude

**Incoming Relationships:**
- DEPARTS_FROM ← Flight
- ARRIVES_AT ← Flight

### Delay (1,542 nodes)
**Properties:**
- delay_id (String) - Unique identifier
- flight_id (String) - Flight reference
- minutes (Integer) - Delay duration
- cause (String) - Delay cause

**Incoming Relationships:**
- HAS_DELAY ← Flight

### Reading (1,036,800 nodes)
**Properties:**
- reading_id (String) - Unique identifier
- sensor_id (String) - Sensor reference
- timestamp (String) - Reading timestamp
- value (Float) - Sensor value

## Relationship Types

| Relationship | Count | From | To | Description |
|---|---|---|---|---|
| HAS_SYSTEM | 1,120 | Aircraft | System | Aircraft contains systems |
| HAS_COMPONENT | 4,480 | System | Component | System contains components |
| HAS_SENSOR | 2,240 | System | Sensor | System has sensors |
| HAS_EVENT | 4,200 | Component | MaintenanceEvent | Component has maintenance events |
| AFFECTS_AIRCRAFT | 4,200 | MaintenanceEvent | Aircraft | Event affects aircraft |
| AFFECTS_SYSTEM | 4,200 | MaintenanceEvent | System | Event affects system |
| OPERATES_FLIGHT | 11,200 | Aircraft | Flight | Aircraft operates flight |
| DEPARTS_FROM | 11,200 | Flight | Airport | Flight departs from airport |
| ARRIVES_AT | 11,200 | Flight | Airport | Flight arrives at airport |
| HAS_DELAY | 7,196 | Flight | Delay | Flight has delay |

## Sample Data Hierarchy

```
Aircraft: N95040A (Boeing B737-800)
├─ System: CFM56-7B #1 (Engine)
│  ├─ Component: Fan Module (Fan)
│  ├─ Component: Compressor Stage (Compressor)
│  ├─ Component: High-Pressure Turbine (Turbine)
│  ├─ Component: Main Fuel Pump (FuelPump)
│  └─ Sensor: Temperature Sensor #1
│     └─ Reading: 2024-01-01T00:00:00Z, 850.5°C
├─ System: Hydraulic System A (Hydraulics)
│  ├─ Component: Hydraulic Pump (Pump)
│  ├─ Component: Reservoir (Tank)
│  └─ Sensor: Pressure Sensor
├─ Flight: FL1234 (ExampleAir)
│  ├─ From: JFK (New York)
│  ├─ To: LAX (Los Angeles)
│  └─ Delay: 15 minutes (Weather)
└─ MaintenanceEvent: EVT001
   ├─ Fault: "Low oil pressure"
   ├─ Severity: "Medium"
   └─ Action: "Oil system inspection and refill"
```

## Query Patterns

### Pattern 1: Aircraft → Systems → Components
```cypher
MATCH (a:Aircraft)-[:HAS_SYSTEM]->(s:System)-[:HAS_COMPONENT]->(c:Component)
WHERE a.tail_number = 'N95040A'
RETURN a, s, c
```

### Pattern 2: Aircraft → Flights → Airports
```cypher
MATCH (a:Aircraft)-[:OPERATES_FLIGHT]->(f:Flight)
MATCH (f)-[:DEPARTS_FROM]->(origin:Airport)
MATCH (f)-[:ARRIVES_AT]->(dest:Airport)
RETURN a.tail_number, f.flight_number, origin.iata, dest.iata
```

### Pattern 3: Component → Maintenance Events
```cypher
MATCH (c:Component)-[:HAS_EVENT]->(m:MaintenanceEvent)
WHERE c.type = 'Turbine'
RETURN c.name, m.fault, m.severity, m.corrective_action
```

### Pattern 4: System → Sensors → Readings
```cypher
MATCH (s:System)-[:HAS_SENSOR]->(sensor:Sensor)
OPTIONAL MATCH (sensor)<-[:HAS_READING]-(r:Reading)
WHERE s.type = 'Engine'
RETURN s.name, sensor.name, count(r) AS reading_count
```

## Database Statistics

- **Total Nodes**: ~1,042,000
- **Total Relationships**: ~55,000
- **Average Relationships per Node**: ~53
- **Deepest Path**: Aircraft → System → Component → MaintenanceEvent (3 hops)
- **Most Connected Node Type**: Flight (4 relationship types)
- **Largest Node Type**: Reading (1,036,800 nodes)

## Use Cases

1. **Fleet Management**: Track all aircraft, their systems, and components
2. **Maintenance Planning**: Monitor maintenance events and component health
3. **Flight Operations**: Manage flight schedules, routes, and delays
4. **Sensor Analytics**: Analyze sensor readings for predictive maintenance
5. **Parts Inventory**: Track components across the entire fleet
6. **Compliance**: Maintain maintenance records for regulatory requirements
