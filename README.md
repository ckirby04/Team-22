# Photon Laser Tag - Main Software

Main software for the Photon Laser Tag system. Provides a GUI for player entry and live game action with real-time scoring, communicating with game equipment via UDP.

## Team Members

| Real Name | GitHub Username |
|-----------|----------------|
| Clark Kirby | ckirby04 |

## Prerequisites

- Debian-based Linux (tested on Debian VM)
- Python 3.8+
- PostgreSQL with `photon` database and `student` role (pre-configured on the VM)
- Network access on UDP ports 7500 (transmit) and 7501 (receive)

## Quick Start

```bash
# Install all dependencies (run once)
sudo bash install.sh

# Launch the application
python3 main.py
```

## Required Software

The install script automatically installs the following. If installing manually, ensure these are present:

| Software | Type | Purpose |
|----------|------|---------|
| python3-pip | System | Python package manager |
| python3-tk | System | Tkinter GUI framework |
| psycopg2-binary | Python | PostgreSQL database adapter |
| Pillow | Python | Image loading (JPEG, TIF) |
| pygame | Python | Audio playback (MP3, WAV) |

PostgreSQL with the `photon` database and `student` role must already be configured on the virtual system.

## Gameplay

1. **Splash Screen** - Logo displays for 3 seconds
2. **Player Entry** - Enter player IDs and assign equipment IDs for both Red and Green teams
3. **Countdown** - 30-second countdown before game begins
4. **Game Action** - 6-minute game with live scoring, event log, and music

## Keyboard Shortcuts

| Key | Screen | Action |
|-----|--------|--------|
| F5 / F3 | Player Entry | Start game |
| F12 | Player Entry | Clear all entries |
| F1 | Play Action | Return to player entry (after game ends) |
| Escape | Any | Quit application |

## Network Configuration

- **Transmit**: Sends UDP packets to `127.0.0.1:7500` by default
- **Receive**: Listens on `0.0.0.0:7501`
- **Protocol**: Messages are `"int:int"` format (transmitter:target)
- **Game codes**: 202 = start, 221 = end, 53 = red base, 43 = green base
- **Changing the network**: On the Player Entry screen, enter a different IP address in the "UDP Network Address" field and click "Set" to broadcast to a different host

## File Structure

```
main.py                        - App entry point, screen transitions
settings.py                    - Constants, paths, configuration
install.sh                     - Automated Debian dependency installer
screens/
  splash_screen.py             - 3-second logo display
  player_entry_screen.py       - Player/team entry UI
  play_action_screen.py        - Live game scoreboard, event log, timer
  countdown_display.py         - 30-second pre-game countdown
core/
  game_state.py                - Player dataclass and game state model
  scoring_engine.py            - Scoring logic (tags, friendly fire, base hits)
  database.py                  - PostgreSQL queries (psycopg2)
  network.py                   - UDP transmit/receive with threading
  music_manager.py             - MP3/WAV playback (pygame)
assets/                        - Images, sounds, and music
docs/                          - Reference photos and videos
```

## Scoring

| Event | Points |
|-------|--------|
| Tag an opponent | +10 |
| Friendly fire (both players) | -10 each |
| Hit enemy base (codes 53/43) | +100 |
