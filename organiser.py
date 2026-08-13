"""
File Organiser Tool
--------------------
Watches a target folder and automatically sorts files into
subfolders based on their file extension. Rules are loaded
from a JSON config file so they're easy to change without
touching the code.
"""

import os
import shutil
import json
import logging
from datetime import datetime


class FileOrganiser:
    def __init__(self, target_folder: str, config_path: str = "config.json"):
        self.target_folder = target_folder
        self.config_path = config_path
        self.rules = self._load_config()
        self._setup_logging()

    def _load_config(self) -> dict:
        """Load extension -> folder mapping from a JSON file."""
        if not os.path.exists(self.config_path):
            # Create a default config if none exists
            default_rules = {
                ".pdf": "Documents",
                ".docx": "Documents",
                ".txt": "Documents",
                ".jpg": "Images",
                ".jpeg": "Images",
                ".png": "Images",
                ".zip": "Archives",
                ".rar": "Archives",
                ".mp3": "Audio",
                ".mp4": "Video",
            }
            with open(self.config_path, "w") as f:
                json.dump(default_rules, f, indent=4)
            return default_rules

        with open(self.config_path, "r") as f:
            return json.load(f)

    def _setup_logging(self):
        """Configure logging to write to a file with timestamps."""
        logging.basicConfig(
            filename="organiser.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        self.logger = logging.getLogger(__name__)

    def _get_destination_folder(self, extension: str) -> str:
        """Return the folder name a given extension should go into."""
        return self.rules.get(extension.lower(), "Other")

    def organise(self):
        """Main method: scan the target folder and sort every file."""
        if not os.path.exists(self.target_folder):
            self.logger.error(f"Target folder does not exist: {self.target_folder}")
            print(f"Error: folder not found -> {self.target_folder}")
            return

        moved_count = 0

        for filename in os.listdir(self.target_folder):
            file_path = os.path.join(self.target_folder, filename)

            # Skip folders and skip the config/log files themselves
            if os.path.isdir(file_path):
                continue
            if filename in (self.config_path, "organiser.log"):
                continue

            extension = os.path.splitext(filename)[1]
            destination_folder_name = self._get_destination_folder(extension)
            destination_folder_path = os.path.join(
                self.target_folder, destination_folder_name
            )

            try:
                os.makedirs(destination_folder_path, exist_ok=True)
                destination_file_path = os.path.join(destination_folder_path, filename)

                # Avoid overwriting a file that already exists there
                if os.path.exists(destination_file_path):
                    self.logger.warning(
                        f"Skipped (already exists at destination): {filename}"
                    )
                    continue

                shutil.move(file_path, destination_file_path)
                self.logger.info(f"Moved: {filename} -> {destination_folder_name}/")
                moved_count += 1

            except PermissionError:
                self.logger.error(f"Permission denied: {filename}")
            except Exception as e:
                self.logger.error(f"Failed to move {filename}: {e}")

        summary = f"Done. {moved_count} file(s) organised at {datetime.now()}"
        self.logger.info(summary)
        print(summary)


if __name__ == "__main__":
    # Change this to whichever folder you want to organise
    TARGET_FOLDER = r"C:\Users\YourUsername\Downloads"

    organiser = FileOrganiser(target_folder=TARGET_FOLDER)
    organiser.organise()
