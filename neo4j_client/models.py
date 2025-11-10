"""Pydantic models for airplane entities in Neo4j."""

from typing import Optional
from pydantic import BaseModel, Field


class Aircraft(BaseModel):
    """Represents an aircraft node in the database.
    
    Attributes:
        aircraft_id: Unique identifier for the aircraft
        tail_number: Aircraft registration/tail number
        icao24: ICAO 24-bit address
        model: Aircraft model (e.g., B737-800, A320-200)
        operator: Operating airline/company
        manufacturer: Aircraft manufacturer (e.g., Boeing, Airbus)
    """
    aircraft_id: str
    tail_number: str
    icao24: str
    model: str
    operator: str
    manufacturer: str


class Airport(BaseModel):
    """Represents an airport node in the database.
    
    Attributes:
        airport_id: Unique identifier for the airport
        iata: IATA airport code (3 letters)
        icao: ICAO airport code (4 letters)
        name: Full airport name
        city: City where airport is located
        country: Country where airport is located
        lat: Latitude coordinate
        lon: Longitude coordinate
    """
    airport_id: str
    iata: str
    icao: str
    name: str
    city: str
    country: str
    lat: float
    lon: float


class Flight(BaseModel):
    """Represents a flight node in the database.
    
    Attributes:
        flight_id: Unique identifier for the flight
        flight_number: Flight number (e.g., EX370)
        aircraft_id: ID of aircraft operating this flight
        operator: Operating airline
        origin: Origin airport IATA code
        destination: Destination airport IATA code
        scheduled_departure: Scheduled departure time (ISO format)
        scheduled_arrival: Scheduled arrival time (ISO format)
    """
    flight_id: str
    flight_number: str
    aircraft_id: str
    operator: str
    origin: str
    destination: str
    scheduled_departure: str
    scheduled_arrival: str


class System(BaseModel):
    """Represents an aircraft system node in the database.
    
    Attributes:
        system_id: Unique identifier for the system
        aircraft_id: ID of aircraft this system belongs to
        name: System name (e.g., CFM56-7B #1)
        type: System type (e.g., Engine, Hydraulics, Avionics)
    """
    system_id: str
    aircraft_id: str
    name: str
    type: str


class Component(BaseModel):
    """Represents a system component node in the database.
    
    Attributes:
        component_id: Unique identifier for the component
        system_id: ID of system this component belongs to
        name: Component name
        type: Component type
    """
    component_id: str
    system_id: str
    name: str
    type: str


class MaintenanceEvent(BaseModel):
    """Represents a maintenance event node in the database.
    
    Attributes:
        event_id: Unique identifier for the event
        aircraft_id: ID of affected aircraft
        system_id: ID of affected system
        component_id: ID of affected component
        fault: Description of the fault
        severity: Severity level (e.g., CRITICAL, MINOR)
        reported_at: When the event was reported (ISO format)
        corrective_action: Action taken to resolve the issue
    """
    event_id: str
    aircraft_id: str
    system_id: str
    component_id: str
    fault: str
    severity: str
    reported_at: str
    corrective_action: str


class Delay(BaseModel):
    """Represents a flight delay node in the database.
    
    Attributes:
        delay_id: Unique identifier for the delay
        flight_id: ID of affected flight
        minutes: Duration of delay in minutes
        cause: Reason for the delay
    """
    delay_id: str
    flight_id: str
    minutes: int
    cause: str


class Sensor(BaseModel):
    """Represents a sensor node in the database.
    
    Attributes:
        sensor_id: Unique identifier for the sensor
        system_id: ID of system this sensor monitors
        name: Sensor name
        type: Sensor type
        unit: Measurement unit
    """
    sensor_id: str
    system_id: str
    name: str
    type: str
    unit: str


class Reading(BaseModel):
    """Represents a sensor reading node in the database.
    
    Attributes:
        reading_id: Unique identifier for the reading
        sensor_id: ID of sensor that took the reading
        timestamp: When the reading was taken (ISO format)
        value: Measured value
    """
    reading_id: str
    sensor_id: str
    timestamp: str
    value: float
