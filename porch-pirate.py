import argparse
import json
from core import porchPirate
import formats

def main():
    parser = argparse.ArgumentParser(
        description="Porch Pirate CLI Tool - A tool to fetch and manipulate workspace data."
    )

    # Arguments
    parser.add_argument('-v', '--verbose', help="Increase output verbosity", action="store_true")
    parser.add_argument('-s', '--search', help="Search using a keyword", type=str)
    parser.add_argument('-w', '--workspace', help="Get workspace details by ID", type=str)
    parser.add_argument('--globals', help="Fetch workspace globals recursively or by ID", action="store_true")
    parser.add_argument('--collections', help="Get workspace collections by ID", action="store_true")
    parser.add_argument('--requests', help="Get collection requests by ID", action="store_true")
    parser.add_argument('--urls', help="Show URLs from collections", action="store_true")
    parser.add_argument('--dump', help="Dump raw JSON response", action="store_true")
    parser.add_argument('--raw', help="Print raw request details", action="store_true")
    parser.add_argument('--curl', help="Convert a request to cURL", action="store_true")

    args = parser.parse_args()
    p = porchPirate()

    # Verbosity helper
    def log(message):
        if args.verbose:
            print(f"[DEBUG] {message}")

    try:
        # Search Functionality
        if args.search:
            log("Performing search...")
            results = json.loads(p.search(args.search))

            if not args.globals:
                formats.format_search(results)
            else:
                log("Fetching workspace globals recursively...")
                results_data = results.get('data', [])
                workspace_ids = []

                # Extract workspace IDs from the search results
                for result in results_data:
                    workspaces = result.get('document', {}).get('workspaces', [])
                    for workspace in workspaces:
                        workspace_ids.append(workspace['id'])

                # Fetch and display workspace globals for each ID
                for workspace_id in set(workspace_ids):  # Use set to remove duplicates
                    log(f"Fetching globals for workspace ID: {workspace_id}")
                    globals_data = json.loads(p.workspace_globals(workspace_id))
                    formats.format_globals(globals_data)

        # Workspace Operations
        if args.workspace:
            log("Fetching workspace details...")
            workspace = json.loads(p.workspace(args.workspace))
            formats.format_workspace(workspace)

            if args.globals:
                log("Fetching workspace globals...")
                globals_data = json.loads(p.workspace_globals(args.workspace))
                formats.format_globals(globals_data)


            if args.collections:
                log("Fetching workspace collections...")
                collections = json.loads(p.collections(args.workspace))
                formats.format_collection(collections)

        # Placeholder: Requests
        if args.requests:
            log("Fetching requests...")
            print("Feature not implemented yet. Please check back later.")
            exit(1)

        # Placeholder: URLs
        if args.urls:
            log("Extracting URLs...")
            print("Feature not implemented yet. Please check back later.")
            exit(1)

        # Placeholder: Dump Raw JSON
        if args.dump:
            log("Dumping raw JSON response...")
            print("Feature not implemented yet. Please check back later.")
            exit(1)

        # Placeholder: Raw Request Details
        if args.raw:
            log("Showing raw request details...")
            print("Feature not implemented yet. Please check back later.")
            exit(1)

        # Placeholder: Generate cURL Command
        if args.curl:
            log("Generating cURL command...")
            print("Feature not implemented yet. Please check back later.")
            exit(1)

    except Exception as e:
        print(f"Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
