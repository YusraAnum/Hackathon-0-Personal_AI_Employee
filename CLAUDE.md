# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Personal AI Employee (Digital FTE)** project - an autonomous agent system that proactively manages personal and business affairs 24/7. The system uses Claude Code as the reasoning engine and Obsidian as the management dashboard.

### Architecture: Perception → Reasoning → Action

The system follows a three-layer architecture:

1. **Perception Layer (Watchers)**: Lightweight Python scripts that monitor external sources (Gmail, WhatsApp, Bank APIs, file system) and create actionable files in the Obsidian vault
2. **Reasoning Layer (Claude Code)**: Reads from the vault, plans actions, and coordinates responses
3. **Action Layer (MCP Servers)**: Executes external actions like sending emails, posting to social media, making payments

## Required Software

- **Claude Code** (Pro subscription or free Gemini API via Claude Code Router)
- **Obsidian** v1.10.6+ (knowledge base & dashboard)
- **Python** 3.13+ (watcher scripts & orchestration)
- **Node.js** v24+ LTS (MCP servers)
- **GitHub Desktop** (version control for vault)

## Repository Structure

The repository uses an Obsidian vault as its central state store. Key folder structure:

```
/ (Vault Root)
├── Needs_Action/          # Items waiting for Claude to process
├── In_Progress/           # Items currently being worked on
├── Plans/                 # Claude-generated plan files
├── Pending_Approval/      # Sensitive actions awaiting human approval
├── Approved/              # Approved actions to execute
├── Rejected/              # Rejected actions
├── Done/                  # Completed items
├── Logs/                  # Audit logs (YYYY-MM-DD.json format)
├── Inbox/                 # Raw input from watchers
├── Dashboard.md           # Real-time summary and status
├── Company_Handbook.md    # Rules of engagement for AI behavior
└── Business_Goals.md      # Objectives and metrics for audits
```

## Development Commands

### Claude Code Operations
```bash
# Verify Claude Code installation
claude --version

# Run Claude Code pointing to vault
cd /path/to/AI_Employee_Vault
claude

# Trigger Ralph Wiggum loop for autonomous task completion
/ralph-loop "Process all files in /Needs_Action, move to /Done when complete" \
  --completion-promise "TASK_COMPLETE" \
  --max-iterations 10
```

### Python Watcher Development
```bash
# Set up UV Python project
uv init

# Install dependencies (when requirements.txt exists)
pip install -r requirements.txt

# Run a watcher script (for testing)
python gmail_watcher.py

# Run with PM2 for process management (recommended)
pm2 start gmail_watcher.py --interpreter python3
pm2 save
pm2 startup
```

### MCP Server Configuration
MCP servers are configured in `~/.config/claude-code/mcp.json`:

```json
{
  "servers": [
    {
      "name": "email",
      "command": "node",
      "args": ["/path/to/email-mcp/index.js"],
      "env": {
        "GMAIL_CREDENTIALS": "/path/to/credentials.json"
      }
    },
    {
      "name": "browser",
      "command": "npx",
      "args": ["@anthropic/browser-mcp"],
      "env": {
        "HEADLESS": "true"
      }
    }
  ]
}
```

## Key Architectural Patterns

### Base Watcher Pattern
All watchers extend `BaseWatcher` with these methods:
- `check_for_updates()` → Returns list of new items to process
- `create_action_file(item)` → Creates .md file in Needs_Action folder
- `run()` → Main loop with error handling and sleep interval

### Human-in-the-Loop (HITL) Pattern
For sensitive actions (payments, new contacts, bulk operations):
1. Claude creates approval request file in `/Pending_Approval/`
2. Human reviews and moves to `/Approved/` or `/Rejected/`
3. Orchestrator detects approved file and triggers MCP action

### File-Based Agent Communication (Platinum Tier)
For cloud-local agent coordination:
- Claim-by-move rule: First agent to move item from `/Needs_Action` to `/In_Progress/<agent>/` owns it
- Cloud writes updates to `/Updates/`, Local merges into `Dashboard.md`
- Single-writer rule for `Dashboard.md` (Local only)

### Ralph Wiggum Loop
A Stop hook pattern that keeps Claude iterating until task complete:
1. Creates state file with prompt
2. Claude works on task
3. On exit, hook checks: Is task file in `/Done`?
4. No → Block exit, re-inject prompt
5. Yes → Allow exit

## Security Requirements

### Credential Management
- **Never** store credentials in plain text or in the vault
- Use `.env` files (add to `.gitignore` immediately)
- Use OS credential managers for banking (Keychain, Credential Manager, 1Password CLI)
- Rotate credentials monthly and after suspected breaches

