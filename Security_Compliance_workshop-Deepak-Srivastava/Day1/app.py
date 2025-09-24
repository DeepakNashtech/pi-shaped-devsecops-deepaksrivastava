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
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

"""
Configuration is loaded from environment variables to avoid hardcoded secrets.
See `env.example` for the list of variables.
"""
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
API_KEY = os.getenv("API_KEY", "")
JWT_SECRET = os.getenv("JWT_SECRET", "")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

# Database configuration
DB_CONFIG = {
    "host": os.getenv("DATABASE_HOST", "localhost"),
    "port": int(os.getenv("DATABASE_PORT", "5432")),
    "database": os.getenv("DATABASE_NAME", "myapp"),
    "user": os.getenv("DATABASE_USER", "admin"),
    "password": DATABASE_PASSWORD,
}

# Redis configuration
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")

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

# Security: Do not expose secrets via any endpoint

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
