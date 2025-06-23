# 📖 API Documentation

Complete reference for the Prompt Engineering Agent Platform API.

## Base URL
```
http://localhost:8001/api
```

## Authentication
Currently, no authentication is required. API keys for LLM providers are configured server-side.

## Response Format

All API responses follow this consistent format:

```json
{
  "id": "unique-identifier",
  "status": "completed|processing|failed",
  "result": "Generated response text",
  "reasoning": ["Step 1", "Step 2", "..."],
  "metadata": {
    "technique": "agent_type",
    "model": "gpt-4o-mini",
    "usage": {
      "prompt_tokens": 123,
      "completion_tokens": 456,
      "total_tokens": 579
    }
  },
  "error": null,
  "created_at": "2025-01-01T12:00:00Z",
  "completed_at": "2025-01-01T12:00:05Z"
}
```

## Agent Endpoints

### List All Agents
Get information about all available agents.

**Request:**
```http
GET /api/agents
```

**Response:**
```json
{
  "agents": [
    {
      "type": "zero_shot",
      "name": "Zero Shot",
      "description": "Performs tasks without examples, relying on the model's pre-trained knowledge"
    },
    {
      "type": "few_shot",
      "name": "Few Shot", 
      "description": "Uses provided examples to guide the model's response generation"
    }
    // ... more agents
  ]
}
```

### Get Agent Information
Get detailed information about a specific agent.

**Request:**
```http
GET /api/agents/{agent_type}
```

**Parameters:**
- `agent_type` (path): Agent identifier (e.g., "zero_shot", "chain_of_thought")

**Response:**
```json
{
  "type": "zero_shot",
  "name": "Zero Shot",
  "description": "Performs tasks without examples, relying on the model's pre-trained knowledge"
}
```

### Process Agent Request
Execute a prompt using a specific agent.

**Request:**
```http
POST /api/agents/process
Content-Type: application/json

{
  "agent_type": "zero_shot",
  "llm_provider": "openai",
  "request": {
    "prompt": "Explain quantum computing in simple terms",
    "context": "Target audience: high school students",
    "examples": [
      {
        "input": "Explain gravity",
        "output": "Gravity is the force that pulls objects toward each other..."
      }
    ],
    "parameters": {
      "temperature": 0.7,
      "max_tokens": 1000
    }
  },
  "session_id": "optional-session-identifier"
}
```

**Parameters:**
- `agent_type` (required): Type of agent to use
- `llm_provider` (required): LLM provider ("openai", "anthropic", "local")
- `request.prompt` (required): The main prompt/question
- `request.context` (optional): Additional context for the prompt
- `request.examples` (optional): Examples for few-shot learning
- `request.parameters` (optional): Additional parameters for the LLM
- `session_id` (optional): Session identifier for tracking

**Agent Types:**
- `zero_shot`: Direct prompting without examples
- `few_shot`: Example-guided prompting
- `chain_of_thought`: Step-by-step reasoning
- `self_consistency`: Multiple reasoning paths
- `tree_of_thoughts`: Branched reasoning exploration
- `react`: Reasoning + action combined
- `rag`: Retrieval augmented generation
- `auto_prompt`: Automatic prompt optimization
- `program_aided`: Code-assisted problem solving
- `factuality_checker`: Content accuracy validation

**LLM Providers:**
- `openai`: OpenAI GPT models (requires API key)
- `anthropic`: Anthropic Claude models (requires API key)
- `local`: Local/placeholder model (always available)

## Workflow Endpoints

### Create Workflow
Create a new multi-agent workflow.

**Request:**
```http
POST /api/workflows
Content-Type: application/json

{
  "name": "Content Analysis Pipeline",
  "description": "Analyze content using multiple agents",
  "steps": [
    {
      "name": "Initial Analysis",
      "agent_type": "zero_shot",
      "prompt": "Analyze this content: {content}",
      "context": "Focus on main themes",
      "llm_provider": "openai",
      "depends_on": [],
      "parameters": {
        "temperature": 0.5
      }
    },
    {
      "name": "Deep Dive",
      "agent_type": "chain_of_thought",
      "prompt": "Provide detailed analysis",
      "llm_provider": "anthropic",
      "depends_on": ["Initial Analysis"]
    }
  ],
  "session_id": "workflow-session-123"
}
```

**Parameters:**
- `name` (required): Workflow name
- `description` (optional): Workflow description
- `steps` (required): Array of workflow steps
- `steps[].name` (required): Step name
- `steps[].agent_type` (required): Agent to use for this step
- `steps[].prompt` (required): Prompt for this step
- `steps[].context` (optional): Additional context
- `steps[].llm_provider` (optional): LLM provider (default: "openai")
- `steps[].depends_on` (optional): Array of step names this depends on
- `steps[].parameters` (optional): Additional parameters

**Response:**
```json
{
  "id": "workflow-id-123",
  "name": "Content Analysis Pipeline",
  "description": "Analyze content using multiple agents",
  "status": "pending",
  "steps": [
    {
      "id": "step-id-1",
      "name": "Initial Analysis",
      "status": "waiting",
      "agent_type": "zero_shot",
      "prompt": "Analyze this content: {content}",
      "result": null,
      "error": null
    }
  ],
  "created_at": "2025-01-01T12:00:00Z",
  "results": {}
}
```

