"""
File System Watcher - Monitors a drop folder for new files

This watcher monitors a designated "drop folder" for new files.
When files are dropped into the folder, it creates action items
in the Needs_Action folder for Claude Code to process.
"""

import time
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import hashlib

from base_watcher import BaseWatcher, create_action_file_template


class FileSystemWatcher(BaseWatcher):
    """
    Watches a designated drop folder for new files.

    When files are dropped into the monitored folder, this watcher:
    1. Copies the file to the vault
    2. Creates a metadata file in Needs_Action
    3. Logs the action

    This is useful for:
    - Dropping invoices for processing
    - Adding documents to review
    - Submitting tasks via file drops
    """

    def __init__(
        self,
        vault_path: str,
        drop_folder_path: str,
        check_interval: int = 30,
        dry_run: bool = True
    ):
        """
        Initialize the file system watcher.

        Args:
            vault_path: Path to the Obsidian vault
            drop_folder_path: Path to the folder to monitor
            check_interval: Seconds between checks (default: 30)
            dry_run: If True, log actions but don't move files (default: True)
        """
        super().__init__(vault_path, check_interval, dry_run)
        self.drop_folder = Path(drop_folder_path)

        # Create drop folder if it doesn't exist
        self.drop_folder.mkdir(parents=True, exist_ok=True)

        # Attachments folder in vault
        self.attachments_folder = self.vault_path / 'Attachments'
        self.attachments_folder.mkdir(parents=True, exist_ok=True)

        self.logger.info(f"Monitoring drop folder: {self.drop_folder}")
        self.logger.info(f"Attachments will be stored in: {self.attachments_folder}")

    def check_for_updates(self) -> List[Dict[str, Any]]:
        """
        Check for new files in the drop folder.

        Returns:
            List of dictionaries containing file information
        """
        items = []

        # Get all files in drop folder (not directories)
        for file_path in self.drop_folder.iterdir():
            if file_path.is_file():
                # Skip hidden files and temporary files
                if file_path.name.startswith('.') or file_path.name.startswith('~'):
                    continue

                items.append({
                    'id': self._get_file_hash(file_path),
                    'path': file_path,
                    'name': file_path.name,
                    'size': file_path.stat().st_size,
                    'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                })

        return items

    def _get_file_hash(self, file_path: Path) -> str:
        """
        Generate a unique hash for a file based on path and modification time.

        Args:
            file_path: Path to the file

        Returns:
            Unique hash string
        """
        stat = file_path.stat()
        content = f"{file_path}_{stat.st_size}_{stat.st_mtime}"
        return hashlib.md5(content.encode()).hexdigest()[:16]

    def _get_file_category(self, filename: str) -> str:
        """
        Determine the category of a file based on its extension.

        Args:
            filename: Name of the file

        Returns:
            Category string
        """
        ext = Path(filename).suffix.lower()

        categories = {
            # Documents
            '.pdf': 'document',
            '.doc': 'document',
            '.docx': 'document',
            '.txt': 'document',
            '.rtf': 'document',
            '.odt': 'document',

            # Spreadsheets
            '.xls': 'spreadsheet',
            '.xlsx': 'spreadsheet',
            '.csv': 'spreadsheet',
            '.ods': 'spreadsheet',

            # Images
            '.jpg': 'image',
            '.jpeg': 'image',
            '.png': 'image',
            '.gif': 'image',
            '.bmp': 'image',
            '.svg': 'image',
            '.webp': 'image',

            # Archives
            '.zip': 'archive',
            '.rar': 'archive',
            '.7z': 'archive',
            '.tar': 'archive',
            '.gz': 'archive',

            # Code
            '.py': 'code',
            '.js': 'code',
            '.html': 'code',
            '.css': 'code',
            '.json': 'code',
            '.xml': 'code',
        }

        return categories.get(ext, 'unknown')

    def _suggest_priority(self, filename: str) -> str:
        """
        Suggest a priority level based on filename keywords.

        Args:
            filename: Name of the file

        Returns:
            Priority level (high, medium, low)
        """
        filename_lower = filename.lower()

        high_priority_keywords = ['urgent', 'asap', 'important', 'invoice', 'payment']
        low_priority_keywords = ['info', 'reference', 'archive', 'backup']

        if any(kw in filename_lower for kw in high_priority_keywords):
            return 'high'
        elif any(kw in filename_lower for kw in low_priority_keywords):
            return 'low'
        else:
            return 'medium'

    def create_action_file(self, item: Dict[str, Any]) -> Path:
        """
        Create an action file for the dropped file.

        Args:
            item: File information dictionary

        Returns:
            Path to the created action file
        """
        file_path = item['path']
        filename = item['name']
        file_size = item['size']
        category = self._get_file_category(filename)
        priority = self._suggest_priority(filename)

        # Copy file to attachments folder
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_filename = f"{timestamp}_{filename}"
        dest_path = self.attachments_folder / safe_filename

        if not self.dry_run:
            shutil.copy2(file_path, dest_path)
            self.logger.info(f"Copied file to: {dest_path}")
        else:
            self.logger.info(f"[DRY RUN] Would copy to: {dest_path}")

        # Format file size
        size_mb = file_size / (1024 * 1024)
        if size_mb < 1:
            size_str = f"{file_size / 1024:.2f} KB"
        else:
            size_str = f"{size_mb:.2f} MB"

        # Build content for action file
        content = f"""## File Information

- **Original Name:** {filename}
- **Category:** {category}
- **Size:** {size_str}
- **Modified:** {item['modified']}

## Suggested Actions

- [ ] Review the file content
- [ ] Categorize and process appropriately
- [ ] Move to Done when complete

## File Location

The file has been saved to: `Attachments/{safe_filename}`

---

**Priority:** {priority}
**Auto-detected category:** {category}
"""

        # Create metadata
        metadata = {
            "original_name": filename,
            "file_size": file_size,
            "category": category,
            "priority": priority,
            "attachment_path": f"Attachments/{safe_filename}",
            "modified": item['modified']
        }

        # Create action file with timestamp prefix
        action_filename = f"FILE_{timestamp}_{filename[:50]}"
        filepath = create_action_file_template(
            self.needs_action,
            action_filename,
            item_type="file_drop",
            title=f"File Drop: {filename}",
            content=content,
            metadata=metadata
        )

        # Optionally remove original file from drop folder
        if not self.dry_run:
            try:
                file_path.unlink()
                self.logger.info(f"Removed original file from drop folder")
            except Exception as e:
                self.logger.warning(f"Could not remove original file: {e}")

        return filepath


def main():
    """
    Main entry point for running the file system watcher.
    """
    import argparse

    parser = argparse.ArgumentParser(
        description='Monitor a drop folder for new files'
    )
    parser.add_argument(
        '--vault',
        type=str,
        default='vault',
        help='Path to the Obsidian vault (default: vault)'
    )
    parser.add_argument(
        '--drop-folder',
        type=str,
        default='drop_folder',
        help='Path to the drop folder to monitor (default: drop_folder)'
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=30,
        help='Check interval in seconds (default: 30)'
    )
    parser.add_argument(
        '--no-dry-run',
        action='store_true',
        help='Disable dry run mode and actually process files'
    )

    args = parser.parse_args()

    # Get absolute paths
    vault_path = Path(args.vault).resolve()
    drop_folder_path = Path(args.drop_folder).resolve()

    print(f"File System Watcher")
    print(f"=" * 50)
    print(f"Vault: {vault_path}")
    print(f"Drop Folder: {drop_folder_path}")
    print(f"Check Interval: {args.interval}s")
    print(f"Dry Run: {not args.no_dry_run}")
    print(f"=" * 50)

    # Create and run watcher
    watcher = FileSystemWatcher(
        vault_path=str(vault_path),
        drop_folder_path=str(drop_folder_path),
        check_interval=args.interval,
        dry_run=not args.no_dry_run
    )

    try:
        watcher.run()
    except KeyboardInterrupt:
        print("\nWatcher stopped by user")


if __name__ == '__main__':
    main()
