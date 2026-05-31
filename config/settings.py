import os
import yaml

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Settings:

    def __init__(self):

        config_path = os.path.join(os.path.dirname(__file__), "config.yaml")

        with open(config_path, "r") as file:
            self.config = yaml.safe_load(file)

        self._resolve_app_path()

    def _resolve_app_path(self):
    
        caps = self.config["appium"]["capabilities"]

        env_path = os.environ.get("APPIUM_APP")

        if env_path:
            caps["app"] = env_path
        elif not os.path.isabs(caps["app"]):
            caps["app"] = os.path.join(PROJECT_ROOT, caps["app"])


settings = Settings().config