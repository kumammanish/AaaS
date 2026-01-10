#!/usr/bin/env python3
"""
AI-Powered Natural Language Parser with Multi-Provider Support
Supports: OpenAI, Anthropic, Google Gemini, Azure OpenAI
With optional Azure MCP integration for best practices
"""
import os
import json
import re
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AIParser:
    """
    Multi-provider AI parser for Azure architecture descriptions

    Providers:
    - gemini: Google Gemini (recommended - cheap & fast)
    - openai: OpenAI GPT models
    - anthropic: Anthropic Claude models
    - azure_openai: Azure OpenAI Service
    """

    def __init__(self):
        self.provider = os.getenv('AI_PROVIDER', 'gemini').lower()
        self.use_mcp = os.getenv('USE_MCP', 'false').lower() == 'true'
        
        # Failover priority: try providers in this order
        self.failover_providers = self._get_failover_providers()
        self.current_provider_index = 0

        print(f" Initializing AI Parser: {self.provider}")
        if len(self.failover_providers) > 1:
            print(f" Failover enabled: {' → '.join(self.failover_providers)}")
        if self.use_mcp:
            print(f" MCP enabled for Azure knowledge")

        self.setup_ai_client()

        # Azure service type mappings
        self.service_types = self._get_service_types()

    def _get_failover_providers(self) -> List[str]:
        """Get list of available providers for failover"""
        providers = []
        
        # Start with primary provider
        providers.append(self.provider)
        
        # Add other providers that have API keys configured
        if self.provider != 'gemini' and os.getenv('GOOGLE_API_KEY'):
            providers.append('gemini')
        if self.provider != 'openai' and os.getenv('OPENAI_API_KEY'):
            providers.append('openai')
        if self.provider != 'anthropic' and os.getenv('ANTHROPIC_API_KEY'):
            providers.append('anthropic')
        if self.provider != 'azure_openai' and os.getenv('AZURE_OPENAI_ENDPOINT') and os.getenv('AZURE_OPENAI_API_KEY'):
            providers.append('azure_openai')
        
        return providers

    def setup_ai_client(self, provider: str = None):
        """Initialize AI client based on provider"""
        if provider:
            self.provider = provider
            
        try:
            if self.provider == 'gemini':
                import google.generativeai as genai
                api_key = os.getenv('GOOGLE_API_KEY')
                if not api_key:
                    raise ValueError("GOOGLE_API_KEY not set in environment")
                genai.configure(api_key=api_key)
                model_name = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')
                self.model = genai.GenerativeModel(model_name)
                self.client = genai  # Store client for consistency
                print(f"✓ Gemini initialized: {model_name}")

            elif self.provider == 'openai':
                import openai
                api_key = os.getenv('OPENAI_API_KEY')
                if not api_key:
                    raise ValueError("OPENAI_API_KEY not set in environment")
                openai.api_key = api_key
                self.model_name = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
                self.client = openai
                print(f" OpenAI initialized: {self.model_name}")

            elif self.provider == 'anthropic':
                import anthropic
                api_key = os.getenv('ANTHROPIC_API_KEY')
                if not api_key:
                    raise ValueError("ANTHROPIC_API_KEY not set in environment")
                # Try initialization - handle version compatibility
                try:
                    self.client = anthropic.Anthropic(api_key=api_key)
                except TypeError as te:
                    # Older version might not accept certain parameters
                    if 'proxies' in str(te):
                        # Retry without any extra parameters
                        self.client = anthropic.Client(api_key=api_key)
                    else:
                        raise
                self.model_name = os.getenv('ANTHROPIC_MODEL', 'claude-3-5-sonnet-20241022')
                print(f"✓ Anthropic initialized: {self.model_name}")

            elif self.provider == 'azure_openai':
                import openai
                endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
                api_key = os.getenv('AZURE_OPENAI_API_KEY')
                if not endpoint or not api_key:
                    raise ValueError("AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY required")
                openai.api_type = "azure"
                openai.api_base = endpoint
                openai.api_key = api_key
                openai.api_version = os.getenv('AZURE_OPENAI_API_VERSION', '2024-02-15-preview')
                self.deployment_name = os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-4')
                self.client = openai
                print(f" Azure OpenAI initialized: {self.deployment_name}")

            else:
                raise ValueError(f"Unknown AI provider: {self.provider}")

        except Exception as e:
            print(f" Error initializing {self.provider}: {e}")
            raise

    def parse(self, description: str) -> Dict:
        """
        Main parsing method - converts natural language to architecture

        Args:
            description: Natural language architecture description

        Returns:
            Dictionary with components, connections, layers
        """
        try:
            print(f"\n Parsing with {self.provider}: {description[:100]}...")

            # Step 1: Generate architecture using AI
            architecture_json = self._call_ai(description)

            # Step 2: Parse and validate JSON
            architecture = self._parse_json_response(architecture_json)

            # Step 3: Convert to internal format
            result = self._convert_to_internal_format(architecture, description)

            print(f" Generated {len(result['components'])} components, {len(result['connections'])} connections")

            return result

        except Exception as e:
            print(f" AI parsing error: {e}")
            # Fallback to simple extraction
            return self._fallback_parse(description)

    def _call_ai(self, description: str) -> str:
        """Call AI provider with prompt and automatic failover"""

        prompt = self._build_prompt(description)
        last_error = None

        # Try each provider in failover list
        for attempt, provider in enumerate(self.failover_providers):
            try:
                # Switch to failover provider if needed
                if provider != self.provider:
                    print(f" Switching to failover provider: {provider}")
                    self.setup_ai_client(provider)

                if self.provider == 'gemini':
                    response = self.model.generate_content(prompt)
                    return response.text

                elif self.provider == 'openai':
                    response = self.client.ChatCompletion.create(
                        model=self.model_name,
                        messages=[
                            {"role": "system", "content": "You are an Azure Solutions Architect. Return only valid JSON."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.1,
                        max_tokens=3000
                    )
                    return response.choices[0].message.content

                elif self.provider == 'anthropic':
                    message = self.client.messages.create(
                        model=self.model_name,
                        max_tokens=3000,
                        temperature=0.1,
                        messages=[
                            {"role": "user", "content": prompt}
                        ]
                    )
                    return message.content[0].text

                elif self.provider == 'azure_openai':
                    response = self.client.ChatCompletion.create(
                        engine=self.deployment_name,
                        messages=[
                            {"role": "system", "content": "You are an Azure Solutions Architect. Return only valid JSON."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.1,
                        max_tokens=3000
                    )
                    return response.choices[0].message.content

            except Exception as e:
                last_error = e
                error_msg = str(e).lower()
                
                # Check if it's an auth/quota error
                if any(keyword in error_msg for keyword in ['auth', 'api key', 'quota', 'rate limit', 'expired', '401', '403', '429']):
                    print(f" {provider} failed (auth/quota): {e}")
                    if attempt < len(self.failover_providers) - 1:
                        print(f" Trying next provider...")
                        continue
                else:
                    # Non-auth error, don't failover
                    print(f" AI API call failed: {e}")
                    raise
        
        # All providers failed
        print(f" All {len(self.failover_providers)} providers failed")
        raise Exception(f"All AI providers exhausted. Last error: {last_error}")

    def _build_prompt(self, description: str) -> str:
        """Build AI prompt with Azure knowledge"""

        mcp_context = ""
        if self.use_mcp:
            mcp_context = """
AZURE BEST PRACTICES (from MCP):
- Use Application Gateway with WAF for web app security
- Implement Redis cache for session management and performance
- Use Key Vault for secrets and connection strings
- Enable Application Insights for monitoring
- For high availability, deploy multiple instances
- For global reach, use Traffic Manager or Front Door
- For e-commerce: separate read/write databases (SQL for writes, Cosmos for reads)
- For IoT: use Event Hub for high-throughput ingestion
- Always include monitoring and security components
"""

        prompt = f"""You are an Azure Solutions Architect. Parse this architecture description and generate Azure components.

USER REQUEST:
"{description}"

{mcp_context}

TASK:
Generate a complete Azure architecture with appropriate services. Return ONLY valid JSON in this format:

{{
  "components": [
    {{
      "type": "service_type",
      "display_name": "Human readable name",
      "layer": "frontend|application|data|messaging|analytics|infrastructure|security|monitoring",
      "quantity": 1,
      "reasoning": "Why this component"
    }}
  ],
  "connections": [
    {{
      "from_type": "source_service_type",
      "to_type": "target_service_type",
      "label": "Connection label",
      "type": "queries|routes_to|caches|stores|processes|monitors"
    }}
  ]
}}

AVAILABLE AZURE SERVICE TYPES:
{self._get_service_list()}

GUIDELINES:
1. Analyze the description for requirements (scale, security, global reach, etc.)
2. Suggest appropriate Azure services based on best practices
3. Include monitoring (appinsights) for production workloads
4. Include security (keyvault) for sensitive data
5. Add caching (redis) for performance when appropriate
6. Use proper layering (frontend → application → data)
7. Consider high availability (multiple instances, load balancers)
8. For e-commerce: include payment security, session management
9. For global systems: include CDN, Traffic Manager
10. For IoT: include Event Hub, Stream Analytics
11. For CI/CD pipelines: include github for source control
12. For documentation/collaboration: include confluence
13. For MCP-enabled systems: include mcpserver for context providers
14. Keep connections simple - avoid creating too many redundant connections

IMPORTANT:
- Return ONLY the JSON, no markdown formatting, no explanations
- Use service types from the available list
- Be specific with display names (e.g., "User Authentication Service" not just "App Service")
"""

        return prompt

    def _parse_json_response(self, response: str) -> Dict:
        """Parse JSON from AI response, handling markdown and errors"""
        try:
            # Remove markdown code blocks if present
            response = response.strip()
            response = re.sub(r'^```json\s*', '', response)
            response = re.sub(r'^```\s*', '', response)
            response = re.sub(r'\s*```$', '', response)
            response = response.strip()

            # Parse JSON
            return json.loads(response)

        except json.JSONDecodeError as e:
            print(f"⚠️ JSON parse error: {e}")
            print(f"Response: {response[:200]}...")
            # Try to extract JSON from response
            match = re.search(r'\{.*\}', response, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(0))
                except:
                    pass
            raise ValueError(f"Could not parse JSON from AI response")

    def _convert_to_internal_format(self, architecture: Dict, description: str) -> Dict:
        """Convert AI output to internal format"""

        components = []
        component_id = 1

        # Process components
        for comp in architecture.get('components', []):
            service_type = comp.get('type', 'appservice')
            quantity = comp.get('quantity', 1)

            for i in range(quantity):
                component = {
                    'id': f"{service_type}_{component_id}",
                    'type': service_type,
                    'name': f"{service_type}{i+1 if quantity > 1 else ''}",
                    'display_name': comp.get('display_name', self._get_default_display_name(service_type)),
                    'layer': comp.get('layer', 'application')
                }
                components.append(component)
                component_id += 1

        # Process connections
        connections = []
        for conn in architecture.get('connections', []):
            from_type = conn.get('from_type')
            to_type = conn.get('to_type')

            # Find all components of these types
            from_comps = [c for c in components if c['type'] == from_type]
            to_comps = [c for c in components if c['type'] == to_type]

            # Simplified connection strategy to avoid diagram clutter
            # Strategy: Create representative connections instead of full mesh
            if from_comps and to_comps:
                # If multiple instances exist, show connection from first instance to first target
                # This represents the logical flow without cluttering the diagram
                from_comp = from_comps[0]
                to_comp = to_comps[0]

                # Update label to indicate multiple instances if applicable
                label = conn.get('label', 'connects to')
                if len(from_comps) > 1 or len(to_comps) > 1:
                    label = f"{label} (×{len(from_comps)})" if len(from_comps) > 1 else label

                connections.append({
                    'from': from_comp['id'],
                    'to': to_comp['id'],
                    'label': label,
                    'type': conn.get('type', 'routes_to')
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

    def _fallback_parse(self, description: str) -> Dict:
        """Fallback to simple keyword matching if AI fails"""
        print("⚠️ Using fallback keyword parser")

        # Import the original keyword parser
        from nl_parser import NaturalLanguageParser
        fallback = NaturalLanguageParser()
        return fallback.parse(description)

    def _get_service_types(self) -> Dict:
        """Get available Azure service types"""
        return {
            'appservice': 'App Service',
            'functionapp': 'Azure Functions',
            'apimanagement': 'API Management',
            'vm': 'Virtual Machine',
            'container': 'Container Instance',
            'aks': 'Azure Kubernetes Service',
            'sqldb': 'SQL Database',
            'cosmosdb': 'Cosmos DB',
            'mysql': 'MySQL Database',
            'postgresql': 'PostgreSQL Database',
            'redis': 'Redis Cache',
            'blobstorage': 'Blob Storage',
            'datalake': 'Data Lake Storage',
            'vnet': 'Virtual Network',
            'appgateway': 'Application Gateway',
            'loadbalancer': 'Load Balancer',
            'firewall': 'Azure Firewall',
            'keyvault': 'Key Vault',
            'mlworkspace': 'Machine Learning Workspace',
            'cognitiveservices': 'Cognitive Services',
            'servicebus': 'Service Bus',
            'eventhub': 'Event Hub',
            'eventgrid': 'Event Grid',
            'synapse': 'Synapse Analytics',
            'datafactory': 'Data Factory',
            'streamanalytics': 'Stream Analytics',
            'monitor': 'Azure Monitor',
            'appinsights': 'Application Insights',
            'iothub': 'IoT Hub',
            'powerbi': 'Power BI',
            # Non-Azure Integrations
            'github': 'GitHub',
            'grafana': 'Grafana',
            'jira': 'Jira',
            'confluence': 'Confluence',
            'mcpserver': 'MCP Server',
            'genericserver': 'Server'
        }

    def _get_default_display_name(self, service_type: str) -> str:
        """Get default display name for service type"""
        return self.service_types.get(service_type, service_type.title())

    def update_architecture(self, current_architecture: Dict, modification: str) -> Dict:
        """
        Update existing architecture based on modification request
        """
        try:
            print(f"\n Updating architecture with: {modification}")
            
            # Step 1: Generate updated architecture using AI
            updated_json = self._call_ai_update(current_architecture, modification)
            
            # Step 2: Parse and validate JSON
            architecture = self._parse_json_response(updated_json)
            
            # Step 3: Convert to internal format (re-using existing logic but keeping IDs if possible)
            # For simplicity in this version, we regenerate IDs to ensure consistency
            result = self._convert_to_internal_format(architecture, f"{current_architecture.get('description', '')} + {modification}")
            
            return result

        except Exception as e:
            print(f" AI update error: {e}")
            raise

    def _call_ai_update(self, current: Dict, modification: str) -> str:
        """Call AI to update architecture with automatic failover"""
        prompt = self._build_update_prompt(current, modification)
        last_error = None
        
        # Try each provider in failover list
        for attempt, provider in enumerate(self.failover_providers):
            try:
                # Switch to failover provider if needed
                if provider != self.provider:
                    print(f" Switching to failover provider: {provider}")
                    self.setup_ai_client(provider)
                
                if self.provider == 'gemini':
                    response = self.model.generate_content(prompt)
                    return response.text
                    
                elif self.provider == 'openai':
                    response = self.client.ChatCompletion.create(
                        model=self.model_name,
                        messages=[
                            {"role": "system", "content": "You are an Azure Solutions Architect. Return only valid JSON."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.1,
                        max_tokens=3000
                    )
                    return response.choices[0].message.content
                    
                elif self.provider == 'anthropic':
                    message = self.client.messages.create(
                        model=self.model_name,
                        max_tokens=3000,
                        temperature=0.1,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    return message.content[0].text
                    
                elif self.provider == 'azure_openai':
                    response = self.client.ChatCompletion.create(
                        engine=self.deployment_name,
                        messages=[
                            {"role": "system", "content": "You are an Azure Solutions Architect. Return only valid JSON."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.1,
                        max_tokens=3000
                    )
                    return response.choices[0].message.content
                      
            except Exception as e:
                last_error = e
                error_msg = str(e).lower()
                
                # Check if it's an auth/quota error
                if any(keyword in error_msg for keyword in ['auth', 'api key', 'quota', 'rate limit', 'expired', '401', '403', '429']):
                    print(f" {provider} failed (auth/quota): {e}")
                    if attempt < len(self.failover_providers) - 1:
                        print(f" Trying next provider...")
                        continue
                else:
                    # Non-auth error, don't failover
                    print(f" AI Update API call failed: {e}")
                    raise
        
        # All providers failed
        print(f" All {len(self.failover_providers)} providers failed for update")
        raise Exception(f"All AI providers exhausted. Last error: {last_error}")

    def _build_update_prompt(self, current: Dict, modification: str) -> str:
        """Build prompt for updating architecture"""
        
        # Simplify current architecture for the prompt to save tokens and focus AI
        simple_current = {
            "components": [{"type": c["type"], "display_name": c["display_name"], "layer": c["layer"]} for c in current.get("components", [])],
            "connections": [{"from_type": self._get_type_from_id(c["from"], current), "to_type": self._get_type_from_id(c["to"], current), "label": c.get("label", "")} for c in current.get("connections", [])]
        }
        
        prompt = f"""You are an Azure Solutions Architect. Update the following architecture based on the user's request.

CURRENT ARCHITECTURE (JSON):
{json.dumps(simple_current, indent=2)}

USER MODIFICATION REQUEST:
"{modification}"

TASK:
1. Analyze the current architecture and the user's request.
2. Add, remove, or modify components and connections as requested.
3. Ensure the resulting architecture is valid and follows best practices.
4. Return the COMPLETE updated architecture as valid JSON.

RETURN FORMAT (JSON ONLY):
{{
  "components": [
    {{
      "type": "service_type",
      "display_name": "Human readable name",
      "layer": "layer_name",
      "quantity": 1
    }}
  ],
  "connections": [
    {{
      "from_type": "source_type",
      "to_type": "target_type",
      "label": "Connection label",
      "type": "routes_to"
    }}
  ]
}}

AVAILABLE SERVICES:
{self._get_service_list()}

IMPORTANT:
- Return the FULL updated architecture schema, not just the diff.
- Keep existing components unless explicitly asked to remove them.
- Ensure all new components are connected logically.
"""
        return prompt

    def _get_type_from_id(self, comp_id: str, architecture: Dict) -> str:
        """Helper to look up type from ID"""
        for comp in architecture.get("components", []):
            if comp["id"] == comp_id:
                return comp["type"]
        return "unknown"

    def _get_service_list(self) -> str:
        """Get formatted list of available services"""
        categories = {
            'Web & Apps': ['appservice', 'functionapp', 'apimanagement'],
            'Compute': ['vm', 'aks', 'container'],
            'Database': ['sqldb', 'cosmosdb', 'mysql', 'postgresql', 'redis'],
            'Storage': ['blobstorage', 'datalake'],
            'Network': ['vnet', 'appgateway', 'loadbalancer', 'firewall'],
            'Security': ['keyvault'],
            'Messaging': ['servicebus', 'eventhub', 'eventgrid'],
            'Analytics': ['synapse', 'datafactory', 'streamanalytics', 'powerbi'],
            'Monitoring': ['monitor', 'appinsights', 'grafana'],
            'AI/ML': ['mlworkspace', 'cognitiveservices'],
            'IoT': ['iothub'],
            'Integrations': ['github', 'jira', 'confluence', 'mcpserver', 'genericserver']
        }

        result = []
        for category, services in categories.items():
            service_names = [f"{s} ({self.service_types.get(s, s)})" for s in services]
            result.append(f"{category}: {', '.join(service_names)}")

        return '\n'.join(result)