### Execute Workflow
Start execution of a workflow.

**Request:**
```http
POST /api/workflows/{workflow_id}/execute
```

**Parameters:**
- `workflow_id` (path): ID of the workflow to execute

**Response:**
```json
{
  "message": "Workflow execution started",
  "workflow_id": "workflow-id-123"
}
```

### Get Workflow Status
Get current status and results of a workflow.

**Request:**
```http
GET /api/workflows/{workflow_id}
```

**Parameters:**
- `workflow_id` (path): ID of the workflow

**Response:**
```json
{
  "id": "workflow-id-123",
  "name": "Content Analysis Pipeline",
  "status": "completed",
  "steps": [
    {
      "id": "step-id-1",
      "name": "Initial Analysis",
      "status": "completed",
      "result": "Analysis result here...",
      "reasoning": ["Applied zero-shot technique"],
      "started_at": "2025-01-01T12:00:00Z",
      "completed_at": "2025-01-01T12:00:05Z"
    }
  ],
  "results": {
    "step-id-1": {
      "result": "Analysis result...",
      "metadata": {...}
    }
  },
  "created_at": "2025-01-01T12:00:00Z",
  "completed_at": "2025-01-01T12:01:00Z"
}
```

### List Workflows
Get list of all workflows.

**Request:**
```http
GET /api/workflows?active_only=false
```

**Parameters:**
- `active_only` (query, optional): Only return active workflows (default: false)

**Response:**
```json
{
  "workflows": [
    {
      "id": "workflow-id-123",
      "name": "Content Analysis Pipeline",
      "status": "completed",
      "created_at": "2025-01-01T12:00:00Z",
      "steps": [...],
      "session_id": "session-123"
    }
  ]
}
```

### Cancel Workflow
Cancel an active workflow.

**Request:**
```http
DELETE /api/workflows/{workflow_id}
```

**Parameters:**
- `workflow_id` (path): ID of the workflow to cancel

**Response:**
```json
{
  "message": "Workflow workflow-id-123 cancelled"
}
```

### Get Workflow Templates
Get pre-built workflow templates.

**Request:**
```http
GET /api/workflow-templates
```

**Response:**
```json
{
  "templates": [
    {
      "id": "analysis_pipeline",
      "name": "Content Analysis Pipeline",
      "description": "Analyze content using multiple agents",
      "steps": [
        {
          "name": "Zero-Shot Analysis",
          "agent_type": "zero_shot",
          "prompt": "Provide initial analysis of: {content}",
          "llm_provider": "openai"
        },
        {
          "name": "Chain-of-Thought Deep Dive",
          "agent_type": "chain_of_thought",
          "prompt": "Provide detailed step-by-step analysis",
          "depends_on": ["Zero-Shot Analysis"],
          "llm_provider": "anthropic"
        }
      ]
    }
  ]
}
```

## Session Endpoints

### Get Session History
Get history of requests for a specific session.

**Request:**
```http
GET /api/sessions/{session_id}/history
```

**Parameters:**
- `session_id` (path): Session identifier

**Response:**
```json
{
  "session_id": "session-123",
  "responses": [
    {
      "id": "response-id-1",
      "agent_type": "zero_shot",
      "result": "Response text...",
      "created_at": "2025-01-01T12:00:00Z"
    }
  ]
}
```

## Error Responses

### HTTP Status Codes
- `200`: Success
- `400`: Bad Request (invalid parameters)
- `404`: Not Found (agent/workflow not found)
- `422`: Validation Error (invalid request format)
- `500`: Internal Server Error

### Error Format
```json
{
  "detail": "Error message describing what went wrong",
  "status_code": 400,
  "error_type": "validation_error"
}
```

### Common Errors

#### Invalid Agent Type
```json
{
  "detail": "Agent 'invalid_agent' not found",
  "status_code": 404
}
```

#### Missing Required Parameters
```json
{
  "detail": "Field 'prompt' is required",
  "status_code": 422
}
```

#### LLM Provider Error
```json
{
  "detail": "Provider 'openai' not available - check API key configuration",
  "status_code": 400
}
```

## Rate Limiting

Currently, there are no rate limits imposed by the platform. However, underlying LLM providers (OpenAI, Anthropic) have their own rate limits.

**Best Practices:**
- Use the `local` provider for testing and development
- Implement client-side delays between requests
- Cache results when possible
- Monitor usage through provider dashboards

## Examples

### Basic Agent Usage

**Simple Question:**
```bash
curl -X POST "http://localhost:8001/api/agents/process" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_type": "zero_shot",
    "llm_provider": "openai",
    "request": {
      "prompt": "What is machine learning?"
    }
  }'
```

**Few-Shot Classification:**
```bash
curl -X POST "http://localhost:8001/api/agents/process" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_type": "few_shot",
    "llm_provider": "openai",
    "request": {
      "prompt": "Classify sentiment: This product is amazing!",
      "examples": [
        {"input": "I love this!", "output": "positive"},
        {"input": "This is terrible", "output": "negative"}
      ]
    }
  }'
```

