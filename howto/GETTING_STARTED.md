# Architecture as a Service - Setup Guide

**Quick Start**: Get up and running in 5 minutes with your own API key

---

## 📋 Prerequisites

### Required
- **Python 3.9+** (3.11+ recommended)
- **GraphViz** (system package)
- **API Key** from one of:
  - Google Gemini (recommended - FREE)
  - OpenAI
  - Anthropic Claude
  - Azure OpenAI

### Optional
- **draw.io** (for editing generated diagrams)
- **VS Code** with draw.io extension

---

##  Installation Steps

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/AaaS.git
cd AaaS/ArchitectureasService
```

---

### 2. Install GraphViz

**macOS**:
```bash
brew install graphviz
```

**Ubuntu/Debian**:
```bash
sudo apt-get update
sudo apt-get install graphviz
```

**Windows**:
1. Download installer from https://graphviz.org/download/
2. Run installer
3. Add to PATH: `C:\Program Files\Graphviz\bin`

**Verify Installation**:
```bash
dot -version
# Should show: dot - graphviz version X.X.X
```

---

### 3. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate

# Verify
which python  # Should point to venv/bin/python
```

---

### 4. Install Python Dependencies

```bash
# Ensure venv is activated (you should see (venv) in prompt)
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep -E "(diagrams|graphviz2drawio|Flask|google-generativeai)"
```

**Expected Output**:
```
diagrams               0.24.4
Flask                  3.0.0
google-generativeai    0.3.2
graphviz               0.20.3
graphviz2drawio        1.1.0
```

---

### 5. Get API Key (Choose ONE)

#### Option A: Google Gemini (RECOMMENDED - FREE)

**Why Gemini?**
-  FREE tier: 60 requests/minute
-  Fast response times (~1-2 seconds)
-  Latest model: Gemini 2.5 Flash
-  Easy setup

**Get API Key**:
1. Visit: https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key (starts with `AIza...`)

**Cost**: FREE (or $0.0001 per request if exceeding free tier)

---

#### Option B: OpenAI

**Why OpenAI?**
-  High quality responses
-  GPT-4 Turbo available
-  More expensive ($0.002-$0.03 per request)

**Get API Key**:
1. Visit: https://platform.openai.com/api-keys
2. Create new secret key
3. Copy the key (starts with `sk-...`)

**Cost**: $0.002 (GPT-3.5) to $0.03 (GPT-4) per diagram

---

#### Option C: Anthropic Claude

**Why Claude?**
-  Excellent reasoning
-  Long context support
-  No free tier

**Get API Key**:
1. Visit: https://console.anthropic.com/
2. Create API key
3. Copy the key

**Cost**: ~$0.015 per diagram

---

#### Option D: Azure OpenAI

**Why Azure OpenAI?**
-  Enterprise compliance
-  Regional deployment
-  Requires Azure subscription

**Setup**:
1. Create Azure OpenAI resource
2. Deploy a model
3. Get endpoint and key from Azure Portal

**Cost**: Varies by region and model

---

### 6. Configure Environment

```bash
# Copy template
cp .env.example .env

# Edit configuration
nano .env  # or use your preferred editor
```

**For Google Gemini** (recommended):
```bash
# Enable AI Parser
USE_AI_PARSER=true

# Choose Gemini provider
AI_PROVIDER=gemini

# Enable MCP (Azure best practices)
USE_MCP=true

# Add your API key
GOOGLE_API_KEY=AIzaSyB...your_actual_key_here

# Optional: Specify model (default is gemini-2.5-flash)
GEMINI_MODEL=gemini-2.5-flash
```

**For OpenAI**:
```bash
USE_AI_PARSER=true
AI_PROVIDER=openai
USE_MCP=true
OPENAI_API_KEY=sk-...your_key_here
OPENAI_MODEL=gpt-4-turbo-preview  # or gpt-3.5-turbo
```

**For Anthropic Claude**:
```bash
USE_AI_PARSER=true
AI_PROVIDER=anthropic
USE_MCP=true
ANTHROPIC_API_KEY=sk-ant-...your_key_here
CLAUDE_MODEL=claude-3-5-sonnet-20241022
```

**For Azure OpenAI**:
```bash
USE_AI_PARSER=true
AI_PROVIDER=azure_openai
USE_MCP=true
AZURE_OPENAI_API_KEY=your_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=your-deployment-name
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

---

### 7. Start the Server

```bash
# Ensure venv is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Start server
python app.py
```

**Expected Output**:
```
 Initializing AI Parser: gemini
 MCP enabled for Azure knowledge
 Gemini initialized: gemini-2.5-flash
================================================================================
 AI-POWERED PARSER ENABLED
   Provider: gemini
   MCP: Enabled
