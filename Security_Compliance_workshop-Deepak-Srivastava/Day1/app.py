#!/usr/bin/env python3
"""
Sample Flask Application with Intentional Secrets
This application contains hardcoded secrets for demonstration purposes.
"""

import os
import json
from flask import Flask, jsonify, request
import psycopg2
import boto3
from datetime import datetime

app = Flask(__name__)

# Intentional secrets for demonstration (DO NOT DO THIS IN PRODUCTION!)
REMOVED = "REMOVED"
REMOVED = "REMOVED"
REMOVED = "REMOVED"
REMOVED = "REMOVED"
REMOVED = "REMOVED"
REMOVED = "REMOVED"
REMOVED = "REMOVED"

# Database configuration with hardcoded credentials
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "myapp",
    "user": "admin",
    "password": "admin_password_123!"
}

# Redis configuration
REMOVED = "REMOVED"

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to the DevSecOps Demo Application",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/users')
def get_users():
    """Simulate user data retrieval"""
    # This would normally connect to a database
    return jsonify({
        "users": [
            {"id": 1, "name": "John Doe", "email": "john@example.com"},
            {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
        ]
    })

@app.route('/config')
def get_config():
    """Endpoint that exposes configuration (including secrets) - SECURITY RISK!"""
    return jsonify({
        "database": {
            "host": DB_CONFIG["host"],
            "port": DB_CONFIG["port"],
            "database": DB_CONFIG["database"]
        },
        "aws_region": "us-east-1",
        "api_version": "v1"
    })

@app.route('/secrets')
def get_secrets():
    """DANGEROUS: This endpoint exposes secrets - NEVER DO THIS!"""
    return jsonify({
        "database_password": REMOVED,
        "aws_access_key": REMOVED,
        "api_key": REMOVED,
        "jwt_secret": REMOVED
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
