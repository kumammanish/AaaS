#!/usr/bin/env python3
"""
Azure Architecture Diagram Generator - Web Application
Generates Azure architecture diagrams from natural language descriptions
"""
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
import sys
import json
import tempfile
import subprocess
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = os.path.join(tempfile.gettempdir(), 'azure_diagrams')
OUTPUT_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Import diagram generator components
from diagram_generator import DiagramGenerator
from nl_parser import NaturalLanguageParser
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize components
diagram_generator = DiagramGenerator()

# Choose parser based on environment variable
USE_AI_PARSER = os.getenv('USE_AI_PARSER', 'false').lower() == 'true'

if USE_AI_PARSER:
    try:
        from ai_parser import AIParser
        nl_parser = AIParser()
        print("=" * 80)
        print(" AI-POWERED PARSER ENABLED")
        print(f"   Provider: {os.getenv('AI_PROVIDER', 'gemini')}")
        print(f"   MCP: {'Enabled' if os.getenv('USE_MCP', 'false').lower() == 'true' else 'Disabled'}")
        print("=" * 80)
    except Exception as e:
        print(f"⚠️ Failed to initialize AI parser: {e}")
        print("   Falling back to keyword parser")
        nl_parser = NaturalLanguageParser()
else:
    nl_parser = NaturalLanguageParser()
    print("=" * 80)
    print(" KEYWORD-BASED PARSER ENABLED")
    print("   Set USE_AI_PARSER=true to enable AI")
    print("=" * 80)

