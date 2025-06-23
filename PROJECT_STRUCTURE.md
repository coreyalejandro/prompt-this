# 📁 Project Structure

Complete overview of the Prompt Engineering Agent Platform project structure.

## 🏗️ Root Directory Structure

```
/app/
├── 📁 backend/                 # FastAPI backend application
├── 📁 frontend/                # React frontend application  
├── 📁 docs/                    # Comprehensive documentation
├── 📁 tests/                   # Additional test files
├── 📁 scripts/                 # Utility scripts
├── 📄 README.md                # Main project documentation
├── 📄 CHANGELOG.md             # Version history and changes
├── 📄 PROJECT_STRUCTURE.md     # This file
└── 📄 yarn.lock                # Root dependencies lock file
```

## 🖥️ Backend Structure (`/app/backend/`)

### Core Files
```
backend/
├── 📄 server.py                # Main FastAPI application
├── 📄 llm_providers.py         # LLM integration layer
├── 📄 workflow_engine.py       # Workflow orchestration system
├── 📄 requirements.txt         # Python dependencies
├── 📄 .env                     # Environment variables
└── 📁 __pycache__/             # Python cache files
```

### Backend Components

#### `server.py` - Main Application
- **FastAPI Application**: Core web framework setup
- **Agent Registry**: Management of all available agents
- **API Endpoints**: RESTful endpoints for agents and workflows
- **Database Integration**: MongoDB connection and operations
- **CORS Configuration**: Cross-origin request handling
- **Error Handling**: Comprehensive exception management

**Key Classes:**
- `BaseAgent`: Abstract base class for all agents
- `AgentType`: Enumeration of available agent types
- `AgentRequest/Response`: Data models for API communication
- `WorkflowRequest/Response`: Workflow-specific data models

**Core Agents Implemented:**
- `ZeroShotAgent`: Direct prompting without examples
- `FewShotAgent`: Example-guided prompting
- `ChainOfThoughtAgent`: Step-by-step reasoning
- `SelfConsistencyAgent`: Multiple reasoning paths
- `TreeOfThoughtsAgent`: Branched reasoning exploration
- `ReActAgent`: Reasoning + action combined

**Advanced Agents Implemented:**
- `RAGAgent`: Retrieval augmented generation
- `AutoPromptAgent`: Automatic prompt optimization
- `ProgramAidedAgent`: Code-assisted problem solving
- `FactualityCheckerAgent`: Content accuracy validation

#### `llm_providers.py` - LLM Integration
- **Provider Management**: Multi-LLM provider support
- **API Integration**: OpenAI, Anthropic, and local models
- **Caching System**: KV cache for improved performance
- **Error Handling**: Provider-specific error management
- **Authentication**: API key management and validation

**Key Classes:**
- `BaseLLMProvider`: Abstract provider interface
- `OpenAIProvider`: OpenAI API integration
- `AnthropicProvider`: Anthropic API integration
- `LocalProvider`: Fallback local implementation
- `LLMProviderManager`: Central provider management

#### `workflow_engine.py` - Workflow Orchestration
- **Workflow Management**: Create, execute, and monitor workflows
- **Dependency Resolution**: Manage step dependencies
- **Result Passing**: Context flow between workflow steps
- **Parallel Execution**: Concurrent step processing
- **Status Tracking**: Real-time workflow monitoring

**Key Classes:**
- `WorkflowEngine`: Core orchestration engine
- `Workflow`: Workflow data model
- `WorkflowStep`: Individual step definition
- `WorkflowStatus`: Status enumeration

## 🖼️ Frontend Structure (`/app/frontend/`)

### Directory Layout
```
frontend/
├── 📁 public/                  # Static assets
│   ├── 📄 index.html           # Main HTML template
│   ├── 📄 favicon.ico          # Website icon
│   └── 📄 manifest.json        # PWA manifest
├── 📁 src/                     # React source code
│   ├── 📄 index.js             # Application entry point
│   ├── 📄 App.js               # Main application component
│   ├── 📄 App.css              # Application styles
│   ├── 📄 WorkflowDesigner.js  # Workflow interface
│   ├── 📄 OnboardingTutorial.js # User tutorial system
│   └── 📁 __tests__/           # Component tests
├── 📄 package.json             # Node.js dependencies
├── 📄 yarn.lock                # Dependency lock file
├── 📄 tailwind.config.js       # Tailwind CSS configuration
├── 📄 postcss.config.js        # PostCSS configuration
├── 📄 .env                     # Frontend environment variables
└── 📁 node_modules/            # Installed dependencies
```

