"""
Configuration file for QKD BB84 Protocol Application

This module provides centralized configuration management for different
environments (development, testing, production).
"""

import os
from typing import Optional


class Config:
    """Base configuration class with shared settings."""
    
    # Flask settings
    DEBUG = False
    TESTING = False
    JSON_SORT_KEYS = False
    
    # QKD settings
    MIN_QUBITS = 10
    MAX_QUBITS = 1000
    DEFAULT_QUBITS = 100
    DEFAULT_MESSAGE = "Hello, Quantum World!"
    
    # Security
    QBER_THRESHOLD = 0.11  # 11% - standard BB84 security bound
    PREVIEW_LENGTH = 20  # Number of items to preview in API responses
    
    # Performance
    MAX_REQUEST_SIZE = 16 * 1024  # 16 KB max request size
    TIMEOUT = 60  # Request timeout in seconds


class DevelopmentConfig(Config):
    """Configuration for development environment."""
    
    DEBUG = True
    TESTING = False
    
    # Flask development settings
    FLASK_ENV = 'development'
    
    # Logging
    LOG_LEVEL = 'DEBUG'
    
    # Allow larger requests in development
    MAX_REQUEST_SIZE = 64 * 1024


class TestingConfig(Config):
    """Configuration for testing environment."""
    
    TESTING = True
    DEBUG = True
    
    # Flask testing settings
    FLASK_ENV = 'testing'
    
    # Logging
    LOG_LEVEL = 'INFO'
    
    # Lower limits for faster tests
    MAX_QUBITS = 500
    DEFAULT_QUBITS = 50


class ProductionConfig(Config):
    """Configuration for production environment."""
    
    DEBUG = False
    TESTING = False
    
    # Flask production settings
    FLASK_ENV = 'production'
    
    # Logging
    LOG_LEVEL = 'WARNING'
    
    # Stricter limits
    MAX_QUBITS = 10000  # Higher for production use
    MAX_REQUEST_SIZE = 8 * 1024  # 8 KB - more restrictive


def get_config(env: Optional[str] = None) -> Config:
    """
    Get configuration object for specified environment.
    
    Args:
        env (str, optional): Environment name ('development', 'testing', 'production').
                           If not provided, uses FLASK_ENV environment variable.
                           Defaults to 'development'.
    
    Returns:
        Config: Configuration object for the specified environment
        
    Example:
        >>> config = get_config('production')
        >>> config.DEBUG
        False
    """
    if env is None:
        env = os.getenv('FLASK_ENV', 'development')
    
    env = env.lower()
    
    if env == 'production':
        return ProductionConfig()
    elif env == 'testing':
        return TestingConfig()
    else:
        return DevelopmentConfig()


# Default configuration instance
config = get_config()
