// Azure Architecture Diagram Generator - Frontend Application

class DiagramApp {
    constructor() {
        this.apiBaseUrl = '/api';
        this.currentDiagramUrl = null;
        this.init();
    }

    init() {
        // Get DOM elements
        this.description = document.getElementById('description');
        this.formatSelect = document.getElementById('format');
        this.styleSelect = document.getElementById('style');
        this.parseBtn = document.getElementById('parseBtn');
        this.generateBtn = document.getElementById('generateBtn');
        this.downloadBtn = document.getElementById('downloadBtn');

        this.loading = document.getElementById('loading');
        this.error = document.getElementById('error');
        this.errorText = document.getElementById('errorText');
        this.preview = document.getElementById('preview');
        this.previewContent = document.getElementById('previewContent');
        this.diagramOutput = document.getElementById('diagramOutput');
        this.placeholder = document.getElementById('placeholder');
        this.diagramImage = document.getElementById('diagramImage');
        this.metadata = document.getElementById('metadata');
        this.examplesContainer = document.getElementById('examplesContainer');

        this.refineSection = document.getElementById('refineSection');
        this.refineInput = document.getElementById('refineInput');
        this.refineBtn = document.getElementById('refineBtn');

        this.currentArchitecture = null;

        // Attach event listeners
        this.parseBtn.addEventListener('click', () => this.handleParse());
        this.generateBtn.addEventListener('click', () => this.handleGenerate());
        this.downloadBtn.addEventListener('click', () => this.handleDownload());
        this.refineBtn.addEventListener('click', () => this.handleRefine());

        // Load examples
        this.loadExamples();

        // Check health on load
        this.checkHealth();
    }

