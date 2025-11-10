# Custom GitHub Copilot Agents with MCP Servers

This repository demonstrates how to set up custom GitHub Copilot agents that integrate with Model Context Protocol (MCP) servers.

## What are Custom GitHub Copilot Agents?

Custom agents extend GitHub Copilot's capabilities by providing specialized tools and domain-specific knowledge. They can be configured to use external tools, APIs, and MCP servers to perform complex tasks beyond standard code completion.

For more details on custom agents, see:
- [GitHub Copilot Custom Agents Documentation](https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-custom-agents)
- [Awesome Copilot Agents Collection](https://github.com/github/awesome-copilot/tree/5cfe2e26159bcd4015ba4c8bdf18fff2a268049c/agents)

## Critical: Organization-Level Setup for MCP Servers

**IMPORTANT**: If your agent uses MCP servers, it MUST be created at the **organization level** in a **private `.github-private` repository**.

Individual repository-level agents cannot access MCP servers and will not work.

### Repository Structure

Your organization should have:
```
<your-org>/.github-private/
└── copilot/
    └── agents/
        ├── your-agent-1.md
        └── your-agent-2.md
```

## Example Agents

This repository includes two example agents that demonstrate different approaches to running MCP servers:

### 1. Docker-Based Agent (`neo4j-docker-client-generator.md`)

Located in `org-setup-files/agents/neo4j-docker-client-generator.md`

This agent runs the MCP server inside a Docker container:

```yaml
mcp-servers:
  neo4j-local:
    type: 'local'
    command: 'docker'
    args: [
      'run',
      '-i',
      '--rm',
      '-e', 'NEO4J_URI',
      '-e', 'NEO4J_USERNAME',
      '-e', 'NEO4J_PASSWORD',
      '-e', 'NEO4J_DATABASE',
      '-e', 'NEO4J_NAMESPACE=neo4j-local',
      '-e', 'NEO4J_TRANSPORT=stdio',
      'mcp/neo4j-cypher:latest'
    ]
    env:
      NEO4J_URI: '${COPILOT_MCP_NEO4J_URI}'
      NEO4J_USERNAME: '${COPILOT_MCP_NEO4J_USERNAME}'
      NEO4J_PASSWORD: '${COPILOT_MCP_NEO4J_PASSWORD}'
      NEO4J_DATABASE: '${COPILOT_MCP_NEO4J_DATABASE}'
    tools: ["*"]
```

### 2. Python Direct Agent (`neo4j-local-client-generator.md`)

Located in `org-setup-files/agents/neo4j-local-client-generator.md`

This agent runs the MCP server directly as a Python command:

```yaml
mcp-servers:
  neo4j-python:
    type: 'local'
    command: 'mcp-neo4j-cypher'
    args: ['--transport', 'stdio', '--namespace', 'neo4j-python']
    env:
      NEO4J_URI: '${COPILOT_MCP_NEO4J_URI}'
      NEO4J_USERNAME: '${COPILOT_MCP_NEO4J_USERNAME}'
      NEO4J_PASSWORD: '${COPILOT_MCP_NEO4J_PASSWORD}'
      NEO4J_DATABASE: '${COPILOT_MCP_NEO4J_DATABASE}'
    tools: ["*"]
```

### Agent File Layout

Each agent definition follows this structure:

```yaml
---
name: agent-name
description: Brief description of what the agent does
tools: ['read', 'edit', 'search', 'shell', 'mcp-server-name/*']
mcp-servers:
  server-name:
    type: 'local'
    command: 'command-to-run'
    args: ['arg1', 'arg2']
    env:
      VAR_NAME: '${ENVIRONMENT_VARIABLE}'
    tools: ["*"]
---

# Agent Instructions

Your agent's detailed instructions go here...
```

## Environment Variables Configuration

Getting environment variables to work correctly with MCP servers requires careful configuration. After extensive testing, this format works reliably:

### 1. Create Environment Variables at Organization Level

Create these environment variables in your GitHub organization settings:

- `COPILOT_MCP_NEO4J_URI`
- `COPILOT_MCP_NEO4J_USERNAME`
- `COPILOT_MCP_NEO4J_PASSWORD`
- `COPILOT_MCP_NEO4J_DATABASE`

**Important**: Use the `COPILOT_MCP_` prefix for all MCP-related variables.

### 2. Create Environment Variables in Repository

Also create the same environment variables at the repository level:

1. Go to Settings → Environments
2. Create an environment named `copilot`
3. Add all the same variables with their values

### 3. Configure Workflow Setup

The Python-based agent requires a GitHub Actions workflow to set up the Python environment. This is critical for agents that run MCP servers directly.

Create `.github/workflows/copilot-setup-steps.yml`:

```yaml
name: "Copilot Setup Steps"

on:
  workflow_dispatch:
  push:
    paths:
      - .github/workflows/copilot-setup-steps.yml

jobs:
  copilot-setup-steps:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install mcp-neo4j-cypher with pip
        run: |
          python3 -m pip install --upgrade pip
          python3 -m pip install mcp-neo4j-cypher

      - name: Verify mcp-neo4j-cypher installation
        run: |
          which mcp-neo4j-cypher
          mcp-neo4j-cypher --help || echo "mcp-neo4j-cypher installed"
```

This workflow ensures that the Python environment and required MCP server packages are available when Copilot agents execute.

## Summary Checklist

When setting up custom agents with MCP servers:

- [ ] Create agents in organization-level `.github-private` repository
- [ ] Define MCP server configuration with proper `command`, `args`, and `env` mapping
- [ ] Create `COPILOT_MCP_*` environment variables at organization level
- [ ] Create matching environment variables in repository settings under `copilot` environment
- [ ] Set up `.github/workflows/copilot-setup-steps.yml` for Python-based MCP servers
- [ ] Test agent with simple queries before deploying complex workflows

## Additional Resources

- [MCP Protocol Documentation](https://modelcontextprotocol.io/)
- [GitHub Copilot Extensions](https://github.com/features/copilot)
- [Neo4j MCP Server](https://github.com/neo4j-contrib/mcp-neo4j)
