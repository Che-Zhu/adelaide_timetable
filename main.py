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

    user_name = input('Enter user name (axxxxxxx):')
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
    home_response = session.get(home_url) # 2 cookies should be received
    print('Connected!')

    # Get client request id
    login_url = home_response.url
    client_id_position = home_response.text.index('client-request-id=')
    client_request_id = home_response.text[client_id_position:client_id_position + 54]

    # Login header
    login_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'adfs.adelaide.edu.au',
        'Origin': 'https://adfs.adelaide.edu.au',
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
        'Referer': login_url,
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1'}

    # Logging in
    print("Logging in...")
    login_full_url = login_url + '&' + client_request_id
    login_response = session.post(login_full_url, data=data, headers=login_headers, allow_redirects=False) # 3 cookies should be received
    if len(session.cookies.get_dict()) < 3:
        print('Your Username or Password is incorrect, please try again')
        continue

    # Get cookie
    login_response = session.get(login_full_url, headers=login_headers) # 6 cookies should be received

    # Get SAMLResponse
    saml_response = login_response.content.decode().partition('name="SAMLResponse" value="')
    saml_response = saml_response[2].partition('" /><noscript><p>Script is disabled. Click Submit to continue.')[0]
    saml_response = {'SAMLResponse': saml_response}

    # Callback header
    callback_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'tt.openshift.services.adelaide.edu.au',
        'Origin': 'https://adfs.adelaide.edu.au',
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
        'Referer': 'https://adfs.adelaide.edu.au/',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-site',
        'Upgrade-Insecure-Requests': '1'}

    # Callback
    callback = session.post(callback_url, data=saml_response, headers=callback_headers)
    print("Confirming SAML response with server...") # 6 cookies should be received
    break

# Access api and preprocessing retrieved data
timetable_response = session.get(timetable_url, headers=callback_headers)
timetable = timetable_response.json()

# Send data to converter
cal_maker.converter(timetable)
