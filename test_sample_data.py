#!/usr/bin/env python
"""Test script to call /api/sample-data endpoint"""
import sys
sys.path.insert(0, 'backend')

from app import app

# Create test client
client = app.test_client()

# Call the endpoint
print('Calling /api/sample-data endpoint...')
response = client.post('/api/sample-data')

print(f'Status: {response.status_code}')
print(f'Response: {response.get_json()}')

if response.status_code == 200:
    print('\n✓ Sample data loaded successfully!')
else:
    print('\n✗ Failed to load sample data')
    sys.exit(1)
