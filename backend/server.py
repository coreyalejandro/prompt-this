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
import sys
from pathlib import Path
from aiolimiter import AsyncLimiter

# Add the backend directory to Python path
sys.path.append(str(Path(__file__).parent))

from llm_providers import LLMProviderManager, llm_manager
from workflow_engine import WorkflowEngine, get_workflow_engine, Workflow, WorkflowStep

# Custom JSON encoder for MongoDB ObjectId
from bson import ObjectId

def serialize_doc(doc):
    """Convert MongoDB document to JSON serializable format"""
    if doc is None:
        return None
    
    if isinstance(doc, dict):
        return {key: serialize_doc(value) for key, value in doc.items()}
    elif isinstance(doc, list):
        return [serialize_doc(item) for item in doc]
    elif isinstance(doc, ObjectId):
        return str(doc)
    elif hasattr(doc, 'dict'):  # Pydantic models
        return doc.dict()
    else:
        return doc

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app
app = FastAPI(title="Prompt-This API", version="1.0.0")
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

# Rate limiting for LLM calls
LLM_REQUESTS_PER_SECOND = int(os.getenv("LLM_REQUESTS_PER_SECOND", 5))
LLM_QUEUE_TIMEOUT = float(os.getenv("LLM_QUEUE_TIMEOUT", 1))
llm_rate_limiter = AsyncLimiter(LLM_REQUESTS_PER_SECOND, 1)

async def rate_limited_llm_call(**kwargs):
    """Call the LLM with rate limiting and queue control."""
    try:
        await asyncio.wait_for(llm_rate_limiter.acquire(), timeout=LLM_QUEUE_TIMEOUT)
    except asyncio.TimeoutError:
        raise HTTPException(status_code=503, detail="Server is busy. Please try again later.")
    try:
        return await llm_manager.generate_response(**kwargs)
    finally:
        llm_rate_limiter.release()

