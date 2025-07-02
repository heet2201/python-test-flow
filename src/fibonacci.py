"""
Fibonacci number calculation module with proper error handling.

This module provides functions to calculate Fibonacci numbers with comprehensive
error handling and input validation.
"""

from typing import Union


def fibonacci(n: int) -> int:
    """
    Calculate the nth Fibonacci number.
    
    The Fibonacci sequence is defined as:
    F(0) = 0
    F(1) = 1
    F(n) = F(n-1) + F(n-2) for n > 1
    
    Args:
        n (int): The position in the Fibonacci sequence (must be non-negative)
        
    Returns:
        int: The nth Fibonacci number
        
    Raises:
        TypeError: If n is not an integer
        ValueError: If n is negative
        OverflowError: If n is too large (> 1000 to prevent excessive computation)
        
    Examples:
        >>> fibonacci(0)
        0
        >>> fibonacci(1)
        1
        >>> fibonacci(10)
        55
        >>> fibonacci(20)
        6765
    """
    # Type validation
    if not isinstance(n, int):
        raise TypeError(f"Expected integer, got {type(n).__name__}")
    
    # Value validation
    if n < 0:
        raise ValueError("Fibonacci number position must be non-negative")
    
    # Prevent excessive computation
    if n > 1000:
        raise OverflowError("Position too large (max 1000 to prevent overflow)")
    
    # Base cases
    if n == 0:
        return 0
    elif n == 1:
        return 1
    
    # Iterative calculation for efficiency
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    
    return b


def fibonacci_sequence(length: int) -> list[int]:
    """
    Generate a list of Fibonacci numbers up to the specified length.
    
    Args:
        length (int): Number of Fibonacci numbers to generate (must be positive)
        
    Returns:
        list[int]: List containing the first 'length' Fibonacci numbers
        
    Raises:
        TypeError: If length is not an integer
        ValueError: If length is not positive
        OverflowError: If length is too large (> 1000)
        
    Examples:
        >>> fibonacci_sequence(5)
        [0, 1, 1, 2, 3]
        >>> fibonacci_sequence(10)
        [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    """
    # Type validation
    if not isinstance(length, int):
        raise TypeError(f"Expected integer, got {type(length).__name__}")
    
    # Value validation
    if length <= 0:
        raise ValueError("Length must be positive")
    
    # Prevent excessive computation
    if length > 1000:
        raise OverflowError("Length too large (max 1000 to prevent overflow)")
    
    # Generate sequence
    sequence = []
    for i in range(length):
        sequence.append(fibonacci(i))
    
    return sequence


def is_fibonacci_number(num: int) -> bool:
    """
    Check if a given number is a Fibonacci number.
    
    A positive integer is a Fibonacci number if and only if one of
    (5*n^2 + 4) or (5*n^2 - 4) is a perfect square.
    
    Args:
        num (int): The number to check (must be non-negative)
        
    Returns:
        bool: True if the number is a Fibonacci number, False otherwise
        
    Raises:
        TypeError: If num is not an integer
        ValueError: If num is negative
        
    Examples:
        >>> is_fibonacci_number(0)
        True
        >>> is_fibonacci_number(1)
        True
        >>> is_fibonacci_number(55)
        True
        >>> is_fibonacci_number(56)
        False
    """
    # Type validation
    if not isinstance(num, int):
        raise TypeError(f"Expected integer, got {type(num).__name__}")
    
    # Value validation
    if num < 0:
        raise ValueError("Number must be non-negative")
    
    # Special case for 0
    if num == 0:
        return True
    
    # Check if (5*n^2 + 4) or (5*n^2 - 4) is a perfect square
    def is_perfect_square(x: int) -> bool:
        if x < 0:
            return False
        root = int(x ** 0.5)
        return root * root == x
    
    return (is_perfect_square(5 * num * num + 4) or 
            is_perfect_square(5 * num * num - 4))
