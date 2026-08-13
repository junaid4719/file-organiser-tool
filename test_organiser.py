"""
Unit tests for the File Organiser Tool.
Run with: pytest test_organiser.py
"""

import os
import json
import pytest
from organiser import FileOrganiser


@pytest.fixture
def temp_folder(tmp_path):
    """
    Creates a temporary folder with some dummy files in it.
    pytest automatically deletes tmp_path after the test finishes.
    """
    folder = tmp_path / "test_folder"
    folder.mkdir()

    (folder / "report.pdf").write_text("dummy pdf content")
    (folder / "photo.jpg").write_text("dummy image content")
    (folder / "notes.txt").write_text("dummy text content")
    (folder / "unknown.xyz").write_text("dummy unknown content")

    return str(folder)


def test_default_config_created(temp_folder):
    """If no config.json exists, one should be created automatically."""
    config_path = os.path.join(temp_folder, "config.json")
    FileOrganiser(target_folder=temp_folder, config_path=config_path)

    assert os.path.exists(config_path)
    with open(config_path) as f:
        rules = json.load(f)
    assert ".pdf" in rules


def test_files_are_sorted_into_correct_folders(temp_folder):
    config_path = os.path.join(temp_folder, "config.json")
    organiser = FileOrganiser(target_folder=temp_folder, config_path=config_path)
    organiser.organise()

    assert os.path.exists(os.path.join(temp_folder, "Documents", "report.pdf"))
    assert os.path.exists(os.path.join(temp_folder, "Images", "photo.jpg"))
    assert os.path.exists(os.path.join(temp_folder, "Documents", "notes.txt"))


def test_unknown_extension_goes_to_other_folder(temp_folder):
    config_path = os.path.join(temp_folder, "config.json")
    organiser = FileOrganiser(target_folder=temp_folder, config_path=config_path)
    organiser.organise()

    assert os.path.exists(os.path.join(temp_folder, "Other", "unknown.xyz"))


def test_missing_target_folder_does_not_crash(tmp_path):
    fake_folder = str(tmp_path / "does_not_exist")
    config_path = str(tmp_path / "config.json")
    organiser = FileOrganiser(target_folder=fake_folder, config_path=config_path)

    # Should log an error and return quietly, not raise an exception
    organiser.organise()


def test_existing_file_at_destination_is_skipped(temp_folder):
    config_path = os.path.join(temp_folder, "config.json")

    # Pre-create the destination so there's already a file.pdf there
    docs_folder = os.path.join(temp_folder, "Documents")
    os.makedirs(docs_folder)
    with open(os.path.join(docs_folder, "report.pdf"), "w") as f:
        f.write("already here")

    organiser = FileOrganiser(target_folder=temp_folder, config_path=config_path)
    organiser.organise()

    # Original file should NOT have been moved/overwritten
    original_still_exists = os.path.exists(os.path.join(temp_folder, "report.pdf"))
    assert original_still_exists
