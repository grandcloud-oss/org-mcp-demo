"""Pydantic models for Neo4j entities."""

from typing import Optional
from pydantic import BaseModel, Field


class Aircraft(BaseModel):
    """Represents an aircraft entity."""
    
    aircraft_id: str
    tail_number: str
    icao24: str
    model: str
    operator: str
    manufacturer: str


class Flight(BaseModel):
    """Represents a flight entity."""
    
    flight_id: str
    flight_number: str
    aircraft_id: str
    operator: str
    origin: str
    destination: str
    scheduled_departure: str
    scheduled_arrival: str


class Airport(BaseModel):
    """Represents an airport entity."""
    
    airport_id: str
    name: str
    city: str
    country: str
    iata: str
    icao: str
    lat: float
    lon: float


class MaintenanceEvent(BaseModel):
    """Represents a maintenance event entity."""
    
    event_id: str
    aircraft_id: str
    system_id: str
    component_id: str
    fault: str
    severity: str
    corrective_action: str
    reported_at: str


class System(BaseModel):
    """Represents an aircraft system entity."""
    
    system_id: str
    aircraft_id: str
    name: str
    type: str


class Component(BaseModel):
    """Represents a system component entity."""
    
    component_id: str
    system_id: str
    name: str
    type: str


class Sensor(BaseModel):
    """Represents a sensor entity."""
    
    sensor_id: str
    system_id: str
    name: str
    type: str
    unit: str


class Delay(BaseModel):
    """Represents a flight delay entity."""
    
    delay_id: str
    flight_id: str
    cause: str
    minutes: int


class Reading(BaseModel):
    """Represents a sensor reading entity."""
    
    reading_id: str
    sensor_id: str
    timestamp: str
    value: float
