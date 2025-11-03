/**
 * Dashboard functionality for Introspect
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

async function loadDashboard() {
    try {
        const response = await authenticatedFetch('/api/dashboard?days=30');
        const data = await response.json();
        
        // Update summary cards
        document.getElementById('total-tests').textContent = data.summary.total_tests.toLocaleString();
        document.getElementById('positive-cases').textContent = data.summary.total_positive.toLocaleString();
        document.getElementById('negative-cases').textContent = data.summary.total_negative.toLocaleString();
        document.getElementById('positivity-rate').textContent = data.summary.overall_positivity_rate.toFixed(1) + '%';
        
        // Update district statistics
        renderDistrictStats(data.district_stats);
        
        // Update recent count
        document.getElementById('recent-count').textContent = `${data.recent_tests} tests in last 7 days`;
        
        // Show content, hide loading
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('dashboard-content').classList.remove('hidden');
        
    } catch (error) {
        console.error('Error loading dashboard:', error);
        showToast('Failed to load dashboard data', 'error');
        document.getElementById('loading').innerHTML = `
            <div class="text-center py-12">
                <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
                </svg>
                <p class="mt-4 text-gray-600">Failed to load dashboard data</p>
                <button onclick="loadDashboard()" class="mt-4 px-4 py-2 bg-cyan-600 text-white rounded-lg hover:bg-cyan-700">
                    Retry
                </button>
            </div>
        `;
    }
}

function renderDistrictStats(stats) {
    const tbody = document.getElementById('district-stats');
    
    if (!stats || stats.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6" class="px-6 py-4 text-center text-gray-500">
                    No data available
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = stats.map(stat => `
        <tr class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-medium text-gray-900">${escapeHtml(stat.district)}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900">${stat.total_tests.toLocaleString()}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-red-600 font-medium">${stat.positive_cases.toLocaleString()}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-green-600 font-medium">${stat.negative_cases.toLocaleString()}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                    <span class="text-sm font-medium ${getPositivityRateColor(stat.positivity_rate)}">
                        ${stat.positivity_rate.toFixed(1)}%
                    </span>
                    <div class="ml-2 w-16 bg-gray-200 rounded-full h-2">
                        <div class="bg-amber-500 h-2 rounded-full" style="width: ${Math.min(stat.positivity_rate, 100)}%"></div>
                    </div>
                </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-500">${stat.clinics_count}</div>
            </td>
        </tr>
    `).join('');
}

function getPositivityRateColor(rate) {
    if (rate < 5) return 'text-green-600';
    if (rate < 15) return 'text-amber-600';
    return 'text-red-600';
}

function getResultBadgeClass(result) {
    const classes = {
        'positive': 'bg-red-100 text-red-800',
        'negative': 'bg-green-100 text-green-800',
        'inconclusive': 'bg-amber-100 text-amber-800'
    };
    return classes[result] || 'bg-gray-100 text-gray-800';
}

function getResultIcon(result) {
    const icons = {
        'positive': `<svg class="h-5 w-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
        </svg>`,
        'negative': `<svg class="h-5 w-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>`,
        'inconclusive': `<svg class="h-5 w-5 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>`
    };
    return icons[result] || '';
}

// Auto-refresh dashboard every 5 minutes
setInterval(() => {
    loadDashboard();
}, 5 * 60 * 1000);

