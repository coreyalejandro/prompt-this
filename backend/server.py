from fastapi import FastAPI, APIRouter, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Literal
import uuid
from datetime import datetime
from enum import Enum
import asyncio
import json
from llm_providers import LLMProviderManager, llm_manager

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app
app = FastAPI(title="Prompt Engineering Agent Platform", version="1.0.0")
api_router = APIRouter(prefix="/api")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Enums and Models
class AgentType(str, Enum):
    ZERO_SHOT = "zero_shot"
    FEW_SHOT = "few_shot"
    CHAIN_OF_THOUGHT = "chain_of_thought"
    SELF_CONSISTENCY = "self_consistency"
    TREE_OF_THOUGHTS = "tree_of_thoughts"
    REACT = "react"

class LLMProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    LOCAL = "local"

class AgentStatus(str, Enum):
    IDLE = "idle"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class PromptRequest(BaseModel):
    prompt: str
    context: Optional[str] = None
    examples: Optional[List[Dict[str, str]]] = None
    parameters: Optional[Dict[str, Any]] = None

class AgentRequest(BaseModel):
    agent_type: AgentType
    llm_provider: LLMProvider = LLMProvider.OPENAI
    request: PromptRequest
    session_id: Optional[str] = None

class AgentResponse(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    agent_type: AgentType
    status: AgentStatus
    result: Optional[str] = None
    reasoning: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None

class WorkflowStep(BaseModel):
    agent_type: AgentType
    request: PromptRequest
    depends_on: Optional[List[str]] = None

class WorkflowRequest(BaseModel):
    name: str
    steps: List[WorkflowStep]
    llm_provider: LLMProvider = LLMProvider.OPENAI
    session_id: Optional[str] = None

class WorkflowResponse(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    status: AgentStatus
    steps: List[AgentResponse]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None

# Agent Registry
AGENT_REGISTRY = {}

class BaseAgent:
    def __init__(self, agent_type: AgentType):
        self.agent_type = agent_type
        self.name = agent_type.value.replace('_', ' ').title()
        self.description = self._get_description()
    
    def _get_description(self) -> str:
        descriptions = {
            AgentType.ZERO_SHOT: "Performs tasks without examples, relying on the model's pre-trained knowledge",
            AgentType.FEW_SHOT: "Uses provided examples to guide the model's response generation",
            AgentType.CHAIN_OF_THOUGHT: "Breaks down complex problems into step-by-step reasoning",
            AgentType.SELF_CONSISTENCY: "Generates multiple reasoning paths and selects the most consistent answer",
            AgentType.TREE_OF_THOUGHTS: "Explores multiple reasoning branches like a search tree",
            AgentType.REACT: "Combines reasoning and action-taking capabilities"
        }
        return descriptions.get(self.agent_type, "Specialized prompt engineering agent")
    
    async def process(self, request: PromptRequest, llm_provider: LLMProvider) -> AgentResponse:
        """Process a request and return response"""
        response = AgentResponse(
            agent_type=self.agent_type,
            status=AgentStatus.PROCESSING
        )
        
        try:
            # Simulate processing - will be replaced with actual LLM calls
            await asyncio.sleep(0.1)  # Simulate async processing
            
            # Call the specific agent's processing method
            result = await self._process_request(request, llm_provider)
            
            response.status = AgentStatus.COMPLETED
            response.result = result.get("result", "")
            response.reasoning = result.get("reasoning", [])
            response.metadata = result.get("metadata", {})
            response.completed_at = datetime.utcnow()
            
        except Exception as e:
            response.status = AgentStatus.FAILED
            response.error = str(e)
            response.completed_at = datetime.utcnow()
            logger.error(f"Agent {self.agent_type} failed: {str(e)}")
        
        return response
    
    async def _process_request(self, request: PromptRequest, llm_provider: LLMProvider) -> Dict[str, Any]:
        """Override this method in specific agent implementations"""
        raise NotImplementedError("Subclasses must implement _process_request")

# Core Agent Implementations
class ZeroShotAgent(BaseAgent):
    def __init__(self):
        super().__init__(AgentType.ZERO_SHOT)
    
    async def _process_request(self, request: PromptRequest, llm_provider: LLMProvider) -> Dict[str, Any]:
        # Zero-shot prompting: direct prompt without examples
        enhanced_prompt = f"""Task: {request.prompt}

Context: {request.context or 'No additional context provided'}

Please provide a direct and accurate response to the task above."""
        
        try:
            # Use actual LLM call
            llm_response = await llm_manager.generate_response(
                provider_type=llm_provider,
                prompt=enhanced_prompt,
                max_tokens=1000,
                temperature=0.7
            )
            
            result = llm_response["response"]
            metadata = {
                "technique": "zero_shot", 
                "prompt_length": len(enhanced_prompt),
                "model": llm_response.get("model", "unknown"),
                "usage": llm_response.get("usage", {})
            }
            
        except Exception as e:
            logger.error(f"LLM call failed: {str(e)}")
            # Fallback to placeholder
            result = f"Zero-shot response to: {request.prompt}"
            metadata = {"technique": "zero_shot", "error": str(e)}
        
        return {
            "result": result,
            "reasoning": ["Applied zero-shot prompting technique"],
            "metadata": metadata
        }

class FewShotAgent(BaseAgent):
    def __init__(self):
        super().__init__(AgentType.FEW_SHOT)
    
    async def _process_request(self, request: PromptRequest, llm_provider: LLMProvider) -> Dict[str, Any]:
        # Few-shot prompting: use examples to guide response
        examples_text = ""
        if request.examples:
            for i, example in enumerate(request.examples, 1):
                examples_text += f"\nExample {i}:\n"
                examples_text += f"Input: {example.get('input', '')}\n"
                examples_text += f"Output: {example.get('output', '')}\n"
        
        enhanced_prompt = f"""Task: {request.prompt}

Context: {request.context or 'No additional context provided'}

Examples:{examples_text}

Now, please provide a response following the pattern shown in the examples above."""
        
        # Placeholder for actual LLM call
        result = f"Few-shot response to: {request.prompt}"
        
        return {
            "result": result,
            "reasoning": [f"Used {len(request.examples or [])} examples to guide response"],
            "metadata": {"technique": "few_shot", "examples_count": len(request.examples or [])}
        }

class ChainOfThoughtAgent(BaseAgent):
    def __init__(self):
        super().__init__(AgentType.CHAIN_OF_THOUGHT)
    
    async def _process_request(self, request: PromptRequest, llm_provider: LLMProvider) -> Dict[str, Any]:
        # Chain of thought: encourage step-by-step reasoning
        enhanced_prompt = f"""Task: {request.prompt}

Context: {request.context or 'No additional context provided'}

Please solve this step by step:
1. First, identify what the task is asking for
2. Break down the problem into smaller parts
3. Solve each part systematically
4. Combine the results for a final answer

Let's work through this step by step:"""
        
        # Placeholder for actual LLM call
        result = f"Chain-of-thought response to: {request.prompt}"
        reasoning = [
            "Step 1: Analyzed the task requirements",
            "Step 2: Broke down the problem into components",
            "Step 3: Solved each component systematically",
            "Step 4: Synthesized the final answer"
        ]
        
        return {
            "result": result,
            "reasoning": reasoning,
            "metadata": {"technique": "chain_of_thought", "reasoning_steps": len(reasoning)}
        }

class SelfConsistencyAgent(BaseAgent):
    def __init__(self):
        super().__init__(AgentType.SELF_CONSISTENCY)
    
    async def _process_request(self, request: PromptRequest, llm_provider: LLMProvider) -> Dict[str, Any]:
        # Self-consistency: generate multiple reasoning paths
        num_paths = request.parameters.get("num_paths", 3) if request.parameters else 3
        
        enhanced_prompt = f"""Task: {request.prompt}

Context: {request.context or 'No additional context provided'}

Please provide multiple reasoning paths to solve this problem step by step:"""
        
        # Simulate multiple reasoning paths
        reasoning_paths = []
        for i in range(num_paths):
            reasoning_paths.append(f"Reasoning path {i+1}: Step-by-step analysis of {request.prompt}")
        
        # Placeholder for actual LLM call and consistency check
        result = f"Self-consistency response to: {request.prompt}"
        
        return {
            "result": result,
            "reasoning": reasoning_paths + ["Selected most consistent answer from multiple paths"],
            "metadata": {"technique": "self_consistency", "reasoning_paths": num_paths}
        }

class TreeOfThoughtsAgent(BaseAgent):
    def __init__(self):
        super().__init__(AgentType.TREE_OF_THOUGHTS)
    
    async def _process_request(self, request: PromptRequest, llm_provider: LLMProvider) -> Dict[str, Any]:
        # Tree of thoughts: explore multiple branches
        depth = request.parameters.get("depth", 2) if request.parameters else 2
        
        enhanced_prompt = f"""Task: {request.prompt}

Context: {request.context or 'No additional context provided'}

Let's explore this problem like a search tree, considering multiple branches of reasoning:"""
        
        # Simulate tree exploration
        tree_branches = []
        for level in range(depth):
            tree_branches.append(f"Level {level+1}: Exploring branch {level+1} of reasoning")
        
        # Placeholder for actual LLM call
        result = f"Tree-of-thoughts response to: {request.prompt}"
        
        return {
            "result": result,
            "reasoning": tree_branches + ["Selected best path from tree exploration"],
            "metadata": {"technique": "tree_of_thoughts", "tree_depth": depth}
        }

class ReActAgent(BaseAgent):
    def __init__(self):
        super().__init__(AgentType.REACT)
    
    async def _process_request(self, request: PromptRequest, llm_provider: LLMProvider) -> Dict[str, Any]:
        # ReAct: Reasoning + Acting
        enhanced_prompt = f"""Task: {request.prompt}

Context: {request.context or 'No additional context provided'}

Use the ReAct (Reasoning + Acting) approach:
1. Think about what you need to do
2. Act on your reasoning
3. Observe the results
4. Reflect and adjust if needed

Let's start:"""
        
        # Simulate ReAct cycle
        react_steps = [
            "Think: Analyzed the task and determined approach",
            "Act: Implemented the solution step",
            "Observe: Evaluated the intermediate result",
            "Reflect: Confirmed the approach is correct"
        ]
        
        # Placeholder for actual LLM call
        result = f"ReAct response to: {request.prompt}"
        
        return {
            "result": result,
            "reasoning": react_steps,
            "metadata": {"technique": "react", "react_cycles": 1}
        }

# Initialize agents
def initialize_agents():
    agents = [
        ZeroShotAgent(),
        FewShotAgent(),
        ChainOfThoughtAgent(),
        SelfConsistencyAgent(),
        TreeOfThoughtsAgent(),
        ReActAgent()
    ]
    
    for agent in agents:
        AGENT_REGISTRY[agent.agent_type] = agent
    
    logger.info(f"Initialized {len(agents)} agents")

# API Routes
@api_router.get("/")
async def root():
    return {"message": "Prompt Engineering Agent Platform API", "version": "1.0.0"}

@api_router.get("/agents")
async def get_agents():
    """Get list of available agents"""
    return {
        "agents": [
            {
                "type": agent.agent_type.value,
                "name": agent.name,
                "description": agent.description
            }
            for agent in AGENT_REGISTRY.values()
        ]
    }

@api_router.post("/agents/process")
async def process_agent_request(request: AgentRequest):
    """Process a request with a specific agent"""
    if request.agent_type not in AGENT_REGISTRY:
        raise HTTPException(status_code=404, detail=f"Agent {request.agent_type} not found")
    
    agent = AGENT_REGISTRY[request.agent_type]
    response = await agent.process(request.request, request.llm_provider)
    
    # Store in database
    await db.agent_responses.insert_one(response.dict())
    
    return response

@api_router.get("/agents/{agent_type}")
async def get_agent_info(agent_type: AgentType):
    """Get information about a specific agent"""
    if agent_type not in AGENT_REGISTRY:
        raise HTTPException(status_code=404, detail=f"Agent {agent_type} not found")
    
    agent = AGENT_REGISTRY[agent_type]
    return {
        "type": agent.agent_type.value,
        "name": agent.name,
        "description": agent.description
    }

@api_router.get("/sessions/{session_id}/history")
async def get_session_history(session_id: str):
    """Get history for a specific session"""
    responses = await db.agent_responses.find({"session_id": session_id}).to_list(100)
    return {"session_id": session_id, "responses": responses}

# Include router
app.include_router(api_router)

# Initialize agents on startup
@app.on_event("startup")
async def startup_event():
    initialize_agents()

@app.on_event("shutdown")
async def shutdown_event():
    client.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)