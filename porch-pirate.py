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
    parser.add_argument('--requests', help="Get collection requests by ID")
    parser.add_argument('--urls', help="Show URLs from a collection ID",action="store_true")
    parser.add_argument('--dump', help="Dump raw JSON response", action="store_true")
    parser.add_argument('--raw', help="Print raw request details", action="store_true")
    parser.add_argument('--curl', help="Convert a request to cURL by ID", type=str)

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

        # Fetch Requests
        if args.requests:
            log(f"Fetching requests for collection ID: {args.requests}")
            collection_requests = json.loads(p.request(args.requests))
            formats.format_request(collection_requests, args.requests)

        # Show URLs from a Collection
        if args.urls:
            log(f"Extracting URLs from collection ID: {args.urls}")
            collection_data = json.loads(p.collection(args.workspace))
            requests = collection_data.get('data', {}).get('order', [])
            for request in requests:
                print(f"URL: {request['url']}")

        # Dump Raw JSON
        if args.dump:
            log("Dumping raw JSON response...")
            if args.workspace:
                response = p.workspace(args.workspace)
            elif args.requests:
                response = p.request(args.requests)
            elif args.search:
                response = p.search(args.search)
            else:
                print(f"[ERROR] No data source specified for dump.")
                return
            print(json.dumps(json.loads(response), indent=4))

        # Print Raw Request Details
        if args.raw:
            log(f"Showing raw request details for ID: {args.requests}")
            if not args.requests:
                print(f"[ERROR] --raw requires a collection request ID via --requests.")
                return
            raw_data = json.loads(p.request(args.requests))
            print(json.dumps(raw_data, indent=4))

        # Generate cURL Command
        if args.curl:
            log(f"Generating cURL command for request ID: {args.curl}")
            raw_request = json.loads(p.request(args.curl))
            curl_command = p.build_curl_request(raw_request)
            print("\nGenerated cURL Command:\n")
            print(curl_command)

    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
