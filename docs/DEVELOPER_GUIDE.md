# 👨‍💻 Developer Guide

Complete guide for developers working on the Prompt-This Platform.

## 🏗️ Architecture Overview

### System Design

The platform follows a modular microservices architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React)                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │ Agent       │  │ Workflow    │  │ Onboarding          │ │
│  │ Library     │  │ Designer    │  │ Tutorial            │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                         HTTP/REST API
                              │
┌─────────────────────────────────────────────────────────────┐
│                  Backend (FastAPI)                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │ Agent       │  │ Workflow    │  │ LLM Provider        │ │
│  │ Registry    │  │ Engine      │  │ Manager             │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                         MongoDB Driver
                              │
┌─────────────────────────────────────────────────────────────┐
│                     MongoDB                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │ Workflows   │  │ Responses   │  │ Sessions            │ │
│  │ Collection  │  │ Collection  │  │ Collection          │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Core Components

#### Backend Components

**1. Agent System (`server.py`)**
- `BaseAgent`: Abstract base class for all agents
- `AgentRegistry`: Manages available agents
- Agent implementations for each prompt engineering technique

**2. Workflow Engine (`workflow_engine.py`)**
- `WorkflowEngine`: Orchestrates multi-agent workflows
- `Workflow`: Data model for workflow definitions
- `WorkflowStep`: Individual step in a workflow
- Dependency management and result passing

**3. LLM Integration (`llm_providers.py`)**
- `LLMProviderManager`: Manages multiple LLM providers
- Provider implementations for OpenAI, Anthropic, Local
- Caching and error handling

#### Frontend Components

**1. Main Application (`App.js`)**
- Routing and navigation
- Global state management
- Integration with onboarding tutorial

**2. Agent Interface**
- `AgentLibrary`: Displays available agents
- `AgentTester`: Individual agent testing interface
- `AgentInfo`: Agent documentation and details

**3. Workflow Interface (`WorkflowDesigner.js`)**
- Workflow creation and editing
- Template management
- Execution monitoring

**4. Onboarding (`OnboardingTutorial.js`)**
- Interactive tutorial system
- Progressive disclosure of features
- User guidance and tips

## 🔧 Development Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- MongoDB 5.0+
- Git

### Local Development Environment

**1. Clone and Setup**
```bash
git clone <repository-url>
cd prompt-this

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install -g yarn
yarn install
```

**2. Environment Configuration**
```bash
# Backend environment
cp backend/.env.example backend/.env
# Edit backend/.env with your API keys

# Frontend environment  
cp frontend/.env.example frontend/.env
# Edit frontend/.env if needed
```

**3. Start Development Servers**
```bash
# Terminal 1: MongoDB
sudo systemctl start mongodb

# Terminal 2: Backend
cd backend
uvicorn server:app --reload --host 0.0.0.0 --port 8001

# Terminal 3: Frontend
cd frontend
yarn start
```

### Development Tools

**Backend Tools:**
- **FastAPI**: Web framework with automatic API documentation
- **Uvicorn**: ASGI server with hot reload
- **Motor**: Async MongoDB driver
- **Pydantic**: Data validation and serialization
- **pytest**: Testing framework

**Frontend Tools:**
- **React 19**: Latest React with hooks
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client for API calls
- **React Router**: Client-side routing
- **ESLint**: Code linting and formatting

**Development Commands:**
```bash
# Backend
pip install -r requirements.txt    # Install dependencies
uvicorn server:app --reload        # Start dev server
pytest                             # Run tests
black .                            # Format code
flake8 .                           # Lint code

# Frontend
yarn install                       # Install dependencies
yarn start                         # Start dev server
yarn test                          # Run tests
yarn build                         # Build for production
yarn lint                          # Lint code
```

## 🔨 Adding New Features

### Adding a New Agent

**1. Define Agent Type**
```python
# In server.py, add to AgentType enum
class AgentType(str, Enum):
    # ... existing agents
    NEW_AGENT = "new_agent"
```

