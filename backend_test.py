#!/usr/bin/env python3
import requests
import json
import sys
import time
from datetime import datetime

class PromptEngineeringAgentTester:
    def __init__(self, base_url="https://6cb68b4d-945c-4a74-bb4b-d396a6d2d70d.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def run_test(self, name, method, endpoint, expected_status, data=None, validate_func=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers)
            else:
                raise ValueError(f"Unsupported method: {method}")

            status_success = response.status_code == expected_status
            
            # Try to parse JSON response
            try:
                response_data = response.json()
            except:
                response_data = {"error": "Failed to parse JSON response"}
            
            # Additional validation if provided
            validation_success = True
            validation_message = ""
            if validate_func and status_success:
                validation_success, validation_message = validate_func(response_data)
            
            success = status_success and validation_success
            
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                if validation_message:
                    print(f"   {validation_message}")
            else:
                if not status_success:
                    print(f"❌ Failed - Expected status {expected_status}, got {response.status_code}")
                if not validation_success:
                    print(f"❌ Failed - {validation_message}")
            
            # Store test result
            self.test_results.append({
                "name": name,
                "success": success,
                "status_code": response.status_code,
                "expected_status": expected_status,
                "validation_message": validation_message,
                "response_data": response_data
            })

            return success, response_data

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            self.test_results.append({
                "name": name,
                "success": False,
                "error": str(e)
            })
            return False, {"error": str(e)}

    def test_root_endpoint(self):
        """Test the root API endpoint"""
        def validate(data):
            if "message" in data and "version" in data:
                return True, "Root endpoint returned expected fields"
            return False, "Root endpoint missing expected fields"
        
        return self.run_test(
            "Root API Endpoint",
            "GET",
            "",
            200,
            validate_func=validate
        )

    def test_get_agents(self):
        """Test the get agents endpoint"""
        def validate(data):
            if "agents" not in data:
                return False, "Response missing 'agents' field"
            
            agents = data["agents"]
            if not isinstance(agents, list):
                return False, "'agents' field is not a list"
            
            if len(agents) != 10:
                return False, f"Expected 10 agents, got {len(agents)}"
            
            # Check if all required agent types are present
            required_types = [
                # Core agents
                "zero_shot", "few_shot", "chain_of_thought", 
                "self_consistency", "tree_of_thoughts", "react",
                # Advanced agents
                "rag", "auto_prompt", "program_aided", "factuality_checker"
            ]
            
            agent_types = [agent["type"] for agent in agents]
            missing_types = [t for t in required_types if t not in agent_types]
            
            if missing_types:
                return False, f"Missing agent types: {', '.join(missing_types)}"
            
            return True, f"Found all 10 required agent types"
        
        return self.run_test(
            "Get Agents List",
            "GET",
            "agents",
            200,
            validate_func=validate
        )

    def test_agent_info(self, agent_type):
        """Test getting info for a specific agent"""
        def validate(data):
            if "type" not in data or "name" not in data or "description" not in data:
                return False, "Response missing required fields"
            
            if data["type"] != agent_type:
                return False, f"Expected agent type {agent_type}, got {data['type']}"
            
            return True, f"Agent info for {agent_type} retrieved successfully"
        
        return self.run_test(
            f"Get Agent Info - {agent_type}",
            "GET",
            f"agents/{agent_type}",
            200,
            validate_func=validate
        )

    def test_agent_process(self, agent_type, llm_provider, prompt, context=None, examples=None):
        """Test processing a request with a specific agent"""
        request_data = {
            "agent_type": agent_type,
            "llm_provider": llm_provider,
            "request": {
                "prompt": prompt,
                "context": context
            }
        }
        
        if examples:
            request_data["request"]["examples"] = examples
        
        def validate(data):
            if "id" not in data or "agent_type" not in data or "status" not in data:
                return False, "Response missing required fields"
            
            if data["agent_type"] != agent_type:
                return False, f"Expected agent type {agent_type}, got {data['agent_type']}"
            
            if data["status"] not in ["completed", "processing", "failed"]:
                return False, f"Invalid status: {data['status']}"
            
            if data["status"] == "completed" and "result" not in data:
                return False, "Completed status but no result field"
            
            if data["status"] == "failed" and "error" not in data:
                return False, "Failed status but no error field"
            
            return True, f"Agent {agent_type} with {llm_provider} processed request successfully"
        
        return self.run_test(
            f"Process Request - {agent_type} with {llm_provider}",
            "POST",
            "agents/process",
            200,
            data=request_data,
            validate_func=validate
        )
        
    def test_get_workflow_templates(self):
        """Test getting workflow templates"""
        def validate(data):
            if "templates" not in data:
                return False, "Response missing 'templates' field"
            
            templates = data["templates"]
            if not isinstance(templates, list):
                return False, "'templates' field is not a list"
            
            if len(templates) != 3:
                return False, f"Expected 3 templates, got {len(templates)}"
            
            # Check if all templates have required fields
            for template in templates:
                if not all(key in template for key in ["id", "name", "description", "steps"]):
                    return False, "Template missing required fields"
            
            return True, f"Found {len(templates)} workflow templates"
        
        return self.run_test(
            "Get Workflow Templates",
            "GET",
            "workflow-templates",
            200,
            validate_func=validate
        )
    
    def test_create_workflow(self, name, steps):
        """Test creating a workflow"""
        workflow_data = {
            "name": name,
            "description": f"Test workflow created at {datetime.now().isoformat()}",
            "steps": steps,
            "session_id": f"test_session_{int(time.time())}"
        }
        
        def validate(data):
            if not all(key in data for key in ["id", "name", "steps", "status"]):
                return False, "Response missing required fields"
            
            if data["name"] != name:
                return False, f"Expected workflow name {name}, got {data['name']}"
            
            if len(data["steps"]) != len(steps):
                return False, f"Expected {len(steps)} steps, got {len(data['steps'])}"
            
            return True, f"Workflow '{name}' created successfully with {len(steps)} steps"
        
        return self.run_test(
            f"Create Workflow - {name}",
            "POST",
            "workflows",
            200,
            data=workflow_data,
            validate_func=validate
        )
    
    def test_get_workflows(self):
        """Test getting the list of workflows"""
        def validate(data):
            if "workflows" not in data:
                return False, "Response missing 'workflows' field"
            
            if not isinstance(data["workflows"], list):
                return False, "'workflows' field is not a list"
            
            return True, f"Retrieved {len(data['workflows'])} workflows"
        
        return self.run_test(
            "Get Workflows List",
            "GET",
            "workflows",
            200,
            validate_func=validate
        )
    
    def test_get_workflow(self, workflow_id):
        """Test getting a specific workflow"""
        def validate(data):
            if "id" not in data or data["id"] != workflow_id:
                return False, f"Response missing 'id' field or incorrect id"
            
            return True, f"Retrieved workflow {workflow_id}"
        
        return self.run_test(
            f"Get Workflow - {workflow_id}",
            "GET",
            f"workflows/{workflow_id}",
            200,
            validate_func=validate
        )
    
    def test_execute_workflow(self, workflow_id):
        """Test executing a workflow"""
        def validate(data):
            if "workflow_id" not in data or data["workflow_id"] != workflow_id:
                return False, "Response missing or incorrect 'workflow_id' field"
            
            if "message" not in data:
                return False, "Response missing 'message' field"
            
            return True, f"Workflow {workflow_id} execution started"
        
        return self.run_test(
            f"Execute Workflow - {workflow_id}",
            "POST",
            f"workflows/{workflow_id}/execute",
            200,
            validate_func=validate
        )

    def run_all_tests(self):
        """Run all API tests"""
        print("=" * 80)
        print("🚀 Starting Prompt Engineering Agent Platform API Tests")
        print("=" * 80)
        
        # Test basic API endpoints
        self.test_root_endpoint()
        self.test_get_agents()
        
        # Test each agent type info endpoint
        agent_types = ["zero_shot", "few_shot", "chain_of_thought", 
                      "self_consistency", "tree_of_thoughts", "react"]
        
        for agent_type in agent_types:
            self.test_agent_info(agent_type)
        
        # Test processing with different agent types and providers
        
        # 1. Zero-shot with OpenAI
        self.test_agent_process(
            "zero_shot", 
            "openai", 
            "What is machine learning?"
        )
        
        # 2. Few-shot with examples
        self.test_agent_process(
            "few_shot",
            "openai",
            "Classify sentiment",
            examples=[
                {"input": "I love this!", "output": "positive"},
                {"input": "This is terrible", "output": "negative"}
            ]
        )
        
        # 3. Chain-of-thought with Anthropic
        self.test_agent_process(
            "chain_of_thought",
            "anthropic",
            "If a train travels 60 mph for 2.5 hours, how far does it go?"
        )
        
        # 4. Self-consistency with Local provider
        self.test_agent_process(
            "self_consistency",
            "local",
            "What is the capital of France?"
        )
        
        # 5. Tree-of-thoughts with context
        self.test_agent_process(
            "tree_of_thoughts",
            "openai",
            "Solve this puzzle",
            context="You have 3 boxes, one contains gold, one contains silver, and one is empty. Each box has a label, but all labels are incorrect."
        )
        
        # 6. ReAct with Anthropic
        self.test_agent_process(
            "react",
            "anthropic",
            "Plan a trip to Japan"
        )
        
        # Print summary
        self.print_summary()
        
        return self.tests_passed == self.tests_run

    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 80)
        print(f"📊 Test Summary: {self.tests_passed}/{self.tests_run} tests passed")
        print("=" * 80)
        
        if self.tests_passed == self.tests_run:
            print("✅ All tests passed!")
        else:
            print("❌ Some tests failed:")
            for result in self.test_results:
                if not result.get("success", False):
                    print(f"  - {result['name']}")
                    if "error" in result:
                        print(f"    Error: {result['error']}")
                    elif "status_code" in result:
                        print(f"    Status: {result['status_code']} (expected {result['expected_status']})")
                    if "validation_message" in result and result["validation_message"]:
                        print(f"    Validation: {result['validation_message']}")
        
        print("=" * 80)

def main():
    # Get base URL from command line if provided
    base_url = "https://6cb68b4d-945c-4a74-bb4b-d396a6d2d70d.preview.emergentagent.com/api"
    
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    
    tester = PromptEngineeringAgentTester(base_url)
    success = tester.run_all_tests()
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())