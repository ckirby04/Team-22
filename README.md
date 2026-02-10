# Photon Laser Tag - Main Software

Main software for the Photon Laser Tag system. Provides a GUI for player entry and live game action with real-time scoring, communicating with game equipment via UDP.

## Prerequisites

- Debian-based Linux (tested on Debian VM)
- Python 3.8+
- PostgreSQL with `photon` database and `student` role
- Network access on UDP ports 7500 (transmit) and 7501 (receive)

## Quick Start

```bash
# Install all dependencies (run once)
sudo bash install.sh

# Launch the application
python3 main.py
```

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

- **Transmit**: Sends UDP packets to `127.0.0.1:7500`
- **Receive**: Listens on `0.0.0.0:7501`
- **Protocol**: Messages are `"int:int"` format (transmitter:target)
- **Game codes**: 202 = start, 221 = end, 53 = red base, 43 = green base

## Testing with Traffic Generator

```bash
# In a separate terminal, run the traffic generator
cd udp_files
python3 python_trafficgenarator_v2.py
```

Enter the equipment IDs that match the players you registered. The traffic generator waits for code 202, then sends random hit events until it receives code 221.

## File Structure

```
main.py                  - App entry point, screen transitions
settings.py              - Constants, paths, configuration
game_state.py            - Player dataclass and game state model
scoring_engine.py        - Scoring logic (tags, friendly fire, base hits)
database.py              - PostgreSQL queries (psycopg2)
network.py               - UDP transmit/receive with threading
music_manager.py         - MP3/WAV playback (pygame)
splash_screen.py         - 3-second logo display
player_entry_screen.py   - Player/team entry UI
play_action_screen.py    - Live game scoreboard, event log, timer
countdown_display.py     - 30-second pre-game countdown
install.sh               - Automated Debian dependency installer
```

## Dependencies

- **tkinter** - GUI framework
- **psycopg2-binary** - PostgreSQL adapter
- **Pillow** - Image loading (JPEG, TIF)
- **pygame** - Audio playback (MP3, WAV)
