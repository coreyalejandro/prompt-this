# 🛠️ Troubleshooting Guide

Comprehensive troubleshooting guide for the Prompt Engineering Agent Platform.

## 📋 Quick Diagnostic Checklist

Before diving into specific issues, run through this quick checklist:

```bash
# 1. Check service status
sudo supervisorctl status

# 2. Test API connectivity
curl http://localhost:8001/api/

# 3. Check database connection
mongo --eval "db.adminCommand('ismaster')"

# 4. Verify environment variables
env | grep -E "(OPENAI|ANTHROPIC|MONGO)"

# 5. Check logs for errors
tail -n 50 /var/log/supervisor/backend.err.log
```

## 🚨 Critical Issues

### Issue: Platform Won't Start

**Symptoms:**
- Services fail to start
- Error messages during startup
- Can't access web interface

**Diagnostic Steps:**
```bash
# Check all services
sudo supervisorctl status

# If services are down, try starting
sudo supervisorctl start all

# Check for port conflicts
netstat -tlnp | grep -E "(3000|8001|27017)"

# Verify MongoDB is running
sudo systemctl status mongodb
```

**Solutions:**
1. **Port Conflicts:**
   ```bash
   # Kill processes using required ports
   sudo lsof -ti:3000 | xargs kill -9
   sudo lsof -ti:8001 | xargs kill -9
   
   # Restart services
   sudo supervisorctl restart all
   ```

2. **MongoDB Issues:**
   ```bash
   # Start MongoDB
   sudo systemctl start mongodb
   sudo systemctl enable mongodb
   
   # Create required directories
   sudo mkdir -p /var/lib/mongodb
   sudo chown mongodb:mongodb /var/lib/mongodb
   ```

3. **Permission Issues:**
   ```bash
   # Fix ownership
   sudo chown -R $USER:$USER /app
   
   # Fix permissions
   chmod +x /app/scripts/*
   ```

### Issue: "Create Workflow" Button Not Working

**Symptoms:**
- Button appears but doesn't respond
- No success/error messages
- Workflows don't appear in list

**Diagnostic Steps:**
```bash
# Check backend logs
tail -f /var/log/supervisor/backend.err.log

# Test workflow endpoint manually
curl -X GET http://localhost:8001/api/workflows

# Check browser console
# Open DevTools (F12) → Console tab
```

**Solutions:**
1. **MongoDB ObjectId Serialization (Fixed):**
   - This was a known issue that has been resolved
   - Ensure you're running the latest version

2. **API Endpoint Issues:**
   ```bash
   # Test workflow creation
   curl -X POST "http://localhost:8001/api/workflows" \
     -H "Content-Type: application/json" \
     -d '{"name": "Test", "steps": [{"name": "Step1", "agent_type": "zero_shot", "prompt": "test"}]}'
   ```

3. **Frontend JavaScript Errors:**
   - Open browser DevTools (F12)
   - Check Console for JavaScript errors
   - Refresh page to reload JavaScript

### Issue: Agents Not Responding

**Symptoms:**
- Agent requests timeout
- Error messages from LLM providers
- Agents return placeholder responses

**Diagnostic Steps:**
```bash
# Test agent endpoint
curl -X GET http://localhost:8001/api/agents

# Test specific agent
curl -X POST "http://localhost:8001/api/agents/process" \
  -H "Content-Type: application/json" \
  -d '{"agent_type": "zero_shot", "llm_provider": "local", "request": {"prompt": "test"}}'

# Check API keys
echo $OPENAI_API_KEY | head -c 10
echo $ANTHROPIC_API_KEY | head -c 10
```

**Solutions:**
1. **Missing API Keys:**
   ```bash
   # Add keys to backend/.env
   echo "OPENAI_API_KEY=your_key_here" >> backend/.env
   echo "ANTHROPIC_API_KEY=your_key_here" >> backend/.env
   
   # Restart backend
   sudo supervisorctl restart backend
   ```

2. **Invalid API Keys:**
   ```bash
   # Test OpenAI key
   curl -H "Authorization: Bearer $OPENAI_API_KEY" \
     https://api.openai.com/v1/models
   
   # Test Anthropic key
   curl -H "x-api-key: $ANTHROPIC_API_KEY" \
     https://api.anthropic.com/v1/messages \
     -H "Content-Type: application/json" \
     -d '{"model": "claude-3-haiku-20240307", "max_tokens": 10, "messages": [{"role": "user", "content": "Hi"}]}'
   ```

3. **Rate Limiting:**
   ```bash
   # Use local provider for testing
   # Change llm_provider to "local" in requests
   # Check provider dashboard for rate limits
   ```

## ⚠️ Common Issues

### Issue: Frontend Build Errors

**Symptoms:**
- `yarn start` fails
- Module not found errors
- Build compilation errors