### Frontend Components

#### `App.js` - Main Application
- **Routing System**: React Router integration
- **Navigation**: Header and footer components
- **Layout Management**: Responsive design structure
- **Agent Library**: Display and interaction with agents
- **Tutorial Integration**: Onboarding system integration

**Key Components:**
- `AgentLibrary`: Browse and select agents
- `AgentTester`: Individual agent testing interface
- `AgentInfo`: Agent documentation display
- `AgentTesterWrapper/AgentInfoWrapper`: Route parameter handling

#### `WorkflowDesigner.js` - Workflow Interface
- **Visual Designer**: Drag-and-drop workflow creation
- **Template Management**: Pre-built workflow templates
- **Workflow Execution**: Start and monitor workflows
- **Step Configuration**: Agent selection and prompt setup
- **Real-time Updates**: Live status monitoring

**Key Features:**
- Multi-tab interface (Designer, Templates, My Workflows)
- Step dependency management
- LLM provider selection per step
- Error handling and user feedback
- Workflow execution monitoring

#### `OnboardingTutorial.js` - User Tutorial
- **Interactive Tutorial**: Step-by-step platform introduction
- **Progressive Disclosure**: Gradual feature introduction
- **User Guidance**: Contextual tips and explanations
- **Tutorial Management**: Skip, restart, and progress tracking

**Tutorial Steps:**
1. Platform welcome and overview
2. Agent library introduction
3. Individual agent testing
4. Workflow orchestration concepts
5. Pre-built templates
6. Custom workflow creation
7. Advanced features
8. Completion and next steps

## 📚 Documentation Structure (`/app/docs/`)

```
docs/
├── 📄 API_DOCUMENTATION.md     # Complete API reference
├── 📄 USER_GUIDE.md            # End-user manual
├── 📄 DEVELOPER_GUIDE.md       # Developer documentation
└── 📄 TROUBLESHOOTING_GUIDE.md # Issue resolution guide
```

### Documentation Components

#### `API_DOCUMENTATION.md`
- **Endpoint Reference**: Complete API documentation
- **Request/Response Examples**: Detailed usage examples
- **Authentication**: API key and provider setup
- **Error Handling**: Error codes and messages
- **SDK Examples**: Python and JavaScript integration

#### `USER_GUIDE.md`
- **Getting Started**: First-time user setup
- **Agent Usage**: How to use each agent type
- **Workflow Creation**: Step-by-step workflow guide
- **Best Practices**: Tips for effective usage
- **Troubleshooting**: Common user issues

#### `DEVELOPER_GUIDE.md`
- **Architecture Overview**: System design and components
- **Development Setup**: Local environment configuration
- **Adding Features**: How to extend the platform
- **Testing Guidelines**: Test setup and requirements
- **Deployment**: Production deployment guide

#### `TROUBLESHOOTING_GUIDE.md`
- **Common Issues**: Frequently encountered problems
- **Diagnostic Tools**: How to identify issues
- **Resolution Steps**: Detailed fix procedures
- **Emergency Recovery**: System reset procedures
- **Getting Help**: Support resources and contacts

## 🧪 Testing Structure (`/app/tests/`)

```
tests/
├── 📄 __init__.py              # Test package initialization
├── 📄 backend_test.py          # Comprehensive backend testing
└── 📁 frontend/                # Frontend test files
    └── 📄 __tests__/           # Component tests
```

### Testing Components

#### Backend Testing
- **Unit Tests**: Individual function testing
- **Integration Tests**: API endpoint validation
- **End-to-End Tests**: Complete workflow testing
- **Performance Tests**: Load and stress testing

#### Frontend Testing
- **Component Tests**: React component validation
- **User Interface Tests**: UI interaction testing
- **Integration Tests**: API communication testing
- **Browser Compatibility**: Cross-browser validation

## 🔧 Configuration Files

### Backend Configuration
- **`.env`**: Environment variables and API keys
- **`requirements.txt`**: Python package dependencies
- **Server configuration**: FastAPI, Uvicorn, MongoDB settings

### Frontend Configuration
- **`.env`**: Frontend environment variables
- **`package.json`**: Node.js dependencies and scripts
- **`tailwind.config.js`**: Tailwind CSS customization
- **`postcss.config.js`**: CSS processing configuration

### Development Configuration
- **ESLint**: Code linting configuration
- **Prettier**: Code formatting rules
- **Git**: Version control settings
- **Docker**: Containerization configuration

## 📊 Database Schema (`MongoDB`)

### Collections

