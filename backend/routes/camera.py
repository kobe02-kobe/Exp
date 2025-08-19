from fastapi import APIRouter, HTTPException, Depends
from typing import List
from models.camera import CameraSettings, CameraSettingsCreate, CameraSettingsUpdate, Recording, RecordingCreate, CameraStatus, CameraCapabilities
from services.camera_service import CameraService
from motor.motor_asyncio import AsyncIOMotorDatabase
import os

router = APIRouter(prefix="/camera", tags=["camera"])

def get_camera_service() -> CameraService:
    from motor.motor_asyncio import AsyncIOMotorClient
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    return CameraService(db)

# Camera Settings Routes
@router.post("/settings", response_model=CameraSettings)
async def create_camera_settings(
    settings_data: CameraSettingsCreate,
    camera_service: CameraService = Depends(get_camera_service)
):
    """Create new camera settings preset"""
    try:
        return await camera_service.create_settings(settings_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/settings/{settings_id}", response_model=CameraSettings)
async def get_camera_settings(
    settings_id: str,
    camera_service: CameraService = Depends(get_camera_service)
):
    """Get specific camera settings by ID"""
    settings = await camera_service.get_settings(settings_id)
    if not settings:
        raise HTTPException(status_code=404, detail="Camera settings not found")
    return settings

@router.get("/settings", response_model=List[CameraSettings])
async def get_all_camera_settings(
    camera_service: CameraService = Depends(get_camera_service)
):
    """Get all saved camera settings"""
    return await camera_service.get_all_settings()

@router.put("/settings/{settings_id}", response_model=CameraSettings)
async def update_camera_settings(
    settings_id: str,
    update_data: CameraSettingsUpdate,
    camera_service: CameraService = Depends(get_camera_service)
):
    """Update existing camera settings"""
    settings = await camera_service.update_settings(settings_id, update_data)
    if not settings:
        raise HTTPException(status_code=404, detail="Camera settings not found")
    return settings

@router.delete("/settings/{settings_id}")
async def delete_camera_settings(
    settings_id: str,
    camera_service: CameraService = Depends(get_camera_service)
):
    """Delete camera settings"""
    success = await camera_service.delete_settings(settings_id)
    if not success:
        raise HTTPException(status_code=404, detail="Camera settings not found")
    return {"message": "Camera settings deleted successfully"}

# Recording Routes
@router.post("/recordings", response_model=Recording)
async def start_recording(
    recording_data: RecordingCreate,
    camera_service: CameraService = Depends(get_camera_service)
):
    """Start a new recording session"""
    try:
        return await camera_service.start_recording(recording_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/recordings/{recording_id}/stop", response_model=Recording)
async def stop_recording(
    recording_id: str,
    camera_service: CameraService = Depends(get_camera_service)
):
    """Stop recording session"""
    recording = await camera_service.stop_recording(recording_id)
    if not recording:
        raise HTTPException(status_code=404, detail="Recording not found or already stopped")
    return recording

@router.get("/recordings", response_model=List[Recording])
async def get_all_recordings(
    camera_service: CameraService = Depends(get_camera_service)
):
    """Get all recordings"""
    return await camera_service.get_all_recordings()

@router.get("/recordings/{recording_id}", response_model=Recording)
async def get_recording(
    recording_id: str,
    camera_service: CameraService = Depends(get_camera_service)
):
    """Get specific recording by ID"""
    recording = await camera_service.get_recording(recording_id)
    if not recording:
        raise HTTPException(status_code=404, detail="Recording not found")
    return recording

@router.delete("/recordings/{recording_id}")
async def delete_recording(
    recording_id: str,
    camera_service: CameraService = Depends(get_camera_service)
):
    """Delete recording"""
    success = await camera_service.delete_recording(recording_id)
    if not success:
        raise HTTPException(status_code=404, detail="Recording not found")
    return {"message": "Recording deleted successfully"}

# Camera Status Routes
@router.get("/status", response_model=CameraStatus)
async def get_camera_status(
    camera_service: CameraService = Depends(get_camera_service)
):
    """Get current camera status"""
    return await camera_service.get_camera_status()

@router.put("/status", response_model=CameraStatus)
async def update_camera_status(
    status_data: dict,
    camera_service: CameraService = Depends(get_camera_service)
):
    """Update camera status"""
    try:
        return await camera_service.update_camera_status(status_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Camera Capabilities Route
@router.get("/capabilities", response_model=CameraCapabilities)
async def get_camera_capabilities(
    camera_service: CameraService = Depends(get_camera_service)
):
    """Get camera capabilities and supported values"""
    return camera_service.get_camera_capabilities()