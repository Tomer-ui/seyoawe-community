# Modules Overview

Modules are plug-and-play Python classes that provide execution capabilities to SeyoAWE workflows. They act as the bridge between the core workflow engine and external systems (like Slack, APIs, Git, or internal business logic).

## Responsibility

Each module is responsible for exactly one domain (e.g., interacting with a specific API, executing a specific script, sending an email). They receive inputs defined in a workflow step, execute their logic, and return a standardized result (`ok`, `fail`, `warn`) back to the engine.

## Boundaries

- Modules do not dictate the flow of execution; the engine does.
- Modules must not hold state across workflow steps. They operate on the inputs and the shared `context` object provided by the engine.
- Modules must expose a `module.yaml` manifest that accurately describes their available methods, expected arguments, and return structures. This is critical for `sawectl` to validate workflows before they run.

## Installed Modules

Based on the `modules/` directory, the following integrations are currently available:
- `api_module`: Generic HTTP client for REST requests.
- `slack_module`: Integration for sending Slack notifications and incidents.
- `git_module`: GitOps actions.
- `email_module`: Sending email alerts.
- `command_module`: Executing arbitrary CLI commands.
- `chatbot_module`: Interacting with LLMs (e.g., OpenAI).
- `delegate_remote_workflow`: Running remote SeyoAWE workflows.
- `webform`: Providing approval forms.
