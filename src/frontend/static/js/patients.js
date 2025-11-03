/**
 * Patients management functionality
 */

let allPatients = [];

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
        allPatients = await response.json();
        
        renderPatients(allPatients);
        
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('patients-content').classList.remove('hidden');
        
    } catch (error) {
        console.error('Error loading patients:', error);
        showToast('Failed to load patients', 'error');
    }
}

function renderPatients(patients) {
    const tbody = document.getElementById('patients-list');
    
    if (!patients || patients.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="7" class="px-6 py-12 text-center text-gray-500">
                    <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
                    </svg>
                    <p class="mt-4">No patients found</p>
                    <button onclick="showAddPatientModal()" class="mt-4 px-4 py-2 bg-cyan-600 text-white rounded-lg hover:bg-cyan-700">
                        Add First Patient
                    </button>
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = patients.map(patient => `
        <tr class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                    <div class="h-10 w-10 flex-shrink-0">
                        <div class="h-10 w-10 rounded-full bg-gradient-to-br from-cyan-400 to-blue-500 flex items-center justify-center text-white font-bold">
                            ${escapeHtml(patient.first_name.charAt(0))}${escapeHtml(patient.last_name.charAt(0))}
                        </div>
                    </div>
                    <div class="ml-4">
                        <div class="text-sm font-medium text-gray-900">
                            ${escapeHtml(patient.first_name)} ${escapeHtml(patient.last_name)}
                        </div>
                    </div>
                </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900">${patient.age || 'N/A'}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
                <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getGenderBadgeClass(patient.gender)}">
                    ${capitalizeFirst(patient.gender)}
                </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900">${escapeHtml(patient.national_id || 'N/A')}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-500">${escapeHtml(patient.village || 'N/A')}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-500">${escapeHtml(patient.phone_number || 'N/A')}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <a href="/analyze?patient_id=${patient.id}" class="text-cyan-600 hover:text-cyan-900 mr-3">
                    Analyze
                </a>
                <button onclick="viewPatient('${patient.id}')" class="text-blue-600 hover:text-blue-900">
                    View
                </button>
            </td>
        </tr>
    `).join('');
}

function getGenderBadgeClass(gender) {
    const classes = {
        'male': 'bg-blue-100 text-blue-800',
        'female': 'bg-pink-100 text-pink-800',
        'other': 'bg-purple-100 text-purple-800'
    };
    return classes[gender] || 'bg-gray-100 text-gray-800';
}

function capitalizeFirst(str) {
    if (!str) return '';
    return str.charAt(0).toUpperCase() + str.slice(1);
}

function handleSearch(event) {
    const query = event.target.value.toLowerCase().trim();
    
    if (!query) {
        renderPatients(allPatients);
        return;
    }
    
    const filtered = allPatients.filter(patient => {
        const fullName = `${patient.first_name} ${patient.last_name}`.toLowerCase();
        const nationalId = (patient.national_id || '').toLowerCase();
        return fullName.includes(query) || nationalId.includes(query);
    });
    
    renderPatients(filtered);
}

function showAddPatientModal() {
    document.getElementById('add-patient-modal').classList.remove('hidden');
}

function closeAddPatientModal() {
    document.getElementById('add-patient-modal').classList.add('hidden');
    document.getElementById('add-patient-form').reset();
}

document.getElementById('add-patient-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const data = {
        first_name: formData.get('first_name'),
        last_name: formData.get('last_name'),
        age: parseInt(formData.get('age')),
        gender: formData.get('gender'),
        national_id: formData.get('national_id') || null,
        village: formData.get('village') || null,
        phone_number: formData.get('phone_number') || null,
        district: 'Gaborone' // Default, should be selected from dropdown in production
    };
    
    try {
        const response = await authenticatedFetch('/api/patients', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            showToast('Patient added successfully', 'success');
            closeAddPatientModal();
            loadPatients();
        } else {
            const error = await response.json();
            showToast(error.detail || 'Failed to add patient', 'error');
        }
    } catch (error) {
        console.error('Error adding patient:', error);
        showToast('Failed to add patient', 'error');
    }
});

function viewPatient(patientId) {
    // In a real app, this would show a detailed view
    showToast('Patient details view - coming soon', 'info');
}

// Close modal when clicking outside
document.getElementById('add-patient-modal').addEventListener('click', (e) => {
    if (e.target.id === 'add-patient-modal') {
        closeAddPatientModal();
    }
});

