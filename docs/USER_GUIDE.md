# 👤 User Guide

Complete guide for using the Prompt Engineering Agent Platform effectively.

## 🎯 Getting Started

### First Time Setup

1. **Complete the Onboarding Tutorial**
   - Automatically appears on first visit
   - Can be accessed anytime via "📚 Tutorial" button
   - Covers all basic concepts and features

2. **Understand the Interface**
   - **Agents Tab**: Individual agent testing
   - **Workflows Tab**: Multi-agent orchestration
   - Navigation bar at the top

3. **Choose Your LLM Provider**
   - **OpenAI**: Best for general tasks, creative content
   - **Anthropic**: Excellent for analytical tasks, safety-focused
   - **Local**: Always available, good for testing

## 🤖 Working with Individual Agents

### Understanding Agent Types

#### Core Agents

**Zero-Shot Agent** 🎯

- **Best for**: General questions, simple tasks
- **Example**: "Explain blockchain technology"
- **When to use**: When you don't have examples or the task is straightforward

**Few-Shot Agent** 📚

- **Best for**: Classification, pattern matching, structured outputs
- **Example**: Sentiment analysis with example classifications
- **When to use**: When you have examples that show the desired pattern

**Chain-of-Thought Agent** 🧠

- **Best for**: Complex reasoning, math problems, step-by-step analysis
- **Example**: "Calculate compound interest over 5 years"
- **When to use**: When you need detailed reasoning steps

**Self-Consistency Agent** ✅

- **Best for**: Validation, multiple perspective analysis
- **Example**: Checking the accuracy of a solution
- **When to use**: When you want multiple reasoning paths for reliability

**Tree-of-Thoughts Agent** 🌳

- **Best for**: Creative problem solving, exploring multiple solutions
- **Example**: "Generate multiple marketing strategies"
- **When to use**: When you need to explore different approaches

**ReAct Agent** 🔄

- **Best for**: Planning, decision-making with actions
- **Example**: "Plan a research project with actionable steps"
- **When to use**: When you need reasoning combined with actionable plans

#### Advanced Agents

**RAG Agent** 🔍

- **Best for**: Knowledge-based queries with context
- **Example**: "Analyze this document: [paste document]"
- **When to use**: When you have specific context or documents to reference

**Auto-Prompt Agent** ✨

- **Best for**: Improving vague or poorly written prompts
- **Example**: Input: "Write something" → Output: Optimized detailed prompt
- **When to use**: When you're not sure how to phrase your request

**Program-Aided Agent** 💻

- **Best for**: Mathematical calculations, logical problems
- **Example**: "Calculate the optimal investment portfolio"
- **When to use**: When the problem can benefit from computational assistance

**Factuality Checker Agent** 🕵️

- **Best for**: Verifying claims, fact-checking content
- **Example**: "Check if this news article contains accurate information"
- **When to use**: When you need to validate the accuracy of statements

### How to Test an Agent

1. **Select an Agent**
   - Click on any agent card in the library
   - Read the description to understand its purpose

2. **Configure the Request**
   - **Prompt**: Your main question or task (required)
   - **Context**: Additional background information (optional)
   - **LLM Provider**: Choose OpenAI, Anthropic, or Local
   - **Examples**: For Few-Shot agent only

3. **Submit and Review**
   - Click "Test Agent"
   - Review the response, reasoning steps, and metadata
   - Note the token usage and processing time

### Best Practices for Prompts

#### Writing Effective Prompts

**✅ Good Prompts:**

- Clear and specific: "Summarize the key benefits of renewable energy"
- Include context: "For a high school audience, explain quantum computing"
- Specify format: "List 5 pros and cons of remote work"

**❌ Poor Prompts:**

- Vague: "Tell me about stuff"
- Too broad: "Explain everything about AI"
- Ambiguous: "What should I do?"

#### Context Usage

**When to Add Context:**

- Providing background information
- Specifying target audience
- Including relevant documents or data
- Setting specific constraints or requirements

**Example:**

```text
Prompt: "Create a marketing strategy"
Context: "For a new sustainable clothing brand targeting millennials with a budget of $50k"
```

#### Examples for Few-Shot Learning

**Structure Examples Clearly:**

```text
Input: "The movie was incredible and moving"
Output: "Positive"

Input: "I wasted my time watching this boring film"  
Output: "Negative"

Input: "The plot was confusing but the acting was decent"
Output: "Mixed"
```

