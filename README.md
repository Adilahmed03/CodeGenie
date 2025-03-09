
# CodeGenie - AI-Powered Code Generation

CodeGenie is an AI-powered code generation tool that helps developers generate high-quality code snippets based on natural language descriptions. It supports multiple programming languages and integrates with AI models to improve coding efficiency.

## 🚀 Features
- **AI-Powered Code Generation**: Generate code snippets from natural language descriptions.
- **Language Detection**: Automatically detect programming language from the prompt.
- **Multiple AI Models**: Supports Mistral 7B, CodeLlama 7B, and Bloomz 7B1.
- **Customizable Code Output**: Choose between different levels of verbosity and styles.
- **Code Explanation**: Provides an explanation of the generated code.
- **Download Generated Code**: Easily download code snippets.
- **User Authentication**: Secure login system.
- **Dark Mode & Modern UI**: Clean, modern, and animated UI for a great user experience.

## 📜 Installation & Setup
### Prerequisites
- Python 3.7+
- Streamlit
- Requests

### Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/Adilahmed03/CodeGenie.git
   cd CodeGenie
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the application:
   ```sh
   streamlit run app1.py
   ```

## 🔑 Environment Variables
Create a `.env` file in the root directory and add the following:
```sh
HUGGINGFACEHUB_API_TOKEN=your_huggingface_api_key
```

## 🖥️ Usage
1. Enter a prompt describing the code you want to generate.
2. Select a programming language or use auto-detection.
3. Click the "Generate Code" button.
4. Review, download, or modify the generated code.
5. View and restore previous generated code in the History tab.

## 🛠️ Technologies Used
- **Frontend**: Streamlit
- **Backend**: Python, Hugging Face API
- **Authentication**: Custom login system

## 📝 License
This project is licensed under the MIT License.

## 🙌 Contributing
Feel free to submit issues and pull requests for improvements.

## 💡 Future Enhancements
- Add more AI models.
- Improve prompt understanding for better accuracy.
- Enhance user experience with more customization options.

**Developed with ❤️ by [Adilahmed03](https://github.com/Adilahmed03)**

