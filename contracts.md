# Camera Application Backend Contracts

## API Endpoints

### Camera Settings Management
- **POST /api/camera/settings** - Save camera settings
- **GET /api/camera/settings/:id** - Get specific camera settings
- **PUT /api/camera/settings/:id** - Update camera settings
- **GET /api/camera/settings** - Get all saved settings profiles

### Recording Session Management
- **POST /api/recordings** - Start new recording session
- **PUT /api/recordings/:id/stop** - Stop recording session
- **GET /api/recordings** - Get all recordings
- **GET /api/recordings/:id** - Get specific recording details
- **DELETE /api/recordings/:id** - Delete recording

### Camera Status & System Info
- **GET /api/camera/status** - Get current camera status (battery, storage, etc.)
- **GET /api/camera/capabilities** - Get camera capabilities and supported values

## Data Models

### CameraSettings
```json
{
  "id": "string",
  "name": "string", // User-defined preset name
  "iso": "number",
  "aperture": "number", 
  "shutterSpeed": "string",
  "focus": "number",
  "whiteBalance": "string",
  "exposure": "number",
  "mode": "string", // manual, auto, cinema, portrait, landscape
  "zoom": "number",
  "recordingFormat": "string", // 4K UHD, FHD, HD
  "frameRate": "string", // 24p, 30p, 60p, 120p
  "colorProfile": "string", // S-Log3, Standard, Cinema
  "stabilization": "boolean",
  "createdAt": "datetime",
  "updatedAt": "datetime"
}
```

### Recording
```json
{
  "id": "string",
  "sessionId": "string",
  "fileName": "string",
  "duration": "number", // in seconds
  "fileSize": "number", // in MB
  "resolution": "string",
  "frameRate": "string",
  "settings": "CameraSettings", // Settings used for this recording
  "startTime": "datetime",
  "endTime": "datetime",
  "status": "string" // recording, completed, failed
}
```

### CameraStatus
```json
{
  "battery": "number", // percentage
  "storage": "string", // total storage
  "storageUsed": "number", // GB used
  "temperature": "string", // Normal, Warning, Hot
  "lastUpdate": "datetime"
}
```

## Mock Data to Replace

### From mock.js - Replace with backend calls:
- `mockCameraSettings` → GET/POST /api/camera/settings
- `mockCameraStatus` → GET /api/camera/status  
- `mockCameraModes` → GET /api/camera/capabilities
- `mockISOValues`, `mockApertureValues`, etc. → GET /api/camera/capabilities

### Frontend Integration Plan

1. **Settings Management**: Replace mock settings with API calls to save/load camera presets
2. **Recording Sessions**: Implement actual recording start/stop with backend tracking
3. **Real-time Status**: WebSocket or polling for live camera status updates
4. **Settings Persistence**: Save user preferences and custom presets to database
5. **Recording History**: Display list of past recordings with metadata

## Implementation Priority

1. **Phase 1**: Camera settings CRUD operations
2. **Phase 2**: Recording session management  
3. **Phase 3**: Camera status monitoring
4. **Phase 4**: Real-time features (WebSocket for live updates)

## Frontend Changes Required

- Remove imports from mock.js
- Add API service layer (services/cameraApi.js)
- Implement error handling for API calls
- Add loading states for async operations
- Connect all UI interactions to backend endpoints