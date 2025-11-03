/**
 * Blood smear analysis functionality
 */

async function loadUserInfo() {
    try {
        const response = await authenticatedFetch('/users/me');
        const user = await response.json();
        document.getElementById('user-name').textContent = `${user.first_name} ${user.last_name}`;
    } catch (error) {
        console.error('Error loading user info:', error);
    }
}

async function loadPatients() {
    try {
        const response = await authenticatedFetch('/api/patients');
        const patients = await response.json();
        
        const select = document.getElementById('patient-select');
        
        if (patients.length === 0) {
            select.innerHTML = '<option value="">No patients found - Add a patient first</option>';
            return;
        }
        
        select.innerHTML = '<option value="">Select a patient...</option>' +
            patients.map(p => `
                <option value="${p.id}">
                    ${escapeHtml(p.first_name)} ${escapeHtml(p.last_name)} - ${p.age || 'N/A'} yrs - ${escapeHtml(p.national_id || 'No ID')}
                </option>
            `).join('');
        
        // Pre-select if patient_id in URL
        const urlParams = new URLSearchParams(window.location.search);
        const patientId = urlParams.get('patient_id');
        if (patientId) {
            select.value = patientId;
        }
        
    } catch (error) {
        console.error('Error loading patients:', error);
        showToast('Failed to load patients', 'error');
    }
}

function previewImage(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    // Validate file size (20MB)
    if (file.size > 20 * 1024 * 1024) {
        showToast('File size must be less than 20MB', 'error');
        event.target.value = '';
        return;
    }
    
    // Validate file type
    if (!file.type.startsWith('image/')) {
        showToast('Please select an image file', 'error');
        event.target.value = '';
        return;
    }
    
    const reader = new FileReader();
    reader.onload = function(e) {
        const preview = document.getElementById('image-preview');
        const container = document.getElementById('preview-container');
        const icon = document.getElementById('upload-icon');
        
        preview.src = e.target.result;
        container.classList.remove('hidden');
        icon.classList.add('hidden');
    };
    reader.readAsDataURL(file);
}

document.getElementById('analyze-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const patientId = formData.get('patient_id');
    
    if (!patientId) {
        showToast('Please select a patient', 'error');
        return;
    }
    
    const imageFile = formData.get('image');
    if (!imageFile || imageFile.size === 0) {
        showToast('Please select an image', 'error');
        return;
    }
    
    // Show loading state
    const submitBtn = document.getElementById('submit-btn');
    const submitText = document.getElementById('submit-text');
    const submitLoading = document.getElementById('submit-loading');
    
    submitBtn.disabled = true;
    submitText.classList.add('hidden');
    submitLoading.classList.remove('hidden');
    
    try {
        // Note: We need to get clinic_id - for now using a placeholder
        // In production, this should come from the user's profile or be selected
        const userResponse = await authenticatedFetch('/users/me');
        const user = await userResponse.json();
        
        // Create form data for multipart upload
        const uploadData = new FormData();
        uploadData.append('image', imageFile);
        uploadData.append('patient_id', patientId);
        uploadData.append('clinic_id', user.clinic_id || '00000000-0000-0000-0000-000000000000'); // Placeholder
        
        const symptoms = formData.get('symptoms');
        if (symptoms) {
            uploadData.append('symptoms', symptoms);
        }
        
        const notes = formData.get('notes');
        if (notes) {
            uploadData.append('notes', notes);
        }
        
        const response = await authenticatedFetch('/api/results/analyze', {
            method: 'POST',
            body: uploadData
            // Don't set Content-Type header - browser will set it with boundary
        });
        
        if (response.ok) {
            const result = await response.json();
            displayResult(result);
            showToast('Analysis complete!', 'success');
        } else {
            const error = await response.json();
            showToast(error.detail || 'Analysis failed', 'error');
        }
        
    } catch (error) {
        console.error('Error analyzing image:', error);
        showToast('Failed to analyze image', 'error');
    } finally {
        // Reset button state
        submitBtn.disabled = false;
        submitText.classList.remove('hidden');
        submitLoading.classList.add('hidden');
    }
});

function displayResult(result) {
    const container = document.getElementById('result-container');
    const content = document.getElementById('result-content');
    
    const resultClass = getResultClass(result.result);
    const resultIcon = getResultIcon(result.result);
    
    content.innerHTML = `
        <div class="flex items-center justify-center p-6 ${resultClass} rounded-xl">
            ${resultIcon}
            <div class="ml-4">
                <h3 class="text-2xl font-bold capitalize">${result.result}</h3>
                <p class="text-sm mt-1">Confidence: ${(result.confidence_score * 100).toFixed(1)}%</p>
            </div>
        </div>
        
        <div class="grid grid-cols-2 gap-4 mt-6">
            <div class="bg-gray-50 rounded-lg p-4">
                <p class="text-sm text-gray-600">Processing Time</p>
                <p class="text-lg font-semibold text-gray-900">${result.processing_time_ms.toFixed(0)} ms</p>
            </div>
            <div class="bg-gray-50 rounded-lg p-4">
                <p class="text-sm text-gray-600">Test Result ID</p>
                <p class="text-xs font-mono text-gray-900">${result.test_result_id.substring(0, 8)}...</p>
            </div>
        </div>
        
        <div class="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <p class="text-sm text-blue-800">
                <strong>Note:</strong> This is a placeholder AI model for demonstration. 
                In production, replace with a trained malaria detection model.
            </p>
        </div>
    `;
    
    container.classList.remove('hidden');
    container.scrollIntoView({ behavior: 'smooth' });
}

function getResultClass(result) {
    const classes = {
        'positive': 'bg-red-50 border-2 border-red-200',
        'negative': 'bg-green-50 border-2 border-green-200',
        'inconclusive': 'bg-amber-50 border-2 border-amber-200'
    };
    return classes[result] || 'bg-gray-50 border-2 border-gray-200';
}

function getResultIcon(result) {
    const icons = {
        'positive': `
            <svg class="h-16 w-16 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
            </svg>
        `,
        'negative': `
            <svg class="h-16 w-16 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
        `,
        'inconclusive': `
            <svg class="h-16 w-16 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
        `
    };
    return icons[result] || '';
}

function resetForm() {
    document.getElementById('analyze-form').reset();
    document.getElementById('result-container').classList.add('hidden');
    document.getElementById('preview-container').classList.add('hidden');
    document.getElementById('upload-icon').classList.remove('hidden');
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

