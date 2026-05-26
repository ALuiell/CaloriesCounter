# Deploy On GCP VM

## Recommended Shape

For this bot, the simplest production setup is:

- `Google Compute Engine` VM
- `Ubuntu 24.04 LTS`
- one long-running `systemd` service
- `SQLite` stored on the VM disk
- code pulled from GitHub

This project uses `Telegram polling`, so it does not need a public HTTP port for the bot itself.

## Why This Fits

- `SQLite` works naturally on a single VM
- `aiogram` polling wants a stable always-on process
- deploys are simple: pull code, install deps, restart service
- backups are easy because the database is just one file

## Suggested VM

Small first deployment:

- machine type: `e2-micro`
- OS: `Ubuntu 24.04 LTS`
- disk: at least `10-20 GB`
- region: choose the one closest to you, unless you are specifically optimizing for a free-tier US region

## Server Layout

Suggested directories:

- app checkout: `/opt/caloriescounter/app`
- shared env and data: `/opt/caloriescounter/shared`
- database file: `/opt/caloriescounter/shared/data/calories_counter.sqlite3`

This keeps data outside the code checkout, so redeploys do not touch the database.

## First-Time Setup

### 1. Install base packages

```bash
sudo apt update
sudo apt install -y git python3 python3-venv
```

### 2. Create a service user

```bash
sudo useradd -m -s /bin/bash caloriesbot || true
```

### 3. Create directories

```bash
sudo mkdir -p /opt/caloriescounter
sudo mkdir -p /opt/caloriescounter/shared/data
sudo chown -R caloriesbot:caloriesbot /opt/caloriescounter
```

### 4. Clone the repository

```bash
sudo -u caloriesbot git clone https://github.com/ALuiell/CaloriesCounter.git /opt/caloriescounter/app
```

### 5. Create the production `.env`

Create `/opt/caloriescounter/shared/.env`:

```env
BOT_TOKEN=your_real_telegram_token
APP_TIMEZONE=Europe/Kiev
DATABASE_PATH=/opt/caloriescounter/shared/data/calories_counter.sqlite3
```

### 6. Install dependencies

```bash
cd /opt/caloriescounter/app
sudo -u caloriesbot python3 -m venv .venv
sudo -u caloriesbot .venv/bin/pip install --upgrade pip
sudo -u caloriesbot .venv/bin/pip install -r requirements.txt
```

## systemd Service

Use [caloriescounter.service.example](F:\Python\CaloriesCounter\deploy\caloriescounter.service.example) as the template.

On Linux, the `ExecStart` must point to:

```ini
ExecStart=/opt/caloriescounter/app/.venv/bin/python -m app.main
```

Create `/etc/systemd/system/caloriescounter.service`, adjust the path if needed, then:

```bash
sudo systemctl daemon-reload
sudo systemctl enable caloriescounter
sudo systemctl start caloriescounter
sudo systemctl status caloriescounter --no-pager
```

## Deploying Updates

Use [deploy_linux.sh](F:\Python\CaloriesCounter\scripts\deploy_linux.sh).

Typical flow:

```bash
cd /opt/caloriescounter/app
chmod +x scripts/deploy_linux.sh
APP_DIR=/opt/caloriescounter/app \
SHARED_DIR=/opt/caloriescounter/shared \
SERVICE_NAME=caloriescounter \
bash scripts/deploy_linux.sh
```

What it does:

- fetches latest code
- checks out the target branch
- pulls updates
- refreshes the virtualenv packages
- restarts the `systemd` service

## Useful Commands

Show live logs:

```bash
sudo journalctl -u caloriescounter -f
```

Restart manually:

```bash
sudo systemctl restart caloriescounter
```

Check bot status:

```bash
sudo systemctl status caloriescounter --no-pager
```

## Backups

At minimum, back up:

- `/opt/caloriescounter/shared/.env`
- `/opt/caloriescounter/shared/data/calories_counter.sqlite3`

Even a simple daily copy is enough for the first version.
