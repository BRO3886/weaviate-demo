import os
from typing import Any

import yaml
from dotenv import load_dotenv


class AppConfig:
    def __init__(self, config_path: str = None):
        load_dotenv()
        self.env = dict(os.environ)
        self.config = {}
        config_file = config_path or os.environ.get(
            "APP_CONFIG_PATH", "configs/config.yaml"
        )
        if os.path.exists(config_file):
            with open(config_file, "r") as f:
                try:
                    self.config = yaml.safe_load(f) or {}
                except Exception:
                    self.config = {}
        self._initialized = True

    def get(self, key: str, default: Any = None) -> Any:
        # Priority: env > config.yaml > default
        if key in self.env:
            return self.env.get(key)
        value = self._get_nested_config(key)
        if value is not None:
            return value
        return default

    def get_env(self, key: str, default: Any = None) -> Any:
        return self.env.get(key, default)

    def get_config(self, key: str, default: Any = None) -> Any:
        value = self._get_nested_config(key)
        if value is not None:
            return value
        return default

    def _get_nested_config(self, key: str) -> Any:
        keys = key.split(".")
        current = self.config
        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return None
        return current


_config = AppConfig()


def get_config() -> AppConfig:
    return _config
