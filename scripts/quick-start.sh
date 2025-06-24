#!/bin/bash

# Promptly Quick Start Script
# This script sets up Promptly for local development

set -e

echo "🤖 Welcome to Promptly Setup!"
echo "================================"

# Check requirements
echo "📋 Checking requirements..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3.11+ is required. Please install Python first."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d" " -f2 | cut -d"." -f1,2)
if ! python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)"; then
    echo "❌ Python 3.11+ is required. Current version: $PYTHON_VERSION"
    exit 1
fi

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 18+ is required. Please install Node.js first."
    exit 1
fi

NODE_VERSION=$(node --version | cut -d"v" -f2 | cut -d"." -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js 18+ is required. Current version: v$NODE_VERSION"
    exit 1
fi

# Check MongoDB
if ! command -v mongod &> /dev/null; then
    echo "⚠️  MongoDB not found. Installing via package manager..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y mongodb
    elif command -v brew &> /dev/null; then
        brew tap mongodb/brew
        brew install mongodb-community
    else
        echo "❌ Please install MongoDB manually: https://docs.mongodb.com/manual/installation/"
        exit 1
    fi
fi

echo "✅ All requirements satisfied!"

# Setup backend
echo ""
echo "🔧 Setting up backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install -r requirements.txt

# Setup environment
if [ ! -f ".env" ]; then
    echo "Creating backend .env file..."
    cat > .env << EOF
MONGO_URL="mongodb://localhost:27017"
DB_NAME="promptly_database"

# LLM API Keys (optional - add your keys to enable providers)
# OPENAI_API_KEY=your_openai_api_key_here
# ANTHROPIC_API_KEY=your_anthropic_api_key_here
EOF
fi

cd ..

# Setup frontend
echo ""
echo "🎨 Setting up frontend..."
cd frontend

if ! command -v yarn &> /dev/null; then
    echo "Installing yarn..."
    npm install -g yarn
fi

echo "Installing frontend dependencies..."
yarn install

# Setup environment
if [ ! -f ".env" ]; then
    echo "Creating frontend .env file..."
    cat > .env << EOF
REACT_APP_BACKEND_URL=http://localhost:8001
EOF
fi

cd ..

# Start MongoDB
echo ""
echo "🗄️  Starting MongoDB..."
if command -v systemctl &> /dev/null; then
    sudo systemctl start mongodb
    sudo systemctl enable mongodb
elif command -v brew &> /dev/null; then
    brew services start mongodb/brew/mongodb-community
else
    echo "Starting MongoDB manually..."
    mongod --dbpath /usr/local/var/mongodb &
fi

# Wait for MongoDB to start
echo "Waiting for MongoDB to start..."
sleep 3

# Create start script
echo ""
echo "📝 Creating start script..."
cat > start-promptly.sh << 'EOF'
#!/bin/bash

echo "🤖 Starting Promptly..."

# Function to kill background processes on exit
cleanup() {
    echo ""
    echo "🛑 Stopping Promptly..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start backend
echo "🔧 Starting backend..."
cd backend
source venv/bin/activate
uvicorn server:app --host 0.0.0.0 --port 8001 --reload > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 5

# Start frontend
echo "🎨 Starting frontend..."
cd frontend
yarn start > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Promptly is starting up!"
echo "🌐 Frontend: http://localhost:3000"
echo "📡 Backend API: http://localhost:8001"
echo "📖 API Docs: http://localhost:8001/docs"
echo ""
echo "📋 To view logs:"
echo "   Backend: tail -f backend.log"
echo "   Frontend: tail -f frontend.log"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for processes
wait $BACKEND_PID $FRONTEND_PID
EOF

chmod +x start-promptly.sh

# Success message
echo ""
echo "🎉 Promptly setup complete!"
echo "=========================="
echo ""
echo "🚀 To start Promptly:"
echo "   ./start-promptly.sh"
echo ""
echo "🌐 Once started, open: http://localhost:3000"
echo ""
echo "💡 First time? The interactive tutorial will guide you!"
echo ""
echo "📚 Documentation:"
echo "   README.md - Overview and features"
echo "   docs/USER_GUIDE.md - How to use Promptly"
echo "   docs/API_DOCUMENTATION.md - API reference"
echo ""
echo "🔑 Optional: Add your API keys to backend/.env for full LLM support"
echo "   - OpenAI API key for GPT models"
echo "   - Anthropic API key for Claude models"
echo ""
echo "Happy prompt engineering! 🚀"