#!/usr/bin/env python3
import os
import json
from diagram_generator import DiagramGenerator

OUT_DIR = os.path.join(os.path.dirname(__file__), 'output')
os.makedirs(OUT_DIR, exist_ok=True)

sample_arch = {
    'description': 'Webapp Test Architecture',
    'components': [
        {'id': 'c1', 'type': 'appservice', 'display_name': 'Web Frontend', 'layer': 'frontend'},
        {'id': 'c2', 'type': 'functionapp', 'display_name': 'API Layer', 'layer': 'application'},
        {'id': 'c3', 'type': 'sqldb', 'display_name': 'User DB', 'layer': 'data'},
        {'id': 'c4', 'type': 'mlworkspace', 'display_name': 'AI Model', 'layer': 'ai'},
    ],
    'connections': [
        {'from': 'c1', 'to': 'c2', 'label': 'HTTPS'},
        {'from': 'c2', 'to': 'c3', 'label': 'queries'},
        {'from': 'c2', 'to': 'c4', 'label': 'predict'}
    ],
    'layers': {'frontend': {}, 'application': {}, 'data': {}, 'ai': {}}
}

if __name__ == '__main__':
    gen = DiagramGenerator()
    outbase = os.path.join(OUT_DIR, 'test_diagram')
    print('Generating diagram to', outbase)
    res = gen.generate(sample_arch, outbase)
    print('\nResult:')
    print(json.dumps(res, indent=2))

    print('\nOutput dir listing:')
    for f in os.listdir(OUT_DIR):
        print(' -', f)
