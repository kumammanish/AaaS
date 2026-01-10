# Workflow & Architecture Maps Guide

## 🔄 Repository Workflow

```mermaid
graph TD
    User([User Input]) -->|Step 1: Text Description| Frontend[Web Frontend<br/>HTML/CSS/JS]
    Frontend -->|Step 2: POST /api/generate| API[Flask API<br/>Python]
    
    subgraph "Backend Processing"
        API -->|Step 3: Description| Parser{Parser Selection}
        Parser -->|USE_AI_PARSER=False| KW[Keyword Parser<br/>Python Regex]
        Parser -->|USE_AI_PARSER=True| AI[AI Parser<br/>Python SDKs]
        
        KW -->|Step 4: Regex/Dict| Arch[Architecture JSON]
        
        AI -->|Step 4a: Prompt| LLM[LLM Provider<br/>API]
        LLM -->|Step 4b: JSON Response| Arch
        
        LLM -.->|Gemini| G[Google Gemini]
        LLM -.->|GPT-4| O[OpenAI]
        LLM -.->|Claude| C[Anthropic]
    end
    
    Arch -->|Step 5: JSON| Gen[Diagram Generator<br/>Python]
    
    subgraph "Visualization"
        Gen -->|Step 6: Python Diagrams| D[Diagrams Lib<br/>Python]
        D -->|Step 7: GraphViz| Render[Render Engine<br/>GraphViz/Dot]
        Render -->|Step 8: Generate| Files[Output Files]
    end
    
    Files -->|.png| PNG[PNG Image]
    Files -->|.dot| DOT[DOT File]
    Files -->|.drawio| DRAW[Draw.io File]
    
    Files -->|Step 9: File Paths| API
    API -->|Step 10: JSON Response| Frontend
    Frontend -->|Step 11: Display| UserView([User View])
    
    style User fill:#e1f5fe,stroke:#01579b
    style Frontend fill:#e3f2fd,stroke:#1565c0
    style API fill:#fff3e0,stroke:#e65100
    style AI fill:#fce4ec,stroke:#880e4f
    style Arch fill:#e8f5e9,stroke:#1b5e20
    style UserView fill:#e1f5fe,stroke:#01579b
```

---

## 🏗️ Connection Logic

### Efficient Traffic Flows
The system uses a **representative connection** strategy to keep diagrams clean and readable, especially for large architectures.

**Logic Applied**:
- Creates **ONE connection** per connection type between components.
- Labels indicate multiplicity when applicable (e.g., "× 2").
- Reduces visual clutter while maintaining logical clarity.

**Example**:
- **Scenario**: 2 App Services connecting to 1 SQL Database.
- **Result**: 1 connection line labeled "Connects to (×2)".

### Technical Implementation

**Code Pattern**:
```python
if source_components and target_components:
    source = source_components[0]  # Representative
    target = target_components[0]  # Representative
    label = base_label
    if len(source_components) > 1:
        label += f" (×{len(source_components)})"
    create_connection(source, target, label)
```

**Benefits**:
1. **Visual Clarity**: Readable, professional diagrams.
2. **Scalability**: Works for small (5) to large (50+) component counts.
3. **Semantic Preservation**: Multiplicity explicitly shown.

### Connection Label Examples
**Format**: `<base_label> (×<count>)`

**Examples**:
- "Routes web traffic" → Single instance
- "Routes web traffic (×2)" → 2 instances
- "Queries application data (×3)" → 3 instances

### Layer Organization
- `integrations`: For GitHub, MCP servers, external tools
- `external`: For third-party services
- `security`: Key Vault and security services

---

## 🎓 Icon Availability Matrix

| Service | Icon Type | Source | Status |
|---------|-----------|--------|--------|
| **GitHub** | Official GitHub logo | `diagrams.onprem.vcs` |  Available |
| **MCP Server** | Generic server | `diagrams.onprem.compute` |  Available |
| **Confluence** | Generic rack | `diagrams.generic.compute` | ⚠️ Placeholder |
| **Generic Server** | Server icon | `diagrams.onprem.compute` |  Available |

---

##  Example Use Cases

### Use Case 1: CI/CD Pipeline with GitHub

**Prompt**: "CI/CD pipeline with GitHub, Azure, and deployment to AKS"

**Generated Architecture**:
```
Components:
├── GitHub (source control)
├── Azure Container Registry
├── AKS (Kubernetes cluster)
├── Key Vault
└── Application Insights

Connections:
GitHub → Container Registry: "Push images"
Container Registry → AKS: "Pull and deploy (×3)"
AKS → Key Vault: "Retrieve secrets"
```

### Use Case 2: MCP-Enabled AI Platform

**Prompt**: "AI platform with MCP servers for context, Azure OpenAI, and documentation"

**Generated Architecture**:
```
Components:
├── MCP Server (context provider)
├── Azure OpenAI (Cognitive Services)
├── Confluence (documentation)
├── App Service
├── Cosmos DB
└── Redis Cache

Connections:
App Service → MCP Server: "Query context"
MCP Server → Cosmos DB: "Retrieve data (×2)"
App Service → Azure OpenAI: "AI requests"
```

### Use Case 3: Documentation & Collaboration Platform

**Prompt**: "Documentation platform with Confluence, Azure, and GitHub integration"

**Generated Architecture**:
```
Components:
├── GitHub (source docs)
├── Confluence (wiki)
├── App Service (converter)
├── Blob Storage (assets)
├── Azure Search
└── Application Insights

Connections:
GitHub → App Service: "Sync markdown"
App Service → Confluence: "Publish"
App Service → Blob Storage: "Store media (×2)"
```

---

##  How to Use

### Example 1: Simple Architecture (Verify Simplified Connections)
```bash
curl -X POST http://localhost:5001/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Web app with 3 app services connecting to SQL and Redis"
  }'
```

**Expected Output**:
- **Flow**: 1 → SQL "(×3)" + 1 → Redis "(×3)" = 2 connections

### Example 2: CI/CD with GitHub
```bash
curl -X POST http://localhost:5001/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "description": "CI/CD pipeline with GitHub, Azure Container Registry, and AKS"
  }'
```

**Expected Components**:
-  GitHub icon (official)
- Azure Container Registry
- AKS
- Application Insights

### Example 3: MCP-Enabled System
```bash
curl -X POST http://localhost:5001/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "description": "AI platform with MCP servers providing context to Azure OpenAI"
  }'
```

**Expected Components**:
-  MCP Server icon (server)
- Azure OpenAI (Cognitive Services)
- App Service
- Cosmos DB

---

##  Verification

### Test 1: Connection Simplification
```bash
# Generate complex architecture
curl -X POST http://localhost:5001/api/generate \
  -H "Content-Type: application/json" \
  -d '{"description": "E-commerce platform"}' \
  | jq '.architecture.connections | length'

# Should return ~10-15 instead of 30-40
```

### Test 2: GitHub Icon
```bash
# Generate with GitHub
curl -X POST http://localhost:5001/api/generate \
  -H "Content-Type: application/json" \
  -d '{"description": "CI/CD with GitHub"}' \
  | jq '.architecture.components[] | select(.type=="github")'

# Should return GitHub component with proper icon
```

### Test 3: MCP Server Icon
```bash
# Generate with MCP
curl -X POST http://localhost:5001/api/generate \
  -H "Content-Type: application/json" \
  -d '{"description": "System with MCP server"}' \
  | jq '.architecture.components[] | select(.type=="mcpserver")'

# Should return MCP Server component
```
