# Custom GitHub Copilot Agents with MCP Servers

This repository demonstrates how to set up custom GitHub Copilot agents that integrate with Model Context Protocol (MCP) servers.

## Testing MCP Servers Directly

Before creating custom agents, it can be useful to first test the MCP servers directly to ensure they're working correctly. This allows you to verify connectivity and functionality independently from the agent configuration.

See the [GitHub documentation on extending the coding agent with MCP](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/extend-coding-agent-with-mcp) for instructions on how to configure and test MCP servers locally.

This repository includes two example MCP server configurations for Neo4j in [`sample-mcp-config/`](sample-mcp-config/):
- [`neo4j-mcp-docker-config.json`](sample-mcp-config/neo4j-mcp-docker-config.json) - Docker-based MCP server configuration
- [`neo4j-mcp-local-config.json`](sample-mcp-config/neo4j-mcp-local-config.json) - Local Python-based MCP server configuration

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

### 1. Docker-Based Agent

See [`org-setup-files/agents/neo4j-docker-client-generator.md`](org-setup-files/agents/neo4j-docker-client-generator.md)

This agent runs the MCP server inside a Docker container.

### 2. Python Direct Agent

See [`org-setup-files/agents/neo4j-local-client-generator.md`](org-setup-files/agents/neo4j-local-client-generator.md)

This agent runs the MCP server directly as a Python command.

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

See [`.github/workflows/copilot-setup-steps.yml`](.github/workflows/copilot-setup-steps.yml) for the workflow configuration.

This workflow ensures that the Python environment and required MCP server packages are available when Copilot agents execute.

## Testing Your Custom Agent

Once your agent is configured, follow these steps to test it:

### 1. Create and Assign an Issue to Copilot

Create a new issue in your repository and assign it to Copilot.

**Important**: You must click away from the assignment dropdown after assigning to Copilot, then return to set the custom agent. The custom agent selection will not be available until you click out first.

![Assigning custom agent to issue](images/custom-agent.png)

### 2. Monitor Agent Startup

Give the agent a couple of minutes to start up. Once it begins, you'll see "Copilot started work on..." in the issue comments. Click on that link to see the status and logs.

![Finding custom agent logs](images/find-custom-agent-logs.png)

### 3. Verify MCP Server Connection

Once started, you'll see the agent connect to Neo4j and retrieve the schema, confirming that the MCP server integration is working correctly.

![Custom agent logs showing Neo4j connection](images/custom-agent-logs.png)

### 4. View Detailed Debug Logs

You can go to the Actions tab in your repository to see detailed debug logs for each agent run.

![Custom agent debug logs in Actions](images/custom-agent-debug-logs.png)

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
