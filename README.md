# OTP Research Tool

A comprehensive research platform for studying One-Time Password (OTP) mechanisms in various protocols for educational purposes.

## Features

- **Advanced OTP Detection**: AI-assisted detection of OTP patterns in web, SMS, and email content
- **PCAP Analysis**: Advanced packet capture analysis with custom OTP filters
- **Security Tool Integration**: Integration with popular security tools like:
  - Metasploit (via MSFRPC)
  - Burp Suite (Professional/Enterprise API)
  - OWASP ZAP
  - Wireshark/tshark
  - Ettercap with custom OTP filters
- **Database Support**: Complete database integration for storing and analyzing captured OTPs
- **User Management**: Secure authentication with role-based access control

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Initialize the database:
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```
5. Run the application:
   ```bash
   python run.py
   ```

## Default Login Credentials

- **Username**: COLLINS
- **Password**: Otp@001

## Research Modules

- **URL OTP Intercept**: Analyze and detect OTPs in web applications
- **PCAP Analyzer**: Extract OTPs from network captures
- **SMS Gateway Simulator**: Research SMS-based OTP vulnerabilities
- **Email OTP Simulator**: Study email-based OTP mechanisms

## API Integration

The tool provides interfaces for integrating with security tools:

```python
# Example Metasploit API usage
from app.utils_api import MetasploitAPI

msf_api = MetasploitAPI(user_id=1)
msf_api.auth_login(username="msf", password="password")
session = msf_api.create_session(target_host="192.168.1.100", target_port=445)
```

## Advanced Packet Filters

Custom packet filters optimized for OTP detection:

```
http contains "otp" or http contains "code" or http contains "token"
http.request.method == "POST" and tcp contains "otp"
tcp port 80 and (tcp contains "sms" or tcp contains "text") and tcp contains "verification"
```

## Disclaimer

This tool is for educational and research purposes only. Always obtain proper authorization before testing any security mechanisms. Unauthorized access to systems or data is illegal and unethical.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
