// Global variables
let patientModal;
let currentPatientId = null;

// Initialize when document is ready
document.addEventListener('DOMContentLoaded', function() {
    patientModal = new bootstrap.Modal(document.getElementById('patientModal'));
    loadPatients();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    document.getElementById('searchPatient').addEventListener('input', function(e) {
        const searchTerm = e.target.value.toLowerCase();
        filterPatients(searchTerm);
    });
}

// Load patients from API
async function loadPatients() {
    try {
        const response = await fetch('/api/patients');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const patients = await response.json();
        displayPatients(patients);
    } catch (error) {
        console.error('Error loading patients:', error);
        showAlert('Error loading patients. Please try again.', 'danger');
    }
}

// Display patients in the table
function displayPatients(patients) {
    const tbody = document.getElementById('patientList');
    tbody.innerHTML = '';

    if (patients.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center">No patients found</td></tr>';
        return;
    }

    patients.forEach(patient => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${patient.name}</td>
            <td>${formatDate(patient.last_visit)}</td>
            <td>${formatDate(patient.next_visit)}</td>
            <td><span class="badge bg-${getRiskLevelColor(patient.risk_level)}">${patient.risk_level || 'N/A'}</span></td>
            <td>${patient.treatment_status || 'N/A'}</td>
            <td>
                <button class="btn btn-sm btn-info" onclick="viewPatientRisk(${patient.id})">View Risk</button>
                <button class="btn btn-sm btn-warning" onclick="editPatient(${patient.id})">Edit</button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

// Format date for display
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    try {
        return new Date(dateString).toLocaleDateString();
    } catch (e) {
        return 'Invalid Date';
    }
}

// Get risk level color for badge
function getRiskLevelColor(riskLevel) {
    switch (riskLevel?.toLowerCase()) {
        case 'high':
            return 'danger';
        case 'medium':
            return 'warning';
        case 'low':
            return 'success';
        default:
            return 'secondary';
    }
}

// Add new patient
function addNewPatient() {
    currentPatientId = null;
    document.getElementById('patientForm').reset();
    patientModal.show();
}

// Edit patient
async function editPatient(patientId) {
    try {
        const response = await fetch(`/api/patients/${patientId}`);
        if (!response.ok) {
            if (response.status === 404) {
                showAlert('Patient not found', 'warning');
                return;
            }
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const patient = await response.json();
        currentPatientId = patientId;
        populatePatientForm(patient);
        patientModal.show();
    } catch (error) {
        console.error('Error loading patient:', error);
        showAlert('Error loading patient data. Please try again.', 'danger');
    }
}

// Populate patient form
function populatePatientForm(patient) {
    document.getElementById('patientName').value = patient.name;
    document.getElementById('patientEmail').value = patient.email;
    document.getElementById('patientPhone').value = patient.phone || '';
    document.getElementById('lastVisit').value = patient.last_visit ? patient.last_visit.split('T')[0] : '';
    document.getElementById('nextVisit').value = patient.next_visit ? patient.next_visit.split('T')[0] : '';
    document.getElementById('treatmentStatus').value = patient.treatment_status || '';
    document.getElementById('patientNotes').value = patient.notes || '';
}

// Save patient
async function savePatient() {
    const patientData = {
        name: document.getElementById('patientName').value,
        email: document.getElementById('patientEmail').value,
        phone: document.getElementById('patientPhone').value,
        last_visit: document.getElementById('lastVisit').value,
        next_visit: document.getElementById('nextVisit').value,
        treatment_status: document.getElementById('treatmentStatus').value,
        notes: document.getElementById('patientNotes').value
    };

    try {
        const response = await fetch('/api/patients', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(patientData)
        });

        if (response.ok) {
            patientModal.hide();
            loadPatients();
            showAlert('Patient saved successfully', 'success');
        } else {
            const error = await response.json();
            throw new Error(error.error || 'Failed to save patient');
        }
    } catch (error) {
        console.error('Error saving patient:', error);
        showAlert(error.message || 'Error saving patient. Please try again.', 'danger');
    }
}

// View patient risk
async function viewPatientRisk(patientId) {
    try {
        const response = await fetch(`/api/patients/${patientId}/risk`);
        if (!response.ok) {
            if (response.status === 404) {
                showAlert('Patient not found', 'warning');
                return;
            }
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        showAlert(data.risk_analysis, 'info', true);
    } catch (error) {
        console.error('Error loading risk analysis:', error);
        showAlert('Error loading risk analysis. Please try again.', 'danger');
    }
}

// Filter patients based on search term
function filterPatients(searchTerm) {
    const rows = document.querySelectorAll('#patientList tr');
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(searchTerm) ? '' : 'none';
    });
}

// Show alert message
function showAlert(message, type = 'info', isLong = false) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    if (!isLong) {
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }
} 