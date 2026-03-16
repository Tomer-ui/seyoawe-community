# sawectl Architecture

## Internal Structure

`sawectl` is implemented as a single Python script (`sawectl/sawectl.py`) alongside two JSON schemas that enforce the structural integrity of SeyoAWE.

### Key Components

1. **`sawectl.py`**: The main entry point. Uses `argparse` to interpret commands and flags.
2. **`dsl.schema.json`**: The JSON Schema representation of a SeyoAWE Workflow. Defines how steps, triggers, error handling, and conditions must be structured.
3. **`module.schema.json`**: The JSON Schema representation of a SeyoAWE Module Manifest (`module.yaml`).

### Command Handlers

The architecture revolves around isolated command handlers within `sawectl.py`:

- **`validate_workflow_deep(args)`**:
  - Loads a target workflow YAML.
  - Validates it against `dsl.schema.json`.
  - Iterates through `steps`, verifying duplicate IDs.
  - For each step, it resolves the targeted module (`action: "slack_module.send_info_message"`).
  - Loads the corresponding `module.yaml` and checks if the `send_info_message` method exists and if required inputs are provided.

- **`init_workflow(args)`**:
  - Dynamically builds an example workflow.
  - If `--full` is specified, it parses the DSL schema to generate boilerplate, resolving references using `$defs`.
  - Also pulls usage examples defined in modules (`usage_reference.yaml`) to inject concrete step implementations.

- **`init_module_from_schema(args)`**:
  - Creates a scaffold for a new module.
  - Generates the python class file, the `module.yaml` manifest, and an initial `usage_reference.yaml`.

- **`run_workflow(args)`**:
  - Performs a simple `POST` request to the SeyoAWE engine to trigger an ad-hoc run.

## Design Decisions

- **JSON Schema Over Code Assertions**: By delegating structural validation to `jsonschema` (Draft202012), `sawectl` guarantees that the validation logic remains declarative.
- **Deep Validation**: Instead of just syntactic checks, deep validation cross-references the DSL configuration with the installed modules, preventing runtime errors related to missing methods or arguments.
- **Standalone execution**: The tool uses minimal external dependencies (`pyyaml`, `requests`, `jsonschema`) allowing easy installation without bringing in the heavier flask server dependencies.