@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate_diagram():
    """
    Generate diagram from natural language description

    Expected JSON:
    {
        "description": "Create a web app with SQL database and Redis cache",
        "format": "png",  # png, svg, pdf
        "style": "default"  # default, detailed, simple
    }
    """
    try:
        data = request.get_json()

        if not data or 'description' not in data:
            return jsonify({'error': 'No description provided'}), 400

        description = data['description']
        output_format = data.get('format', 'svg')
        style = data.get('style', 'default')

        # Parse natural language to extract architecture components
        parsed_architecture = nl_parser.parse(description)

        if not parsed_architecture:
            return jsonify({'error': 'Could not parse architecture from description'}), 400

        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        diagram_name = f"azure_arch_{timestamp}"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], diagram_name)

        # Generate diagram
        result = diagram_generator.generate(
            architecture=parsed_architecture,
            output_path=output_path,
            output_format=output_format,
            style=style
        )

        if result['success']:
            # Build file URLs for all generated formats
            file_urls = {
                'png': f'/download/{diagram_name}.png',
                'dot': f'/download/{diagram_name}.dot'
            }

            # Add draw.io URL if it was generated
            if 'drawio' in result.get('output_files', {}):
                file_urls['drawio'] = f'/download/{diagram_name}.drawio'

            # Add requested format if different from png/dot
            if output_format and output_format not in ['png', 'dot']:
                 file_urls[output_format] = f'/download/{diagram_name}.{output_format}'

            return jsonify({
                'success': True,
                'diagram_url': f'/download/{diagram_name}.png',  # Always return PNG for display
                'file_urls': file_urls,  # All available formats
                'architecture': parsed_architecture,
                'metadata': {
                    'generated_at': timestamp,
                    'format': result.get('format', output_format),  # Updated format string
                    'components': len(parsed_architecture.get('components', []))
                },
                'local_paths': {
                    'folder': app.config['OUTPUT_FOLDER'],
                    'png': os.path.join(app.config['OUTPUT_FOLDER'], f"{diagram_name}.png"),
                    'dot': os.path.join(app.config['OUTPUT_FOLDER'], f"{diagram_name}.dot"),
                    'drawio': os.path.join(app.config['OUTPUT_FOLDER'], f"{diagram_name}.drawio") if 'drawio' in result.get('output_files', {}) else None,
                    output_format: os.path.join(app.config['OUTPUT_FOLDER'], f"{diagram_name}.{output_format}") if output_format not in ['png', 'dot', 'drawio'] else None
                }
            })
        else:
            return jsonify({'error': result.get('error', 'Generation failed')}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/parse', methods=['POST'])
def parse_description():
    """
    Parse natural language description without generating diagram
    Useful for preview/validation
    """
    try:
        data = request.get_json()

        if not data or 'description' not in data:
            return jsonify({'error': 'No description provided'}), 400

        description = data['description']
        parsed_architecture = nl_parser.parse(description)

        return jsonify({
            'success': True,
            'architecture': parsed_architecture,
            'component_count': len(parsed_architecture.get('components', [])),
            'connections': len(parsed_architecture.get('connections', []))
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/refine', methods=['POST'])
def refine_diagram():
    """
    Refine existing diagram based on new instructions
    """
    try:
        data = request.get_json()

        if not data or 'current_architecture' not in data or 'modification' not in data:
            return jsonify({'error': 'Missing current_architecture or modification'}), 400

        current_architecture = data['current_architecture']
        modification = data['modification']
        output_format = data.get('format', 'png')
        style = data.get('style', 'default')
        
        # Use AI parser for refinement (requires AI capabilities)
        if not USE_AI_PARSER:
             return jsonify({'error': 'Refinement requires AI features to be enabled (USE_AI_PARSER=true)'}), 400
             
        # Update architecture
        updated_architecture = nl_parser.update_architecture(current_architecture, modification)

        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        diagram_name = f"azure_arch_{timestamp}"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], diagram_name)

        # Generate diagram
        result = diagram_generator.generate(
            architecture=updated_architecture,
            output_path=output_path,
            output_format=output_format,
            style=style
        )

        if result['success']:
            # Build file URLs
            file_urls = {
                'png': f'/download/{diagram_name}.png',
                'dot': f'/download/{diagram_name}.dot'
            }
            
            if 'drawio' in result.get('output_files', {}):
                file_urls['drawio'] = f'/download/{diagram_name}.drawio'
                
            if output_format and output_format not in ['png', 'dot']:
                 file_urls[output_format] = f'/download/{diagram_name}.{output_format}'

            return jsonify({
                'success': True,
                'diagram_url': f'/download/{diagram_name}.png',
                'file_urls': file_urls,
                'architecture': updated_architecture,
                'metadata': {
                    'generated_at': timestamp,
                    'format': result.get('format', output_format),
                    'components': len(updated_architecture.get('components', []))
                },
                'local_paths': {
                    'folder': app.config['OUTPUT_FOLDER'],
                    'png': os.path.join(app.config['OUTPUT_FOLDER'], f"{diagram_name}.png"),
                    'dot': os.path.join(app.config['OUTPUT_FOLDER'], f"{diagram_name}.dot"),
                    'drawio': os.path.join(app.config['OUTPUT_FOLDER'], f"{diagram_name}.drawio") if 'drawio' in result.get('output_files', {}) else None,
                    output_format: os.path.join(app.config['OUTPUT_FOLDER'], f"{diagram_name}.{output_format}") if output_format not in ['png', 'dot', 'drawio'] else None
                }
            })
        else:
            return jsonify({'error': result.get('error', 'Generation failed')}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/examples', methods=['GET'])
def get_examples():
    """Get example architecture descriptions"""
    examples = [
        {
            'title': '3-Tier Web Application',
            'description': 'Create a 3-tier web application with Application Gateway as frontend, two Web Apps in the middle tier, and SQL Database with Redis cache in the backend.',
            'tags': ['web', 'database', 'cache']
        },
        {
            'title': 'Microservices Platform',
            'description': 'Build a microservices architecture with AKS cluster, Azure Service Bus for messaging, Cosmos DB for data storage, and API Management gateway.',
            'tags': ['microservices', 'kubernetes', 'messaging']
        },
        {
            'title': 'Data Analytics Platform',
            'description': 'Design a data analytics platform with Azure Data Factory for ingestion, Data Lake Storage, Azure Synapse for analytics, and Power BI for visualization.',
            'tags': ['analytics', 'data', 'bi']
        },
        {
            'title': 'IoT Solution',
            'description': 'Create an IoT solution with IoT Hub for device connectivity, Stream Analytics for processing, Cosmos DB for storage, and Azure Functions for serverless processing.',
            'tags': ['iot', 'streaming', 'serverless']
        },
        {
            'title': 'Secure Infrastructure',
            'description': 'Build secure infrastructure with Virtual Network, Application Gateway with WAF, Web App with private endpoints, Key Vault for secrets, and Azure Monitor for logging.',
            'tags': ['security', 'networking', 'monitoring']
        }
    ]

    return jsonify({'examples': examples})

@app.route('/download/<filename>')
def download_file(filename):
    """Download generated diagram"""
    try:
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)

        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404

        return send_file(file_path)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'components': {
            'diagram_generator': 'operational',
            'nl_parser': 'operational'
        }
    })

if __name__ == '__main__':
    print("="*80)
    print(" Azure Architecture Diagram Generator - Web Application")
    print("="*80)
    print("\n Starting server...")
    print(f"   Output folder: {app.config['OUTPUT_FOLDER']}")
    print(f"   Temp folder: {app.config['UPLOAD_FOLDER']}")
    print("\n Access the application at: http://localhost:5001")
    print("\n API Endpoints:")
    print("   POST /api/generate - Generate diagram from description")
    print("   POST /api/parse - Parse description without generating")
    print("   GET  /api/examples - Get example descriptions")
    print("   GET  /api/health - Health check")
    print("\n" + "="*80 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5001)
