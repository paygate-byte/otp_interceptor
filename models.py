from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import json

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    """User model for authentication"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime, default=None)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class CapturedOTP(db.Model):
    """Model for storing captured OTPs"""
    id = db.Column(db.Integer, primary_key=True)
    otp_value = db.Column(db.String(20), nullable=False)
    source_type = db.Column(db.String(20), nullable=False)  # 'web', 'sms', 'email'
    source_identifier = db.Column(db.String(255), nullable=False)  # URL, phone number, email
    confidence = db.Column(db.Float, default=0.0)
    detection_method = db.Column(db.String(50))
    tool_used = db.Column(db.String(50))
    raw_data = db.Column(db.Text)  # Can store JSON or raw captured data
    metadata = db.Column(db.Text)  # For additional data as JSON
    capture_time = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship with PCAP file if applicable
    pcap_id = db.Column(db.Integer, db.ForeignKey('pcap_file.id'), nullable=True)
    pcap = db.relationship('PCAPFile', backref=db.backref('otps', lazy=True))

    def get_metadata_dict(self):
        if self.metadata:
            try:
                return json.loads(self.metadata)
            except:
                return {}
        return {}

    def set_metadata_dict(self, metadata_dict):
        self.metadata = json.dumps(metadata_dict)

    def __repr__(self):
        return f'<CapturedOTP {self.otp_value} from {self.source_type}>'

class PCAPFile(db.Model):
    """Model for stored PCAP files"""
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(512), nullable=False)
    file_size = db.Column(db.Integer)  # Size in bytes
    md5_hash = db.Column(db.String(32))
    analysis_count = db.Column(db.Integer, default=0)
    last_analyzed = db.Column(db.DateTime)
    upload_time = db.Column(db.DateTime, default=datetime.utcnow)
    filter_used = db.Column(db.String(255))
    packet_count = db.Column(db.Integer)

    # Foreign key to user who uploaded it (optional)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    user = db.relationship('User', backref=db.backref('pcap_files', lazy=True))

    def __repr__(self):
        return f'<PCAPFile {self.filename}>'

class ToolConfig(db.Model):
    """Model for tool configurations"""
    id = db.Column(db.Integer, primary_key=True)
    tool_name = db.Column(db.String(50), nullable=False, unique=True)
    tool_path = db.Column(db.String(512))
    is_active = db.Column(db.Boolean, default=False)
    api_key = db.Column(db.String(255))
    api_url = db.Column(db.String(255))
    version = db.Column(db.String(50))
    config_json = db.Column(db.Text)  # JSON of tool-specific config
    last_check = db.Column(db.DateTime)

    def get_config_dict(self):
        if self.config_json:
            try:
                return json.loads(self.config_json)
            except:
                return {}
        return {}

    def set_config_dict(self, config_dict):
        self.config_json = json.dumps(config_dict)

    def __repr__(self):
        return f'<ToolConfig {self.tool_name}>'

class APITransaction(db.Model):
    """Model for tracking API calls to external tools"""
    id = db.Column(db.Integer, primary_key=True)
    tool_name = db.Column(db.String(50), nullable=False)
    endpoint = db.Column(db.String(255))
    request_data = db.Column(db.Text)
    response_data = db.Column(db.Text)
    status_code = db.Column(db.Integer)
    success = db.Column(db.Boolean, default=False)
    error_message = db.Column(db.Text)
    execution_time = db.Column(db.Float)  # In seconds
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign key to user who initiated it (optional)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    user = db.relationship('User', backref=db.backref('api_transactions', lazy=True))

    def __repr__(self):
        return f'<APITransaction {self.tool_name} {self.endpoint}>'

class AppSettings(db.Model):
    """Model for application settings"""
    id = db.Column(db.Integer, primary_key=True)
    setting_key = db.Column(db.String(50), nullable=False, unique=True)
    setting_value = db.Column(db.Text)
    setting_type = db.Column(db.String(20), default='string')  # string, int, float, boolean, json
    description = db.Column(db.String(255))

    def get_typed_value(self):
        """Return the value converted to its proper type"""
        if not self.setting_value:
            return None

        if self.setting_type == 'int':
            return int(self.setting_value)
        elif self.setting_type == 'float':
            return float(self.setting_value)
        elif self.setting_type == 'boolean':
            return self.setting_value.lower() in ('true', 't', 'yes', 'y', '1')
        elif self.setting_type == 'json':
            try:
                return json.loads(self.setting_value)
            except:
                return {}
        else:  # Default to string
            return self.setting_value

    def set_typed_value(self, value):
        """Set the value, converting from its type"""
        if value is None:
            self.setting_value = None
            return

        if self.setting_type == 'json':
            self.setting_value = json.dumps(value)
        else:
            self.setting_value = str(value)

    def __repr__(self):
        return f'<AppSettings {self.setting_key}>'

class ActivityLog(db.Model):
    """Model for logging user activities"""
    id = db.Column(db.Integer, primary_key=True)
    activity_type = db.Column(db.String(50), nullable=False)  # login, otp_capture, tool_use, etc.
    description = db.Column(db.Text)
    ip_address = db.Column(db.String(50))
    details = db.Column(db.Text)  # JSON for additional details
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign key to user who performed the activity
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    user = db.relationship('User', backref=db.backref('activities', lazy=True))

    def get_details_dict(self):
        if self.details:
            try:
                return json.loads(self.details)
            except:
                return {}
        return {}

    def set_details_dict(self, details_dict):
        self.details = json.dumps(details_dict)

    def __repr__(self):
        return f'<ActivityLog {self.activity_type} {self.timestamp}>'
