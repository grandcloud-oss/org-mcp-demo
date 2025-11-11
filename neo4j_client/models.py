"""Pydantic models for airplane database entities."""

from typing import Optional
from pydantic import BaseModel, Field


class Aircraft(BaseModel):
    """Represents an aircraft in the fleet."""
    
    aircraft_id: str
    tail_number: str
    icao24: Optional[str] = None
    model: str
    manufacturer: str
    operator: str


class Airport(BaseModel):
    """Represents an airport."""
    
    airport_id: str
    name: str
    iata: str
    icao: str
    city: str
    country: str
    lat: float
    lon: float


class Flight(BaseModel):
    """Represents a flight operation."""
    
    flight_id: str
    flight_number: str
    aircraft_id: str
    operator: str
    origin: str
    destination: str
    scheduled_departure: str
    scheduled_arrival: str


class Delay(BaseModel):
    """Represents a flight delay."""
    
    delay_id: str
    flight_id: str
    cause: str
    minutes: int


class System(BaseModel):
    """Represents an aircraft system."""
    
    system_id: str
    aircraft_id: str
    name: str
    type: str


class Component(BaseModel):
    """Represents a component within a system."""
    
    component_id: str
    system_id: str
    name: str
    type: str


class Sensor(BaseModel):
    """Represents a sensor monitoring a system."""
    
    sensor_id: str
    system_id: str
    name: str
    type: str
    unit: str


class MaintenanceEvent(BaseModel):
    """Represents a maintenance event."""
    
    event_id: str
    aircraft_id: str
    component_id: str
    system_id: str
    fault: str
    severity: str
    corrective_action: str
    reported_at: str


class Reading(BaseModel):
    """Represents a sensor reading."""
    
    reading_id: str
    sensor_id: str
    timestamp: str
    value: float
