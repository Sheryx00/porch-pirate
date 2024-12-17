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

def format_search(search_results):
    """
    Format and display search results in a human-readable format.
    :param search_results: JSON object containing the search results
    """
    if 'data' not in search_results or not search_results['data']:
        print("No results found.")
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
