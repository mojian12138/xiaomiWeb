document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('stepForm');
    const stepsInput = document.getElementById('steps');
    const stepSlider = document.getElementById('stepSlider');
    const submitBtn = document.getElementById('submitBtn');
    const resultMessage = document.getElementById('resultMessage');
    const accountInput = document.getElementById('account');
    const passwordInput = document.getElementById('password');

    // Tab Switching Logic
    const tabUpdate = document.getElementById('tab-update');
    const tabAbout = document.getElementById('tab-about');
    const updateSection = document.getElementById('updateSection');
    const aboutSection = document.getElementById('aboutSection');

    tabUpdate.addEventListener('click', () => {
        tabUpdate.classList.add('active');
        tabAbout.classList.remove('active');
        updateSection.style.display = 'block';
        aboutSection.style.display = 'none';
    });

    tabAbout.addEventListener('click', () => {
        tabAbout.classList.add('active');
        tabUpdate.classList.remove('active');
        aboutSection.style.display = 'block';
        updateSection.style.display = 'none';
    });

    // Sync input and slider
    stepsInput.addEventListener('input', () => {
        let val = parseInt(stepsInput.value);
        if (val > 98800) val = 98800;
        if (val < 1) val = 1;
        stepSlider.value = val;
    });

    stepSlider.addEventListener('input', () => {
        stepsInput.value = stepSlider.value;
    });

    // Form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const account = accountInput.value.trim();
        const password = passwordInput.value.trim();
        const steps = parseInt(stepsInput.value);

        if (!account || !password) {
            showResult('请输入账号和密码', false);
            return;
        }

        // Loading state
        submitBtn.disabled = true;
        const originalBtnText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> 处理中...';
        resultMessage.style.display = 'none';

        try {
            const response = await fetch('/api/update', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    account: account,
                    password: password,
                    steps: steps
                })
            });

            const data = await response.json();

            if (data.success) {
                showResult(data.message || '步数更新成功！', true);
            } else {
                showResult(data.message || '步数更新失败，请重试', false);
            }
        } catch (error) {
            console.error('Error:', error);
            showResult('请求失败: ' + error.message, false);
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalBtnText;
        }
    });

    function showResult(message, isSuccess) {
        resultMessage.textContent = message;
        resultMessage.style.display = 'block';
        resultMessage.className = 'result-message ' + (isSuccess ? 'result-success' : 'result-error');
    }
});
