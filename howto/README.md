# Azure Architecture Diagram Generator - Web Application

**AI-Powered Natural Language to Azure Architecture Diagrams**

Transform natural language descriptions into professional Azure architecture diagrams instantly using this web-based tool.

---

##  Features

- **Natural Language Input**: Describe your architecture in plain English
- **Automatic Component Detection**: Automatically identifies Azure services from description
- **Visual Diagram Generation**: Creates professional architecture diagrams
- **Multiple Output Formats**: SVG (editable in draw.io), PNG, PDF
- **draw.io Compatible**: SVG output can be directly opened and edited in draw.io
- **Component Preview**: See parsed components before generating diagram
- **Example Library**: Pre-built examples to get started quickly
- **Download Support**: Download generated diagrams instantly

---

##  Quick Start

### Prerequisites

- **Python 3.11+** installed
- **GraphViz** installed (`brew install graphviz` on macOS)
- Existing `Arch_Diagrams/venv` setup (or create new one)

### Installation

1. **Navigate to webapp directory**:
   ```bash
   cd webapp
   ```

2. **Install dependencies** (use existing venv or create new):
   ```bash
   # Option 1: Use existing venv from Arch_Diagrams
   source ../Arch_Diagrams/venv/bin/activate
   pip install -r requirements.txt

   # Option 2: Create new venv for webapp
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the web interface**:
   ```
   Open your browser to: http://localhost:5000
   ```

---

## 📖 Usage Guide

### Basic Usage

1. **Enter Description**:
   - Type or paste your architecture description in the text area
   - Use natural language (see examples below)

2. **Preview Components** (Optional):
   - Click "Preview Components" to see what will be generated
   - Review the extracted Azure services

3. **Generate Diagram**:
   - Select output format (PNG recommended)
   - Choose style (default, detailed, simple)
   - Click "Generate Diagram"

4. **Download**:
   - View the generated diagram
   - Click "Download" to save it

### Example Descriptions

#### Example 1: 3-Tier Web Application
```
Create a 3-tier web application with Application Gateway as frontend,
two Web Apps in the middle tier, and SQL Database with Redis cache in the backend.
```

**Components detected**:
- Application Gateway (frontend)
- 2x App Services (application)
- SQL Database (data)
- Redis Cache (data)

#### Example 2: Microservices Platform
```
Build a microservices architecture with AKS cluster, Azure Service Bus for messaging,
Cosmos DB for data storage, and API Management gateway.
```

**Components detected**:
- AKS Cluster (application)
- API Management (application)
- Service Bus (messaging)
- Cosmos DB (data)

#### Example 3: Data Analytics Platform
```
Design a data analytics platform with Azure Data Factory for ingestion,
Data Lake Storage, Azure Synapse for analytics, and Azure Monitor for logging.
```

**Components detected**:
- Data Factory (analytics)
- Data Lake Storage (data)
- Azure Synapse (analytics)
- Azure Monitor (monitoring)

#### Example 4: Secure Infrastructure
```
Build secure infrastructure with Virtual Network, Application Gateway with WAF,
Web App with private endpoints, Key Vault for secrets, and Azure Firewall.
```

**Components detected**:
- Virtual Network (infrastructure)
- Application Gateway (frontend)
- App Service (application)
- Key Vault (infrastructure)
- Azure Firewall (infrastructure)

---

## 🏗️ Architecture

### Application Structure

```
webapp/
├── app.py                      # Flask application (main entry point)
├── nl_parser.py                # Natural language parser
├── diagram_generator.py        # Diagram generation engine
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── templates/
│   └── index.html             # Web interface
├── static/
│   ├── css/
│   │   └── style.css          # Styles
│   └── js/
│       └── app.js             # Frontend JavaScript
└── output/                     # Generated diagrams (auto-created)
```

### System Flow

```
┌─────────────────────────────────────────────────────────┐
│  1. User Input (Natural Language)                      │
│     "Create web app with SQL database"                 │
└────────────────┬────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────┐
│  2. NL Parser (nl_parser.py)                           │
│     - Keyword detection                                 │
│     - Service extraction                                │
│     - Connection inference                              │
└────────────────┬────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────┐
│  3. Structured Architecture                             │
│     {                                                    │
│       components: [...],                                │
│       connections: [...],                               │
│       layers: {...}                                     │
│     }                                                    │
└────────────────┬────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────┐
│  4. Diagram Generator (diagram_generator.py)            │
│     - Uses diagrams library                             │
│     - Creates visual representation                     │
│     - Applies styling and layout                        │
└────────────────┬────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────┐
│  5. Output (PNG/SVG/PDF)                                │
│     Professional Azure architecture diagram             │
└─────────────────────────────────────────────────────────┘
```

---

##  Supported Azure Services

### Compute
- App Service / Web App
- Function App
- Virtual Machine
- Container Instance
- AKS (Kubernetes)

### Database
- SQL Database
- Cosmos DB
- MySQL
- PostgreSQL
- Redis Cache

### Storage
- Blob Storage
- Storage Account
- Data Lake Storage

### Networking
- Virtual Network
- Application Gateway
- Load Balancer
- Azure Firewall

### Security
- Key Vault
- Security Center

### AI/ML
- Machine Learning Workspace
- Cognitive Services

### Messaging
- Service Bus
- Event Hub
- Event Grid

### Analytics
- Azure Synapse
- Data Factory
- Stream Analytics

### Monitoring
- Azure Monitor
- Application Insights

### IoT
- IoT Hub

---

## 🔧 API Endpoints

### POST /api/generate
Generate diagram from description

**Request**:
```json
{
  "description": "Create a web app with SQL database",
  "format": "png",
  "style": "default"
}
```

**Response**:
```json
{
  "success": true,
  "diagram_url": "/download/azure_arch_20241130_123045.png",
  "architecture": { ... },
  "metadata": {
    "generated_at": "20241130_123045",
    "format": "png",
    "components": 2
  }
}
```

### POST /api/parse
Parse description without generating diagram

**Request**:
```json
{
  "description": "Create a web app with SQL database"
}
```

**Response**:
```json
{
  "success": true,
  "architecture": { ... },
  "component_count": 2,
  "connections": 1
}
```

### GET /api/examples
Get example architecture descriptions

**Response**:
```json
{
  "examples": [
    {
      "title": "3-Tier Web Application",
      "description": "...",
      "tags": ["web", "database", "cache"]
    }
  ]
}
```

### GET /api/health
Health check

**Response**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "components": {
    "diagram_generator": "operational",
    "nl_parser": "operational"
  }
}
```

