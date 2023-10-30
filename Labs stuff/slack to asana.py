import asana
import requests
import pprint


# Replace with your Asana access token
access_token = '1/1204960001161395:e5966986869d1ff349919810799b95b1'

# Set the Asana API base URL
base_url = 'https://app.asana.com/api/1.0/'

# Make a GET request to list tasks in a project
project_id = '1200313734887847'  # Replace with the ID of your project
url = f'{base_url}projects/{project_id}/tasks'
headers = {
    'Authorization': f'Bearer {access_token}',
}

response = requests.get(url, headers=headers).json()['data']

if response.status_code == 200:
    pprint.pprint(response)
else:
    print(f'Error: {response.status_code}, {response.text}')
