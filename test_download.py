#!/usr/bin/env python3
"""
Simple test script to demonstrate file downloading using requests
"""
from download_file import download_file

def test_downloads():
    """Test the download functionality with sample URLs"""
    print("Testing file download functionality...")
    print("=" * 50)
    
    # Test 1: Download a small JSON file
    print("\nTest 1: Downloading JSON file from httpbin.org")
    try:
        result = download_file("https://httpbin.org/json", "sample.json")
        print(f"✓ Successfully downloaded: {result}")
    except Exception as e:
        print(f"✗ Test 1 failed: {e}")
    
    # Test 2: Download a text file from GitHub
    print("\nTest 2: Downloading README from Python repository")
    try:
        result = download_file("https://raw.githubusercontent.com/python/cpython/main/README.rst", "python_readme.rst")
        print(f"✓ Successfully downloaded: {result}")
    except Exception as e:
        print(f"✗ Test 2 failed: {e}")
    
    # Test 3: Download with auto-filename
    print("\nTest 3: Downloading with automatic filename")
    try:
        result = download_file("https://httpbin.org/uuid")
        print(f"✓ Successfully downloaded: {result}")
    except Exception as e:
        print(f"✗ Test 3 failed: {e}")

if __name__ == "__main__":
    test_downloads()
