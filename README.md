# 🤖 Promptly

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Node.js](https://img.shields.io/badge/node.js-18+-green.svg)](https://nodejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-red.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19+-blue.svg)](https://reactjs.org/)

**The Ultimate Prompt Engineering Agent Platform**

Transform the D.A.I.R. Prompt Engineering Guide into practical, modularized agents with advanced workflow orchestration.

---

## ✨ Features at a Glance

🎯 **10 Specialized Agents** | 🔗 **Workflow Orchestration** | 🚀 **Multi-LLM Support** | 💡 **Interactive Tutorial**

<p align="center">
  <img src="https://img.shields.io/badge/Agents-10%20Specialized-brightgreen" alt="10 Agents">
  <img src="https://img.shields.io/badge/Providers-OpenAI%20%7C%20Anthropic%20%7C%20Local-blue" alt="LLM Providers">
  <img src="https://img.shields.io/badge/Workflows-Visual%20Designer-purple" alt="Workflow Designer">
  <img src="https://img.shields.io/badge/Templates-3%20Pre--built-orange" alt="Templates">
</p>

---

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Agent Library](#agent-library)
- [Workflow Orchestration](#workflow-orchestration)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🎯 About Promptly

Promptly is a comprehensive, modularized agentic platform that transforms the D.A.I.R. Prompt Engineering Guide into practical, working agents with advanced workflow orchestration capabilities.

### Key Benefits
- **10 Specialized Agents**: Core + Advanced prompt engineering techniques
- **Multi-LLM Support**: OpenAI, Anthropic, and local models
- **Workflow Orchestration**: Chain agents with dependency management
- **Professional Interface**: React-based dashboard with comprehensive testing
- **Production Ready**: Error handling, monitoring, and scalability

## ✨ Features

### Core Agents (6)
1. **Zero-Shot Prompting** - Direct task execution without examples
2. **Few-Shot Prompting** - Example-guided response generation
3. **Chain-of-Thought** - Step-by-step reasoning breakdown
4. **Self-Consistency** - Multiple reasoning path validation
5. **Tree-of-Thoughts** - Branched reasoning exploration
6. **ReAct** - Reasoning + Action combined approach

### Advanced Agents (4)
1. **RAG Agent** - Retrieval Augmented Generation
2. **Auto-Prompt** - Automatic prompt optimization
3. **Program-Aided** - Code-assisted problem solving
4. **Factuality Checker** - Content accuracy validation

### Workflow Features
- **Visual Designer** - Drag-and-drop workflow creation
- **Template Library** - Pre-built workflow patterns
- **Dependency Management** - Sequential and parallel execution
- **Real-time Monitoring** - Live status updates
- **Result Passing** - Context flows between agents

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- MongoDB
- OpenAI API Key (optional)
- Anthropic API Key (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd prompt-engineering-platform
   ```

2. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   
   # Configure environment variables
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   yarn install
   ```

4. **Start Services**
   ```bash
   # Start MongoDB
   sudo systemctl start mongodb
   
   # Start Backend
   cd backend
   uvicorn server:app --host 0.0.0.0 --port 8001 --reload
   
   # Start Frontend
   cd frontend
   yarn start
   ```

5. **Access the Platform**
   - Frontend: `http://localhost:3000`
   - Backend API: `http://localhost:8001`
   - API Documentation: `http://localhost:8001/docs`

### Environment Configuration

**Backend (.env)**
```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=prompt_engineering_platform

# LLM API Keys (optional but recommended)
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

**Frontend (.env)**
```env
REACT_APP_BACKEND_URL=http://localhost:8001
```

## 🏗️ Architecture

### Technology Stack
- **Backend**: FastAPI, MongoDB, Python async/await
- **Frontend**: React 19, Tailwind CSS, Axios
- **LLM Integration**: OpenAI, Anthropic, Local models
- **Database**: MongoDB with proper serialization
- **Orchestration**: Custom workflow engine with dependency management

### System Components

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend │    │  FastAPI Backend │    │     MongoDB     │
│                 │◄──►│                 │◄──►│                 │
│ - Agent Library │    │ - Agent Registry │    │ - Workflows     │
│ - Workflow UI   │    │ - Workflow Engine│    │ - Results       │
│ - Templates     │    │ - LLM Integration│    │ - Sessions      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌─────────────────┐
│   User Browser  │    │  External LLMs  │
│                 │    │                 │
│ - Testing UI    │    │ - OpenAI        │
│ - Monitoring    │    │ - Anthropic     │
│ - Results       │    │ - Local Models  │
└─────────────────┘    └─────────────────┘
```

## 🔧 Agent Library

### Core Agents

#### Zero-Shot Agent
**Purpose**: Execute tasks without examples using pre-trained knowledge
**Use Cases**: General questions, basic analysis, simple tasks
**Example**:
```python
{
  "agent_type": "zero_shot",
  "prompt": "Explain quantum computing",
  "llm_provider": "openai"
}
```

#### Few-Shot Agent
**Purpose**: Guide responses using provided examples
**Use Cases**: Classification, pattern matching, structured outputs
**Example**:
```python
{
  "agent_type": "few_shot",
  "prompt": "Classify sentiment",
  "examples": [
    {"input": "I love this!", "output": "positive"},
    {"input": "This is terrible", "output": "negative"}
  ]
}
```

#### Chain-of-Thought Agent
**Purpose**: Break down complex problems into step-by-step reasoning
**Use Cases**: Mathematical problems, logical reasoning, complex analysis
**Example**:
```python
{
  "agent_type": "chain_of_thought",
  "prompt": "Calculate 15% tip on $80 bill"
}
```

### Advanced Agents

#### RAG Agent
**Purpose**: Combine external knowledge with generation
**Use Cases**: Knowledge-based queries, fact-checking, research
**Example**:
```python
{
  "agent_type": "rag",
  "prompt": "Explain recent developments in AI",
  "context": "Recent news articles and research papers about AI"
}
```

#### Auto-Prompt Agent
**Purpose**: Automatically optimize prompts for better results
**Use Cases**: Prompt improvement, response quality enhancement
**Example**:
```python
{
  "agent_type": "auto_prompt",
  "prompt": "Write a summary"  # Will be optimized automatically
}
```

## 🔗 Workflow Orchestration

### Workflow Types

#### 1. Sequential Workflows
Steps execute one after another, passing results forward.
```
Step 1 → Step 2 → Step 3
```

#### 2. Parallel Workflows
Independent steps execute simultaneously.
```
Step 1 ┌→ Step 2
       └→ Step 3
```

#### 3. Dependency Workflows
Complex dependencies with result passing.
```
Step 1 → Step 2 ┌→ Step 4
       → Step 3 └→ Step 5
```

### Pre-built Templates

#### Content Analysis Pipeline
1. **Zero-Shot Analysis** - Initial content review
2. **Chain-of-Thought Deep Dive** - Detailed analysis
3. **Factuality Check** - Accuracy validation

#### Problem Solving Workflow
1. **Tree-of-Thoughts Exploration** - Multiple solution paths
2. **Program-Aided Solution** - Code-assisted solving
3. **Self-Consistency Check** - Solution validation

#### Content Generation & Optimization
1. **Initial Generation** - Basic content creation
2. **Auto-Prompt Optimization** - Prompt improvement
3. **RAG Enhancement** - Knowledge augmentation

### Creating Custom Workflows

1. **Go to Workflows → Designer**
2. **Add Workflow Information**
   - Name: Descriptive workflow name
   - Description: What the workflow accomplishes
3. **Add Steps**
   - Choose agent type
   - Configure prompt and context
   - Set LLM provider
   - Define dependencies
4. **Create and Execute**

## 📚 API Documentation

### Agent Endpoints

#### List All Agents
```http
GET /api/agents
```
Returns list of available agents with descriptions.

#### Get Agent Information
```http
GET /api/agents/{agent_type}
```
Returns detailed information about a specific agent.

#### Process Agent Request
```http
POST /api/agents/process
Content-Type: application/json

{
  "agent_type": "zero_shot",
  "llm_provider": "openai",
  "request": {
    "prompt": "Your prompt here",
    "context": "Optional context",
    "examples": [{"input": "example", "output": "response"}]
  }
}
```

### Workflow Endpoints

#### Create Workflow
```http
POST /api/workflows
Content-Type: application/json

{
  "name": "My Workflow",
  "description": "Workflow description",
  "steps": [
    {
      "name": "Step 1",
      "agent_type": "zero_shot",
      "prompt": "Initial prompt",
      "llm_provider": "openai"
    }
  ]
}
```

#### Execute Workflow
```http
POST /api/workflows/{workflow_id}/execute
```

#### Get Workflows
```http
GET /api/workflows
```

#### Get Workflow Status
```http
GET /api/workflows/{workflow_id}
```

### Response Format

All responses follow this format:
```json
{
  "id": "unique-id",
  "status": "completed|failed|processing",
  "result": "Generated response",
  "reasoning": ["Step 1", "Step 2"],
  "metadata": {
    "technique": "agent_type",
    "model": "gpt-4o-mini",
    "usage": {"total_tokens": 100}
  },
  "error": null
}
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. Backend Won't Start

**Symptoms**: 
- `ModuleNotFoundError` when starting backend
- Import errors

**Solutions**:
```bash
# Install dependencies
pip install -r requirements.txt

# Check Python version
python --version  # Should be 3.11+

# Verify MongoDB is running
sudo systemctl status mongodb
```

#### 2. LLM Provider Errors

**Symptoms**:
- "Provider not available" errors
- API key authentication failures

**Solutions**:
```bash
# Check API keys in .env file
cat backend/.env

# Test API keys
curl -H "Authorization: Bearer YOUR_OPENAI_KEY" https://api.openai.com/v1/models

# Use local provider as fallback
# Change llm_provider to "local" in requests
```

#### 3. Workflow Creation Fails

**Symptoms**:
- "Create Workflow" button not working
- No workflows appearing in list

**Solutions**:
```bash
# Check backend logs
tail -f /var/log/supervisor/backend.err.log

# Verify MongoDB connection
mongo --eval "db.adminCommand('ismaster')"

# Check frontend console for errors
# Open browser DevTools → Console
```

#### 4. Frontend Build Issues

**Symptoms**:
- Build failures with dependency errors
- Module resolution errors

**Solutions**:
```bash
# Clear cache and reinstall
rm -rf node_modules yarn.lock
yarn install

# Check Node.js version
node --version  # Should be 18+

# Try alternative package manager
npm install --legacy-peer-deps
```

#### 5. MongoDB Connection Issues

**Symptoms**:
- Database connection timeouts
- Collection not found errors

**Solutions**:
```bash
# Start MongoDB service
sudo systemctl start mongodb
sudo systemctl enable mongodb

# Check MongoDB status
sudo systemctl status mongodb

# Verify connection
mongo mongodb://localhost:27017/test_database
```

#### 6. Workflow Execution Hangs

**Symptoms**:
- Workflows stuck in "running" status
- No progress updates

**Solutions**:
1. **Check Agent Dependencies**:
   - Verify all dependent steps completed
   - Check for circular dependencies
   
2. **Monitor Resource Usage**:
   ```bash
   # Check CPU and memory
   htop
   
   # Check disk space
   df -h
   ```

3. **Restart Backend**:
   ```bash
   sudo supervisorctl restart backend
   ```

#### 7. API Rate Limiting

**Symptoms**:
- 429 Too Many Requests errors
- Slow response times

**Solutions**:
1. **Implement Request Delays**:
   - Add delays between agent calls
   - Use local provider for testing
   
2. **Monitor Usage**:
   - Check API usage dashboards
   - Implement caching for repeated requests

### Performance Optimization

#### 1. Backend Performance
```python
# Increase worker processes
uvicorn server:app --workers 4

# Enable caching
# Use Redis for improved caching
pip install redis
```

#### 2. Frontend Performance
```bash
# Build optimized version
yarn build

# Use production server
serve -s build -l 3000
```

#### 3. Database Optimization
```javascript
// Create indexes for common queries
db.workflows.createIndex({ "created_at": -1 })
db.agent_responses.createIndex({ "session_id": 1 })
```

### Debugging Tools

#### 1. Backend Debugging
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# Use Python debugger
import pdb; pdb.set_trace()
```

#### 2. Frontend Debugging
```javascript
// Enable React DevTools
// Install React Developer Tools browser extension

// Debug API calls
console.log('API Request:', requestData);
console.log('API Response:', responseData);
```

#### 3. Database Debugging
```javascript
// MongoDB queries
db.workflows.find().pretty()
db.agent_responses.find().limit(5).sort({created_at: -1})
```

### Getting Help

#### 1. Check Logs
```bash
# Backend logs
tail -f /var/log/supervisor/backend.err.log

# Frontend logs
# Check browser console (F12)

# MongoDB logs
tail -f /var/log/mongodb/mongod.log
```

#### 2. Verify Configuration
```bash
# Environment variables
env | grep -E "(OPENAI|ANTHROPIC|MONGO)"

# Service status
sudo supervisorctl status

# Port availability
netstat -tlnp | grep -E "(3000|8001|27017)"
```

#### 3. Test Components Individually
```bash
# Test backend API
curl http://localhost:8001/api/agents

# Test database connection
mongo --eval "db.runCommand({connectionStatus: 1})"

# Test LLM providers
python -c "from llm_providers import llm_manager; import asyncio; asyncio.run(llm_manager.initialize_all_providers())"
```

## 🔧 Development

### Project Structure
```
/app/
├── backend/
│   ├── server.py              # Main FastAPI application
│   ├── llm_providers.py       # LLM integration layer
│   ├── workflow_engine.py     # Workflow orchestration
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Environment variables
├── frontend/
│   ├── src/
│   │   ├── App.js            # Main React application
│   │   ├── WorkflowDesigner.js # Workflow interface
│   │   ├── App.css           # Styling
│   │   └── index.js          # Entry point
│   ├── package.json          # Node dependencies
│   └── .env                  # Frontend environment
└── README.md                 # Documentation
```

### Adding New Agents

1. **Create Agent Class**:
```python
class NewAgent(BaseAgent):
    def __init__(self):
        super().__init__(AgentType.NEW_AGENT)
    
    async def _process_request(self, request, llm_provider):
        # Implementation here
        return {"result": "response", "reasoning": [], "metadata": {}}
```

2. **Register Agent**:
```python
# Add to AgentType enum
class AgentType(str, Enum):
    NEW_AGENT = "new_agent"

# Add to initialize_agents()
def initialize_agents():
    agents = [
        # ... existing agents
        NewAgent()
    ]
```

### Contributing

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/new-feature`
3. **Make changes and test thoroughly**
4. **Submit pull request with detailed description**

#### Code Style
- **Python**: Follow PEP 8
- **JavaScript**: Use ESLint configuration
- **Documentation**: Update README for new features

#### Testing
```bash
# Backend tests
pytest backend/tests/

# Frontend tests
yarn test

# Integration tests
python backend_test.py
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- D.A.I.R. AI for the original Prompt Engineering Guide
- OpenAI and Anthropic for LLM APIs
- The open-source community for tools and libraries

---

For additional support, please check the troubleshooting section or create an issue in the repository.