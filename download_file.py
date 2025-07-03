import requests
import os
import logging
from typing import Optional
from urllib.parse import urlparse
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_file(url: str, destination: Optional[str] = None, chunk_size: int = 8192) -> str:
    """
    Download a file from a URL using requests.
    
    Args:
        url: The URL to download from
        destination: Local path to save the file. If None, uses filename from URL
        chunk_size: Size of chunks to download at a time (default: 8192 bytes)
    
    Returns:
        Path to the downloaded file
        
    Raises:
        ValueError: If URL is invalid or empty
        requests.RequestException: If there's an error with the HTTP request
        IOError: If there's an error writing the file
    """
    if not url or not isinstance(url, str):
        raise ValueError("URL must be a non-empty string")
    
    if chunk_size <= 0:
        raise ValueError("Chunk size must be positive")
    try:
        # Send GET request
        print(f"Downloading from: {url}")
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Determine filename if not provided
        if destination is None:
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            if not filename:
                filename = "downloaded_file"
            destination = filename
        
        # Create directory if it doesn't exist
        Path(destination).parent.mkdir(parents=True, exist_ok=True)
        
        # Get file size for progress tracking
        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0
        
        # Download and save file
        with open(destination, 'wb') as file:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:  # Filter out keep-alive chunks
                    file.write(chunk)
                    downloaded_size += len(chunk)
                    
                    # Show progress for files larger than 1MB
                    if total_size > 1024 * 1024:
                        progress = (downloaded_size / total_size) * 100
                        print(f"\rProgress: {progress:.1f}%", end="", flush=True)
        
        if total_size > 1024 * 1024:
            print()  # New line after progress
            
        print(f"File downloaded successfully: {destination}")
        print(f"File size: {downloaded_size} bytes")
        return destination
        
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
        raise
    except IOError as e:
        print(f"Error saving file: {e}")
        raise

def main() -> None:
    """
    Example usage of the download_file function
    """
    # Example URLs for testing
    test_urls = [
        "https://httpbin.org/json",  # Small JSON file
        "https://raw.githubusercontent.com/python/cpython/main/README.rst"  # Text file
    ]
    
    print("File Download Script")
    print("=" * 50)
    
    # Interactive mode
    while True:
        print("\nOptions:")
        print("1. Download from custom URL")
        print("2. Test with sample URLs")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            url = input("Enter URL to download: ").strip()
            if url:
                try:
                    destination = input("Enter destination path (press Enter for auto): ").strip()
                    if not destination:
                        destination = None
                    download_file(url, destination)
                except Exception as e:
                    print(f"Download failed: {e}")
            else:
                print("Invalid URL")
                
        elif choice == "2":
            for i, url in enumerate(test_urls, 1):
                print(f"\nTesting URL {i}: {url}")
                try:
                    download_file(url, f"test_file_{i}")
                except Exception as e:
                    print(f"Test {i} failed: {e}")
                    
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
