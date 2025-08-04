# 🤝 Contributing to Prompt-This

We love your input! We want to make contributing to Prompt-This as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## 🚀 Quick Start

1. **Fork the repository**
2. **Clone your fork**: `git clone https://github.com/yourusername/prompt-this.git`
3. **Install dependencies**: Follow the setup guide in README.md
4. **Create a branch**: `git checkout -b feature/amazing-feature`
5. **Make your changes**: Follow our coding guidelines
6. **Test thoroughly**: Run all tests and add new ones
7. **Submit a pull request**: Use our PR template

## 📋 Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

### 🔄 Git Workflow

1. **Branch Naming**:
   - `feature/description` - New features
   - `bugfix/description` - Bug fixes
   - `hotfix/description` - Critical fixes
   - `docs/description` - Documentation updates

2. **Commit Messages**:

   ```text
   type(scope): description
   
   feat(agents): add new factuality checker agent
   fix(workflows): resolve dependency resolution bug
   docs(api): update endpoint documentation
   test(frontend): add component tests for workflow designer
   ```

3. **Pull Request Process**:
   - Use the pull request template
   - Include tests for new functionality
   - Update documentation as needed
   - Link to related issues

## 🛠️ Development Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- MongoDB 5.0+
- Git

### Local Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/prompt-this.git
cd prompt-this

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup
cd ../frontend
yarn install

# Start development servers
# Terminal 1: MongoDB
sudo systemctl start mongodb

# Terminal 2: Backend
cd backend
uvicorn server:app --reload --host 0.0.0.0 --port 8001

# Terminal 3: Frontend
cd frontend
yarn start
```

## 🧪 Testing

### Running Tests

**Backend Tests:**

```bash
cd backend
pytest                          # Run all tests
pytest --cov=.                  # Run with coverage
pytest tests/test_agents.py     # Run specific test file
pytest -v                       # Verbose output
```

**Frontend Tests:**

```bash
cd frontend
yarn test                       # Run all tests
yarn test --coverage            # Run with coverage
yarn test --watch               # Run in watch mode
```

### Test Requirements

- All new features must include tests
- Maintain >90% code coverage for backend
- Maintain >80% component coverage for frontend
- All tests must pass before merging

### Writing Tests

**Backend Test Example:**

```python
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
```

**Frontend Test Example:**

```javascript
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import App from '../App';

test('renders app header', () => {
  render(
    <BrowserRouter>
      <App />
    </BrowserRouter>
  );
  
  const header = screen.getByText(/Prompt-This/i);
  expect(header).toBeInTheDocument();
});
```

## 📝 Coding Standards

### Python (Backend)

- Follow PEP 8
- Use type hints
- Document functions with docstrings
- Use async/await for I/O operations
- Format with Black: `black .`
- Lint with flake8: `flake8 .`

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

### JavaScript (Frontend)

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

## 🔧 Adding New Features

### Adding a New Agent

1. **Define Agent Type** in `server.py`:

```python
class AgentType(str, Enum):
    # ... existing agents
    NEW_AGENT = "new_agent"
```

1. **Create Agent Class**:

```python
class NewAgent(BaseAgent):
    def __init__(self):
        super().__init__(AgentType.NEW_AGENT)
    
    async def _process_request(self, request: PromptRequest, llm_provider: LLMProvider) -> Dict[str, Any]:
        # Implementation here
        pass
```

1. **Register Agent** in `initialize_agents()`
2. **Add Tests** for the new agent
3. **Update Documentation**

### Adding a New LLM Provider

1. **Create Provider Class** in `llm_providers.py`
2. **Update Provider Manager**
3. **Add to Frontend UI**
4. **Add Tests**
5. **Update Documentation**

### Adding Frontend Components

1. **Create Component File**
2. **Add to Routing** (if needed)
3. **Add Navigation** (if needed)
4. **Write Tests**
5. **Update Documentation**

## 📚 Documentation

### What to Document

- All new features and APIs
- Breaking changes
- Setup and configuration changes
- Examples and use cases

### Documentation Files to Update

- `README.md` - Main project documentation
- `docs/API_DOCUMENTATION.md` - API reference
- `docs/USER_GUIDE.md` - User manual
- `docs/DEVELOPER_GUIDE.md` - Developer guide
- `CHANGELOG.md` - Version history

### Documentation Standards

- Use clear, concise language
- Include examples where helpful
- Keep documentation up-to-date with code changes
- Use consistent formatting

## 🐛 Bug Reports

Use the bug report template and include:

- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Environment information
- Error logs (if applicable)
- Screenshots (if helpful)

### Bug Report Checklist

- [ ] Check if issue already exists
- [ ] Use the bug report template
- [ ] Include reproduction steps
- [ ] Add relevant labels
- [ ] Provide environment details

## 💡 Feature Requests

Use the feature request template and include:

- Clear description of the feature
- Use cases and examples
- Expected impact
- Implementation considerations

### Feature Request Guidelines

- [ ] Check if feature already requested
- [ ] Use the feature request template
- [ ] Explain the use case clearly
- [ ] Consider implementation complexity
- [ ] Add relevant labels

## 🔒 Security

### Reporting Security Issues

- **DO NOT** open a public issue for security vulnerabilities
- Email security concerns to: [security@prompt-this.ai]
- Include detailed description and reproduction steps
- Allow reasonable time for response before disclosure

### Security Best Practices

- Never commit API keys or secrets
- Validate all user inputs
- Use environment variables for configuration
- Follow OWASP guidelines

## 📜 Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the project team. All complaints will be reviewed and investigated promptly and fairly.

## 🏷️ Labels and Tags

### Issue Labels

- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Improvements or additions to docs
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention is needed
- `priority: high` - High priority issue
- `priority: low` - Low priority issue

### Component Labels

- `backend` - Backend/API related
- `frontend` - Frontend/UI related
- `agents` - Agent-specific issues
- `workflows` - Workflow-related
- `docs` - Documentation related

## 🎉 Recognition

Contributors will be recognized in:

- CHANGELOG.md for significant contributions
- README.md contributors section
- Release notes for major features

## 📞 Getting Help

### Development Questions

- Create a discussion in GitHub Discussions
- Join our community chat [if available]
- Check existing issues and documentation

### Stuck on Something?

1. Check the documentation first
2. Search existing issues
3. Create a new issue with the question label
4. Be specific about what you're trying to achieve

## 📈 Project Roadmap

Check our [GitHub Projects](https://github.com/yourusername/prompt-this/projects) for:

- Current sprint goals
- Feature roadmap
- Known issues
- Future enhancements

---

Thank you for contributing to Prompt-This! 🚀

Every contribution, no matter how small, helps make Prompt-This better for everyone.