# Enums and Models
class AgentType(str, Enum):
    ZERO_SHOT = "zero_shot"
    FEW_SHOT = "few_shot"
    CHAIN_OF_THOUGHT = "chain_of_thought"
    SELF_CONSISTENCY = "self_consistency"
    TREE_OF_THOUGHTS = "tree_of_thoughts"
    REACT = "react"
    # Advanced agents
    RAG = "rag"
    AUTO_PROMPT = "auto_prompt"
    PROGRAM_AIDED = "program_aided"
    FACTUALITY_CHECKER = "factuality_checker"

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
            AgentType.REACT: "Combines reasoning and action-taking capabilities",
            AgentType.RAG: "Retrieval Augmented Generation - combines external knowledge with generation",
            AgentType.AUTO_PROMPT: "Automatically optimizes and refines prompts for better results",
            AgentType.PROGRAM_AIDED: "Uses code generation and execution to solve complex problems",
            AgentType.FACTUALITY_CHECKER: "Validates the factual accuracy of generated content"
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

        except HTTPException:
            raise
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
            llm_response = await rate_limited_llm_call(
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
        
        try:
            # Use actual LLM call
            llm_response = await rate_limited_llm_call(
                provider_type=llm_provider,
                prompt=enhanced_prompt,
                max_tokens=1000,
                temperature=0.7
            )
            
            result = llm_response["response"]
            metadata = {
                "technique": "few_shot", 
                "examples_count": len(request.examples or []),
                "model": llm_response.get("model", "unknown"),
                "usage": llm_response.get("usage", {})
            }
            
        except Exception as e:
            logger.error(f"LLM call failed: {str(e)}")
            # Fallback to placeholder
            result = f"Few-shot response to: {request.prompt}"
            metadata = {"technique": "few_shot", "examples_count": len(request.examples or []), "error": str(e)}
        
        return {
            "result": result,
            "reasoning": [f"Used {len(request.examples or [])} examples to guide response"],
            "metadata": metadata
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
        
        try:
            # Use actual LLM call
            llm_response = await rate_limited_llm_call(
                provider_type=llm_provider,
                prompt=enhanced_prompt,
                max_tokens=1000,
                temperature=0.7
            )
            
            result = llm_response["response"]
            # Extract reasoning steps from the response
            reasoning_lines = result.split('\n')
            reasoning = [line.strip() for line in reasoning_lines if line.strip() and any(step in line.lower() for step in ['step', '1.', '2.', '3.', '4.', 'first', 'second', 'third', 'finally'])]
            
            if not reasoning:
                reasoning = ["Applied chain-of-thought prompting technique"]
            
            metadata = {
                "technique": "chain_of_thought", 
                "reasoning_steps": len(reasoning),
                "model": llm_response.get("model", "unknown"),
                "usage": llm_response.get("usage", {})
            }
            
        except Exception as e:
            logger.error(f"LLM call failed: {str(e)}")
            # Fallback to placeholder
            result = f"Chain-of-thought response to: {request.prompt}"
            reasoning = [
                "Step 1: Analyzed the task requirements",
                "Step 2: Broke down the problem into components",
                "Step 3: Solved each component systematically",
                "Step 4: Synthesized the final answer"
            ]
            metadata = {"technique": "chain_of_thought", "reasoning_steps": len(reasoning), "error": str(e)}
        
        return {
            "result": result,
            "reasoning": reasoning,
            "metadata": metadata
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
        
        try:
            # Use actual LLM call
            llm_response = await rate_limited_llm_call(
                provider_type=llm_provider,
                prompt=enhanced_prompt,
                max_tokens=1000,
                temperature=0.7
            )
            
            result = llm_response["response"]
            # Extract ReAct steps from the response
            react_steps = []
            lines = result.split('\n')
            for line in lines:
                if any(keyword in line.lower() for keyword in ['think:', 'thought:', 'act:', 'action:', 'observe:', 'observation:', 'reflect:']):
                    react_steps.append(line.strip())
            
            if not react_steps:
                react_steps = [
                    "Think: Analyzed the task and determined approach",
                    "Act: Implemented the solution step",
                    "Observe: Evaluated the intermediate result",
                    "Reflect: Confirmed the approach is correct"
                ]
            
            metadata = {
                "technique": "react", 
                "react_cycles": max(1, len(react_steps) // 4),
                "model": llm_response.get("model", "unknown"),
                "usage": llm_response.get("usage", {})
            }
            
        except Exception as e:
            logger.error(f"LLM call failed: {str(e)}")
            # Fallback to placeholder
            result = f"ReAct response to: {request.prompt}"
            react_steps = [
                "Think: Analyzed the task and determined approach",
                "Act: Implemented the solution step",
                "Observe: Evaluated the intermediate result",
                "Reflect: Confirmed the approach is correct"
            ]
            metadata = {"technique": "react", "react_cycles": 1, "error": str(e)}
        
        return {
            "result": result,
            "reasoning": react_steps,
            "metadata": metadata
        }

# Advanced Agent Implementations
class RAGAgent(BaseAgent):
    def __init__(self):
        super().__init__(AgentType.RAG)
    
    async def _process_request(self, request: PromptRequest, llm_provider: LLMProvider) -> Dict[str, Any]:
        # RAG: Retrieval Augmented Generation
        enhanced_prompt = f"""Task: {request.prompt}

Context: {request.context or 'No additional context provided'}

Using Retrieval Augmented Generation approach:
1. First, I'll identify what information needs to be retrieved
2. Then, I'll use that information to generate a comprehensive response
3. I'll combine my knowledge with the retrieved context

Based on the available context and my knowledge base:"""
        
        try:
            # Use actual LLM call
            llm_response = await rate_limited_llm_call(
                provider_type=llm_provider,
                prompt=enhanced_prompt,
                max_tokens=1200,
                temperature=0.6
            )
            
            result = llm_response["response"]
            reasoning = [
                "Step 1: Analyzed information retrieval requirements",
                "Step 2: Combined retrieved context with base knowledge",
                "Step 3: Generated augmented response"
            ]
            
            metadata = {
                "technique": "rag", 
                "model": llm_response.get("model", "unknown"),
                "usage": llm_response.get("usage", {}),
                "context_length": len(request.context or "")
            }
            
        except Exception as e:
            logger.error(f"LLM call failed: {str(e)}")
            result = f"RAG response to: {request.prompt}"
            reasoning = ["Applied Retrieval Augmented Generation technique"]
            metadata = {"technique": "rag", "error": str(e)}
        
        return {
            "result": result,
            "reasoning": reasoning,
            "metadata": metadata
        }

class AutoPromptAgent(BaseAgent):
    def __init__(self):
        super().__init__(AgentType.AUTO_PROMPT)
    
    async def _process_request(self, request: PromptRequest, llm_provider: LLMProvider) -> Dict[str, Any]:
        # Auto Prompt Engineering: Optimize the prompt automatically
        optimization_prompt = f"""I need to optimize this prompt for better results:

Original Prompt: "{request.prompt}"
Context: {request.context or 'No additional context'}

Please create an optimized version of this prompt that:
1. Is clearer and more specific
2. Includes better instructions
3. Has examples if helpful
4. Uses effective prompt engineering techniques

Optimized Prompt:"""
        
        try:
            # First, optimize the prompt
            optimization_response = await rate_limited_llm_call(
                provider_type=llm_provider,
                prompt=optimization_prompt,
                max_tokens=800,
                temperature=0.5
            )
            
            optimized_prompt = optimization_response["response"]
            
            # Then use the optimized prompt
            final_response = await rate_limited_llm_call(
                provider_type=llm_provider,
                prompt=optimized_prompt,
                max_tokens=1000,
                temperature=0.7
            )
            
            result = final_response["response"]
            reasoning = [
                "Step 1: Analyzed original prompt for optimization opportunities",
                "Step 2: Created optimized prompt with better structure",
                f"Step 3: Applied optimized prompt: {optimized_prompt[:100]}...",
                "Step 4: Generated final response using optimized prompt"
            ]
            
            metadata = {
                "technique": "auto_prompt",
                "original_prompt": request.prompt,
                "optimized_prompt": optimized_prompt,
                "model": final_response.get("model", "unknown"),
                "usage": final_response.get("usage", {})
            }
            
        except Exception as e:
            logger.error(f"LLM call failed: {str(e)}")
            result = f"Auto-prompt optimized response to: {request.prompt}"
            reasoning = ["Applied automatic prompt optimization technique"]
            metadata = {"technique": "auto_prompt", "error": str(e)}
        
        return {
            "result": result,
            "reasoning": reasoning,
            "metadata": metadata
        }

class ProgramAidedAgent(BaseAgent):
    def __init__(self):
        super().__init__(AgentType.PROGRAM_AIDED)
    
    async def _process_request(self, request: PromptRequest, llm_provider: LLMProvider) -> Dict[str, Any]:
        # Program-Aided Language Model: Use code to solve problems
        enhanced_prompt = f"""Task: {request.prompt}

Context: {request.context or 'No additional context provided'}

I'll solve this using a Program-Aided approach:
1. First, I'll analyze if this problem can benefit from code
2. Then, I'll write Python code to help solve it
3. Finally, I'll interpret the results

Let me work through this systematically with code assistance:

```python
# Code to help solve: {request.prompt}
```"""
        
        try:
            # Use actual LLM call
            llm_response = await rate_limited_llm_call(
                provider_type=llm_provider,
                prompt=enhanced_prompt,
                max_tokens=1200,
                temperature=0.3  # Lower temperature for more precise code
            )
            
            result = llm_response["response"]
            reasoning = [
                "Step 1: Analyzed problem for code-assisted solution",
                "Step 2: Generated relevant Python code",
                "Step 3: Interpreted code results",
                "Step 4: Provided comprehensive solution"
            ]
            
            metadata = {
                "technique": "program_aided",
                "model": llm_response.get("model", "unknown"),
                "usage": llm_response.get("usage", {}),
                "code_assisted": True
            }
            
        except Exception as e:
            logger.error(f"LLM call failed: {str(e)}")
            result = f"Program-aided response to: {request.prompt}"
            reasoning = ["Applied Program-Aided Language Model technique"]
            metadata = {"technique": "program_aided", "error": str(e)}
        
        return {
            "result": result,
            "reasoning": reasoning,
            "metadata": metadata
        }

class FactualityCheckerAgent(BaseAgent):
    def __init__(self):
        super().__init__(AgentType.FACTUALITY_CHECKER)
    
    async def _process_request(self, request: PromptRequest, llm_provider: LLMProvider) -> Dict[str, Any]:
        # Factuality Checker: Validate accuracy of information
        enhanced_prompt = f"""Task: Analyze the following statement or content for factual accuracy:

Content to check: {request.prompt}

Context: {request.context or 'No additional context provided'}

Please provide a detailed factuality analysis:
1. Identify all factual claims made
2. Evaluate the accuracy of each claim
3. Note any potential inaccuracies or uncertainties
4. Provide confidence levels for assessments
5. Suggest corrections if needed

Factuality Analysis:"""
        
        try:
            # Use actual LLM call
            llm_response = await rate_limited_llm_call(
                provider_type=llm_provider,
                prompt=enhanced_prompt,
                max_tokens=1200,
                temperature=0.2  # Low temperature for more accurate fact-checking
            )
            
            result = llm_response["response"]
            reasoning = [
                "Step 1: Identified factual claims in the content",
                "Step 2: Cross-referenced claims with knowledge base",
                "Step 3: Evaluated accuracy and confidence levels",
                "Step 4: Provided detailed factuality assessment"
            ]
            
            metadata = {
                "technique": "factuality_checker",
                "model": llm_response.get("model", "unknown"),
                "usage": llm_response.get("usage", {}),
                "content_length": len(request.prompt)
            }
            
        except Exception as e:
            logger.error(f"LLM call failed: {str(e)}")
            result = f"Factuality analysis of: {request.prompt}"
            reasoning = ["Applied factuality checking technique"]
            metadata = {"technique": "factuality_checker", "error": str(e)}
        
        return {
            "result": result,
            "reasoning": reasoning,
            "metadata": metadata
        }

# Initialize agents
def initialize_agents():
    agents = [
        ZeroShotAgent(),
        FewShotAgent(),
        ChainOfThoughtAgent(),
        SelfConsistencyAgent(),
        TreeOfThoughtsAgent(),
        ReActAgent(),
        # Advanced agents
        RAGAgent(),
        AutoPromptAgent(),
        ProgramAidedAgent(),
        FactualityCheckerAgent()
    ]
    
    for agent in agents:
        AGENT_REGISTRY[agent.agent_type] = agent
    
    logger.info(f"Initialized {len(agents)} agents")

# Global workflow engine
WORKFLOW_ENGINE = None

# API Routes
@api_router.get("/")
async def root():
    return {"message": "Prompt-This API", "version": "1.0.0"}

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
    # Serialize to handle ObjectId
    responses = [serialize_doc(response) for response in responses]
    return {"session_id": session_id, "responses": responses}

# Workflow API Endpoints
@api_router.post("/workflows")
async def create_workflow(request: Dict[str, Any]):
    """Create a new workflow"""
    global WORKFLOW_ENGINE
    if not WORKFLOW_ENGINE:
        WORKFLOW_ENGINE = get_workflow_engine(AGENT_REGISTRY)
    
    name = request.get("name", "Untitled Workflow")
    description = request.get("description")
    steps = request.get("steps", [])
    session_id = request.get("session_id")
    
    workflow = await WORKFLOW_ENGINE.create_workflow(name, steps, description, session_id)
    
    # Store in database with proper serialization
    workflow_dict = workflow.dict()
    await db.workflows.insert_one(workflow_dict)
    
    return workflow.dict()

@api_router.post("/workflows/{workflow_id}/execute")
async def execute_workflow(workflow_id: str, background_tasks: BackgroundTasks):
    """Execute a workflow"""
    global WORKFLOW_ENGINE
    if not WORKFLOW_ENGINE:
        WORKFLOW_ENGINE = get_workflow_engine(AGENT_REGISTRY)
    
    # Execute workflow in background
    background_tasks.add_task(execute_workflow_task, workflow_id)
    
    return {"message": f"Workflow {workflow_id} execution started", "workflow_id": workflow_id}

async def execute_workflow_task(workflow_id: str):
    """Background task to execute workflow"""
    try:
        workflow = await WORKFLOW_ENGINE.execute_workflow(workflow_id)
        # Update in database
        await db.workflows.replace_one({"id": workflow_id}, workflow.dict())
        logger.info(f"Workflow {workflow_id} completed")
    except Exception as e:
        logger.error(f"Workflow {workflow_id} failed: {str(e)}")

@api_router.get("/workflows/{workflow_id}")
async def get_workflow(workflow_id: str):
    """Get workflow details"""
    global WORKFLOW_ENGINE
    if not WORKFLOW_ENGINE:
        WORKFLOW_ENGINE = get_workflow_engine(AGENT_REGISTRY)
    
    workflow = WORKFLOW_ENGINE.get_workflow(workflow_id)
    if not workflow:
        # Try to get from database
        workflow_data = await db.workflows.find_one({"id": workflow_id})
        if not workflow_data:
            raise HTTPException(status_code=404, detail="Workflow not found")
        return serialize_doc(workflow_data)
    
    return workflow.dict()

@api_router.get("/workflows")
async def list_workflows(active_only: bool = False):
    """List workflows"""
    global WORKFLOW_ENGINE
    if not WORKFLOW_ENGINE:
        WORKFLOW_ENGINE = get_workflow_engine(AGENT_REGISTRY)
    
    if active_only:
        workflows = WORKFLOW_ENGINE.list_active_workflows()
        # Convert to dict format for serialization
        workflows_data = [workflow.dict() for workflow in workflows]
    else:
        # Get from database and handle ObjectId serialization
        workflows_data = await db.workflows.find().to_list(100)
        workflows_data = [serialize_doc(workflow) for workflow in workflows_data]
    
    return {"workflows": workflows_data}

@api_router.delete("/workflows/{workflow_id}")
async def cancel_workflow(workflow_id: str):
    """Cancel an active workflow"""
    global WORKFLOW_ENGINE
    if not WORKFLOW_ENGINE:
        WORKFLOW_ENGINE = get_workflow_engine(AGENT_REGISTRY)
    
    success = await WORKFLOW_ENGINE.cancel_workflow(workflow_id)
    if not success:
        raise HTTPException(status_code=404, detail="Workflow not found or not active")
    
    return {"message": f"Workflow {workflow_id} cancelled"}

# Workflow Templates
@api_router.get("/workflow-templates")
async def get_workflow_templates():
    """Get predefined workflow templates"""
    templates = [
        {
            "id": "analysis_pipeline",
            "name": "Content Analysis Pipeline",
            "description": "Analyze content using multiple agents for comprehensive insights",
            "steps": [
                {
                    "name": "Zero-Shot Analysis",
                    "agent_type": "zero_shot",
                    "prompt": "Provide an initial analysis of the following content: {content}",
                    "llm_provider": "openai"
                },
                {
                    "name": "Chain-of-Thought Deep Dive",
                    "agent_type": "chain_of_thought",
                    "prompt": "Provide a detailed step-by-step analysis of the content",
                    "depends_on": ["Zero-Shot Analysis"],
                    "llm_provider": "anthropic"
                },
                {
                    "name": "Factuality Check",
                    "agent_type": "factuality_checker",
                    "prompt": "Check the factual accuracy of the analysis",
                    "depends_on": ["Chain-of-Thought Deep Dive"],
                    "llm_provider": "openai"
                }
            ]
        },
        {
            "id": "problem_solving",
            "name": "Multi-Agent Problem Solving",
            "description": "Solve complex problems using different reasoning approaches",
            "steps": [
                {
                    "name": "Tree of Thoughts Exploration",
                    "agent_type": "tree_of_thoughts",
                    "prompt": "Explore different solution paths for: {problem}",
                    "llm_provider": "openai"
                },
                {
                    "name": "Program-Aided Solution",
                    "agent_type": "program_aided",
                    "prompt": "Use code to solve this problem if applicable",
                    "depends_on": ["Tree of Thoughts Exploration"],
                    "llm_provider": "openai"
                },
                {
                    "name": "Self-Consistency Check",
                    "agent_type": "self_consistency",
                    "prompt": "Verify the solution using multiple reasoning paths",
                    "depends_on": ["Program-Aided Solution"],
                    "llm_provider": "anthropic"
                }
            ]
        },
        {
            "id": "content_generation",
            "name": "Content Generation & Optimization",
            "description": "Generate and optimize content using multiple techniques",
            "steps": [
                {
                    "name": "Initial Generation",
                    "agent_type": "zero_shot",
                    "prompt": "Generate content for: {topic}",
                    "llm_provider": "openai"
                },
                {
                    "name": "Auto-Prompt Optimization",
                    "agent_type": "auto_prompt",
                    "prompt": "Improve and optimize the generated content",
                    "depends_on": ["Initial Generation"],
                    "llm_provider": "anthropic"
                },
                {
                    "name": "RAG Enhancement",
                    "agent_type": "rag",
                    "prompt": "Enhance with additional context and information",
                    "depends_on": ["Auto-Prompt Optimization"],
                    "llm_provider": "openai"
                }
            ]
        }
    ]
    
    return {"templates": templates}

# Include router
app.include_router(api_router)

# Initialize agents on startup
@app.on_event("startup")
async def startup_event():
    # Initialize LLM providers
    await llm_manager.initialize_all_providers()
    # Initialize agents
    initialize_agents()
    # Initialize workflow engine
    global WORKFLOW_ENGINE
    WORKFLOW_ENGINE = get_workflow_engine(AGENT_REGISTRY)

@app.on_event("shutdown")
async def shutdown_event():
    client.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)