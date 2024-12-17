import requests
import warnings
from urllib3.exceptions import InsecureRequestWarning

# cooked up by
# Dominik Penner (@zer0pwn)
# &&& Jake Bolam (@xixasec)
# -------------------------
# rewrited by
# Sheryx00 (@sheryx00)


WHITE   = '\033[37m'
BLUE    = '\033[34m'
BLACK   = "\u001b[30m"
RED     = "\u001b[31m"
YELLOW  = "\u001b[33m"
MAGENTA = "\u001b[35m"
CYAN    = "\u001b[36m"
WHITE   = "\u001b[37m"
GREEN   = "\u001b[32m"
BOLD    = '\033[1m'
END     = '\033[0m'

class porchPirate():
    warnings.simplefilter('ignore', InsecureRequestWarning)
    def __init__(self, proxy=None):
        self.WS_API_URL = 'https://www.postman.com/_api/ws/proxy'
        self.WORKSPACE_API_URL = 'https://www.postman.com/_api/workspace'
        self.INDICE_KEYWORDS = {
            "workspace": "collaboration.workspace",
            "collection": "runtime.collection",
            "request": "runtime.request",
            "api": "adp.api",
            "flow": "flow.flow",
            "team": "apinetwork.team"
        }
        if proxy is not None:
            self.proxies = {
                'http': 'http://' + proxy,
                'https': 'http://' + proxy
            }
        else:
            self.proxies = None

    def search(self, term, page=None, indice=None, limit=100):
        if limit != 100:
            limit = int(limit)
        if page is not None:
            page = int(page)*limit
        else:
            page = 0
        search_headers = {
            "Content-Type": "application/json",
            "X-App-Version": "10.18.8-230926-0808",
            "X-Entity-Team-Id": "0",
            "Origin": "https://www.postman.com",
            "Referer": "https://www.postman.com/search?q=&scope=public&type=all",
        }
        
        if indice is not None:
            if indice in self.INDICE_KEYWORDS:
                queryIndices = [self.INDICE_KEYWORDS[indice]]
            else:
                raise ValueError("Invalid keyword provided for 'indice'")
        else:
            queryIndices = [
                "collaboration.workspace",
                "runtime.collection",
                "runtime.request",
                "adp.api",
                "flow.flow",
                "apinetwork.team"
            ]
        
        search_data = {
            "service": "search",
            "method": "POST",
            "path": "/search-all",
            "body": {
                "queryIndices": queryIndices,
                "queryText": "{0}".format(term),
                "size": limit,
                "from": page,
                "clientTraceId": "",
                "requestOrigin": "srp",
                "mergeEntities": "true",
                "nonNestedRequests": "true",
                "domain": "public"
            }
        }
        response = requests.post(self.WS_API_URL, headers=search_headers, json=search_data, proxies=self.proxies, verify=False)
        return response.text

    def search_stats(self, term):
        stat_headers = {
            "Content-Type": "application/json",
            "X-App-Version": "10.18.8-230926-0808",
            "X-Entity-Team-Id": "0",
            "Origin": "https://www.postman.com",
            "Referer": "https://www.postman.com/search?q=&scope=public&type=all",
        }
        stat_data = {
            "service":"search",
            "method":"POST",
            "path":"/count",
            "body": {
                "queryText":"{0}".format(term),
                "queryIndices":[
                    "collaboration.workspace",
                    "runtime.collection",
                    "runtime.request",
                    "adp.api",
                    "flow.flow",
                    "apinetwork.team"
                    ],
                "domain":"public"
            }
        }
        response = requests.post(self.WS_API_URL, headers=stat_headers, json=stat_data, proxies=self.proxies, verify=False)
        return response.text
    
    def build_curl_request(self, request):
        curl_request = f"curl -X {request['method']} '{YELLOW}{request['url']}{END}' \\\n"
        for header in request['headerData']:
            curl_request += f"-H '{YELLOW}{header['key']}{END}: {GREEN}{header['value']}{END}' \\\n"
        try:
            if request['auth']['type'] == 'basic':
                curl_request += f"-u '{GREEN}{request['auth']['basic'][1]['value']}{END}:{GREEN}{request['auth']['basic'][0]['value']}{END}' \\\n"
            elif request['auth']['type'] == 'oauth2':
                # add oauth2 oauth1 etc support
                pass
        except:
            pass
        if request['dataMode'] == 'params':
            for parameter in request['data']:
                curl_request += f"-d '{YELLOW}{parameter['key']}{END}={GREEN}{parameter['value']}{END}' "
        elif request['dataMode'] == 'raw':
            curl_request += f"--data-raw '{GREEN}{request['rawModeData']}{END}'"
        return curl_request

    def workspace(self, id):
        response = requests.get(f'https://www.postman.com/_api/workspace/{id}', proxies=self.proxies, verify=False)
        return response.text
    
    def workspace_globals(self, id):
        response = requests.get(f'https://www.postman.com/_api/workspace/{id}/globals', proxies=self.proxies, verify=False)
        return response.text
    
    def collection(self, id):
        response = requests.get(f'https://www.postman.com/_api/collection/{id}', proxies=self.proxies, verify=False)
        return response.text
    
    def collections(self, id):
        response = requests.post(f'https://www.postman.com/_api/list/collection?workspace={id}', proxies=self.proxies, verify=False)
        return response.text

    def request(self, id):
        response = requests.get(f'https://www.postman.com/_api/request/{id}', proxies=self.proxies, verify=False)
        return response.text
    
    def environment(self, id):
        response = requests.get(f'https://www.postman.com/_api/environment/{id}', proxies=self.proxies, verify=False)
        return response.text
    
    def profile(self, handle):
        header = {
            'Content-Type': 'application/json'
        }
        postdata = {
            "path": f'/api/profiles/{handle}',
            "service": "ums",
            "method": "get"
        }
        response = requests.post(self.WS_API_URL, json=postdata, headers=header, proxies=self.proxies, verify=False)
        return response.text
    
    def user(self, userid):
        headers = {
            'Content-Type': 'application/json'
        }
        postdata = {
            "service":"publishing",
            "method":"get",
            "path":f"/v1/api/profile/user/{userid}"
        }
        response = requests.post(self.WS_API_URL, json=postdata, headers=headers, proxies=self.proxies, verify=False)
        return response.text   
    
    def user_collections(self, userid):
        headers = {
            'Content-Type': 'application/json'
        }
        postdata = {
            "service":"publishing",
            "method":"get",
            "path":f"/v1/api/profile/user/{userid}?requestedData=collection"
        }
        response = requests.post(self.WS_API_URL, json=postdata, headers=headers, proxies=self.proxies, verify=False)
        return response.text

    def user_workspaces(self, userid):
        headers = {
            'Content-Type': 'application/json'
        }
        postdata = {
            "service":"publishing",
            "method":"get",
            "path":f"/v1/api/profile/user/{userid}?requestedData=workspace"
        }
        response = requests.post(self.WS_API_URL, json=postdata, headers=headers, proxies=self.proxies, verify=False)
        return response.text

    def team(self, teamid):
        headers = {
            'Content-Type': 'application/json'
        }
        postdata = {
            "service":"publishing",
            "method":"get",
            "path":f"/v1/api/profile/team/{teamid}"
        }
        response = requests.post(self.WS_API_URL, json=postdata, headers=headers, proxies=self.proxies, verify=False)
        return response.text
    
    def team_collections(self, teamid):
        headers = {
            'Content-Type': 'application/json'
        }
        postdata = {
            "service":"publishing",
            "method":"get",
            "path":f"/v1/api/profile/team/{teamid}?requestedData=collection"
        }
        response = requests.post(self.WS_API_URL, json=postdata, headers=headers, proxies=self.proxies, verify=False)
        return response.text

    def team_workspaces(self, teamid):
        headers = {
            'Content-Type': 'application/json'
        }
        postdata = {
            "service":"publishing",
            "method":"get",
            "path":f"/v1/api/profile/team/{teamid}?requestedData=workspace"
        }
        response = requests.post(self.WS_API_URL, json=postdata, headers=headers, proxies=self.proxies, verify=False)
        return response.text