**Chain-of-Thought Reasoning:**
```bash
curl -X POST "http://localhost:8001/api/agents/process" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_type": "chain_of_thought",
    "llm_provider": "anthropic",
    "request": {
      "prompt": "If a train travels 60 mph for 2.5 hours, how far does it go?"
    }
  }'
```

### Workflow Creation and Execution

**Create Simple Workflow:**
```bash
curl -X POST "http://localhost:8001/api/workflows" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Simple Analysis",
    "steps": [
      {
        "name": "Initial Review",
        "agent_type": "zero_shot",
        "prompt": "Review this content: Machine learning is transforming industries",
        "llm_provider": "openai"
      },
      {
        "name": "Detailed Analysis",
        "agent_type": "chain_of_thought",
        "prompt": "Provide detailed analysis of the content",
        "depends_on": ["Initial Review"],
        "llm_provider": "anthropic"
      }
    ]
  }'
```

**Execute Workflow:**
```bash
curl -X POST "http://localhost:8001/api/workflows/WORKFLOW_ID/execute"
```

**Check Status:**
```bash
curl -X GET "http://localhost:8001/api/workflows/WORKFLOW_ID"
```

## SDK Examples

### Python SDK Example
```python
import requests
import json

class PromptEngineeringClient:
    def __init__(self, base_url="http://localhost:8001/api"):
        self.base_url = base_url
    
    def process_agent(self, agent_type, prompt, llm_provider="openai", **kwargs):
        response = requests.post(
            f"{self.base_url}/agents/process",
            json={
                "agent_type": agent_type,
                "llm_provider": llm_provider,
                "request": {
                    "prompt": prompt,
                    **kwargs
                }
            }
        )
        return response.json()
    
    def create_workflow(self, name, steps, description=None):
        response = requests.post(
            f"{self.base_url}/workflows",
            json={
                "name": name,
                "description": description,
                "steps": steps
            }
        )
        return response.json()
    
    def execute_workflow(self, workflow_id):
        response = requests.post(
            f"{self.base_url}/workflows/{workflow_id}/execute"
        )
        return response.json()

# Usage
client = PromptEngineeringClient()

# Test an agent
result = client.process_agent(
    agent_type="zero_shot",
    prompt="Explain artificial intelligence",
    llm_provider="openai"
)
print(result["result"])

# Create and execute workflow
workflow = client.create_workflow(
    name="AI Explanation Pipeline",
    steps=[
        {
            "name": "Basic Explanation",
            "agent_type": "zero_shot",
            "prompt": "Explain AI in simple terms",
            "llm_provider": "openai"
        },
        {
            "name": "Technical Details",
            "agent_type": "chain_of_thought",
            "prompt": "Provide technical details about AI",
            "depends_on": ["Basic Explanation"],
            "llm_provider": "anthropic"
        }
    ]
)

execution = client.execute_workflow(workflow["id"])
print(f"Workflow started: {execution['message']}")
```

### JavaScript SDK Example
```javascript
class PromptEngineeringClient {
  constructor(baseUrl = "http://localhost:8001/api") {
    this.baseUrl = baseUrl;
  }

  async processAgent(agentType, prompt, llmProvider = "openai", options = {}) {
    const response = await fetch(`${this.baseUrl}/agents/process`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        agent_type: agentType,
        llm_provider: llmProvider,
        request: {
          prompt,
          ...options
        }
      })
    });
    return await response.json();
  }

  async createWorkflow(name, steps, description = null) {
    const response = await fetch(`${this.baseUrl}/workflows`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name,
        description,
        steps
      })
    });
    return await response.json();
  }

  async executeWorkflow(workflowId) {
    const response = await fetch(`${this.baseUrl}/workflows/${workflowId}/execute`, {
      method: "POST"
    });
    return await response.json();
  }
}

// Usage
const client = new PromptEngineeringClient();

// Test an agent
const result = await client.processAgent(
  "chain_of_thought",
  "Solve this math problem: 25 * 4 + 10",
  "openai"
);
console.log(result.result);

// Create workflow
const workflow = await client.createWorkflow(
  "Problem Solving Pipeline",
  [
    {
      name: "Initial Attempt",
      agent_type: "zero_shot",
      prompt: "Solve: 25 * 4 + 10",
      llm_provider: "openai"
    },
    {
      name: "Verification",
      agent_type: "chain_of_thought",
      prompt: "Verify the solution step by step",
      depends_on: ["Initial Attempt"],
      llm_provider: "anthropic"
    }
  ]
);

await client.executeWorkflow(workflow.id);
```

## WebSocket Support (Future)

Currently, all API communication is HTTP-based. WebSocket support for real-time workflow monitoring is planned for future releases.

## Versioning

The API follows semantic versioning. Current version is v1. Breaking changes will result in a new version (v2, v3, etc.) with appropriate migration guides.

---

For more examples and advanced usage, see the main README.md file.