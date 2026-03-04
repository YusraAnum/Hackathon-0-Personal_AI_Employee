# Personal AI Employee - Bronze Tier

An autonomous AI agent system that proactively manages personal and business affairs using Claude Code as the reasoning engine and Obsidian as the management dashboard.

## Architecture

The system follows a three-layer architecture:

1. **Perception Layer (Watchers)**: Lightweight Python scripts that monitor external sources and create actionable files
2. **Reasoning Layer (Claude Code)**: Reads from the vault, plans actions, and coordinates responses
3. **Action Layer (Agent Skills)**: Executes tasks and workflows

## Features (Bronze Tier)

- ✅ Obsidian vault with Dashboard.md and Company_Handbook.md
- ✅ File System Watcher for monitoring drop folder
- ✅ Basic folder structure (Inbox, Needs_Action, Done, Logs, Plans)
- ✅ Agent Skills for processing tasks and updating dashboard
- ✅ Local-first architecture with privacy focus

## Prerequisites

- Python 3.13+
- Claude Code (Pro subscription or free Gemini API)
- Obsidian (v1.10.6+)
- Node.js v24+ LTS (for future MCP servers)

## Setup

### 1. Clone or Download This Repository

```bash
cd Personal_Ai_Employee_FTEs
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
# Copy the example env file
cp .env.example .env

# Edit .env with your configuration
# At minimum, set:
# VAULT_PATH=<absolute_path_to_vault>
# DRY_RUN=true (for testing)
```

### 4. Open Obsidian with the Vault

1. Open Obsidian
2. Click "Open folder as vault"
3. Select the `vault` folder in this repository

### 5. Test the File System Watcher

```bash
# Test in dry-run mode (default)
python watchers/filesystem_watcher.py --vault vault --drop-folder drop_folder

# Test with actual file processing
python watchers/filesystem_watcher.py --vault vault --drop-folder drop_folder --no-dry-run
```

### 6. Test with Claude Code

```bash
# From the repository root
cd C:/Personal_Ai_Employee_FTEs

# Start Claude Code
claude

# In Claude Code, use the skills:
# /process-needs-action - Process items in Needs_Action
# /update-dashboard - Update the Dashboard with current status
```

## Folder Structure

```
Personal_Ai_Employee_FTEs/
├── vault/                      # Obsidian vault
│   ├── Inbox/                  # Raw input from watchers
│   ├── Needs_Action/           # Items requiring action
│   ├── Done/                   # Completed items
│   ├── Logs/                   # System logs
│   ├── Plans/                  # Planning documents
│   ├── Attachments/            # File attachments
│   ├── Dashboard.md            # Main dashboard
│   └── Company_Handbook.md     # Rules of engagement
├── watchers/                   # Python watcher scripts
│   ├── base_watcher.py         # Base class for watchers
│   └── filesystem_watcher.py   # File system monitor
├── drop_folder/                # Drop files here for processing
├── .claude/                    # Claude Code configuration
│   └── skills/                 # Agent skills
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
└── README.md                  # This file
```

## Usage

### Processing Dropped Files

1. Drop a file into the `drop_folder` directory
2. The File System Watcher will detect it and create an action item in `vault/Needs_Action/`
3. Use Claude Code with the `/process-needs-action` skill to process the item
4. The item will be categorized and either processed or marked for approval

### Using Agent Skills

From within Claude Code:

```
/process-needs-action
```

This will:
- Read all items in Needs_Action
- Process according to Company_Handbook.md rules
- Update Dashboard.md
- Move completed items to Done

```
/update-dashboard
```

This will:
- Scan all folders for current status
- Update the Dashboard with latest counts
- Show recent activity from logs

## Bronze Tier Checklist

- [x] Obsidian vault with Dashboard.md and Company_Handbook.md
- [x] One working Watcher script (File System Watcher)
- [x] Claude Code Agent Skills for processing
- [x] Basic folder structure: /Inbox, /Needs_Action, /Done, /Logs, /Plans
- [x] Environment configuration template
- [x] Documentation (README.md)

## Next Steps (Silver Tier)

To upgrade to Silver Tier, add:
- Gmail Watcher for email monitoring
- WhatsApp Watcher for message monitoring
- MCP server for sending emails
- Human-in-the-loop approval workflow
- Scheduling via cron or Task Scheduler
- Plan.md generation workflow

## Troubleshooting

### Claude Code can't find the vault
Make sure you're running Claude Code from the repository root directory, or specify the vault path with the `--cwd` flag.

### Watcher not detecting files
- Check that the drop_folder path is correct in .env
- Ensure the watcher is running
- Check the logs in `vault/Logs/` for errors

### Files not being processed
- Verify that Claude Code has access to the vault folder
- Check that the Agent Skills are properly installed in `.claude/skills/`
- Review the Company_Handbook.md for processing rules

## Security Notes

- Never commit the `.env` file to version control
- Use `DRY_RUN=true` for testing
- Credentials should be stored in environment variables only
- All actions are logged to `vault/Logs/` for audit

## Contributing

This is a personal AI Employee project. Customize the Company_Handbook.md and workflows to match your specific needs.

## License

This project is part of the Personal AI Employee Hackathon.

## Resources

- [Hackathon Document](Personal%20AI%20Employee%20Hackathon%200_%20Building%20Autonomous%20FTEs%20in%202026.md)
- [Claude Code Documentation](https://docs.anthropic.com/claude-code)
- [CLAUDE.md](CLAUDE.md) - Project-specific guidance for Claude Code

## Research Meetings

Join us every Wednesday at 10:00 PM:
- Zoom: https://us06web.zoom.us/j/87188707642?pwd=a9XloCsinvn1JzICbPc2YGUvWTbOTr.1
- Meeting ID: 871 8870 7642
- Passcode: 744832
- YouTube: https://www.youtube.com/@panaversity
