document.addEventListener('DOMContentLoaded', function() {
    // Dark mode toggle
    const darkModeSwitch = document.getElementById('darkModeSwitch');
    if (darkModeSwitch) {
        // Check if user has previously set a preference
        const darkModeEnabled = localStorage.getItem('darkModeEnabled') === 'true';
        if (darkModeEnabled) {
            document.body.classList.add('dark-mode');
            darkModeSwitch.checked = true;
        }

        darkModeSwitch.addEventListener('change', function() {
            if (this.checked) {
                document.body.classList.add('dark-mode');
                localStorage.setItem('darkModeEnabled', 'true');
            } else {
                document.body.classList.remove('dark-mode');
                localStorage.setItem('darkModeEnabled', 'false');
            }
        });
    }

    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Toggle tool settings sections
    const toolSettingsToggles = document.querySelectorAll('.tool-settings-toggle');
    toolSettingsToggles.forEach(function(toggle) {
        toggle.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                if (targetElement.style.display === 'none') {
                    targetElement.style.display = 'block';
                    this.innerHTML = '<i class="fas fa-chevron-up"></i> Hide Settings';
                } else {
                    targetElement.style.display = 'none';
                    this.innerHTML = '<i class="fas fa-chevron-down"></i> Show Settings';
                }
            }
        });
    });

    // Function to simulate terminal output typing effect
    window.simulateTyping = function(elementId, text, speed = 30) {
        const element = document.getElementById(elementId);
        if (!element) return;

        element.textContent = ''; // Clear existing content
        let i = 0;

        function typeNextCharacter() {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
                element.scrollTop = element.scrollHeight; // Auto-scroll to bottom
                setTimeout(typeNextCharacter, speed);
            }
        }

        typeNextCharacter();
    };

    // Generic function to show loading spinner
    window.showLoading = function(buttonElement, loadingText = 'Processing...') {
        if (!buttonElement) return;

        const originalText = buttonElement.innerHTML;
        buttonElement.disabled = true;
        buttonElement.innerHTML = `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> ${loadingText}`;

        return function() {
            buttonElement.disabled = false;
            buttonElement.innerHTML = originalText;
        };
    };

    // Intercept form submissions for tool forms
    const toolForms = document.querySelectorAll('.tool-form');
    toolForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const submitButton = form.querySelector('button[type="submit"]');
            const stopLoading = window.showLoading(submitButton);

            // For demo purposes, we'll simulate processing
            // In a real app, this would be replaced with actual form submission
            if (form.getAttribute('data-demo') === 'true') {
                e.preventDefault();

                const outputElement = document.getElementById(form.getAttribute('data-output'));
                if (outputElement) {
                    // Clear previous results
                    outputElement.innerHTML = '';

                    // Show "connecting" message in terminal style
                    setTimeout(function() {
                        const terminalOutput = document.createElement('div');
                        terminalOutput.className = 'terminal-output';
                        terminalOutput.id = 'demo-terminal-output';
                        outputElement.appendChild(terminalOutput);

                        // Simulate tool execution with typing effect
                        window.simulateTyping('demo-terminal-output',
                            `[*] Initializing...\n` +
                            `[*] Loading configuration...\n` +
                            `[+] Configuration loaded.\n` +
                            `[*] Connecting to target...\n` +
                            `[+] Connection established.\n` +
                            `[*] Analyzing traffic...\n` +
                            `[*] Searching for OTP patterns...\n` +
                            `[+] Analysis complete.\n` +
                            `\n` +
                            `[RESULT] Found potential OTP: 123456\n` +
                            `[RESULT] Found potential OTP: 654321\n` +
                            `\n` +
                            `[*] Session completed.\n`
                        );

                        // Reset the button
                        setTimeout(function() {
                            stopLoading();

                            // Add a results section
                            const resultsSection = document.createElement('div');
                            resultsSection.className = 'mt-4';
                            resultsSection.innerHTML = `
                                <h5>Captured Results:</h5>
                                <div class="otp-result">
                                    <span class="badge bg-info method-badge">SMS</span> 123456
                                </div>
                                <div class="otp-result">
                                    <span class="badge bg-primary method-badge">EMAIL</span> 654321
                                </div>
                            `;
                            outputElement.appendChild(resultsSection);
                        }, 3000);
                    }, 1000);
                }
            }
        });
    });

    // Tool execution buttons
    const toolExecuteButtons = document.querySelectorAll('.tool-execute');
    toolExecuteButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const toolId = this.getAttribute('data-tool');
            const outputId = this.getAttribute('data-output');
            const outputElement = document.getElementById(outputId);

            if (!outputElement) return;

            const stopLoading = window.showLoading(this, 'Running Tool...');

            // Simulate tool execution
            setTimeout(function() {
                outputElement.innerHTML = '<div class="terminal-output" id="tool-output"></div>';
                window.simulateTyping('tool-output',
                    `[*] Executing ${toolId}...\n` +
                    `[*] This is a simulated output for demonstration purposes.\n` +
                    `[*] In a real environment, this would execute the actual security tool.\n` +
                    `[+] Tool execution completed.\n`
                );

                stopLoading();
            }, 1500);
        });
    });

    // Copy to clipboard functionality
    const copyButtons = document.querySelectorAll('.copy-btn');
    copyButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const textToCopy = document.getElementById(this.getAttribute('data-copy-target')).textContent;

            navigator.clipboard.writeText(textToCopy).then(function() {
                const originalText = button.innerHTML;
                button.innerHTML = '<i class="fas fa-check"></i> Copied!';

                setTimeout(function() {
                    button.innerHTML = originalText;
                }, 2000);
            }).catch(function(err) {
                console.error('Could not copy text: ', err);
            });
        });
    });
});
