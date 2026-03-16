# sawectl Data Flow

This document outlines how `sawectl` processes, validates, and acts upon workflow definitions.

## Workflow Deep Validation Flow

```mermaid
sequenceDiagram
    participant User as CLI User
    participant CLI as sawectl.py
    participant DSL as dsl.schema.json
    participant ModManifest as module.yaml

    User->>CLI: validate-workflow my_wf.yaml
    CLI->>DSL: validate structure via jsonschema
    DSL-->>CLI: schema valid

    loop For each step in Workflow
        CLI->>CLI: Extract target action (e.g., slack.send_info_message)
        CLI->>ModManifest: Read manifest for target module
        CLI->>CLI: Validate method exists in manifest
        CLI->>CLI: Validate required arguments are provided
    end

    alt Validation Failed
        CLI-->>User: Exit 1, Error message (Missing argument)
    else Validation Succeeded
        CLI-->>User: Exit 0, "Validation Passed"
    end
```

## Workflow Execution (Ad-hoc run)

When triggering an ad-hoc run, the data flow simply consists of loading the YAML and posting it to the engine. The Engine is responsible for runtime execution.

```mermaid
sequenceDiagram
    participant CLI as sawectl.py
    participant FS as File System
    participant Engine as SeyoAWE Engine (localhost:8080)

    CLI->>FS: Load my_wf.yaml
    FS-->>CLI: YAML Data
    CLI->>Engine: POST /api/adhoc { "workflow": yaml_data }
    Engine-->>CLI: 200 OK (Execution queued)
    CLI-->>CLI: Print success
```

## Scaffolding (`init workflow --full`)

The full scaffolding process reads from both schemas and module directories to stitch together a comprehensive starting template.

1. **Load Schema**: Reads `dsl.schema.json` and recursively builds an empty dict structure using `$defs` definitions.
2. **Resolve Trigger**: Validates and assigns the `--trigger` flag directly into the template.
3. **Collect Steps**: Scans the `modules/` directory for `usage_reference.yaml` files.
4. **Assemble Workflow**: Populates the template `steps` list with real-world examples taken from the modules.
5. **Format YAML**: Writes back out to `workflows/<name>.yaml`, injecting custom spacing for readability.
