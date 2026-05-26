# GCP Deployment Recommendations

## Purpose

This document lists short practical recommendations for deploying the bot on a Google Cloud `e2-micro` VM.

## Scope

These notes are intended for a small Python bot running on a single Compute Engine instance, especially within the free tier constraints.

## Recommendations

- Add a `1-2 GB` swap file.
  This helps protect the bot from sudden `Out of Memory` crashes on a VM with only `1 GB RAM`.

- Run the bot as a `systemd` service.
  This ensures automatic startup after reboot and automatic restart after crashes.

- Use absolute paths in the code.
  Do not rely on the current working directory when opening the SQLite database, logs, or config files.

- Keep server access locked down.
  Use SSH keys only and limit firewall rules to the minimum required ports.
  For a polling-based Telegram bot, no public inbound application port is required.

- Keep timezone handling explicit.
  Prefer storing the server in `UTC` and handling business time in the application code.
  If the bot depends on local midnight or morning reports, define the target timezone explicitly.

- Avoid uncontrolled log growth.
  Use `systemd` logs or rotate file-based logs so they do not consume the whole disk over time.

- Back up the SQLite database regularly.
  A simple daily copy to another directory or to cloud storage is enough for an early-stage deployment.

- Keep secrets outside the codebase.
  Store the Telegram bot token and other sensitive settings in environment variables or a protected config file.

## Practical Minimum

For the first stable deployment, the most important items are:

- `systemd`
- swap
- absolute paths
- SSH and firewall hardening
- database backup

## Related Files

- [Architecture](F:\Python\CaloriesCounter\docs\architecture.md)
- [Implementation Plan](F:\Python\CaloriesCounter\docs\implementation-plan.md)
- [Handover](F:\Python\CaloriesCounter\docs\handover.md)