### Environment Variables Template
```bash
# .env - NEVER commit this file
GMAIL_CLIENT_ID=your_client_id
GMAIL_CLIENT_SECRET=your_client_secret
BANK_API_TOKEN=your_token
WHATSAPP_SESSION_PATH=/secure/path/session
DRY_RUN=true  # Set to false for production
```

### Permission Boundaries
| Action Category | Auto-Approve | Always Require Approval |
|-----------------|--------------|------------------------|
| Email replies | Known contacts | New contacts, bulk sends |
| Payments | <$50 recurring | All new payees, >$100 |
| Social media | Scheduled posts | Replies, DMs |
| File operations | Create, read | Delete, move outside vault |

## Audit Logging Format
All actions must be logged in `/Vault/Logs/YYYY-MM-DD.json`:
```json
{
  "timestamp": "2026-01-07T10:30:00Z",
  "action_type": "email_send",
  "actor": "claude_code",
  "target": "client@example.com",
  "parameters": {"subject": "Invoice #123"},
  "approval_status": "approved",
  "approved_by": "human",
  "result": "success"
}
```

## Hackathon Tiers

### Bronze (Foundation)
- Obsidian vault with Dashboard.md and Company_Handbook.md
- One working Watcher script
- Claude reading/writing to vault
- Basic folder structure

### Silver (Functional Assistant)
- Two+ Watcher scripts
- LinkedIn auto-posting
- Plan.md generation
- One MCP server for external actions
- HITL approval workflow
- Scheduling via cron/Task Scheduler

### Gold (Autonomous Employee)
- Cross-domain integration (Personal + Business)
- Odoo Community integration via MCP
- Facebook, Instagram, Twitter integration
- Multiple MCP servers
- Weekly Business Audit with CEO Briefing
- Error recovery and graceful degradation
- Comprehensive audit logging
- Ralph Wiggum loop

### Platinum (Always-On Cloud + Local)
- Cloud VM 24/7 operation
- Work-Zone specialization (Cloud: drafts, Local: approvals)
- Synced vault via Git/Syncthing
- Odoo on Cloud VM with HTTPS
- A2A messaging upgrade (optional)

## AI Functionality as Agent Skills

All AI functionality should be implemented as [Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview). Skills are reusable prompts that Claude can invoke to perform specific tasks.

Skills are located in `.claude/skills/` directory. Each skill has a `SKILL.md` file defining its behavior.

## Common Workflows

### Invoice Flow Example
1. WhatsApp Watcher detects "invoice" keyword → Creates `WHATSAPP_client_a_YYYY-MM-DD.md` in `/Needs_Action/`
2. Claude reads file → Creates plan in `/Plans/PLAN_invoice_client_a.md`
3. Claude generates invoice PDF → Creates approval request in `/Pending_Approval/EMAIL_invoice_client_a.md`
4. Human reviews → Moves to `/Approved/`
5. Orchestrator detects → Triggers Email MCP to send
6. Claude updates Dashboard → Moves files to `/Done/`

### Weekly CEO Briefing
1. Scheduled task (Sunday night) triggers Claude
2. Claude reads: `Business_Goals.md`, `/Tasks/Done/`, `/Accounting/Current_Month.md`
3. Generates briefing in `/Briefings/YYYY-MM-DD_Monday_Briefing.md`
4. Includes: Revenue summary, bottlenecks, proactive suggestions

## Error Recovery

### Retry Logic with Exponential Backoff
```python
def with_retry(max_attempts=3, base_delay=1, max_delay=60):
    # Retry decorator for transient errors
    # Network timeout, API rate limit
```

### Graceful Degradation
- Gmail API down: Queue emails locally
- Banking API timeout: Never auto-retry payments
- Claude unavailable: Watchers continue collecting
- Obsidian locked: Write to temp folder

## Research Meetings

Weekly research meetings every Wednesday at 10:00 PM via Zoom:
- Meeting ID: 871 8870 7642
- Passcode: 744832
- YouTube: https://www.youtube.com/@panaversity

## Learning Resources

- Claude Code features: https://agentfactory.panaversity.org/docs/AI-Tool-Landscape/claude-code-features-and-workflows
- Claude + Obsidian: https://www.youtube.com/watch?v=sCIS05Qt79Y
- MCP Quickstart: https://modelcontextprotocol.io/quickstart
- Agent Skills: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- Odoo 19 JSON-RPC API: https://www.odoo.com/documentation/19.0/developer/reference/external_api.html
- Ralph Wiggum reference: https://github.com/anthropics/claude-code/tree/main/.claude/plugins/ralph-wiggum
