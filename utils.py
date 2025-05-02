import os
import re
import json
import base64
import random
import string
import subprocess
from datetime import datetime
from functools import wraps
from typing import Dict, List, Optional, Union, Tuple, Any
from flask import request, flash, redirect, url_for, current_app

# Utility functions for handling files
def allowed_file(filename: str) -> bool:
    """Check if the file extension is allowed"""
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in current_app.config['ALLOWED_EXTENSIONS']

def secure_filename(filename: str) -> str:
    """Make a filename secure by removing unsafe characters"""
    # This is a simplified version - in production use werkzeug.utils.secure_filename
    # Remove bad characters and normalize whitespace
    filename = re.sub(r'[^\w\s.-]', '', filename)
    filename = re.sub(r'\s+', '_', filename).strip()
    return filename

def ensure_dir(directory: str) -> str:
    """Ensure a directory exists, creating it if necessary"""
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

# Simulation utilities for demo
def simulate_otp_detection(source_type: str = 'sms', length: int = 6) -> Dict[str, Any]:
    """Simulate detecting an OTP from various sources"""
    otp = ''.join(random.choices(string.digits, k=length))
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return {
        'otp': otp,
        'source': source_type,
        'confidence': random.uniform(0.75, 0.99),
        'timestamp': timestamp,
        'method': random.choice(['pattern_match', 'ai_detection', 'header_analysis']),
    }

def simulate_tool_output(tool_name: str, command_args: List[str] = None) -> str:
    """Simulate output from security tools"""
    tool_outputs = {
        'wireshark': [
            "[Wireshark] Capturing on interface eth0",
            "[Wireshark] Packets: 1257 Displayed: 1257 Marked: 0",
            "[Wireshark] Filter for HTTP/HTTPS traffic applied",
            "[Wireshark] Found potential OTP in packet #452 (HTTP POST data)",
            "[Wireshark] Analysis complete - saved to capture.pcapng"
        ],
        'burpsuite': [
            "[Burp Suite] Proxy started on port 8080",
            "[Burp Suite] Intercepting HTTP/HTTPS requests...",
            "[Burp Suite] Captured form submission with potential OTP field",
            "[Burp Suite] Scan complete - Found 3 potential OTP transmissions"
        ],
        'zap': [
            "[ZAP] Starting session...",
            "[ZAP] Active scanning enabled for URL: {0}",
            "[ZAP] Found form with potential session validation",
            "[ZAP] Detected OTP pattern in response at 14:25:36",
            "[ZAP] Scan summary: 2 alerts, 1 OTP form detected"
        ],
        'ettercap': [
            "[Ettercap] Starting in unified sniffing mode",
            "[Ettercap] Scanning for hosts...",
            "[Ettercap] 12 hosts added to the hosts list",
            "[Ettercap] ARP poisoning victims:",
            "[Ettercap] GROUP 1 : 192.168.1.5 00:DE:AD:BE:EF:00",
            "[Ettercap] GROUP 2 : 192.168.1.1 00:11:22:33:44:55",
            "[Ettercap] Monitoring session for OTP patterns..."
        ],
        'tcpdump': [
            "[tcpdump] listening on eth0, link-type EN10MB (Ethernet)",
            "[tcpdump] 16:42:35.792058 IP 192.168.1.5.58799 > 216.58.212.142.443: TCP",
            "[tcpdump] 16:42:36.123057 IP 216.58.212.142.443 > 192.168.1.5.58799: TCP",
            "[tcpdump] 16:42:37.255929 IP 192.168.1.5.58799 > 216.58.212.142.443: SSL/TLS",
            "[tcpdump] Packet capture complete: 1459 packets captured"
        ],
        'metasploit': [
            "[msf] Started reverse TCP handler on 192.168.1.5:4444",
            "[msf] Using auxiliary module: auxiliary/server/socks_proxy",
            "[msf] SOCKS proxy started on 0.0.0.0:1080",
            "[msf] Proxying traffic to facilitate OTP interception",
            "[msf] Session monitoring for authentication attempts"
        ],
    }

    # Get the tool output
    outputs = tool_outputs.get(tool_name.lower(), [
        f"[{tool_name}] Tool simulation started",
        f"[{tool_name}] No predefined output for this tool - generic simulation",
        f"[{tool_name}] Execution completed"
    ])

    # Add command arguments to the output if provided
    if command_args:
        cmd_str = " ".join(command_args)
        outputs.insert(0, f"[{tool_name}] Executing command: {cmd_str}")

    # Add some randomness to make outputs look more realistic
    if random.random() > 0.5:
        outputs.append(f"[{tool_name}] Execution time: {random.uniform(0.5, 10.2):.2f} seconds")

    # Add a simulated OTP if this is one of our core tools
    if tool_name.lower() in ['wireshark', 'burpsuite', 'zap', 'ettercap', 'tcpdump']:
        otp_result = simulate_otp_detection()
        outputs.append(f"[{tool_name}] Potential OTP detected: {otp_result['otp']} (confidence: {otp_result['confidence']:.2f})")

    return "\n".join(outputs)

