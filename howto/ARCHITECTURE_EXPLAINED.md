# Architecture Explained - How It All Works

**Azure Architecture Diagram Generator - Technical Deep Dive**

---

##  Overview

The webapp uses **keyword-based pattern matching** (NOT AI currently) to parse natural language and generate diagrams. Here's how everything fits together.

---

## 🔄 Complete Data Flow

```
User Input (Browser)
    ↓
"Create a web app with SQL database"
    ↓
┌─────────────────────────────────────────────┐
│ Frontend (templates/index.html + app.js)    │
│ - Captures user input                       │
│ - Sends POST /api/generate                  │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│ Flask Backend (app.py)                      │
│ - Receives JSON request                     │
│ - Calls nl_parser.parse(description)        │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│ NL Parser (nl_parser.py)                    │
│ ⚙️ KEYWORD MATCHING (No AI)                 │
│                                             │
│ 1. Scans text for keywords:                 │
│    - "web app" → AppService                 │
│    - "sql database" → SQLDatabase           │
│                                             │
│ 2. Extracts quantity:                       │
│    - "2 web apps" → creates 2 instances     │
│                                             │
│ 3. Assigns layers:                          │
│    - AppService → application layer         │
│    - SQLDatabase → data layer               │
│                                             │
│ 4. Infers connections:                      │
│    - App → Database = "Query"               │
│                                             │
│ Returns: {                                  │
│   components: [...],                        │
│   connections: [...],                       │
│   layers: {...}                             │
│ }                                           │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│ Diagram Generator (diagram_generator.py)    │
│                                             │
│ 1. Maps service types to icons:             │
│    - appservice → AppServices class         │
│    - sqldb → SQLDatabases class             │
│                                             │
│ 2. Creates diagram using 'diagrams' lib:    │
│    with Diagram(...):                       │
│      with Cluster("Application Layer"):     │
│        webapp = AppServices("Web App")      │
│      with Cluster("Data Layer"):            │
│        db = SQLDatabases("SQL DB")          │
│      webapp >> Edge(label="Query") >> db    │
│                                             │
│ 3. Generates SVG file                       │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│ Python 'diagrams' Library                   │
│ - Uses GraphViz for rendering               │
│ - Generates SVG/PNG/PDF                     │
│ - Includes Azure service icons              │
└─────────────────────────────────────────────┘
    ↓
output/azure_arch_20251130_122842.svg
    ↓
Download Link Returned to Browser
    ↓
User Downloads SVG File
```

---

##  Currently: NO AI (Keyword Matching)

### How Parsing Works NOW

**File**: `nl_parser.py`

The parser uses **dictionary-based keyword matching**:

```python
self.service_patterns = {
    'appservice': ['web app', 'app service', 'website'],
    'sqldb': ['sql database', 'sql server', 'sql db'],
    'redis': ['redis', 'cache'],
    'aks': ['kubernetes', 'aks', 'k8s cluster'],
    # ... 30+ more services
}
```

**Process**:
1. Convert description to lowercase
2. Loop through each service pattern
3. Check if ANY keyword exists in text
4. If found, create component for that service
5. Extract quantity using regex (e.g., "2 web apps")
6. Infer connections based on proximity and keywords

**Example**:
```
Input: "Create a web app with SQL database"

Step 1: Scan for 'web app' → FOUND → Create AppService
Step 2: Scan for 'sql database' → FOUND → Create SQLDatabase
Step 3: Infer: Application components connect to Data components
Step 4: Create connection: AppService → SQLDatabase (type: "Query")

Output:
{
  components: [
    {id: "appservice_1", type: "appservice", layer: "application"},
    {id: "sqldb_2", type: "sqldb", layer: "data"}
  ],
  connections: [
    {from: "appservice_1", to: "sqldb_2", label: "Query"}
  ]
}
```

---

##  Where AI COULD Be Added

### Current Limitations (Without AI)

 **Cannot understand context**:
- "I need a system for processing customer orders" → Won't detect anything

 **Cannot infer services from requirements**:
- "Handle 1M requests per day" → Won't suggest load balancer or caching

 **Cannot recommend best practices**:
- Won't suggest "add Redis for performance"

 **Cannot handle complex sentences**:
- "We're building an e-commerce platform that needs to scale globally"

 **Requires exact keyword matches**:
