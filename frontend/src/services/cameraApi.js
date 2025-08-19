import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

class CameraApiService {
  // Camera Settings API
  async createSettings(settingsData) {
    try {
      const response = await axios.post(`${API}/camera/settings`, settingsData);
      return response.data;
    } catch (error) {
      console.error('Error creating camera settings:', error);
      throw error;
    }
  }

  async getSettings(settingsId) {
    try {
      const response = await axios.get(`${API}/camera/settings/${settingsId}`);
      return response.data;
    } catch (error) {
      console.error('Error getting camera settings:', error);
      throw error;
    }
  }

  async getAllSettings() {
    try {
      const response = await axios.get(`${API}/camera/settings`);
      return response.data;
    } catch (error) {
      console.error('Error getting all camera settings:', error);
      throw error;
    }
  }

  async updateSettings(settingsId, updateData) {
    try {
      const response = await axios.put(`${API}/camera/settings/${settingsId}`, updateData);
      return response.data;
    } catch (error) {
      console.error('Error updating camera settings:', error);
      throw error;
    }
  }

  async deleteSettings(settingsId) {
    try {
      const response = await axios.delete(`${API}/camera/settings/${settingsId}`);
      return response.data;
    } catch (error) {
      console.error('Error deleting camera settings:', error);
      throw error;
    }
  }

  // Recording API
  async startRecording(recordingData) {
    try {
      const response = await axios.post(`${API}/camera/recordings`, recordingData);
      return response.data;
    } catch (error) {
      console.error('Error starting recording:', error);
      throw error;
    }
  }

  async stopRecording(recordingId) {
    try {
      const response = await axios.put(`${API}/camera/recordings/${recordingId}/stop`);
      return response.data;
    } catch (error) {
      console.error('Error stopping recording:', error);
      throw error;
    }
  }

  async getAllRecordings() {
    try {
      const response = await axios.get(`${API}/camera/recordings`);
      return response.data;
    } catch (error) {
      console.error('Error getting recordings:', error);
      throw error;
    }
  }

  async getRecording(recordingId) {
    try {
      const response = await axios.get(`${API}/camera/recordings/${recordingId}`);
      return response.data;
    } catch (error) {
      console.error('Error getting recording:', error);
      throw error;
    }
  }

  async deleteRecording(recordingId) {
    try {
      const response = await axios.delete(`${API}/camera/recordings/${recordingId}`);
      return response.data;
    } catch (error) {
      console.error('Error deleting recording:', error);
      throw error;
    }
  }

  // Camera Status API
  async getCameraStatus() {
    try {
      const response = await axios.get(`${API}/camera/status`);
      return response.data;
    } catch (error) {
      console.error('Error getting camera status:', error);
      throw error;
    }
  }

  async updateCameraStatus(statusData) {
    try {
      const response = await axios.put(`${API}/camera/status`, statusData);
      return response.data;
    } catch (error) {
      console.error('Error updating camera status:', error);
      throw error;
    }
  }

  // Camera Capabilities API
  async getCameraCapabilities() {
    try {
      const response = await axios.get(`${API}/camera/capabilities`);
      return response.data;
    } catch (error) {
      console.error('Error getting camera capabilities:', error);
      throw error;
    }
  }
}

export default new CameraApiService();