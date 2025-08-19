import React, { useState, useEffect } from 'react';
import { Play, Square, Settings, Camera, Video, Zap, Battery, HardDrive } from 'lucide-react';
import { Button } from './ui/button';
import { Card } from './ui/card';
import { Slider } from './ui/slider';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Badge } from './ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { mockCameraSettings, mockCameraModes, mockISOValues, mockApertureValues, mockShutterSpeeds, mockWhiteBalanceOptions, mockCameraStatus, mockCameraStream } from '../mock';

const CameraApp = () => {
  const [settings, setSettings] = useState(mockCameraSettings);
  const [status, setStatus] = useState(mockCameraStatus);
  const [showMenu, setShowMenu] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);

  useEffect(() => {
    let interval;
    if (settings.recording) {
      interval = setInterval(() => {
        setRecordingTime(prev => prev + 1);
      }, 1000);
    } else {
      setRecordingTime(0);
    }
    return () => clearInterval(interval);
  }, [settings.recording]);

  const formatTime = (seconds) => {
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hrs.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const updateSetting = (key, value) => {
    setSettings(prev => ({ ...prev, [key]: value }));
  };

  const toggleRecording = () => {
    updateSetting('recording', !settings.recording);
  };

  const toggleMode = () => {
    updateSetting('mode', settings.mode === 'manual' ? 'auto' : 'manual');
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white overflow-hidden">
      {/* Status Bar */}
      <div className="flex justify-between items-center p-4 bg-black/50 backdrop-blur-sm">
        <div className="flex items-center space-x-4">
          <Badge variant="secondary" className="bg-red-600/20 text-red-400 border-red-600/30">
            {settings.recording ? '● REC' : '○ STANDBY'}
          </Badge>
          <span className="text-lg font-mono">{formatTime(recordingTime)}</span>
          <Badge variant="outline" className="text-green-400 border-green-600/30">
            {status.resolution} • {status.fps}fps
          </Badge>
        </div>
        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-1">
            <Battery className="w-4 h-4" />
            <span className="text-sm">{status.battery}%</span>
          </div>
          <div className="flex items-center space-x-1">
            <HardDrive className="w-4 h-4" />
            <span className="text-sm">{status.storageUsed}GB</span>
          </div>
        </div>
      </div>

      <div className="flex h-[calc(100vh-4rem)]">
        {/* Main Viewfinder */}
        <div className="flex-1 relative bg-black">
          <div className="absolute inset-4 border border-gray-600/30 rounded-lg overflow-hidden">
            <img 
              src={mockCameraStream} 
              alt="Camera viewfinder"
              className="w-full h-full object-cover"
            />
            
            {/* Viewfinder Overlay */}
            <div className="absolute inset-0 pointer-events-none">
              {/* Center Focus Point */}
              <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
                <div className="w-8 h-8 border-2 border-white/70 rounded-full"></div>
              </div>
              
              {/* Rule of Thirds Grid */}
              <div className="absolute inset-0 grid grid-cols-3 grid-rows-3 opacity-30">
                {Array.from({ length: 9 }).map((_, i) => (
                  <div key={i} className="border border-white/20"></div>
                ))}
              </div>

              {/* Camera Info Overlay */}
              <div className="absolute bottom-4 left-4 space-y-1">
                <div className="text-sm font-mono bg-black/50 px-2 py-1 rounded">
                  ISO {settings.iso} • f/{settings.aperture} • {settings.shutterSpeed}
                </div>
                <div className="text-xs text-gray-300 bg-black/50 px-2 py-1 rounded">
                  WB: {settings.whiteBalance.toUpperCase()} • Focus: {settings.focus}mm
                </div>
              </div>
            </div>
          </div>

          {/* Recording Controls */}
          <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 flex items-center space-x-4">
            <Button
              onClick={toggleRecording}
              size="lg"
              className={`w-16 h-16 rounded-full ${
                settings.recording 
                  ? 'bg-red-600 hover:bg-red-700 animate-pulse' 
                  : 'bg-red-600/30 hover:bg-red-600/50 border-2 border-red-600'
              }`}
            >
              {settings.recording ? <Square className="w-6 h-6" /> : <Play className="w-6 h-6" />}
            </Button>
            
            <Button variant="outline" size="lg" className="bg-black/50 border-gray-600">
              <Camera className="w-5 h-5" />
            </Button>
          </div>
        </div>

        {/* Control Panel */}
        <div className="w-80 bg-gray-800/95 backdrop-blur-sm border-l border-gray-700">
          <Tabs defaultValue="manual" className="h-full">
            <TabsList className="grid w-full grid-cols-3 bg-gray-900/50">
              <TabsTrigger value="manual" className="text-xs">Manual</TabsTrigger>
              <TabsTrigger value="auto" className="text-xs">Auto</TabsTrigger>
              <TabsTrigger value="menu" className="text-xs">Menu</TabsTrigger>
            </TabsList>

            <div className="p-4 space-y-6 h-[calc(100%-3rem)] overflow-y-auto">
              <TabsContent value="manual" className="space-y-6 mt-0">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold">Manual Controls</h3>
                  <Button
                    onClick={toggleMode}
                    variant="outline"
                    size="sm"
                    className={settings.mode === 'manual' ? 'bg-blue-600/20 border-blue-600' : ''}
                  >
                    {settings.mode.toUpperCase()}
                  </Button>
                </div>

                {/* ISO Control */}
                <Card className="p-4 bg-gray-900/50 border-gray-600">
                  <div className="space-y-3">
                    <div className="flex justify-between items-center">
                      <label className="text-sm font-medium">ISO</label>
                      <span className="text-lg font-mono text-blue-400">{settings.iso}</span>
                    </div>
                    <Select value={settings.iso.toString()} onValueChange={(value) => updateSetting('iso', parseInt(value))}>
                      <SelectTrigger className="bg-gray-800 border-gray-600">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {mockISOValues.map(iso => (
                          <SelectItem key={iso} value={iso.toString()}>{iso}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                </Card>

                {/* Aperture Control */}
                <Card className="p-4 bg-gray-900/50 border-gray-600">
                  <div className="space-y-3">
                    <div className="flex justify-between items-center">
                      <label className="text-sm font-medium">Aperture</label>
                      <span className="text-lg font-mono text-green-400">f/{settings.aperture}</span>
                    </div>
                    <Select value={settings.aperture.toString()} onValueChange={(value) => updateSetting('aperture', parseFloat(value))}>
                      <SelectTrigger className="bg-gray-800 border-gray-600">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {mockApertureValues.map(aperture => (
                          <SelectItem key={aperture} value={aperture.toString()}>f/{aperture}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                </Card>

                {/* Shutter Speed */}
                <Card className="p-4 bg-gray-900/50 border-gray-600">
                  <div className="space-y-3">
                    <div className="flex justify-between items-center">
                      <label className="text-sm font-medium">Shutter Speed</label>
                      <span className="text-lg font-mono text-yellow-400">{settings.shutterSpeed}</span>
                    </div>
                    <Select value={settings.shutterSpeed} onValueChange={(value) => updateSetting('shutterSpeed', value)}>
                      <SelectTrigger className="bg-gray-800 border-gray-600">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {mockShutterSpeeds.map(speed => (
                          <SelectItem key={speed} value={speed}>{speed}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                </Card>

                {/* Focus Control */}
                <Card className="p-4 bg-gray-900/50 border-gray-600">
                  <div className="space-y-3">
                    <div className="flex justify-between items-center">
                      <label className="text-sm font-medium">Focus</label>
                      <span className="text-lg font-mono text-purple-400">{settings.focus}mm</span>
                    </div>
                    <Slider
                      value={[settings.focus]}
                      onValueChange={(value) => updateSetting('focus', value[0])}
                      min={10}
                      max={300}
                      step={5}
                      className="w-full"
                    />
                  </div>
                </Card>

                {/* White Balance */}
                <Card className="p-4 bg-gray-900/50 border-gray-600">
                  <div className="space-y-3">
                    <div className="flex justify-between items-center">
                      <label className="text-sm font-medium">White Balance</label>
                      <span className="text-sm text-orange-400">{settings.whiteBalance.toUpperCase()}</span>
                    </div>
                    <Select value={settings.whiteBalance} onValueChange={(value) => updateSetting('whiteBalance', value)}>
                      <SelectTrigger className="bg-gray-800 border-gray-600">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {mockWhiteBalanceOptions.map(wb => (
                          <SelectItem key={wb.id} value={wb.id}>
                            {wb.name} ({wb.temp}K)
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                </Card>
              </TabsContent>

              <TabsContent value="auto" className="space-y-6 mt-0">
                <div className="text-center py-8">
                  <Zap className="w-16 h-16 mx-auto mb-4 text-blue-400" />
                  <h3 className="text-xl font-semibold mb-2">Auto Mode</h3>
                  <p className="text-gray-400 mb-6">Camera will automatically adjust settings for optimal results</p>
                  
                  <div className="space-y-4">
                    <Button
                      onClick={() => updateSetting('mode', 'auto')}
                      className="w-full bg-blue-600 hover:bg-blue-700"
                      disabled={settings.mode === 'auto'}
                    >
                      Enable Auto Mode
                    </Button>
                    
                    {settings.mode === 'auto' && (
                      <Card className="p-4 bg-green-900/20 border-green-600/30">
                        <p className="text-sm text-green-400">Auto mode active - camera is optimizing settings automatically</p>
                      </Card>
                    )}
                  </div>
                </div>
              </TabsContent>

              <TabsContent value="menu" className="space-y-4 mt-0">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold">Camera Settings</h3>
                  <Settings className="w-5 h-5 text-gray-400" />
                </div>

                <Card className="p-4 bg-gray-900/50 border-gray-600">
                  <h4 className="font-medium mb-3">Recording Format</h4>
                  <Select defaultValue="4k-uhd">
                    <SelectTrigger className="bg-gray-800 border-gray-600">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="4k-uhd">4K UHD (3840x2160)</SelectItem>
                      <SelectItem value="fhd">Full HD (1920x1080)</SelectItem>
                      <SelectItem value="hd">HD (1280x720)</SelectItem>
                    </SelectContent>
                  </Select>
                </Card>

                <Card className="p-4 bg-gray-900/50 border-gray-600">
                  <h4 className="font-medium mb-3">Frame Rate</h4>
                  <Select defaultValue="24p">
                    <SelectTrigger className="bg-gray-800 border-gray-600">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="24p">24p Cinema</SelectItem>
                      <SelectItem value="30p">30p Standard</SelectItem>
                      <SelectItem value="60p">60p Smooth</SelectItem>
                      <SelectItem value="120p">120p Slow Motion</SelectItem>
                    </SelectContent>
                  </Select>
                </Card>

                <Card className="p-4 bg-gray-900/50 border-gray-600">
                  <h4 className="font-medium mb-3">Color Profile</h4>
                  <Select defaultValue="s-log3">
                    <SelectTrigger className="bg-gray-800 border-gray-600">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="s-log3">S-Log3 (Professional)</SelectItem>
                      <SelectItem value="standard">Standard</SelectItem>
                      <SelectItem value="cinema">Cinema</SelectItem>
                      <SelectItem value="vivid">Vivid</SelectItem>
                    </SelectContent>
                  </Select>
                </Card>

                <Card className="p-4 bg-gray-900/50 border-gray-600">
                  <div className="flex justify-between items-center">
                    <span className="font-medium">Image Stabilization</span>
                    <Button variant="outline" size="sm" className="bg-green-600/20 border-green-600 text-green-400">
                      ON
                    </Button>
                  </div>
                </Card>
              </TabsContent>
            </div>
          </Tabs>
        </div>
      </div>
    </div>
  );
};

export default CameraApp;