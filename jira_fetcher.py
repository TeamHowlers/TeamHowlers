import requests
import base64
import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

JIRA_BASE_URL = os.getenv('JIRA_BASE_URL')
JIRA_EMAIL = os.getenv('JIRA_EMAIL')
JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')

def get_jira_ticket(ticket_id):
    url = f"{JIRA_BASE_URL}rest/api/3/issue/{ticket_id}"
    auth_str = f"{JIRA_EMAIL}:{JIRA_API_TOKEN}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()
    headers = {
        "Authorization": f"Basic {b64_auth}",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    fields = data['fields']
    title = fields.get('summary', '')

    description_data = fields.get('description', {})
    description = ''
    if isinstance(description_data, dict) and 'content' in description_data:
        for block in description_data['content']:
            if 'content' in block:
                for item in block['content']:
                    if item.get('type') == 'text':
                        description += item.get('text', '')

    labels = fields.get('labels', [])
    return {
        'title': title,
        'description': description,
        'labels': labels
    }

if __name__ == "__main__":
    import sys
    ticket_id = sys.argv[1]
    info = get_jira_ticket(ticket_id)
    print(info)
