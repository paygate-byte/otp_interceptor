import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'development-key-for-research-only'
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    ALLOWED_EXTENSIONS = {'pcap', 'cap', 'txt'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    DEBUG = os.environ.get('DEBUG') or True

    # Simulated tool paths - in real environment these would be actual paths
    WIRESHARK_PATH = os.environ.get('WIRESHARK_PATH') or '/usr/bin/wireshark'
    TSHARK_PATH = os.environ.get('TSHARK_PATH') or '/usr/bin/tshark'
    BURPSUITE_PATH = os.environ.get('BURPSUITE_PATH') or '/usr/bin/burpsuite'
    ZAP_PATH = os.environ.get('ZAP_PATH') or '/usr/bin/zap.sh'
    ETTERCAP_PATH = os.environ.get('ETTERCAP_PATH') or '/usr/bin/ettercap'
    TCPDUMP_PATH = os.environ.get('TCPDUMP_PATH') or '/usr/bin/tcpdump'
    METASPLOIT_PATH = os.environ.get('METASPLOIT_PATH') or '/usr/bin/msfconsole'

    # API keys and endpoints (would be stored in .env file in production)
    # These are simulated - you would use actual API keys in production
    API_KEYS = {
        'burpsuite': os.environ.get('BURPSUITE_API_KEY') or 'simulated_key',
        'zap': os.environ.get('ZAP_API_KEY') or 'simulated_key',
    }
