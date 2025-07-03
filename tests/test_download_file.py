#!/usr/bin/env python3
"""
Comprehensive test suite for download_file module using pytest
"""
import pytest
import requests
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
from download_file import download_file


class TestDownloadFile:
    """Test cases for the download_file function"""
    
    def test_download_file_with_valid_url_and_destination(self):
        """Test downloading a file with valid URL and destination"""
        mock_response = Mock()
        mock_response.headers = {'content-length': '100'}
        mock_response.iter_content.return_value = [b'test content']
        mock_response.raise_for_status.return_value = None
        
        with patch('requests.get', return_value=mock_response),              patch('builtins.open', mock_open()) as mock_file,              patch('pathlib.Path.mkdir'):
            
            result = download_file('https://example.com/test.txt', 'test_output.txt')
            
            assert result == 'test_output.txt'
            mock_file.assert_called_once_with('test_output.txt', 'wb')
    
    def test_download_file_with_auto_filename(self):
        """Test downloading a file with automatic filename detection"""
        mock_response = Mock()
        mock_response.headers = {'content-length': '50'}
        mock_response.iter_content.return_value = [b'content']
        mock_response.raise_for_status.return_value = None
        
        with patch('requests.get', return_value=mock_response),              patch('builtins.open', mock_open()) as mock_file,              patch('pathlib.Path.mkdir'):
            
            result = download_file('https://example.com/file.json')
            
            assert result == 'file.json'
            mock_file.assert_called_once_with('file.json', 'wb')
    
    def test_download_file_with_no_filename_in_url(self):
        """Test downloading when URL has no filename"""
        mock_response = Mock()
        mock_response.headers = {'content-length': '25'}
        mock_response.iter_content.return_value = [b'data']
        mock_response.raise_for_status.return_value = None
        
        with patch('requests.get', return_value=mock_response),              patch('builtins.open', mock_open()) as mock_file,              patch('pathlib.Path.mkdir'):
            
            result = download_file('https://example.com/')
            
            assert result == 'downloaded_file'
            mock_file.assert_called_once_with('downloaded_file', 'wb')
    
    def test_download_file_invalid_url_raises_value_error(self):
        """Test that invalid URL raises ValueError"""
        with pytest.raises(ValueError, match="URL must be a non-empty string"):
            download_file('')
        
        with pytest.raises(ValueError, match="URL must be a non-empty string"):
            download_file(None)
    
    def test_download_file_invalid_chunk_size_raises_value_error(self):
        """Test that invalid chunk size raises ValueError"""
        with pytest.raises(ValueError, match="Chunk size must be positive"):
            download_file('https://example.com/test.txt', chunk_size=0)
        
        with pytest.raises(ValueError, match="Chunk size must be positive"):
            download_file('https://example.com/test.txt', chunk_size=-1)
    
    def test_download_file_http_error_raises_request_exception(self):
        """Test that HTTP errors are properly raised"""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        
        with patch('requests.get', return_value=mock_response):
            with pytest.raises(requests.exceptions.HTTPError):
                download_file('https://example.com/nonexistent.txt')
    
    def test_download_file_connection_error_raises_request_exception(self):
        """Test that connection errors are properly raised"""
        with patch('requests.get', side_effect=requests.exceptions.ConnectionError("Connection failed")):
            with pytest.raises(requests.exceptions.ConnectionError):
                download_file('https://invalid-domain.com/test.txt')
    
    def test_download_file_io_error_raises_io_error(self):
        """Test that file I/O errors are properly raised"""
        mock_response = Mock()
        mock_response.headers = {'content-length': '100'}
        mock_response.iter_content.return_value = [b'test content']
        mock_response.raise_for_status.return_value = None
        
        with patch('requests.get', return_value=mock_response),              patch('builtins.open', side_effect=IOError("Permission denied")),              patch('pathlib.Path.mkdir'):
            
            with pytest.raises(IOError):
                download_file('https://example.com/test.txt', 'readonly/test.txt')
    
    def test_download_file_creates_directory_structure(self):
        """Test that directory structure is created when needed"""
        mock_response = Mock()
        mock_response.headers = {'content-length': '50'}
        mock_response.iter_content.return_value = [b'content']
        mock_response.raise_for_status.return_value = None
        
        with patch('requests.get', return_value=mock_response),              patch('builtins.open', mock_open()),              patch('pathlib.Path.mkdir') as mock_mkdir:
            
            download_file('https://example.com/test.txt', 'subdir/test.txt')
            
            mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
    
    def test_download_file_progress_display_for_large_files(self):
        """Test progress display for files larger than 1MB"""
        mock_response = Mock()
        # Set content-length to > 1MB
        mock_response.headers = {'content-length': str(2 * 1024 * 1024)}
        mock_response.iter_content.return_value = [b'x' * (1024 * 1024), b'x' * (1024 * 1024)]
        mock_response.raise_for_status.return_value = None
        
        with patch('requests.get', return_value=mock_response),              patch('builtins.open', mock_open()),              patch('pathlib.Path.mkdir'),              patch('builtins.print') as mock_print:
            
            download_file('https://example.com/large_file.zip')
            
            # Verify progress was printed
            progress_calls = [call for call in mock_print.call_args_list 
                            if 'Progress:' in str(call)]
            assert len(progress_calls) > 0
    
    def test_download_file_with_custom_chunk_size(self):
        """Test downloading with custom chunk size"""
        mock_response = Mock()
        mock_response.headers = {'content-length': '100'}
        mock_response.iter_content.return_value = [b'chunk1', b'chunk2']
        mock_response.raise_for_status.return_value = None
        
        with patch('requests.get', return_value=mock_response) as mock_get,              patch('builtins.open', mock_open()),              patch('pathlib.Path.mkdir'):
            
            download_file('https://example.com/test.txt', chunk_size=4096)
            
            # Verify iter_content was called with custom chunk size
            mock_response.iter_content.assert_called_once_with(chunk_size=4096)


