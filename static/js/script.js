// File upload handling
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const notesText = document.getElementById('notesText');
const previewSection = document.getElementById('previewSection');
const mcqSection = document.getElementById('mcqSection');
const loadingSpinner = document.getElementById('loadingSpinner');
const errorMessage = document.getElementById('errorMessage');
const mcqContainer = document.getElementById('mcqContainer');

// Drag and drop events
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileUpload(files[0]);
    }
});

// File input change event
fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileUpload(e.target.files[0]);
    }
});

// Handle file upload
async function handleFileUpload(file) {
    // Validate file
    const allowedFormats = ['text/plain', 'application/pdf', 'image/png', 'image/jpeg'];
    if (!allowedFormats.includes(file.type) && !file.name.endsWith('.txt') && !file.name.endsWith('.pdf')) {
        showError('Invalid file format. Please upload TXT, PDF, or image files.');
        return;
    }

    if (file.size > 50 * 1024 * 1024) {
        showError('File size exceeds 50MB limit.');
        return;
    }

    showLoading(true);
    clearError();

    try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Upload failed');
        }

        const data = await response.json();
        notesText.value = data.text;
        previewSection.style.display = 'block';
        mcqSection.style.display = 'none';
        window.scrollTo({ top: previewSection.offsetTop, behavior: 'smooth' });
    } catch (error) {
        showError('Error uploading file: ' + error.message);
    } finally {
        showLoading(false);
    }
}

// Generate MCQs
async function generateMCQs() {
    const text = notesText.value.trim();
    const numQuestions = parseInt(document.getElementById('numQuestions').value);

    if (!text) {
        showError('Please extract text from a file first.');
        return;
    }

    if (numQuestions < 1 || numQuestions > 20) {
        showError('Number of questions must be between 1 and 20.');
        return;
    }

    showLoading(true);
    clearError();

    try {
        const response = await fetch('/api/generate-mcq', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: text,
                num_questions: numQuestions
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'MCQ generation failed');
        }

        const data = await response.json();
        displayMCQs(data.mcqs);
        mcqSection.style.display = 'block';
        window.scrollTo({ top: mcqSection.offsetTop, behavior: 'smooth' });
    } catch (error) {
        showError('Error generating MCQs: ' + error.message);
    } finally {
        showLoading(false);
    }
}

// Display MCQs
function displayMCQs(mcqs) {
    mcqContainer.innerHTML = '';

    mcqs.forEach((mcq, index) => {
        const mcqCard = document.createElement('div');
        mcqCard.className = 'mcq-card';
        mcqCard.innerHTML = `
            <div class="mcq-number">Question ${index + 1}</div>
            <div class="mcq-question">${mcq.question}</div>
            <div class="mcq-options">
                ${Object.entries(mcq.options).map(([key, value]) => `
                    <div class="mcq-option ${mcq.correct_answer === key ? 'correct' : ''}">
                        <span class="mcq-option-letter">${key}</span>
                        <span class="mcq-option-text">
                            ${value}
                            ${mcq.correct_answer === key ? '<span class="correct-badge">Correct Answer</span>' : ''}
                        </span>
                    </div>
                `).join('')}
            </div>
            <div class="mcq-explanation">
                <strong>Explanation:</strong> ${mcq.explanation}
            </div>
        `;
        mcqContainer.appendChild(mcqCard);
    });
}

// Download quiz
async function downloadQuiz(format) {
    const mcqs = extractMCQsFromDisplay();
    
    if (mcqs.length === 0) {
        showError('No MCQs to download.');
        return;
    }

    showLoading(true);

    try {
        const response = await fetch('/api/download-quiz', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                mcqs: mcqs,
                format: format
            })
        });

        if (!response.ok) {
            throw new Error('Download failed');
        }

        // For now, show a message
        showSuccess(`Download feature for ${format} format coming soon!`);
    } catch (error) {
        showError('Error downloading quiz: ' + error.message);
    } finally {
        showLoading(false);
    }
}

// Extract MCQs from display
function extractMCQsFromDisplay() {
    // This would extract MCQs from the displayed cards
    // For now, returning empty array - implement based on your needs
    return [];
}

// Reset all
function resetAll() {
    notesText.value = '';
    mcqContainer.innerHTML = '';
    previewSection.style.display = 'none';
    mcqSection.style.display = 'none';
    fileInput.value = '';
    clearError();
    window.scrollTo({ top: uploadArea.offsetTop, behavior: 'smooth' });
}

// UI Helpers
function showLoading(show) {
    loadingSpinner.style.display = show ? 'flex' : 'none';
}

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
}

function clearError() {
    errorMessage.style.display = 'none';
    errorMessage.textContent = '';
}

function showSuccess(message) {
    // You can implement a success message display here
    alert(message);
}