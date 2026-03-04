"""
Base Watcher - Template for all AI Employee watchers

This module provides the abstract base class that all watchers should extend.
It defines the common interface and behavior for monitoring external sources
and creating actionable files in the Obsidian vault.
"""

import time
import logging
from pathlib import Path
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Any, Optional
import json


class BaseWatcher(ABC):
    """
    Abstract base class for all watcher scripts.

    All watchers should extend this class and implement:
    - check_for_updates(): Returns a list of new items to process
    - create_action_file(item): Creates an .md file in the Needs_Action folder
    """

    def __init__(
        self,
        vault_path: str,
        check_interval: int = 60,
        dry_run: bool = True
    ):
        """
        Initialize the watcher.

        Args:
            vault_path: Path to the Obsidian vault
            check_interval: Seconds between checks (default: 60)
            dry_run: If True, log actions but don't create files (default: True)
        """
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.logs = self.vault_path / 'Logs'
        self.check_interval = check_interval
        self.dry_run = dry_run

        # Create directories if they don't exist
        self.needs_action.mkdir(parents=True, exist_ok=True)
        self.logs.mkdir(parents=True, exist_ok=True)

        # Set up logging
        self._setup_logging()

        # Track processed items to avoid duplicates
        self.processed_ids = set()

        self.logger.info(f"Initializing {self.__class__.__name__}")
        self.logger.info(f"Vault path: {self.vault_path}")
        self.logger.info(f"Check interval: {self.check_interval}s")
        self.logger.info(f"Dry run: {self.dry_run}")

    def _setup_logging(self):
        """Configure logging to both file and console."""
        log_dir = self.vault_path / 'Logs'
        log_dir.mkdir(parents=True, exist_ok=True)

        # Create logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)

        # File handler
        log_file = log_dir / f"{self.__class__.__name__}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    @abstractmethod
    def check_for_updates(self) -> List[Any]:
        """
        Check for new items to process.

        Returns:
            List of new items. Each item should be a dict or object
            containing enough information to create an action file.
        """
        pass

    @abstractmethod
    def create_action_file(self, item: Any) -> Optional[Path]:
        """
        Create an action file in the Needs_Action folder.

        Args:
            item: An item returned by check_for_updates()

        Returns:
            Path to the created file, or None if file was not created
        """
        pass

    def get_item_id(self, item: Any) -> str:
        """
        Get a unique identifier for an item.
        Override this method for custom ID generation.

        Args:
            item: An item to identify

        Returns:
            Unique string identifier
        """
        if isinstance(item, dict):
            return item.get('id', str(hash(str(item))))
        return str(id(item))

    def should_process_item(self, item: Any) -> bool:
        """
        Determine if an item should be processed.
        Checks if the item has already been processed.

        Args:
            item: An item to check

        Returns:
            True if item should be processed, False otherwise
        """
        item_id = self.get_item_id(item)
        return item_id not in self.processed_ids

    def mark_as_processed(self, item: Any):
        """
        Mark an item as processed to avoid duplicates.

        Args:
            item: An item to mark
        """
        item_id = self.get_item_id(item)
        self.processed_ids.add(item_id)

    def log_action(self, action_type: str, details: dict):
        """
        Log an action to the daily log file.

        Args:
            action_type: Type of action (e.g., 'file_created', 'error')
            details: Dictionary containing action details
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "watcher": self.__class__.__name__,
            "action_type": action_type,
            **details
        }

        # Write to daily log file
        log_file = self.logs / f"{datetime.now().strftime('%Y-%m-%d')}.json"
        logs = []

        # Read existing logs if file exists
        if log_file.exists():
            try:
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            except json.JSONDecodeError:
                logs = []

        # Append new log entry
        logs.append(log_entry)

        # Write back to file
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)

    def run_once(self) -> int:
        """
        Run a single check cycle.

        Returns:
            Number of items processed
        """
        try:
            items = self.check_for_updates()
            processed_count = 0

            for item in items:
                if not self.should_process_item(item):
                    continue

                if self.dry_run:
                    self.logger.info(f"[DRY RUN] Would create action file for: {item}")
                    self.log_action("dry_run", {"item": str(item)})
                else:
                    filepath = self.create_action_file(item)
                    if filepath:
                        processed_count += 1
                        self.logger.info(f"Created action file: {filepath}")
                        self.log_action("file_created", {
                            "filepath": str(filepath),
                            "item": str(item)
                        })

                self.mark_as_processed(item)

            return processed_count

        except Exception as e:
            self.logger.error(f"Error in run_once: {e}", exc_info=True)
            self.log_action("error", {"error": str(e)})
            return 0

    def run(self):
        """
        Main run loop - continuously checks for updates.
        Use Ctrl+C to stop.
        """
        self.logger.info(f"Starting {self.__class__.__name__} main loop")
        self.log_action("watcher_started", {
            "check_interval": self.check_interval,
            "dry_run": self.dry_run
        })

        try:
            while True:
                processed = self.run_once()
                if processed > 0:
                    self.logger.info(f"Processed {processed} item(s)")

                time.sleep(self.check_interval)

        except KeyboardInterrupt:
            self.logger.info(f"Stopping {self.__class__.__name__} (user interrupt)")
            self.log_action("watcher_stopped", {"reason": "user_interrupt"})

        except Exception as e:
            self.logger.error(f"Fatal error: {e}", exc_info=True)
            self.log_action("watcher_stopped", {
                "reason": "error",
                "error": str(e)
            })
            raise


def create_action_file_template(
    needs_action_path: Path,
    filename: str,
    item_type: str,
    title: str,
    content: str,
    metadata: dict = None
) -> Path:
    """
    Helper function to create a standardized action file.

    Args:
        needs_action_path: Path to the Needs_Action folder
        filename: Name for the file (will have .md appended if needed)
        item_type: Type of item (email, file_drop, etc.)
        title: Title for the action item
        content: Main content of the file
        metadata: Optional additional metadata

    Returns:
        Path to the created file
    """
    if metadata is None:
        metadata = {}

    frontmatter = {
        "type": item_type,
        "title": title,
        "created": datetime.now().isoformat(),
        "status": "pending",
        **metadata
    }

    # Build YAML frontmatter
    yaml_lines = ["---"]
    for key, value in frontmatter.items():
        if isinstance(value, str):
            yaml_lines.append(f"{key}: {value}")
        elif isinstance(value, list):
            yaml_lines.append(f"{key}:")
            for v in value:
                yaml_lines.append(f"  - {v}")
        elif isinstance(value, dict):
            yaml_lines.append(f"{key}:")
            for k, v in value.items():
                yaml_lines.append(f"  {k}: {v}")
        else:
            yaml_lines.append(f"{key}: {value}")
    yaml_lines.append("---")

    # Combine frontmatter and content
    file_content = "\n".join(yaml_lines) + "\n\n" + content

    # Ensure filename ends with .md
    if not filename.endswith('.md'):
        filename += '.md'

    filepath = needs_action_path / filename
    filepath.write_text(file_content, encoding='utf-8')

    return filepath
