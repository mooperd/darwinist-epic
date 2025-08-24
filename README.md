# Epic FHIR API Client

A basic Flask/Bootstrap utility to connect to Epic's FHIR API and extract patient data.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser to `http://localhost:5008`

## Configuration

The app is configured to use your Epic sandbox credentials:
- **Application Name**: darwinist-epic
- **Sandbox Client ID**: 736d022d-a807-485e-812d-d031010cfb63
- **Sandbox Client Secret**: (configured in app.py)

## Usage

1. Click "Connect to Epic FHIR" to start the OAuth flow
2. You'll be redirected to Epic's authorization server
3. After successful authentication, you'll return to the dashboard
4. Click "Load Patient Data" to fetch FHIR patient information

## Features

- OAuth 2.0 authentication with Epic
- Bootstrap UI for clean interface
- JSON display of FHIR patient data
- Error handling and loading states

## Notes

- Currently configured for sandbox environment
- Uses patient/*.read scope for basic patient data access
- Requires Epic test patient credentials for full testing
## 
Epic App Registration Requirements

If you're getting "Invalid OAuth 2.0 request" errors, check these in your Epic app registration:

### Required Settings:
1. **Redirect URI**: Must exactly match `http://localhost:5008/callback`
2. **Application Type**: Should be "Confidential" (since you have a client secret)
3. **Scopes**: Make sure `patient/*.read` is enabled
4. **JWK Set URLs**: Leave blank for now (you're using client secret auth)

### Troubleshooting:
- Visit `/debug` route to see current configuration
- Check that your Epic app registration redirect URI exactly matches the one in the app
- Ensure your client ID and secret are correct
- Make sure the app is approved/active in Epic's system

### Common Issues:
- **Redirect URI mismatch**: Epic is very strict about exact matches
- **Scope not approved**: Some scopes need Epic approval
- **App not activated**: Check if your Epic app registration is in "active" status