**2. Create Agent Class**
```python
class NewAgent(BaseAgent):
    def __init__(self):
        super().__init__(AgentType.NEW_AGENT)
    
    def _get_description(self) -> str:
        return "Description of what this agent does"
    
    async def _process_request(self, request: PromptRequest, llm_provider: LLMProvider) -> Dict[str, Any]:
        # Implement agent-specific logic
        enhanced_prompt = f"Enhanced prompt: {request.prompt}"
        
        try:
            # Use LLM provider
            llm_response = await llm_manager.generate_response(
                provider_type=llm_provider,
                prompt=enhanced_prompt,
                max_tokens=1000,
                temperature=0.7
            )
            
            result = llm_response["response"]
            reasoning = ["Step 1: Did something", "Step 2: Did something else"]
            metadata = {
                "technique": "new_agent",
                "model": llm_response.get("model", "unknown"),
                "usage": llm_response.get("usage", {})
            }
            
        except Exception as e:
            logger.error(f"LLM call failed: {str(e)}")
            # Fallback implementation
            result = f"Fallback response for: {request.prompt}"
            reasoning = ["Applied new agent technique"]
            metadata = {"technique": "new_agent", "error": str(e)}
        
        return {
            "result": result,
            "reasoning": reasoning,
            "metadata": metadata
        }
```

**3. Register Agent**
```python
# In initialize_agents() function
def initialize_agents():
    agents = [
        # ... existing agents
        NewAgent()
    ]
    
    for agent in agents:
        AGENT_REGISTRY[agent.agent_type] = agent
```

**4. Add Tests**
```python
# In tests/test_agents.py
async def test_new_agent():
    agent = NewAgent()
    request = PromptRequest(prompt="Test prompt")
    response = await agent.process(request, LLMProvider.LOCAL)
    
    assert response.status == AgentStatus.COMPLETED
    assert response.result is not None
    assert "new_agent" in response.metadata["technique"]
```

### Adding a New LLM Provider

**1. Create Provider Class**
```python
# In llm_providers.py
class NewProvider(BaseLLMProvider):
    def __init__(self):
        super().__init__(LLMProvider.NEW_PROVIDER)
        self.client = None
        self.cache = {}
    
    async def initialize(self) -> bool:
        try:
            api_key = os.getenv("NEW_PROVIDER_API_KEY")
            if not api_key:
                logger.error("NEW_PROVIDER_API_KEY not found")
                return False
            
            # Initialize client
            self.client = NewProviderClient(api_key=api_key)
            self.initialized = True
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize new provider: {str(e)}")
            return False
    
    async def generate_response(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7, **kwargs) -> Dict[str, Any]:
        if not self.initialized:
            raise RuntimeError("New provider not initialized")
        
        try:
            # Make API call
            response = await self.client.generate(
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return {
                "response": response.text,
                "model": response.model,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                },
                "provider": "new_provider"
            }
            
        except Exception as e:
            logger.error(f"New provider API error: {str(e)}")
            raise e
```

**2. Update Provider Manager**
```python
# In LLMProviderManager.initialize_all_providers()
async def initialize_all_providers(self) -> Dict[LLMProvider, bool]:
    results = {}
    
    # ... existing providers
    
    # Initialize new provider
    new_provider = NewProvider()
    results[LLMProvider.NEW_PROVIDER] = await new_provider.initialize()
    if results[LLMProvider.NEW_PROVIDER]:
        self.providers[LLMProvider.NEW_PROVIDER] = new_provider
    
    return results
```

**3. Update Frontend**
```javascript
// In frontend components, add to provider options
<select>
  <option value="openai">OpenAI</option>
  <option value="anthropic">Anthropic</option>
  <option value="local">Local</option>
  <option value="new_provider">New Provider</option>
</select>
```

### Adding New API Endpoints

