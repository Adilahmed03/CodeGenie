import streamlit as st
import requests
import json
import os
import re
from datetime import datetime
from login import authenticate_user, initialize_user_database  # Import the login functions
import time


# Initialize the user database at startup
initialize_user_database()

# Add custom CSS with animations and color scheme
def load_css():
    st.markdown("""
    <style>
    /* Modern Color Scheme */
    :root {
        --primary: #6C63FF;
        --secondary: #FF6584;
        --accent: #43CBFF;
        --bg-gradient: linear-gradient(135deg, #43CBFF 10%, #9708CC 100%);
        --card-bg: rgba(255, 255, 255, 0.95);
        --success: #00D09C;
        --warning: #FFBF00;
        --error: #FF5470;
        --text-dark: #333333;
        --text-light: #FFFFFF;
    }

    /* Main Container Styling */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }

    /* Header Animation */
    h1, h2, h3 {
        background: var(--bg-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: colorShift 8s infinite alternate;
    }

    /* Card styling with hover effects */
    .stButton>button, .stDownloadButton>button {
        background: var(--bg-gradient);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
        transform: translateY(0);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .stButton>button:hover, .stDownloadButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 7px 14px rgba(0, 0, 0, 0.1);
    }

    .stButton>button:active, .stDownloadButton>button:active {
        transform: translateY(1px);
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 5px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        transition: background-color 0.3s ease, color 0.3s ease;
    }

    .stTabs [aria-selected="true"] {
        background-color: var(--primary);
        color: white;
    }

    /* Code block styling */
    pre {
        border-radius: 10px;
        border-left: 5px solid var(--primary);
        background-color: #2a2a2a;
        transition: all 0.3s ease;
    }

    pre:hover {
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
        transform: translateY(-2px);
    }

    /* Animate explanation blocks */
    .explanation {
        animation: fadeIn 0.8s ease-out;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-image: linear-gradient(180deg, rgba(108, 99, 255, 0.2) 0%, rgba(67, 203, 255, 0.2) 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 0.5rem;
    }

    /* Sliding animations */
    @keyframes slideInRight {
        from { transform: translateX(50px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }

    @keyframes slideInLeft {
        from { transform: translateX(-50px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    @keyframes colorShift {
        0% { filter: hue-rotate(0deg); }
        100% { filter: hue-rotate(90deg); }
    }

    /* Loading animation */
    .loading-animation {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100px;
    }

    .loading-animation div {
        width: 20px;
        height: 20px;
        margin: 0 5px;
        border-radius: 50%;
        background: var(--primary);
        animation: pulse 1.5s infinite ease-in-out;
    }

    .loading-animation div:nth-child(2) {
        animation-delay: 0.2s;
        background: var(--secondary);
    }

    .loading-animation div:nth-child(3) {
        animation-delay: 0.4s;
        background: var(--accent);
    }

    @keyframes pulse {
        0%, 100% { transform: scale(0.5); opacity: 0.5; }
        50% { transform: scale(1.2); opacity: 1; }
    }

    /* Toast notifications */
    .toast {
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 25px;
        border-radius: 10px;
        color: white;
        z-index: 1000;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        animation: slideInRight 0.5s ease-out, fadeOut 0.5s ease-in 2.5s forwards;
    }

    .success-toast {
        background-color: var(--success);
    }

    .error-toast {
        background-color: var(--error);
    }

    @keyframes fadeOut {
        from { opacity: 1; }
        to { opacity: 0; }
    }

    /* Floating logo animation */
    .logo {
        display: inline-block;
        animation: float 3s ease-in-out infinite;
    }

    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    </style>
    """, unsafe_allow_html=True)

# Check authentication status
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Define file extensions dictionary - moved to global scope so it's accessible everywhere
file_extensions = {
    "Python": "py", "JavaScript": "js", "Java": "java", "C++": "cpp", 
    "C": "c", "C#": "cs", "Go": "go", "Ruby": "rb", "PHP": "php",
    "Swift": "swift", "Kotlin": "kt", "Rust": "rs", "TypeScript": "ts",
    "HTML": "html", "CSS": "css", "SQL": "sql", "Shell/Bash": "sh",
    "Perl": "pl", "R": "r", "MATLAB": "m"
}

# Show login page if not authenticated
if not st.session_state["authenticated"]:
    from login import login_page
    login_page()
