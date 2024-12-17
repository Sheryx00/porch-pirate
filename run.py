import argparse
import json
from core import porchPirate
import formats

def main():
    parser = argparse.ArgumentParser(
        description="Porch Pirate CLI Tool - A tool to fetch and manipulate workspace data."
    )

    # Verbosity argument
    parser.add_argument('-v', '--verbose', help="Increase output verbosity", action="store_true")

    # Group: Search Operations
    group_search = parser.add_argument_group('Search Operations')
    group_search.add_argument('-s', '--search', help="Search using a keyword", type=str)

    # Group: Workspace Operations
    group_workspace = parser.add_argument_group('Workspace Operations')
    group_workspace.add_argument('-w', '--workspace', help="Get workspace details by ID", type=str)
    group_workspace.add_argument('--globals', help="Get workspace globals by ID", action="store_true")
    group_workspace.add_argument('--collections', help="Get workspace collections by ID", action="store_true")

    # Group: Collection Operations
    group_collection = parser.add_argument_group('Collection Operations')
    group_collection.add_argument('--requests', help="Get collection requests by ID", action="store_true")
    group_collection.add_argument('--urls', help="Show URLs from collections", action="store_true")

    # Group: Miscellaneous Operations
    group_misc = parser.add_argument_group('Miscellaneous Operations')
    group_misc.add_argument('--dump', help="Dump raw JSON response", action="store_true")
    group_misc.add_argument('--raw', help="Print raw request details", action="store_true")
    group_misc.add_argument('--curl', help="Convert a request to cURL", action="store_true")

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
            results = p.search(args.search)
            formats.format_search(json.loads(results))

        # Workspace Operations
        if args.workspace:
            log("Fetching workspace details...")
            workspace = p.workspace(args.workspace)
            print(json.dumps(workspace, indent=4))

            if args.globals:
                log("Fetching workspace globals...")
                globals_data = p.workspace_globals(args.workspace)
                print(json.dumps(globals_data, indent=4))

            if args.collections:
                log("Fetching workspace collections...")
                collections = p.collections(args.workspace)
                print(json.dumps(collections, indent=4))

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