## 🔗 Working with Workflows

### Understanding Workflows

Workflows allow you to chain multiple agents together, where results from one agent can enhance the prompts for subsequent agents.

**Benefits:**

- **Sequential Processing**: Build on previous results
- **Parallel Execution**: Run independent tasks simultaneously
- **Quality Improvement**: Multiple perspectives and validation
- **Complex Analysis**: Break down complex tasks into manageable steps

### Using Pre-built Templates

#### Content Analysis Pipeline

**Purpose**: Comprehensive content analysis with validation
**Steps**:

1. Zero-Shot Analysis → Initial review
2. Chain-of-Thought → Detailed analysis  
3. Factuality Checker → Accuracy validation

**Best for**: Analyzing articles, reports, research papers

#### Problem Solving Workflow

**Purpose**: Multi-approach problem solving with verification
**Steps**:

1. Tree-of-Thoughts → Explore multiple solutions
2. Program-Aided → Code-assisted solving
3. Self-Consistency → Solution validation

**Best for**: Complex reasoning, mathematical problems, strategic planning

#### Content Generation & Optimization

**Purpose**: Create and improve content quality
**Steps**:

1. Zero-Shot → Initial content generation
2. Auto-Prompt → Prompt optimization
3. RAG → Knowledge enhancement

**Best for**: Writing, content creation, research summaries

### Creating Custom Workflows

#### Planning Your Workflow

##### 1. Define Your Goal

- What do you want to accomplish?
- What's the expected final output?
- How complex is the task?

##### 2. Break Down the Process

- What are the logical steps?
- Which agents are best for each step?
- What dependencies exist between steps?

##### 3. Choose Agent Sequence

- Start simple (2-3 agents)
- Consider which provider works best for each step
- Plan how results will flow between agents

#### Workflow Design Examples

##### Research Analysis Workflow

```text
Step 1: RAG Agent
- Prompt: "Analyze this research paper: [content]"
- Provider: Anthropic

Step 2: Chain-of-Thought Agent  
- Prompt: "Provide detailed methodology analysis"
- Depends on: Step 1
- Provider: OpenAI

Step 3: Factuality Checker
- Prompt: "Verify the claims and conclusions"
- Depends on: Step 2
- Provider: Anthropic
```

##### Creative Writing Workflow

```text
Step 1: Tree-of-Thoughts Agent
- Prompt: "Generate story ideas for: [theme]"
- Provider: OpenAI

Step 2: Zero-Shot Agent
- Prompt: "Write a short story based on the best idea"
- Depends on: Step 1
- Provider: OpenAI

Step 3: Auto-Prompt Agent
- Prompt: "Improve and refine the story"
- Depends on: Step 2
- Provider: Anthropic
```

#### Execution and Monitoring

##### 1. Create the Workflow

- Add all steps with proper configuration
- Set dependencies correctly
- Choose appropriate LLM providers

##### 2. Execute and Monitor

- Click "Execute" to start the workflow
- Watch real-time status updates
- Review completed steps as they finish

##### 3. Review Results

- Check the final output
- Review intermediate results
- Analyze the reasoning process

### Workflow Best Practices

#### Design Principles

##### ✅ Good Practices

- Start with simple workflows (2-3 steps)
- Use descriptive step names
- Test individual agents first
- Consider provider strengths for each task
- Plan for error handling

##### ❌ Common Mistakes

- Creating overly complex workflows initially
- Not testing agents individually first
- Circular dependencies between steps
- Using the same provider for all steps
- Vague step names and prompts

##### Optimization Tips

##### Performance

- Use parallel execution when possible
- Choose the fastest provider for each task type
- Cache results for repeated patterns
- Monitor token usage across providers

##### Quality

- Include validation steps for important workflows
- Use different providers for different perspectives
- Add factuality checking for critical information
- Build in self-consistency checks

## 🎛️ Advanced Features

### Provider Selection Strategy

#### OpenAI (GPT-4O-mini)

- **Strengths**: Creative tasks, general knowledge, code generation
- **Best for**: Content creation, brainstorming, programming help
- **Use when**: You need creative or innovative responses

#### Anthropic (Claude-3-Haiku)

- **Strengths**: Analysis, safety, structured thinking
- **Best for**: Research analysis, fact-checking, detailed reasoning
- **Use when**: You need careful, analytical responses

#### Local Provider

- **Strengths**: Always available, privacy, testing
- **Best for**: Development, testing, offline scenarios
- **Use when**: Testing workflows or API unavailable

