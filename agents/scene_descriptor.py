from . import BaseAgent
from typing import Dict, Any

class SceneDescriptor(BaseAgent):
    def __init__(self):
        super().__init__(name="SceneDescriptor", role="Scene Developer")
        
    def execute(self, plot: str, characters: str, creative_direction: str) -> str:
        """Generate scene descriptions based on plot, characters, and creative direction"""
        messages = [
            {
                "role": "system",
                "content": """You are a scene writer for screenplays. Break down the plot into detailed, vivid scenes that include:
                
                - Scene number and setting description
                - Time of day and atmosphere
                - Character presence and positioning
                - Action descriptions
                - Key dialogue points and emotional beats
                - Visual elements and cinematography notes
                - Scene transitions
                
                Format each scene clearly with numbered sections and ensure smooth flow between scenes.
                Focus on showing rather than telling, using vivid sensory details."""
            },
            {
                "role": "user",
                "content": f"""Break down this story into detailed scenes based on:

                Plot:
                {plot}

                Characters:
                {characters}

                Creative Direction:
                {creative_direction}

                Create a sequence of scenes that brings the story to life visually and emotionally.
                Each scene should advance the plot while revealing character and theme.
                Remember to vary the pacing and emotional intensity across scenes."""
            }
        ]
        
        return self.get_completion(messages) 