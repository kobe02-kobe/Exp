from datetime import datetime
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from models.camera import CameraSettings, CameraSettingsCreate, CameraSettingsUpdate, Recording, RecordingCreate, CameraStatus, CameraCapabilities
import time

class CameraService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.settings_collection = db.camera_settings
        self.recordings_collection = db.recordings
        self.status_collection = db.camera_status

    async def create_settings(self, settings_data: CameraSettingsCreate) -> CameraSettings:
        """Create new camera settings preset"""
        settings = CameraSettings(**settings_data.dict())
        await self.settings_collection.insert_one(settings.dict())
        return settings

    async def get_settings(self, settings_id: str) -> Optional[CameraSettings]:
        """Get specific camera settings by ID"""
        settings_doc = await self.settings_collection.find_one({"id": settings_id})
        if settings_doc:
            return CameraSettings(**settings_doc)
        return None

    async def get_all_settings(self) -> List[CameraSettings]:
        """Get all saved camera settings"""
        cursor = self.settings_collection.find().sort("createdAt", -1)
        settings_list = await cursor.to_list(length=100)
        return [CameraSettings(**settings) for settings in settings_list]

    async def update_settings(self, settings_id: str, update_data: CameraSettingsUpdate) -> Optional[CameraSettings]:
        """Update existing camera settings"""
        update_dict = {k: v for k, v in update_data.dict().items() if v is not None}
        if update_dict:
            update_dict["updatedAt"] = datetime.utcnow()
            await self.settings_collection.update_one(
                {"id": settings_id}, 
                {"$set": update_dict}
            )
            return await self.get_settings(settings_id)
        return None

    async def delete_settings(self, settings_id: str) -> bool:
        """Delete camera settings"""
        result = await self.settings_collection.delete_one({"id": settings_id})
        return result.deleted_count > 0

    async def start_recording(self, recording_data: RecordingCreate) -> Recording:
        """Start a new recording session"""
        recording = Recording(
            fileName=recording_data.fileName,
            resolution=recording_data.resolution,
            frameRate=recording_data.frameRate,
            settings=recording_data.settings,
            startTime=datetime.utcnow(),
            status="recording"
        )
        await self.recordings_collection.insert_one(recording.dict())
        return recording

    async def stop_recording(self, recording_id: str) -> Optional[Recording]:
        """Stop recording session"""
        recording = await self.get_recording(recording_id)
        if recording and recording.status == "recording":
            end_time = datetime.utcnow()
            duration = (end_time - recording.startTime).total_seconds()
            file_size = duration * 0.5  # Simulate file size (0.5 MB per second)
            
            await self.recordings_collection.update_one(
                {"id": recording_id},
                {
                    "$set": {
                        "endTime": end_time,
                        "duration": duration,
                        "fileSize": file_size,
                        "status": "completed"
                    }
                }
            )
            return await self.get_recording(recording_id)
        return None

    async def get_recording(self, recording_id: str) -> Optional[Recording]:
        """Get specific recording by ID"""
        recording_doc = await self.recordings_collection.find_one({"id": recording_id})
        if recording_doc:
            return Recording(**recording_doc)
        return None

    async def get_all_recordings(self) -> List[Recording]:
        """Get all recordings"""
        cursor = self.recordings_collection.find().sort("startTime", -1)
        recordings_list = await cursor.to_list(length=100)
        return [Recording(**recording) for recording in recordings_list]

    async def delete_recording(self, recording_id: str) -> bool:
        """Delete recording"""
        result = await self.recordings_collection.delete_one({"id": recording_id})
        return result.deleted_count > 0

    async def get_camera_status(self) -> CameraStatus:
        """Get current camera status"""
        status_doc = await self.status_collection.find_one({}, sort=[("lastUpdate", -1)])
        if status_doc:
            return CameraStatus(**status_doc)
        
        # Return default status if none exists
        default_status = CameraStatus()
        await self.status_collection.insert_one(default_status.dict())
        return default_status

    async def update_camera_status(self, status_data: dict) -> CameraStatus:
        """Update camera status"""
        status_data["lastUpdate"] = datetime.utcnow()
        
        # Upsert the status (update if exists, create if doesn't)
        await self.status_collection.replace_one(
            {},  # Match any document
            status_data,
            upsert=True
        )
        return CameraStatus(**status_data)

    def get_camera_capabilities(self) -> CameraCapabilities:
        """Get camera capabilities and supported values"""
        return CameraCapabilities(
            modes=[
                {"id": "manual", "name": "Manual", "description": "Full manual control"},
                {"id": "auto", "name": "Auto", "description": "Automatic settings"},
                {"id": "cinema", "name": "Cinema", "description": "Cinema optimized"},
                {"id": "portrait", "name": "Portrait", "description": "Portrait mode"},
                {"id": "landscape", "name": "Landscape", "description": "Landscape mode"}
            ],
            isoValues=[100, 200, 400, 800, 1600, 3200, 6400, 12800],
            apertureValues=[1.4, 2, 2.8, 4, 5.6, 8, 11, 16],
            shutterSpeeds=["1/4000", "1/2000", "1/1000", "1/500", "1/250", "1/125", "1/60", "1/30", "1/15", "1/8"],
            whiteBalanceOptions=[
                {"id": "auto", "name": "Auto", "temp": 5500},
                {"id": "daylight", "name": "Daylight", "temp": 5500},
                {"id": "cloudy", "name": "Cloudy", "temp": 6500},
                {"id": "tungsten", "name": "Tungsten", "temp": 3200},
                {"id": "fluorescent", "name": "Fluorescent", "temp": 4000},
                {"id": "flash", "name": "Flash", "temp": 5500}
            ],
            recordingFormats=["4K UHD", "FHD", "HD"],
            frameRates=["24p", "30p", "60p", "120p"],
            colorProfiles=["S-Log3", "Standard", "Cinema", "Vivid"]
        )