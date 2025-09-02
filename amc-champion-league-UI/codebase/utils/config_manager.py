import configparser
import os
from typing import Dict, Any, Optional, List

class ConfigManager:
    _instance = None
    _config = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self):
        """Load configuration from the config file"""
        config_file = os.path.join(os.path.dirname(__file__), "..", "config", "config.ini")
        self._config = configparser.ConfigParser()
        self._config.read(config_file)
        
        # Override with environment variables if present
        for section in self._config.sections():
            for key in self._config[section]:
                env_key = f"{section.upper()}_{key.upper()}"
                if env_key in os.environ:
                    self._config[section][key] = os.environ[env_key]
    
    def get_database_url(self) -> str:
        """Get database URL with fallback to SQLite if not configured"""
        if not self._config.has_section("database"):
            return "sqlite:///amc_champion_league.db"
        
        db_url = self._config.get("database", "db_url", fallback=None)
        if not db_url:
            # Get SQLite URL
            return self._config.get("database", "sqlite_url", fallback="sqlite:///amc_champion_league.db")
        return db_url
    
    def get_storage_config(self) -> Dict[str, Any]:
        """Get storage configuration"""
        if not self._config.has_section("storage"):
            return {
                "use_s3": False,
                "s3_bucket_name": "amc-champion-league",
                "s3_region": "us-east-1",
                "local_image_dir": "./images"
            }
        
        return {
            "use_s3": self._config.getboolean("storage", "use_s3", fallback=False),
            "s3_bucket_name": self._config.get("storage", "s3_bucket_name", fallback="amc-champion-league"),
            "s3_region": self._config.get("storage", "s3_region", fallback="us-east-1"),
            "local_image_dir": self._config.get("storage", "local_image_dir", fallback="./images")
        }
    
    def get_application_config(self) -> Dict[str, Any]:
        """Get application configuration"""
        if not self._config.has_section("application"):
            return {
                "debug": True,
                "host": "0.0.0.0",
                "port": 8000,
                "log_level": "INFO"
            }
        
        return {
            "debug": self._config.getboolean("application", "debug", fallback=True),
            "host": self._config.get("application", "host", fallback="0.0.0.0"),
            "port": self._config.getint("application", "port", fallback=8000),
            "log_level": self._config.get("application", "log_level", fallback="INFO")
        }
    
    def get_supported_games(self) -> List[str]:
        """Get list of supported games"""
        if not self._config.has_section("games"):
            return [
                "Badminton", "Table Tennis", "Pool", "Carom", 
                "Pickle ball", "Chess", "Box Cricket", "Foosball"
            ]
        
        games_str = self._config.get("games", "supported_games", fallback="")
        if not games_str:
            return []
        return [game.strip() for game in games_str.split(",")]
    
    def get_default_win_points(self) -> int:
        """Get default points for winning a match"""
        if not self._config.has_section("scoring"):
            return 10
        return self._config.getint("scoring", "default_win_points", fallback=10)
    
    def get(self, section: str, key: str, fallback: Any = None) -> Any:
        """Get a specific config value"""
        if not self._config.has_section(section):
            return fallback
        return self._config.get(section, key, fallback=fallback)

# Create a singleton instance
config = ConfigManager()
