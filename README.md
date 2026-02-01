# my-linux-workstation
Personal Linux workstation configuration (Wayland, niri, Neovim) with scripts and reproducible setup.

## Table of Contents
- [Terminal Setup](#terminal-setup)
- [Neovim Configuration](#neovim-configuration)
- [Claude Code](#claude-code)
- [Window Manager](#window-manager)
  - [Keybindings](#keybindings)
  - [Top Bar (Waybar)](#top-bar-waybar)

## Terminal Setup
- **Terminal Emulator**: [kitty](https://sw.kovidgoyal.net/kitty/)
- **Shell**: [fish](https://fishshell.com/)

> [What's the difference?](https://www.youtube.com/watch?v=hMSByvFHOro) - Terminal vs. Bash vs. Command line vs. Prompt

## Neovim Configuration
<!-- TODO: Document Neovim setup -->

## Claude Code

Configuration for [Claude Code](https://claude.ai/code) AI assistant.

See [`config/claude-code/claude-presets.json`](config/claude-code/claude-presets.json)

## Window Manager

- **Compositor**: [niri](https://github.com/YaLTeR/niri) (Wayland)
- **Desktop**: [omarchy](https://omarchy.app/)

### Keybindings

See full keybindings in [`config/niri/config.kdl`](config/niri/config.kdl)

#### Application Launchers
| Key | Action |
|-----|--------|
| `Mod+Return` | Terminal (kitty) |
| `Mod+F` | File Manager (Nautilus) |
| `Mod+B` | Browser |
| `Mod+Shift+B` | Browser (Private) |
| `Mod+N` | Default Editor |
| `Mod+T` | GNOME Editor |
| `Mod+Shift+T` | Activity (btop) |
| `Mod+D` | Docker (lazydocker) |
| `Mod+M` | Music (Spotify) |
| `Mod+O` | Obsidian |
| `Mod+/` | 1Password |

#### Web Apps
| Key | Action |
|-----|--------|
| `Mod+A` | ChatGPT |
| `Mod+Shift+A` | Grok |
| `Mod+Y` | YouTube |
| `Mod+G` | GitHub |
| `Mod+Shift+G` | WhatsApp |
| `Mod+X` | X (Twitter) |
| `Mod+H` | Discord |
| `Mod+C` | Codeforces |

#### Window Management
| Key | Action |
|-----|--------|
| `Mod+W` | Close Window |
| `Mod+Shift+F` | Expand to Available Width |
| `Mod+Shift+V` | Toggle Floating |
| `Mod+Q` | Toggle Tabbed |
| `Mod+Ctrl+F` | Fullscreen |

#### Navigation
| Key | Action |
|-----|--------|
| `Mod+←/→` | Focus Column Left/Right |
| `Mod+↑/↓` | Focus Window Up/Down |
| `Mod+Shift+←/→` | Move Column Left/Right |
| `Mod+Shift+↑/↓` | Move Window Up/Down |

#### Workspaces
| Key | Action |
|-----|--------|
| `Mod+1-9` | Switch to Workspace |
| `Mod+Shift+1-9` | Move to Workspace |
| `Mod+U/I` | Focus Workspace Up/Down |
| `Mod+Ctrl+U/I` | Move to Workspace Up/Down |

**Workspace Layout:**
| # | Apps |
|---|------|
| 1 | Vivaldi |
| 2 | VSCode / Sublime |
| 3 | Terminal |
| 4 | Obsidian |
| 5 | Discord / Slack |

#### Screenshots
| Key | Action |
|-----|--------|
| `Print` | Screenshot |
| `Ctrl+Print` | Screenshot Screen |
| `Alt+Print` | Screenshot Window |

#### System
| Key | Action |
|-----|--------|
| `Mod+Escape` | Settings/Power |
| `Mod+Shift+S` | Suspend |
| `Mod+Alt+S` | Lock & Suspend |

### Top Bar (Waybar)

See config: [`config/waybar/config.jsonc`](config/waybar/config.jsonc)

**Modules:**
| Position | Modules |
|----------|---------|
| Left | Omarchy Menu, Workspaces |
| Center | Clock, Update Indicator, Screen Recording |
| Right | Language, Tray, Bluetooth, Network, Audio, CPU, Battery |
