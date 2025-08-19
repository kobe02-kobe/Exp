// Mock data for camera application
export const mockCameraSettings = {
  iso: 800,
  aperture: 2.8,
  shutterSpeed: "1/60",
  focus: 85,
  whiteBalance: "daylight",
  exposure: 0,
  mode: "manual", // manual or auto
  recording: false,
  zoom: 1.0
};

export const mockCameraModes = [
  { id: "manual", name: "Manual", description: "Full manual control" },
  { id: "auto", name: "Auto", description: "Automatic settings" },
  { id: "cinema", name: "Cinema", description: "Cinema optimized" },
  { id: "portrait", name: "Portrait", description: "Portrait mode" },
  { id: "landscape", name: "Landscape", description: "Landscape mode" }
];

export const mockISOValues = [100, 200, 400, 800, 1600, 3200, 6400, 12800];
export const mockApertureValues = [1.4, 2, 2.8, 4, 5.6, 8, 11, 16];
export const mockShutterSpeeds = ["1/4000", "1/2000", "1/1000", "1/500", "1/250", "1/125", "1/60", "1/30", "1/15", "1/8"];
export const mockWhiteBalanceOptions = [
  { id: "auto", name: "Auto", temp: 5500 },
  { id: "daylight", name: "Daylight", temp: 5500 },
  { id: "cloudy", name: "Cloudy", temp: 6500 },
  { id: "tungsten", name: "Tungsten", temp: 3200 },
  { id: "fluorescent", name: "Fluorescent", temp: 4000 },
  { id: "flash", name: "Flash", temp: 5500 }
];

export const mockCameraStatus = {
  battery: 85,
  storage: "64GB",
  storageUsed: 23.5,
  recordingTime: "00:00:00",
  fps: 24,
  resolution: "4K UHD",
  temperature: "Normal"
};

// Simulate camera stream (placeholder)
export const mockCameraStream = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iODAwIiBoZWlnaHQ9IjYwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICA8ZGVmcz4KICAgIDxsaW5lYXJHcmFkaWVudCBpZD0iZ3JhZGllbnQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMTAwJSIgeTI9IjEwMCUiPgogICAgICA8c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjojMmEyYTJhO3N0b3Atb3BhY2l0eToxIiAvPgogICAgICA8c3RvcCBvZmZzZXQ9IjUwJSIgc3R5bGU9InN0b3AtY29sb3I6IzM3MzczNztzdG9wLW9wYWNpdHk6MSIgLz4KICAgICAgPHN0b3Agb2Zmc2V0PSIxMDAlIiBzdHlsZT0ic3RvcC1jb2xvcjojMmEyYTJhO3N0b3Atb3BhY2l0eToxIiAvPgogICAgPC9saW5lYXJHcmFkaWVudD4KICA8L2RlZnM+CiAgPHJlY3Qgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgZmlsbD0idXJsKCNncmFkaWVudCkiLz4KICA8Y2lyY2xlIGN4PSI0MDAiIGN5PSIzMDAiIHI9IjUwIiBmaWxsPSIjNWY1ZjVmIiBvcGFjaXR5PSIwLjMiLz4KICA8dGV4dCB4PSI0MDAiIHk9IjMxMCIgZm9udC1mYW1pbHk9IkFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjE0IiBmaWxsPSIjOWY5ZjlmIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj5WSUVXRKLOREVSPC90ZXh0Pgo8L3N2Zz4=";

export const mockMenuItems = [
  { id: "image-quality", name: "Image Quality", options: ["RAW", "JPEG", "RAW+JPEG"] },
  { id: "video-format", name: "Video Format", options: ["4K UHD", "FHD", "HD"] },
  { id: "frame-rate", name: "Frame Rate", options: ["24p", "30p", "60p", "120p"] },
  { id: "color-profile", name: "Color Profile", options: ["S-Log3", "Standard", "Cinema"] },
  { id: "stabilization", name: "Stabilization", options: ["On", "Off"] }
];