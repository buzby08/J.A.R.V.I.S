import webbrowser
from typing import Union

import requests

import speech


def open_website(message: str) -> int:
    """
    This will open a specific website depending on the parameters.
    
    Parameters: 
        message: str - This is the message that you have, and then this
            function will decide what website to open.
    
    Returns:
        int - A 0 for success, or a number < 0 for an error.
    """

    web_links: dict[str, str] = {
        "instagram": "https://www.instagram.com/",
        "facebook": "https://www.facebook.com/",
        "google": "https://www.google.com/",
        "messages": "https://messages.google.com/web/authentication",
        "maps": "https://www.google.co.uk/maps/",
        "whatsapp": "https://web.whatsapp.com/",
        "chat gpt": "https://chatgpt.com/"
    }

    for name, website in web_links.items():
        if name in message:
            speech.say(f"Opening {name}")
            webbrowser.open(website, 2)
            return 0
            

    return -1


def wikipedia_search(message: str) -> int:    
    language_code = 'en'
    search_query = message
    number_of_results = 1
    headers = {
      # 'Authorization': f'Bearer {access_token}',
      'User-Agent': 'J.A.R.V.I.S (lbusby685+wikipedia@gmail.com)'
    }
    
    base_url = 'https://api.wikimedia.org/core/v1/wikipedia/'
    endpoint = '/search/page'
    url = base_url + language_code + endpoint
    parameters = {'q': search_query, 'limit': number_of_results}
    response = requests.get(url, headers=headers, params=parameters)
    data = response.json()

    page = data['pages'][0]

    page_key = page['key']

    summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{page_key}"

    summary_data = requests.get(summary_url)
    summary = summary_data.json()['extract']

    speech.say(str(summary))
    
    
    return 0


def search(querey: str, browser: int = 0) -> int:
    """
    This is designed to search an item using the webbrowser.
    
    Parameters:
        querey: str - The message you want to search.
        browser: int - The search engine to use.
                        0: Google.com
                        1: Bing.com
                        2. DuckDuckGo.com
                        3. Yahoo.com
                        4. YouTube.com"""
    new_querey = ""
    for word in querey.strip().split(" "):
        new_querey += word
        new_querey += "+" if word != " " else ''

    if new_querey.endswith('+'):
        new_querey = new_querey[:-1]
        
    google: str = f"https://www.google.com/search?q={new_querey}"
    bing: str = f"https://www.bing.com/search?q={new_querey}"
    duckduckgo: str = f"https://duckduckgo.com/?t=h_&q={new_querey}&ia=web"
    yahoo: str = f"https://uk.search.yahoo.com/search?p={new_querey}"
    youtube: str = f"https://www.youtube.com/results?search_query={new_querey}"

    url: Union[tuple[str, str], None] = None
    
    if browser == 0: url = (google, "Google")
    if browser == 1: url = (bing, "Bing")
    if browser == 2: url = (duckduckgo, "Duck Duck Go")
    if browser == 3: url = (yahoo, "Yahoo")
    if browser == 4: url = (youtube, "YouTube")

    if url is None:
        return -1

    speech.say(f"Searching {querey.strip()} on {url[1]}.")
    
    webbrowser.open(url[0])
    
    return 0


client_ID = 'f287bb8a692f97349119a0c7b1807328'
client_secret = 'eef7909d133bb958c7483d56c6ff7defbf1628ef'
access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJmMjg3YmI4YTY5MmY5NzM0OTExOWEwYzdiMTgwNzMyOCIsImp0aSI6ImRiN2U3YjQwZDgwYTc2NjU0M2YxNGIyOTNhOGNjMWZkZGQyNDUxOWI1NmVkMTdiZTVmNWM1YTlmZTQxODYwYzcxMDFlYjk1ZWRlNWQ5ZjFkIiwiaWF0IjoxNzE3ODQzMDA3LjQxMzIyOSwibmJmIjoxNzE3ODQzMDA3LjQxMzIzMywiZXhwIjozMzI3NDc1MTgwNy40MTA5MDQsInN1YiI6Ijc1ODMzNTI4IiwiaXNzIjoiaHR0cHM6Ly9tZXRhLndpa2ltZWRpYS5vcmciLCJyYXRlbGltaXQiOnsicmVxdWVzdHNfcGVyX3VuaXQiOjUwMDAsInVuaXQiOiJIT1VSIn0sInNjb3BlcyI6WyJiYXNpYyJdfQ.Rguf7N5YWwJWwlryIg_3j2nj3dQW0D_E5jzkt7AfnSl1dM5RBEby4miZXXsMBZQMeV5K9cW22ZxSaRgFG5APXFweXuTAj4yvvhY1jaj27gpOo04Qj7S78NXJCGUAQNq8bWEY0ykYZKSeKlid-uJl246LP_zy3tYLp900rvpp6y_VWN17puebuDSCqQVaDcWZV2CehIyboCPG9PXr6b-zrhUUom403p8oXdETPGuYU-Nk_kMCn66Z_PZNEmLjcLcElY8V91C-iX05kHUzb1QJL9N6gMTzlrzPH0XRYTQyb6h01wA_Z9oZnYZ2s4bJBwzUn88pQaXqJ8Ok0syUUSyH4nDzzDmsOdrqQ3Te0zav4Va7k9SDNYznS2Hr-q3EFklwCcFMC-D4Ccg1pFWigi272tM8luE59EIYIcS-Iu_7JirAtlqMBSRF65U1y-eHgHqKh_I88c_rp1YF3EGmDZ4fkO021FYotpayEOMw-ifzilPHbip9mZUnF7MHi8wBP8NaTeTV01sBbdhoYE9GZ2e35bwqXBHhLu70sFKfz_FevOT_fGb6IV7ryTLXKpQCwweNFAi7d0hwLHmmqCl8iJ5Kbz51kA0RZHiF0m8KD4H6n4Jujqcs_34WdjKUecYTHKiYq2nOpSDoKo6p0swEpSOlgozg8moMtI7B1IDMXMw88Oo'

