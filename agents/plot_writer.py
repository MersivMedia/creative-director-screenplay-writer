from . import BaseAgent
from typing import Dict, Any

class PlotWriter(BaseAgent):
    def __init__(self):
        super().__init__(name="PlotWriter", role="Plot Developer")
        
    def execute(self, story_idea: str, characters: str, creative_direction: str) -> str:
        """Generate plot based on story idea, characters, and creative direction"""
        messages = [
            {
                "role": "system",
                "content": """You are a plot writer for screenplays. Create engaging and well-structured plots that include:
                
                - A compelling synopsis
                - Clear three-act structure
                - Major plot points and turning points
                - Character arcs and development
                - Subplots and their integration
                - Theme development
                - Conflict escalation and resolution
                
                Format your response with clear sections and ensure the plot fits within the given time constraints."""
            },
            {
                "role": "user",
                "content": f"""Develop a detailed plot based on:

                Story Idea:
                {story_idea}

                Characters:
                {characters}

                Creative Direction:
                {creative_direction}

                Create a plot that effectively utilizes these characters and follows the creative direction.
                Make sure each character's arc is meaningful and contributes to the overall story."""
            }
        ]
        
        return self.get_completion(messages) 