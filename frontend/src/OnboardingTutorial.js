import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";

const OnboardingTutorial = ({ onComplete }) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [isVisible, setIsVisible] = useState(true);

  const tutorialSteps = [
    {
      id: "welcome",
      title: "Welcome to the Prompt Engineering Agent Platform! 🎉",
      content: (
        <div className="space-y-4">
          <p className="text-lg">
            This platform transforms the D.A.I.R. Prompt Engineering Guide into practical, working agents.
          </p>
          <div className="bg-blue-50 p-4 rounded-lg">
            <h4 className="font-semibold text-blue-800 mb-2">What you can do:</h4>
            <ul className="text-blue-700 space-y-1">
              <li>✅ Test 10 specialized prompt engineering agents</li>
              <li>✅ Create complex multi-agent workflows</li>
              <li>✅ Use OpenAI, Anthropic, or local models</li>
              <li>✅ Build sophisticated reasoning pipelines</li>
            </ul>
          </div>
          <p className="text-gray-600">
            Let's take a quick tour to get you started!
          </p>
        </div>
      ),
      action: "Start Tour",
      skipable: true
    },
    {
      id: "agents-overview",
      title: "Agent Library Overview 🤖",
      content: (
        <div className="space-y-4">
          <p>The Agent Library contains 10 specialized agents based on prompt engineering techniques:</p>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-green-50 p-3 rounded-lg">
              <h4 className="font-semibold text-green-800 mb-2">Core Agents (6)</h4>
              <ul className="text-green-700 text-sm space-y-1">
                <li>• Zero-Shot Prompting</li>
                <li>• Few-Shot Prompting</li>
                <li>• Chain-of-Thought</li>
                <li>• Self-Consistency</li>
                <li>• Tree-of-Thoughts</li>
                <li>• ReAct</li>
              </ul>
            </div>
            
            <div className="bg-purple-50 p-3 rounded-lg">
              <h4 className="font-semibold text-purple-800 mb-2">Advanced Agents (4)</h4>
              <ul className="text-purple-700 text-sm space-y-1">
                <li>• RAG (Retrieval Augmented)</li>
                <li>• Auto-Prompt Optimizer</li>
                <li>• Program-Aided Solver</li>
                <li>• Factuality Checker</li>
              </ul>
            </div>
          </div>
          
          <p className="text-gray-600">
            Each agent specializes in a specific prompt engineering technique and can work individually or in teams.
          </p>
        </div>
      ),
      action: "Continue",
      skipable: true
    },
    {
      id: "testing-agents",
      title: "Testing Individual Agents 🧪",
      content: (
        <div className="space-y-4">
          <p>Let's learn how to test an individual agent:</p>
          
          <div className="bg-gray-50 p-4 rounded-lg">
            <h4 className="font-semibold mb-2">Steps to test an agent:</h4>
            <ol className="list-decimal list-inside space-y-2 text-gray-700">
              <li>Click on any agent card in the library</li>
              <li>Choose your LLM provider (OpenAI, Anthropic, or Local)</li>
              <li>Enter your prompt and optional context</li>
              <li>For Few-Shot agents, add examples</li>
              <li>Click "Test Agent" to see results</li>
            </ol>
          </div>
          
          <div className="bg-yellow-50 p-3 rounded-lg">
            <h4 className="font-semibold text-yellow-800 mb-1">💡 Pro Tip:</h4>
            <p className="text-yellow-700 text-sm">
              Try the same prompt with different agents to see how each technique approaches the problem differently!
            </p>
          </div>
          
          <p className="text-gray-600">
            Each response includes the result, reasoning steps, and metadata about the processing.
          </p>
        </div>
      ),
      action: "Got it!",
      skipable: true
    },
    {
      id: "workflow-intro",
      title: "Workflow Orchestration 🔗",
      content: (
        <div className="space-y-4">
          <p>The real power comes from chaining agents together in workflows:</p>
          
          <div className="bg-indigo-50 p-4 rounded-lg">
            <h4 className="font-semibold text-indigo-800 mb-2">Workflow Benefits:</h4>
            <ul className="text-indigo-700 space-y-1">
              <li>🔄 <strong>Sequential Processing:</strong> Results from one agent feed into the next</li>
              <li>⚡ <strong>Parallel Execution:</strong> Run independent agents simultaneously</li>
              <li>🎯 <strong>Dependency Management:</strong> Complex workflows with smart routing</li>
              <li>📊 <strong>Real-time Monitoring:</strong> Watch your workflow execute step by step</li>
            </ul>
          </div>
          
          <div className="bg-orange-50 p-3 rounded-lg">
            <h4 className="font-semibold text-orange-800 mb-1">Example Workflow:</h4>
            <p className="text-orange-700 text-sm">
              Content Analysis → Chain-of-Thought Deep Dive → Factuality Check → Final Report
            </p>
          </div>
        </div>
      ),
      action: "Show me workflows",
      skipable: true
    },
    {
      id: "workflow-templates",
      title: "Pre-built Templates 📋",
      content: (
        <div className="space-y-4">
          <p>Get started quickly with our pre-built workflow templates:</p>
          
          <div className="space-y-3">
            <div className="border border-blue-200 p-3 rounded-lg">
              <h4 className="font-semibold text-blue-800">📊 Content Analysis Pipeline</h4>
              <p className="text-sm text-gray-600">
                Zero-Shot Analysis → Chain-of-Thought → Factuality Check
              </p>
              <p className="text-xs text-gray-500 mt-1">
                Perfect for analyzing documents, articles, or any content
              </p>
            </div>
            
            <div className="border border-green-200 p-3 rounded-lg">
              <h4 className="font-semibold text-green-800">🧩 Problem Solving</h4>
              <p className="text-sm text-gray-600">
                Tree-of-Thoughts → Program-Aided → Self-Consistency
              </p>
              <p className="text-xs text-gray-500 mt-1">
                Ideal for complex reasoning and mathematical problems
              </p>
            </div>
            
            <div className="border border-purple-200 p-3 rounded-lg">
              <h4 className="font-semibold text-purple-800">✍️ Content Generation</h4>
              <p className="text-sm text-gray-600">
                Initial Generation → Auto-Prompt → RAG Enhancement
              </p>
              <p className="text-xs text-gray-500 mt-1">
                Great for creating and optimizing written content
              </p>
            </div>
          </div>
          
          <p className="text-gray-600">
            Click "Use Template" to instantly load any template into the workflow designer.
          </p>
        </div>
      ),
      action: "Continue",
      skipable: true
    },
    {
      id: "custom-workflows",
      title: "Creating Custom Workflows 🛠️",
      content: (
        <div className="space-y-4">
          <p>Build your own workflows tailored to your specific needs:</p>
          
          <div className="bg-gray-50 p-4 rounded-lg">
            <h4 className="font-semibold mb-2">Workflow Designer Steps:</h4>
            <ol className="list-decimal list-inside space-y-2 text-gray-700">
              <li><strong>Add Workflow Info:</strong> Name and description</li>
              <li><strong>Add Steps:</strong> Choose agents and configure prompts</li>
              <li><strong>Set Dependencies:</strong> Define which steps depend on others</li>
              <li><strong>Choose Providers:</strong> Select LLM for each step</li>
              <li><strong>Create & Execute:</strong> Run your custom pipeline</li>
            </ol>
          </div>
          
          <div className="bg-green-50 p-3 rounded-lg">
            <h4 className="font-semibold text-green-800 mb-1">🎯 Best Practices:</h4>
            <ul className="text-green-700 text-sm space-y-1">
              <li>• Start simple with 2-3 steps</li>
              <li>• Use clear, descriptive step names</li>
              <li>• Test individual agents first</li>
              <li>• Consider which provider works best for each task</li>
            </ul>
          </div>
        </div>
      ),
      action: "Almost done!",
      skipable: true
    },
    {
      id: "advanced-features",
      title: "Advanced Features 🚀",
      content: (
        <div className="space-y-4">
          <p>Unlock the full potential with these advanced capabilities:</p>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-blue-50 p-3 rounded-lg">
              <h4 className="font-semibold text-blue-800 mb-2">🔄 Result Passing</h4>
              <p className="text-blue-700 text-sm">
                Results from previous steps automatically enhance prompts for dependent steps.
              </p>
            </div>
            
            <div className="bg-red-50 p-3 rounded-lg">
              <h4 className="font-semibold text-red-800 mb-2">📊 Real-time Monitoring</h4>
              <p className="text-red-700 text-sm">
                Watch workflows execute with live status updates and progress tracking.
              </p>
            </div>
            
            <div className="bg-yellow-50 p-3 rounded-lg">
              <h4 className="font-semibold text-yellow-800 mb-2">🔍 Auto-Optimization</h4>
              <p className="text-yellow-700 text-sm">
                The Auto-Prompt agent automatically improves prompts for better results.
              </p>
            </div>
            
            <div className="bg-green-50 p-3 rounded-lg">
              <h4 className="font-semibold text-green-800 mb-2">🧠 Multi-Provider</h4>
              <p className="text-green-700 text-sm">
                Use different LLM providers within the same workflow for optimal results.
              </p>
            </div>
          </div>
          
          <div className="bg-purple-50 p-4 rounded-lg">
            <h4 className="font-semibold text-purple-800 mb-2">💡 Expert Tips:</h4>
            <ul className="text-purple-700 text-sm space-y-1">
              <li>• Use Chain-of-Thought for complex reasoning tasks</li>
              <li>• Try RAG agent when you need external knowledge</li>
              <li>• Use Factuality Checker to validate important information</li>
              <li>• Experiment with different agent combinations</li>
            </ul>
          </div>
        </div>
      ),
      action: "Ready to start!",
      skipable: true
    },
    {
      id: "completion",
      title: "You're All Set! 🎯",
      content: (
        <div className="space-y-4">
          <div className="text-center">
            <div className="text-6xl mb-4">🎉</div>
            <h3 className="text-xl font-semibold text-gray-800 mb-2">
              Welcome to the Future of Prompt Engineering!
            </h3>
          </div>
          
          <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-4 rounded-lg">
            <h4 className="font-semibold mb-2">Quick Start Options:</h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              <Link 
                to="/" 
                className="bg-blue-500 text-white p-3 rounded-lg text-center hover:bg-blue-600 transition-colors"
              >
                🤖 Explore Agents
              </Link>
              <Link 
                to="/workflows" 
                className="bg-purple-500 text-white p-3 rounded-lg text-center hover:bg-purple-600 transition-colors"
              >
                🔗 Try Workflows
              </Link>
            </div>
          </div>
          
          <div className="bg-gray-50 p-4 rounded-lg">
            <h4 className="font-semibold mb-2">Need Help?</h4>
            <ul className="text-gray-700 text-sm space-y-1">
              <li>📚 Check the README.md for detailed documentation</li>
              <li>🐛 Each agent shows example usage and descriptions</li>
              <li>💡 Hover over elements for additional tips</li>
              <li>🔄 You can replay this tutorial anytime from settings</li>
            </ul>
          </div>
          
          <div className="text-center">
            <p className="text-gray-600">
              Happy prompt engineering! 🚀
            </p>
          </div>
        </div>
      ),
      action: "Start Using Platform",
      skipable: false
    }
  ];

  const nextStep = () => {
    if (currentStep < tutorialSteps.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      completeTutorial();
    }
  };

  const prevStep = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const skipTutorial = () => {
    completeTutorial();
  };

  const completeTutorial = () => {
    localStorage.setItem('onboarding_completed', 'true');
    setIsVisible(false);
    if (onComplete) {
      onComplete();
    }
  };

  const restartTutorial = () => {
    setCurrentStep(0);
    setIsVisible(true);
  };

  useEffect(() => {
    const completed = localStorage.getItem('onboarding_completed');
    if (completed === 'true') {
      setIsVisible(false);
    }
  }, []);

  if (!isVisible) {
    return (
      <button
        onClick={restartTutorial}
        className="fixed bottom-4 right-4 bg-blue-500 text-white px-4 py-2 rounded-lg shadow-lg hover:bg-blue-600 transition-colors z-50"
      >
        📚 Tutorial
      </button>
    );
  }

  const step = tutorialSteps[currentStep];

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-90vh overflow-y-auto">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-500 to-purple-600 text-white p-6 rounded-t-lg">
          <div className="flex justify-between items-start">
            <div>
              <h2 className="text-2xl font-bold mb-2">{step.title}</h2>
              <div className="flex items-center space-x-2 text-blue-100">
                <span className="text-sm">
                  Step {currentStep + 1} of {tutorialSteps.length}
                </span>
                <div className="flex-1 bg-blue-400 h-2 rounded-full ml-3">
                  <div 
                    className="bg-white h-2 rounded-full transition-all duration-300"
                    style={{ width: `${((currentStep + 1) / tutorialSteps.length) * 100}%` }}
                  ></div>
                </div>
              </div>
            </div>
            {step.skipable && (
              <button
                onClick={skipTutorial}
                className="text-blue-100 hover:text-white transition-colors"
              >
                ✕ Skip
              </button>
            )}
          </div>
        </div>

        {/* Content */}
        <div className="p-6">
          {step.content}
        </div>

        {/* Footer */}
        <div className="bg-gray-50 px-6 py-4 rounded-b-lg flex justify-between items-center">
          <button
            onClick={prevStep}
            disabled={currentStep === 0}
            className="px-4 py-2 text-gray-600 hover:text-gray-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            ← Previous
          </button>

          <div className="flex space-x-2">
            {tutorialSteps.map((_, index) => (
              <div
                key={index}
                className={`w-2 h-2 rounded-full transition-colors ${
                  index === currentStep 
                    ? 'bg-blue-500' 
                    : index < currentStep 
                      ? 'bg-green-500' 
                      : 'bg-gray-300'
                }`}
              ></div>
            ))}
          </div>

          <button
            onClick={nextStep}
            className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 transition-colors"
          >
            {step.action}
          </button>
        </div>
      </div>
    </div>
  );
};

export default OnboardingTutorial;