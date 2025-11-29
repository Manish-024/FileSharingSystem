// API Base URL
const API_BASE_URL = 'https://filesharingsystem-5rd1.onrender.com/api';

// Global state
let currentUser = '';
let currentTab = 'home';
let charts = {};

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

// Initialize application
async function initializeApp() {
    await loadStats();
    await loadFiles();
    setupEventListeners();
    
    // Load user from localStorage
    const savedUser = localStorage.getItem('userName');
    if (savedUser) {
        document.getElementById('uploader').value = savedUser;
        currentUser = savedUser;
    }
}

// Setup event listeners
function setupEventListeners() {
    const uploadForm = document.getElementById('uploadForm');
    uploadForm.addEventListener('submit', handleFileUpload);
    
    const uploaderInput = document.getElementById('uploader');
    uploaderInput.addEventListener('change', (e) => {
        currentUser = e.target.value;
        localStorage.setItem('userName', currentUser);
    });
}

// Tab switching
function switchTab(tabName) {
    currentTab = tabName;
    
    // Update tab buttons
    document.querySelectorAll('.nav-tab').forEach(tab => tab.classList.remove('active'));
    event.target.classList.add('active');
    
    // Update tab content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    
    const tabContent = document.getElementById(`${tabName}Tab`);
    if (tabContent) {
        tabContent.classList.add('active');
    }
    
    // Load tab-specific data
    if (tabName === 'analytics') {
        loadAnalytics();
    } else if (tabName === 'verification') {
        loadVerificationStats();
    } else if (tabName === 'blockchain') {
        loadBlockchain();
    }
}

// Toggle password field
function togglePassword() {
    const checkbox = document.getElementById('encryptFile');
    const passwordGroup = document.getElementById('passwordGroup');
    const passwordInput = document.getElementById('password');
    
    if (checkbox.checked) {
        passwordGroup.style.display = 'block';
        passwordInput.required = true;
    } else {
        passwordGroup.style.display = 'none';
        passwordInput.required = false;
        passwordInput.value = '';
    }
}

