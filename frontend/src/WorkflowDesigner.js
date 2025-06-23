import React, { useState, useEffect } from "react";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const WorkflowDesigner = () => {
  const [workflows, setWorkflows] = useState([]);
  const [templates, setTemplates] = useState([]);
  const [agents, setAgents] = useState([]);
  const [currentWorkflow, setCurrentWorkflow] = useState(null);
  const [workflowName, setWorkflowName] = useState("");
  const [workflowDescription, setWorkflowDescription] = useState("");
  const [steps, setSteps] = useState([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState("designer");

  useEffect(() => {
    fetchAgents();
    fetchWorkflows();
    fetchTemplates();
  }, []);

  const fetchAgents = async () => {
    try {
      const response = await axios.get(`${API}/agents`);
      setAgents(response.data.agents);
    } catch (error) {
      console.error("Error fetching agents:", error);
    }
  };

  const fetchWorkflows = async () => {
    try {
      const response = await axios.get(`${API}/workflows`);
      setWorkflows(response.data.workflows);
    } catch (error) {
      console.error("Error fetching workflows:", error);
      alert("Failed to load workflows. Please try again.");
    }
  };

  const fetchTemplates = async () => {
    try {
      const response = await axios.get(`${API}/workflow-templates`);
      setTemplates(response.data.templates);
    } catch (error) {
      console.error("Error fetching templates:", error);
    }
  };

  const addStep = () => {
    const newStep = {
      id: Date.now().toString(),
      name: `Step ${steps.length + 1}`,
      agent_type: "zero_shot",
      prompt: "",
      context: "",
      llm_provider: "openai",
      depends_on: [],
      parameters: {}
    };
    setSteps([...steps, newStep]);
  };

  const updateStep = (stepId, field, value) => {
    setSteps(steps.map(step => 
      step.id === stepId ? { ...step, [field]: value } : step
    ));
  };

  const removeStep = (stepId) => {
    setSteps(steps.filter(step => step.id !== stepId));
  };

  const createWorkflow = async () => {
    if (!workflowName.trim() || steps.length === 0) {
      alert("Please provide a workflow name and at least one step");
      return;
    }

    setLoading(true);
    try {
      const workflowData = {
        name: workflowName,
        description: workflowDescription,
        steps: steps.map(step => ({
          name: step.name,
          agent_type: step.agent_type,
          prompt: step.prompt,
          context: step.context || null,
          llm_provider: step.llm_provider,
          depends_on: step.depends_on || [],
          parameters: step.parameters || {}
        })),
        session_id: `workflow_${Date.now()}`
      };

      const response = await axios.post(`${API}/workflows`, workflowData);
      setCurrentWorkflow(response.data);
      await fetchWorkflows();
      
      // Show success message and switch to workflows tab
      alert(`Workflow "${workflowName}" created successfully!`);
      setActiveTab("workflows");
      
      // Reset form
      setWorkflowName("");
      setWorkflowDescription("");
      setSteps([]);
      
    } catch (error) {
      console.error("Error creating workflow:", error);
      const errorMessage = error.response?.data?.detail || error.message || "Unknown error occurred";
      alert(`Failed to create workflow: ${errorMessage}`);
    } finally {
      setLoading(false);
    }
  };

  const executeWorkflow = async (workflowId) => {
    setLoading(true);
    try {
      await axios.post(`${API}/workflows/${workflowId}/execute`);
      alert("Workflow execution started!");
      // Refresh workflows to see status updates
      setTimeout(fetchWorkflows, 2000);
    } catch (error) {
      console.error("Error executing workflow:", error);
      alert("Error executing workflow");
    } finally {
      setLoading(false);
    }
  };

  const loadTemplate = (template) => {
    setWorkflowName(template.name);
    setWorkflowDescription(template.description);
    setSteps(template.steps.map(step => ({
      ...step,
      id: Date.now().toString() + Math.random()
    })));
    setActiveTab("designer");
  };

  const resetWorkflow = () => {
    setWorkflowName("");
    setWorkflowDescription("");
    setSteps([]);
    setCurrentWorkflow(null);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-8">🔗 Workflow Orchestration</h1>

      {/* Tab Navigation */}
      <div className="mb-6">
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex space-x-8">
            <button
              onClick={() => setActiveTab("designer")}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === "designer"
                  ? "border-blue-500 text-blue-600"
                  : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
              }`}
            >
              Designer
            </button>
            <button
              onClick={() => setActiveTab("templates")}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === "templates"
                  ? "border-blue-500 text-blue-600"
                  : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
              }`}
            >
              Templates
            </button>
            <button
              onClick={() => setActiveTab("workflows")}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === "workflows"
                  ? "border-blue-500 text-blue-600"
                  : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
              }`}
            >
              My Workflows
            </button>
          </nav>
        </div>
      </div>

      {/* Designer Tab */}
      {activeTab === "designer" && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Workflow Configuration */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-xl font-semibold">Workflow Designer</h2>
                <div className="space-x-2">
                  <button
                    onClick={resetWorkflow}
                    className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600"
                  >
                    Reset
                  </button>
                  <button
                    onClick={addStep}
                    className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                  >
                    Add Step
                  </button>
                </div>
              </div>

              {/* Workflow Info */}
              <div className="mb-6 space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Workflow Name *
                  </label>
                  <input
                    type="text"
                    value={workflowName}
                    onChange={(e) => setWorkflowName(e.target.value)}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    placeholder="Enter workflow name..."
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Description
                  </label>
                  <textarea
                    value={workflowDescription}
                    onChange={(e) => setWorkflowDescription(e.target.value)}
                    rows={2}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    placeholder="Describe what this workflow does..."
                  />
                </div>
              </div>

              {/* Steps */}
              <div className="space-y-4">
                {steps.map((step, index) => (
                  <div key={step.id} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex justify-between items-center mb-4">
                      <h3 className="text-lg font-medium">Step {index + 1}</h3>
                      <button
                        onClick={() => removeStep(step.id)}
                        className="text-red-500 hover:text-red-700"
                      >
                        Remove
                      </button>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Step Name
                        </label>
                        <input
                          type="text"
                          value={step.name}
                          onChange={(e) => updateStep(step.id, "name", e.target.value)}
                          className="w-full p-2 border border-gray-300 rounded-md"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Agent Type
                        </label>
                        <select
                          value={step.agent_type}
                          onChange={(e) => updateStep(step.id, "agent_type", e.target.value)}
                          className="w-full p-2 border border-gray-300 rounded-md"
                        >
                          {agents.map(agent => (
                            <option key={agent.type} value={agent.type}>
                              {agent.name}
                            </option>
                          ))}
                        </select>
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          LLM Provider
                        </label>
                        <select
                          value={step.llm_provider}
                          onChange={(e) => updateStep(step.id, "llm_provider", e.target.value)}
                          className="w-full p-2 border border-gray-300 rounded-md"
                        >
                          <option value="openai">OpenAI</option>
                          <option value="anthropic">Anthropic</option>
                          <option value="local">Local</option>
                        </select>
                      </div>
                    </div>

                    <div className="mt-4 space-y-3">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Prompt *
                        </label>
                        <textarea
                          value={step.prompt}
                          onChange={(e) => updateStep(step.id, "prompt", e.target.value)}
                          rows={3}
                          className="w-full p-2 border border-gray-300 rounded-md"
                          placeholder="Enter the prompt for this step..."
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Context (Optional)
                        </label>
                        <textarea
                          value={step.context}
                          onChange={(e) => updateStep(step.id, "context", e.target.value)}
                          rows={2}
                          className="w-full p-2 border border-gray-300 rounded-md"
                          placeholder="Additional context for this step..."
                        />
                      </div>
                    </div>
                  </div>
                ))}

                {steps.length === 0 && (
                  <div className="text-center py-12 text-gray-500">
                    <p>No steps added yet. Click "Add Step" to get started.</p>
                  </div>
                )}
              </div>

              {/* Create Workflow Button */}
              {steps.length > 0 && (
                <div className="mt-6">
                  <button
                    onClick={createWorkflow}
                    disabled={loading}
                    className="w-full bg-green-500 text-white py-3 px-4 rounded-lg hover:bg-green-600 disabled:bg-gray-400"
                  >
                    {loading ? "Creating..." : "Create Workflow"}
                  </button>
                </div>
              )}
            </div>
          </div>

          {/* Agent Library Sidebar */}
          <div>
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold mb-4">Available Agents</h3>
              <div className="space-y-3">
                {agents.map(agent => (
                  <div key={agent.type} className="border border-gray-200 rounded-lg p-3">
                    <h4 className="font-medium text-sm">{agent.name}</h4>
                    <p className="text-xs text-gray-600 mt-1">{agent.description}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Templates Tab */}
      {activeTab === "templates" && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {templates.map(template => (
            <div key={template.id} className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-xl font-semibold mb-2">{template.name}</h3>
              <p className="text-gray-600 mb-4">{template.description}</p>
              <div className="mb-4">
                <span className="text-sm text-gray-500">
                  {template.steps.length} steps
                </span>
              </div>
              <button
                onClick={() => loadTemplate(template)}
                className="w-full bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600"
              >
                Use Template
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Workflows Tab */}
      {activeTab === "workflows" && (
        <div className="space-y-4">
          {workflows.map(workflow => (
            <div key={workflow.id} className="bg-white rounded-lg shadow-md p-6">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="text-xl font-semibold">{workflow.name}</h3>
                  {workflow.description && (
                    <p className="text-gray-600 mt-1">{workflow.description}</p>
                  )}
                  <div className="mt-2 flex items-center space-x-4">
                    <span className="text-sm text-gray-500">
                      {workflow.steps?.length || 0} steps
                    </span>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      workflow.status === 'completed' ? 'bg-green-100 text-green-800' :
                      workflow.status === 'running' ? 'bg-yellow-100 text-yellow-800' :
                      workflow.status === 'failed' ? 'bg-red-100 text-red-800' :
                      'bg-gray-100 text-gray-800'
                    }`}>
                      {workflow.status || 'pending'}
                    </span>
                  </div>
                </div>
                <div className="space-x-2">
                  <button
                    onClick={() => executeWorkflow(workflow.id)}
                    disabled={loading || workflow.status === 'running'}
                    className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 disabled:bg-gray-400"
                  >
                    Execute
                  </button>
                </div>
              </div>
            </div>
          ))}

          {workflows.length === 0 && (
            <div className="text-center py-12 text-gray-500">
              <p>No workflows created yet. Use the designer to create your first workflow.</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default WorkflowDesigner;