**1. Define Pydantic Models**
```python
# In server.py
class NewFeatureRequest(BaseModel):
    name: str
    parameters: Dict[str, Any]

class NewFeatureResponse(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    result: str
    status: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

**2. Create Endpoint**
```python
@api_router.post("/new-feature")
async def new_feature_endpoint(request: NewFeatureRequest):
    """New feature endpoint"""
    try:
        # Process request
        result = process_new_feature(request)
        
        response = NewFeatureResponse(
            result=result,
            status="completed"
        )
        
        # Store in database
        await db.new_features.insert_one(response.dict())
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/new-feature/{feature_id}")
async def get_new_feature(feature_id: str):
    """Get new feature by ID"""
    feature = await db.new_features.find_one({"id": feature_id})
    if not feature:
        raise HTTPException(status_code=404, detail="Feature not found")
    
    return serialize_doc(feature)
```

**3. Add Frontend Integration**
```javascript
// In appropriate React component
const callNewFeature = async (data) => {
  try {
    const response = await axios.post(`${API}/new-feature`, data);
    return response.data;
  } catch (error) {
    console.error("Error calling new feature:", error);
    throw error;
  }
};
```

### Adding Frontend Components

**1. Create Component File**
```javascript
// frontend/src/NewComponent.js
import React, { useState, useEffect } from "react";
import axios from "axios";

