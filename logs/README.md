# Logs Directory

This directory contains application log files.

## Log Files

- `app.log` - Main application logs (rotated automatically)
- `app.log.1`, `app.log.2`, etc. - Rotated log files (up to 5 backups)

## Log Format

Logs are written in JSON format for structured logging, containing:
- Timestamp (ISO format)
- Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Logger name
- Message
- Additional context fields

## Configuration

Log configuration is managed in `src/email_templates_gen/utils/logging_config.py`:
- Log level can be set via `LOG_LEVEL` environment variable
- Debug mode can be enabled via `DEBUG` environment variable
- Log rotation: 10MB max file size, 5 backup files

## Viewing Logs

To view logs in real-time:
```bash
tail -f logs/app.log
```

To view logs with JSON formatting:
```bash
cat logs/app.log | jq
```