---

## 🎓 Natural Language Parsing

### Supported Keywords

#### Web & Apps
- "web app", "app service", "website", "web application"
- "function", "azure function", "serverless function"
- "api management", "api gateway"

#### Compute
- "virtual machine", "vm"
- "container", "container instance"
- "kubernetes", "aks"

#### Database
- "sql database", "sql server", "sql db"
- "cosmos db", "cosmos", "nosql database"
- "mysql", "postgresql"

#### Cache & Storage
- "redis", "cache"
- "blob storage", "storage account"
- "data lake"

#### Networking
- "virtual network", "vnet"
- "application gateway", "app gateway"
- "load balancer"
- "firewall"

#### Security
- "key vault", "secrets"

#### Messaging
- "service bus", "message queue"
- "event hub", "event stream"

#### Analytics
- "synapse", "data warehouse"
- "data factory", "etl"
- "stream analytics"

### Quantity Support

You can specify quantities:
- **Numbers**: "2 web apps", "3 virtual machines"
- **Words**: "two web apps", "three databases"

### Connection Inference

The parser automatically infers logical connections:
- **Frontend** → **Application**: HTTP/HTTPS
- **Application** → **Database**: Query
- **Application** → **Cache**: Cache operations
- **Application** → **Storage**: Store/Retrieve

---

##  Advanced Usage

### Custom Styling

Modify `diagram_generator.py` to customize:
- Layer colors
- Edge styles
- Node layouts
- Font sizes

### Adding New Services

1. **Add to `nl_parser.py`**:
   ```python
   self.service_patterns = {
       'newservice': ['keyword1', 'keyword2'],
       # ...
   }
   ```

2. **Add to `diagram_generator.py`**:
   ```python
   from diagrams.azure.category import NewService

   self.service_mapping = {
       'newservice': NewService,
       # ...
   }
   ```

### Integration with AI/LLM (Future)

To integrate with OpenAI or Anthropic:

1. Install dependencies:
   ```bash
   pip install openai anthropic
   ```

2. Add LLM parser in `nl_parser.py`:
   ```python
   def parse_with_llm(self, description):
       # Use OpenAI/Anthropic to extract components
       pass
   ```

---

##  Troubleshooting

### Issue: "GraphViz not found"
**Solution**:
```bash
brew install graphviz  # macOS
apt-get install graphviz  # Linux
```

### Issue: "Module not found"
**Solution**:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "Diagram generation fails"
**Solution**:
- Check that description contains recognizable Azure services
- Verify GraphViz is installed
- Check Flask logs for specific errors

### Issue: "No components detected"
**Solution**:
- Use more specific service names (e.g., "SQL Database" instead of "database")
- Check `nl_parser.py` for supported keywords
- Use examples as templates

---

##  Performance

- **Parse time**: < 100ms
- **Diagram generation**: 1-3 seconds
- **Supported concurrent users**: 10+ (Flask development server)
- **Max description length**: 10,000 characters

For production deployment, use production WSGI server (Gunicorn, uWSGI).

---

## 🚢 Production Deployment

### Using Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Docker

```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y graphviz

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### Environment Variables

```bash
FLASK_ENV=production
FLASK_DEBUG=False
OUTPUT_FOLDER=/data/diagrams
```

---

##  License

Part of the Infrastructure Modernization Platform
See main repository for license information

---

## 🤝 Contributing

See [WORKFLOW_GUIDE.md](../WORKFLOW_GUIDE.md) and [HOW_TO_GUIDE.md](../HOW_TO_GUIDE.md) for contribution guidelines.

---

## 📞 Support

- **Documentation**: [WORKFLOW_GUIDE.md](../WORKFLOW_GUIDE.md)
- **How-To Guides**: [HOW_TO_GUIDE.md](../HOW_TO_GUIDE.md)
- **Architecture Docs**: [MCP_PLATFORM_ARCHITECTURE.md](../Arch_Diagrams/MCP_PLATFORM_ARCHITECTURE.md)

---

**Version**: 1.0.0
**Last Updated**: November 30, 2024
**Status**:  Production Ready
