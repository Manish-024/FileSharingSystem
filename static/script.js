// API Base URL
const API_BASE_URL = 'http://localhost:5001/api';

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

// Initialize application
async function initializeApp() {
    await loadStats();
    await loadFiles();
    setupEventListeners();
}

// Setup event listeners
function setupEventListeners() {
    const uploadForm = document.getElementById('uploadForm');
    uploadForm.addEventListener('submit', handleFileUpload);
}

// Load blockchain statistics
async function loadStats() {
    try {
        const response = await fetch(`${API_BASE_URL}/stats`);
        const data = await response.json();
        
        document.getElementById('totalBlocks').textContent = data.total_blocks;
        document.getElementById('totalUploads').textContent = data.total_uploads;
        document.getElementById('totalDownloads').textContent = data.total_downloads;
        
        const chainValidElement = document.getElementById('chainValid');
        if (data.is_valid) {
            chainValidElement.innerHTML = '<span class="status-indicator">✓</span>';
        } else {
            chainValidElement.innerHTML = '<span class="status-indicator" style="color: #ef4444;">✗</span>';
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Handle file upload
async function handleFileUpload(event) {
    event.preventDefault();
    
    const formData = new FormData();
    const fileInput = document.getElementById('fileInput');
    const uploaderInput = document.getElementById('uploader');
    const statusDiv = document.getElementById('uploadStatus');
    
    const file = fileInput.files[0];
    const uploader = uploaderInput.value;
    
    if (!file) {
        showStatus('Please select a file', 'error');
        return;
    }
    
    formData.append('file', file);
    formData.append('uploader', uploader);
    
    // Show loading status
    showStatus('Uploading file and mining block...', 'info');
    
    try {
        const response = await fetch(`${API_BASE_URL}/upload`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showStatus(`✓ File uploaded successfully! Block #${data.block.index} mined.`, 'success');
            
            // Reset form
            event.target.reset();
            
            // Refresh data
            await loadStats();
            await loadFiles();
        } else {
            showStatus(`✗ Error: ${data.error}`, 'error');
        }
    } catch (error) {
        showStatus(`✗ Error: ${error.message}`, 'error');
    }
}

// Show status message
function showStatus(message, type) {
    const statusDiv = document.getElementById('uploadStatus');
    statusDiv.textContent = message;
    statusDiv.className = `status-message ${type}`;
    
    // Auto-hide after 5 seconds for success messages
    if (type === 'success') {
        setTimeout(() => {
            statusDiv.style.display = 'none';
        }, 5000);
    }
}

// Load files from blockchain
async function loadFiles() {
    const filesList = document.getElementById('filesList');
    
    try {
        const response = await fetch(`${API_BASE_URL}/files`);
        const data = await response.json();
        
        if (data.files.length === 0) {
            filesList.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">📭</div>
                    <p>No files uploaded yet. Be the first to share!</p>
                </div>
            `;
            return;
        }
        
        // Sort files by timestamp (most recent first)
        data.files.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
        
        filesList.innerHTML = data.files.map(file => createFileItem(file)).join('');
    } catch (error) {
        console.error('Error loading files:', error);
        filesList.innerHTML = `
            <div class="empty-state">
                <p>Error loading files. Please try again.</p>
            </div>
        `;
    }
}

// Create file item HTML
function createFileItem(file) {
    const fileSize = formatFileSize(file.file_size);
    const timestamp = formatTimestamp(file.timestamp);
    const shortHash = file.file_hash.substring(0, 16) + '...';
    
    return `
        <div class="file-item">
            <div class="file-header">
                <div class="file-name">📄 ${file.file_name}</div>
                <button class="btn btn-download" onclick="downloadFile('${file.file_hash}', '${file.file_name}')">
                    ⬇️ Download
                </button>
            </div>
            <div class="file-details">
                <div class="file-detail">
                    <div class="file-detail-label">Uploader</div>
                    <div class="file-detail-value">${file.uploader}</div>
                </div>
                <div class="file-detail">
                    <div class="file-detail-label">File Size</div>
                    <div class="file-detail-value">${fileSize}</div>
                </div>
                <div class="file-detail">
                    <div class="file-detail-label">Upload Time</div>
                    <div class="file-detail-value">${timestamp}</div>
                </div>
                <div class="file-detail">
                    <div class="file-detail-label">Block #</div>
                    <div class="file-detail-value">${file.block_index}</div>
                </div>
            </div>
            <div class="file-detail">
                <div class="file-detail-label">File Hash (SHA-256)</div>
                <div class="file-detail-value" title="${file.file_hash}">${shortHash}</div>
            </div>
        </div>
    `;
}

// Download file
async function downloadFile(fileHash, fileName) {
    const uploader = document.getElementById('uploader').value || 'Anonymous';
    
    try {
        const response = await fetch(`${API_BASE_URL}/download/${fileHash}?downloader=${uploader}`);
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = fileName;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            // Refresh stats to show new download
            await loadStats();
            
            showStatus(`✓ File downloaded successfully!`, 'success');
        } else {
            const data = await response.json();
            showStatus(`✗ Error: ${data.error}`, 'error');
        }
    } catch (error) {
        showStatus(`✗ Error: ${error.message}`, 'error');
    }
}

// Refresh files list
async function refreshFiles() {
    await loadStats();
    await loadFiles();
    showStatus('✓ Files refreshed!', 'success');
}

// Toggle blockchain explorer
async function toggleBlockchain() {
    const container = document.getElementById('blockchainContainer');
    const toggleText = document.getElementById('blockchainToggleText');
    
    if (container.style.display === 'none') {
        container.style.display = 'block';
        toggleText.textContent = 'Hide Blockchain';
        await loadBlockchain();
    } else {
        container.style.display = 'none';
        toggleText.textContent = 'Show Blockchain';
    }
}

// Load blockchain
async function loadBlockchain() {
    const blockchainList = document.getElementById('blockchainList');
    
    try {
        const response = await fetch(`${API_BASE_URL}/blockchain`);
        const data = await response.json();
        
        // Reverse to show newest blocks first
        const chain = [...data.chain].reverse();
        
        blockchainList.innerHTML = chain.map(block => createBlockItem(block)).join('');
    } catch (error) {
        console.error('Error loading blockchain:', error);
        blockchainList.innerHTML = `
            <div class="empty-state">
                <p>Error loading blockchain. Please try again.</p>
            </div>
        `;
    }
}

// Create block item HTML
function createBlockItem(block) {
    const timestamp = formatTimestamp(new Date(block.timestamp * 1000).toISOString());
    const blockType = block.data.type || 'unknown';
    const blockTypeClass = blockType.replace('_', '-');
    
    let dataPreview = '';
    if (blockType === 'file_upload') {
        dataPreview = `
            <strong>File:</strong> ${block.data.file_name}<br>
            <strong>Uploader:</strong> ${block.data.uploader}<br>
            <strong>Size:</strong> ${formatFileSize(block.data.file_size)}<br>
            <strong>Hash:</strong> ${block.data.file_hash.substring(0, 32)}...
        `;
    } else if (blockType === 'file_download') {
        dataPreview = `
            <strong>File:</strong> ${block.data.file_name}<br>
            <strong>Downloader:</strong> ${block.data.downloader}
        `;
    } else if (blockType === 'genesis') {
        dataPreview = `<strong>Message:</strong> ${block.data.message}`;
    }
    
    return `
        <div class="block-item">
            <div class="block-header">
                <div class="block-index">Block #${block.index}</div>
                <div class="block-type ${blockTypeClass}">${blockType}</div>
            </div>
            <div class="block-details">
                <strong>Timestamp:</strong> ${timestamp}<br>
                <strong>Nonce:</strong> ${block.nonce}<br>
                ${dataPreview}
                <div class="block-hash">
                    <strong>Hash:</strong> ${block.hash}<br>
                    <strong>Previous Hash:</strong> ${block.previous_hash}
                </div>
            </div>
        </div>
    `;
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
}

// Format timestamp
function formatTimestamp(isoString) {
    const date = new Date(isoString);
    const options = {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return date.toLocaleDateString('en-US', options);
}
