import requests
import json
import argparse

def fetch_variables(base_url, integration=None, search_term=None, saved_values=None):
    endpoint = f"{base_url}/wp-json/block-visibility/v1/variables"
    params = {}

    if integration:
        params["integration"] = integration
    if search_term:
        params["search_term"] = search_term
    if saved_values:
        params["saved_values"] = saved_values

    try:
        response = requests.get(endpoint, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"[!] Request failed: {e}")
        return None

def pretty_print(data, indent=2):
    print(json.dumps(data, indent=indent))

def main():
    parser = argparse.ArgumentParser(description="Block Visibility REST API Enumerator")
    parser.add_argument("url", help="Target base URL (e.g., https://example.com)")
    parser.add_argument("-i", "--integration", help="Integration to test (e.g., woocommerce, edd, wp_fusion)")
    parser.add_argument("-s", "--search", help="Search term for product/tag enumeration")
    parser.add_argument("--saved", help="Comma-separated saved values (optional)")

    args = parser.parse_args()
    result = fetch_variables(args.url.rstrip("/"), args.integration, args.search, args.saved)

    if result:
        print("\n[+] Response from /variables endpoint:\n")
        pretty_print(result)
    else:
        print("[!] No data returned or error occurred.")

if __name__ == "__main__":
    main()