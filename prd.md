1. Overview
You will build a Python-based application that guides a user through creating a screenplay, step by step. The application leverages:

Autogen2 for coordinating multiple agents.
OpenAI for text generation, utilizing structured output (JSON) responses.
A single Streamlit interface where the user can:
Input a story concept and desired film length.
View real-time logs of agent conversations (both in the backend console and in a frontend “console” panel).
See the final structured screenplay.
Key Features
Single-page UI (Screenwriting): All screenwriting interactions occur in one interface panel.
Agents:
Director: Oversees the creative direction and coordinates the entire pipeline.
Screenwriter: Consolidates all structured outputs from other agents into a coherent screenplay script.
CharacterWriter: Provides character details (appearance, motivations, history, mannerisms).
PlotWriter: Crafts plot lines and story arcs.
SceneDescriptor: Breaks down the story into scenes with visual details.
TimeStamper: Estimates time durations for each scene or shot.
ImagePrompter: Creates image prompts for each scene.
Structured Output: The final screenplay is a JSON object conforming to a specified schema (including all agent contributions).
Film Length Input: User specifies a length (minutes up to 15). This influences scene pacing and timestamps.
Logging: Agent messages and debug logs appear:
In the backend console (for developers).
In a scrollable log panel on the front end (for end users).
Deployable on a DigitalOcean Droplet or similar environment running Python 3.9.
2. Architecture
Below is a simplified high-level view of the system:

mermaid
Copy code
flowchart LR
    A[User: Story Idea + Film Length] -->|Streamlit UI| B[Director]
    B --> CW[CharacterWriter]
    B --> PW[PlotWriter]
    B --> SD[SceneDescriptor]
    B --> TS[TimeStamper]
    B --> IP[ImagePrompter]
    B --> SW[Screenwriter]
    SW -->|Final JSON| C[UI Output]
    C -->|Logs| D[Console & UI Logs]
Director orchestrates the workflow by calling sub-agents in turn:
CharacterWriter → Generate character details
PlotWriter → Outline plot arcs
SceneDescriptor → Create scene-by-scene breakdown
TimeStamper → Estimate durations per scene
ImagePrompter → Generate prompts for each scene’s imagery
Screenwriter → Gathers all sub-agent outputs into a final screenplay JSON
Streamlit UI calls the Director agent to initiate or re-run the pipeline.
All logs from each agent’s interactions appear in both the server console and a front-end “console log” section.
3. Agents & Responsibilities
Director

Role: High-level controller, receives user input (story idea, desired length) and coordinates all sub-agents.
Key Tasks:
Receives message from the UI with {"action": "start_screenwriting", "story_idea": ..., "length_minutes": ...}
Invokes sub-agents in the correct order.
Collects partial JSON outputs and passes them to the Screenwriter.
CharacterWriter

Role: Based on the story idea and direction from the Director, creates a JSON array of characters.
Structured Output Example:
json
Copy code
{
  "characters": [
    {
      "name": "Alice",
      "physical_description": "...",
      "motivations": "...",
      "history": "...",
      "mannerisms": "..."
    }
    ...
  ]
}
PlotWriter

Role: Crafts the narrative arc, major conflicts, and resolutions.
Structured Output Example:
json
Copy code
{
  "plot": {
    "synopsis": "...",
    "major_events": [
      "Event1",
      "Event2"
    ]
  }
}
SceneDescriptor

Role: Breaks the plot into scenes, describing the setting, key actions, atmosphere, etc.
Structured Output Example:
json
Copy code
{
  "scenes": [
    {
      "scene_number": 1,
      "setting": "...",
      "action": "Characters discuss plan...",
      "dialogue_summary": "...",
      "visuals": "Dimly lit room..."
    },
    ...
  ]
}
TimeStamper

Role: Based on the plot, scene count, and user’s desired film length (up to 15 min), estimates timestamps for each scene.
Structured Output Example:
json
Copy code
{
  "timestamps": [
    {
      "scene_number": 1,
      "start_time": "00:00",
      "end_time": "01:30"
    },
    ...
  ]
}
ImagePrompter

Role: Creates textual prompts that could be used to generate images for each scene (but does not generate images).
Structured Output Example:
json
Copy code
{
  "scene_prompts": [
    {
      "scene_number": 1,
      "prompt": "Cinematic shot of a dimly lit room..."
    },
    ...
  ]
}
Screenwriter

