# python-test-flow

A Python utility for downloading files from URLs with progress tracking and robust error handling.

## Features

- Download files from any URL with progress tracking
- Automatic filename detection from URLs
- Configurable chunk size for downloads
- Comprehensive error handling and validation
- Type hints for better code quality
- Extensive test suite with >99% coverage

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### As a Module

```python
from download_file import download_file

# Download with automatic filename
result = download_file('https://example.com/file.zip')

# Download to specific location
result = download_file('https://example.com/file.zip', 'downloads/myfile.zip')

# Download with custom chunk size
result = download_file('https://example.com/file.zip', chunk_size=4096)
```

### Command Line Interface

```bash
python3 download_file.py
```

## Development

### Running Tests

```bash
# Run all tests
python3 -m pytest

# Run with coverage
python3 -m pytest --cov=download_file --cov-report=term-missing

# Run only unit tests (skip integration tests)
python3 -m pytest -m "not integration"
```

### Code Quality

```bash
# Format code
black .

# Lint code
flake8 .

# Type checking
mypy download_file.py
```

## API Reference

### download_file(url, destination=None, chunk_size=8192)

Download a file from a URL.

**Parameters:**
- `url` (str): The URL to download from
- `destination` (str, optional): Local path to save the file. If None, uses filename from URL
- `chunk_size` (int): Size of chunks to download at a time (default: 8192 bytes)

**Returns:**
- `str`: Path to the downloaded file

**Raises:**
- `ValueError`: If URL is invalid or empty, or chunk_size is not positive
- `requests.RequestException`: If there's an error with the HTTP request
- `IOError`: If there's an error writing the file