class TestIntegration:
    """Integration tests with real HTTP requests (optional, can be skipped in CI)"""
    
    @pytest.mark.integration
    def test_real_download_small_file(self):
        """Test downloading a real small file from httpbin.org"""
        with tempfile.TemporaryDirectory() as temp_dir:
            destination = os.path.join(temp_dir, 'test.json')
            
            try:
                result = download_file('https://httpbin.org/json', destination)
                
                assert result == destination
                assert os.path.exists(destination)
                assert os.path.getsize(destination) > 0
                
                # Verify it's valid JSON
                with open(destination, 'r') as f:
                    content = f.read()
                    assert 'slideshow' in content or 'args' in content
                    
            except requests.exceptions.RequestException:
                pytest.skip("Network unavailable for integration test")


class TestMainFunction:
    """Test cases for the main function"""
    
    def test_main_function_choice_1_valid_url(self):
        """Test main function with choice 1 and valid URL"""
        from download_file import main
        
        mock_response = Mock()
        mock_response.headers = {'content-length': '50'}
        mock_response.iter_content.return_value = [b'content']
        mock_response.raise_for_status.return_value = None
        
        inputs = ['1', 'https://example.com/test.txt', 'output.txt', '3']
        
        with patch('builtins.input', side_effect=inputs),              patch('requests.get', return_value=mock_response),              patch('builtins.open', mock_open()),              patch('pathlib.Path.mkdir'),              patch('builtins.print'):
            
            main()
    
    def test_main_function_choice_1_empty_url(self):
        """Test main function with choice 1 and empty URL"""
        from download_file import main
        
        inputs = ['1', '', '3']
        
        with patch('builtins.input', side_effect=inputs),              patch('builtins.print') as mock_print:
            
            main()
            
            # Check that "Invalid URL" was printed
            print_calls = [str(call) for call in mock_print.call_args_list]
            assert any("Invalid URL" in call for call in print_calls)
    
    def test_main_function_choice_1_download_exception(self):
        """Test main function with choice 1 and download exception"""
        from download_file import main
        
        inputs = ['1', 'https://example.com/test.txt', '', '3']
        
        with patch('builtins.input', side_effect=inputs),              patch('requests.get', side_effect=requests.exceptions.ConnectionError("Network error")),              patch('builtins.print') as mock_print:
            
            main()
            
            # Check that download failed message was printed
            print_calls = [str(call) for call in mock_print.call_args_list]
            assert any("Download failed" in call for call in print_calls)
    
    def test_main_function_choice_2_test_urls(self):
        """Test main function with choice 2 (test URLs)"""
        from download_file import main
        
        mock_response = Mock()
        mock_response.headers = {'content-length': '100'}
        mock_response.iter_content.return_value = [b'test content']
        mock_response.raise_for_status.return_value = None
        
        inputs = ['2', '3']
        
        with patch('builtins.input', side_effect=inputs),              patch('requests.get', return_value=mock_response),              patch('builtins.open', mock_open()),              patch('pathlib.Path.mkdir'),              patch('builtins.print'):
            
            main()
    
    def test_main_function_choice_2_with_exception(self):
        """Test main function with choice 2 and download exception"""
        from download_file import main
        
        inputs = ['2', '3']
        
        with patch('builtins.input', side_effect=inputs),              patch('requests.get', side_effect=requests.exceptions.HTTPError("404 Not Found")),              patch('builtins.print') as mock_print:
            
            main()
            
            # Check that test failed message was printed
            print_calls = [str(call) for call in mock_print.call_args_list]
            assert any("failed" in call for call in print_calls)
    
    def test_main_function_choice_3_exit(self):
        """Test main function with choice 3 (exit)"""
        from download_file import main
        
        inputs = ['3']
        
        with patch('builtins.input', side_effect=inputs),              patch('builtins.print') as mock_print:
            
            main()
            
            # Check that goodbye message was printed
            print_calls = [str(call) for call in mock_print.call_args_list]
            assert any("Goodbye!" in call for call in print_calls)
    
    def test_main_function_invalid_choice(self):
        """Test main function with invalid choice"""
        from download_file import main
        
        inputs = ['invalid', '3']
        
        with patch('builtins.input', side_effect=inputs),              patch('builtins.print') as mock_print:
            
            main()
            
            # Check that invalid choice message was printed
            print_calls = [str(call) for call in mock_print.call_args_list]
            assert any("Invalid choice" in call for call in print_calls)