    async checkHealth() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/health`);
            const data = await response.json();
            console.log('API Health:', data);
        } catch (error) {
            console.error('API health check failed:', error);
        }
    }

    async loadExamples() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/examples`);
            const data = await response.json();

            if (data.examples) {
                this.renderExamples(data.examples);
            }
        } catch (error) {
            console.error('Failed to load examples:', error);
        }
    }

    renderExamples(examples) {
        this.examplesContainer.innerHTML = examples.map(example => `
            <div class="example-card" data-description="${this.escapeHtml(example.description)}">
                <h4>${example.title}</h4>
                <p>${example.description}</p>
                <div class="example-tags">
                    ${example.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                </div>
            </div>
        `).join('');

        // Attach click handlers to example cards
        document.querySelectorAll('.example-card').forEach(card => {
            card.addEventListener('click', () => {
                const description = card.getAttribute('data-description');
                this.description.value = description;
                this.description.focus();
                // Scroll to top
                window.scrollTo({ top: 0, behavior: 'smooth' });
            });
        });
    }

    async handleParse() {
        const description = this.description.value.trim();

        if (!description) {
            this.showError('Please enter an architecture description');
            return;
        }

        this.hideAll();
        this.showLoading('Parsing your description...');

        try {
            const response = await fetch(`${this.apiBaseUrl}/parse`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ description })
            });

            const data = await response.json();

            if (data.success) {
                this.showPreview(data.architecture);
            } else {
                this.showError(data.error || 'Failed to parse description');
            }
        } catch (error) {
            this.showError(`Error: ${error.message}`);
        }
    }

    async handleGenerate() {
        const description = this.description.value.trim();
        const format = this.formatSelect.value;
        const style = this.styleSelect.value;

        if (!description) {
            this.showError('Please enter an architecture description');
            return;
        }

        this.hideAll();
        this.showLoading('Generating your architecture diagram...');
        this.disableButtons();

        try {
            const response = await fetch(`${this.apiBaseUrl}/generate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ description, format, style })
            });

            const data = await response.json();

            if (data.success) {
                this.currentArchitecture = data.architecture;
                this.showDiagram(data);
            } else {
                this.showError(data.error || 'Failed to generate diagram');
            }
        } catch (error) {
            this.showError(`Error: ${error.message}`);
        } finally {
            this.enableButtons();
        }
    }

    async handleRefine() {
        const modification = this.refineInput.value.trim();
        const format = this.formatSelect.value;
        const style = this.styleSelect.value;

        if (!modification) {
            this.showError('Please enter a modification request');
            return;
        }

        if (!this.currentArchitecture) {
            this.showError('No active diagram to refine. Please generate one first.');
            return;
        }

        this.hideAll();
        this.showLoading('Refining your architecture...');
        this.disableButtons();
        this.refineBtn.disabled = true;

        try {
            const response = await fetch(`${this.apiBaseUrl}/refine`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    current_architecture: this.currentArchitecture,
                    modification: modification,
                    format,
                    style
                })
            });

            const data = await response.json();

            if (data.success) {
                this.currentArchitecture = data.architecture;
                this.refineInput.value = ''; // Clear input
                this.showDiagram(data);
            } else {
                this.showError(data.error || 'Failed to refine diagram');
                // Re-show diagram output if failure, so state isn't lost
                if (this.currentArchitecture) {
                    // Ideally we'd restore view, but simple error showing is fine for MVP
                }
            }
        } catch (error) {
            this.showError(`Error: ${error.message}`);
        } finally {
            this.enableButtons();
            this.refineBtn.disabled = false;
        }
    }

    handleDownload() {
        if (this.currentDiagramUrl) {
            const link = document.createElement('a');
            link.href = this.currentDiagramUrl;
            // Extract filename from URL
            const filename = this.currentDiagramUrl.split('/').pop();
            link.download = filename;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    }

    showPreview(architecture) {
        this.hideAll();
        this.preview.classList.remove('hidden');

        const components = architecture.components || [];
        const connections = architecture.connections || [];

        let html = '<div style="margin-bottom: 15px;">';
        html += `<p><strong>Components:</strong> ${components.length} | <strong>Connections:</strong> ${connections.length}</p>`;
        html += '</div>';

        // Group by layer
        const layers = {};
        components.forEach(comp => {
            if (!layers[comp.layer]) {
                layers[comp.layer] = [];
            }
            layers[comp.layer].push(comp);
        });

        // Display by layer
        for (const [layer, comps] of Object.entries(layers)) {
            html += `<div style="margin-bottom: 15px;">`;
            html += `<h4 style="color: #0078D4; margin-bottom: 10px;">${layer.replace('_', ' ').toUpperCase()} Layer</h4>`;
            comps.forEach(comp => {
                html += `<div class="component-item">`;
                html += `<strong>${comp.display_name}</strong> (${comp.name})`;
                html += `</div>`;
            });
            html += `</div>`;
        }

        this.previewContent.innerHTML = html;
    }

    showDiagram(data) {
        this.hideAll();
        this.diagramOutput.classList.remove('hidden');

        // Set diagram image
        this.diagramImage.src = data.diagram_url;
        this.currentDiagramUrl = data.diagram_url;

        // Set metadata
        const metadata = data.metadata;
        this.metadata.innerHTML = `
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                <div>
                    <strong>Generated:</strong> ${this.formatTimestamp(metadata.generated_at)}
                </div>
                <div>
                    <strong>Format:</strong> ${metadata.format.toUpperCase()}
                </div>
                <div>
                    <strong>Components:</strong> ${metadata.components}
                </div>
            </div>`;

        // Add local paths if available
        if (data.local_paths) {
            const paths = data.local_paths;
            const urls = data.file_urls || {};

            const createLink = (label, path, url) => `
                <div style="margin-bottom: 8px; display: flex; align-items: center; gap: 10px;">
                    <strong style="color: var(--primary-color); min-width: 60px;">${label}:</strong> 
                    <span style="flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="${path}">${path}</span>
                    ${url ? `<a href="${url}" download class="btn-sm" style="background: var(--primary-color); color: white; padding: 2px 8px; border-radius: 4px; text-decoration: none; font-size: 0.9em;">Download</a>` : ''}
                </div>`;

            this.metadata.innerHTML += `
                <div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid rgba(0,0,0,0.1); width: 100%;">
                    <h4 style="margin-bottom: 8px; font-size: 0.9em; color: var(--text-secondary); text-transform: uppercase;">Generated Files</h4>
                    <div style="background: rgba(0,0,0,0.03); padding: 10px; border-radius: 8px; font-family: 'Consolas', 'Monaco', monospace; font-size: 0.85em; color: var(--text-primary);">
                        ${paths.drawio ? createLink('Draw.io', paths.drawio, urls.drawio) : ''}
                        ${createLink('DOT', paths.dot, urls.dot)}
                        <div style="display: flex; gap: 10px; align-items: center;">
                            <strong style="color: var(--primary-color); min-width: 60px;">Folder:</strong> 
                            <span title="${paths.folder}">${paths.folder}</span>
                        </div>
                    </div>
                </div>
            `;
        }
    }

    showLoading(message = 'Loading...') {
        this.hideAll();
        this.loading.classList.remove('hidden');
        this.loading.querySelector('p').textContent = message;
    }

    showError(message) {
        this.hideAll();
        this.error.classList.remove('hidden');
        this.errorText.textContent = message;
    }

    hideAll() {
        this.loading.classList.add('hidden');
        this.error.classList.add('hidden');
        this.preview.classList.add('hidden');
        this.diagramOutput.classList.add('hidden');
        this.placeholder.classList.add('hidden');
    }

    disableButtons() {
        this.parseBtn.disabled = true;
        this.generateBtn.disabled = true;
    }

    enableButtons() {
        this.parseBtn.disabled = false;
        this.generateBtn.disabled = false;
    }

    formatTimestamp(timestamp) {
        // Format: 20241130_123045 -> Nov 30, 2024 12:30:45
        if (timestamp.length !== 15) return timestamp;

        const year = timestamp.substring(0, 4);
        const month = timestamp.substring(4, 6);
        const day = timestamp.substring(6, 8);
        const hour = timestamp.substring(9, 11);
        const minute = timestamp.substring(11, 13);
        const second = timestamp.substring(13, 15);

        const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

        return `${months[parseInt(month) - 1]} ${day}, ${year} ${hour}:${minute}:${second}`;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.diagramApp = new DiagramApp();
});
