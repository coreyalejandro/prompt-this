import React, { useState, useEffect } from "react";
import { BrowserRouter, Routes, Route, Link, useParams } from "react-router-dom";
import Guidebook from "./Guidebook";
import axios from "axios";
import Exercises from "./Exercises";
import "./App.css";
import WorkflowDesigner from "./WorkflowDesigner";
import OnboardingTutorial from "./OnboardingTutorial";
import { AuthProvider, useAuth } from "./AuthContext";
import LoginModal from "./LoginModal";
import Profile from "./Profile";
import { useTranslation } from "react-i18next";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Agent Library Component
const AgentLibrary = () => {
  const { t } = useTranslation();
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAgents();
  }, []);

  const fetchAgents = async () => {
    try {
      const response = await axios.get(`${API}/agents`);
      setAgents(response.data.agents);
      setLoading(false);
    } catch (error) {
      console.error("Error fetching agents:", error);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-8">{t('agentLibrary')}</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {agents.map((agent) => (
          <div key={agent.type} className="glass rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
            <h3 className="text-xl font-semibold text-gray-800 mb-2">{agent.name}</h3>
            <p className="text-gray-600 mb-4">{agent.description}</p>
            <div className="flex space-x-2">
              <Link
                to={`/agent/${agent.type}`}
                className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors"
              >
                {t('testAgent')}
              </Link>
              <Link
                to={`/agent/${agent.type}/info`}
                className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600 transition-colors"
              >
                {t('viewInfo')}
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

// Agent Testing Component
const AgentTester = ({ agentType }) => {
  const [agent, setAgent] = useState(null);
  const [prompt, setPrompt] = useState("");
  const [context, setContext] = useState("");
  const [examples, setExamples] = useState([{ input: "", output: "" }]);
  const [llmProvider, setLlmProvider] = useState("openai");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showExamples, setShowExamples] = useState(false);

  useEffect(() => {
    fetchAgentInfo();
  }, [agentType]);

  const fetchAgentInfo = async () => {
    try {
      const response = await axios.get(`${API}/agents/${agentType}`);
      setAgent(response.data);
    } catch (error) {
      console.error("Error fetching agent info:", error);
    }
  };

  const addExample = () => {
    setExamples([...examples, { input: "", output: "" }]);
  };

  const updateExample = (index, field, value) => {
    const newExamples = [...examples];
    newExamples[index][field] = value;
    setExamples(newExamples);
  };

  const removeExample = (index) => {
    const newExamples = examples.filter((_, i) => i !== index);
    setExamples(newExamples);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResponse(null);

    try {
      const requestData = {
        agent_type: agentType,
        llm_provider: llmProvider,
        request: {
          prompt,
          context: context || null,
          examples: showExamples ? examples.filter(ex => ex.input && ex.output) : null
        }
      };

      const result = await axios.post(`${API}/agents/process`, requestData);
      setResponse(result.data);
    } catch (error) {
      console.error("Error processing request:", error);
      setResponse({
        status: "failed",
        error: error.response?.data?.detail || error.message
      });
    } finally {
      setLoading(false);
    }
  };

  if (!agent) {
    return <div className="text-center">Loading agent information...</div>;
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-4">
        <Link to="/" className="text-blue-500 hover:text-blue-700">← Back to Library</Link>
      </div>
      
      <h1 className="text-3xl font-bold text-gray-800 mb-2">{agent.name}</h1>
      <p className="text-gray-600 mb-8">{agent.description}</p>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Input Form */}
        <div className="glass rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">Test Configuration</h2>
          
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* LLM Provider Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                LLM Provider
              </label>
              <select
                value={llmProvider}
                onChange={(e) => setLlmProvider(e.target.value)}
                className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="openai">OpenAI</option>
                <option value="anthropic">Anthropic</option>
                <option value="local">Local Model</option>
              </select>
            </div>

            {/* Prompt Input */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Prompt *
              </label>
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                rows={4}
                className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="Enter your prompt here..."
                required
              />
            </div>

            {/* Context Input */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Context (Optional)
              </label>
              <textarea
                value={context}
                onChange={(e) => setContext(e.target.value)}
                rows={3}
                className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="Additional context for the prompt..."
              />
            </div>

            {/* Examples Section */}
            <div>
              <div className="flex items-center mb-2">
                <input
                  type="checkbox"
                  id="showExamples"
                  checked={showExamples}
                  onChange={(e) => setShowExamples(e.target.checked)}
                  className="mr-2"
                />
                <label htmlFor="showExamples" className="text-sm font-medium text-gray-700">
                  Include Examples (for Few-Shot prompting)
                </label>
              </div>
              
              {showExamples && (
                <div className="space-y-3">
                  {examples.map((example, index) => (
                    <div key={index} className="border border-gray-200 rounded-md p-3">
                      <div className="flex justify-between items-center mb-2">
                        <span className="text-sm font-medium text-gray-700">Example {index + 1}</span>
                        {examples.length > 1 && (
                          <button
                            type="button"
                            onClick={() => removeExample(index)}
                            className="text-red-500 hover:text-red-700 text-sm"
                          >
                            Remove
                          </button>
                        )}
                      </div>
                      <div className="space-y-2">
                        <input
                          type="text"
                          placeholder="Input"
                          value={example.input}
                          onChange={(e) => updateExample(index, 'input', e.target.value)}
                          className="w-full p-2 border border-gray-300 rounded-md text-sm"
                        />
                        <input
                          type="text"
                          placeholder="Output"
                          value={example.output}
                          onChange={(e) => updateExample(index, 'output', e.target.value)}
                          className="w-full p-2 border border-gray-300 rounded-md text-sm"
                        />
                      </div>
                    </div>
                  ))}
                  <button
                    type="button"
                    onClick={addExample}
                    className="text-blue-500 hover:text-blue-700 text-sm"
                  >
                    + Add Example
                  </button>
                </div>
              )}
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading || !prompt.trim()}
              className="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? "Processing..." : "Test Agent"}
            </button>
          </form>
        </div>

        {/* Response Display */}
        <div className="glass rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">Response</h2>
          
          {loading && (
            <div className="flex justify-center items-center h-32">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
            </div>
          )}

          {response && !loading && (
            <div className="space-y-4">
              {/* Status */}
              <div className="flex items-center space-x-2">
                <span className="text-sm font-medium text-gray-700">Status:</span>
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                  response.status === 'completed' ? 'bg-green-100 text-green-800' :
                  response.status === 'failed' ? 'bg-red-100 text-red-800' :
                  'bg-yellow-100 text-yellow-800'
                }`}>
                  {response.status}
                </span>
              </div>

              {/* Result */}
              {response.result && (
                <div>
                  <h3 className="text-lg font-medium text-gray-800 mb-2">Result:</h3>
                  <div className="bg-gray-50 rounded-md p-3">
                    <p className="text-gray-800 whitespace-pre-wrap">{response.result}</p>
                  </div>
                </div>
              )}

              {/* Reasoning */}
              {response.reasoning && response.reasoning.length > 0 && (
                <div>
                  <h3 className="text-lg font-medium text-gray-800 mb-2">Reasoning Steps:</h3>
                  <ul className="bg-gray-50 rounded-md p-3 space-y-1">
                    {response.reasoning.map((step, index) => (
                      <li key={index} className="text-gray-700">• {step}</li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Metadata */}
              {response.metadata && (
                <div>
                  <h3 className="text-lg font-medium text-gray-800 mb-2">Metadata:</h3>
                  <div className="bg-gray-50 rounded-md p-3">
                    <pre className="text-sm text-gray-700 overflow-x-auto">
                      {JSON.stringify(response.metadata, null, 2)}
                    </pre>
                  </div>
                </div>
              )}

              {/* Error */}
              {response.error && (
                <div className="bg-red-50 border border-red-200 rounded-md p-3">
                  <h3 className="text-lg font-medium text-red-800 mb-2">Error:</h3>
                  <p className="text-red-700">{response.error}</p>
                </div>
              )}
            </div>
          )}

          {!response && !loading && (
            <div className="text-center text-gray-500 py-8">
              Enter a prompt and click "Test Agent" to see the response
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

// Agent Info Component
const AgentInfo = ({ agentType }) => {
  const [agent, setAgent] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAgentInfo();
  }, [agentType]);

  const fetchAgentInfo = async () => {
    try {
      const response = await axios.get(`${API}/agents/${agentType}`);
      setAgent(response.data);
      setLoading(false);
    } catch (error) {
      console.error("Error fetching agent info:", error);
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-center">Loading...</div>;
  }

  if (!agent) {
    return <div className="text-center text-red-500">Agent not found</div>;
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-4">
        <Link to="/" className="text-blue-500 hover:text-blue-700">← Back to Library</Link>
      </div>
      
      <div className="glass rounded-lg shadow-md p-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-4">{agent.name}</h1>
        <p className="text-gray-600 mb-6">{agent.description}</p>
        
        <div className="mb-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-3">Agent Type</h2>
          <code className="bg-gray-100 px-3 py-1 rounded">{agent.type}</code>
        </div>

        <div className="flex space-x-4">
          <Link
            to={`/agent/${agent.type}`}
            className="bg-blue-500 text-white px-6 py-2 rounded hover:bg-blue-600 transition-colors"
          >
            Test This Agent
          </Link>
        </div>
      </div>
    </div>
  );
};

// Main App Component
const AppContent = () => {
  const [showOnboarding, setShowOnboarding] = useState(false);
  const [showLogin, setShowLogin] = useState(false);
  const { user, isAuthenticated, logout } = useAuth();
  const { t, i18n } = useTranslation();

  useEffect(() => {
    // Check if user has completed onboarding
    const completed = localStorage.getItem('onboarding_completed');
    if (completed !== 'true') {
      setShowOnboarding(true);
    }
    
    // Check if user needs to log in
    if (!isAuthenticated) {
      // Show login modal after a short delay to let the UI load
      setTimeout(() => setShowLogin(true), 1000);
    }
  }, [isAuthenticated]);

  const handleOnboardingComplete = () => {
    setShowOnboarding(false);
  };

  const handleTutorialClick = () => {
    console.log("Tutorial button clicked"); // Debug log
    setShowOnboarding(true);
  };

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900 text-gray-900 dark:text-gray-100">
      <BrowserRouter>
        {/* Header */}
        <header className="bg-white/70 dark:bg-gray-800/50 backdrop-blur-md shadow-sm">
          <div className="container mx-auto px-4 py-4">
<div className="flex flex-col sm:flex-row sm:justify-between sm:items-center">
  <Link to="/" className="text-xl font-bold text-gray-800 dark:text-gray-100 mb-4 sm:mb-0">
    {t('title')}
  </Link>
  {/* You can add other elements here if needed */}
</div>
              </Link>
              <nav className="flex flex-col sm:flex-row items-center sm:justify-end gap-2 sm:gap-6">
                <Link to="/" className="text-gray-600 hover:text-gray-800">
                  {t('agents')}
                </Link>
                <Link to="/workflows" className="text-gray-600 hover:text-gray-800">
                  {t('workflows')}
                </Link>
                <Link to="/guidebook" className="text-gray-600 hover:text-gray-800">
                  Guidebook
                </Link>
                <button
                  onClick={handleTutorialClick}
                  className="text-gray-600 hover:text-gray-800 dark:hover:text-gray-200 transition-colors"
                >
                  {t('tutorial')}
                </button>
                <select
                  value={i18n.language}
                  onChange={(e) => i18n.changeLanguage(e.target.value)}
                  className="border rounded p-1 text-sm bg-transparent"
                >
                  <option value="en">EN</option>
                  <option value="es">ES</option>
                </select>
                {isAuthenticated && (
import Profile from "./Profile";
import { useTranslation } from "react-i18next";
                    <span className="text-sm text-gray-600 dark:text-gray-300">
                      {user?.username}
                    </span>
                    <button
                      onClick={logout}
                      className="text-sm text-gray-500 hover:text-gray-700"
                    >
                      {t('logout')}
                    </button>
                  </div>
                )}
              </nav>
            </div>
          </div>
        </header>

        {/* Routes */}
        <Routes>
          <Route path="/" element={<AgentLibrary />} />
          <Route path="/workflows" element={<WorkflowDesigner />} />
          <Route path="/guidebook" element={<Guidebook />} />
          <Route path="/agent/:agentType" element={<AgentTesterWrapper />} />
          <Route path="/agent/:agentType/info" element={<AgentInfoWrapper />} />
<Route path="/profile" element={<Profile />} />
<Route path="/exercises/:chapter" element={<ExercisesWrapper />} />
        </Routes>

        {/* Footer */}
        <footer className="bg-white border-t mt-12">
          <div className="container mx-auto px-4 py-6 text-center text-gray-600">
            <p>{t('builtWith')}</p>
            <div className="mt-2 text-sm space-x-4">
              <a href="/docs/README.md" className="text-blue-500 hover:text-blue-700">{t('documentation')}</a>
              <a href="/docs/API_DOCUMENTATION.md" className="text-blue-500 hover:text-blue-700">{t('apiDocs')}</a>
              <a href="/docs/TROUBLESHOOTING_GUIDE.md" className="text-blue-500 hover:text-blue-700">{t('troubleshooting')}</a>
            </div>
          </div>
        </footer>

        {/* Login Modal */}
        <LoginModal isOpen={showLogin} onClose={() => setShowLogin(false)} />

        {/* Onboarding Tutorial */}
        {showOnboarding && (
          <OnboardingTutorial onComplete={handleOnboardingComplete} />
        )}
      </BrowserRouter>
    </div>
  );
};

const App = () => {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
};

// Wrapper components to pass route params
const AgentTesterWrapper = () => {
  const { agentType } = useParams();
  return <AgentTester agentType={agentType} />;
};

const AgentInfoWrapper = () => {
  const { agentType } = useParams();
  return <AgentInfo agentType={agentType} />;
};

const ExercisesWrapper = () => {
  const { chapter } = useParams();
  return <Exercises chapter={chapter} />;
};

export default ExercisesWrapper;