================================================================================
 Azure Architecture Diagram Generator - Web Application
 Access the application at: http://localhost:5001
```

---

### 8. Open Web Interface

Open your browser and visit:
```
http://localhost:5001
```

You should see the **Architecture as a Service** web interface!

---

## 🧪 Test Your Setup

### Test 1: Simple Web App

1. Enter in the text box:
   ```
   Create a web application with database and caching
   ```

2. Click "Generate Diagram"

3. **Expected Result**:
   - Generation takes ~2-3 seconds
   - PNG preview appears
   - Download links for PNG, DOT, and draw.io files
   - Architecture includes:
     - Application Gateway
     - App Service
     - SQL Database
     - Redis Cache
     - Key Vault
     - Application Insights

---

### Test 2: E-Commerce Platform

1. Enter:
   ```
   Build a scalable e-commerce platform with payment processing
   ```

2. **Expected Result**:
   - 13 components generated
   - Includes:
     - Application Gateway + WAF
     - Web Frontend (load balanced)
     - API Management
     - Backend APIs
     - SQL Database + Cosmos DB
     - Redis Cache
     - Key Vault
     - Monitoring

---

### Test 3: CI/CD Pipeline with GitHub

1. Enter:
   ```
   CI/CD pipeline with GitHub, Azure Container Registry, and AKS deployment
   ```

2. **Expected Result**:
   - GitHub icon appears
   - Azure Container Registry
   - AKS cluster
   - Key Vault
   - Application Insights

---

## 💡 Supported Services

### Monitoring
- Azure Monitor
- Application Insights
- Grafana (Integration)
- Power BI (Integration)

### Collaboration (Integration)
- Jira
- Confluence
- GitHub

### IoT
- IoT Hub

---

## 📁 Output Files

Generated diagrams are saved in `output/` directory:

```bash
ls -lh output/

# You'll see:
azure_arch_TIMESTAMP.png      # 142-297 KB - Image file
azure_arch_TIMESTAMP.dot      # 7.8-19 KB - GraphViz source
azure_arch_TIMESTAMP.drawio   # 184-338 KB - Editable in draw.io
```

---

##  Using Generated Diagrams

### View PNG

```bash
# macOS
open output/azure_arch_TIMESTAMP.png

# Linux
xdg-open output/azure_arch_TIMESTAMP.png

# Windows
start output/azure_arch_TIMESTAMP.png
```

---

### Edit in draw.io

**Option 1: Online**
1. Visit https://app.diagrams.net
2. File → Open → Choose `azure_arch_TIMESTAMP.drawio`
3. Edit and export

**Option 2: VS Code**
1. Install draw.io extension
2. Open `.drawio` file in VS Code
3. Edit directly

**Option 3: Desktop App**
1. Download from https://github.com/jgraph/drawio-desktop/releases
2. Install and open `.drawio` file

---

### Version Control (DOT files)

```bash
# Add to git
git add output/azure_arch_TIMESTAMP.dot

# Commit
git commit -m "Add architecture diagram for e-commerce platform"

# Push
git push
```

---

## 🔧 Configuration Options

### Environment Variables

| Variable | Required | Default | Options |
|----------|----------|---------|---------|
| `USE_AI_PARSER` | Yes | `false` | `true`, `false` |
| `AI_PROVIDER` | Yes | `gemini` | `gemini`, `openai`, `anthropic`, `azure_openai` |
| `USE_MCP` | No | `true` | `true`, `false` |
| `GOOGLE_API_KEY` | If Gemini | - | Your API key |
| `OPENAI_API_KEY` | If OpenAI | - | Your API key |
| `ANTHROPIC_API_KEY` | If Claude | - | Your API key |
| `AZURE_OPENAI_API_KEY` | If Azure | - | Your API key |

### Model Selection

**Gemini**:
- `gemini-2.5-flash` (recommended - fastest, cheapest)
- `gemini-1.5-pro` (more capable, slower)

**OpenAI**:
- `gpt-3.5-turbo` (fast, cheap)
- `gpt-4-turbo-preview` (best quality, expensive)
- `gpt-4` (high quality, very expensive)

**Claude**:
- `claude-3-5-sonnet-20241022` (recommended)
- `claude-3-opus-20240229` (most capable)

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'diagrams'"

**Solution**:
```bash
# Ensure venv is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

---

### Issue: "graphviz2drawio not found"

**Solution**:
```bash
pip install graphviz2drawio
```

---

### Issue: "Graphviz executable not found"

**Solution**: Install GraphViz system package (see Step 2)

---

### Issue: "AI parser failed to initialize"

**Causes**:
1. Invalid API key
2. Wrong provider name
3. Missing `.env` file