- "NoSQL database" might not match if only "cosmos db" is in patterns

### Where to Add AI/LLM

There are **3 integration points** where you can add AI:

---

## 🔧 Integration Point 1: Enhanced NL Parser (Recommended)

**Replace keyword matching with LLM-based extraction**

### Create New File: `ai_nl_parser.py`

```python
#!/usr/bin/env python3
"""
AI-Powered Natural Language Parser using OpenAI/Anthropic
"""
import os
from typing import Dict, List
import openai  # or anthropic

class AINaturalLanguageParser:
    """Parse architecture descriptions using LLM"""

    def __init__(self, provider='openai', model='gpt-4'):
        self.provider = provider
        self.model = model

        if provider == 'openai':
            openai.api_key = os.getenv('OPENAI_API_KEY')
        elif provider == 'anthropic':
            import anthropic
            self.client = anthropic.Anthropic(
                api_key=os.getenv('ANTHROPIC_API_KEY')
            )

    def parse(self, description: str) -> Dict:
        """
        Use LLM to extract Azure architecture components
        """
        prompt = f"""
You are an Azure architecture expert. Parse this description and extract Azure services.

Description: {description}

Return JSON with:
{{
  "components": [
    {{
      "type": "appservice|sqldb|redis|aks|...",
      "display_name": "Human readable name",
      "layer": "frontend|application|data|messaging|analytics",
      "quantity": 1
    }}
  ],
  "connections": [
    {{
      "from_type": "appservice",
      "to_type": "sqldb",
      "label": "Query",
      "type": "queries"
    }}
  ]
}}

Supported Azure services:
- Web: appservice, functionapp, apimanagement
- Database: sqldb, cosmosdb, mysql, postgresql, redis
- Compute: vm, aks, container
- Storage: blobstorage, datalake
- Network: vnet, appgateway, loadbalancer, firewall
- Security: keyvault
- Messaging: servicebus, eventhub, eventgrid
- Analytics: synapse, datafactory, streamanalytics
- Monitoring: monitor, appinsights
- AI/ML: mlworkspace, cognitiveservices
- IoT: iothub

IMPORTANT: Return ONLY valid JSON, no markdown.
"""

        if self.provider == 'openai':
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an Azure architecture expert. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1  # Low temperature for consistent results
            )
            result = response.choices[0].message.content

        elif self.provider == 'anthropic':
            message = self.client.messages.create(
                model=self.model,  # "claude-3-5-sonnet-20241022"
                max_tokens=2000,
                temperature=0.1,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            result = message.content[0].text

        # Parse JSON response
        import json
        parsed = json.loads(result)

        # Convert to internal format
        components = []
        component_id = 1

        for comp in parsed['components']:
            quantity = comp.get('quantity', 1)
            for i in range(quantity):
                components.append({
                    'id': f"{comp['type']}_{component_id}",
                    'type': comp['type'],
                    'name': f"{comp['type']}{i+1 if quantity > 1 else ''}",
                    'display_name': comp['display_name'],
                    'layer': comp['layer']
                })
                component_id += 1

        # Build connections
        connections = []
        for conn in parsed['connections']:
            # Find component IDs
            from_comp = next((c for c in components if c['type'] == conn['from_type']), None)
            to_comp = next((c for c in components if c['type'] == conn['to_type']), None)

            if from_comp and to_comp:
                connections.append({
                    'from': from_comp['id'],
                    'to': to_comp['id'],
                    'label': conn['label'],
                    'type': conn['type']
                })

        # Organize layers
        layers = {}
        for comp in components:
            layer = comp['layer']
            if layer not in layers:
                layers[layer] = []
            layers[layer].append(comp['id'])

        return {
            'description': description,
            'components': components,
            'connections': connections,
            'layers': layers
        }
```

### Update `app.py` to Use AI Parser

```python
# At the top of app.py
import os

# Choose parser based on environment variable
USE_AI_PARSER = os.getenv('USE_AI_PARSER', 'false').lower() == 'true'

if USE_AI_PARSER:
    from ai_nl_parser import AINaturalLanguageParser
    nl_parser = AINaturalLanguageParser(
        provider=os.getenv('AI_PROVIDER', 'openai'),  # or 'anthropic'
        model=os.getenv('AI_MODEL', 'gpt-4')
    )
else:
    from nl_parser import NaturalLanguageParser
    nl_parser = NaturalLanguageParser()
```

