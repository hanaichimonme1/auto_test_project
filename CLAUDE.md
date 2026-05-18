# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Is

A Python test automation framework covering both API tests (via `requests`) and UI tests (via Selenium/Chrome). It targets the [reqres.in](https://reqres.in) demo API and a local `demo_login.html` page.

## Running Tests

```bash
# Run all tests
pytest

# Run only API tests
pytest -m api

# Run only UI tests
pytest -m ui

# Run only login-related tests
pytest -m login

# Run a single test file
pytest testcases/api/test_login.py

# Run a single test by name
pytest testcases/ui/test_login_ui.py -k "登录成功"

# Run UI tests in headless mode (pass headless=True to create_driver manually or modify browser_util.py)
```

Logs are written to `test.log` in the project root. Failure screenshots are saved to `reports/screenshots/`.

## Architecture

### `common/` — Shared utilities

- **`config.py`** — Loads `config/config.yaml` (base URL, API key, timeout) into a module-level `config` dict.
- **`request_util.py`** — `RequestUtil.send_method(url, method, headers, data)` wraps `requests`, auto-injects the `x-api-key` header from config, and logs all request/response details.
- **`browser_util.py`** — Creates a Chrome WebDriver (`create_driver`), provides `wait_find` / `wait_click` helpers with explicit waits, and `save_screenshot`.
- **`assert_util.py`** — `assert_response(res, expected_status)` checks status code and validates that 200 responses have a `token` field and error responses have an `error` field.
- **`data_util.py`** — `load_json_data(path)` reads test data JSON files; `validate_login_cases(cases)` enforces required fields.
- **`logger.py`** — Returns a singleton `logging.Logger` named `"api_test"` that writes to both console and `test.log`.

### `testcases/`

- **`api/test_login.py`** — Parametrized API login tests driven by `data/api_test_data.json`.
- **`api/test_user.py`** — Uses the session-scoped `get_token` fixture (defined in `conftest.py`) to test an authenticated GET endpoint.
- **`ui/test_login_ui.py`** — Parametrized UI login tests driven by `data/login_ui_data.json`, running against the local `demo_login.html`.

### `conftest.py` (root)

- `driver` fixture: creates and tears down Chrome for each UI test.
- `get_token` fixture (session scope): POSTs to the login API once and returns the bearer token.
- `pytest_runtest_makereport` hook: captures a timestamped screenshot on any UI test failure.

### Test data

- `data/api_test_data.json` — Each entry needs `name`, `data` (request body), and `expected` (status code).
- `data/login_ui_data.json` — Each entry needs `case_name`, `username`, `password`, `expected_message`.

## Configuration

`config/config.yaml` holds `base_url`, `api_key`, and `timeout`. `config.py` opens this file relative to the **current working directory**, so tests must be run from the project root.

## Markers

Defined in `pytest.ini`:
- `ui` — Selenium UI tests
- `api` — HTTP API tests
- `login` — Login-module tests (used in both layers)
