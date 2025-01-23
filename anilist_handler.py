import json
import webbrowser
import requests

with open("client_secrets.json")as secrets:
    secret=json.load(secrets)
    client_id = secret['client_id']
    client_secret = secret['client_secret']
    redirect_uri = 'http://localhost/callback'
    auth_url = f'https://anilist.co/api/v2/oauth/authorize?client_id={client_id}&response_type=token'
    token_url = 'https://anilist.co/api/v2/oauth/token'

    webbrowser.open(auth_url)
    token = input("kod:")
    access_token = token.split("access_token=")[1].split("&")[0]
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    print(access_token)
    query = {
        "query": """
            {
              Viewer {
                name
              }
            }
            """
    }

    profile_response = requests.post('https://graphql.anilist.co', json=query, headers=headers)
    if profile_response.status_code == 200:
        profile_data = profile_response.json()['data']['Viewer']
        print(f" {profile_data['name']}")
    else:
        print("nie działa")