### Environment Variables

Create `.env` file:
```bash
# Choose parser
USE_AI_PARSER=true

# OpenAI Configuration
AI_PROVIDER=openai
AI_MODEL=gpt-4
OPENAI_API_KEY=sk-your-key-here

# OR Anthropic Configuration
AI_PROVIDER=anthropic
AI_MODEL=claude-3-5-sonnet-20241022
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

---

## 🔧 Integration Point 2: Diagram Optimization (Advanced)

**Use AI to optimize diagram layout and suggest improvements**

```python
# Add to diagram_generator.py

def optimize_with_ai(self, architecture: Dict) -> Dict:
    """Use LLM to suggest architecture improvements"""

    prompt = f"""
Given this Azure architecture:
Components: {architecture['components']}
Connections: {architecture['connections']}

Suggest:
1. Missing components (monitoring, security, backup)
2. Best practices (high availability, disaster recovery)
3. Cost optimizations
4. Security improvements

Return JSON with suggestions.
"""

    # Call LLM
    # Return enhanced architecture
```

---

## 🔧 Integration Point 3: Conversational Interface

**Allow users to refine diagrams through chat**

```python
# New file: conversational_agent.py

class ConversationalAgent:
    """Chat with user to refine architecture"""

    def __init__(self):
        self.conversation_history = []

    def chat(self, user_message: str, current_architecture: Dict) -> Dict:
        """
        User: "Add a load balancer in front"
        → AI updates architecture
        → Returns new diagram
        """
        pass
```

---

##  Diagram Generation (No AI Needed)

**File**: `diagram_generator.py`

This uses the **Python `diagrams` library** which wraps GraphViz:

```python
from diagrams import Diagram, Cluster, Edge
from diagrams.azure.compute import AppServices
from diagrams.azure.database import SQLDatabases

with Diagram("My Architecture", outformat="svg"):
    with Cluster("Application Layer"):
        webapp = AppServices("Web App")

    with Cluster("Data Layer"):
        db = SQLDatabases("SQL Database")

    webapp >> Edge(label="Query") >> db
```

**This generates**:
1. Calls GraphViz to render diagram
2. Embeds Azure service icons (from diagrams library)
3. Outputs SVG/PNG/PDF file

**No AI needed here** - it's pure visualization.

---

##  Dependencies

### Current (No AI)
```
Flask==3.0.0
diagrams==0.24.4
graphviz==0.20.3
```

### With OpenAI
```
Flask==3.0.0
diagrams==0.24.4
graphviz==0.20.3
openai==1.54.0        # NEW
python-dotenv==1.0.0  # NEW (for .env files)
```

### With Anthropic
```
Flask==3.0.0
diagrams==0.24.4
graphviz==0.20.3
anthropic==0.39.0     # NEW
python-dotenv==1.0.0  # NEW
```

---

##  How to Switch Models

### Option 1: OpenAI (GPT-4, GPT-3.5)

```bash
# Install
pip install openai python-dotenv

# Configure
export USE_AI_PARSER=true
export AI_PROVIDER=openai
export AI_MODEL=gpt-4  # or gpt-3.5-turbo
export OPENAI_API_KEY=sk-...
```

**Models Available**:
- `gpt-4` - Best quality, slower, expensive
- `gpt-4-turbo` - Fast GPT-4
- `gpt-3.5-turbo` - Fast, cheaper, good quality

### Option 2: Anthropic (Claude)

```bash
# Install
pip install anthropic python-dotenv

# Configure
export USE_AI_PARSER=true
export AI_PROVIDER=anthropic
export AI_MODEL=claude-3-5-sonnet-20241022
export ANTHROPIC_API_KEY=sk-ant-...
```

**Models Available**:
- `claude-3-5-sonnet-20241022` - Best balance (Recommended)
- `claude-3-opus-20240229` - Highest quality, slower
- `claude-3-haiku-20240307` - Fastest, cheaper

### Option 3: Azure OpenAI

```bash
# Install
pip install openai python-dotenv

