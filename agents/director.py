from . import BaseAgent
from typing import Dict, Any
import os
from pathlib import Path

class Director(BaseAgent):
    def __init__(self):
        super().__init__(name="Director", role="Creative Director and Coordinator")
        self.character_writer = None
        self.plot_writer = None
        self.scene_descriptor = None
        self.time_stamper = None
        self.image_prompter = None
        self.screenwriter = None
        
    def execute(self, story_idea: str, length_minutes: int) -> str:
        """Coordinate the screenplay creation process"""
        # Create scenes directory if it doesn't exist
        scenes_dir = Path("data/current/scenes")
        scenes_dir.mkdir(parents=True, exist_ok=True)
        
        # First, establish creative direction
        self.log_message("Starting creative direction phase...")
        direction_messages = [
            {
                "role": "system", 
                "content": f"""You are a creative film director. Provide creative direction for this story. 
                Include your vision for:
                - Visual style and tone
                - Key themes to emphasize
                - Emotional journey
                - Cinematographic elements
                - Pacing and rhythm
                - Approximate scene count (considering length)
                
                For a {length_minutes} minute film, we need approximately {length_minutes * 2} distinct scenes 
                to maintain proper pacing (roughly 30 seconds per scene on average).
                
                Format your response in clear sections with headers."""
            },
            {
                "role": "user", 
                "content": f"Story idea: {story_idea}\nDesired length: {length_minutes} minutes\n\nProvide detailed creative direction for this film."
            }
        ]
        
        creative_direction = self.get_completion(direction_messages)
        self.log_message("Creative direction established. Moving to character development...")

        # Get character details
        characters = self.character_writer.execute(story_idea, creative_direction)
        self.log_message("Characters developed. Moving to plot development...")

        # Get plot structure
        plot = self.plot_writer.execute(story_idea, characters, creative_direction)
        self.log_message("Plot structure created. Moving to scene breakdown...")

        # Get scene outlines
        scene_outlines = self.scene_descriptor.execute(plot, characters, creative_direction)
        self.log_message("Scene outlines created. Writing detailed scenes...")

        # Write each scene in detail and get timestamps
        scene_files = []
        timestamps = {}
        image_prompts = {}
        
        # Split scene outlines into individual scenes
        scenes = [s.strip() for s in scene_outlines.split('Scene') if s.strip()]
        
        for i, scene_outline in enumerate(scenes, 1):
            self.log_message(f"Writing detailed scene {i}...")
            
            # Get detailed scene from screenwriter
            detailed_scene = self.screenwriter.execute_scene(
                scene_outline,
                characters,
                creative_direction
            )
            
            # Save scene to file
            scene_file = scenes_dir / f"scene_{i:02d}.txt"
            with open(scene_file, 'w', encoding='utf-8') as f:
                f.write(detailed_scene)
            scene_files.append(scene_file)
            
            # Get timestamp for scene
            timestamp = self.time_stamper.execute_single_scene(detailed_scene, length_minutes)
            timestamps[i] = timestamp
            
            # Get image prompt for scene
            image_prompt = self.image_prompter.execute(scene_outline)
            image_prompts[i] = image_prompt
            
            self.log_message(f"Scene {i} completed with timestamp: {timestamp}")

        # Verify total length
        total_seconds = sum([
            sum(int(x) * 60**i for i, x in enumerate(reversed(t.split(':'))))
            for t in timestamps.values()
        ])
        
        while total_seconds < length_minutes * 60 * 0.9:  # Allow 10% margin
            self.log_message(f"Current length: {total_seconds//60}:{total_seconds%60:02d}. Need more content...")
            
            # Add a new scene
            i = len(scene_files) + 1
            new_scene = self.screenwriter.execute_additional_scene(
                plot,
                characters,
                creative_direction,
                total_seconds,
                length_minutes * 60
            )
            
            scene_file = scenes_dir / f"scene_{i:02d}.txt"
            with open(scene_file, 'w', encoding='utf-8') as f:
                f.write(new_scene)
            scene_files.append(scene_file)
            
            timestamp = self.time_stamper.execute_single_scene(new_scene, length_minutes)
            timestamps[i] = timestamp
            
            image_prompt = self.image_prompter.execute(new_scene)
            image_prompts[i] = image_prompt
            
            total_seconds += sum(int(x) * 60**i for i, x in enumerate(reversed(timestamp.split(':'))))
        
        # Compile final screenplay
        self.log_message("Compiling final screenplay...")
        final_screenplay = f"""Title: {story_idea.split()[0:5]}...

Character Descriptions:
{characters}

Plot Description:
{plot}

"""
        
        for i, scene_file in enumerate(scene_files, 1):
            with open(scene_file, 'r', encoding='utf-8') as f:
                scene_text = f.read()
            
            final_screenplay += f"""
Scene {i}: {timestamps[i]}
Image Prompt: {image_prompts[i]}
{scene_text}
"""
        
        self.log_message("Screenplay compilation complete!")
        return final_screenplay 