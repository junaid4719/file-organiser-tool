# File Organiser Tool

A Python tool that automatically organises files in a target folder into subfolders based on file type (Documents, Images, Archives, Audio, Video, etc.). Sorting rules are defined in an external JSON config file rather than hardcoded, and every action is logged with a timestamp.

## Why this project

Manually sorting downloaded or exported files is repetitive and error-prone. This tool automates that process while demonstrating good software engineering practices: clean separation of logic, configurable behaviour, error handling, logging, and automated testing.

## Features

- **Configurable rules** — file-type-to-folder mappings are stored in `config.json`, so behaviour can be changed without editing code
- **Safe by default** — never overwrites an existing file at the destination; skips it and logs a warning instead
- **Logging** — every file move (and any errors) is recorded with a timestamp in `organiser.log`
- **Error handling** — gracefully handles missing folders, permission errors, and other failures without crashing
- **Unit tested** — covered by a `pytest` suite (see `test_organiser.py`)

## How it works

Scan target folder
↓
Read file extension
↓
Look up destination folder in config.json
↓
Create destination folder if needed
↓
Move file (skip if a duplicate already exists there)
↓
Log the result


## Requirements

- Python 3.10+
- `pytest` (for running tests)

## Installation

```bash
git clone https://github.com/junaid4719/file-organiser-tool.git
cd file-organiser-tool
pip install pytest
```

## Usage

1. Open `organiser.py` and set `TARGET_FOLDER` to the folder you want organised.
2. Run the script:
```bash
   python organiser.py
```
3. On first run, a default `config.json` is created automatically if one doesn't exist. Edit it to customise which extensions go where, e.g.:
```json
   {
       ".pdf": "Documents",
       ".jpg": "Images",
       ".zip": "Archives"
   }
```
4. Check `organiser.log` to see exactly what was moved.

## Running the tests

```bash
pytest test_organiser.py -v
```

## Project structure

file-organiser-tool/
├── organiser.py # Main application logic
├── test_organiser.py # Unit tests
├── config.json # Auto-generated sorting rules (created on first run)
├── organiser.log # Auto-generated log file (created on first run)
└── README.md


## Possible future improvements

- Watch a folder continuously (using `watchdog`) instead of running as a one-off script
- Add a command-line interface for choosing the target folder without editing code
- Package as a standalone executable

## Licence

MIT