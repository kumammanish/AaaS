#!/usr/bin/env python3
"""
Natural Language Parser for Azure Architecture Descriptions
Parses user descriptions into structured architecture components
"""
import re
from typing import Dict, List, Optional

class NaturalLanguageParser:
    """
    Parse natural language descriptions into Azure architecture components

    Supports keywords like:
    - Web: App Service, Web App, Website
    - Database: SQL, MySQL, PostgreSQL, Cosmos DB
    - Cache: Redis, Cache
    - Storage: Blob Storage, Storage Account, Data Lake
    - Compute: VM, Virtual Machine, Container, AKS, Kubernetes
    - Networking: VNet, Application Gateway, Load Balancer, Firewall
    - Security: Key Vault, Security Center, Firewall, WAF
    - AI/ML: Machine Learning, Cognitive Services, AI
    - Messaging: Service Bus, Event Hub, Event Grid
    - Analytics: Synapse, Data Factory, Stream Analytics
    """

    def __init__(self):
        # Azure service keywords mapping
        self.service_patterns = {
            # Web & Apps
            'appservice': ['web app', 'app service', 'website', 'web application'],
            'functionapp': ['function', 'azure function', 'serverless function', 'lambda'],
            'apimanagement': ['api management', 'api gateway', 'apim'],

            # Compute
            'vm': ['virtual machine', 'vm', 'compute instance'],
            'container': ['container instance', 'container', 'aci'],
            'aks': ['kubernetes', 'aks', 'k8s cluster'],

            # Database
            'sqldb': ['sql database', 'sql server', 'sql db', 'mssql'],
            'cosmosdb': ['cosmos db', 'cosmos', 'nosql database', 'document db'],
            'mysql': ['mysql', 'mysql database'],
            'postgresql': ['postgresql', 'postgres', 'postgres database'],

            # Cache & Storage
            'redis': ['redis', 'cache', 'redis cache'],
            'blobstorage': ['blob storage', 'blob', 'object storage', 'storage account'],
            'datalake': ['data lake', 'adls', 'data lake storage'],

            # Networking
            'vnet': ['virtual network', 'vnet', 'network'],
            'appgateway': ['application gateway', 'app gateway', 'waf'],
            'loadbalancer': ['load balancer', 'lb'],
            'firewall': ['firewall', 'azure firewall'],

            # Security
            'keyvault': ['key vault', 'secrets', 'vault'],
            'securitycenter': ['security center', 'defender'],

            # AI/ML
            'mlworkspace': ['machine learning', 'ml workspace', 'ai studio', 'ml'],
            'cognitiveservices': ['cognitive services', 'ai services'],

            # Messaging
            'servicebus': ['service bus', 'message queue', 'messaging'],
            'eventhub': ['event hub', 'event stream'],
            'eventgrid': ['event grid', 'events'],

            # Analytics
            'synapse': ['synapse', 'data warehouse', 'analytics workspace'],
            'datafactory': ['data factory', 'adf', 'etl'],
            'streamanalytics': ['stream analytics', 'streaming'],

            # Monitoring
            'monitor': ['azure monitor', 'monitoring', 'log analytics'],
            'appinsights': ['application insights', 'app insights', 'apm'],

            # IoT
            'iothub': ['iot hub', 'iot', 'device management'],
        }

        # Connection keywords
        self.connection_patterns = {
            'connects_to': ['connects to', 'connected to', 'links to', 'communicates with'],
            'stores_in': ['stores in', 'saves to', 'persists to', 'writes to'],
            'reads_from': ['reads from', 'fetches from', 'queries'],
            'routes_through': ['routes through', 'via', 'through'],
            'protected_by': ['protected by', 'secured by', 'behind']
        }

        # Quantity patterns
        self.quantity_patterns = [
            r'(\d+)\s+(\w+)',  # "2 web apps"
            r'(two|three|four|five|six|seven|eight|nine|ten)\s+(\w+)',  # "two web apps"
        ]

    def parse(self, description: str) -> Dict:
        """
        Parse natural language description into structured architecture

        Args:
            description: Natural language architecture description

        Returns:
            Dictionary containing:
            - components: List of Azure components
            - connections: List of connections between components
            - layers: Logical grouping of components
        """
        description_lower = description.lower()

        # Extract components
        components = self._extract_components(description_lower)

        # Extract connections
        connections = self._extract_connections(description_lower, components)

        # Organize into layers (frontend, backend, data, etc.)
        layers = self._organize_layers(components)

        return {
            'description': description,
            'components': components,
            'connections': connections,
            'layers': layers
        }

    def _extract_components(self, description: str) -> List[Dict]:
        """Extract Azure components from description"""
        components = []
        component_id = 1

        for service_type, keywords in self.service_patterns.items():
            for keyword in keywords:
                if keyword in description:
                    # Extract quantity if specified
                    quantity = self._extract_quantity(description, keyword)

                    for i in range(quantity):
                        component = {
                            'id': f'{service_type}_{component_id}',
                            'type': service_type,
                            'name': self._generate_component_name(service_type, i + 1 if quantity > 1 else None),
                            'display_name': self._get_display_name(service_type),
                            'layer': self._get_layer(service_type)
                        }
                        components.append(component)
                        component_id += 1

                    break  # Found this service, move to next

        return components

    def _extract_quantity(self, description: str, keyword: str) -> int:
        """Extract quantity for a service (default 1)"""
        # Look for patterns like "2 web apps" or "two databases"
        pattern = rf'(\d+|two|three|four|five|six|seven|eight|nine|ten)\s+{keyword}'
        match = re.search(pattern, description)

        if match:
            num_str = match.group(1)
            number_words = {
                'two': 2, 'three': 3, 'four': 4, 'five': 5,
                'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10
            }
            return int(num_str) if num_str.isdigit() else number_words.get(num_str, 1)

        return 1

    def _generate_component_name(self, service_type: str, index: Optional[int] = None) -> str:
        """Generate component name"""
        base_names = {
            'appservice': 'webapp',
            'functionapp': 'func',
            'apimanagement': 'apim',
            'vm': 'vm',
            'container': 'container',
            'aks': 'aks',
            'sqldb': 'sqldb',
            'cosmosdb': 'cosmosdb',
            'mysql': 'mysql',
            'postgresql': 'postgres',
            'redis': 'redis',
            'blobstorage': 'storage',
            'datalake': 'datalake',
            'vnet': 'vnet',
            'appgateway': 'appgw',
            'loadbalancer': 'lb',
            'firewall': 'firewall',
            'keyvault': 'kv',
            'securitycenter': 'security',
            'mlworkspace': 'ml',
            'cognitiveservices': 'cognitive',
            'servicebus': 'servicebus',
            'eventhub': 'eventhub',
            'eventgrid': 'eventgrid',
            'synapse': 'synapse',
            'datafactory': 'adf',
            'streamanalytics': 'asa',
            'monitor': 'monitor',
            'appinsights': 'appinsights',
            'iothub': 'iothub'
        }

        base_name = base_names.get(service_type, service_type)
        return f"{base_name}{index if index else ''}"

    def _get_display_name(self, service_type: str) -> str:
        """Get human-readable display name"""
        display_names = {
            'appservice': 'App Service',
            'functionapp': 'Function App',
            'apimanagement': 'API Management',
            'vm': 'Virtual Machine',
            'container': 'Container Instance',
            'aks': 'AKS Cluster',
            'sqldb': 'SQL Database',
            'cosmosdb': 'Cosmos DB',
            'mysql': 'MySQL',
            'postgresql': 'PostgreSQL',
            'redis': 'Redis Cache',
            'blobstorage': 'Blob Storage',
            'datalake': 'Data Lake',
            'vnet': 'Virtual Network',
            'appgateway': 'Application Gateway',
            'loadbalancer': 'Load Balancer',
            'firewall': 'Azure Firewall',
            'keyvault': 'Key Vault',
            'securitycenter': 'Security Center',
            'mlworkspace': 'ML Workspace',
            'cognitiveservices': 'Cognitive Services',
            'servicebus': 'Service Bus',
            'eventhub': 'Event Hub',
            'eventgrid': 'Event Grid',
            'synapse': 'Azure Synapse',
            'datafactory': 'Data Factory',
            'streamanalytics': 'Stream Analytics',
            'monitor': 'Azure Monitor',
            'appinsights': 'App Insights',
            'iothub': 'IoT Hub'
        }

        return display_names.get(service_type, service_type.title())

    def _get_layer(self, service_type: str) -> str:
        """Determine which logical layer component belongs to"""
        layer_mapping = {
            # Frontend
            'appgateway': 'frontend',
            'loadbalancer': 'frontend',

            # Application
            'appservice': 'application',
            'functionapp': 'application',
            'apimanagement': 'application',
            'container': 'application',
            'aks': 'application',
            'vm': 'application',

            # Data
            'sqldb': 'data',
            'cosmosdb': 'data',
            'mysql': 'data',
            'postgresql': 'data',
            'redis': 'data',
            'blobstorage': 'data',
            'datalake': 'data',

            # Messaging
            'servicebus': 'messaging',
            'eventhub': 'messaging',
            'eventgrid': 'messaging',

            # Analytics
            'synapse': 'analytics',
            'datafactory': 'analytics',
            'streamanalytics': 'analytics',

            # Security
            'vnet': 'infrastructure',
            'firewall': 'infrastructure',
            'keyvault': 'infrastructure',
            'securitycenter': 'infrastructure',

            # AI/ML
            'mlworkspace': 'ai',
            'cognitiveservices': 'ai',

            # Monitoring
            'monitor': 'monitoring',
            'appinsights': 'monitoring',

            # IoT
            'iothub': 'iot'
        }

        return layer_mapping.get(service_type, 'application')

    def _extract_connections(self, description: str, components: List[Dict]) -> List[Dict]:
        """Extract connections between components"""
        connections = []

        # Auto-generate logical connections based on architecture patterns
        frontend_components = [c for c in components if c['layer'] == 'frontend']
        app_components = [c for c in components if c['layer'] == 'application']
        data_components = [c for c in components if c['layer'] == 'data']

        # Frontend -> Application
        for frontend in frontend_components:
            for app in app_components:
                connections.append({
                    'from': frontend['id'],
                    'to': app['id'],
                    'type': 'routes_to',
                    'label': 'HTTP/HTTPS'
                })

        # Application -> Data
        for app in app_components:
            for data in data_components:
                # Web apps connect to databases and cache
                if 'sqldb' in data['type'] or 'cosmosdb' in data['type'] or 'mysql' in data['type']:
                    connections.append({
                        'from': app['id'],
                        'to': data['id'],
                        'type': 'queries',
                        'label': 'Query'
                    })
                elif 'redis' in data['type']:
                    connections.append({
                        'from': app['id'],
                        'to': data['id'],
                        'type': 'caches',
                        'label': 'Cache'
                    })
                elif 'blobstorage' in data['type'] or 'datalake' in data['type']:
                    connections.append({
                        'from': app['id'],
                        'to': data['id'],
                        'type': 'stores',
                        'label': 'Store'
                    })

        return connections

    def _organize_layers(self, components: List[Dict]) -> Dict[str, List[str]]:
        """Organize components into logical layers"""
        layers = {}

        for component in components:
            layer = component['layer']
            if layer not in layers:
                layers[layer] = []
            layers[layer].append(component['id'])

        return layers
