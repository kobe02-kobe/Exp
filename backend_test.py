#!/usr/bin/env python3
"""
Comprehensive Backend API Tests for Professional Camera Application
Tests all camera-related endpoints including settings, recordings, status, and capabilities.
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any

# Get backend URL from environment
BACKEND_URL = "https://pro-camera-1.preview.emergentagent.com/api"

class CameraAPITester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.session = requests.Session()
        self.test_results = []
        self.created_settings_ids = []
        self.created_recording_ids = []
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test results"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")
        if details:
            print(f"   Details: {details}")
    
    def test_basic_connectivity(self):
        """Test basic API connectivity"""
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                data = response.json()
                self.log_test("Basic API Connectivity", True, f"Response: {data.get('message', 'No message')}")
                return True
            else:
                self.log_test("Basic API Connectivity", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Basic API Connectivity", False, f"Error: {str(e)}")
            return False
    
    def test_camera_capabilities(self):
        """Test camera capabilities endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/camera/capabilities")
            if response.status_code == 200:
                data = response.json()
                required_fields = ['modes', 'isoValues', 'apertureValues', 'shutterSpeeds', 
                                 'whiteBalanceOptions', 'recordingFormats', 'frameRates', 'colorProfiles']
                
                missing_fields = [field for field in required_fields if field not in data]
                if not missing_fields:
                    self.log_test("Camera Capabilities", True, 
                                f"All required fields present. ISO values: {len(data['isoValues'])}, Modes: {len(data['modes'])}")
                    return True
                else:
                    self.log_test("Camera Capabilities", False, f"Missing fields: {missing_fields}")
                    return False
            else:
                self.log_test("Camera Capabilities", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Camera Capabilities", False, f"Error: {str(e)}")
            return False
    
    def test_camera_settings_crud(self):
        """Test complete CRUD operations for camera settings"""
        # Test data for professional camera settings
        test_settings = {
            "name": "Professional Portrait Setup",
            "iso": 800,
            "aperture": 2.8,
            "shutterSpeed": "1/125",
            "focus": 85,
            "whiteBalance": "daylight",
            "exposure": 0.3,
            "mode": "manual",
            "zoom": 1.5,
            "recordingFormat": "4K UHD",
            "frameRate": "24p",
            "colorProfile": "S-Log3",
            "stabilization": True
        }
        
        # CREATE - Test creating new settings
        try:
            response = self.session.post(f"{self.base_url}/camera/settings", json=test_settings)
            if response.status_code == 200:
                created_settings = response.json()
                settings_id = created_settings.get('id')
                self.created_settings_ids.append(settings_id)
                self.log_test("Create Camera Settings", True, f"Created settings with ID: {settings_id}")
            else:
                self.log_test("Create Camera Settings", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
        except Exception as e:
            self.log_test("Create Camera Settings", False, f"Error: {str(e)}")
            return False
        
        # READ - Test getting specific settings
        try:
            response = self.session.get(f"{self.base_url}/camera/settings/{settings_id}")
            if response.status_code == 200:
                retrieved_settings = response.json()
                if retrieved_settings['name'] == test_settings['name'] and retrieved_settings['iso'] == test_settings['iso']:
                    self.log_test("Get Specific Camera Settings", True, f"Retrieved settings: {retrieved_settings['name']}")
                else:
                    self.log_test("Get Specific Camera Settings", False, "Data mismatch in retrieved settings")
                    return False
            else:
                self.log_test("Get Specific Camera Settings", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Get Specific Camera Settings", False, f"Error: {str(e)}")
            return False
        
        # READ ALL - Test getting all settings
        try:
            response = self.session.get(f"{self.base_url}/camera/settings")
            if response.status_code == 200:
                all_settings = response.json()
                if isinstance(all_settings, list) and len(all_settings) > 0:
                    self.log_test("Get All Camera Settings", True, f"Retrieved {len(all_settings)} settings")
                else:
                    self.log_test("Get All Camera Settings", False, "No settings returned or invalid format")
                    return False
            else:
                self.log_test("Get All Camera Settings", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Get All Camera Settings", False, f"Error: {str(e)}")
            return False
        
        # UPDATE - Test updating settings
        update_data = {
            "name": "Updated Professional Portrait Setup",
            "iso": 1600,
            "aperture": 4.0
        }
        try:
            response = self.session.put(f"{self.base_url}/camera/settings/{settings_id}", json=update_data)
            if response.status_code == 200:
                updated_settings = response.json()
                if updated_settings['name'] == update_data['name'] and updated_settings['iso'] == update_data['iso']:
                    self.log_test("Update Camera Settings", True, f"Updated settings: {updated_settings['name']}")
                else:
                    self.log_test("Update Camera Settings", False, "Update data not reflected correctly")
                    return False
            else:
                self.log_test("Update Camera Settings", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Update Camera Settings", False, f"Error: {str(e)}")
            return False
        
        return True
    
    def test_recording_management(self):
        """Test recording session management"""
        # Test data for recording
        recording_data = {
            "fileName": "professional_shoot_001.mp4",
            "resolution": "4K UHD",
            "frameRate": "24p",
            "settings": {
                "iso": 800,
                "aperture": 2.8,
                "shutterSpeed": "1/50",
                "whiteBalance": "daylight"
            }
        }
        
        # START RECORDING - Test starting a recording
        try:
            response = self.session.post(f"{self.base_url}/camera/recordings", json=recording_data)
            if response.status_code == 200:
                recording = response.json()
                recording_id = recording.get('id')
                self.created_recording_ids.append(recording_id)
                if recording['status'] == 'recording':
                    self.log_test("Start Recording", True, f"Started recording: {recording['fileName']}")
                else:
                    self.log_test("Start Recording", False, f"Recording status not 'recording': {recording['status']}")
                    return False
            else:
                self.log_test("Start Recording", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
        except Exception as e:
            self.log_test("Start Recording", False, f"Error: {str(e)}")
            return False
        
        # Wait a moment to simulate recording time
        time.sleep(2)
        
        # STOP RECORDING - Test stopping the recording
        try:
            response = self.session.put(f"{self.base_url}/camera/recordings/{recording_id}/stop")
            if response.status_code == 200:
                stopped_recording = response.json()
                if stopped_recording['status'] == 'completed' and stopped_recording.get('duration', 0) > 0:
                    self.log_test("Stop Recording", True, 
                                f"Stopped recording. Duration: {stopped_recording['duration']}s, Size: {stopped_recording.get('fileSize', 0)}MB")
                else:
                    self.log_test("Stop Recording", False, f"Recording not properly stopped: {stopped_recording}")
                    return False
            else:
                self.log_test("Stop Recording", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Stop Recording", False, f"Error: {str(e)}")
            return False
        
        # GET SPECIFIC RECORDING - Test retrieving specific recording
        try:
            response = self.session.get(f"{self.base_url}/camera/recordings/{recording_id}")
            if response.status_code == 200:
                retrieved_recording = response.json()
                if retrieved_recording['fileName'] == recording_data['fileName']:
                    self.log_test("Get Specific Recording", True, f"Retrieved recording: {retrieved_recording['fileName']}")
                else:
                    self.log_test("Get Specific Recording", False, "Recording data mismatch")
                    return False
            else:
                self.log_test("Get Specific Recording", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Get Specific Recording", False, f"Error: {str(e)}")
            return False
        
        # GET ALL RECORDINGS - Test retrieving all recordings
        try:
            response = self.session.get(f"{self.base_url}/camera/recordings")
            if response.status_code == 200:
                all_recordings = response.json()
                if isinstance(all_recordings, list) and len(all_recordings) > 0:
                    self.log_test("Get All Recordings", True, f"Retrieved {len(all_recordings)} recordings")
                else:
                    self.log_test("Get All Recordings", False, "No recordings returned or invalid format")
                    return False
            else:
                self.log_test("Get All Recordings", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Get All Recordings", False, f"Error: {str(e)}")
            return False
        
        return True
    
    def test_camera_status(self):
        """Test camera status operations"""
        # GET STATUS - Test getting current camera status
        try:
            response = self.session.get(f"{self.base_url}/camera/status")
            if response.status_code == 200:
                status = response.json()
                required_fields = ['battery', 'storage', 'storageUsed', 'temperature', 'lastUpdate']
                missing_fields = [field for field in required_fields if field not in status]
                if not missing_fields:
                    self.log_test("Get Camera Status", True, 
                                f"Battery: {status['battery']}%, Storage: {status['storage']}, Temp: {status['temperature']}")
                else:
                    self.log_test("Get Camera Status", False, f"Missing fields: {missing_fields}")
                    return False
            else:
                self.log_test("Get Camera Status", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Get Camera Status", False, f"Error: {str(e)}")
            return False
        
        # UPDATE STATUS - Test updating camera status
        update_status = {
            "battery": 75,
            "storage": "128GB",
            "storageUsed": 45.2,
            "temperature": "Normal"
        }
        try:
            response = self.session.put(f"{self.base_url}/camera/status", json=update_status)
            if response.status_code == 200:
                updated_status = response.json()
                if updated_status['battery'] == update_status['battery']:
                    self.log_test("Update Camera Status", True, 
                                f"Updated status - Battery: {updated_status['battery']}%, Storage Used: {updated_status['storageUsed']}GB")
                else:
                    self.log_test("Update Camera Status", False, "Status update not reflected correctly")
                    return False
            else:
                self.log_test("Update Camera Status", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Update Camera Status", False, f"Error: {str(e)}")
            return False
        
        return True
    
    def test_data_validation(self):
        """Test data validation with invalid inputs"""
        # Test invalid camera settings
        invalid_settings = {
            "name": "Invalid Settings Test",
            "iso": 50000,  # Invalid ISO value
            "aperture": 0.5,  # Invalid aperture
            "shutterSpeed": "invalid_speed",
            "focus": -10  # Invalid focus
        }
        
        try:
            response = self.session.post(f"{self.base_url}/camera/settings", json=invalid_settings)
            if response.status_code == 422:  # Validation error expected
                self.log_test("Data Validation - Invalid Settings", True, "Properly rejected invalid settings")
            else:
                self.log_test("Data Validation - Invalid Settings", False, 
                            f"Should have rejected invalid data but got status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Data Validation - Invalid Settings", False, f"Error: {str(e)}")
            return False
        
        # Test invalid recording data
        invalid_recording = {
            "fileName": "",  # Empty filename
            "resolution": "invalid_resolution",
            "frameRate": "invalid_rate",
            "settings": "not_a_dict"  # Should be dict
        }
        
        try:
            response = self.session.post(f"{self.base_url}/camera/recordings", json=invalid_recording)
            if response.status_code in [422, 500]:  # Validation or server error expected
                self.log_test("Data Validation - Invalid Recording", True, "Properly handled invalid recording data")
            else:
                self.log_test("Data Validation - Invalid Recording", False, 
                            f"Should have rejected invalid data but got status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Data Validation - Invalid Recording", False, f"Error: {str(e)}")
            return False
        
        return True
    
    def test_error_handling(self):
        """Test error handling for non-existent resources"""
        # Test getting non-existent settings
        fake_id = "non-existent-id-12345"
        try:
            response = self.session.get(f"{self.base_url}/camera/settings/{fake_id}")
            if response.status_code == 404:
                self.log_test("Error Handling - Non-existent Settings", True, "Properly returned 404 for non-existent settings")
            else:
                self.log_test("Error Handling - Non-existent Settings", False, 
                            f"Expected 404 but got: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Error Handling - Non-existent Settings", False, f"Error: {str(e)}")
            return False
        
        # Test stopping non-existent recording
        try:
            response = self.session.put(f"{self.base_url}/camera/recordings/{fake_id}/stop")
            if response.status_code == 404:
                self.log_test("Error Handling - Non-existent Recording", True, "Properly returned 404 for non-existent recording")
            else:
                self.log_test("Error Handling - Non-existent Recording", False, 
                            f"Expected 404 but got: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Error Handling - Non-existent Recording", False, f"Error: {str(e)}")
            return False
        
        return True
    
    def cleanup_test_data(self):
        """Clean up test data created during testing"""
        cleanup_success = True
        
        # Delete created settings
        for settings_id in self.created_settings_ids:
            try:
                response = self.session.delete(f"{self.base_url}/camera/settings/{settings_id}")
                if response.status_code == 200:
                    self.log_test(f"Cleanup Settings {settings_id}", True, "Successfully deleted test settings")
                else:
                    self.log_test(f"Cleanup Settings {settings_id}", False, f"Failed to delete: {response.status_code}")
                    cleanup_success = False
            except Exception as e:
                self.log_test(f"Cleanup Settings {settings_id}", False, f"Error: {str(e)}")
                cleanup_success = False
        
        # Delete created recordings
        for recording_id in self.created_recording_ids:
            try:
                response = self.session.delete(f"{self.base_url}/camera/recordings/{recording_id}")
                if response.status_code == 200:
                    self.log_test(f"Cleanup Recording {recording_id}", True, "Successfully deleted test recording")
                else:
                    self.log_test(f"Cleanup Recording {recording_id}", False, f"Failed to delete: {response.status_code}")
                    cleanup_success = False
            except Exception as e:
                self.log_test(f"Cleanup Recording {recording_id}", False, f"Error: {str(e)}")
                cleanup_success = False
        
        return cleanup_success
    
    def run_all_tests(self):
        """Run all camera API tests"""
        print("🎬 Starting Professional Camera API Tests")
        print("=" * 50)
        
        # Test basic connectivity first
        if not self.test_basic_connectivity():
            print("❌ Basic connectivity failed. Stopping tests.")
            return False
        
        # Run all test suites
        test_suites = [
            ("Camera Capabilities", self.test_camera_capabilities),
            ("Camera Settings CRUD", self.test_camera_settings_crud),
            ("Recording Management", self.test_recording_management),
            ("Camera Status", self.test_camera_status),
            ("Data Validation", self.test_data_validation),
            ("Error Handling", self.test_error_handling)
        ]
        
        all_passed = True
        for suite_name, test_func in test_suites:
            print(f"\n📋 Running {suite_name} Tests:")
            print("-" * 30)
            if not test_func():
                all_passed = False
                print(f"❌ {suite_name} tests failed")
            else:
                print(f"✅ {suite_name} tests passed")
        
        # Cleanup test data
        print(f"\n🧹 Cleaning up test data:")
        print("-" * 30)
        self.cleanup_test_data()
        
        # Print summary
        print(f"\n📊 Test Summary:")
        print("=" * 50)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        total_tests = len(self.test_results)
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if all_passed:
            print("\n🎉 All camera API tests passed successfully!")
        else:
            print("\n⚠️  Some tests failed. Check the details above.")
            
        return all_passed

def main():
    """Main function to run camera API tests"""
    tester = CameraAPITester()
    success = tester.run_all_tests()
    
    # Save detailed results to file
    with open('/app/camera_api_test_results.json', 'w') as f:
        json.dump(tester.test_results, f, indent=2)
    
    print(f"\n📄 Detailed test results saved to: /app/camera_api_test_results.json")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)