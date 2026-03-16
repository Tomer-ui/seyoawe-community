# sawectl Overview

`sawectl` is the official Command Line Interface (CLI) and deep validation tool for SeyoAWE. It exists to manage, validate, and scaffold workflows and modules. By treating workflows as code (GitOps-native), `sawectl` ensures that all your definitions adhere to the formal DSL and module schemas before they are sent to the engine for execution.

## Responsibilities

1. **Workflow Validation**: Validates `workflow.yaml` files against `dsl.schema.json`. It also performs deep validation by checking if the action called in a step actually exists within the target module and if the inputs map correctly to the expected arguments.
2. **Module Validation**: Validates custom module manifests (`module.yaml`) against `module.schema.json`.
3. **Scaffolding/Templating**: Initializes empty or fully-templated workflow files and generates skeleton classes and YAML manifests for new custom modules.
4. **Triggering Workflows**: Runs an ad-hoc workflow against a running local or remote SeyoAWE Engine.

## Boundaries

- `sawectl` is primarily a client-side tool. It does **not** execute workflow steps or interact directly with the integrations (like Slack, Git, etc.). It strictly talks to the engine's `/api/adhoc` endpoint or to the file system to validate schemas.
- It parses Python source indirectly via manifestations mapping (the `module.yaml` defines what the python code expects).