// Load blockchain statistics
async function loadStats() {
    try {
        const [statsResponse, verifyStatsResponse] = await Promise.all([
            fetch(`${API_BASE_URL}/stats`),
            fetch(`${API_BASE_URL}/verification/stats`)
        ]);
        
        const stats = await statsResponse.json();
        const verifyStats = await verifyStatsResponse.json();
        
        document.getElementById('totalBlocks').textContent = stats.total_blocks;
        document.getElementById('totalUploads').textContent = stats.total_uploads;
        document.getElementById('totalDownloads').textContent = stats.total_downloads;
        document.getElementById('encryptedFiles').textContent = stats.encrypted_files || 0;
        document.getElementById('verifiedFiles').textContent = verifyStats.verified_files || 0;
        
        const chainValidElement = document.getElementById('chainValid');
        if (stats.is_valid) {
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
    const encryptCheckbox = document.getElementById('encryptFile');
    const passwordInput = document.getElementById('password');
    const isPublicCheckbox = document.getElementById('isPublic');
    const maxDownloadsInput = document.getElementById('maxDownloads');
    const expirationInput = document.getElementById('expirationHours');
    
    const file = fileInput.files[0];
    const uploader = uploaderInput.value;
    
    if (!file) {
        showStatus('Please select a file', 'error');
        return;
    }
    
    if (encryptCheckbox.checked && !passwordInput.value) {
        showStatus('Please enter a password for encryption', 'error');
        return;
    }
    
    formData.append('file', file);
    formData.append('uploader', uploader);
    formData.append('encrypt', encryptCheckbox.checked);
    formData.append('password', passwordInput.value);
    formData.append('is_public', isPublicCheckbox.checked);
    
    if (maxDownloadsInput.value) {
        formData.append('max_downloads', maxDownloadsInput.value);
    }
    
    if (expirationInput.value) {
        formData.append('expiration_hours', expirationInput.value);
    }
    
    // Show loading status
    showStatus('⏳ Uploading file and mining block...', 'info');
    
    try {
        const response = await fetch(`${API_BASE_URL}/upload`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            let message = `✓ File uploaded successfully! Block #${data.block.index} mined.`;
            if (data.is_encrypted) {
                message += ' 🔒 File is encrypted.';
            }
            showStatus(message, 'success');
            
            // Reset form
            event.target.reset();
            document.getElementById('passwordGroup').style.display = 'none';
            document.getElementById('isPublic').checked = true;
            
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
        
        // Add verification data to each file
        const filesWithVerification = await Promise.all(
            data.files.map(async (file) => {
                try {
                    const verifyResponse = await fetch(`${API_BASE_URL}/verification/${file.file_hash}`);
                    const verifyData = await verifyResponse.json();
                    file.verification = verifyData;
                } catch (e) {
                    file.verification = { status: 'unverified', authenticity_score: 0 };
                }
                return file;
            })
        );
        
        filesList.innerHTML = filesWithVerification.map(file => createFileItem(file)).join('');
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
    
    // Verification badge
    let verificationBadge = '';
    const verification = file.verification || {};
    if (verification.status === 'verified') {
        verificationBadge = '<span class="badge verified">✓ Verified</span>';
    } else if (verification.status === 'disputed') {
        verificationBadge = '<span class="badge disputed">⚠ Disputed</span>';
    } else if (verification.status === 'suspicious') {
        verificationBadge = '<span class="badge suspicious">✗ Suspicious</span>';
    }
    
    // Encryption badge
    const encryptionBadge = file.is_encrypted 
        ? '<span class="badge encrypted">🔒 Encrypted</span>' 
        : '';
    
    // Version badge
    const versionBadge = file.version > 1 
        ? `<span class="badge version">v${file.version}</span>` 
        : '';
    
    return `
        <div class="file-item">
            <div class="file-header">
                <div class="file-name">📄 ${file.file_name}</div>
                <div class="file-badges">
                    ${encryptionBadge}
                    ${verificationBadge}
                    ${versionBadge}
                </div>
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
            <div class="file-actions">
                <button class="btn btn-download" onclick="initiateDownload('${file.file_hash}', '${file.file_name}', ${file.is_encrypted})">
                    ⬇️ Download
                </button>
                <button class="btn btn-secondary" onclick="showFileDetails('${file.file_hash}')">
                    ℹ️ Details
                </button>
                <button class="btn btn-secondary" onclick="showVerifyModal('${file.file_hash}')">
                    ✓ Verify
                </button>
            </div>
        </div>
    `;
}

// Initiate download
function initiateDownload(fileHash, fileName, isEncrypted) {
    if (isEncrypted) {
        showDownloadModal(fileHash, fileName);
    } else {
        downloadFile(fileHash, fileName, '');
    }
}

// Show download modal
function showDownloadModal(fileHash, fileName) {
    const modal = document.getElementById('downloadModal');
    const modalBody = document.getElementById('downloadModalBody');
    
    modalBody.innerHTML = `
        <p><strong>File:</strong> ${fileName}</p>
        <p>🔒 This file is encrypted. Please enter the password to download.</p>
        <div class="form-group">
            <label for="downloadPassword">Password:</label>
            <input type="password" id="downloadPassword" placeholder="Enter password" required>
        </div>
        <button class="btn btn-primary" onclick="downloadEncryptedFile('${fileHash}', '${fileName}')">
            Download
        </button>
    `;
    
    modal.style.display = 'block';
}

// Close download modal
function closeDownloadModal() {
    const modal = document.getElementById('downloadModal');
    modal.style.display = 'none';
}

// Download encrypted file
async function downloadEncryptedFile(fileHash, fileName) {
    const password = document.getElementById('downloadPassword').value;
    
    if (!password) {
        alert('Please enter a password');
        return;
    }
    
    await downloadFile(fileHash, fileName, password);
    closeDownloadModal();
}

// Download file
async function downloadFile(fileHash, fileName, password) {
    const uploader = currentUser || document.getElementById('uploader').value || 'Anonymous';
    
    try {
        const response = await fetch(`${API_BASE_URL}/download/${fileHash}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                downloader: uploader,
                password: password
            })
        });
        
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

// Show file details modal
async function showFileDetails(fileHash) {
    try {
        const response = await fetch(`${API_BASE_URL}/file/${fileHash}`);
        const file = await response.json();
        
        const modal = document.getElementById('fileModal');
        const modalBody = document.getElementById('modalBody');
        
        const verification = file.verification || {};
        const contract = file.contract || {};
        
        modalBody.innerHTML = `
            <h2>📄 File Details</h2>
            <div class="file-detail">
                <strong>Name:</strong> ${file.file_name}
            </div>
            <div class="file-detail">
                <strong>Hash:</strong> <code>${file.file_hash}</code>
            </div>
            <div class="file-detail">
                <strong>Size:</strong> ${formatFileSize(file.file_size)}
            </div>
            <div class="file-detail">
                <strong>Uploader:</strong> ${file.uploader}
            </div>
            <div class="file-detail">
                <strong>Encrypted:</strong> ${file.is_encrypted ? '🔒 Yes' : 'No'}
            </div>
            <div class="file-detail">
                <strong>Version:</strong> v${file.version || 1}
            </div>
            <hr>
            <h3>🔍 Verification Status</h3>
            <div class="file-detail">
                <strong>Status:</strong> <span class="badge ${verification.status}">${verification.status || 'unverified'}</span>
            </div>
            <div class="file-detail">
                <strong>Authenticity Score:</strong> ${verification.authenticity_score || 0}%
            </div>
            <div class="file-detail">
                <strong>Total Votes:</strong> ${verification.total_votes || 0} (👍 ${verification.positive_votes || 0} / 👎 ${verification.negative_votes || 0})
            </div>
            ${contract.total_accesses ? `
                <hr>
                <h3>📋 Smart Contract</h3>
                <div class="file-detail">
                    <strong>Access Type:</strong> ${contract.is_public ? 'Public' : 'Private'}
                </div>
                <div class="file-detail">
                    <strong>Total Accesses:</strong> ${contract.total_accesses}
                </div>
                <div class="file-detail">
                    <strong>Successful Downloads:</strong> ${contract.successful_downloads}
                </div>
            ` : ''}
        `;
        
        modal.style.display = 'block';
    } catch (error) {
        console.error('Error loading file details:', error);
        alert('Error loading file details');
    }
}

// Close modal
function closeModal() {
    const modal = document.getElementById('fileModal');
    modal.style.display = 'none';
}

// Show verify modal
function showVerifyModal(fileHash) {
    const modal = document.getElementById('fileModal');
    const modalBody = document.getElementById('modalBody');
    
    modalBody.innerHTML = `
        <h2>✓ Verify File</h2>
        <p>Help the community by verifying if this file is authentic and safe.</p>
        <div class="form-group">
            <label for="verifyComment">Comment (optional):</label>
            <textarea id="verifyComment" rows="3" style="width: 100%; padding: 10px; border-radius: 8px; border: 2px solid #e0e0e0;"></textarea>
        </div>
        <div class="vote-buttons">
            <button class="btn-vote-authentic" onclick="submitVerification('${fileHash}', true)">
                ✓ Authentic
            </button>
            <button class="btn-vote-suspicious" onclick="submitVerification('${fileHash}', false)">
                ✗ Suspicious
            </button>
        </div>
    `;
    
    modal.style.display = 'block';
}

// Submit verification
async function submitVerification(fileHash, isAuthentic) {
    const user = currentUser || document.getElementById('uploader').value || 'Anonymous';
    const comment = document.getElementById('verifyComment').value;
    
    try {
        const response = await fetch(`${API_BASE_URL}/verify/${fileHash}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user: user,
                is_authentic: isAuthentic,
                comment: comment
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert(`✓ Verification submitted! Score: ${data.verification.authenticity_score}%`);
            closeModal();
            await loadFiles();
            await loadStats();
        } else {
            alert(`Error: ${data.error}`);
        }
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}

// Search files
async function searchFiles() {
    const query = document.getElementById('searchQuery').value;
    const fileType = document.getElementById('fileTypeFilter').value;
    const encryptedOnly = document.getElementById('encryptedOnly').checked;
    
    try {
        let url = `${API_BASE_URL}/files/search?q=${encodeURIComponent(query)}`;
        if (fileType) url += `&type=${fileType}`;
        if (encryptedOnly) url += `&encrypted=true`;
        
        const response = await fetch(url);
        const data = await response.json();
        
        const filesList = document.getElementById('filesList');
        
        if (data.files.length === 0) {
            filesList.innerHTML = `
                <div class="empty-state">
                    <p>No files match your search criteria.</p>
                </div>
            `;
        } else {
            filesList.innerHTML = data.files.map(file => createFileItem(file)).join('');
        }
    } catch (error) {
        console.error('Error searching files:', error);
    }
}

// Refresh files list
async function refreshFiles() {
    await loadStats();
    await loadFiles();
    showStatus('✓ Files refreshed!', 'success');
}

// Load analytics
async function loadAnalytics() {
    try {
        const response = await fetch(`${API_BASE_URL}/analytics`);
        const data = await response.json();
        
        // Activity Timeline Chart
        createActivityChart(data.activity_timeline);
        
        // File Type Distribution
        createFileTypeChart(data.file_type_distribution);
        
        // Top Uploaders
        createUploadersChart(data.top_uploaders);
        
        // Hourly Activity
        createHourlyChart(data.hourly_activity);
        
    } catch (error) {
        console.error('Error loading analytics:', error);
    }
}

// Create activity timeline chart
function createActivityChart(data) {
    const ctx = document.getElementById('activityChart');
    
    if (charts.activity) {
        charts.activity.destroy();
    }
    
    charts.activity = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.map(d => d.date),
            datasets: [{
                label: 'Uploads',
                data: data.map(d => d.uploads),
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                tension: 0.4
            }, {
                label: 'Downloads',
                data: data.map(d => d.downloads),
                borderColor: '#10b981',
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true
                }
            }
        }
    });
}

// Create file type chart
function createFileTypeChart(data) {
    const ctx = document.getElementById('fileTypeChart');
    
    if (charts.fileType) {
        charts.fileType.destroy();
    }
    
    charts.fileType = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: data.map(d => d.type.toUpperCase()),
            datasets: [{
                data: data.map(d => d.count),
                backgroundColor: [
                    '#667eea', '#764ba2', '#10b981', '#f59e0b',
                    '#ef4444', '#8b5cf6', '#ec4899', '#06b6d4'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true
        }
    });
}

// Create uploaders chart
function createUploadersChart(data) {
    const ctx = document.getElementById('uploadersChart');
    
    if (charts.uploaders) {
        charts.uploaders.destroy();
    }
    
    charts.uploaders = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(d => d.user),
            datasets: [{
                label: 'Uploads',
                data: data.map(d => d.count),
                backgroundColor: '#667eea'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            indexAxis: 'y'
        }
    });
}

// Create hourly chart
function createHourlyChart(data) {
    const ctx = document.getElementById('hourlyChart');
    
    if (charts.hourly) {
        charts.hourly.destroy();
    }
    
    charts.hourly = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(d => `${d.hour}:00`),
            datasets: [{
                label: 'Activity',
                data: data.map(d => d.uploads + d.downloads),
                backgroundColor: '#667eea'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true
        }
    });
}

