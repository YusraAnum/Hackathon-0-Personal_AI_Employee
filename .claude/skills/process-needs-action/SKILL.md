# Process Needs Action

## Description

Processes items in the Needs_Action folder of the AI Employee vault. This skill reads pending action items, analyzes them, and either processes them directly or creates approval requests for sensitive actions.

## Usage

Invoke this skill when you want to process pending items in the Needs_Action folder. The skill will:

1. Read all items from the Needs_Action folder
2. Analyze each item based on its type and metadata
3. Take appropriate action based on the Company_Handbook.md rules
4. Update the Dashboard.md with current status
5. Move completed items to the Done folder

## Instructions

1. **Read the vault path from environment** or use `vault/` as default
2. **List all files** in the Needs_Action folder
3. **For each file**:
   - Read the file contents and frontmatter metadata
   - Determine the item type (email, file_drop, etc.)
   - Check the Company_Handbook.md for rules on how to handle this type
   - If the action is auto-approved, process it
   - If the action requires approval, create a file in the appropriate folder
4. **Update Dashboard.md** with current status
5. **Move processed items** to Done folder

## Rules

- Always read Company_Handbook.md before taking any action
- Items marked as "high" priority should be flagged in the Dashboard
- Never take actions that require approval without explicit human consent
- Always log actions to the appropriate log file
- Maintain the file structure and naming conventions

## Output

After processing, provide a summary of:
- Number of items processed
- Items requiring human approval
- Items moved to Done
- Any errors or issues encountered
