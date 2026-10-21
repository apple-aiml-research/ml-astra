# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
import json
import os
from pathlib import Path
from typing import Any


class ProtagonistOperaPaths:
    def __init__(self, base_paths: list[str], plot_ids: str = "ALL"):
        self.paths = base_paths
        self.plot_ids = plot_ids
        self.calendar_paths = [
            Path(path) / "calendar_events.json"
            for path in self.paths
            if "calendar_events.json" in os.listdir(path)
        ]
        self.contact_paths = [
            Path(path) / "contacts.json"
            for path in self.paths
            if "contacts.json" in os.listdir(path)
        ]
        self.phonecall_paths = [
            Path(path) / "call_logs.json"
            for path in self.paths
            if "call_logs.json" in os.listdir(path)
        ]
        self.messaging_paths = [
            Path(path) / "message_conversations.json"
            for path in self.paths
            if "message_conversations.json" in os.listdir(path)
        ]
        self.email_paths = [
            Path(path) / "emails.json"
            for path in self.paths
            if "emails.json" in os.listdir(path)
        ]
        self.whatsapp_paths = [
            Path(path) / "whatsapp_messages.json"
            for path in self.paths
            if "whatsapp_messages.json" in os.listdir(path)
        ]

    def display_paths(self) -> None:
        print(f"Paths: {self.paths}")
        print(f"Plot IDs: {self.plot_ids}")
        print(f"Calendar Paths: {self.calendar_paths}")
        print(f"Contact Paths: {self.contact_paths}")
        print(f"Phone Call Paths: {self.phonecall_paths}")
        print(f"Messaging Paths: {self.messaging_paths}")
        print(f"Email Paths: {self.email_paths}")
        print(f"WhatsApp Paths: {self.whatsapp_paths}")

    def to_dict(self) -> dict[str, Any]:
        return {
            "paths": self.paths,
            "plot_ids": self.plot_ids,
            "calendar_paths": self.calendar_paths,
            "contact_paths": self.contact_paths,
            "messaging_paths": self.messaging_paths,
            "email_paths": self.email_paths,
            "whatsapp_paths": self.whatsapp_paths,
            "phonecall_paths": self.phonecall_paths,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ProtagonistOperaPaths":
        base_paths: list[str] = data["paths"]
        plot_ids: str = data["plot_ids"]
        return cls(base_paths=base_paths, plot_ids=plot_ids)

    def save_to_json(self, file_path: Path) -> None:
        with file_path.open("w") as f:
            json.dump(self.to_dict(), f)

    @classmethod
    def from_json(cls, file_path: str) -> "ProtagonistOperaPaths":
        with open(file_path, "r") as f:
            data = json.load(f)
        return cls.from_dict(data)
