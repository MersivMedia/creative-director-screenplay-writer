import streamlit as st
from agents.director import Director
from agents.character_writer import CharacterWriter
from agents.plot_writer import PlotWriter
from agents.scene_descriptor import SceneDescriptor
from agents.time_stamper import TimeStamper
from agents.image_prompter import ImagePrompter
from agents.screenwriter import Screenwriter
from services.data_manager import DataManager
import os
import base64

# Custom CSS for terminal-like styling
TERMINAL_STYLE = """
<style>
    /* Force dark theme on header */
    [data-testid="stHeader"] {
        background-color: black !important;
    }
    
    /* Fix main content spacing */
    .main > div:first-child {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    .block-container {
        padding-top: 2rem !important;
        max-width: none !important;
    }
    [data-testid="stSidebarContent"] {
        padding-top: 2rem !important;
    }
    
    /* Remove white backgrounds from Streamlit */
    .stTextArea > label, .stSlider > label {
        color: #00ff00 !important;
    }
    .stTextArea > div, .stSlider > div {
        background-color: black !important;
        color: #00ff00 !important;
        border-color: #00ff00 !important;
    }
    .stTextArea textarea {
        background-color: black !important;
        color: #00ff00 !important;
        border-color: #00ff00 !important;
    }
    .stMarkdown {
        background-color: transparent !important;
        color: #00ff00 !important;
    }
    div[data-testid="stVerticalBlock"] {
        background-color: black !important;
    }
    
    /* Fix any remaining white borders */
    div[data-testid="stDecoration"] {
        background-color: black !important;
        border-color: #00ff00 !important;
    }
    
    div[data-testid="stToolbar"] {
        background-color: black !important;
        border-color: #00ff00 !important;
    }
    
    /* Terminal styling */
    .terminal {
        background-color: black;
        color: #00ff00;
        font-family: 'Courier New', Courier, monospace;
        padding: 20px;
        border-radius: 5px;
        margin: 10px 0;
        height: 500px;
        overflow-y: auto;
        white-space: pre-wrap;
        border: 1px solid #00ff00;
        display: flex;
        flex-direction: column;
    }
    
    #terminal-messages {
        flex-grow: 1;
        overflow-y: auto;
        scroll-behavior: auto;
        -ms-overflow-style: none;
        scrollbar-width: none;
    }
    
    #terminal-messages::-webkit-scrollbar {
        display: none;
    }
    
    .terminal-message {
        margin: 5px 0;
        line-height: 1.3;
        color: #00ff00;
    }
    
    /* Override any white backgrounds in messages */
    .terminal-message pre {
        background-color: black !important;
        border-color: #00ff00 !important;
    }
    
    .terminal-message code {
        background-color: black !important;
        border-color: #00ff00 !important;
    }
    
    /* Fix code block styling */
    .stMarkdown pre {
        background-color: black !important;
        border: 1px solid #00ff00 !important;
    }
    
    .stMarkdown code {
        background-color: black !important;
        color: #00ff00 !important;
        border-color: #00ff00 !important;
    }
    
    /* Force dark background */
    section[data-testid="stSidebar"] {
        background-color: black !important;
        color: #00ff00 !important;
    }
    .stApp {
        background-color: black !important;
    }
    
    /* Style headers and all text */
    h1, h2, h3, p, span, div {
        color: #00ff00 !important;
    }
    
    /* Console title styling */
    .console-title {
        font-family: 'Courier New', Courier, monospace;
        color: #00ff00 !important;
        margin-bottom: 5px;
        padding: 5px 0;
        font-size: 1.2em;
        font-weight: bold;
        border-bottom: 1px solid #00ff00;
    }
    
    /* Style buttons */
    .stButton > button {
        background-color: #004400 !important;
        color: #00ff00 !important;
        border: 1px solid #00ff00 !important;
    }
    .stButton > button:hover {
        background-color: #006600 !important;
        border-color: #00ff00 !important;
    }

    /* Style Streamlit's settings menu */
    button[kind="header"] {
        background-color: black !important;
        color: #00ff00 !important;
    }
    .stDeployButton {
        display: none !important;
    }
    section[data-testid="stSidebar"] > div {
        background-color: black !important;
    }
    .stSlider > div[data-baseweb="slider"] > div {
        background-color: #004400 !important;
    }
    .stSlider > div[data-baseweb="slider"] > div > div > div {
        background-color: #00ff00 !important;
    }
    
    /* Force all text within terminal to be green */
    .terminal div, .terminal span, .terminal p {
        color: #00ff00 !important;
        background-color: black !important;
    }

    /* Footer styling */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        width: 100%;
        padding: 15px;
        text-align: center;
        background-color: black !important;
        border-top: 1px solid #00ff00;
        z-index: 1000000;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 10px;
    }
    
    /* Add padding to main content to prevent footer overlap */
    .main .block-container {
        padding-bottom: 100px !important;
    }
    
    /* Ensure footer stays above sidebar */
    section[data-testid="stSidebar"] {
        z-index: auto !important;
    }
    
    .footer a {
        color: #00ff00 !important;
        text-decoration: none;
        font-family: 'Courier New', Courier, monospace;
    }
    
    .footer a:hover {
        color: #00ff00 !important;
        text-decoration: underline;
    }
    
    .social-icons {
        margin: 0;
        padding: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 20px;
    }
    
    .social-icons a {
        display: flex;
        align-items: center;
    }
    
    .social-icons svg {
        width: 20px;
        height: 20px;
        fill: #00ff00;
        transition: fill 0.3s ease;
    }
    
    .social-icons svg:hover {
        fill: #00ff00;
        filter: brightness(1.2);
    }

    /* Override the blue color in the third icon */
    .social-icons svg path[fill="#00b4ff"] {
        fill: #00ff00 !important;
    }
</style>

<script>
    function forceScroll() {
        const terminal = document.querySelector('#terminal-messages');
        if (terminal) {
            const shouldScroll = Math.abs(terminal.scrollHeight - terminal.clientHeight - terminal.scrollTop) < 50;
            if (shouldScroll) {
                terminal.scrollTo({
                    top: terminal.scrollHeight,
                    behavior: 'auto'
                });
            }
        }
    }

    function setupTerminal() {
        const terminal = document.querySelector('#terminal-messages');
        if (terminal) {
            // Initial scroll
            terminal.scrollTop = terminal.scrollHeight;
            
            // Watch for changes
            const observer = new MutationObserver((mutations) => {
                requestAnimationFrame(() => {
                    terminal.scrollTop = terminal.scrollHeight;
                });
            });
            
            observer.observe(terminal, {
                childList: true,
                subtree: true,
                characterData: true
            });
            
            // Force scroll on any content changes
            terminal.addEventListener('DOMNodeInserted', () => {
                requestAnimationFrame(() => {
                    terminal.scrollTop = terminal.scrollHeight;
                });
            });
        }
    }

    // Run setup
    document.addEventListener('DOMContentLoaded', setupTerminal);
    setInterval(forceScroll, 100);
</script>
"""

