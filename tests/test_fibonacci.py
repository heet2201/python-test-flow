"""
Comprehensive unit tests for the Fibonacci module.

This module contains extensive tests for all Fibonacci functions including
normal cases, edge cases, and error conditions to ensure >80% test coverage.
"""

import pytest
from src.fibonacci import fibonacci, fibonacci_sequence, is_fibonacci_number


class TestFibonacci:
    """Test cases for the fibonacci function."""
    
    def test_fibonacci_base_cases(self):
        """Test base cases for Fibonacci sequence."""
        assert fibonacci(0) == 0
        assert fibonacci(1) == 1
    
    def test_fibonacci_small_numbers(self):
        """Test Fibonacci calculation for small numbers."""
        assert fibonacci(2) == 1
        assert fibonacci(3) == 2
        assert fibonacci(4) == 3
        assert fibonacci(5) == 5
        assert fibonacci(6) == 8
        assert fibonacci(7) == 13
        assert fibonacci(8) == 21
        assert fibonacci(9) == 34
        assert fibonacci(10) == 55
    
    def test_fibonacci_larger_numbers(self):
        """Test Fibonacci calculation for larger numbers."""
        assert fibonacci(15) == 610
        assert fibonacci(20) == 6765
        assert fibonacci(25) == 75025
        assert fibonacci(30) == 832040
    
    def test_fibonacci_type_error(self):
        """Test TypeError for non-integer inputs."""
        with pytest.raises(TypeError, match="Expected integer, got"):
            fibonacci(3.14)
        
        with pytest.raises(TypeError, match="Expected integer, got"):
            fibonacci("5")
        
        with pytest.raises(TypeError, match="Expected integer, got"):
            fibonacci([1, 2, 3])
        
        with pytest.raises(TypeError, match="Expected integer, got"):
            fibonacci(None)
    
    def test_fibonacci_value_error(self):
        """Test ValueError for negative inputs."""
        with pytest.raises(ValueError, match="Fibonacci number position must be non-negative"):
            fibonacci(-1)
        
        with pytest.raises(ValueError, match="Fibonacci number position must be non-negative"):
            fibonacci(-10)
        
        with pytest.raises(ValueError, match="Fibonacci number position must be non-negative"):
            fibonacci(-100)
    
    def test_fibonacci_overflow_error(self):
        """Test OverflowError for excessively large inputs."""
        with pytest.raises(OverflowError, match="Position too large"):
            fibonacci(1001)
        
        with pytest.raises(OverflowError, match="Position too large"):
            fibonacci(5000)
    
    def test_fibonacci_boundary_values(self):
        """Test boundary values."""
        assert fibonacci(1000) > 0  # Should work at the boundary
        
        # Test just below the boundary
        assert fibonacci(999) > 0


class TestFibonacciSequence:
    """Test cases for the fibonacci_sequence function."""
    
    def test_fibonacci_sequence_small(self):
        """Test small Fibonacci sequences."""
        assert fibonacci_sequence(1) == [0]
        assert fibonacci_sequence(2) == [0, 1]
        assert fibonacci_sequence(3) == [0, 1, 1]
        assert fibonacci_sequence(5) == [0, 1, 1, 2, 3]
        assert fibonacci_sequence(10) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    
    def test_fibonacci_sequence_larger(self):
        """Test larger Fibonacci sequences."""
        seq_15 = fibonacci_sequence(15)
        assert len(seq_15) == 15
        assert seq_15[0] == 0
        assert seq_15[1] == 1
        assert seq_15[-1] == fibonacci(14)  # Last element should be F(14)
    
    def test_fibonacci_sequence_type_error(self):
        """Test TypeError for non-integer inputs."""
        with pytest.raises(TypeError, match="Expected integer, got"):
            fibonacci_sequence(5.5)
        
        with pytest.raises(TypeError, match="Expected integer, got"):
            fibonacci_sequence("10")
        
        with pytest.raises(TypeError, match="Expected integer, got"):
            fibonacci_sequence([5])
    
    def test_fibonacci_sequence_value_error(self):
        """Test ValueError for non-positive inputs."""
        with pytest.raises(ValueError, match="Length must be positive"):
            fibonacci_sequence(0)
        
        with pytest.raises(ValueError, match="Length must be positive"):
            fibonacci_sequence(-1)
        
        with pytest.raises(ValueError, match="Length must be positive"):
            fibonacci_sequence(-10)
    
    def test_fibonacci_sequence_overflow_error(self):
        """Test OverflowError for excessively large inputs."""
        with pytest.raises(OverflowError, match="Length too large"):
            fibonacci_sequence(1001)
        
        with pytest.raises(OverflowError, match="Length too large"):
            fibonacci_sequence(2000)
    
    def test_fibonacci_sequence_boundary(self):
        """Test boundary values for sequence generation."""
        seq = fibonacci_sequence(1000)
        assert len(seq) == 1000
        assert seq[0] == 0
        assert seq[1] == 1


