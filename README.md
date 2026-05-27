# discord-time-bot

A tiny Discord bot that exposes a single `/time` slash command. When invoked, it
prints the current local time across a configured list of regions — handy for
coordinating with friends, teammates, or family across multiple time zones.

## What it does

Running `/time` in a Discord channel produces output like:

```
Here are the current local times in the following regions:
US-Hawaii    2026-05-27  09:14 (09:14 AM)  HST
US-West      2026-05-27  12:14 (12:14 PM)  PDT
US-Mountain  2026-05-27  13:14 (01:14 PM)  MDT
US-Central   2026-05-27  14:14 (02:14 PM)  CDT
US-East      2026-05-27  15:14 (03:14 PM)  EDT
EU-France    2026-05-27  21:14 (09:14 PM)  CEST
EU-Turkey    2026-05-27  22:14 (10:14 PM)  +03
Japan        2026-05-28  04:14 (04:14 AM)  JST
```

Each row shows the date, 24-hour time, 12-hour time with AM/PM, and the
timezone abbreviation.

## Purpose

I built this for a single Discord server where the members are spread across
several time zones. Instead of mentally converting "is 3pm my time okay?" every
time someone schedules a hangout, anyone can run `/time` and get the answer at
a glance.

It is intentionally minimal — one command, one server, no database, no state.

## How it works

- Built on [discord.py](https://github.com/Rapptz/discord.py) with the
  `app_commands` API for slash commands.
- Slash commands are registered to a single guild (`GUILD_ID` in `.env`) rather
  than globally, so they appear instantly and don't propagate to other servers.
- Timezone conversion uses Python's stdlib `zoneinfo` (no extra dependency).
- The list of regions lives at the top of [bot.py](bot.py) as a list of
  `(label, IANA timezone)` tuples — edit that list to add, remove, or rename
  regions, then restart the bot.

## Setup

Requires Python 3.10+ (for `zoneinfo`).

```
git clone https://github.com/atandy/discord_timebot.git
cd discord_timebot
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # then edit .env with your bot token and server ID
python bot.py
```

You'll need to register a bot application at
[discord.com/developers/applications](https://discord.com/developers/applications),
copy its token into `.env` as `DISCORD_TOKEN`, and invite it to your server via
OAuth2 with the `bot` and `applications.commands` scopes.

## Deployment (Hetzner / any Linux VPS)

A `discord-time-bot.service` systemd unit is included for production use:

```
sudo cp discord-time-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now discord-time-bot
sudo journalctl -u discord-time-bot -f
```

The unit expects the code at `/opt/discord-time-bot`, the venv at
`/opt/discord-time-bot/.venv`, and the `.env` at `/opt/discord-time-bot/.env`,
all owned by a `discordbot` system user. `Restart=always` ensures the bot
recovers from crashes and survives reboots.

## License

MIT — do whatever you want with it.
