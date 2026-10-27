"""Configuration module for GrowthOS."""

class Settings:
    """Application settings."""
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
