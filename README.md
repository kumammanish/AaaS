# Architecture as a Service

> **AI-Powered Azure Architecture Diagram Generator** - Transform natural language into professional, editable architecture diagrams

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)

---

##  Quick Start

```bash
# 1. Install dependencies
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Install GraphViz
brew install graphviz  # macOS
# OR: sudo apt-get install graphviz  # Linux

# 3. Configure
cp .env.example .env
nano .env  # Add your API key

# 4. Run
python app.py

# 5. Open browser
# Visit: http://localhost:5001
```

**Get FREE API Key**: [Google AI Studio](https://aistudio.google.com/app/apikey) (60 requests/minute)

---

##  Features

-  **Multi-Provider AI**: Google Gemini (FREE), OpenAI, Claude, Azure OpenAI
-  **30+ Azure Services**: Compute, Database, Storage, Network, Security, AI/ML
-  **Editable Diagrams**: PNG, DOT, draw.io formats
-  **Simplified Workflows**: Clean connections (67-90% reduction)
-  **Integration Icons**: GitHub, MCP servers, Confluence
-  **Easy Setup**: 5-minute installation
-  **Web Interface**: Simple, intuitive UI

---

##  Example Usage

**Input**:
```
Build a scalable e-commerce platform with payment processing
```

**Generated** (13 components):
- Application Gateway + WAF
- Web Frontend (load balanced)
- API Management
- Backend APIs (multiple instances)
- SQL Database + Cosmos DB
- Redis Cache + Key Vault
- Application Insights + Azure Monitor
- Virtual Network

**Output Files**:
- `azure_arch_TIMESTAMP.png` (297 KB)
- `azure_arch_TIMESTAMP.dot` (19 KB)
- `azure_arch_TIMESTAMP.drawio` (338 KB)

---

##  Documentation

All comprehensive guides are in the **[howto/](howto/)** directory:

### Getting Started
- **[SETUP_GUIDE.md](howto/SETUP_GUIDE.md)** - Complete setup walkthrough
- **[QUICK_AI_SETUP.md](howto/QUICK_AI_SETUP.md)** - 5-minute AI setup

### Architecture & Implementation
- **[ARCHITECTURE_EXPLAINED.md](howto/ARCHITECTURE_EXPLAINED.md)** - How it works
- **[AI_MCP_INTEGRATION_GUIDE.md](howto/AI_MCP_INTEGRATION_GUIDE.md)** - AI integration details
- **[AI_IMPLEMENTATION_TEST_RESULTS.md](howto/AI_IMPLEMENTATION_TEST_RESULTS.md)** - Performance tests

### Features & Updates
- **[DRAW_IO_UPDATE_SUMMARY.md](howto/DRAW_IO_UPDATE_SUMMARY.md)** - draw.io compatibility
- **[WORKFLOW_SIMPLIFICATION_AND_ICONS_UPDATE.md](howto/WORKFLOW_SIMPLIFICATION_AND_ICONS_UPDATE.md)** - Connection optimization
- **[SVG_DRAWIO_GUIDE.md](howto/SVG_DRAWIO_GUIDE.md)** - SVG and draw.io guide
- **[TEST_RESULTS.md](howto/TEST_RESULTS.md)** - Test results

---

## 🛠️ Supported Services

**Azure Services**: App Service, Azure Functions, VM, AKS, Container Instances, SQL Database, Cosmos DB, MySQL, PostgreSQL, Redis Cache, Blob Storage, Data Lake, VNet, Application Gateway, Load Balancer, Firewall, Key Vault, API Management, Service Bus, Event Hub, Event Grid, Synapse Analytics, Data Factory, Stream Analytics, Azure Monitor, Application Insights, ML Workspace, Cognitive Services, IoT Hub

**Integrations**: GitHub, Confluence, MCP Servers, Generic Servers

---

## 🔧 AI Providers

| Provider | Cost | Speed | Free Tier |
|----------|------|-------|-----------|
| **Google Gemini**  | $0.0001/req |  Fast |  60/min |
| **OpenAI GPT-3.5** | $0.002/req | Fast |  No |
| **OpenAI GPT-4** | $0.03/req |  Slow |  No |
| **Anthropic Claude** | $0.015/req |  Fast |  No |
| **Azure OpenAI** | Varies | Medium |  No |

---

## 📁 Project Structure

```
ArchitectureasService/
├── app.py                      # Flask web server
├── ai_parser.py                # AI-powered parser (multi-provider)
├── diagram_generator.py        # Diagram generation engine
├── nl_parser.py                # Keyword-based fallback parser
├── requirements.txt            # Python dependencies
├── .env.example                # Configuration template
├── templates/                  # HTML templates
├── static/                     # CSS, JS, assets
├── output/                     # Generated diagrams
└── howto/                      # Documentation
    ├── SETUP_GUIDE.md          # Setup instructions
    ├── ARCHITECTURE_EXPLAINED.md
    ├── AI_IMPLEMENTATION_TEST_RESULTS.md
    └── ... (more guides)
```

---

##  Example Prompts

**Simple Web App**:
```
Create a web application with database and caching
```

**CI/CD Pipeline**:
```
CI/CD pipeline with GitHub, Azure Container Registry, and AKS deployment
```

**IoT Platform**:
```
IoT data processing platform with device connectivity and real-time analytics
```

**Microservices**:
```
Microservices e-commerce platform with API Gateway, event-driven messaging, and separate databases per service
```

---

##  Troubleshooting

**GraphViz not found?**
```bash
brew install graphviz  # macOS
sudo apt-get install graphviz  # Linux
```

**AI parser not working?**
- Check `.env` file exists
- Verify API key is set correctly
- Ensure `USE_AI_PARSER=true`

**Port 5001 in use?**
```bash
lsof -ti:5001 | xargs kill -9
```

**See [SETUP_GUIDE.md](howto/SETUP_GUIDE.md) for complete troubleshooting**

---

##  Performance

- **Simple** (5-10 components): ~2-3 seconds
- **Medium** (10-15 components): ~3-5 seconds
- **Complex** (20+ components): ~5-8 seconds

---

##  API Endpoints

```bash
# Generate diagram
POST /api/generate
{
  "description": "Your architecture description",
  "format": "png",
  "style": "default"
}

# Parse only (no diagram)
POST /api/parse
{
  "description": "Your architecture description"
}

# Get examples
GET /api/examples

# Health check
GET /api/health
```

---

##  License

MIT License - see main repository for details

---

##  Acknowledgments

- [Diagrams](https://diagrams.mingrammer.com/) - Python diagram library
- [GraphViz](https://graphviz.org/) - Graph visualization
- [graphviz2drawio](https://github.com/hbmartin/graphviz2drawio) - DOT to draw.io converter
- [Flask](https://flask.palletsprojects.com/) - Web framework
- AI Providers: Google Gemini, OpenAI, Anthropic, Azure OpenAI

---

**Made with ❤️ for the Azure community**

**For complete documentation, see [howto/](howto/) directory**
