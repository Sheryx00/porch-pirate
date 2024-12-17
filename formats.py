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
    data = safe_get(workspace_results, ['data'], {})
    profile = safe_get(data, ['profileInfo'], {})
    collections = safe_get(data, ['dependencies', 'collections'], [])
    globals = safe_get(workspace_results, ['globals'], [])

    format_header(f"Workspace: {safe_get(data, ['name'], 'Unknown')}")
    format_print("User", safe_get(profile, ['publicName'], 'N/A'))
    format_print("User ID", safe_get(profile, ['profileId'], 'N/A'))
    print()

    for environment in globals:
        name = safe_get(environment, ['data', 'name'], "Globals")
        format_header(f"Environment: {name}", level=2)
        for e in safe_get(environment, ['data', 'values'], []):
            format_print(safe_get(e, ['key'], 'N/A'), safe_get(e, ['value'], 'N/A'), value_color=GREEN)

    format_header(f"Collections ({len(collections)})")
    for collection in collections:
        format_print("Collection", collection, value_color=YELLOW)

def format_collection(collection):
    data = safe_get(collection, ['data'], {})

    format_header(f"Collection: {safe_get(data, ['name'], 'Unknown')}")
    format_print("Collection ID", safe_get(data, ['id'], 'N/A'), value_color=YELLOW)
    format_print("Owner", safe_get(data, ['owner'], 'Unknown'))
    format_print("Created At", safe_get(data, ['createdAt'], 'N/A'))
    format_print("Updated At", safe_get(data, ['updatedAt'], 'N/A'))

def format_request(request, requestid):
    format_header(f"Request: {safe_get(request, ['name'], 'Unnamed')}")
    format_print("Request ID", requestid)
    format_print("URL", safe_get(request, ['url'], 'N/A'))
    format_print("Method", safe_get(request, ['method'], 'N/A'))
    
    # Handle Headers
    for header in safe_get(request, ['headerData'], []):
        format_print(f"Header {safe_get(header, ['key'], 'N/A')}", safe_get(header, ['value'], ''), value_color=GREEN)

    # Handle Query Parameters
    for param in safe_get(request, ['queryParams'], []):
        format_print(f"Parameter {safe_get(param, ['key'], 'N/A')}", safe_get(param, ['value'], ''), value_color=GREEN)

    # Handle Authorization
    auth_type = safe_get(request, ['auth', 'type'], None)
    if auth_type:
        format_print("Authorization", auth_type)

def format_user(profile, collections, workspaces):
    format_header("User Information")
    format_print("Username", safe_get(profile, ['info', 'slug'], 'N/A'))
    format_print("Friendly", safe_get(profile, ['info', 'friendly'], 'N/A'))
    format_print("User ID", safe_get(profile, ['entity_id'], 'N/A'))

    # Collections
    format_header("Collections", level=2)
    for entity in safe_get(collections, ['data', 'collections'], []):
        format_print(safe_get(entity, ['entityId'], 'N/A'), safe_get(entity, ['name'], 'Unnamed'), value_color=YELLOW)

    # Workspaces
    format_header("Workspaces", level=2)
    for entity in safe_get(workspaces, ['data', 'workspaces'], []):
        format_print(safe_get(entity, ['entityId'], 'N/A'), safe_get(entity, ['name'], 'Unnamed'), value_color=YELLOW)

def format_globals(global_results):
    workspace = safe_get(global_results, ['data', 'workspace'], 'N/A')
    format_print("Workspace", workspace, value_color=YELLOW)

    values = safe_get(global_results, ['data', 'values'], [])
    if not values:
        print(f"{RED}No globals found.{END}")
        return

    for idx, result in enumerate(values, 1):
        format_print(f"Global {idx}", f"{safe_get(result, ['key'], 'N/A')} = {safe_get(result, ['value'], 'N/A')}", value_color=GREEN)

def format_search(search_results):
    format_header("Search Results")
    if not safe_get(search_results, ['data'], []):
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