const NewComponent = ({ prop1, prop2 }) => {
  const [state, setState] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Component initialization
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/data`);
      setState(response.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-center">Loading...</div>;
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">New Component</h1>
      {/* Component content */}
    </div>
  );
};

export default NewComponent;
```

**2. Add to Routing**
```javascript
// In App.js
import NewComponent from "./NewComponent";

// Add to routes
<Routes>
  {/* Existing routes */}
  <Route path="/new-feature" element={<NewComponent />} />
</Routes>
```

**3. Add Navigation**
```javascript
// In navigation section
<nav className="flex space-x-6">
  {/* Existing nav items */}
  <Link to="/new-feature" className="text-gray-600 hover:text-gray-800">
    New Feature
  </Link>
</nav>
```

## 🧪 Testing

### Backend Testing

**Unit Tests (`backend/tests/`)**
```python
# test_agents.py
import pytest
from server import ZeroShotAgent, PromptRequest, LLMProvider

@pytest.mark.asyncio
async def test_zero_shot_agent():
    agent = ZeroShotAgent()
    request = PromptRequest(prompt="Test prompt")
    
    response = await agent.process(request, LLMProvider.LOCAL)
    
    assert response.status == "completed"
    assert response.result is not None
    assert response.agent_type == "zero_shot"

# test_workflows.py
import pytest
from workflow_engine import WorkflowEngine

@pytest.mark.asyncio
async def test_workflow_creation():
    engine = WorkflowEngine({})
    
    workflow = await engine.create_workflow(
        name="Test Workflow",
        steps=[{
            "name": "Test Step",
            "agent_type": "zero_shot",
            "prompt": "Test prompt"
        }]
    )
    
    assert workflow.name == "Test Workflow"
    assert len(workflow.steps) == 1
```

**Integration Tests**
```python
# test_api.py
import pytest
from fastapi.testclient import TestClient
from server import app

client = TestClient(app)

def test_get_agents():
    response = client.get("/api/agents")
    assert response.status_code == 200
    assert "agents" in response.json()

def test_process_agent():
    response = client.post("/api/agents/process", json={
        "agent_type": "zero_shot",
        "llm_provider": "local",
        "request": {"prompt": "Test prompt"}
    })
    assert response.status_code == 200
```

**Running Backend Tests**
```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_agents.py

# Run with verbose output
pytest -v
```

### Frontend Testing

**Component Tests (`frontend/src/__tests__/`)**
```javascript
// App.test.js
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import App from '../App';

test('renders app header', () => {
  render(
    <BrowserRouter>
      <App />
    </BrowserRouter>
  );
  
  const header = screen.getByText(/Prompt Engineering Agent Platform/i);
  expect(header).toBeInTheDocument();
});

// AgentLibrary.test.js
import { render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import AgentLibrary from '../AgentLibrary';

jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

test('loads and displays agents', async () => {
  const mockAgents = {
    agents: [
      { type: 'zero_shot', name: 'Zero Shot', description: 'Test description' }
    ]
  };
  
  mockedAxios.get.mockResolvedValue({ data: mockAgents });
  
  render(<AgentLibrary />);
  
  await waitFor(() => {
    expect(screen.getByText('Zero Shot')).toBeInTheDocument();
  });
});
```

**Running Frontend Tests**
```bash
cd frontend

# Run all tests
yarn test

# Run with coverage
yarn test --coverage

# Run in watch mode
yarn test --watch
```

### End-to-End Testing

**Using the Testing Agent**
```python
# backend_test.py (already created)
python backend_test.py
```

**Manual Testing Checklist**
```
□ All agents respond correctly
□ Workflow creation works
□ Workflow execution completes
□ Templates load properly
□ Error handling displays messages
□ Navigation works correctly
□ Onboarding tutorial functions
□ Mobile responsiveness works
```

## 📦 Deployment

### Production Build

**Backend Preparation**
```bash
cd backend

# Install production dependencies
pip install -r requirements.txt

# Run tests
pytest

# Check code quality
flake8 .
black --check .
```

**Frontend Preparation**
```bash
cd frontend

# Install dependencies
yarn install

# Run tests
yarn test --watchAll=false

# Build for production
yarn build

# Test production build
serve -s build -l 3000
```

### Environment Configuration

**Production Environment Variables**
```bash
# backend/.env
MONGO_URL=mongodb://production-mongo:27017
DB_NAME=production_database
OPENAI_API_KEY=prod_openai_key
ANTHROPIC_API_KEY=prod_anthropic_key

# frontend/.env
REACT_APP_BACKEND_URL=https://api.yourdomain.com
```

### Docker Deployment

**Backend Dockerfile**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8001"]
```

**Frontend Dockerfile**
```dockerfile
FROM node:18-alpine as build

WORKDIR /app

COPY package.json yarn.lock ./
RUN yarn install

COPY . .
RUN yarn build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

**Docker Compose**
```yaml
version: '3.8'

services:
  mongodb:
    image: mongo:5.0
    volumes:
      - mongodb_data:/data/db
    ports:
      - "27017:27017"

  backend:
    build: ./backend
    ports:
      - "8001:8001"
    environment:
      - MONGO_URL=mongodb://mongodb:27017
    depends_on:
      - mongodb

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend

volumes:
  mongodb_data:
```

### Monitoring and Logging

**Application Monitoring**
```python
# In server.py, add monitoring
import time
from fastapi import Request

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    logger.info(f"{request.method} {request.url} - {response.status_code} - {process_time:.2f}s")
    return response
```

**Health Check Endpoints**
```python
@api_router.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        await db.command("ping")
        
        # Test LLM providers
        providers = await llm_manager.initialize_all_providers()
        
        return {
            "status": "healthy",
            "database": "connected",
            "providers": providers,
            "timestamp": datetime.utcnow()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow()
        }
```

## 🔐 Security Considerations

### API Security

**Input Validation**
- All inputs validated using Pydantic models
- SQL injection prevention through ODM
- Cross-site scripting (XSS) prevention

**Rate Limiting** (Future Enhancement)
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@api_router.post("/agents/process")
@limiter.limit("10/minute")
async def process_agent_request(request: Request, agent_request: AgentRequest):
    # Existing implementation
```

### Data Security

**API Key Management**
- API keys stored in environment variables
- Never logged or exposed in responses
- Separate keys for different environments

**Data Sanitization**
```python
def sanitize_input(text: str) -> str:
    """Sanitize user input"""
    # Remove potential script injections
    text = re.sub(r'<script.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    # Remove SQL injection attempts
    text = re.sub(r'(union|select|insert|delete|drop|create|alter)\s', '', text, flags=re.IGNORECASE)
    return text.strip()
```

### Frontend Security

**Environment Variables**
```javascript
// Only expose REACT_APP_ prefixed variables
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
// Never expose API keys in frontend
```

**Content Security Policy**
```html
<!-- In public/index.html -->
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';">
```

## 📊 Performance Optimization

### Backend Optimization

**Async Processing**
```python
# Use async/await throughout
async def process_multiple_agents(requests: List[AgentRequest]):
    tasks = [process_single_agent(req) for req in requests]
    results = await asyncio.gather(*tasks)
    return results
```

**Caching Strategy**
```python
# Implement Redis caching
import redis
import json

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

async def cached_llm_call(prompt: str, provider: str, cache_ttl: int = 3600):
    cache_key = f"llm:{provider}:{hash(prompt)}"
    
    # Check cache
    cached_result = redis_client.get(cache_key)
    if cached_result:
        return json.loads(cached_result)
    
    # Make LLM call
    result = await llm_manager.generate_response(provider, prompt)
    
    # Cache result
    redis_client.setex(cache_key, cache_ttl, json.dumps(result))
    
    return result
```

**Database Optimization**
```python
# Create indexes for common queries
async def create_indexes():
    await db.workflows.create_index([("created_at", -1)])
    await db.agent_responses.create_index([("session_id", 1)])
    await db.agent_responses.create_index([("agent_type", 1), ("created_at", -1)])
```

### Frontend Optimization

**Code Splitting**
```javascript
// Lazy load components
import { lazy, Suspense } from 'react';

const WorkflowDesigner = lazy(() => import('./WorkflowDesigner'));

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <WorkflowDesigner />
    </Suspense>
  );
}
```

**Memoization**
```javascript
import { memo, useMemo, useCallback } from 'react';

