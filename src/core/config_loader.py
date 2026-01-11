"""
Configuration management for ComplianceGuard
"""

import yaml
import os
from typing import Dict, Any
from pathlib import Path


class ConfigLoader:
    """Loads and validates configuration from YAML file"""
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize configuration loader
        
        Args:
            config_path: Path to configuration YAML file
        """
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        return config
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by dot-notation key
        
        Args:
            key: Configuration key (e.g., 'scanning.frameworks')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value
    
    def get_scanning_config(self) -> Dict:
        """Get scanning configuration section"""
        return self.config.get('scanning', {})
    
    def get_reporting_config(self) -> Dict:
        """Get reporting configuration section"""
        return self.config.get('reporting', {})
    
    def get_scoring_config(self) -> Dict:
        """Get scoring configuration section"""
        return self.config.get('scoring', {})


if __name__ == "__main__":
    # Test configuration loader
    config = ConfigLoader()
    print("Configuration loaded successfully")
    print(f"Frameworks: {config.get('scanning.frameworks')}")
    print(f"Report formats: {config.get('reporting.formats')}")
