# LangGraph Agent with Qdrant Knowledge Base and Tavily Search

A modular LangGraph agent that combines knowledge retrieval from Qdrant vector database with real-time web search capabilities using Tavily.

## Features

- **Knowledge Base Retrieval**: Query your Qdrant vector database for stored knowledge (books, literature, etc.)
- **Real-time Web Search**: Get current information using Tavily API (news, weather, current events)
- **Intelligent Tool Selection**: LLM automatically chooses the appropriate tool based on query type
- **Modular Architecture**: Clean, organized codebase with separated concerns

## Project Structure

```
your-project/
├── agent.py                 # Main graph definition and compilation
├── models/
│   ├── __init__.py         # Module exports
│   └── state.py            # AgentState definition with message handling
├── tools/
│   ├── __init__.py         # Tool exports
│   ├── knowledge.py        # Qdrant knowledge retrieval tool
│   └── search.py           # Tavily web search tool
├── nodes/
│   ├── __init__.py         # Node exports
│   └── agent_node.py       # Agent logic with tool binding
├── config/
│   ├── __init__.py         # Configuration exports
│   └── settings.py         # LLM, embeddings, and client configurations
├── langgraph.json          # LangGraph Studio configuration
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
└── README.md              # This file
```

## Module Explanation

### `models/`
- **`state.py`**: Defines `AgentState` with typed message handling using LangChain message types
- Handles conversation state management with proper type annotations

### `tools/`
- **`knowledge.py`**: Qdrant vector database tool for retrieving stored knowledge
  - Uses OpenAI embeddings for query vectorization
  - Searches your knowledge base for relevant information
- **`search.py`**: Tavily web search tool for real-time information
  - Handles current events, weather, dates, and breaking news
  - Includes direct date handling and improved query formatting

### `nodes/`
- **`agent_node.py`**: Core agent logic
  - Binds tools to the LLM
  - Processes user messages and generates responses
  - Manages tool calls and message flow

### `config/`
- **`settings.py`**: Centralized configuration
  - LLM initialization (GPT-4o-mini)
  - OpenAI embeddings setup
  - Qdrant client configuration

### `agent.py`
- Main graph assembly and compilation
- Defines workflow nodes and edges
- Implements conditional logic for tool selection
- Exports the compiled graph for LangGraph Studio

## Requirements

### API Keys
You need the following API keys:

1. **OpenAI API Key** - For LLM and embeddings
2. **Qdrant Cloud** - For vector database (URL + API key)
3. **Tavily API Key** - For web search
4. **LangSmith API Key** - For LangGraph Studio

### Python Dependencies

```txt
langgraph
langchain-openai
qdrant-client
tavily-python
```

## Setup Instructions

### 1. Clone and Setup Project Structure
Create the directory structure as shown above and copy the respective files.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file with your API keys:

```env
OPENAI_API_KEY=your-openai-api-key
QDRANT_URL=your-qdrant-cloud-url
QDRANT_API_KEY=your-qdrant-api-key
QDRANT_COLLECTION_NAME=your-collection-name
LANGSMITH_API_KEY=your-langsmith-api-key
TAVILY_API_KEY=your-tavily-api-key
```

### 4. Qdrant Setup
- Create a collection in Qdrant Cloud
- Ensure your collection uses OpenAI `text-embedding-3-small` vectors
- Store documents with `text` field in payload

### 5. Run with LangGraph Studio

Install LangGraph CLI:
```bash
pip install langgraph-cli
```

Start LangGraph Studio:
```bash
langgraph up --port 8125
```

Access the interface at: <<YOU WILL SRR A GENERATED LINK AFTER THE PERVIOUSE COMMAND>>

## Usage Examples

### Knowledge Base Queries
- "What is the answer to the ultimate question in The Hitchhiker's Guide to the Galaxy?"
- "Tell me about Arthur Dent"
- "What happens in the first chapter of [book name]?"

### Real-time Information
- "What's today's date?"
- "What's the current weather?"
- "What's happening in the news today?"
- "What are the latest tech trends?"

## Tool Selection Logic

The agent automatically selects tools based on query content:

- **Qdrant Tool**: Literature, books, stored knowledge, character information
- **Tavily Tool**: Current events, weather, dates, news, real-time data

## Configuration

### Model Settings
- **LLM**: GPT-4o-mini (configurable in `config/settings.py`)
- **Embeddings**: text-embedding-3-small
- **Temperature**: 0 (deterministic responses)

### Search Settings
- **Qdrant**: Returns top 3 most relevant results
- **Tavily**: Basic search depth, max 3 results with direct answers

## Troubleshooting

### Common Issues

1. **Port conflicts**: Use `--port` flag with different port number (if you have something on that port)
2. **API key errors**: Verify all keys are set in `.env`
3. **Qdrant connection**: Check URL format and API key validity
4. **Import errors**: Ensure all `__init__.py` files are present

### Debug Mode
LangGraph Studio provides visual debugging with:
- Graph execution flow
- Tool call monitoring
- State inspection
- Message tracing

## Extending the Agent

### Adding New Tools
1. Create tool in `tools/` directory
2. Add to `tools/__init__.py`
3. Import in `nodes/agent_node.py` and `agent.py`
4. Update tool descriptions for proper LLM selection

### Modifying Models
- Update `config/settings.py` for different LLM or embedding models
- Ensure Qdrant collection matches embedding dimensions

### Custom Nodes
- Add new nodes in `nodes/` directory
- Update graph structure in `agent.py`
- Implement custom logic as needed