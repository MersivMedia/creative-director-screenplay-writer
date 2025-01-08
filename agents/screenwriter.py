from . import BaseAgent
from typing import Dict, Any

class Screenwriter(BaseAgent):
    def __init__(self):
        super().__init__(name="Screenwriter", role="Final Screenplay Writer")
        
    def execute_scene(self, scene_outline: str, characters: str, creative_direction: str) -> str:
        """Write a detailed scene based on the outline"""
        messages = [
            {
                "role": "system",
                "content": """You are a professional screenwriter. Write a detailed scene that:
                
                - Uses proper screenplay formatting
                - Includes vivid action descriptions
                - Features natural, character-driven dialogue
                - Incorporates specific visual and atmospheric details
                - Maintains consistent character voices
                - Follows standard screenplay conventions
                
                Format your scene with:
                - Scene heading (INT/EXT, LOCATION, TIME)
                - Action paragraphs (present tense, active voice)
                - Character dialogue with parentheticals when needed
                - Proper transitions
                
                Make each scene substantial enough for proper timing (aim for 30-60 seconds of screen time)."""
            },
            {
                "role": "user",
                "content": f"""Write a detailed scene based on this outline:

                Scene Outline:
                {scene_outline}

                Characters:
                {characters}

                Creative Direction:
                {creative_direction}

                Write a substantial scene that brings this moment to life.
                Include detailed action and meaningful dialogue.
                Remember this needs to fill 30-60 seconds of screen time."""
            }
        ]
        
        return self.get_completion(messages)
        
    def execute_additional_scene(
        self,
        plot: str,
        characters: str,
        creative_direction: str,
        current_time: int,
        target_time: int
    ) -> str:
        """Write an additional scene to help reach the target length"""
        remaining_time = target_time - current_time
        
        messages = [
            {
                "role": "system",
                "content": f"""You are a professional screenwriter. Create a new scene that:
                
                - Fits naturally within the existing plot
                - Adds depth to characters or story
                - Can fill approximately {remaining_time//60} minutes of screen time
                - Maintains the established tone and style
                
                The scene should feel essential, not like filler content.
                Focus on character development, subplot exploration, or theme reinforcement."""
            },
            {
                "role": "user",
                "content": f"""Create a new scene that fits within this story:

                Plot:
                {plot}

                Characters:
                {characters}

                Creative Direction:
                {creative_direction}

                Current Runtime: {current_time//60}:{current_time%60:02d}
                Target Runtime: {target_time//60}:{target_time%60:02d}

                Write a substantial scene that adds value to the story while helping reach the target length."""
            }
        ]
        
        return self.get_completion(messages) 