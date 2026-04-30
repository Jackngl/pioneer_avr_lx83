# AGENTS.md

## Cursor Cloud specific instructions

This is a **Home Assistant custom integration** (not a standalone app). There is no server to start or UI to launch — the code runs inside Home Assistant as a plugin.

### Development commands

| Task | Command |
|------|---------|
| Lint (critical errors) | `flake8 custom_components/pioneer_avr_lx83 --count --select=E9,F63,F7,F82 --show-source --statistics` |
| Format check | `black --check custom_components/pioneer_avr_lx83` |
| Import sort check | `isort --check-only custom_components/pioneer_avr_lx83` |
| Run tests | `pytest tests/ -v` |

### Notes

- Linting with `black` and `isort` is **non-blocking** in CI (`continue-on-error: true`). Only `flake8` critical errors (E9, F63, F7, F82) are strictly enforced.
- The `test_pioneer_avr_name` test is a known pre-existing failure (HA's `Entity` base class returns `None` for `.name` instead of `_name`). It does not indicate a regression.
- The PyYAML system package conflicts with pip installs. Use `pip install --ignore-installed PyYAML` when installing `homeassistant` in a fresh environment.
- There is no `setup.py` or installable package; the integration is loaded by Home Assistant from `custom_components/pioneer_avr_lx83/`.
