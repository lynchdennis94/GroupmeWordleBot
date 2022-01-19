import json
import pycurl
from io import BytesIO
from urllib.parse import urlencode


def retrieve_group_ids(token):
    """
    Used as a tutorial call to GET items
    :param token: the access token for the bots
    :return: information on all group ids associated with the access token
    """
    jsonresponse = json.loads(get_curl_response(f'https://api.groupme.com/v3/groups?token={token}'))
    print(json.dumps(jsonresponse, indent=4))


def get_messages(token, group_id, since_id=None, limit=None):
    url = f'https://api.groupme.com/v3/groups/{group_id}/messages?token={token}'
    if since_id is not None:
        url = url + f'&since_id={since_id}'
    if limit is not None:
        url = url + f'&limit={limit}'

    print(url)

    curl_response = get_curl_response(url)
    print(curl_response)
    return curl_response



def send_message(bot_id, text):
    """
    Given a specific bot id and text to send, sends a POST request to send a message to the group via the bot
    :param bot_id: the id of the bot being used to send the message
    :param text: the text the bot should send
    :return: None
    """
    data = {'bot_id': f'{bot_id}', 'text': f'{text}'}
    post_curl_message(f'https://api.groupme.com/v3/bots/post', data)


def post_curl_message(url, data):
    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.POSTFIELDS, json.dumps(data))
    curl.perform()
    curl.close()


def get_curl_response(url):
    buffer = BytesIO()
    curl = pycurl.Curl()
    curl.setopt(curl.URL, url)
    curl.setopt(curl.WRITEDATA, buffer)
    curl.perform()
    curl.close()
    response = buffer.getvalue()
    return response.decode('utf8')
