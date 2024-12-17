import json

# Define color constants
WHITE   = '\033[37m'
BLUE    = '\033[34m'
BLACK   = "\u001b[30m"
RED     = "\u001b[31m"
YELLOW  = "\u001b[33m"
MAGENTA = "\u001b[35m"
CYAN    = "\u001b[36m"
GREEN   = "\u001b[32m"
BOLD    = '\033[1m'
END     = '\033[0m'

# Utility Functions
def format_header(title, color=BLUE, level=1):
    """Prints a styled header."""
    print(f"\n{BOLD}{color}{'='*level} {title} {'='*level}{END}")

def format_print(key, value, key_color=CYAN, value_color=WHITE):
    """Prints key-value pairs with consistent styling."""
    print(f"{BOLD}{key_color}{key}:{END} {value_color}{value}{END}")

def safe_get(data, keys, default=None):
    """Safely retrieves a nested key from a dictionary."""
    try:
        for key in keys:
            data = data[key]
        return data
    except (KeyError, IndexError, TypeError):
        return default

# Core Formatters
def format_workspace(workspace_results):
    data = workspace_results['data']
    profile = data['profileInfo']
    collections = data['dependencies']['collections']
    globals = workspace_results.get('globals', [])

    format_header(f"Workspace: {data['name']}")
    format_print("User", profile['publicName'])
    format_print("User ID", profile['profileId'])
    print()

    for environment in globals:
        name = environment['data'].get('name', "Globals")
        format_header(f"Environment: {name}", level=2)
        for e in environment['data'].get('values', []):
            format_print(e['key'], e['value'], value_color=GREEN)

    format_header(f"Collections ({len(collections)})")
    for collection in collections:
        format_print("Collection", collection, value_color=YELLOW)

def format_collection(collection):
    data = collection['data']
    format_header(f"Collection: {data['name']}")
    format_print("Collection ID", data['id'], value_color=YELLOW)
    format_print("Owner", data['owner'])
    format_print("Created At", data['createdAt'])
    format_print("Updated At", data['updatedAt'])

def format_request(request, requestid):
    format_header(f"Request: {request['name']}")
    format_print("Request ID", requestid)
    format_print("URL", request['url'])
    format_print("Method", request['method'])
    
    # Handle Headers
    for header in request.get('headerData', []):
        if header['value']:
            format_print(f"Header {header['key']}", header['value'], value_color=GREEN)

    # Handle Query Parameters
    for param in request.get('queryParams', []):
        format_print(f"Parameter {param['key']}", param['value'], value_color=GREEN)

    # Handle Authorization
    auth = request.get('auth', {}).get('type')
    if auth:
        format_print("Authorization", auth)

def format_user(profile, collections, workspaces):
    format_header("User Information")
    format_print("Username", profile['info']['slug'])
    format_print("Friendly", profile['info']['friendly'])
    format_print("User ID", profile['entity_id'])

    # Collections
    format_header("Collections", level=2)
    for entity in collections.get('data', {}).get('collections', []):
        format_print(entity['entityId'], entity['name'], value_color=YELLOW)

    # Workspaces
    format_header("Workspaces", level=2)
    for entity in workspaces.get('data', {}).get('workspaces', []):
        format_print(entity['entityId'], entity['name'], value_color=YELLOW)

def format_globals(global_results):
    format_print(key="Workspace", value=global_results['data']['workspace'])
    if 'data' not in global_results or 'values' not in global_results['data']:
        print(f"{RED}No globals found.{END}")
        return
    for idx, result in enumerate(global_results['data']['values'], 1):
        format_print(f"Global {idx}", f"{result.get('key', 'N/A')} = {result.get('value', 'N/A')}", value_color=GREEN)

def format_search(search_results):
    format_header("Search Results")
    if 'data' not in search_results or not search_results['data']:
        print(f"{RED}No results found.{END}")
        return

    fields = {
        "Entity Type": ["document", "entityType"],
        "Entity ID": ["document", "id"],
        "Name": ["document", "name"],
        "Author": ["document", "publisherHandle"],
        "Workspace": ["document", "workspaces", 0, "id"],
        "Description": ["document", "description"],
        "Last Updated": ["document", "updatedAt"]
    }

    for idx, result in enumerate(search_results['data'], 1):
        format_header(f"Result {idx}", level=2)
        for key, path in fields.items():
            value = safe_get(result, path, "N/A")
            format_print(key, value, value_color=YELLOW if "ID" in key else GREEN)
