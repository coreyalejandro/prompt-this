#!/bin/bash

echo "🤖 Starting Prompt-This..."

# Function to kill background processes on exit
cleanup() {
    echo ""
    echo "🛑 Stopping Prompt-This..."
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
echo "✅ Prompt-This is starting up!"
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
