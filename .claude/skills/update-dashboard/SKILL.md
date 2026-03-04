# Update Dashboard

## Description

Updates the AI Employee Dashboard.md with current status information. This skill scans the vault folders and provides a real-time summary of pending tasks, completed items, and system status.

## Usage

Invoke this skill to refresh the Dashboard with current information from:
- Needs_Action folder (pending items)
- Done folder (completed items)
- Logs folder (recent activity)
- Current system status

## Instructions

1. **Count items** in each folder:
   - Needs_Action: items awaiting processing
   - Done: items completed today
   - Plans: active plans

2. **Read recent logs** from today's log file (YYYY-MM-DD.json) to populate "Recent Activity"

3. **Update Dashboard.md** with:
   - Current date/time as "Last Updated"
   - Pending task counts
   - Completed today count
   - Recent activity list (last 10 actions)
   - System health status

4. **Maintain the template structure** - only update the data sections, preserve the formatting

## Template Sections to Update

- `Last Updated`: Current timestamp
- `Pending Tasks`: Count from Needs_Action
- `Completed Today`: Count from Done with today's date
- `Items in Needs_Action`: Count
- `Recent Activity`: Last 10 entries from logs
- `Current Tasks > Needs Action`: List items from Needs_Action
- `System Health`: Update component statuses

## Notes

- Use ISO format for timestamps (YYYY-MM-DD HH:MM:SS)
- Keep the Dashboard.md format consistent
- Don't modify the Quick Links section
- Always preserve the markdown formatting