**Solutions:**
```bash
# Clear cache and reinstall
cd frontend
rm -rf node_modules yarn.lock
yarn install

# Check Node.js version
node --version  # Should be 18+

# Alternative package manager
npm install --legacy-peer-deps

# Force reinstall specific packages
yarn add react react-dom --force
```

### Issue: Backend Import Errors

**Symptoms:**
- `ModuleNotFoundError` when starting
- Python import failures

**Solutions:**
```bash
# Install missing dependencies
cd backend
pip install -r requirements.txt

# Update pip and setuptools
pip install --upgrade pip setuptools

# Use virtual environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Check Python version
python --version  # Should be 3.11+
```

### Issue: Database Connection Failures

**Symptoms:**
- "Connection refused" errors
- MongoDB timeout errors
- Collection not found errors

**Solutions:**
```bash
# Start MongoDB
sudo systemctl start mongodb

# Check MongoDB status
sudo systemctl status mongodb

# Test connection
mongo mongodb://localhost:27017/test_database

# Reset database (if needed)
mongo --eval "db.dropDatabase()" test_database

# Check disk space
df -h
```

### Issue: Workflow Execution Hangs

**Symptoms:**
- Workflows stuck in "running" status
- Steps don't progress
- No error messages

**Solutions:**
1. **Check Dependencies:**
   ```bash
   # Look for circular dependencies
   # Verify all required steps exist
   # Check step names match exactly
   ```

2. **Resource Issues:**
   ```bash
   # Check memory usage
   free -h
   
   # Check CPU usage
   top
   
   # Check disk space
   df -h
   ```

3. **Agent Failures:**
   ```bash
   # Check individual agents
   curl -X POST "http://localhost:8001/api/agents/process" \
     -H "Content-Type: application/json" \
     -d '{"agent_type": "zero_shot", "llm_provider": "local", "request": {"prompt": "test"}}'
   ```

4. **Restart Services:**
   ```bash
   sudo supervisorctl restart all
   ```

### Issue: Slow Performance

**Symptoms:**
- Long response times
- Timeouts
- UI feels sluggish

**Solutions:**
1. **Backend Optimization:**
   ```bash
   # Increase worker processes
   uvicorn server:app --workers 4 --host 0.0.0.0 --port 8001
   
   # Enable caching
   # Consider Redis for better caching
   ```

2. **Frontend Optimization:**
   ```bash
   # Build production version
   cd frontend
   yarn build
   serve -s build -l 3000
   ```

3. **Database Optimization:**
   ```javascript
   // Create indexes
   db.workflows.createIndex({ "created_at": -1 })
   db.agent_responses.createIndex({ "session_id": 1 })
   ```

4. **Provider Selection:**
   - Use `local` provider for testing
   - Choose fastest provider for each agent type
   - Implement request batching

## 🔍 Debugging Techniques

### Backend Debugging

**Enable Debug Logging:**
```python
# In server.py, change logging level
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

**Python Debugger:**
```python
# Add breakpoints in code
import pdb; pdb.set_trace()

# Or use ipdb for better debugging
import ipdb; ipdb.set_trace()
```

**API Request Debugging:**
```bash
# Verbose curl for detailed request/response
curl -v -X POST "http://localhost:8001/api/agents/process" \
  -H "Content-Type: application/json" \
  -d '{"agent_type": "zero_shot", "llm_provider": "local", "request": {"prompt": "test"}}'
```

### Frontend Debugging

**React DevTools:**
- Install React Developer Tools browser extension
- Inspect component state and props
- Track re-renders and performance

**Browser Console:**
```javascript
// Enable debugging in browser console
localStorage.setItem('debug', 'true');

// Debug API calls
console.log('API Request:', requestData);
console.log('API Response:', responseData);

// Check React errors
window.addEventListener('error', (e) => {
  console.error('JavaScript Error:', e.error);
});
```

**Network Tab:**
- Open DevTools (F12) → Network tab
- Monitor API requests and responses
- Check for failed requests or slow responses

### Database Debugging

**MongoDB Queries:**
```javascript
// Check collections
show collections

// Query workflows
db.workflows.find().pretty()

// Query with filters
db.workflows.find({"status": "running"}).pretty()

// Check indexes
db.workflows.getIndexes()

// Query performance
db.workflows.find({"status": "completed"}).explain("executionStats")
```

**Connection Testing:**
```bash
# Test connection
mongo --eval "db.adminCommand('ismaster')"

# Check database size
mongo --eval "db.stats()" test_database

# Monitor operations
mongo --eval "db.currentOp()"
```

## 📊 Monitoring and Logs

### Log Locations

**Backend Logs:**
```bash
# Supervisor logs
/var/log/supervisor/backend.out.log  # stdout
/var/log/supervisor/backend.err.log  # stderr

# Application logs
tail -f /var/log/supervisor/backend.err.log