### Result Passing and Context Enhancement

**How It Works:**
When agents depend on previous steps, their prompts are automatically enhanced with results from dependent steps.

**Example:**

```text
Step 1 Result: "The main themes are sustainability and innovation"

Step 2 Enhanced Prompt: 
"Provide detailed analysis of the content

Results from previous steps:
- Initial Analysis: The main themes are sustainability and innovation

[Original Step 2 prompt]"
```

**Benefits:**

- Automatic context building
- Improved response quality
- Seamless information flow
- No manual copy-pasting required

### Session Management

**Sessions automatically track:**

- Individual agent requests
- Workflow executions
- Results history
- Performance metrics

**Access Session History:**

- View past requests and responses
- Compare different agent approaches
- Track workflow performance over time
- Export results for analysis

### Performance Monitoring

**Real-time Monitoring:**

- Workflow execution progress
- Individual step status
- Token usage tracking
- Response time metrics

**Analytics:**

- Most used agents
- Average response times
- Success/failure rates
- Token consumption patterns

## 🎓 Use Case Examples

### Content Analysis

**Scenario**: Analyzing a research paper for accuracy and insights

**Approach**:

1. Use RAG Agent with the full paper as context
2. Follow with Chain-of-Thought for detailed analysis
3. Finish with Factuality Checker for validation

**Expected Outcome**: Comprehensive analysis with verified accuracy

### Creative Writing

**Scenario**: Writing a marketing campaign for a new product

**Approach**:

1. Tree-of-Thoughts to explore different campaign angles
2. Zero-Shot to develop the best concept
3. Auto-Prompt to refine the messaging

**Expected Outcome**: Creative, well-refined marketing content

### Problem Solving

**Scenario**: Optimizing a business process

**Approach**:

1. Chain-of-Thought to analyze current process
2. Tree-of-Thoughts to explore alternatives
3. Program-Aided to calculate optimization metrics
4. Self-Consistency to validate the solution

**Expected Outcome**: Data-driven process optimization with validation

### Fact Checking

**Scenario**: Verifying claims in a news article

**Approach**:

1. RAG Agent to analyze the article with relevant context
2. Factuality Checker to verify specific claims
3. Chain-of-Thought to assess overall credibility

**Expected Outcome**: Detailed fact-check report with reasoning

## 🛟 Troubleshooting

### Common Issues

**Agent Not Responding:**

- Check if the correct LLM provider is selected
- Verify API keys are configured (use Local provider to test)
- Try a simpler prompt first

**Workflow Stuck:**

- Check for circular dependencies
- Verify all step names are unique
- Ensure dependent steps exist and are spelled correctly

**Poor Quality Responses:**

- Try different LLM providers
- Add more context to your prompt
- Use examples for Few-Shot agent
- Consider breaking complex tasks into smaller steps

**Performance Issues:**

- Use Local provider for testing
- Reduce prompt length and complexity
- Consider workflow optimization
- Check internet connection

### Getting Help

1. **Use the Tutorial**: Click "📚 Tutorial" anytime for guidance
2. **Check Documentation**: Review README.md and troubleshooting guides
3. **Start Simple**: Test basic functionality before complex workflows
4. **Experiment**: Try different agents and providers for the same task

## 📈 Tips for Success

### Learning the Platform

1. **Start with Individual Agents**
   - Test each agent type with simple prompts
   - Understand their strengths and use cases
   - Compare responses across different providers

2. **Progress to Simple Workflows**
   - Use pre-built templates first
   - Create 2-step custom workflows
   - Gradually add complexity

3. **Experiment and Iterate**
   - Try the same task with different agents
   - Compare provider performance
   - Refine prompts based on results

### Maximizing Results

1. **Choose the Right Agent**
   - Zero-Shot for simple, direct questions
   - Chain-of-Thought for complex reasoning
   - RAG when you have specific context
   - Auto-Prompt when unsure how to ask

2. **Optimize Your Prompts**
   - Be specific and clear
   - Provide relevant context
   - Specify desired output format
   - Include examples when appropriate

3. **Leverage Workflows**
   - Use multiple perspectives for important decisions
   - Include validation steps for critical information
   - Build on previous results for comprehensive analysis
   - Mix different agent types for diverse approaches

---

Happy prompt engineering! 🚀 The platform is designed to grow with your skills - start simple and gradually explore more advanced features as you become comfortable with the basics.