Role: Consolidates all partial JSONs (characters, plot, scenes, timestamps, image prompts) into a final Screenplay JSON.
Structured Output Example (final screenplay):
json
Copy code
{
  "title": "Example Film",
  "length_minutes": 15,
  "characters": [...],
  "plot": {...},
  "scenes": [...],
  "timestamps": [...],
  "scene_prompts": [...],
  "final_script_text": "Combined script text or summary if needed."
}
Each agent will leverage OpenAI with structured output to produce these JSON responses.
(See OpenAI’s structured output documentation for details.)

4. Tech Stack & Dependencies
The application is designed for Python 3.9 to ensure compatibility. Required dependencies (pinned versions provided):

autogen2 (>=0.2.0) – For building multi-agent flows.
openai (>=1.58.0) – LLM calls with structured outputs.
flaml[automl] (>=1.2.8) – Optional if used by autogen2 for certain tasks.
streamlit (==1.29.0) – Single-tab user interface.
python-dotenv (==1.0.0) – Manage environment variables.
requests (==2.31.0) – For HTTP calls.
sqlalchemy (==2.0.23) – If needed for DB interactions.
pillow (>=8.3.2,<10.1.0) – Image library if needed for any basic image processing.
numpy (==1.24.3) – Numerical computations if needed.
decorator (==4.4.2) – Required by some libraries.
proglog (==0.1.10) – Logging support for some generative tasks if required.
tqdm (==4.66.1) – Progress bar in console logs.
Example requirements.txt:

makefile
Copy code
openai>=1.58.0
autogen>=0.2.0
flaml[automl]>=1.2.8
streamlit==1.29.0
python-dotenv==1.0.0
requests==2.31.0
sqlalchemy==2.0.23
pillow>=8.3.2,<10.1.0
numpy==1.24.3
decorator==4.4.2
proglog==0.1.10
tqdm==4.66.1
5. Project Structure
A simplified directory structure:

arduino
Copy code
my-screenwriter-app/
  ├─ agents/
  │   ├─ __init__.py
  │   ├─ director.py
  │   ├─ character_writer.py
  │   ├─ plot_writer.py
  │   ├─ scene_descriptor.py
  │   ├─ time_stamper.py
  │   ├─ image_prompter.py
  │   └─ screenwriter.py
  ├─ services/
  │   ├─ openai_service.py
  │   └─ ...
  ├─ main.py
  ├─ requirements.txt
  ├─ run.sh
  └─ .env
Where:

agents/ houses each agent’s class definition.
services/ might hold wrappers around OpenAI or DB logic.
main.py runs the Streamlit server, orchestrates the UI → Director agent flow.
run.sh script to create/activate a Python 3.9 virtual environment, install dependencies, and start the app.
6. JSON Schema Examples
6.1. Final Screenplay Schema (High-Level)
jsonc
Copy code
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Screenplay",
  "type": "object",
  "properties": {
    "title": { "type": "string" },
    "length_minutes": { "type": "number" },
    "characters": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {"type": "string"},
          "physical_description": {"type": "string"},
          "motivations": {"type": "string"},
          "history": {"type": "string"},
          "mannerisms": {"type": "string"}
        },
        "required": ["name", "physical_description"]
      }
    },
    "plot": {
      "type": "object",
      "properties": {
        "synopsis": {"type": "string"},
        "major_events": {
          "type": "array",
          "items": {"type": "string"}
        }
      },
      "required": ["synopsis"]
    },
    "scenes": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "scene_number": {"type": "number"},
          "setting": {"type": "string"},
          "action": {"type": "string"},
          "dialogue_summary": {"type": "string"},
          "visuals": {"type": "string"}
        },
        "required": ["scene_number", "setting"]
      }
    },
    "timestamps": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "scene_number": {"type": "number"},
          "start_time": {"type": "string"},
          "end_time": {"type": "string"}
        },
        "required": ["scene_number", "start_time"]
      }
    },
    "scene_prompts": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "scene_number": {"type": "number"},
          "prompt": {"type": "string"}
        },
        "required": ["scene_number", "prompt"]
      }
    },
    "final_script_text": {"type": "string"}
  },
  "required": ["title", "length_minutes", "characters", "plot", "scenes", "timestamps"]
}
This schema ensures each element (characters, plot, scenes, etc.) is well-defined and required fields are present.

7. Sample Code Snippets
7.1. Director Agent
python
Copy code
# agents/director.py
from autogen2.core import Agent, Message
from .character_writer import CharacterWriter
from .plot_writer import PlotWriter
from .scene_descriptor import SceneDescriptor
from .time_stamper import TimeStamper
from .image_prompter import ImagePrompter
from .screenwriter import Screenwriter

