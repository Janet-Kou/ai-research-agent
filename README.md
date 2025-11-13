
# AI Research Agent (Langchain + OpenAI)

This is a proof of concept research assistant utilizing Langchain and OpenAI's GPT-4 model, based on the TechWithTim AI Agent Tutorial.
The agent uses tool-calling agent to search the web (via DuckDuckGo) and Wikipedia.
If requested, the agent will store the summarized research in structed form to a newly created file in the current directory
Built and tested in Google Colab.

# Features
- LangChain Agent: uses `create_tool_calling_agent` and `AgentExecutor` for reasoning and action.
- DuckDuckGo Search Integration: live web search through `langchain_community.tools`.
- Pydantic Output Parsing: structured outputs with automatic validation.
- Environment Variable Management: uses `.env` with `dotenv` for secure API key loading.
- Extensible Tooling System: add more tools easily.

# Project Structure

ai-research-agent/\
│\
├── main.py # Core agent logic\
├── tools.py # Search and other helper tools\
├── requirements.txt # Python dependencies\
├── .env # Environment file (excluded from git)\
├── README.md # Project documentation\
└── .gitignore # Excludes venvs, .env, caches, etc.

# Setup Instructions
  1. Clone the repository 
  (```bash
  git clone https://github.com/Janet-Kou/ai-research-agent.git
  cd ai-research-agent
  )

  2. Create and activate a virtual environment\
    Windows:\
      python -m venv venv \
      venv\Scripts\activate \
    macOS/Linux \
      python3 -m venv venv \
      source venv/bin/activate 

  4. Install dependencies\
      pip install -r requirements.txt

  5. Environment setup\
      Create a .env file in the project root with your OpenAI API key\
      OPENAI_API_KEY=sk-your-openai-api-key

  6. Run the Agent\
      a. In terminal run : python main.py\
      b. You will be prompted with "What can I help you research?"\
      c. Type what you would like to research and hit enter. Optionally, you can request that the information is saved to a file. The agent will create a new file in your directory with the researched infromation.

# Author
GitHub: Janet-Kou




