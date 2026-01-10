#!/usr/bin/env python3
"""
Diagram Generator - Creates Azure architecture diagrams from parsed components
Uses the diagrams library to generate visual representations
"""
import os
import sys
import subprocess
from typing import Dict, List
from diagrams import Diagram, Cluster, Edge
from diagrams.azure.compute import VM, ContainerInstances, FunctionApps, AppServices
from diagrams.azure.web import AppServices as WebApp
from diagrams.azure.database import SQLDatabases, CosmosDb, CacheForRedis, DatabaseForMysqlServers, DatabaseForPostgresqlServers
from diagrams.azure.storage import BlobStorage, StorageAccounts, DataLakeStorage
from diagrams.azure.network import VirtualNetworks, ApplicationGateway, LoadBalancers, Firewall
from diagrams.azure.security import KeyVaults
from diagrams.azure.integration import APIManagement, ServiceBus, EventGridTopics
from diagrams.azure.analytics import SynapseAnalytics, DataFactories, StreamAnalyticsJobs, EventHubs
from diagrams.azure.analytics import LogAnalyticsWorkspaces
from diagrams.azure.devops import ApplicationInsights
from diagrams.azure.ml import MachineLearningServiceWorkspaces, CognitiveServices
from diagrams.azure.iot import IotHub
# Non-Azure icons for integrations
from diagrams.onprem.vcs import Github
from diagrams.onprem.compute import Server
from diagrams.generic.compute import Rack

