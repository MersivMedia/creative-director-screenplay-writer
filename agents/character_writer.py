from . import BaseAgent
from typing import Dict, Any

class CharacterWriter(BaseAgent):
    def __init__(self):
        super().__init__(name="CharacterWriter", role="Character Developer")
        
    def execute(self, story_idea: str, creative_direction: str) -> str:
        """Generate character details based on story idea and creative direction"""
        messages = [
            {
                "role": "system",
                "content": """You are a character writer for screenplays. Create detailed character profiles 
                that include:
                - Name and basic demographics
                - Physical description
                - Personality traits and mannerisms
                - Background and history
                - Motivations and goals
                - Key relationships
                
                Format each character profile with clear headers and sections."""
            },
            {
                "role": "user",
                "content": f"""Based on this story idea and creative direction, develop the main characters:
                
                Story Idea:
                {story_idea}
                
                Creative Direction:
                {creative_direction}
                
                Please provide detailed character profiles that will bring this story to life."""
            }
        ]
        
        return self.get_completion(messages) 