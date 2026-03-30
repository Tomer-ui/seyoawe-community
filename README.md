# ⚙️ SeyoAWE — Universal Workflow Automation Engine

**Version:** 1.0  
**Author:** Yuri Bernstein  
**License:** Dual (Community Edition | Commercial Edition)  
**Website:** [seyoawe.dev](https://seyoawe.dev) *(Coming soon)*

---

## 🚀 What is SeyoAWE?

**SeyoAWE** is a modular, GitOps-native, human-in-the-loop automation platform.  
Define powerful, reliable workflows in YAML — with built-in support for approvals, forms, Git, APIs, Slack, and more.

### 🔥 What Makes SeyoAWE Different

- **Modular by Design**: Each Python module is a clear, composable unit.
- **GitOps-Native**: Treat workflows as code. Push to Git. Trigger via webhook or poll.
- **Human-in-the-Loop**: Slack approvals, webforms, dynamic approval links, and chatbot interactions built-in.
- **Crash-Resilient**: Persistent state, resumable runs, and detailed logs.
- **Pluggable**: Add your own modules in minutes. APIs, scripts, workflows, or UIs.

---

## 📦 Quickstart

### ✅ Requirements

**Engine:** no dependencies (pre-compiled binary)

**sawectl:**
- As a binary: no dependencies
- As a Python script: Python 3.10+

### 🚀 Setup

```bash
# 1. Set up the sawectl alias (once per shell)
alias sawectl="$PWD/sawectl/binaries/linux/sawectl"   # Linux
# alias sawectl="$PWD/sawectl/binaries/macos.arm/sawectl"   # Apple Silicon

# 2. Link webform assets (once after cloning)
cd modules/webform && ./link_assets.sh && cd ../..

# 3. Start the engine (from the repo root)
./run.sh linux   # or ./run.sh macos
```

This launches the SeyoAWE engine at `http://localhost:8080` and the webform asset server at `http://localhost:9000`.

The `configuration/config.yaml` is pre-configured with paths relative to the repo root:
```yaml
directories:
  workdir: .
  modules: ./modules
  workflows: ./workflows
  lifetimes: ./lifetimes
  logs: ./logs
```

---

## 🧬 Writing Your First Workflow

```bash
sawectl init workflow hello-world
```

Creates a scaffold in `workflows/default/hello-world.yaml`.

### 🧾 Example Workflow

```yaml
workflow:
  name: hello-world
  trigger:
    type: ad-hoc

  context_variables:
    - name: greeting
      type: string
      default: "Hello from SeyoAWE!"

  steps:
    - id: greet
      type: action
      action: command_module.Command.run
      input:
        command: "echo '{{ context.greeting }}'"
```

### 💡 Run it

```bash
sawectl run --workflow workflows/default/hello-world.yaml --server localhost:8080
```

---

## 🧰 sawectl CLI

The official CLI tool to manage, validate, and run workflows.

### 🔑 Common Commands

```bash
sawectl run --workflow <path.yaml> --server localhost:8080   # Run ad-hoc workflow
sawectl validate-workflow --workflow <wf.yaml>               # Deep schema + module validation
sawectl validate-modules                                     # Validate all module manifests
sawectl init workflow <name>                                 # Scaffold a new workflow
sawectl init module <name>                                   # Scaffold a custom module
```

---

## ⏰ Trigger System

| Trigger      | Description                                                            |
| ------------ | -----------------------------------------------------------------------|
| `api`        | Exposes an endpoint to receive and parse events                        |
| `git`        | Monitors Git repos (poll or webhook) for file changes                  |
| `scheduled`  | Uses cron syntax with for recurring workflows                          |
| `ad-hoc`     | Manually executed via CLI or UI                                        |

---

## 🧩 Modules

Modules are plug-and-play Python classes with full control.

### 📦 Built-In Modules

| Module             | Description                                         |
|--------------------|-----------------------------------------------------|
| `command_module`   | Execute shell commands                              |
| `webform`          | React-based approval form renderer                  |
| `slack_module`     | Sends messages and links via Slack                  |
| `email_module`     | Sends rich email notifications or approval requests |
| `api_module`       | Makes dynamic REST API calls                        |
| `git_module`       | GitOps actions: branches, commits, PRs              |
| `chatbot_module`   | Interacts with users using LLMs (OpenAI, Mistral)   |
| `logger`           | Simple logging module for workflow messages          |

---

### 🧑‍🔧 Build Your Own Module

```bash
sawectl init module mymodule
```

Creates:
```plaintext
modules/mymodule/
  ├── module.yaml
  └── mymodule.py
```

Edit `module.yaml`:
```yaml
name: mymodule
entrypoint: mymodule.py
description: My custom module
```

Edit `mymodule.py`:
```python
class Module:
    def execute(self, input_data, context, **kwargs):
        # do something here
        return {'status': 'ok', 'message': 'Success'}
```

Modules return:
- `ok` → step succeeded
- `fail` → halts workflow
- `warn` → logs warning, proceeds

---

## 🧾 Webforms & Approvals

Any step can pause for human approval:

```yaml
approval: true
delivery_step:
  module: slack
  config:
    message: "Please approve: {{ context.approval_link }}"
```

You can also define rich webforms with structured input. The engine waits, collects the form data, and resumes with `context.form_data`.

---

## 🧠 Workflow Context

The engine maintains a context object across steps.

- Use `context` to inject dynamic values
- Update context between steps
- Access previous results via `context.step_id.output`

---

## 🐞 Logs & Recovery

Each run generates:

- A UUID
- A lifetime state JSON file
- A full per-run log

```bash
lifetimes/3f21fa2b-...json
logs/run_3f21fa2b-...log
```

Crash? Restart the engine — it will resume in-place.

---

## 🎯 Real-World Use Cases

✅ CI/CD with approvals  
✅ Slack & email alerting  
✅ Integration with any system or tool using generic `api` and `command` modules
✅ GitOps PR automation  
✅ Multi-step integrations with manual gates

Involve human review(s) at any stage !
---

## 🔌 Communicating with SeyoAWE

There are three ways to interact with a running SeyoAWE engine:

### 1. sawectl CLI

The primary interface for workflow management and execution.

```bash
# Set up the alias (once per shell)
alias sawectl="$PWD/sawectl/binaries/linux/sawectl"

# Validate a workflow
sawectl validate-workflow --workflow workflows/default/hello-world.yaml

# Run a workflow against the engine
sawectl run --workflow workflows/default/hello-world.yaml --server localhost:8080

# Scaffold a new module and workflow
sawectl init module mymodule
sawectl init workflow my_flow --full --modules mymodule --trigger api
```

### 2. REST API

The engine exposes HTTP endpoints for triggering workflows programmatically.
Workflows with `trigger.type: api` register routes automatically at startup.

```bash
# Trigger a workflow via curl
curl -X POST http://localhost:8080/api/default/hello-world

# Trigger with a JSON payload (parsed by payload_parser in the workflow)
curl -X POST http://localhost:8080/api/default/employee_onboarding \
  -H "Content-Type: application/json" \
  -d '{"employee_name": "Jane", "role": "Engineer"}'

# Check engine health
curl http://localhost:8080/poll
```

The URL pattern is: `POST /api/<customer_id>/<workflow_name>`
where `customer_id` is set in `configuration/config.yaml` (default: `default`)
and `workflow_name` matches the YAML filename under `workflows/<customer_id>/`.

### 3. Webform UI

For human-in-the-loop workflows, the engine serves interactive web forms.

When a workflow reaches a `type: webform` step, it generates a **one-time approval link**:
```
http://localhost:8080/webform/<workflow_uid>/<step_id>/t.webform.html?config_file=<config>.js
```

This link is typically delivered via Slack or email (configured in the workflow's `delivery_step`).
The form collects user input and posts it back to the engine, which resumes the workflow
with the submitted data available at `context.<step_id>.status.form_data`.

The webform asset server runs on port **9000** (started automatically by `run.sh`).
To verify it's working:
```bash
curl -s -o /dev/null -w '%{http_code}' http://localhost:9000/webform_bundle.js
# Should return 200
```

### Quick Reference

| Method | When to Use | Example |
|--------|-------------|---------|
| **sawectl CLI** | Ad-hoc runs, validation, scaffolding | `sawectl run --workflow ... --server localhost:8080` |
| **REST API** | Automated triggers, webhooks, CI/CD integration | `curl -X POST http://localhost:8080/api/default/<wf>` |
| **Webform UI** | Human approvals, data collection forms | Delivered via Slack/email link, opened in browser |

---

## 📜 License

SeyoAWE is dual-licensed:

| Edition            | License       | Details                                                |
|--------------------|---------------|--------------------------------------------------------|
| **Community**      | Custom        | Free to use internally. No resale or monetization.     |
| **Commercial**     | Proprietary   | Adds DB, secrets, premium modules, premium support,    |
|                    |               | dashboards and reports and more.                       |

See [`LICENSE`](./LICENSE) for full details.

---

## 🙋 Get Involved

- 💡 Want to contribute a module? PR to `modules/`
- 🧪 Testing a module in a large org? Reach out for early access!
- 🧰 Using in a CI/CD pipeline? Tell us how it helped!

---

## 🏁 Final Word

SeyoAWE isn’t just another automation engine.

It’s a human-aware, Git-native, modular platform for teams who need infinitley flexible, yet simple automation solution

---

## DevOps Platform — CI/CD, Infrastructure & Monitoring

### Services & Tools Overview

#### GitHub Services

| Service | What For | Component |
|---------|----------|-----------|
| **GitHub Actions** (pipeline.yaml) | Unified pipeline: build, test, release, deploy | CI/CD |
| **GitHub Releases** | Version tagging & release management | CI/CD |
| **GitHub Artifacts** | Store/retrieve Terraform state between jobs | CI/CD |
| **GitHub Environments** | Teardown approval gate (protection rules) | CI/CD |
| **Docker Hub** | Container image registry (engine + CLI) | CI/CD |
| **Slack Webhooks** | CI/CD failure/success notifications | Notifications |
| **Jira API** | Auto-create bug tickets on pipeline failure | Notifications |

#### AWS Services

| Service | What For | Component |
|---------|----------|-----------|
| **EC2** | Compute for K8s nodes (t3.small) | Infrastructure |
| **EKS** | Managed Kubernetes cluster (v1.31) | Infrastructure |
| **VPC** | Network isolation (10.0.0.0/16, 2 subnets, 2 AZs) | Infrastructure |
| **Internet Gateway** | Public internet access for VPC | Infrastructure |
| **EBS + CSI Driver** | Persistent storage for engine logs (gp3) | Infrastructure |
| **IAM + OIDC/IRSA** | Roles for EKS, nodes, pod-level permissions | Infrastructure |
| **NLB** (via nginx ingress) | Network Load Balancer for external traffic | Infrastructure |

#### Tools

| Tool | What For | Component |
|------|----------|-----------|
| **Terraform** (v1.7.5) | Provision all AWS resources | IaC |
| **Ansible** | Node configuration & manifest deployment | IaC |
| **Prometheus** (v2.51.0) | Metrics collection & storage | Monitoring |
| **Grafana** (v10.4.1) | Metrics visualization & dashboards | Monitoring |
| **nginx ingress controller** (v1.11.3) | Route external traffic into cluster | Networking |

### Repository Structure

```
.github/workflows/
  pipeline.yaml         # Unified pipeline: Build → Test → Release → Deploy → Destroy
engine/Dockerfile       # Engine container (ubuntu:22.04 + seyoawe.linux binary)
cli/Dockerfile          # CLI container (python:3.11-slim + sawectl.py)
tests/
  engine/              # Unit, integration, e2e tests for the engine
  cli/                 # Unit, integration, e2e tests for the CLI
terraform/             # VPC + EKS cluster + node groups (app + monitoring)
ansible/
  playbooks/
    configure-nodes.yaml    # kubeconfig, StorageClass, node readiness
    deploy-manifests.yaml   # App + monitoring deployment to EKS
k8s/                   # Engine StatefulSet, CLI Deployment, Services, Ingress
monitoring/            # Prometheus + Grafana on dedicated monitoring node
```

### Pipeline (pipeline.yaml)

A single unified pipeline triggered on every push, with sequential stages:

```
Build → Unit Tests → Integration Tests → E2E Tests → Build & Release → Deploy → Teardown Gate → Destroy → Post Actions
```

1. **Build** — builds both Docker images (engine + CLI) and pushes them to Docker Hub with a `ci-<sha>` tag
2. **Unit Tests** — runs engine and CLI unit tests
3. **Integration Tests** — pulls the tested engine image, starts a container, runs integration tests for both components
4. **E2E Tests** — full end-to-end tests against a running engine container
5. **Build & Release** *(main branch only)* — promotes the tested images by re-tagging with the semantic version (no rebuild), creates a GitHub Release
6. **Deploy** — `terraform apply` → `ansible-playbook configure-nodes` → `ansible-playbook deploy-manifests`
7. **Teardown Gate** — manual approval button (GitHub Environment protection rule)
8. **Destroy** — cleans up ingress + monitoring namespaces then `terraform destroy`. Runs automatically on deploy failure (no approval needed)
9. **Post Actions** — always runs: Slack notification + Jira bug ticket on failure

If any stage fails, all downstream stages are skipped and Post Actions handles notifications.

### Infrastructure (Terraform)

- AWS VPC (10.0.0.0/16) with 2 public subnets across 2 AZs
- EKS cluster (v1.31) with EBS CSI driver (OIDC/IRSA)
- App node group: 2 x t3.small (single AZ for cost)
- Monitoring node group: 1 x t3.small, tainted `role=monitoring:NoSchedule`

### Kubernetes Architecture

| Workload | Kind | Node | Purpose |
|---|---|---|---|
| seyoawe-engine | StatefulSet | app nodes | Runs the engine binary, PVC for logs |
| seyoawe-cli | Deployment | app nodes | Stateless CLI utility |
| prometheus | Deployment | monitoring node | Scrapes cluster metrics via cAdvisor |
| grafana | Deployment | monitoring node | Dashboards (auto-provisioned) |

External access via nginx ingress controller (AWS NLB).

### Monitoring

Prometheus scrapes container CPU/memory/network metrics from all nodes via cAdvisor. Grafana boots with community dashboard [18283](https://grafana.com/grafana/dashboards/18283) ("Kubernetes cluster monitoring via Prometheus"), downloaded automatically at pod startup by an init container — no manual import required.

### GitHub Secrets Required

`DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`, `SLACK_WEBHOOK_URL`, `JIRA_API_TOKEN`, `JIRA_USER_EMAIL`, `JIRA_BASE_URL`, `JIRA_PROJECT_KEY`

---