class DiagramGenerator:
    """Generate Azure architecture diagrams from parsed components"""

    def __init__(self):
        # Map service types to diagrams library classes
        self.service_mapping = {
            # Azure Services
            'appservice': AppServices,
            'functionapp': FunctionApps,
            'apimanagement': APIManagement,
            'vm': VM,
            'container': ContainerInstances,
            'aks': ContainerInstances,  # Use container icon for AKS
            'sqldb': SQLDatabases,
            'cosmosdb': CosmosDb,
            'mysql': DatabaseForMysqlServers,
            'postgresql': DatabaseForPostgresqlServers,
            'redis': CacheForRedis,
            'blobstorage': BlobStorage,
            'datalake': DataLakeStorage,
            'vnet': VirtualNetworks,
            'appgateway': ApplicationGateway,
            'loadbalancer': LoadBalancers,
            'firewall': Firewall,
            'keyvault': KeyVaults,
            'mlworkspace': MachineLearningServiceWorkspaces,
            'cognitiveservices': CognitiveServices,
            'servicebus': ServiceBus,
            'eventhub': EventHubs,
            'eventgrid': EventGridTopics,
            'synapse': SynapseAnalytics,
            'datafactory': DataFactories,
            'streamanalytics': StreamAnalyticsJobs,
            'monitor': LogAnalyticsWorkspaces,
            'appinsights': ApplicationInsights,
            'iothub': IotHub,
            # Non-Azure Integrations
            'github': Github,
            'mcpserver': Server,  # MCP Server (Model Context Protocol)
            'confluence': Rack,   # Using Rack as placeholder for Confluence
            'genericserver': Server
        }

        # Layer colors
        self.layer_colors = {
            'frontend': '#BBDEFB',      # Light Blue
            'application': '#FFE0B2',   # Light Orange
            'data': '#F8BBD0',          # Light Pink
            'messaging': '#E1BEE7',     # Light Purple
            'analytics': '#C5E1A5',     # Light Lime
            'infrastructure': '#D1C4E9', # Light Indigo
            'ai': '#FFF9C4',            # Light Yellow
            'monitoring': '#B2EBF2',    # Light Cyan
            'iot': '#C8E6C9',           # Light Green
            'security': '#E0E0E0',      # Light Gray
            'integrations': '#F0F4C3',  # Light Lime Yellow
            'external': '#FFE0B2'       # Light Peach
        }

    def generate(self, architecture: Dict, output_path: str,
                 output_format: str = 'png', style: str = 'default') -> Dict:
        """
        Generate diagram from parsed architecture

        Args:
            architecture: Parsed architecture dictionary
            output_path: Path for output file (without extension)
            output_format: Output format (png, svg, pdf)
            style: Diagram style (default, detailed, simple)

        Returns:
            Dictionary with success status and file paths
        """
        try:
            components = architecture.get('components', [])
            connections = architecture.get('connections', [])
            layers = architecture.get('layers', {})

            if not components:
                return {
                    'success': False,
                    'error': 'No components found in architecture'
                }

            # Generate diagram
            graph_attr = {
                "splines": "ortho",
                "nodesep": "1.0",
                "ranksep": "1.5",
                "fontsize": "13",
                "bgcolor": "white",
                "pad": "0.5",
                "compound": "true",  # Enable proper icon rendering
            }

            # Determine formats to generate
            formats = ["png", "dot"]
            if output_format and output_format not in ["png", "dot"]:
                formats.append(output_format)

            with Diagram(
                architecture.get('description', 'Azure Architecture'),
                filename=output_path,
                outformat=formats,
                show=False,
                direction="TB",
                graph_attr=graph_attr
            ):
                # Create node instances
                nodes = {}

                # Group components by layer
                layer_components = {}
                for component in components:
                    layer = component['layer']
                    if layer not in layer_components:
                        layer_components[layer] = []
                    layer_components[layer].append(component)

                # Create clusters for each layer
                for layer_name, layer_comps in layer_components.items():
                    cluster_attr = {
                        "fontsize": "14",
                        "bgcolor": self.layer_colors.get(layer_name, "#E0E0E0"),
                        "style": "rounded",
                        "margin": "20"
                    }

                    layer_display_name = layer_name.replace('_', ' ').title()

                    with Cluster(f"{layer_display_name} Layer", graph_attr=cluster_attr):
                        for component in layer_comps:
                            node_class = self.service_mapping.get(component['type'])

                            if node_class:
                                node = node_class(component['display_name'])
                                nodes[component['id']] = node

                # Create connections
                for connection in connections:
                    from_id = connection.get('from')
                    to_id = connection.get('to')

                    if from_id in nodes and to_id in nodes:
                        from_node = nodes[from_id]
                        to_node = nodes[to_id]
                        label = connection.get('label', '')

                        # Create edge
                        from_node >> Edge(label=label, style="bold", penwidth="2") >> to_node

            # Files generated by diagrams library
            png_file = f"{output_path}.png"
            dot_file = f"{output_path}.dot"
            drawio_file = f"{output_path}.drawio"

            # Convert DOT to draw.io format
            try:
                subprocess.run([
                    "graphviz2drawio",
                    dot_file,
                    "-o",
                    drawio_file
                ], check=True, capture_output=True)
                print(f" Generated draw.io file: {drawio_file}")
                drawio_generated = True
            except FileNotFoundError:
                print("⚠️  graphviz2drawio not found - install with: pip install graphviz2drawio")
                drawio_generated = False
            except Exception as e:
                print(f"⚠️  Draw.io conversion error: {e}")
                drawio_generated = False

            result = {
                'success': True,
                'output_files': {
                    'png': png_file,
                    'dot': dot_file,
                },
                'format': 'png, dot',
                'component_count': len(components),
                'connection_count': len(connections)
            }

            # Add draw.io file if successfully generated
            if drawio_generated:
                result['output_files']['drawio'] = drawio_file
                result['format'] = 'png, dot, drawio'

            # Keep backward compatibility
            result['output_file'] = png_file

            return result

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def _get_edge_color(self, connection_type: str) -> str:
        """Get edge color based on connection type"""
        color_mapping = {
            'routes_to': '#1976D2',   # Blue
            'queries': '#388E3C',     # Green
            'caches': '#F57C00',      # Orange
            'stores': '#7B1FA2',      # Purple
            'processes': '#C2185B',   # Pink
            'monitors': '#00838F'     # Cyan
        }
        return color_mapping.get(connection_type, '#000000')