class Director(Agent):
    def __init__(self):
        super().__init__(name="Director", role="Overseer")
        self.character_writer = CharacterWriter()
        self.plot_writer = PlotWriter()
        self.scene_descriptor = SceneDescriptor()
        self.time_stamper = TimeStamper()
        self.image_prompter = ImagePrompter()
        self.screenwriter = Screenwriter()

    def handle_message(self, message: Message):
        action = message.content.get("action")

        if action == "start_screenwriting":
            story_idea = message.content.get("story_idea")
            length_minutes = message.content.get("length_minutes")

            # 1. Create characters
            characters_json = self.character_writer.execute(story_idea)

            # 2. Write plot
            plot_json = self.plot_writer.execute(story_idea, characters_json)

            # 3. Describe scenes
            scenes_json = self.scene_descriptor.execute(plot_json, characters_json)

            # 4. Estimate timestamps
            timestamps_json = self.time_stamper.execute(scenes_json, length_minutes)

            # 5. Generate image prompts
            image_prompts_json = self.image_prompter.execute(scenes_json)

            # 6. Consolidate final screenplay
            screenplay = self.screenwriter.execute(
                story_idea, length_minutes,
                characters_json, plot_json, scenes_json,
                timestamps_json, image_prompts_json
            )
            return screenplay

        return {"error": "No valid action found."}
7.2. CharacterWriter (Example)
python
Copy code
# agents/character_writer.py
from autogen2.core import Agent

class CharacterWriter(Agent):
    def __init__(self):
        super().__init__(name="CharacterWriter", role="Creating character profiles")

    def execute(self, story_idea: str):
        # Use OpenAI with structured output to return a JSON with "characters" array
        # Below is a mock to illustrate
        response_json = {
            "characters": [
                {
                    "name": "Alex",
                    "physical_description": "Tall, athletic build...",
                    "motivations": "Find the truth about X...",
                    "history": "Grew up in a small town...",
                    "mannerisms": "Often taps foot nervously..."
                }
            ]
        }
        return response_json
7.3. Streamlit Front End (Single Tab)
python
Copy code
# main.py
import streamlit as st
from agents.director import Director

# Real-time log container
if "console_logs" not in st.session_state:
    st.session_state["console_logs"] = []

def log_to_console(msg: str):
    """Utility to log messages in session state (for UI) and also print to backend console."""
    st.session_state["console_logs"].append(msg)
    print(msg)

def show_logs():
    """Display logs in a scrollable text box."""
    logs_text = "\n".join(st.session_state["console_logs"])
    st.text_area("Console Logs", value=logs_text, height=200)

# Instantiate Director
director_agent = Director()

st.title("AI Screenwriting MVP")

story_idea = st.text_area("Enter your story idea:")
length_minutes = st.slider("Desired film length (minutes):", min_value=1, max_value=15, value=10)

if st.button("Generate Screenplay"):
    log_to_console("Starting screenwriting process...")
    screenplay = director_agent.handle_message({
        "content": {
            "action": "start_screenwriting",
            "story_idea": story_idea,
            "length_minutes": length_minutes
        }
    })
    log_to_console(f"Screenplay generated: {screenplay}")

    st.subheader("Structured Screenplay Output")
    st.json(screenplay)

show_logs()
7.4. run.sh (Example Start Script)
bash
Copy code
#!/usr/bin/env bash

# Ensure we're using Python 3.9
python3.9 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

echo "Starting Streamlit app on port 8501..."
streamlit run main.py --server.port 8501
Make the script executable: chmod +x run.sh

Then on your DigitalOcean Droplet (or local), run:

arduino
Copy code
./run.sh
This ensures the correct dependencies, Python version, and starts the Streamlit server.

8. Deployment Notes
DigitalOcean:
You can deploy this as a simple VM (Droplet) or container.
Make sure to install Python 3.9 on the server.
Copy the project files, run run.sh.
Environment Variables:
Store your OpenAI (and any other) API keys in a .env file or pass them via environment variables.
Example .env:
bash
Copy code
OPENAI_API_KEY=sk-xxxxxx
Load with python-dotenv if needed in your code (from dotenv import load_dotenv; load_dotenv()).
Scaling:
For an MVP, one instance is likely sufficient. For heavier usage, you may scale or run behind a reverse proxy.
9. Conclusion
This reduced-scope PRD focuses on screenwriting only, removing more complex post-production (storyboarding, video, audio). The system:

Gathers user input (story idea & desired film length).
Uses multiple Autogen2 agents that produce structured outputs in JSON.
Consolidates everything into a final Screenplay JSON, including:
Character details
Plot outline
Scene descriptions
Timestamps for each scene
Image prompts (just text)
The application is packaged with pinned dependencies, runs on Python 3.9, logs agent communications both in the backend console and a Streamlit front-end, and can be easily deployed to DigitalOcean or similar.