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

`eninge`: none

`sawectl`:
  `binary`: none
  `python script`:
    - Python 3.10+


### 🚀 Running SeyoAWE (Local Engine)

```bash
./run.sh linux   # or ./run.sh macos
```

This launches the Flask-powered SeyoAWE runtime at `http://localhost:8080`.

Your `configurations/config.yaml` should point to:
```yaml
directories:
  workdir: /path/to/seyoawe-execution-plane
  modules: /path/to/seyoawe/modules
  workflows: /path/to/seyoawe/workflows
```

---

## 🧬 Writing Your First Workflow

```bash
sawectl workflow init hello-world
```

Creates a scaffold in `workflows/hello-world.yaml`.

### 🧾 Example Workflow

```yaml
name: hello-world
trigger:
  type: ad-hoc

context_variables:
  name: "Yura"

steps:
  - id: greet
    module: slack
    config:
      message: "Hello, {{ context.name }}! Welcome to SeyoAWE."
```

### 💡 Run it

```bash
sawectl run workflows/hello-world.yaml
```

---

## 🧰 sawectl CLI

The official CLI tool to manage, validate, and run workflows.

### 🔑 Common Commands

```bash
sawectl run <path.yaml>             # Run ad-hoc workflow
sawectl validate-workflow <wf.yaml> # Deep schema + module validation
sawectl list-modules                # View installed modules
sawectl workflow init <name>        # Scaffold a new workflow
sawectl module create <name>        # Scaffold a custom module
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

| Module     | Description                                         |
|------------|-----------------------------------------------------|
| `webform`  | React-based approval form renderer                  |
| `slack`    | Sends messages and links via Slack                  |
| `email`    | Sends rich email notifications or approval requests |
| `api`      | Makes dynamic REST API calls                        |
| `git`      | GitOps actions: branches, commits, PRs              |
| `chatbot`  | Interacts with users using LLMs (OpenAI, Mistral)   |

---

### 🧑‍🔧 Build Your Own Module

```bash
sawectl module create mymodule
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
| **GitHub Actions** (ci.yaml, cd.yaml) | Build, test, version, release, deploy pipelines | CI/CD |
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
  ci.yaml              # CI: build, test, version, push to Docker Hub
  cd.yaml              # CD: Terraform → Ansible → K8s deploy → destroy
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

### CI Pipeline (ci.yaml)

Triggered on every push. Two parallel jobs:

1. **engine-ci** — build Docker image, run unit tests, start container, run integration + e2e tests
2. **cli-ci** — build Docker image, run unit + integration tests, start engine, run e2e tests

If either fails: Slack notification + Jira bug ticket created automatically.

If both pass: **version-and-release** job bumps the semantic version, pushes both images to Docker Hub with matching tags, creates a GitHub Release, and triggers the CD pipeline.

### CD Pipeline (cd.yaml)

Three-job structure:

1. **deploy** — `terraform apply` (VPC + EKS + monitoring node) then `ansible-playbook configure-nodes` then `ansible-playbook deploy-manifests` (app + monitoring)
2. **teardown-gate** — manual approval button (GitHub Environment protection rule). Pauses so the live cluster can be inspected before destruction.
3. **destroy** — cleans up ingress + monitoring namespaces then `terraform destroy`. Runs automatically on deploy failure (no approval needed).

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

Prometheus scrapes container CPU/memory/network metrics from all nodes via cAdvisor. Grafana boots with a pre-provisioned "Seyoawe Cluster Overview" dashboard — no manual setup required.

### GitHub Secrets Required

`DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`, `SLACK_WEBHOOK_URL`, `JIRA_API_TOKEN`, `JIRA_USER_EMAIL`, `JIRA_BASE_URL`, `JIRA_PROJECT_KEY`

---