# Filter for errors
grep -i error /var/log/supervisor/backend.err.log
```

**Frontend Logs:**
```bash
# Supervisor logs
/var/log/supervisor/frontend.out.log
/var/log/supervisor/frontend.err.log

# Build logs
yarn start > frontend.log 2>&1 &
tail -f frontend.log
```

**MongoDB Logs:**
```bash
# Default MongoDB log location
/var/log/mongodb/mongod.log

# Monitor MongoDB logs
tail -f /var/log/mongodb/mongod.log

# Filter for errors
grep -i error /var/log/mongodb/mongod.log
```

### Health Checks

**System Health Script:**
```bash
#!/bin/bash
echo "=== Health Check Report ==="
echo "Date: $(date)"
echo

echo "--- Service Status ---"
sudo supervisorctl status

echo
echo "--- Port Status ---"
netstat -tlnp | grep -E "(3000|8001|27017)"

echo
echo "--- API Test ---"
curl -s http://localhost:8001/api/ || echo "API not responding"

echo
echo "--- Database Test ---"
mongo --quiet --eval "print('MongoDB: ' + (db.adminCommand('ismaster').ismaster ? 'OK' : 'ERROR'))"

echo
echo "--- Disk Space ---"
df -h | grep -E "(/$|/var)"

echo
echo "--- Memory Usage ---"
free -h

echo "=== End Health Check ==="
```

**Automated Monitoring:**
```bash
# Create monitoring script
cat > /app/scripts/monitor.sh << 'EOF'
#!/bin/bash
while true; do
  if ! curl -s http://localhost:8001/api/ > /dev/null; then
    echo "$(date): API down, restarting backend"
    sudo supervisorctl restart backend
  fi
  sleep 60
done
EOF

chmod +x /app/scripts/monitor.sh
# Run in background: nohup /app/scripts/monitor.sh &
```

## 🚑 Emergency Recovery

### Complete System Reset

**When Everything Fails:**
```bash
# 1. Stop all services
sudo supervisorctl stop all

# 2. Kill any hanging processes
sudo pkill -f "uvicorn\|node\|mongo"

# 3. Clean up temporary files
rm -rf /tmp/mongodb-*.sock
rm -rf /app/frontend/node_modules/.cache

# 4. Restart MongoDB
sudo systemctl restart mongodb

# 5. Reinstall dependencies
cd /app/backend && pip install -r requirements.txt
cd /app/frontend && rm -rf node_modules && yarn install

# 6. Start services
sudo supervisorctl start all

# 7. Verify everything works
curl http://localhost:8001/api/
```

### Database Recovery

**Reset Database:**
```bash
# Backup existing data (optional)
mongodump --db test_database --out /tmp/backup

# Drop and recreate database
mongo --eval "db.dropDatabase()" test_database

# Restart backend to recreate collections
sudo supervisorctl restart backend
```

### Configuration Recovery

**Reset to Default Configuration:**
```bash
# Backup current config
cp /app/backend/.env /app/backend/.env.backup
cp /app/frontend/.env /app/frontend/.env.backup

# Restore default configuration
cat > /app/backend/.env << 'EOF'
MONGO_URL="mongodb://localhost:27017"
DB_NAME="test_database"

# LLM API Keys (add your keys here)
# OPENAI_API_KEY=your_openai_api_key_here
# ANTHROPIC_API_KEY=your_anthropic_api_key_here
EOF

cat > /app/frontend/.env << 'EOF'
WDS_SOCKET_PORT=443
REACT_APP_BACKEND_URL=http://localhost:8001
EOF

# Restart services
sudo supervisorctl restart all
```

## 📞 Getting Help

### Self-Diagnosis Steps

1. **Check the Quick Diagnostic Checklist** (top of this document)
2. **Review relevant log files** for error messages
3. **Test individual components** (API, database, frontend)
4. **Compare with known working configurations**

### Information to Collect

When seeking help, collect this information:

```bash
# System Information
uname -a
python --version
node --version

# Service Status
sudo supervisorctl status

# Recent Logs
tail -n 100 /var/log/supervisor/backend.err.log
tail -n 100 /var/log/supervisor/frontend.err.log

# Configuration
cat /app/backend/.env | sed 's/API_KEY=.*/API_KEY=***HIDDEN***/'
cat /app/frontend/.env

# API Test
curl -v http://localhost:8001/api/

# Database Test
mongo --eval "db.adminCommand('ismaster')"
```

### Contact and Resources

- **Documentation**: Check README.md and API_DOCUMENTATION.md
- **GitHub Issues**: Create detailed issue reports
- **Community Forums**: Share experiences and solutions
- **Stack Overflow**: Tag questions with relevant technologies

---

Remember: Most issues can be resolved by carefully following the diagnostic steps and checking logs for specific error messages. When in doubt, try the complete system reset procedure.