// Load verification stats
async function loadVerificationStats() {
    try {
        const [statsResponse, verifiersResponse] = await Promise.all([
            fetch(`${API_BASE_URL}/verification/stats`),
            fetch(`${API_BASE_URL}/verification/top-verifiers?limit=10`)
        ]);
        
        const stats = await statsResponse.json();
        const verifiers = await verifiersResponse.json();
        
        document.getElementById('verifiedFilesCount').textContent = stats.verified_files || 0;
        document.getElementById('totalVotes').textContent = stats.total_votes || 0;
        document.getElementById('avgAuthenticity').textContent = `${stats.average_authenticity || 0}%`;
        
        // Display top verifiers
        const verifiersList = document.getElementById('topVerifiers');
        if (verifiers.verifiers && verifiers.verifiers.length > 0) {
            verifiersList.innerHTML = verifiers.verifiers.map(v => `
                <div class="verifier-item">
                    <div class="verifier-rank">#${v.rank}</div>
                    <div class="verifier-name">${v.user}</div>
                    <div class="verifier-reputation">${v.reputation.toFixed(2)}</div>
                </div>
            `).join('');
        } else {
            verifiersList.innerHTML = '<p class="empty-state">No verifiers yet.</p>';
        }
    } catch (error) {
        console.error('Error loading verification stats:', error);
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
        const encrypted = block.data.is_encrypted ? ' 🔒' : '';
        const version = block.data.version > 1 ? ` (v${block.data.version})` : '';
        dataPreview = `
            <strong>File:</strong> ${block.data.file_name}${encrypted}${version}<br>
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

// Close modal on outside click
window.onclick = function(event) {
    const fileModal = document.getElementById('fileModal');
    const downloadModal = document.getElementById('downloadModal');
    if (event.target == fileModal) {
        fileModal.style.display = 'none';
    }
    if (event.target == downloadModal) {
        downloadModal.style.display = 'none';
    }
}
