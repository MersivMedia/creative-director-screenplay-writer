from . import BaseAgent
from typing import Dict, Any

class ImagePrompter(BaseAgent):
    def __init__(self):
        super().__init__(name="ImagePrompter", role="Visual Prompter")
        
    def execute(self, scenes: str) -> str:
        """Generate image prompts for each scene"""
        messages = [
            {
                "role": "system",
                "content": """You are a visual prompt expert for screenplays. Create detailed image prompts that capture:
                
                - Scene composition and framing
                - Lighting and color palette
                - Character positioning and expressions
                - Key visual elements and props
                - Atmosphere and mood
                - Camera angles and movement
                - Special effects or unique visual elements
                
                Format each prompt with:
                - Scene number
                - Primary shot description
                - Key visual elements
                - Mood and atmosphere notes
                - Technical considerations
                
                Make each prompt detailed enough to create a clear mental image while being concise and focused."""
            },
            {
                "role": "user",
                "content": f"""Create detailed visual prompts for these scenes:

                Scenes:
                {scenes}

                For each scene, provide a prompt that would help visualize the key moment or essence of the scene.
                Focus on the most cinematically impactful elements and ensure visual continuity across scenes."""
            }
        ]
        
        return self.get_completion(messages) 