**Solutions**:
```bash
# Check .env file exists
ls -la .env

# Verify API key is set
grep API_KEY .env

# Test API key manually
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('Provider:', os.getenv('AI_PROVIDER'))
print('API Key exists:', os.getenv('GOOGLE_API_KEY') is not None)
"
```

---

### Issue: "Port 5001 already in use"

**Solution**:
```bash
# Kill process on port 5001
lsof -ti:5001 | xargs kill -9

# Or change port in app.py
# Change line: app.run(host='0.0.0.0', port=5001, debug=True)
# To:           app.run(host='0.0.0.0', port=5002, debug=True)
```

---

### Issue: "No Azure icons in diagrams"

**Expected**: Icons are embedded in PNG files automatically

**Verify**:
1. Check PNG file size (should be 100+ KB)
2. Open PNG file - you should see Azure service icons
3. If icons are missing, ensure diagrams library is correctly installed:
   ```bash
   pip install --upgrade diagrams
   ```

---

### Issue: "draw.io files not editable"

**Solution**: Ensure graphviz2drawio is installed:
```bash
pip install graphviz2drawio
```

Check server output for:
```
 Generated draw.io file: /path/to/file.drawio
```

---

### Issue: "Rate limit exceeded"

**Cause**: Too many requests to AI provider

**Solutions**:
- **Gemini**: Free tier is 60 requests/minute - wait 1 minute
- **OpenAI**: Check your usage limits
- **Claude**: Check your API quota
- **Temporary**: Switch to different provider

---

### Issue: "AI generates wrong architecture"

**Solutions**:
1. **Be more specific** in description
2. **Mention exact services** needed
3. **Describe layers** (frontend, application, data)
4. **Include requirements** (scale, security, performance)

**Example**:
 Bad: "Create a web app"
 Good: "Create a scalable web application with load balancer, multiple app instances, SQL database for data, Redis for caching, and monitoring"

---

##  Performance Tips

### Faster Generation

1. **Use Gemini** - Fastest AI provider (~1-2 seconds)
2. **Disable MCP** if not needed - Set `USE_MCP=false`
3. **Use simpler descriptions** - Fewer components = faster generation

### Lower Costs

1. **Use Gemini FREE tier** - 60 requests/minute free
2. **Batch requests** - Generate multiple variations at once
3. **Use GPT-3.5 instead of GPT-4** if using OpenAI

### Better Quality

1. **Enable MCP** - Set `USE_MCP=true` for Azure best practices
2. **Be specific** - Detailed descriptions = better architectures
3. **Use GPT-4** - Best quality (but expensive)

---

## 🎓 Next Steps

### 1. Learn Best Practices
- Review `WORKFLOW_GUIDE.md` to understand the generation process.

### 2. Explore Features
- Try different AI providers
- Test with complex architectures
- Edit diagrams in draw.io

### 3. Customize
- Modify `ai_parser.py` for custom prompts
- Update `diagram_generator.py` for custom styles
- Add new service types to `service_mapping`

### 4. Integrate
- Use API endpoints in your apps
- Automate diagram generation
- Version control diagrams with git

---

## Additional Resources

### Documentation
- [WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md) - Workflow and Connection logic
- [AI_INTEGRATION.md](AI_INTEGRATION.md) - AI & MCP Integration details

### API Endpoints

```bash
# Health check
curl http://localhost:5001/api/health

# Generate diagram
curl -X POST http://localhost:5001/api/generate \
  -H "Content-Type: application/json" \
  -d '{"description": "Your architecture description"}'

# Parse only (no diagram generation)
curl -X POST http://localhost:5001/api/parse \
  -H "Content-Type: application/json" \
  -d '{"description": "Your architecture description"}'

# Get examples
curl http://localhost:5001/api/examples
```

---

## 🤝 Getting Help

### Common Issues
1. Check this guide's Troubleshooting section
2. Review error messages in terminal
3. Check `output/` directory for generated files

### Still Need Help?
1. Check documentation in `docs/` directory
2. Open GitHub issue
3. Check GitHub discussions

---

##  Setup Checklist

- [ ] Python 3.9+ installed
- [ ] GraphViz installed (`dot -version` works)
- [ ] Repository cloned
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] API key obtained (Gemini recommended)
- [ ] `.env` file created and configured
- [ ] Server starts without errors
- [ ] Web interface accessible at http://localhost:5001
- [ ] Test diagram generates successfully
- [ ] PNG, DOT, and draw.io files created

---

## 🎉 You're Ready!

Your Architecture as a Service is now set up and ready to use!

**Next**: Open http://localhost:5001 and start generating diagrams!

---

**Version**: 1.1.0
**Last Updated**: January 10, 2026
**Status**:  Production Ready
**Support**: [GitHub Issues](https://github.com/yourusername/AaaS/issues)
