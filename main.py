from linkedin import linkedin

# LinkedIn API credentials
API_KEY = 'your_client_id'
API_SECRET = 'your_client_secret'
RETURN_URL = 'http://localhost:8000'

# LinkedIn authentication
authentication = linkedin.LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL, linkedin.PERMISSIONS.enums.values())
print('Please go to this URL to authorize the application:', authentication.authorization_url)

# Get the authorization code and access token
authorization_code = input('Enter the authorization code: ')
authentication.authorization_code = authorization_code
access_token = authentication.get_access_token()

# Create a LinkedIn application instance
application = linkedin.LinkedInApplication(token=access_token)

# Get the list of new connections
new_connections = []
connections = application.get_connections(selectors=['id'], params={'start': 0, 'count': 10})
for connection in connections['values']:
    if connection['id'] not in new_connections:
        new_connections.append(connection['id'])

# Send welcome message to new connections
for connection in connections['values']:
    if connection['id'] in new_connections:
        message = 'Hello ' + connection['firstName'] + ', welcome to my LinkedIn network!'
        application.send_message(recipients=[{'person': {'_path': '/people/' + connection['id']}}], message=message)
