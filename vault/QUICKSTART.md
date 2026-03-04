# How to Run & Test the Bronze Tier AI Employee

## Prerequisites Check

Before starting, ensure you have:
- Python 3.13+ installed
- Claude Code installed and working
- Obsidian installed (optional, for viewing the vault)

---

## Step 1: Set Up the Environment

```bash
# Navigate to the project directory
cd C:/Personal_Ai_Employee_FTEs

# Create a virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Step 2: Configure Environment (Optional)

```bash
# Copy the example env file
cp .env.example .env

# Edit .env if you want to customize paths
# Default settings work for testing
```

---

## Step 3: Open the Vault in Obsidian (Optional but Recommended)

1. Open Obsidian
2. Click "Open folder as vault"
3. Select: `C:/Personal_Ai_Employee_FTEs\vault`
4. Open `Dashboard.md` to see the real-time status

---

## Step 4: Test the File System Watcher

### Option A: Quick Test (Dry Run Mode)

```bash
# Run watcher in dry-run mode (logs actions but doesn't process)
python watchers/filesystem_watcher.py --vault vault --drop-folder drop_folder
```

### Option B: Full Test (Actual Processing)

```bash
# Run watcher with actual file processing
python watchers/filesystem_watcher.py --vault vault --drop-folder drop_folder --no-dry-run
```

**Keep the watcher running** in a terminal window.

---

## Step 5: Drop a Test File

While the watcher is running:

1. Create a test file in the `drop_folder`:

```bash
# Windows (in another terminal)
echo "This is a test invoice for $500" > drop_folder/test_invoice_2.txt
```

2. **Or manually:** Create any file and drag it to `C:/Personal_Ai_Employee_FTEs\drop_folder\`

---

## Step 6: Verify the Results

Within 30 seconds, you should see:

### In the Watcher Terminal:
```
[INFO] Copied file to: C:\...\vault\Attachments\20260304_XXXXXX_test_invoice_2.txt
[INFO] Created action file: C:\...\vault\Needs_Action\FILE_XXXXXX_test_invoice_2.txt.md
```

### In the Vault:
1. Check `vault/Needs_Action/` - New action file created
2. Check `vault/Attachments/` - Original file copied here
3. Check `vault/Logs/` - New log entry added
4. Check `drop_folder/` - Original file removed

---

## Step 7: Process with Claude Code

### Option A: Using Claude Code CLI

```bash
# From project root
cd C:/Personal_Ai_Employee_FTEs

# Start Claude Code
claude

# In Claude Code, use the skills:
/process-needs-action
/update-dashboard
```

### Option B: Manual Processing

1. Read the action file: `vault/Needs_Action/FILE_*.md`
2. Follow the suggested actions
3. When done, move files:
```bash
# Move completed items to Done
mv vault/Needs_Action/* vault/Done/
mv vault/Plans/* vault/Done/
```

---

## Step 8: View Results

### Check the Dashboard:
- Open `vault/Dashboard.md` in Obsidian or any text editor
- Verify "Completed Today" count increased
- Check "Recent Activity" for new entries

### Check the Logs:
```bash
# View today's log
cat vault/Logs/2026-03-04.json
```

---

## Complete Test Workflow Summary

```
1. Start watcher (Terminal 1)
   └── python watchers/filesystem_watcher.py --vault vault --drop-folder drop_folder --no-dry-run

2. Drop test file (Terminal 2 or File Explorer)
   └── Create file in drop_folder/

3. Verify watcher created action file
   └── Check vault/Needs_Action/

4. Process with Claude Code (Terminal 3)
   └── claude → /process-needs-action

5. Update dashboard
   └── /update-dashboard

6. Move to Done
   └── mv vault/Needs_Action/* vault/Done/

7. View results
   └── Open vault/Dashboard.md
```

---

## Troubleshooting

### Watcher not detecting files?
- Check the drop folder path is correct
- Ensure the watcher is running (no errors in terminal)
- Check `vault/Logs/FileSystemWatcher.log` for errors

### Claude Code can't find vault?
- Make sure you're running from the project root directory
- Or use `--cwd` flag: `claude --cwd C:/Personal_Ai_Employee_FTEs`

### Files not being processed?
- Verify the watcher created an action file in `Needs_Action/`
- Check the log file for any errors
- Ensure you have proper file permissions

---

## Next Steps

Once Bronze Tier is working, you can:
1. **Add more file types** to test categorization
2. **Create multiple test files** to test batch processing
3. **Customize Company_Handbook.md** with your own rules
4. **Move to Silver Tier** - Add Gmail/WhatsApp watchers

---

## Quick Reference Commands

```bash
# Run watcher (actual processing)
python watchers/filesystem_watcher.py --vault vault --drop-folder drop_folder --no-dry-run

# Run watcher (dry run - for testing)
python watchers/filesystem_watcher.py --vault vault --drop-folder drop_folder

# View logs
cat vault/Logs/$(date +%Y-%m-%d).json

# Check Needs_Action folder
ls vault/Needs_Action/

# Check Done folder
ls vault/Done/

# View Dashboard
cat vault/Dashboard.md
```
