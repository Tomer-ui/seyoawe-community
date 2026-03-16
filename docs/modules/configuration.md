# Modules Configuration

Modules receive their default configuration from the global SeyoAWE config file located at `configuration/config.yaml`. The engine parses this file and injects the corresponding dictionary into the module's constructor as `**module_config`.

## `config.yaml` Example Settings

Here are the standard configuration blocks for the built-in modules. Ensure these are set correctly in your environment.

```yaml
module_defaults:
  chatbot:
    provider: openai
    model: gpt-4
    temperature: 0.7
    api_key: ""

  api:
    timeout: 15
    headers:
      Content-Type: "application/json"
      Authorization: "Bearer {{ context.default_api_token }}"
    blocking_defaults:
      poll_interval_seconds: 5
      timeout_minutes: 3

  email_module:
    smtp_host: smtp.gmail.com
    smtp_port: 587
    smtp_user: your@email.com
    smtp_pass: ""
    from_addr: "SeyoAWE Bot <your@email.com>"

  slack_module:
    webhook_url: "https://hooks.slack.com/services/<your_webhook_url>"

  git_module:
    github_token: ""
```

## How It Works

When a workflow step triggers `slack_module.send_info_message`, the engine:
1. Instantiates `Slack(context, **module_config)`.
2. Passes the `module_defaults.slack_module` dict from `config.yaml` into `**module_config`.
3. The module can then fallback to these config values if they are not explicitly provided in the workflow step.

For instance, in `slack.py`:
```python
webhook_url = (
    webhook_url or                           # Provided in workflow step
    self.context.get("slack_webhook_url") or # Set in workflow context
    self.config.get("webhook_url")           # Injected from config.yaml
)
```
