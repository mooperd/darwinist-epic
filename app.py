from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import requests
import base64
import json
from urllib.parse import urlencode
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

# Epic FHIR Configuration
EPIC_CONFIG = {
    'sandbox_client_id': '736d022d-a807-485e-812d-d031010cfb63',
    'sandbox_client_secret': '3O9ke4snKUnxkVtMFVBw38AX6Enh8kBp93KJrXpuftmHIQoUzKd+Y3cGEHlNvXHs1ifn2SD+TXZ8NScVJFCG8Q==',
    'auth_url': 'https://fhir.epic.com/interconnect-fhir-oauth/oauth2/authorize',
    'token_url': 'https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token',
    'fhir_base_url': 'https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4',
    'redirect_uri': 'http://127.0.0.1:5008/callback'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/auth')
def auth():
    # Use sandbox credentials for testing
    params = {
        'response_type': 'code',
        'client_id': EPIC_CONFIG['sandbox_client_id'],
        'redirect_uri': EPIC_CONFIG['redirect_uri'],
        'scope': 'patient/*.read',
        'state': 'test-state'
    }
    
    auth_request_url = f"{EPIC_CONFIG['auth_url']}?{urlencode(params)}"
    print(f"Auth URL: {auth_request_url}")  # Debug print
    return redirect(auth_request_url)

@app.route('/debug')
def debug():
    """Debug route to show current configuration"""
    return f"""
    <h2>Epic FHIR Debug Info</h2>
    <p><strong>Client ID:</strong> {EPIC_CONFIG['sandbox_client_id']}</p>
    <p><strong>Redirect URI:</strong> {EPIC_CONFIG['redirect_uri']}</p>
    <p><strong>Auth URL:</strong> {EPIC_CONFIG['auth_url']}</p>
    <p><strong>Token URL:</strong> {EPIC_CONFIG['token_url']}</p>
    <p><strong>FHIR Base URL:</strong> {EPIC_CONFIG['fhir_base_url']}</p>
    <br>
    <a href="/auth">Test Auth Flow</a>
    """

@app.route('/callback')
def callback():
    code = request.args.get('code')
    error = request.args.get('error')
    error_description = request.args.get('error_description')
    
    if error:
        return f"Authorization error: {error} - {error_description}", 400
    
    if not code:
        return "Authorization failed - no code received", 400
    
    # Exchange code for token
    token_url = EPIC_CONFIG['token_url']
    
    # Create basic auth header
    credentials = f"{EPIC_CONFIG['sandbox_client_id']}:{EPIC_CONFIG['sandbox_client_secret']}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    
    headers = {
        'Authorization': f'Basic {encoded_credentials}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': EPIC_CONFIG['redirect_uri']
    }
    
    try:
        response = requests.post(token_url, headers=headers, data=data)
        token_data = response.json()
        
        if response.status_code == 200:
            session['access_token'] = token_data.get('access_token')
            session['patient_id'] = token_data.get('patient')
            return redirect(url_for('dashboard'))
        else:
            return f"Token exchange failed: {token_data}", 400
            
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/dashboard')
def dashboard():
    if 'access_token' not in session:
        return redirect(url_for('index'))
    
    return render_template('dashboard.html', patient_id=session.get('patient_id'))

@app.route('/api/patient')
def get_patient():
    if 'access_token' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    patient_id = session.get('patient_id')
    if not patient_id:
        return jsonify({'error': 'No patient ID'}), 400
    
    headers = {
        'Authorization': f'Bearer {session["access_token"]}',
        'Accept': 'application/fhir+json'
    }
    
    try:
        url = f"{EPIC_CONFIG['fhir_base_url']}/Patient/{patient_id}"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'error': f'API request failed: {response.status_code}'}), response.status_code
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5008)