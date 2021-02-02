import requests
import cal_maker

# Info and Urls
program_version = 'v1.0'
home_url = 'https://tt.openshift.services.adelaide.edu.au/login'
callback_url = 'https://tt.openshift.services.adelaide.edu.au/login/callback'
timetable_url = 'https://tt.openshift.services.adelaide.edu.au/api/timetable'

user_name_prefix = 'uofa\\'

while True:
    print('\r')
    print('*'*25, program_version, '*'*25)

    user_name = input('Enter username (axxxxxxx):')
    password = input('Enter password:')
    print('*' * 56)
    print('\r')

    data = {'AuthMethod': 'FormsAuthentication',
            'UserName': user_name_prefix + user_name,
            'Password': password}

    # Session start
    print('Connecting to university server, please wait...')

    session = requests.Session()

    # A response that contains SAML request and cookies
    home_response = session.get(home_url)  # 2 cookies should be received
    print('Connected!')

    # Get client request id
    login_url = home_response.url
    client_id_position = home_response.text.index('client-request-id=')
    client_request_id = home_response.text[client_id_position:client_id_position + 54]

    # Logging in
    print("Logging in...")
    login_full_url = login_url + '&' + client_request_id
    login_response = session.post(login_full_url, data=data, allow_redirects=False)  # 3 cookies should be received
    if len(session.cookies.get_dict()) < 3:
        print('Your Username or Password is incorrect, please try again')
        continue

    # Get cookie
    login_response = session.get(login_full_url)  # 6 cookies should be received

    # Get SAMLResponse
    saml_response = login_response.content.decode().partition('name="SAMLResponse" value="')
    saml_response = saml_response[2].partition('" /><noscript><p>Script is disabled. Click Submit to continue.')[0]
    saml_response = {'SAMLResponse': saml_response}

    # Callback
    callback = session.post(callback_url, data=saml_response)
    print("Confirming SAML response with server...")  # 6 cookies should be received
    break

# Access api and preprocessing retrieved data
timetable_response = session.get(timetable_url)
timetable = timetable_response.json()

# Send data to converter
cal_maker.converter(timetable)

input('Please enter to exit.')
