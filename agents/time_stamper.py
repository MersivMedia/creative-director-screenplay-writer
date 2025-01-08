from . import BaseAgent
from typing import Dict, Any

class TimeStamper(BaseAgent):
    def __init__(self):
        super().__init__(name="TimeStamper", role="Scene Timer")
        
    def execute_single_scene(self, scene_text: str, total_length_minutes: int) -> str:
        """Estimate the duration of a single scene"""
        messages = [
            {
                "role": "system",
                "content": """You are a timing expert for screenplays. Analyze this scene and determine its duration based on:
                
                - Amount and complexity of dialogue
                - Action sequence descriptions
                - Scene transitions
                - Establishing shots
                - Character movements and interactions
                
                Guidelines:
                - Dialogue: ~3 seconds per line
                - Action descriptions: ~5 seconds per line
                - Establishing shots: ~10 seconds
                - Complex action sequences: 5-10 seconds per beat
                - Scene transitions: 5 seconds
                
                Return ONLY the timestamp in MM:SS format."""
            },
            {
                "role": "user",
                "content": f"""Analyze this scene and provide its duration:

                Scene:
                {scene_text}

                Consider all elements and provide a realistic duration that would properly convey all action and dialogue.
                Remember that scenes typically run 30-60 seconds.
                Return ONLY the timestamp (MM:SS)."""
            }
        ]
        
        duration = self.get_completion(messages).strip()
        
        # Validate format and return
        try:
            minutes, seconds = map(int, duration.split(':'))
            return f"{minutes:02d}:{seconds:02d}"
        except:
            return "00:45"  # Default to 45 seconds if format is invalid 