# Mock integrations with security tools (simulation only)
class ToolInterface:
    """Interface for security tools - in a real app, this would execute actual tools"""

    @staticmethod
    def execute_command(command: List[str], cwd: Optional[str] = None) -> Tuple[int, str, str]:
        """
        Simulate executing a command and returning exit code, stdout, and stderr
        In a real environment, this would use subprocess.run()
        """
        # For simulation, always return success (0) with simulated output
        stdout = f"SIMULATED OUTPUT: Would execute: {' '.join(command)}\n"

        # Add tool-specific simulation if the command starts with a known tool
        tool_cmd = command[0].split('/')[-1]  # Get last part of path
        if tool_cmd in ['wireshark', 'tshark', 'burpsuite', 'zap.sh', 'ettercap', 'tcpdump', 'msfconsole']:
            stdout += simulate_tool_output(tool_cmd, command[1:])

        return 0, stdout, ""

    @staticmethod
    def wireshark_analyze(pcap_file: str, filter_expr: Optional[str] = None) -> Dict[str, Any]:
        """
        Simulate Wireshark/tshark analysis of a pcap file
        In real implementation, would use tshark command line or pyshark
        """
        # Simulate finding OTPs
        results = {
            'packets_analyzed': random.randint(500, 5000),
            'potential_otps': [simulate_otp_detection() for _ in range(random.randint(1, 3))],
            'analysis_time': random.uniform(0.5, 5.0),
            'filter_applied': filter_expr or 'http or https'
        }
        return results

    @staticmethod
    def burpsuite_api(endpoint: str, method: str = 'GET', data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Simulate Burp Suite API interactions
        In real implementation, would make HTTP requests to the Burp REST API
        """
        # Simulate API response
        responses = {
            'start_proxy': {
                'success': True,
                'port': 8080,
                'interfaces': ['127.0.0.1', '0.0.0.0']
            },
            'scan_url': {
                'success': True,
                'scan_id': f"SCAN-{random.randint(1000, 9999)}",
                'issues_found': random.randint(0, 10),
                'scan_status': 'completed'
            },
            'get_results': {
                'success': True,
                'findings': [
                    {
                        'type': 'information',
                        'name': 'OTP Form Detected',
                        'confidence': 'firm',
                        'severity': 'information',
                        'url': data.get('url', 'https://example.com') if data else 'https://example.com',
                    }
                ]
            }
        }

        return responses.get(endpoint, {'success': False, 'error': 'Endpoint not found'})

    @staticmethod
    def zap_api(action: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Simulate ZAP API interactions
        In real implementation, would use the python-owasp-zap-v2.4 library
        """
        # Simulate ZAP actions and responses
        actions = {
            'core/newSession': {
                'success': True,
                'session': f"session-{random.randint(1000, 9999)}"
            },
            'spider/scan': {
                'success': True,
                'scan_id': random.randint(1, 100)
            },
            'ascan/scan': {
                'success': True,
                'scan_id': random.randint(1, 100)
            },
            'search/urlsByUrlRegex': {
                'success': True,
                'urls': [
                    f"https://example.com/auth/{random.randint(100, 999)}",
                    f"https://example.com/verify-otp/{random.randint(100, 999)}"
                ]
            }
        }

        action_key = action.replace('/', '')
        return actions.get(action, {'success': False, 'error': 'Action not supported'})

    @staticmethod
    def parse_pcap_for_otp(pcap_file: str) -> List[Dict[str, Any]]:
        """
        Simulate parsing a pcap file to find OTPs
        In real implementation, would use pyshark or similar
        """
        # Simulate finding 1-3 OTPs
        return [simulate_otp_detection() for _ in range(random.randint(1, 3))]

# Security helpers
def generate_csrf_token() -> str:
    """Generate a CSRF token - in real app use Flask-WTF's generate_csrf function"""
    token = base64.b64encode(os.urandom(32)).decode('utf-8')
    return token

def require_auth(f):
    """Decorator to require authentication - simulate this for demo purposes"""
    @wraps(f)
    def decorated(*args, **kwargs):
        # In a real app, verify session or auth token
        if not request.cookies.get('demo_auth'):
            flash('Authentication required', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated
