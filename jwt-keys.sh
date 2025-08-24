#!/bin/zsh

# Generate a 2048-bit RSA private key
openssl genrsa -out private.key 2048

# Create a self-signed X.509 public certificate (valid for 365 days)
openssl req -new -x509 -key private.key -out public.crt -days 365 -subj "/CN=jwt-signing"

# Base64 encode the public certificate
base64 public.crt > public.crt.b64

echo "Keys generated:"
echo "  private.key      (RSA private key)"
echo "  public.crt       (X.509 public certificate)"
echo "  public.crt.b64   (Base64-encoded certificate for upload)"