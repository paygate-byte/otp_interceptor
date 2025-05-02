import os
import json
import random
from flask import (
    render_template, request, redirect, url_for, flash,
    jsonify, send_from_directory, Response, make_response
)
from werkzeug.utils import secure_filename
from app import app
from app.utils import (
    allowed_file, ensure_dir, simulate_otp_detection,
    simulate_tool_output, ToolInterface, generate_csrf_token
)

# Ensure upload directory exists
ensure_dir(app.config['UPLOAD_FOLDER'])

# Create uploads directory for PCAP files
PCAP_FOLDER = os.path.join(app.config['UPLOAD_FOLDER'], 'pcap')
ensure_dir(PCAP_FOLDER)

@app.route('/')
def index():
    """Home page with dashboard"""
    tool_statuses = {
        'wireshark': random.choice(['active', 'inactive']),
        'burpsuite': random.choice(['active', 'inactive']),
        'zap': random.choice(['active', 'inactive']),
        'ettercap': random.choice(['active', 'inactive', 'error']),
        'tcpdump': random.choice(['active', 'inactive']),
        'metasploit': random.choice(['active', 'inactive']),
    }

    stats = {
        'total_scans': random.randint(5, 50),
        'otps_detected': random.randint(10, 100),
        'active_sessions': random.randint(0, 3),
        'tools_enabled': sum(1 for status in tool_statuses.values() if status == 'active')
    }

    recent_activities = [
        {
            'timestamp': '2025-05-02 10:15:23',
            'action': 'URL OTP Interception',
            'target': 'https://example-shop.com/verify',
            'result': 'Success - OTP: 123456'
        },
        {
            'timestamp': '2025-05-02 09:45:12',
            'action': 'PCAP Analysis',
            'target': 'capture_2025-05-02.pcap',
            'result': 'Found 2 potential OTPs'
        },
        {
            'timestamp': '2025-05-01 17:32:09',
            'action': 'SMS Gateway Test',
            'target': '+1234567890',
            'result': 'Simulated SMS with OTP: 876543'
        }
    ]

    return render_template(
        'index.html',
        tool_statuses=tool_statuses,
        stats=stats,
        recent_activities=recent_activities
    )

@app.route('/url-intercept', methods=['GET', 'POST'])
def url_intercept():
    """URL-based OTP interception tool"""
    result = None
    tool_output = None

    if request.method == 'POST':
        url = request.form.get('url')
        tool = request.form.get('tool', 'auto')

        if not url:
            flash('URL is required', 'danger')
        else:
            # Simulate tool execution for the URL
            if tool == 'auto':
                tool = random.choice(['burpsuite', 'zap'])

            tool_output = simulate_tool_output(tool)

            # Simulate OTP detection
            otp_data = simulate_otp_detection('web')

            result = {
                'url': url,
                'tool_used': tool,
                'otp': otp_data['otp'],
                'confidence': otp_data['confidence'],
                'timestamp': otp_data['timestamp'],
                'method': otp_data['method']
            }

            flash(f'OTP interception for {url} completed successfully!', 'success')

    return render_template(
        'url_intercept.html',
        result=result,
        tool_output=tool_output
    )

@app.route('/pcap-analyzer', methods=['GET', 'POST'])
def pcap_analyzer():
    """PCAP file analysis tool"""
    results = None
    tool_output = None

    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(PCAP_FOLDER, filename)

            # In a real app, save the file and process it
            # file.save(file_path)

            # For demo, we'll simulate analysis
            analysis_filter = request.form.get('filter', 'http or https')
            tool = request.form.get('tool', 'wireshark')

            # Simulate tool execution for the PCAP file
            tool_output = simulate_tool_output(tool)

            # Get simulated analysis results
            results = ToolInterface.wireshark_analyze(
                pcap_file=file_path,
                filter_expr=analysis_filter
            )

            flash(f'PCAP file analyzed successfully!', 'success')
        else:
            flash(f'File type not allowed. Allowed types: {", ".join(app.config["ALLOWED_EXTENSIONS"])}', 'danger')

    return render_template(
        'pcap_analyzer.html',
        results=results,
        tool_output=tool_output
    )

@app.route('/sms-gateway', methods=['GET', 'POST'])
def sms_gateway():
    """SMS Gateway OTP Simulation"""
    result = None
    tool_output = None

    if request.method == 'POST':
        phone_number = request.form.get('phone_number')
        tool = request.form.get('tool', 'custom')

        if not phone_number:
            flash('Phone number is required', 'danger')
        else:
            # Simulate SMS gateway with OTP
            otp_data = simulate_otp_detection('sms')

            # Simulate tool output
            tool_output = simulate_tool_output('sms_interceptor')

            result = {
                'phone_number': phone_number,
                'otp': otp_data['otp'],
                'confidence': otp_data['confidence'],
                'timestamp': otp_data['timestamp'],
                'method': otp_data['method']
            }

            flash(f'SMS OTP simulation for {phone_number} completed successfully!', 'success')

    return render_template(
        'sms_gateway.html',
        result=result,
        tool_output=tool_output
    )

