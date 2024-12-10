# Backend Directory Structure

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
- **`requirements.txt`**: Lists the dependencies for the project.

#### `data/`
Stores data files:
- **`fake_users.csv`**: Sample user data in CSV format.

#### `logs/`
Directory for log files.

#### `src/`
Contains the main source code for the backend:
- **`__init__.py`**: Marks the directory as a Python package.
- **`middleware.py`**: Middleware functions for the application.
- **`models.py`**: Defines database models.
- **`routes.py`**: Handles API routes.
- **`utils.py`**: Includes utility functions and classes.

#### `scripts/`
Contains utility scripts for the project:
- **`__init__.py`**: Marks the directory as a Python package.
- **`DB_Utils.py`**: Provides database utility functions.
- **`gen_fake.py`**: Generates fake data.

#### `tests/`
Holds unit tests for the backend:
- **`__init__.py`**: Marks the directory as a Python package.
- **`test_app.py`**: Tests for the Flask application.
- **`test_DB.py`**: Tests for database functionality.
- **`test_fake.py`**: Tests for fake data generation scripts.

---

## Python Module Usage

When running Python scripts or main application files, use absolute paths to ensure correct execution. For example:

- To run `gen_fake.py`:
  ```bash
  python3 -m scripts.gen_fake
  ```
- The `-m` flag specifies that the file is part of a module (indicated by `__init__.py`).

This practice also applies to running tests located in the `tests` module:
```bash
python3 -m tests.test_app
```

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