# sawectl API Reference

`sawectl` is a CLI tool. This reference outlines all available commands, flags, and their behaviors.

### Global Options

- `-h, --help`: Show help message and exit.
- `-v, --version`: Show version and exit.

---

### `sawectl init module`

Create a new custom module, generating a `module.yaml`, a Python class, and a `usage_reference.yaml`.

```bash
sawectl init module <name> [--modules <path>]
```

**Arguments:**
- `name` (required): The name of the module to create (e.g. `slack_module`).
- `--modules`: Path to the directory where the module should be created (default: `modules`).

**Example Usage:**
```bash
python sawectl.py init module auth_module
```

---

### `sawectl init workflow`

Scaffold a new workflow definition file.

```bash
sawectl init workflow <name> [flags]
```

**Arguments:**
- `name` (required): The base name for the workflow file.
- `--minimal`: Generates a barebones workflow with one logger step.
- `--full`: Generates an exhaustive workflow leveraging `$defs` in the DSL schema and injecting real step examples from installed modules.
- `--modules <csv>`: Comma-separated list of module names to include when using `--full`.
- `--modules-path <path>`: Directory containing modules (default: `modules`).
- `--workflows-path <path>`: Output directory for the workflow file (default: `workflows`).
- `--trigger <type>`: Type of trigger for the workflow. Options: `api`, `git`, `scheduled`, `ad-hoc` (default: `api`).

**Example Usage:**
```bash
python sawectl.py init workflow my_onboarding --full --trigger ad-hoc
```

---

### `sawectl run`

Triggers an ad-hoc execution of a given workflow against the SeyoAWE Engine.

```bash
sawectl run --workflow <file> --server <host:port>
```

**Arguments:**
- `--workflow` (required): Path to the YAML file to run.
- `--server` (required): Address of the running engine.

**Example Usage:**
```bash
python sawectl.py run --workflow workflows/my-workflow.yaml --server localhost:8080
```

---

### `sawectl validate-workflow`

Performs deep validation on a workflow file. It checks syntax against the DSL schema, and semantics against the manifests of the modules it references.

```bash
sawectl validate-workflow --workflow <file> [flags]
```

**Arguments:**
- `--workflow` (required): Path to the YAML file.
- `--modules`: Path to the installed modules directory (default: `modules`).
- `--verbose`: Prints success validations for every step.

**Example Usage:**
```bash
python sawectl.py validate-workflow --workflow workflows/my-workflow.yaml --verbose
```

---

### `sawectl validate-modules`

Iterates over all directories inside the modules path and ensures that every `module.yaml` manifest adheres to the `module.schema.json`.

```bash
sawectl validate-modules [--modules <path>]
```

**Arguments:**
- `--modules`: Path to the installed modules directory (default: `modules`).

**Example Usage:**
```bash
python sawectl.py validate-modules
```
