```
## 🔐 Unauthenticated Metadata Disclosure in Block Visibility Plugin

Title:
Unauthenticated Metadata Disclosure via REST API in Block Visibility Plugin

Summary:
A vulnerability was discovered in the Block Visibility – Conditional Visibility Control for the Block Editor plugin (tested on version 3.7.1), which exposes sensitive internal configuration data via a publicly accessible REST API endpoint:

  GET /wp-json/block-visibility/v1/variables

This endpoint is accessible without authentication due to an insecure permission callback, allowing any remote attacker to retrieve:

- Full list of registered user roles (including custom roles from plugins like WooCommerce, Timetics, Eventin, etc.)
- WooCommerce product metadata (IDs and names)
- Integration states (EDD, ACF, WP Fusion)
- Plugin settings (including plugin version and admin settings page URL)

This exposure can assist in reconnaissance, targeted attacks, and crafting access control bypasses.

Usage:
An unauthenticated user can access the endpoint directly using tools like curl, a browser, or any HTTP client to retrieve structured JSON data from:

  https://targetsite.com/wp-json/block-visibility/v1/variables

No authentication, nonce, or permission check is required. The data returned may include custom business logic, product groupings, or user segmentation that can aid in exploitation or information gathering.

Mitigation:
Plugin developers should apply proper access control by updating the REST API route registration to restrict access to authenticated users only. For example:

  'permission_callback' => function () {
      return current_user_can('edit_posts');
  }

Additionally, plugin responses should avoid disclosing sensitive data (like full product labels or role names) unless explicitly required by a validated user action.

Discovered by: Mrj Haxcore
```
