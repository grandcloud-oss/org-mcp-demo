"""Pydantic models for airplane data entities."""

from typing import Optional
from pydantic import BaseModel, Field


class Aircraft(BaseModel):
    """Represents an aircraft in the fleet."""
    
    aircraft_id: str = Field(..., description="Unique aircraft identifier")
    tail_number: str = Field(..., description="Aircraft tail number")
    icao24: str = Field(..., description="ICAO 24-bit address")
    model: str = Field(..., description="Aircraft model (e.g., B737-800)")
    operator: str = Field(..., description="Operating airline")
    manufacturer: str = Field(..., description="Aircraft manufacturer")


class Airport(BaseModel):
    """Represents an airport."""
    
    airport_id: str = Field(..., description="Unique airport identifier")
    name: str = Field(..., description="Airport name")
    iata: str = Field(..., description="IATA airport code")
    icao: str = Field(..., description="ICAO airport code")
    city: str = Field(..., description="City where airport is located")
    country: str = Field(..., description="Country where airport is located")
    lat: float = Field(..., description="Latitude coordinate")
    lon: float = Field(..., description="Longitude coordinate")


class Flight(BaseModel):
    """Represents a flight operation."""
    
    flight_id: str = Field(..., description="Unique flight identifier")
    flight_number: str = Field(..., description="Flight number")
    aircraft_id: str = Field(..., description="Aircraft operating this flight")
    operator: str = Field(..., description="Operating airline")
    origin: str = Field(..., description="Origin airport IATA code")
    destination: str = Field(..., description="Destination airport IATA code")
    scheduled_departure: str = Field(..., description="Scheduled departure time (ISO format)")
    scheduled_arrival: str = Field(..., description="Scheduled arrival time (ISO format)")


class MaintenanceEvent(BaseModel):
    """Represents a maintenance event for an aircraft."""
    
    event_id: str = Field(..., description="Unique event identifier")
    aircraft_id: str = Field(..., description="Aircraft affected by this event")
    system_id: str = Field(..., description="System affected by this event")
    component_id: str = Field(..., description="Component affected by this event")
    fault: str = Field(..., description="Description of the fault")
    severity: str = Field(..., description="Severity level of the event")
    corrective_action: str = Field(..., description="Corrective action taken")
    reported_at: str = Field(..., description="Time when event was reported (ISO format)")


class System(BaseModel):
    """Represents an aircraft system."""
    
    system_id: str = Field(..., description="Unique system identifier")
    aircraft_id: str = Field(..., description="Aircraft this system belongs to")
    name: str = Field(..., description="System name")
    type: str = Field(..., description="System type")


class Component(BaseModel):
    """Represents a component within a system."""
    
    component_id: str = Field(..., description="Unique component identifier")
    system_id: str = Field(..., description="System this component belongs to")
    name: str = Field(..., description="Component name")
    type: str = Field(..., description="Component type")


class Sensor(BaseModel):
    """Represents a sensor within a system."""
    
    sensor_id: str = Field(..., description="Unique sensor identifier")
    system_id: str = Field(..., description="System this sensor belongs to")
    name: str = Field(..., description="Sensor name")
    type: str = Field(..., description="Sensor type")
    unit: str = Field(..., description="Unit of measurement")


class Delay(BaseModel):
    """Represents a flight delay."""
    
    delay_id: str = Field(..., description="Unique delay identifier")
    flight_id: str = Field(..., description="Flight affected by this delay")
    cause: str = Field(..., description="Cause of the delay")
    minutes: int = Field(..., description="Duration of delay in minutes")


class Reading(BaseModel):
    """Represents a sensor reading."""
    
    reading_id: str = Field(..., description="Unique reading identifier")
    sensor_id: str = Field(..., description="Sensor that captured this reading")
    timestamp: str = Field(..., description="Time of reading (ISO format)")
    value: float = Field(..., description="Reading value")