class TestIsFibonacciNumber:
    """Test cases for the is_fibonacci_number function."""
    
    def test_is_fibonacci_number_true_cases(self):
        """Test cases where the number is a Fibonacci number."""
        fibonacci_numbers = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987]
        
        for num in fibonacci_numbers:
            assert is_fibonacci_number(num) is True, f"{num} should be a Fibonacci number"
    
    def test_is_fibonacci_number_false_cases(self):
        """Test cases where the number is not a Fibonacci number."""
        non_fibonacci_numbers = [4, 6, 7, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 22]
        
        for num in non_fibonacci_numbers:
            assert is_fibonacci_number(num) is False, f"{num} should not be a Fibonacci number"
    
    def test_is_fibonacci_number_large_values(self):
        """Test with larger Fibonacci and non-Fibonacci numbers."""
        # Large Fibonacci numbers
        assert is_fibonacci_number(1597) is True
        assert is_fibonacci_number(2584) is True
        assert is_fibonacci_number(4181) is True
        
        # Large non-Fibonacci numbers
        assert is_fibonacci_number(1000) is False
        assert is_fibonacci_number(2000) is False
        assert is_fibonacci_number(3000) is False
    
    def test_is_fibonacci_number_type_error(self):
        """Test TypeError for non-integer inputs."""
        with pytest.raises(TypeError, match="Expected integer, got"):
            is_fibonacci_number(5.5)
        
        with pytest.raises(TypeError, match="Expected integer, got"):
            is_fibonacci_number("13")
        
        with pytest.raises(TypeError, match="Expected integer, got"):
            is_fibonacci_number([8])
        
        with pytest.raises(TypeError, match="Expected integer, got"):
            is_fibonacci_number(None)
    
    def test_is_fibonacci_number_value_error(self):
        """Test ValueError for negative inputs."""
        with pytest.raises(ValueError, match="Number must be non-negative"):
            is_fibonacci_number(-1)
        
        with pytest.raises(ValueError, match="Number must be non-negative"):
            is_fibonacci_number(-5)
        
        with pytest.raises(ValueError, match="Number must be non-negative"):
            is_fibonacci_number(-100)


class TestIntegration:
    """Integration tests combining multiple functions."""
    
    def test_sequence_and_individual_calculation_consistency(self):
        """Test that fibonacci_sequence and individual fibonacci calls are consistent."""
        length = 20
        sequence = fibonacci_sequence(length)
        
        for i in range(length):
            assert sequence[i] == fibonacci(i), f"Mismatch at position {i}"
    
    def test_is_fibonacci_with_generated_sequence(self):
        """Test is_fibonacci_number with numbers from generated sequence."""
        sequence = fibonacci_sequence(15)
        
        for num in sequence:
            assert is_fibonacci_number(num) is True, f"{num} from sequence should be Fibonacci"
    
    def test_performance_boundary(self):
        """Test performance at boundary conditions."""
        # This should complete without timeout
        result = fibonacci(1000)
        assert result > 0
        
        # Sequence generation should also complete
        seq = fibonacci_sequence(100)
        assert len(seq) == 100


# Parametrized tests for comprehensive coverage
class TestParametrized:
    """Parametrized tests for comprehensive coverage."""
    
    @pytest.mark.parametrize("n,expected", [
        (0, 0), (1, 1), (2, 1), (3, 2), (4, 3), (5, 5),
        (6, 8), (7, 13), (8, 21), (9, 34), (10, 55),
        (11, 89), (12, 144), (13, 233), (14, 377), (15, 610)
    ])
    def test_fibonacci_parametrized(self, n, expected):
        """Parametrized test for Fibonacci calculations."""
        assert fibonacci(n) == expected
    
    @pytest.mark.parametrize("invalid_input", [
        3.14, "5", [1, 2, 3], {"key": "value"}, None, complex(1, 2)
    ])
    def test_fibonacci_invalid_types_parametrized(self, invalid_input):
        """Parametrized test for invalid input types."""
        with pytest.raises(TypeError):
            fibonacci(invalid_input)
    
    @pytest.mark.parametrize("negative_input", [-1, -5, -10, -100, -1000])
    def test_fibonacci_negative_values_parametrized(self, negative_input):
        """Parametrized test for negative input values."""
        with pytest.raises(ValueError):
            fibonacci(negative_input)
    
    @pytest.mark.parametrize("fib_num", [0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144])
    def test_is_fibonacci_true_parametrized(self, fib_num):
        """Parametrized test for valid Fibonacci numbers."""
        assert is_fibonacci_number(fib_num) is True
    
    @pytest.mark.parametrize("non_fib_num", [4, 6, 7, 9, 10, 11, 12, 14, 15, 16])
    def test_is_fibonacci_false_parametrized(self, non_fib_num):
        """Parametrized test for non-Fibonacci numbers."""
        assert is_fibonacci_number(non_fib_num) is False