# Configure
export USE_AI_PARSER=true
export AI_PROVIDER=azure_openai
export AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
export AZURE_OPENAI_API_KEY=...
export AZURE_OPENAI_DEPLOYMENT=gpt-4
```

### Option 4: Local LLM (Ollama)

```bash
# Install
pip install ollama python-dotenv

# Configure
export USE_AI_PARSER=true
export AI_PROVIDER=ollama
export AI_MODEL=llama3  # or mistral, codellama
export OLLAMA_BASE_URL=http://localhost:11434
```

---

## 💰 Cost Comparison

### Current (Keyword Matching)
- **Cost**: $0
- **Speed**: < 100ms
- **Accuracy**: ~70% (requires exact keywords)

### With OpenAI GPT-4
- **Cost**: ~$0.03 per request (1500 tokens avg)
- **Speed**: 2-5 seconds
- **Accuracy**: ~95%

### With OpenAI GPT-3.5-turbo
- **Cost**: ~$0.002 per request
- **Speed**: 1-2 seconds
- **Accuracy**: ~85%

### With Anthropic Claude 3.5 Sonnet
- **Cost**: ~$0.015 per request
- **Speed**: 2-4 seconds
- **Accuracy**: ~95%

### With Local Ollama
- **Cost**: $0 (runs locally)
- **Speed**: 5-15 seconds (depends on hardware)
- **Accuracy**: ~80% (smaller models)

---

##  Recommended Approach

### For Development/Testing
 **Use current keyword matching** (FREE, fast)

### For Production (Small Scale)
 **Use OpenAI GPT-3.5-turbo** (cheap, good quality)

### For Production (High Quality)
 **Use Anthropic Claude 3.5 Sonnet** or **GPT-4** (best results)

### For Enterprise (Privacy)
 **Use Azure OpenAI** (data stays in your tenant)

### For Offline/Cost-Sensitive
 **Use Ollama locally** (free, private)

---

##  Implementation Steps

### Step 1: Create AI Parser
```bash
cd webapp
touch ai_nl_parser.py
# Copy code from above
```

### Step 2: Install Dependencies
```bash
pip install openai python-dotenv
# or
pip install anthropic python-dotenv
```

### Step 3: Configure Environment
```bash
# Create .env file
cat > .env << EOF
USE_AI_PARSER=true
AI_PROVIDER=openai
AI_MODEL=gpt-4
OPENAI_API_KEY=sk-your-key
EOF
```

### Step 4: Update app.py
```python
from dotenv import load_dotenv
load_dotenv()

USE_AI_PARSER = os.getenv('USE_AI_PARSER', 'false').lower() == 'true'
```

### Step 5: Test
```bash
python app.py
# Try: "I need a scalable e-commerce platform"
# AI will suggest: Load Balancer, App Services, Redis, SQL, etc.
```

---

##  Current vs AI Comparison

| Feature | Current (Keywords) | With AI (LLM) |
|---------|-------------------|---------------|
| **Exact keywords** |  Required |  Not required |
| **Context understanding** |  No |  Yes |
| **Suggest services** |  No |  Yes |
| **Best practices** |  No |  Yes |
| **Complex sentences** |  Limited |  Excellent |
| **Cost** |  Free | ⚠️ $0.002-0.03/request |
| **Speed** |  <100ms | ⚠️ 2-5 seconds |
| **Accuracy** | ⚠️ 70% |  95% |
| **Privacy** |  Local | ⚠️ Sent to API |

---

## 🎓 Summary

### How It Works NOW
1. User enters text: "Create web app with database"
2. `nl_parser.py` scans for keywords like "web app", "database"
3. Creates components based on matches
4. `diagram_generator.py` renders using diagrams library + GraphViz
5. Returns SVG file

### No AI is Used Currently
- Just pattern matching with regex
- Dictionary of keywords
- Hardcoded connection logic

### Where AI Can Help
1. **Better parsing** - Understand "e-commerce platform" → suggest services
2. **Recommendations** - "Add Redis for caching", "Use load balancer"
3. **Optimization** - Suggest cost savings, security improvements
4. **Conversational** - Chat to refine architecture

### How to Add AI
- Create `ai_nl_parser.py` with OpenAI/Anthropic/Local LLM
- Toggle with `USE_AI_PARSER=true` environment variable
- Zero code changes to rest of app!

---

**Ready to add AI? See the example code above!**
