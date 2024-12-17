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

def format_globals(global_results):
    """
    Format and display workspace globals in a human-readable format.
    :param global_results: JSON object containing the global workspace values
    """
    if 'data' not in global_results or 'values' not in global_results['data']:
        print(f"{RED}No globals found.{END}")
        return

    workspace_id = global_results['data']['workspace']
    print(f"{BOLD}{BLUE}=== Workspace: {RED}{workspace_id} {BLUE}==={END}")
    for idx, result in enumerate(global_results['data']['values'], 1):
        key = result.get('key', f"{RED}No key available.{END}")
        value = result.get('value', f"{RED}No value available.{END}")

        # Display each global key-value pair
        print(f"{GREEN}Global {idx}:{END}")
        print(f"{CYAN}Key:{END} {WHITE}{key}{END}")
        print(f"{MAGENTA}Value:{END} {WHITE}{value}{END}\n")

def format_search(search_results):
    """
    Format and display search results in a human-readable format.
    :param search_results: JSON object containing the search results
    """
    if 'data' not in search_results or not search_results['data']:
        print(f"{RED}No results found.{END}")
        return

    for idx, result in enumerate(search_results['data'], 1):
        # Extract data with fallbacks
        name = result.get('document', {}).get('name', f"{RED}No name available.{END}")
        author = result.get('document', {}).get('publisherName', f"{RED}Unknown author.{END}")
        description = result.get('document', {}).get('description', f"{YELLOW}No description available.{END}")
        lastupdated = result.get('document', {}).get('updatedAt', f"{RED}No data available.{END}")

        # Display the formatted and colored output
        print(f"{BOLD}{BLUE}=== Search Result {idx} ==={END}")
        print(f"{GREEN}Item Name:{END} {WHITE}{name}{END}")
        print(f"{CYAN}Author:{END} {WHITE}{author}{END}")
        print(f"{MAGENTA}Last Updated:{END} {WHITE}{lastupdated}{END}")
        print(f"{YELLOW}Description:{END} {WHITE}{description}{END}\n")