@app.route('/email-otp', methods=['GET', 'POST'])
def email_otp():
    """Email OTP Simulation"""
    result = None
    tool_output = None

    if request.method == 'POST':
        email = request.form.get('email')
        tool = request.form.get('tool', 'custom')

        if not email:
            flash('Email address is required', 'danger')
        else:
            # Simulate email OTP
            otp_data = simulate_otp_detection('email')

            # Simulate tool output
            tool_output = simulate_tool_output('email_interceptor')

            result = {
                'email': email,
                'otp': otp_data['otp'],
                'confidence': otp_data['confidence'],
                'timestamp': otp_data['timestamp'],
                'method': otp_data['method']
            }

            flash(f'Email OTP simulation for {email} completed successfully!', 'success')

    return render_template(
        'email_otp.html',
        result=result,
        tool_output=tool_output
    )

@app.route('/tool-manager')
def tool_manager():
    """Tool management interface"""
    # Simulate tool configurations
    tools = [
        {
            'id': 'wireshark',
            'name': 'Wireshark',
            'version': '3.6.2',
            'path': app.config['WIRESHARK_PATH'],
            'status': random.choice(['active', 'inactive']),
            'description': 'Network protocol analyzer for OTP packet inspection',
            'icon': 'fa-solid fa-wifi'
        },
        {
            'id': 'burpsuite',
            'name': 'Burp Suite',
            'version': '2022.3.4',
            'path': app.config['BURPSUITE_PATH'],
            'status': random.choice(['active', 'inactive']),
            'description': 'Web vulnerability scanner and proxy for OTP interception',
            'icon': 'fa-solid fa-spider'
        },
        {
            'id': 'zap',
            'name': 'OWASP ZAP',
            'version': '2.12.0',
            'path': app.config['ZAP_PATH'],
            'status': random.choice(['active', 'inactive']),
            'description': 'Open-source web app scanner for OTP request/response analysis',
            'icon': 'fa-solid fa-bolt'
        },
        {
            'id': 'ettercap',
            'name': 'Ettercap',
            'version': '0.8.3',
            'path': app.config['ETTERCAP_PATH'],
            'status': random.choice(['active', 'inactive', 'error']),
            'description': 'MITM attack tool useful for network OTP sniffing',
            'icon': 'fa-solid fa-network-wired'
        },
        {
            'id': 'tcpdump',
            'name': 'tcpdump',
            'version': '4.99.1',
            'path': app.config['TCPDUMP_PATH'],
            'status': random.choice(['active', 'inactive']),
            'description': 'Command-line packet analyzer for OTP capture',
            'icon': 'fa-solid fa-terminal'
        },
        {
            'id': 'metasploit',
            'name': 'Metasploit',
            'version': '6.2.9',
            'path': app.config['METASPLOIT_PATH'],
            'status': random.choice(['active', 'inactive']),
            'description': 'Penetration testing framework with OTP modules',
            'icon': 'fa-solid fa-skull'
        }
    ]

    return render_template('tool_manager.html', tools=tools)

@app.route('/settings')
def settings():
    """Application settings"""
    # Simulate settings
    settings = {
        'proxy_port': 8080,
        'interface': 'eth0',
        'log_level': 'INFO',
        'auto_analyze': True,
        'otp_regex_patterns': [
            r'\b\d{6}\b',
            r'\b\d{4}\b',
            r'verification[\s-]*code[\s:]*([0-9]{4,8})',
            r'one[\s-]*time[\s-]*password[\s:]*([0-9]{4,8})'
        ]
    }

    return render_template('settings.html', settings=settings)

@app.route('/about')
def about():
    """About page with documentation"""
    return render_template('about.html')

@app.route('/disclaimer')
def disclaimer():
    """Legal disclaimer"""
    return render_template('disclaimer.html')

@app.route('/api/execute-tool', methods=['POST'])
def api_execute_tool():
    """API endpoint to execute a security tool (simulated)"""
    data = request.json

    if not data or 'tool' not in data:
        return jsonify({'error': 'Tool ID is required'}), 400

    tool_id = data.get('tool')
    params = data.get('params', {})

    # Simulate tool execution
    if tool_id == 'wireshark':
        result = ToolInterface.wireshark_analyze(
            pcap_file=params.get('file', 'capture.pcap'),
            filter_expr=params.get('filter', 'http or https')
        )
    elif tool_id == 'burpsuite':
        result = ToolInterface.burpsuite_api(
            endpoint=params.get('endpoint', 'scan_url'),
            method=params.get('method', 'POST'),
            data=params.get('data', {'url': 'https://example.com'})
        )
    elif tool_id == 'zap':
        result = ToolInterface.zap_api(
            action=params.get('action', 'core/newSession'),
            params=params.get('params', {})
        )
    else:
        # Generic tool simulation
        output = simulate_tool_output(tool_id)
        result = {
            'success': True,
            'tool': tool_id,
            'output': output,
            'timestamp': '2025-05-02 12:34:56'
        }

    # Add simulated delay for realism
    # In real app this would be the actual tool execution time
    # time.sleep(random.uniform(0.5, 2.0))

    return jsonify(result)

@app.route('/uploads/<path:filename>')
def download_file(filename):
    """Serve uploaded files"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Simple login page for demo authentication"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Demo authentication - ONLY FOR DEMO PURPOSES
        # In production, use proper authentication like Flask-Login
        if username == 'research' and password == 'demo123':
            resp = make_response(redirect(url_for('index')))
            resp.set_cookie('demo_auth', 'authenticated', max_age=3600)
            flash('Login successful', 'success')
            return resp
        else:
            flash('Invalid credentials', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout route"""
    resp = make_response(redirect(url_for('login')))
    resp.delete_cookie('demo_auth')
    flash('Logged out successfully', 'success')
    return resp
