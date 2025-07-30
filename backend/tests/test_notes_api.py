# -*- coding: utf-8 -*-
import importlib
from datetime import datetime, timezone
from unittest import TestCase
from unittest.mock import patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

# 👉 Set correct import path for your router
MODULE_PATH = "backend.app.notes.notes"  # adjust if needed


def iso_now():
    return datetime.now(timezone.utc).isoformat()


def sample_note_dict(note_id=1, name="Title", node="Body"):
    return {
        "id": note_id,
        "name": name,
        # Models now use 'node' (not 'note')
        "node": node,
        "createdate": iso_now(),
        # Models now use 'updatedate' (not 'editdate')
        "updatedate": iso_now(),
    }


class TestNotesAPI(TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.api_mod = importlib.import_module(MODULE_PATH)

        # Setup FastAPI app and include router
        cls.app = FastAPI()
        cls.app.include_router(cls.api_mod.router)

        # Override DB dependency
        from backend.app.db import get_session

        def override_get_session():
            class DummySession:
                pass
            yield DummySession()

        cls.app.dependency_overrides[get_session] = override_get_session

        cls.client = TestClient(cls.app)

        # ⚠️ Check your router decorators
        # If you have prefix="/notes" and endpoint "/notes/", full path = "/notes/notes/"
        cls.BASE = "/notes/notes/"  # change to "/notes/" if you fix the double prefix

    #
    # Create
    #
    def test_add_note_success(self):
        payload = {"name": "First", "node": "Hello"}
        returned = sample_note_dict(1, "First", "Hello")

        with patch(f"{self.api_mod.__name__}.create_note", return_value=returned) as mocked:
            r = self.client.post(self.BASE, json=payload)
            self.assertEqual(r.status_code, 200)
            data = r.json()
            self.assertEqual(data["id"], 1)
            self.assertEqual(data["name"], "First")
            self.assertEqual(data["node"], "Hello")
            mocked.assert_called_once()

    #
    # List
    #
    def test_list_notes_success(self):
        returned = [
            sample_note_dict(1, "A", "aaa"),
            sample_note_dict(2, "B", "bbb"),
        ]

        with patch(f"{self.api_mod.__name__}.get_notes", return_value=returned) as mocked:
            r = self.client.get(self.BASE)
            self.assertEqual(r.status_code, 200)
            data = r.json()
            self.assertIsInstance(data, list)
            self.assertEqual(len(data), 2)
            self.assertEqual({d["id"] for d in data}, {1, 2})
            mocked.assert_called_once()

    #
    # Read by ID
    #
    def test_read_note_found(self):
        returned = sample_note_dict(3, "C", "ccc")

        with patch(f"{self.api_mod.__name__}.get_note", return_value=returned) as mocked:
            r = self.client.get(self.BASE + "3")
            self.assertEqual(r.status_code, 200)
            data = r.json()
            self.assertEqual(data["id"], 3)
            self.assertEqual(data["name"], "C")
            self.assertEqual(data["node"], "ccc")
            mocked.assert_called_once_with(None, 3)

    def test_read_note_not_found(self):
        with patch(f"{self.api_mod.__name__}.get_note", return_value=None) as mocked:
            r = self.client.get(self.BASE + "999")
            self.assertEqual(r.status_code, 404)
            self.assertEqual(r.json()["detail"], "Note not found")
            mocked.assert_called_once()

    #
    # Update
    #
    def test_edit_note_success(self):
        payload = {"name": "Updated", "node": "new body"}
        returned = sample_note_dict(5, "Updated", "new body")

        with patch(f"{self.api_mod.__name__}.update_note", return_value=returned) as mocked:
            r = self.client.put(self.BASE + "5", json=payload)
            self.assertEqual(r.status_code, 200)
            data = r.json()
            self.assertEqual(data["id"], 5)
            self.assertEqual(data["name"], "Updated")
            self.assertEqual(data["node"], "new body")
            mocked.assert_called_once()

    def test_edit_note_not_found(self):
        payload = {"name": "Updated", "node": "new body"}

        with patch(f"{self.api_mod.__name__}.update_note", return_value=None) as mocked:
            r = self.client.put(self.BASE + "404", json=payload)
            self.assertEqual(r.status_code, 404)
            self.assertEqual(r.json()["detail"], "Note not found")
            mocked.assert_called_once()

    #
    # Delete
    #
    def test_remove_note_success(self):
        returned = sample_note_dict(6, "Z", "zzz")

        with patch(f"{self.api_mod.__name__}.delete_note", return_value=returned) as mocked:
            r = self.client.delete(self.BASE + "6")
            self.assertEqual(r.status_code, 200)
            data = r.json()
            self.assertEqual(data["id"], 6)
            mocked.assert_called_once()

    def test_remove_note_not_found(self):
        with patch(f"{self.api_mod.__name__}.delete_note", return_value=None) as mocked:
            r = self.client.delete(self.BASE + "777")
            self.assertEqual(r.status_code, 404)
            self.assertEqual(r.json()["detail"], "Note not found")
            mocked.assert_called_once()
