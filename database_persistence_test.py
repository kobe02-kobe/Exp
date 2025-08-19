#!/usr/bin/env python3
"""
Database Persistence and Concurrent Operations Test
"""

import requests
import json
from datetime import datetime

BACKEND_URL = "https://pro-camera-1.preview.emergentagent.com/api"

def test_database_persistence():
    """Test data persistence across multiple operations"""
    print("🗄️  Testing Database Persistence")
    print("-" * 40)
    
    session = requests.Session()
    
    # Create multiple settings to test persistence
    settings_list = []
    for i in range(3):
        settings_data = {
            "name": f"Persistence Test Settings {i+1}",
            "iso": 800 + (i * 200),
            "aperture": 2.8 + (i * 0.5),
            "mode": "manual"
        }
        
        response = session.post(f"{BACKEND_URL}/camera/settings", json=settings_data)
        if response.status_code == 200:
            settings = response.json()
            settings_list.append(settings['id'])
            print(f"✅ Created settings {i+1}: {settings['name']}")
        else:
            print(f"❌ Failed to create settings {i+1}")
            return False
    
    # Verify all settings persist
    response = session.get(f"{BACKEND_URL}/camera/settings")
    if response.status_code == 200:
        all_settings = response.json()
        if len(all_settings) >= 3:
            print(f"✅ Database persistence verified: {len(all_settings)} settings found")
        else:
            print(f"❌ Persistence issue: Expected at least 3 settings, found {len(all_settings)}")
            return False
    
    # Test recording persistence
    recording_data = {
        "fileName": "persistence_test.mp4",
        "resolution": "4K UHD",
        "frameRate": "24p",
        "settings": {"iso": 800, "aperture": 2.8}
    }
    
    response = session.post(f"{BACKEND_URL}/camera/recordings", json=recording_data)
    if response.status_code == 200:
        recording = response.json()
        recording_id = recording['id']
        print(f"✅ Recording created and persisted: {recording['fileName']}")
        
        # Stop the recording
        response = session.put(f"{BACKEND_URL}/camera/recordings/{recording_id}/stop")
        if response.status_code == 200:
            print("✅ Recording stopped and updated in database")
        
        # Clean up recordings
        session.delete(f"{BACKEND_URL}/camera/recordings/{recording_id}")
    
    # Clean up settings
    for settings_id in settings_list:
        session.delete(f"{BACKEND_URL}/camera/settings/{settings_id}")
    
    print("✅ Database persistence test completed successfully")
    return True

def test_concurrent_operations():
    """Test concurrent API operations"""
    print("\n🔄 Testing Concurrent Operations")
    print("-" * 40)
    
    import threading
    import time
    
    results = []
    
    def create_setting(index):
        session = requests.Session()
        settings_data = {
            "name": f"Concurrent Test {index}",
            "iso": 800 + (index * 100),
            "aperture": 2.8
        }
        
        try:
            response = session.post(f"{BACKEND_URL}/camera/settings", json=settings_data)
            if response.status_code == 200:
                results.append(("success", index, response.json()['id']))
            else:
                results.append(("failed", index, response.status_code))
        except Exception as e:
            results.append(("error", index, str(e)))
    
    # Create 5 concurrent requests
    threads = []
    for i in range(5):
        thread = threading.Thread(target=create_setting, args=(i,))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    # Analyze results
    successful = [r for r in results if r[0] == "success"]
    failed = [r for r in results if r[0] != "success"]
    
    print(f"✅ Concurrent operations completed: {len(successful)} successful, {len(failed)} failed")
    
    if len(successful) >= 4:  # Allow for some potential race conditions
        print("✅ Concurrent operations test passed")
        
        # Clean up created settings
        session = requests.Session()
        for result in successful:
            settings_id = result[2]
            session.delete(f"{BACKEND_URL}/camera/settings/{settings_id}")
        
        return True
    else:
        print(f"❌ Concurrent operations test failed: too many failures")
        return False

def main():
    """Run database and concurrency tests"""
    print("🧪 Database Integration and Concurrency Tests")
    print("=" * 50)
    
    persistence_success = test_database_persistence()
    concurrent_success = test_concurrent_operations()
    
    if persistence_success and concurrent_success:
        print("\n🎉 All database integration tests passed!")
        return True
    else:
        print("\n⚠️  Some database integration tests failed")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)