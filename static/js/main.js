document.addEventListener('DOMContentLoaded', () => {
    const loanForm = document.getElementById('loanForm');
    const submitBtn = document.getElementById('submitBtn');
    const btnText = document.querySelector('.btn-text');
    const btnLoader = document.getElementById('btnLoader');
    
    const resultOverlay = document.getElementById('resultOverlay');
    const closeResult = document.getElementById('closeResult');
    const resetBtn = document.getElementById('resetBtn');
    
    const resultIcon = document.getElementById('resultIcon');
    const resultTitle = document.getElementById('resultTitle');
    const resultMessage = document.getElementById('resultMessage');

    const toggleLoading = (isLoading) => {
        if (isLoading) {
            btnText.classList.add('hidden');
            btnLoader.classList.remove('hidden');
            submitBtn.disabled = true;
        } else {
            btnText.classList.remove('hidden');
            btnLoader.classList.add('hidden');
            submitBtn.disabled = false;
        }
    };

    loanForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Gather data
        const formData = new FormData(loanForm);
        const jsonData = {};
        formData.forEach((value, key) => {
            jsonData[key] = value;
        });

        toggleLoading(true);

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(jsonData)
            });

            const data = await response.json();
            
            if (response.ok && data.status === 'success') {
                showResult(data.prediction);
            } else {
                showResult('Error');
                console.error("Server Error:", data.error);
            }

        } catch (err) {
            console.error("Fetch error:", err);
            showResult('Error');
        } finally {
            toggleLoading(false);
        }
    });

    const showResult = (status) => {
        resultOverlay.classList.remove('hidden');
        resetBtn.classList.remove('hidden');
        
        // Clear previous state
        resultIcon.className = 'result-icon';
        
        if (status === 'Approved') {
            resultIcon.classList.add('approved');
            resultIcon.innerHTML = '✓';
            resultTitle.textContent = 'Congratulations!';
            resultTitle.style.color = 'var(--success)';
            resultMessage.textContent = 'Based on our AI analysis, your loan application is likely to be APPROVED.';
        } else if (status === 'Rejected') {
            resultIcon.classList.add('rejected');
            resultIcon.innerHTML = '✕';
            resultTitle.textContent = 'Application Declined';
            resultTitle.style.color = 'var(--accent)';
            resultMessage.textContent = 'Based on our current lending criteria, we are currently unable to approve your application.';
        } else {
            resultIcon.innerHTML = '!';
            resultTitle.textContent = 'System Error';
            resultTitle.style.color = 'var(--text-main)';
            resultMessage.textContent = 'There was a problem processing your request. Please try again later.';
        }
    };

    const hideResult = () => {
        resultOverlay.classList.add('hidden');
    };

    closeResult.addEventListener('click', hideResult);
    resetBtn.addEventListener('click', () => {
        hideResult();
        loanForm.reset();
    });
});
