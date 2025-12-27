// ==========================================
// Form Handling & Prediction
// ==========================================

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('predictionForm');
    const resultsSection = document.getElementById('resultsSection');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const results = document.getElementById('results');
    const errorMessage = document.getElementById('errorMessage');

    // Form submission
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Show results section and loading spinner
        resultsSection.style.display = 'block';
        loadingSpinner.style.display = 'block';
        results.style.display = 'none';
        errorMessage.style.display = 'none';

        // Smooth scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });

        // Collect form data
        const formData = collectFormData();

        try {
            // Send prediction request
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (response.ok) {
                displayResults(data);
            } else {
                showError(data.error || 'Une erreur est survenue lors de la prédiction');
            }
        } catch (error) {
            showError('Erreur de connexion au serveur: ' + error.message);
        } finally {
            loadingSpinner.style.display = 'none';
        }
    });

    // Reset form
    form.addEventListener('reset', function() {
        resultsSection.style.display = 'none';
        errorMessage.style.display = 'none';
    });

    // ==========================================
    // Collect Form Data
    // ==========================================
    function collectFormData() {
        const data = {
            age: document.getElementById('age').value,
            gender: document.querySelector('input[name="gender"]:checked').value,
            race: document.getElementById('race').value
        };

        // Collect gene mutations
        const geneCheckboxes = document.querySelectorAll('.gene-checkbox');
        geneCheckboxes.forEach(checkbox => {
            data[checkbox.name] = checkbox.checked;
        });

        return data;
    }

    // ==========================================
    // Display Results
    // ==========================================
    function displayResults(data) {
        results.style.display = 'block';

        // Update prediction card
        const predictionCard = document.getElementById('predictionCard');
        const predictionResult = document.getElementById('predictionResult');
        const confidenceText = document.getElementById('confidenceText');

        predictionResult.textContent = data.prediction;
        confidenceText.textContent = `Confiance: ${data.confidence.toFixed(1)}%`;

        // Change card color based on prediction
        predictionCard.classList.remove('lgg', 'gbm');
        if (data.prediction_class === 0) {
            predictionCard.classList.add('lgg');
        } else {
            predictionCard.classList.add('gbm');
        }

        // Update probability bars
        updateProbabilityBar('lgg', data.probability_lgg);
        updateProbabilityBar('gbm', data.probability_gbm);

        // Update interpretation
        document.getElementById('interpretationText').textContent = data.interpretation;

        // Animate the results
        animateResults();
    }

    // ==========================================
    // Update Probability Bars
    // ==========================================
    function updateProbabilityBar(type, probability) {
        const bar = document.getElementById(`${type}Bar`);
        const probText = document.getElementById(`${type}Prob`);

        // Animate the bar
        setTimeout(() => {
            bar.style.width = probability + '%';
        }, 100);

        probText.textContent = probability.toFixed(1) + '%';
    }

    // ==========================================
    // Show Error Message
    // ==========================================
    function showError(message) {
        errorMessage.style.display = 'block';
        errorMessage.innerHTML = `
            <i class="fas fa-exclamation-circle"></i>
            <strong>Erreur:</strong> ${message}
        `;
        results.style.display = 'none';
    }

    // ==========================================
    // Animate Results
    // ==========================================
    function animateResults() {
        // Add fade-in animation to result elements
        const elements = results.querySelectorAll('.prediction-card, .probability-section, .interpretation-box');
        elements.forEach((element, index) => {
            element.style.opacity = '0';
            element.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                element.style.transition = 'all 0.5s ease-out';
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }, index * 150);
        });
    }

    // ==========================================
    // Gene Card Interactions
    // ==========================================
    const geneCards = document.querySelectorAll('.gene-card');
    geneCards.forEach(card => {
        const checkbox = card.querySelector('.gene-checkbox');
        
        card.addEventListener('click', function(e) {
            // Toggle checkbox if clicking anywhere on the card
            if (e.target !== checkbox) {
                checkbox.checked = !checkbox.checked;
            }
            
            // Visual feedback
            if (checkbox.checked) {
                card.style.borderColor = '#7c3aed';
                card.style.backgroundColor = '#f5f3ff';
            } else {
                card.style.borderColor = '#e5e7eb';
                card.style.backgroundColor = 'white';
            }
        });

        // Initialize card style based on checkbox state
        checkbox.addEventListener('change', function() {
            if (this.checked) {
                card.style.borderColor = '#7c3aed';
                card.style.backgroundColor = '#f5f3ff';
            } else {
                card.style.borderColor = '#e5e7eb';
                card.style.backgroundColor = 'white';
            }
        });
    });

    // ==========================================
    // Input Validation & User Feedback
    // ==========================================
    const ageInput = document.getElementById('age');
    ageInput.addEventListener('input', function() {
        if (this.value < 0) {
            this.value = 0;
        } else if (this.value > 120) {
            this.value = 120;
        }
    });

    // ==========================================
    // Keyboard Shortcuts
    // ==========================================
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + Enter to submit form
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            form.dispatchEvent(new Event('submit'));
        }
        
        // Escape to reset form
        if (e.key === 'Escape') {
            form.reset();
        }
    });

    // ==========================================
    // Tooltip for genes (optional enhancement)
    // ==========================================
    const geneDescriptions = document.querySelectorAll('.gene-description');
    geneDescriptions.forEach(desc => {
        desc.addEventListener('mouseenter', function() {
            this.style.color = '#374151';
        });
        
        desc.addEventListener('mouseleave', function() {
            this.style.color = '#6b7280';
        });
    });

    // ==========================================
    // Progress indicator for form completion
    // ==========================================
    function updateFormProgress() {
        const totalFields = 3; // age, gender, race
        let completed = 0;

        if (ageInput.value) completed++;
        if (document.querySelector('input[name="gender"]:checked')) completed++;
        if (document.getElementById('race').value) completed++;

        // You can add a progress bar here if desired
        const progress = (completed / totalFields) * 100;
        console.log(`Form completion: ${progress}%`);
    }

    // Add listeners for progress tracking
    ageInput.addEventListener('input', updateFormProgress);
    document.querySelectorAll('input[name="gender"]').forEach(radio => {
        radio.addEventListener('change', updateFormProgress);
    });
    document.getElementById('race').addEventListener('change', updateFormProgress);

    // ==========================================
    // Accessibility improvements
    // ==========================================
    // Add ARIA labels and improve keyboard navigation
    const submitButton = document.querySelector('.btn-primary');
    submitButton.setAttribute('aria-label', 'Soumettre le formulaire pour analyse');

    // Add visual feedback for keyboard focus
    document.querySelectorAll('input, select, button').forEach(element => {
        element.addEventListener('focus', function() {
            this.style.outline = '3px solid rgba(37, 99, 235, 0.5)';
        });
        
        element.addEventListener('blur', function() {
            this.style.outline = 'none';
        });
    });
});

// ==========================================
// Utility Functions
// ==========================================

// Format percentage with animation
function animateValue(element, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        element.textContent = (progress * (end - start) + start).toFixed(1) + '%';
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

// Copy results to clipboard (optional feature)
function copyResultsToClipboard() {
    const predictionText = document.getElementById('predictionResult').textContent;
    const interpretationText = document.getElementById('interpretationText').textContent;
    
    const textToCopy = `
Résultat de l'analyse:
${predictionText}

Interprétation:
${interpretationText}
    `.trim();
    
    navigator.clipboard.writeText(textToCopy).then(() => {
        alert('Résultats copiés dans le presse-papiers!');
    }).catch(err => {
        console.error('Erreur lors de la copie:', err);
    });
}

// Export results as PDF (would require additional library)
function exportResultsAsPDF() {
    // This would require a library like jsPDF
    console.log('Export PDF feature - to be implemented with jsPDF library');
}
