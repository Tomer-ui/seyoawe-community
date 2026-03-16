# Modules Architecture

## Internal Structure

A SeyoAWE module is composed of a directory containing at least three essential files:

1. **`module.yaml` (Manifest)**: Defines the module's identity, methods, and schema.
2. **`[module_name].py` (Implementation)**: The Python class that executes the logic.
3. **`usage_reference.yaml` (Examples)**: Used by `sawectl` to generate full workflow templates.

### The `module.yaml` Manifest

This file is the contract between the module and the SeyoAWE engine. It is validated against the `module.schema.json`.

```yaml
name: mymodule
class: Mymodule
version: 1.0
author: Developer Name

methods:
  - name: execute_task
    description: Describes what this method does.
    arguments:
      - name: param1
        type: string
        required: true
    returns:
      type: object
      structure:
        status: one_of(['ok', 'fail', 'warn'])
        message: string
        data: object
```

### The Python Implementation

The Python class must exactly match the `class` name specified in the manifest. It must accept `context` and `**module_config` in its constructor.

```python
class Mymodule:
    def __init__(self, context, **module_config):
        self.context = context
        self.config = module_config or {}

    def execute_task(self, param1):
        try:
            # Business logic here
            return {
                "status": "ok",
                "message": "Task succeeded",
                "data": {"result": param1.upper()}
            }
        except Exception as e:
            return {
                "status": "fail",
                "message": str(e),
                "data": None
            }
```

## Design Decisions

- **Standardized Returns**: All methods must return a dictionary with `status`, `message`, and `data`. This standardization allows the engine to uniformly handle successes, failures, and context updates regardless of the underlying action.
- **Context Injection**: The `context` object is passed into the module upon initialization. This allows the module to access workflow-level variables (like `context.default_api_token`) or previous step outputs without explicitly requiring them as arguments.
- **Config Driven**: Modules receive their global configuration (from `config.yaml`) via `**module_config`, allowing secrets and defaults to be managed centrally rather than hardcoded in workflows.
