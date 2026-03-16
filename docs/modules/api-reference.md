# Modules API Reference

This reference details the available built-in modules and their methods, derived from their respective `module.yaml` files.

## `api_module`

A generic HTTP client for REST requests.

### Methods

- **`call`**: Makes a single HTTP API request.
  - **Arguments**: `method` (string, required), `url` (string, required), `headers` (dict), `params` (dict), `json` (dict), `data` (dict), `timeout` (int).
  - **Returns**: Status (`ok`, `fail`), message, and response data.

- **`blocking_call`**: Makes a blocking/polling API request, waiting for a condition to be met.
  - **Arguments**: `method` (string, required), `url` (string, required), `headers` (dict), `params` (dict), `body` (dict), `poll_interval_seconds` (int, default: 10), `timeout_minutes` (int, default: 5), `polling_mode` (string, default: "status_code"), `expected_status_code` (int, default: 200), `success_condition` (dict).
  - **Returns**: Status (`success`, `timeout`, `fail`), and response data.

## `slack_module`

Integration for sending Slack notifications and incident alerts.

### Methods

- **`send_info_message`**: Sends an informational Slack message with optional fields or flattened form data.
  - **Arguments**: `channel` (string, required), `title` (string, required), `message` (string), `keyed_message` (list), `flatten_form_result` (boolean), `color` (string, default: "info"), `webhook_url` (string).
  - **Returns**: Status and message.

- **`send_incident_message`**: Sends an incident alert to Slack with severity and on-call details.
  - **Arguments**: `channel` (string, required), `message` (string, required), `severity` (string), `oncall_user` (string).
  - **Returns**: Status and message.

*(Note: Additional modules like `git_module`, `chatbot_module`, `email_module`, etc., follow the same structural pattern. Consult their respective `module.yaml` files in the `modules/` directory for full argument lists.)*