const AgentCard = memo(({ agent, onSelect }) => {
  const handleClick = useCallback(() => {
    onSelect(agent.type);
  }, [agent.type, onSelect]);

  return (
    <div onClick={handleClick}>
      {agent.name}
    </div>
  );
});

const AgentLibrary = () => {
  const sortedAgents = useMemo(() => {
    return agents.sort((a, b) => a.name.localeCompare(b.name));
  }, [agents]);

  return (
    <div>
      {sortedAgents.map(agent => (
        <AgentCard key={agent.type} agent={agent} onSelect={onSelect} />
      ))}
    </div>
  );
};
```

## 🔄 Contributing Guidelines

### Code Style

**Python (Backend)**
- Follow PEP 8
- Use type hints
- Document functions with docstrings
- Use async/await for I/O operations

```python
async def process_agent_request(
    agent_type: AgentType, 
    request: PromptRequest, 
    llm_provider: LLMProvider
) -> AgentResponse:
    """
    Process a request using the specified agent.
    
    Args:
        agent_type: Type of agent to use
        request: The prompt request data
        llm_provider: LLM provider to use
    
    Returns:
        AgentResponse: The processed response
    
    Raises:
        ValueError: If agent type is not found
    """
    # Implementation here
```

**JavaScript (Frontend)**
- Use functional components with hooks
- Follow ESLint configuration
- Use descriptive variable names
- Document complex functions

```javascript
/**
 * Fetches and processes agent data from the API
 * @param {string} agentType - The type of agent to fetch
 * @param {Object} options - Additional options for the request
 * @returns {Promise<Object>} The agent response data
 */
const fetchAgentData = useCallback(async (agentType, options = {}) => {
  try {
    const response = await axios.get(`${API}/agents/${agentType}`, {
      params: options
    });
    return response.data;
  } catch (error) {
    console.error(`Error fetching agent ${agentType}:`, error);
    throw error;
  }
}, []);
```

### Git Workflow

**Branch Naming**
- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `hotfix/description` - Critical fixes
- `docs/description` - Documentation updates

**Commit Messages**
```
type(scope): description

feat(agents): add new factuality checker agent
fix(workflows): resolve dependency resolution bug
docs(api): update endpoint documentation
test(frontend): add component tests for workflow designer
```

**Pull Request Process**
1. Create feature branch from main
2. Implement changes with tests
3. Update documentation if needed
4. Submit PR with detailed description
5. Address review feedback
6. Merge after approval

### Testing Requirements

**All Changes Must Include:**
- Unit tests for new functions
- Integration tests for API changes
- Component tests for UI changes
- Updated documentation

**Test Coverage Goals:**
- Backend: >90% code coverage
- Frontend: >80% component coverage
- Critical paths: 100% coverage

---

This developer guide provides the foundation for contributing to and extending the Prompt-This Platform. For specific implementation questions, refer to the existing codebase and follow established patterns.