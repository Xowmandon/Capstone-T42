# Backend Directory Structure

**Last Update:** Dec 10, 2024

This document outlines the structure and usage of the `Backend` directory, providing clarity for developers.

## Overview

The `Backend` directory contains the main backend application code for the project, including configuration files, scripts, data, logs, and tests.

---

## Directory Structure

### Main Files

- **`app.py`**: The main entry point for the Flask application.
- **`README.md`**: Documentation for the backend configuration.

---

### Subdirectories

#### `config/`
Contains configuration files:
- **`models.json`**: JSON Representing database models - Gen by meta_info and meta_display in `scripts/`
- **`requirements.txt`**: Lists the dependencies for the project.
- **`routes.json`**: JSON Repr. of API Routes - Gen by meta_info and meta_display in `scripts/`

#### `data/`
Stores data files:
- **`fake_users.csv`**: Sample user data in CSV format.

#### `docs/`
Directory for additional documentation.

#### `logs/`
Directory for log files.

#### `scripts/`
Contains utility scripts for the project:
- **`__init__.py`**: Marks the directory as a Python package.
- **`DB_Utils.py`**: Provides database utility functions - Deletion and Creation
- **`gen_fake.py`**: Generates fake data, used to populate and simulate DB
- **`meta_display.py`**: Script for displaying route and model metadata
- **`meta_info.py`**: Script for Generating current routes and models in JSON
- **`sql/`**: Directory for SQL scripts.

#### `src/`
Contains the main source code for the backend:
- **`__init__.py`**: Marks the directory as a Python package.
- **`extensions.py`**: Extensions for the application, db,ma, and socketIO configs
- **`models/`**: Contains database model definitions.
- **`routes/`**: Handles API routes.
- **`sockets/`**: Handles Socket Routes and Events
- **`utils.py`**: Includes utility functions and classes.
- **`validators/`**: Contains validation functions.

#### `tests/`
Holds unit tests for the backend:
- **`__init__.py`**: Marks the directory as a Python package.
- **`test_app.py`**: Tests for the Flask application.
- **`test_DB.py`**: Tests for database functionality.
- **`test_message_routes.py`**: Simple One-shot tests for Message Routes
- **`test_user_routes.py`**: Simple One-shot tests for User Routes

---

## Python Module Usage

When running Python scripts or main application files, use absolute paths to ensure correct execution. For example:

- To run `gen_fake.py`:
  ```bash
  python3 -m Backend.scripts.gen_fake

---

## Setting Up the Environment

1. **Virtual Environment**
   - Ensure the working directory is `Backend`.
   - Create a virtual environment:
     ```bash
     python3 -m venv ./.venv
     ```
   - Activate the virtual environment:
     - On macOS/Linux:
       ```bash
       source ./.venv/bin/activate
       ```

2. **Install Dependencies**
   
   - Install required libraries:
     ```bash
     pip install -r ./config/requirements.txt
     ```

3. **Update `requirements.txt`**
   
   - Freeze dependencies and update the `requirements.txt` file:
     ```bash
     pip freeze > ./config/requirements.txt
     ```

---