# Initialize session state
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []
if "data_manager" not in st.session_state:
    st.session_state["data_manager"] = DataManager()

def format_terminal_message(message: str) -> str:
    """Format a message for terminal display"""
    if "Error" in message:
        return f'<div class="terminal-message error-message">{message}</div>'
    elif any(role in message for role in ["Director", "Writer", "Developer", "Timer", "Prompter"]):
        return f'<div class="terminal-message agent-message">{message}</div>'
    else:
        return f'<div class="terminal-message system-message">{message}</div>'

def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
    return href

def initialize_agents():
    """Initialize all agents"""
    director = Director()
    director.character_writer = CharacterWriter()
    director.plot_writer = PlotWriter()
    director.scene_descriptor = SceneDescriptor()
    director.time_stamper = TimeStamper()
    director.image_prompter = ImagePrompter()
    director.screenwriter = Screenwriter()
    return director

def main():
    st.title("Creative Director Screenwriter")
    
    # Sidebar
    with st.sidebar:
        st.title("Story Controls")
        if st.button("Start New Story"):
            st.session_state["data_manager"].clear_current_story()
            st.session_state["data_manager"].create_new_story()
            st.session_state["message_history"] = []
            st.experimental_rerun()
            
        if st.button("Save Story"):
            try:
                zip_path = st.session_state["data_manager"].create_zip_archive()
                st.markdown(get_binary_file_downloader_html(zip_path, 'Story Archive'), unsafe_allow_html=True)
            except ValueError as e:
                st.error("No story to save yet!")
    
    # Initialize agents
    director = initialize_agents()
    
    # User inputs and generate button
    col1, col2 = st.columns([3, 1])
    with col1:
        story_idea = st.text_area("Enter your story idea:", height=100)
    with col2:
        length_minutes = st.slider("Film length (minutes):", min_value=1, max_value=10, value=5)
        generate_button = st.button("Generate Screenplay")
    
    # Create message container
    message_container = st.empty()
    
    # Function to update terminal display
    def update_terminal():
        messages_html = "\n".join([format_terminal_message(msg) for msg in st.session_state["message_history"]])
        message_container.markdown(
            f"{TERMINAL_STYLE}<div class='console-title'>Agent Communication Console</div><div class='terminal'><div id='terminal-messages'>{messages_html}</div></div>",
            unsafe_allow_html=True
        )
    
    # Initial terminal display
    update_terminal()
    
    if generate_button:
        if not story_idea:
            st.error("Please enter a story idea.")
            return
            
        try:
            # Store container reference for agents
            st.session_state["message_container"] = message_container
            st.session_state["update_terminal"] = update_terminal
            
            screenplay = director.execute(story_idea, length_minutes)
            st.session_state["data_manager"].save_output(screenplay, "screenplay_package.txt")
            
            # Final terminal update
            update_terminal()
            
            # Display final screenplay in a separate text area
            st.subheader("Generated Screenplay")
            st.text_area("Final Screenplay", value=screenplay, height=400)
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.session_state["message_history"].append(f"❌ Error: {str(e)}")
            update_terminal()

    # Add footer
    st.markdown("""
    <div class="footer">
        <div class="social-icons">
            <a href="https://x.com/VirtualsFILM" target="_blank">
                <svg viewBox="0 0 24 24">
                    <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
                </svg>
            </a>
            <a href="https://github.com/mersivmedia" target="_blank">
                <svg viewBox="0 0 24 24">
                    <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/>
                </svg>
            </a>
            <a href="https://app.virtuals.io/prototypes/0x6416161FCf3c15EEE06Be847fcD028eA99cA1D74" target="_blank">
                <svg width="28" height="28" viewBox="0 0 56 56" xmlns="http://www.w3.org/2000/svg">
                    <path fill-rule="evenodd" d="M33.98 19.75a7.14 7.14 0 0 0-2.47-2.78 6.53 6.53 0 0 0-6.55-.2 7.42 7.42 0 0 0-3.11 3.03 6.1 6.1 0 0 0-.64 4.61c.25 1 .73 1.93 1.44 2.81a8.42 8.42 0 0 0 6.78 3.17.1.1 0 0 1 .09.06.1.1 0 0 1 0 .1 25.73 25.73 0 0 1-2.37 4.1c-.04.05-.08.05-.12-.01a98.5 98.5 0 0 0-.76-1.16l-.04-.06-.1-.15a27.28 27.28 0 0 0-4.22-4.9 25.12 25.12 0 0 0-10.29-5.81c-.32-.1-.96-.22-1.94-.39-.18-.03-.31-.02-.4.02-.2.09-.3.23-.28.44.02.2.12.35.31.45A31.14 31.14 0 0 1 23.6 37.93l.12.26a110.53 110.53 0 0 1 .32.74c.2.45.36.77.5.95.38.5.88.83 1.52 1 1.13.3 2.1.04 2.89-.79a26.67 26.67 0 0 0 3.16-4.14 22.8 22.8 0 0 0 2.79-6.42.2.2 0 0 1 .12-.14 24.52 24.52 0 0 0 7.74-4.7c.17-.15.27-.27.29-.36a.53.53 0 0 0-.07-.42c-.08-.15-.2-.22-.36-.2a.73.73 0 0 0-.32.1 25.44 25.44 0 0 1-6.85 2.93c-.05.01-.07 0-.07-.06.1-2.08-.2-4.08-.94-6a7.72 7.72 0 0 0-.45-.93Zm-4.66 7.49 1.24.16h.04c.02-.02.03-.03.03-.05.32-1.27.4-2.54.24-3.81a5.93 5.93 0 0 0-1.1-2.8 2.26 2.26 0 0 0-2.1-.85c-.81.08-1.5.43-2.05 1.06-.75.85-.93 1.81-.54 2.9.33.95.88 1.72 1.64 2.3.72.57 1.59.93 2.6 1.09Z" fill="#00ff00"/>
                    <path d="M44.64 21.74c.17-.16.39-.28.64-.36.27-.09.52-.11.77-.08.6.07.92.41.95 1.03.02.38-.09.73-.32 1.05-.22.3-.51.5-.87.61a.96.96 0 0 1-.82-.1c-.23-.14-.4-.37-.49-.67-.1-.33-.15-.6-.15-.8 0-.28.1-.5.29-.68Z" fill="#00ff00"/>
                </svg>
            </a>
        </div>
        <div>
            <a href="https://mersivmedia.com" target="_blank">Made by Mersiv Media</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 