else:
    # Set page configuration
    st.set_page_config(
        page_title="CodeGenie - AI Code Generation",
        page_icon="🧞‍♂️",
        layout="wide"
    )
    
    # Load custom CSS
    load_css()

    # Add animated logo and title with staggered animation
    st.markdown("""
    <div style="text-align: center; animation: fadeIn 0.8s ease-out;">
        <h1><span class="logo">🧞‍♂️</span> CodeGenie</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome message with animation
    st.markdown(f"""
    <div style="animation: slideInLeft 0.6s ease-out;">
        <h3>Welcome, {st.session_state['username']}!</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="animation: slideInRight 0.8s ease-out;">
        <h3>AI-Powered Code Generation using AI Models</h3>
        <p>Input a description of what you want to achieve, and CodeGenie will generate the code for you.</p>
    </div>
    """, unsafe_allow_html=True)

    # Pre-configured API key (embedded for hackathon purposes)
    DEFAULT_API_KEY ="api-key"

    # Function to detect programming language from user's prompt
    def detect_language_from_prompt(prompt):
        # Dictionary of programming languages and their related keywords/patterns
        language_patterns = {
            "Python": [r'\bpython\b', r'\.py\b', r'\bpip\b', r'\bdjango\b', r'\bflask\b', r'\bnumpy\b', r'\bpandas\b'],
            "JavaScript": [r'\bjavascript\b', r'\bjs\b', r'\.js\b', r'\bnode\.js\b', r'\bnpm\b', r'\breact\b', r'\bangular\b', r'\bvue\b'],
            "Java": [r'\bjava\b', r'\.java\b', r'\bspring\b', r'\bmaven\b', r'\bhibernate\b'],
            "C++": [r'\bc\+\+\b', r'\.cpp\b', r'\bcmake\b', r'\bstl\b', r'\bvector<\b'],
            "C": [r'\bc\b', r'\.c\b', r'\bpointer\b', r'\bmalloc\b', r'\bstdio\b', r'\bstdlib\b', r'\bprintf\b'],
            "C#": [r'\bc#\b', r'\.cs\b', r'\bdotnet\b', r'\basync\b', r'\bawait\b', r'\busing\b'],
            "Go": [r'\bgo\b', r'\bgolang\b', r'\.go\b', r'\bgoroutine\b'],
            "Ruby": [r'\bruby\b', r'\.rb\b', r'\brails\b', r'\bgem\b'],
            "PHP": [r'\bphp\b', r'\.php\b', r'\blaravel\b', r'\bsymphony\b'],
            "Swift": [r'\bswift\b', r'\.swift\b', r'\bios\b', r'\bxcode\b', r'\bcocoa\b'],
            "Kotlin": [r'\bkotlin\b', r'\.kt\b', r'\bandroid\b'],
            "Rust": [r'\brust\b', r'\.rs\b', r'\bcargo\b', r'\bcrate\b'],
            "TypeScript": [r'\btypescript\b', r'\bts\b', r'\.ts\b', r'\bangular\b', r'\bvue\b'],
            "HTML": [r'\bhtml\b', r'\.html\b', r'\bhtml5\b', r'\bdiv\b', r'\bspan\b', r'\binput\b', r'\bform\b', r'\bmarkup\b'],
            "CSS": [r'\bcss\b', r'\.css\b', r'\bstylesheet\b', r'\bstyle\b', r'\bflex\b', r'\bgrid\b', r'\bbootstrap\b'],
            "SQL": [r'\bsql\b', r'\bmysql\b', r'\bpostgresql\b', r'\bselect\b', r'\bfrom\b', r'\bwhere\b', r'\bgroup by\b'],
            "Shell/Bash": [r'\bbash\b', r'\bshell\b', r'\.sh\b', r'\blinux\b', r'\bunix\b', r'\bscript\b'],
            "Perl": [r'\bperl\b', r'\.pl\b', r'\bregex\b'],
            "R": [r'\br\b', r'\.r\b', r'\bstatistics\b', r'\bggplot\b', r'\bdplyr\b'],
            "MATLAB": [r'\bmatlab\b', r'\.m\b', r'\bmatrix\b', r'\boctave\b']
        }
        
        # Check for explicit language mentions
        prompt_lower = prompt.lower()
        for language, patterns in language_patterns.items():
            for pattern in patterns:
                if re.search(pattern, prompt_lower, re.IGNORECASE):
                    return language
        
        # Look for language mentions like "in Python" or "using JavaScript"
        for language in language_patterns.keys():
            if f"in {language.lower()}" in prompt_lower or f"using {language.lower()}" in prompt_lower:
                return language
            
        # Default to Python if no language is detected
        return "Python"

    # Custom loading animation for API requests
    def show_loading_animation():
        st.markdown("""
        <div class="loading-animation">
            <div></div>
            <div></div>
            <div></div>
        </div>
        <p style="text-align: center;">CodeGenie is working its magic...</p>
        """, unsafe_allow_html=True)

    # Toast notification function
    def show_toast(message, type="success"):
        toast_class = "success-toast" if type == "success" else "error-toast"
        st.markdown(f"""
        <div class="toast {toast_class}" id="toast">
            {message}
        </div>
        """, unsafe_allow_html=True)

    # Sidebar for settings with animations
    with st.sidebar:
        st.markdown("""
        <div style="animation: slideInLeft 0.6s ease-out;">
            <h2>✨ Settings</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # List of all supported programming languages
        all_languages = [
            "Python", "JavaScript", "Java", "C++", "C", "C#", "Go", "Ruby", 
            "PHP", "Swift", "Kotlin", "Rust", "TypeScript", "HTML", "CSS", 
            "SQL", "Shell/Bash", "Perl", "R", "MATLAB"
        ]
        
        # Initialize programming_language in session state if not already there
        if "programming_language" not in st.session_state:
            st.session_state["programming_language"] = "Python"
        
        # Allow manual override with a checkbox
        auto_detect = st.checkbox("Auto-detect language from prompt", value=True)
        
        # Only show manual selection if auto-detect is off
        if not auto_detect:
            programming_language = st.selectbox(
                "Programming Language",
                all_languages,
                index=all_languages.index(st.session_state["programming_language"]) if st.session_state["programming_language"] in all_languages else 0
            )
            st.session_state["programming_language"] = programming_language
        
        # Model selection with visual indicators
        st.markdown("""
        <div style="animation: fadeIn 0.8s ease-out;">
            <h3>Model Selection</h3>
        </div>
        """, unsafe_allow_html=True)
        
        model_options = {
            "Mistral 7B Instruct": "mistralai/Mistral-7B-Instruct-v0.2",
            "CodeLlama 7B Instruct": "codellama/CodeLlama-7b-Instruct-hf",
            "Bloomz 7B1": "bigscience/bloomz-7b1"
        }
        
        # Prepare model cards with icons
        models_html = ""
        for model_name in model_options.keys():
            icon = "🔮" if "Mistral" in model_name else "🦙" if "CodeLlama" in model_name else "🌸"
            models_html += f"<option value='{model_name}'>{icon} {model_name}</option>"
        
        selected_model = st.selectbox("Select AI Model", list(model_options.keys()))
        model_id = model_options[selected_model]
        
        # Hidden settings (not visible to user but still functional)
        max_length = 500  # Default value
        temperature = 0.7  # Default value
        api_key = DEFAULT_API_KEY  # Default value
        
        # Add a history tab directly in the sidebar
        st.markdown("""
        <div style="animation: fadeIn 0.8s ease-out;">
            <h3>Your Code History</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Create history directory if it doesn't exist
        if not os.path.exists("history"):
            os.makedirs("history")
        
        # Get list of history files specific to the current user
        history_files = []
        for filename in os.listdir("history"):
            if filename.startswith("code_") and filename.endswith(".txt"):
                # Read the file to check if it belongs to the current user
                with open(os.path.join("history", filename), "r") as f:
                    content = f.read()
                    if f"User: {st.session_state['username']}" in content:
                        history_files.append(filename)
        
        # Sort by timestamp (newest first)
        history_files.sort(reverse=True)
        
        if not history_files:
            st.info("No code history found. Generate some code first!")
        else:
            # Create history cards with animation
            for i, filename in enumerate(history_files):
                with open(os.path.join("history", filename), "r") as f:
                    content = f.read()
                
                # Extract metadata
                prompt = "Unknown"
                language = "Unknown"
                timestamp = "Unknown"
                
                for line in content.split("\n"):
                    if line.startswith("Prompt:"):
                        prompt = line[8:].strip()
                    elif line.startswith("Language:"):
                        language = line[10:].strip()
                    elif line.startswith("Timestamp:"):
                        timestamp = line[11:].strip()
                    elif line.startswith("--- Generated Code ---"):
                        break
                
                # Extract the code
                code_parts = content.split("--- Generated Code ---")
                if len(code_parts) > 1:
                    code = code_parts[1].strip()
                else:
                    code = "No code found"
                
                # Create a card for each history item with staggered animation
                st.markdown(f"""
                <div style="animation: slideInLeft {0.5 + i*0.1}s ease-out;">
                    <h4>{language} - {timestamp.split()[0]}</h4>
                    <p style="font-size: 0.9em;">{prompt[:75]}{"..." if len(prompt) > 75 else ""}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Determine language for syntax highlighting
                highlight_lang = language.lower()
                if highlight_lang == "shell/bash":
                    highlight_lang = "bash"
                
                with st.expander("Show Code"):
                    st.code(code, language=highlight_lang)
                    
                    # File extension for download
                    file_ext = file_extensions.get(language, language.lower())
                    
                    # Create download button for this history item
                    st.download_button(
                        label="📥 Download This Code",
                        data=code,
                        file_name=f"history_code_{filename.replace('.txt', '')}.{file_ext}",
                        mime="text/plain"
                    )
                
                st.markdown("<hr style='margin: 8px 0; opacity: 0.3;'>", unsafe_allow_html=True)
        
        # Add a logout button to the sidebar with animation
        st.markdown("""
        <div style="animation: fadeIn 1s ease-out; margin-top: 20px;">
        """, unsafe_allow_html=True)
        if st.button("Logout"):
            # Add a logout animation
            st.markdown("""
            <div style="text-align: center; animation: fadeIn 0.5s ease-out;">
                <p>Logging out...</p>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(1)  # Brief pause for animation
            st.session_state["authenticated"] = False
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("""
        <div style="animation: slideInLeft 1s ease-out;">
            <h3>About CodeGenie</h3>
            <p>CodeGenie uses AI models to generate code based on natural language descriptions.
            This tool helps developers save time and reduce errors by automating code generation.</p>
        </div>
        """, unsafe_allow_html=True)

    # Function to generate code using Hugging Face Inference API
    def generate_code_api(prompt, language, model_id, max_length, temperature, api_key=DEFAULT_API_KEY):
        # API endpoint
        api_url = f"https://api-inference.huggingface.co/models/{model_id}"
        
        # Headers for the API request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        # Construct the full prompt based on the model and language
        language_file_extension = {
            "Python": "py", "JavaScript": "js", "Java": "java", "C++": "cpp", 
            "C": "c", "C#": "cs", "Go": "go", "Ruby": "rb", "PHP": "php",
            "Swift": "swift", "Kotlin": "kt", "Rust": "rs", "TypeScript": "ts",
            "HTML": "html", "CSS": "css", "SQL": "sql", "Shell/Bash": "sh",
            "Perl": "pl", "R": "r", "MATLAB": "m"
        }
        
        # Default extension if language not found
        file_ext = language_file_extension.get(language, language.lower())
        
        # Special handling for HTML/CSS/JS combined projects
        is_web_project = False
        if "HTML" in prompt.upper() and "CSS" in prompt.upper():
            is_web_project = True
        
        if "codellama" in model_id.lower():
            # CodeLlama specific prompt
            if is_web_project:
                full_prompt = f"""
                Write code based on this description:
                {prompt}
                
                Include HTML structure, CSS styling, and JavaScript if needed.
                Format the code properly with clear comments.
                
                Code:
                ```
                """
            else:
                full_prompt = f"""
                Write a {language} function based on this description:
                {prompt}
                
                Include necessary imports, clear comments, and format the code properly.
                
                {language} code:
                ```{file_ext}
                """
        else:
            # Generic prompt for other models
            if is_web_project:
                full_prompt = f"""
                Task: Write code based on the following description.
                Description: {prompt}
                Requirements:
                - Create proper HTML structure
                - Add CSS styling
                - Include JavaScript functionality if needed
                - Format the code properly with clear sections
                
                CODE:
                """
            else:
                full_prompt = f"""
                Task: Write a {language} function based on the following description.
                Description: {prompt}
                Requirements:
                - Include necessary imports
                - Add clear comments
                - Format the code properly
                - Follow best practices for {language}
                
                {language} CODE:
                """
        
        # Payload for the API request
        payload = {
            "inputs": full_prompt,
            "parameters": {
                "max_new_tokens": max_length,
                "temperature": temperature,
                "top_p": 0.95,
                "do_sample": True
            }
        }
        
        try:
            # Make the API request
            response = requests.post(api_url, headers=headers, json=payload)
            
            # Check if the request was successful
            if response.status_code == 200:
                # Parse the response
                output = response.json()
                
                # Extract the generated text
                if isinstance(output, list) and len(output) > 0:
                    generated_text = output[0].get("generated_text", "")
                else:
                    generated_text = str(output)
                
                # Extract only the code part (after the prompt)
                code_part = generated_text[len(full_prompt):]
                
                # Clean up the code (remove trailing backticks if any)
                if "```" in code_part:
                    code_parts = code_part.split("```")
                    if len(code_parts) > 1:
                        code_part = code_parts[1]
                    else:
                        code_part = code_parts[0]
                
                return code_part.strip(), None
            else:
                error_msg = f"API request failed with status code {response.status_code}: {response.text}"
                return None, error_msg
        
        except Exception as e:
            return None, f"Error making API request: {str(e)}"

    # Function to explain code with animation
    def explain_code(code, language):
        # Language-specific keywords to look for in explanations
        language_specific = {
            "HTML": ["html", "body", "div", "span", "form", "input", "button", "tag", "element"],
            "CSS": ["style", "class", "id", "margin", "padding", "color", "background", "flex", "grid"],
            "JavaScript": ["function", "const", "let", "var", "document", "window", "event", "callback"],
            "Python": ["def", "class", "import", "with", "as", "try", "except", "list", "dict"],
            "Java": ["class", "public", "private", "static", "void", "interface", "extends", "implements"],
            "C++": ["class", "template", "namespace", "vector", "map", "cout", "cin", "pointer"],
            "C": ["pointer", "malloc", "free", "struct", "printf", "scanf", "include"],
            "C#": ["class", "using", "namespace", "public", "private", "async", "await", "List<>"],
            "SQL": ["select", "from", "where", "join", "group by", "having", "order by", "insert", "update"],
            "Go": ["func", "defer", "goroutine", "channel", "struct", "interface", "package"]
        }
        
        # Common code elements to look for
        common_code_elements = {
            "import": "This section imports necessary libraries and modules.",
            "include": "This includes necessary header files.",
            "def": "This defines a function that implements the requested functionality.",
            "function": "This defines a function that implements the requested functionality.",
            "class": "This defines a class to organize the functionality.",
            "for": "This loop iterates through the input data.",
            "while": "This loop executes code repeatedly until a condition is false.",
            "if": "This condition checks for specific cases.",
            "return": "This returns the final result from the function.",
            "try": "This implements error handling for the code.",
            "switch": "This provides multiple case conditions for different scenarios.",
            "struct": "This defines a custom data structure.",
            "constructor": "This initializes the object when it's created."
        }
        
        explanation = f"""<div class="explanation">
            <h3>{language} Code Analysis:</h3>
            <p>This code implements the requested functionality with proper structure and best practices for {language}.</p>
        """
        
        # Add language-specific explanations
        if language in language_specific:
            explanation += f"<h3>{language}-Specific Features:</h3>"
            
            # Count language-specific keywords in the code
            found_features = []
            for keyword in language_specific[language]:
                if keyword in code.lower():
                    found_features.append(keyword)
            
            if found_features:
                explanation += f"<p>The code utilizes {language}-specific features like: {', '.join(found_features)}</p>"
        
        # Add common code element explanations
        explanation += "<h3>Code Structure Breakdown:</h3><ul>"
        
        # Add some specific explanations based on code content
        for key, desc in common_code_elements.items():
            if key in code.lower():
                explanation += f"<li><strong>{key.capitalize()}</strong>: {desc}</li>"
        
        explanation += "</ul>"
        
        # Add performance and usage notes
        explanation += """
            <h3>Performance and Usage Notes:</h3>
            <ul>
                <li>The code is designed to handle the specific requirements efficiently.</li>
                <li>Error handling is implemented where appropriate.</li>
                <li>Follow best practices when integrating this code.</li>
            </ul>
        </div>
        """
        
        return explanation

    # Function to save code history
    def save_code_history(prompt, language, code):
        # Create a directory for history if it doesn't exist
        if not os.path.exists("history"):
            os.makedirs("history")
        
        # Generate a timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create a filename
        filename = f"history/code_{timestamp}.txt"
        
        # Save the code with metadata
        with open(filename, "w") as f:
            f.write(f"Prompt: {prompt}\n")
            f.write(f"Language: {language}\n")
            f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"User: {st.session_state['username']}\n")  # Added username to history
            f.write("\n--- Generated Code ---\n\n")
            f.write(code)

    # Add tabs for different features with animated transitions
    st.markdown("""
    <div style="animation: fadeIn 1s ease-out;">
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["✨ Generate Code", "❓ Help"])

    with tab1:
        # Main input area with animation
        st.markdown("""
        <div style="animation: slideInLeft 0.8s ease-out;">
        """, unsafe_allow_html=True)
        
        user_prompt = st.text_area("Describe the functionality you need:", height=150, 
                                placeholder="Example: Create a Python function that takes a list of numbers and returns the average of the even numbers. Or: Create an HTML page with a responsive navbar and contact form using CSS.")
        
        # Advanced options (collapsed by default)
        with st.expander("Advanced Options"):
            st.markdown("""
            <div style="animation: fadeIn 0.8s ease-out;">
            """, unsafe_allow_html=True)
            
            # Add some extra customization options
            st.markdown("#### Code Generation Options")
            
            # Allow setting code length (number of lines)
            code_length = st.slider("Approximate Code Length (lines)", 
                                   min_value=10, max_value=100, value=30, step=5)
            
            # Allow specifying code style
            code_style = st.selectbox("Code Style", 
                                     ["Standard", "Concise", "Heavily Commented", "Production Ready"])
            
            # Allow additional requirements
            additional_reqs = st.text_area("Additional Requirements", 
                                          placeholder="Enter any additional requirements or specifications...")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Generate code button with animation
        st.markdown("""
        <div style="animation: slideInRight 1s ease-out;">
        """, unsafe_allow_html=True)
        
        if st.button("🪄 Generate Code", use_container_width=True):
            if user_prompt:
                # Auto-detect language if enabled
                if auto_detect:
                    detected_language = detect_language_from_prompt(user_prompt)
                    st.session_state["programming_language"] = detected_language
                    st.info(f"Auto-detected language: {detected_language}")
                
                # Get the current programming language from session state
                programming_language = st.session_state["programming_language"]
                
                # Update prompt with additional requirements if provided
                full_prompt = user_prompt
                if 'additional_reqs' in locals() and additional_reqs:
                    full_prompt += f"\n\nAdditional requirements: {additional_reqs}"
                
                # Update prompt with code style if provided
                if 'code_style' in locals() and code_style != "Standard":
                    full_prompt += f"\n\nPlease make the code {code_style.lower()}."
                
                # Update prompt with code length if provided
                if 'code_length' in locals():
                    full_prompt += f"\n\nThe code should be approximately {code_length} lines long."
                
                # Display loading animation
                with st.spinner():
                    show_loading_animation()
                    
                    # Call the API to generate code
                    generated_code, error = generate_code_api(
                        full_prompt, 
                        programming_language,
                        model_id, 
                        max_length, 
                        temperature,
                        api_key
                    )
                
                # Handle the response
                if error:
                    st.error(f"Error generating code: {error}")
                    show_toast("Error generating code", "error")
                else:
                    # Save to history
                    save_code_history(user_prompt, programming_language, generated_code)
                    
                    # Show the generated code with syntax highlighting
                    st.markdown("""
                    <div style="animation: fadeIn 1s ease-out;">
                        <h3>✨ Generated Code:</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Determine language for syntax highlighting
                    highlight_lang = programming_language.lower()
                    if highlight_lang == "shell/bash":
                        highlight_lang = "bash"
                    
                    st.code(generated_code, language=highlight_lang)
                    
                    # Show toast notification
                    show_toast("Code generated successfully!")
                    
                    # Add download button
                    file_ext = file_extensions.get(programming_language, programming_language.lower())
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    
                    st.download_button(
                        label="📥 Download Code",
                        data=generated_code,
                        file_name=f"generated_code_{timestamp}.{file_ext}",
                        mime="text/plain",
                        use_container_width=True
                    )
                    
                    # Add code explanation with animation
                    st.markdown("""
                    <div style="animation: slideInRight 1.2s ease-out;">
                        <h3>🔍 Code Explanation:</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    explanation = explain_code(generated_code, programming_language)
                    st.markdown(explanation, unsafe_allow_html=True)
            else:
                st.warning("Please enter a prompt first.")
                show_toast("Please enter a prompt first", "error")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        # Help tab with animation
        st.markdown("""
        <div style="animation: fadeIn 0.8s ease-out;">
            <h3>How to Use CodeGenie</h3>
            
            <div class="card">
                <h4>Step 1: Describe what you want</h4>
                <p>Start by clearly describing the functionality you need. The more specific your description, the better the results.</p>
                
                <p><strong>Good example:</strong> "Create a Python function that takes a list of numbers, filters out the negative values, and returns the sum of the squares of the remaining positive numbers."</p>
                
                <p><strong>Weak example:</strong> "Make a function that handles numbers."</p>
            </div>
            
            <div class="card">
                <h4>Step 2: Select language or use auto-detect</h4>
                <p>You can either:</p>
                <ul>
                    <li>Keep "Auto-detect language from prompt" checked to let CodeGenie determine the programming language</li>
                    <li>Uncheck this option and manually select your preferred language</li>
                </ul>
            </div>
            
            <div class="card">
                <h4>Step 3: Choose a model</h4>
                <p>Select an AI model based on your needs:</p>
                <ul>
                    <li><strong>Mistral 7B Instruct:</strong> Good general-purpose code generation</li>
                    <li><strong>CodeLlama 7B Instruct:</strong> Specialized for code generation</li>
                    <li><strong>Bloomz 7B1:</strong> Another option with different capabilities</li>
                </ul>
            </div>
            
            <div class="card">
                <h4>Step 4: Generate and use the code</h4>
                <p>Click "Generate Code" and:</p>
                <ul>
                    <li>Review the generated code</li>
                    <li>Read the explanation to understand how it works</li>
                    <li>Download the code if you want to use it</li>
                    <li>Access your code history from the sidebar</li>
                </ul>
            </div>
            
            <h3>Tips for Better Results</h3>
            <ul>
                <li>Be specific about functionality, inputs, and outputs</li>
                <li>Mention error handling if needed</li>
                <li>Specify any libraries or frameworks you want to use</li>
                <li>Use the "Additional Requirements" field for extra details</li>
                <li>Try different models if you're not satisfied with the results</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="card">
            <h4>Keyboard Shortcuts</h4>
            <ul>
                <li><strong>Ctrl + Enter:</strong> Submit input in text areas</li>
                <li><strong>Esc:</strong> Unfocus text input</li>
                <li><strong>Ctrl + F:</strong> Search within the page</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer section with animation
    st.markdown("""
    <div style="animation: fadeIn 1.2s ease-out; margin-top: 2rem; text-align: center;">
        <hr style="margin: 1rem 0;">
        <p>🧞‍♂️ CodeGenie v1.0 | Created with ❤️from CodeCrafter5| Powered by AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Debug mode (hidden, can be enabled for troubleshooting)
    debug_mode = False
    if debug_mode:
        with st.expander("Debug Information", expanded=False):
            st.write("### Session State")
            st.write(st.session_state)
            
            st.write("### Current Settings")
            st.write({
                "Model": selected_model,
                "Model ID": model_id,
                "Programming Language": st.session_state.get("programming_language", "Python"),
                "Max Length": max_length,
                "Temperature": temperature
            })

# Error handling for the entire app
try:
    # Main app execution would happen here
    pass
except Exception as e:
    st.error(f"An unexpected error occurred: {str(e)}")
    
    # Log the error (in a production environment, you might want to save this to a file)
    print(f"Error: {str(e)}")
    
    # Offer a way to recover
    if st.button("Reset Application"):
        # Clear certain session state items
        for key in ["programming_language"]:
            if key in st.session_state:
                del st.session_state[key]
        
        # Rerun the app
        st.rerun()

# Add event handlers for client-side interactivity
st.markdown("""
<script>
    // JavaScript functions for additional interactivity
    // Note: This is limited in Streamlit but included for demonstration
    
    // Auto-hide toast notifications after 3 seconds
    setTimeout(function() {
        const toast = document.getElementById('toast');
        if (toast) {
            toast.style.opacity = '0';
            setTimeout(function() {
                toast.style.display = 'none';
            }, 500);
        }
    }, 3000);
</script>
""", unsafe_allow_html=True)