#### `agent_responses`
```javascript
{
  _id: ObjectId,
  id: String,                    // UUID for agent response
  agent_type: String,            // Type of agent used
  status: String,                // Response status
  result: String,                // Generated response
  reasoning: [String],           // Reasoning steps
  metadata: Object,              // Usage metrics and info
  error: String,                 // Error message (if any)
  created_at: Date,              // Creation timestamp
  completed_at: Date,            // Completion timestamp
  session_id: String             // Session identifier
}
```

#### `workflows`
```javascript
{
  _id: ObjectId,
  id: String,                    // UUID for workflow
  name: String,                  // Workflow name
  description: String,           // Workflow description
  status: String,                // Workflow status
  steps: [                       // Workflow steps
    {
      id: String,                // Step UUID
      name: String,              // Step name
      agent_type: String,        // Agent type
      prompt: String,            // Step prompt
      context: String,           // Additional context
      llm_provider: String,      // LLM provider
      depends_on: [String],      // Dependencies
      parameters: Object,        // Additional parameters
      status: String,            // Step status
      result: String,            // Step result
      error: String,             // Step error
      started_at: Date,          // Step start time
      completed_at: Date         // Step completion time
    }
  ],
  results: Object,               // Step results mapping
  created_at: Date,              // Creation timestamp
  started_at: Date,              // Execution start time
  completed_at: Date,            // Execution completion time
  session_id: String             // Session identifier
}
```

#### `sessions` (Future Enhancement)
```javascript
{
  _id: ObjectId,
  session_id: String,            // Session identifier
  user_id: String,               // User identifier
  created_at: Date,              // Session creation
  last_activity: Date,           // Last activity
  metadata: Object               // Session metadata
}
```

## 🚀 Deployment Structure

### Production Deployment
```
production/
├── 📁 docker/                  # Docker configuration
│   ├── 📄 Dockerfile.backend   # Backend container
│   ├── 📄 Dockerfile.frontend  # Frontend container
│   └── 📄 docker-compose.yml   # Multi-container setup
├── 📁 kubernetes/              # Kubernetes manifests
│   ├── 📄 backend-deployment.yaml
│   ├── 📄 frontend-deployment.yaml
│   └── 📄 ingress.yaml
└── 📁 scripts/                 # Deployment scripts
    ├── 📄 deploy.sh             # Deployment automation
    ├── 📄 backup.sh             # Database backup
    └── 📄 monitor.sh            # Health monitoring
```

### Environment Files
- **Development**: Local development configuration
- **Staging**: Pre-production testing environment
- **Production**: Live production configuration
- **Testing**: Isolated testing environment

## 📈 Monitoring and Logging

### Log Files
```
logs/
├── 📄 backend.log              # Backend application logs
├── 📄 frontend.log             # Frontend access logs
├── 📄 mongodb.log              # Database logs
├── 📄 nginx.log                # Web server logs (production)
└── 📄 supervisor.log           # Process management logs
```

### Monitoring Components
- **Health Checks**: Endpoint monitoring
- **Performance Metrics**: Response time tracking
- **Error Tracking**: Exception monitoring
- **Usage Analytics**: User interaction tracking

## 🔐 Security Structure

### Security Components
- **Input Validation**: Request sanitization
- **API Key Management**: Secure credential storage
- **CORS Configuration**: Cross-origin security
- **Error Sanitization**: Safe error exposure
- **Environment Isolation**: Configuration security

### Security Files
- **Environment Variables**: Secure configuration
- **SSL Certificates**: HTTPS encryption (production)
- **Firewall Rules**: Network security (production)
- **Access Logs**: Security audit trails

## 📦 Dependency Management

### Backend Dependencies
- **Core Framework**: FastAPI, Uvicorn, Pydantic
- **Database**: Motor (MongoDB), PyMongo
- **LLM Integration**: OpenAI, Anthropic
- **Testing**: pytest, coverage
- **Development**: black, flake8, mypy

### Frontend Dependencies
- **Core Framework**: React, React Router
- **Styling**: Tailwind CSS, PostCSS
- **HTTP Client**: Axios
- **Testing**: Jest, React Testing Library
- **Development**: ESLint, Prettier

### Development Tools
- **Version Control**: Git
- **Package Management**: pip (Python), yarn (Node.js)
- **Process Management**: Supervisor
- **Documentation**: Markdown
- **Containerization**: Docker

---

This project structure provides a comprehensive overview of the entire Prompt Engineering Agent Platform, enabling developers and users to quickly understand the organization and locate specific components.