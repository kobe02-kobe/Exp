from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

class CameraSettings(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(default="Default Settings")
    iso: int = Field(default=800, ge=100, le=12800)
    aperture: float = Field(default=2.8, ge=1.4, le=16.0)
    shutterSpeed: str = Field(default="1/60")
    focus: int = Field(default=85, ge=10, le=300)
    whiteBalance: str = Field(default="daylight")
    exposure: float = Field(default=0.0, ge=-3.0, le=3.0)
    mode: str = Field(default="manual")
    zoom: float = Field(default=1.0, ge=0.5, le=10.0)
    recordingFormat: str = Field(default="4K UHD")
    frameRate: str = Field(default="24p")
    colorProfile: str = Field(default="S-Log3")
    stabilization: bool = Field(default=True)
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

class CameraSettingsCreate(BaseModel):
    name: Optional[str] = "Custom Settings"
    iso: Optional[int] = 800
    aperture: Optional[float] = 2.8
    shutterSpeed: Optional[str] = "1/60"
    focus: Optional[int] = 85
    whiteBalance: Optional[str] = "daylight"
    exposure: Optional[float] = 0.0
    mode: Optional[str] = "manual"
    zoom: Optional[float] = 1.0
    recordingFormat: Optional[str] = "4K UHD"
    frameRate: Optional[str] = "24p"
    colorProfile: Optional[str] = "S-Log3"
    stabilization: Optional[bool] = True

class CameraSettingsUpdate(BaseModel):
    name: Optional[str] = None
    iso: Optional[int] = None
    aperture: Optional[float] = None
    shutterSpeed: Optional[str] = None
    focus: Optional[int] = None
    whiteBalance: Optional[str] = None
    exposure: Optional[float] = None
    mode: Optional[str] = None
    zoom: Optional[float] = None
    recordingFormat: Optional[str] = None
    frameRate: Optional[str] = None
    colorProfile: Optional[str] = None
    stabilization: Optional[bool] = None

class Recording(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    sessionId: str = Field(default_factory=lambda: str(uuid.uuid4()))
    fileName: str
    duration: float = Field(default=0.0)  # in seconds
    fileSize: float = Field(default=0.0)  # in MB
    resolution: str
    frameRate: str
    settings: dict  # Store camera settings used
    startTime: datetime
    endTime: Optional[datetime] = None
    status: str = Field(default="recording")  # recording, completed, failed

class RecordingCreate(BaseModel):
    fileName: str
    resolution: str = "4K UHD"
    frameRate: str = "24p"
    settings: dict

class CameraStatus(BaseModel):
    battery: int = Field(default=85, ge=0, le=100)  # percentage
    storage: str = Field(default="64GB")  # total storage
    storageUsed: float = Field(default=23.5)  # GB used
    temperature: str = Field(default="Normal")  # Normal, Warning, Hot
    lastUpdate: datetime = Field(default_factory=datetime.utcnow)

class CameraCapabilities(BaseModel):
    modes: List[dict]
    isoValues: List[int]
    apertureValues: List[float]
    shutterSpeeds: List[str]
    whiteBalanceOptions: List[dict]
    recordingFormats: List[str]
    frameRates: List[str]
    colorProfiles: List[str]