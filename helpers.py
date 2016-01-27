from zaqarclient.queues import client

import os

conf = {
    'auth_opts': {
        'backend': 'keystone',
        'options': {
            'os_username': os.environ.get('OS_USERNAME'),
            'os_password': os.environ.get('OS_PASSWORD'),
            'os_project_name': os.environ.get('OS_PROJECT_NAME', 'admin'),
            'os_auth_url': os.environ.get('OS_AUTH_URL') + '/v2.0/',
            'insecure': '',
        },
    },
}

client = client.Client(url='http://192.168.122.58:8888', version=2, conf=conf)
