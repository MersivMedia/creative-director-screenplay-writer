import os
import json
import shutil
from datetime import datetime
from pathlib import Path

class DataManager:
    def __init__(self):
        self.data_dir = Path("data")
        self.current_story_dir = None
        self.ensure_data_directory()
    
    def ensure_data_directory(self):
        """Ensure the data directory exists"""
        self.data_dir.mkdir(exist_ok=True)
    
    def create_new_story(self):
        """Create a new story directory"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.current_story_dir = self.data_dir / f"story_{timestamp}"
        self.current_story_dir.mkdir(exist_ok=True)
        return self.current_story_dir
    
    def save_output(self, content: str, filename: str):
        """Save content to a file in the current story directory"""
        if not self.current_story_dir:
            self.create_new_story()
        
        filepath = self.current_story_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return filepath
    
    def create_zip_archive(self) -> str:
        """Create a zip archive of the current story"""
        if not self.current_story_dir:
            raise ValueError("No current story to archive")
        
        zip_path = str(self.current_story_dir) + ".zip"
        shutil.make_archive(str(self.current_story_dir), 'zip', self.current_story_dir)
        return zip_path
    
    def clear_current_story(self):
        """Clear the current story data"""
        if self.current_story_dir and self.current_story_dir.exists():
            shutil.rmtree(self.current_story_dir)
        self.current_story_dir = None 