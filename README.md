# config-drift-sentinel

A dependency-free CLI that compares environment configurations while keeping declared sensitive values out of reports.

## Quick start

```bash
python drift.py staging.json production.json --sensitive DATABASE_URL --allow LOG_LEVEL
```

The report detects missing and mismatched keys, calculates an environment health score, and emits only SHA-256 fingerprints for sensitive differences. It exits nonzero when unexpected drift is found.

## Test

```bash
python -m unittest discover -v
```

## License

MIT.
