import asyncio
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class WorkflowStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class StepStatus(str, Enum):
    WAITING = "waiting"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"

class WorkflowStep(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    agent_type: str
    prompt: str
    context: Optional[str] = None
    examples: Optional[List[Dict[str, str]]] = None
    llm_provider: str = "openai"
    depends_on: List[str] = Field(default_factory=list)
    parameters: Optional[Dict[str, Any]] = None
    status: StepStatus = StepStatus.WAITING
    result: Optional[str] = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class Workflow(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: Optional[str] = None
    steps: List[WorkflowStep]
    status: WorkflowStatus = WorkflowStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    results: Dict[str, Any] = Field(default_factory=dict)
    session_id: Optional[str] = None

class WorkflowEngine:
    """Advanced workflow orchestration engine"""
    
    def __init__(self, agent_registry):
        self.agent_registry = agent_registry
        self.active_workflows: Dict[str, Workflow] = {}
        self.workflow_history: List[Workflow] = []
    
    async def create_workflow(self, name: str, steps: List[Dict], description: Optional[str] = None, session_id: Optional[str] = None) -> Workflow:
        """Create a new workflow"""
        workflow_steps = []
        
        for step_data in steps:
            step = WorkflowStep(
                name=step_data.get("name", f"Step {len(workflow_steps) + 1}"),
                agent_type=step_data["agent_type"],
                prompt=step_data["prompt"],
                context=step_data.get("context"),
                examples=step_data.get("examples"),
                llm_provider=step_data.get("llm_provider", "openai"),
                depends_on=step_data.get("depends_on", []),
                parameters=step_data.get("parameters")
            )
            workflow_steps.append(step)
        
        workflow = Workflow(
            name=name,
            description=description,
            steps=workflow_steps,
            session_id=session_id
        )
        
        self.active_workflows[workflow.id] = workflow
        logger.info(f"Created workflow {workflow.id}: {name}")
        
        return workflow
    
    async def execute_workflow(self, workflow_id: str) -> Workflow:
        """Execute a workflow with dependency management"""
        if workflow_id not in self.active_workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        workflow = self.active_workflows[workflow_id]
        workflow.status = WorkflowStatus.RUNNING
        workflow.started_at = datetime.utcnow()
        
        logger.info(f"Starting workflow execution: {workflow.name}")
        
        try:
            # Build dependency graph
            dependency_graph = self._build_dependency_graph(workflow.steps)
            
            # Execute steps in dependency order
            await self._execute_steps_with_dependencies(workflow, dependency_graph)
            
            workflow.status = WorkflowStatus.COMPLETED
            workflow.completed_at = datetime.utcnow()
            
            logger.info(f"Workflow {workflow.id} completed successfully")
            
        except Exception as e:
            workflow.status = WorkflowStatus.FAILED
            workflow.completed_at = datetime.utcnow()
            logger.error(f"Workflow {workflow.id} failed: {str(e)}")
            raise e
        
        # Move to history
        self.workflow_history.append(workflow)
        del self.active_workflows[workflow_id]
        
        return workflow
    
    def _build_dependency_graph(self, steps: List[WorkflowStep]) -> Dict[str, List[str]]:
        """Build dependency graph from workflow steps"""
        graph = {}
        step_map = {step.id: step for step in steps}
        
        for step in steps:
            graph[step.id] = []
            for dep_id in step.depends_on:
                if dep_id in step_map:
                    graph[step.id].append(dep_id)
        
        return graph
    
    async def _execute_steps_with_dependencies(self, workflow: Workflow, dependency_graph: Dict[str, List[str]]):
        """Execute workflow steps respecting dependencies"""
        step_map = {step.id: step for step in workflow.steps}
        completed_steps = set()
        running_tasks = {}
        
        while len(completed_steps) < len(workflow.steps):
            # Find steps ready to run
            ready_steps = []
            for step_id, step in step_map.items():
                if (step_id not in completed_steps and 
                    step_id not in running_tasks and
                    step.status == StepStatus.WAITING and
                    all(dep_id in completed_steps for dep_id in dependency_graph.get(step_id, []))):
                    ready_steps.append(step)
            
            # Start ready steps
            for step in ready_steps:
                step.status = StepStatus.RUNNING
                step.started_at = datetime.utcnow()
                
                # Prepare step context with previous results
                step_context = await self._prepare_step_context(step, workflow, completed_steps, step_map)
                
                # Create task
                task = asyncio.create_task(self._execute_single_step(step, step_context))
                running_tasks[step.id] = task
                
                logger.info(f"Started step {step.name} ({step.id})")
            
            # Wait for at least one task to complete
            if running_tasks:
                done, pending = await asyncio.wait(running_tasks.values(), return_when=asyncio.FIRST_COMPLETED)
                
                # Process completed tasks
                for task in done:
                    step_id = None
                    for sid, t in running_tasks.items():
                        if t == task:
                            step_id = sid
                            break
                    
                    if step_id:
                        step = step_map[step_id]
                        try:
                            result = await task
                            step.result = result.get("result", "")
                            step.status = StepStatus.COMPLETED
                            step.completed_at = datetime.utcnow()
                            
                            # Store result in workflow
                            workflow.results[step.id] = result
                            
                            logger.info(f"Completed step {step.name} ({step.id})")
                            
                        except Exception as e:
                            step.error = str(e)
                            step.status = StepStatus.FAILED
                            step.completed_at = datetime.utcnow()
                            logger.error(f"Step {step.name} failed: {str(e)}")
                        
                        completed_steps.add(step_id)
                        del running_tasks[step_id]
            
            # Check if any steps failed and stop execution
            failed_steps = [step for step in workflow.steps if step.status == StepStatus.FAILED]
            if failed_steps:
                # Cancel remaining tasks
                for task in running_tasks.values():
                    task.cancel()
                raise Exception(f"Workflow failed due to step failures: {[s.name for s in failed_steps]}")
    
    async def _prepare_step_context(self, step: WorkflowStep, workflow: Workflow, completed_steps: set, step_map: Dict[str, WorkflowStep]) -> Dict[str, Any]:
        """Prepare context for step execution including previous results"""
        context = {
            "original_prompt": step.prompt,
            "original_context": step.context,
            "examples": step.examples,
            "parameters": step.parameters or {}
        }
        
        # Add results from dependent steps
        if step.depends_on:
            dependent_results = {}
            for dep_id in step.depends_on:
                if dep_id in completed_steps and dep_id in workflow.results:
                    dep_step = step_map[dep_id]
                    dependent_results[dep_step.name] = workflow.results[dep_id]
            
            context["dependent_results"] = dependent_results
            
            # Enhance prompt with dependent results if available
            if dependent_results:
                enhanced_prompt = step.prompt + "\n\nResults from previous steps:\n"
                for step_name, result in dependent_results.items():
                    enhanced_prompt += f"- {step_name}: {result.get('result', '')}\n"
                context["enhanced_prompt"] = enhanced_prompt
        
        return context
    
    async def _execute_single_step(self, step: WorkflowStep, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single workflow step"""
        if step.agent_type not in self.agent_registry:
            raise ValueError(f"Agent {step.agent_type} not found")
        
        agent = self.agent_registry[step.agent_type]
        
        # Prepare request
        from server import PromptRequest, LLMProvider
        
        # Use enhanced prompt if available (includes results from dependencies)
        prompt = context.get("enhanced_prompt", context["original_prompt"])
        
        request = PromptRequest(
            prompt=prompt,
            context=context.get("original_context"),
            examples=context.get("examples"),
            parameters=context.get("parameters")
        )
        
        # Convert string to enum
        llm_provider = LLMProvider(step.llm_provider)
        
        # Execute agent
        response = await agent.process(request, llm_provider)
        
        if response.status == "failed":
            raise Exception(response.error or "Agent execution failed")
        
        return {
            "result": response.result,
            "reasoning": response.reasoning,
            "metadata": response.metadata,
            "agent_response": response.dict()
        }
    
    def get_workflow(self, workflow_id: str) -> Optional[Workflow]:
        """Get workflow by ID"""
        if workflow_id in self.active_workflows:
            return self.active_workflows[workflow_id]
        
        for workflow in self.workflow_history:
            if workflow.id == workflow_id:
                return workflow
        
        return None
    
    def list_active_workflows(self) -> List[Workflow]:
        """List all active workflows"""
        return list(self.active_workflows.values())
    
    def list_workflow_history(self, limit: int = 50) -> List[Workflow]:
        """List workflow history"""
        return self.workflow_history[-limit:]
    
    async def cancel_workflow(self, workflow_id: str) -> bool:
        """Cancel an active workflow"""
        if workflow_id not in self.active_workflows:
            return False
        
        workflow = self.active_workflows[workflow_id]
        workflow.status = WorkflowStatus.CANCELLED
        workflow.completed_at = datetime.utcnow()
        
        # Move to history
        self.workflow_history.append(workflow)
        del self.active_workflows[workflow_id]
        
        logger.info(f"Cancelled workflow {workflow.id}")
        return True

# Global workflow engine instance
workflow_engine = None

def get_workflow_engine(agent_registry):
    """Get or create workflow engine instance"""
    global workflow_engine
    if workflow_engine is None:
        workflow_engine = WorkflowEngine(agent_registry)
    return workflow_engine