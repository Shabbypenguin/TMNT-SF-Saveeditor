# TMNT: Splintered Fate — Save Editor

A save editor for TMNT: Splintered Fate (Steam / Epic). Made with the help of Claude after the game softlocked me out of a few artifacts with no way to recover them without restarting. No one else had made one, so here we are.

---

## Web editor (no install)

**https://shabbypenguin.github.io/TMNT-SF-Saveeditor/**

**https://tmntsf.shabbygames.club/** — beta, newer changes land here first

Load a save file by dragging it onto the drop zone or clicking to browse. Save files are named:
```
saveSlot.GameState0.cloud.json
saveSlot.GameState1.cloud.json
saveSlot.GameState2.cloud.json
```
On Windows they live in `%appdata%\TMNTSF`. Make a backup before editing. When you're done, click **EXPORT SAVE** and drop the file back into your TMNTSF folder.

---

## Desktop app (exe)

A standalone Windows app that finds your save folder automatically, lets you pick a slot, saves directly back to the right place, and keeps automatic backups of every change.

### Download

Grab the latest `TMNTSF_SaveEditor.exe` from the [Releases](../../releases) page. No installation needed — just double-click it.

> **Requirement:** Windows 10 or 11 with [Microsoft Edge WebView2](https://developer.microsoft.com/en-us/microsoft-edge/webview2/) installed. This is pre-installed on most up-to-date Windows systems. If the app does not open, install the WebView2 runtime from that link.

### Features

- **Auto-detects your save folder** — opens straight to a slot picker showing all three save slots with their character names
- **Saves directly back** — no downloading and copying files manually
- **Automatic backups** — every time you save, a timestamped backup is written to a `TMNTSF_backups` folder next to the exe before anything is overwritten
- **Backup restore** — view all backups for a slot and restore any of them with one click
- **Switch slot** — jump between save slots without restarting
- Closing the window fully exits the app — no background processes left running

---

## Update notifications

Both the web and desktop editors check for a newer build on launch and show a banner at the top of the window if one is available, linking straight to the Releases page. The check is silent if you're offline or already up to date, and never blocks the editor from loading.

---

## Building the exe yourself

Requirements: Python 3.10+ on Windows.

**1. Install dependencies**
```
pip install flask pywebview pyinstaller
```

**2. Clone the repo**
```
git clone https://github.com/Shabbypenguin/TMNT-SF-Saveeditor.git
cd TMNT-SF-Saveeditor
```

**3. Build**
```
pyinstaller tool-src/TMNTSF_SaveEditor.spec
```

The finished exe will be at `dist/TMNTSF_SaveEditor.exe`. It is fully self-contained — the editor, all images, and the Python runtime are bundled inside. Copy it anywhere and run it.

> **Note:** The spec file expects `index.html` and `media/` to be in the repo root (one level above `tool-src/`). Do not move things around.

---

## What you can edit

### Artifacts tab
- Add any artifact to your inventory (starts at Lv 1)
- Remove an artifact by decreasing its level below 1
- Adjust level between 1 and the artifact's max using +/−

### Current Run tab

**Powers**
- Full power grid across all trees: Flame, Water, Ooze, Ninja, Utrom, Robotics, Astral Light, Astral Dark, Legendary, and Dash
- 132 powers mapped with correct enhancement symbols — upgrades apply properly in-game
- Slot enforcement: picking a Strike/Abilities/Dash/Charged power automatically removes the conflicting one
- Level powers from Lv 1 to Lv 3
- Conflict indicator shows which power will be replaced before you commit
- SELECT ALL, DESELECT, MAX ALL, ZERO ALL bulk controls
- Per-tree SELECT TREE toggle

**Tools** CURRENTLY BROKEN, THE WAY THE GAME HANDLES IT ISNT AS CLEAN OR AS EASY AS I THOUGHT
- One active tool per run. Selecting a tool swaps it in; the editor mirrors the game exactly — your hero's default kit tool is preserved and the swapped tool is set as active. Picking a different tool replaces the previous swap.
- Default kit tools (one per hero): Leo Shuriken, Michelangelo Taunt, Raphael Turtle Line, Donatello Hardened Shell, Casey Juice, Alopex Kunai, Metalhead Landmines
- Pool / store tools selectable as swaps: Shuriken Storm, Ooze Shuriken, Fireball, Meteor Storm, Smoke Bomb, Ride the Wave, Water Sweep, Utrom Drone, Utrom Rod, Utrom Shuriken, Attack Drone, Unstable Canister

**Inspirations & Masteries**
- All 14 character inspirations (2 per hero) injectable with correct altar sync
- Inspiration levels are read by the game from your Dragon Coin altar upgrades, not the run entry — the editor edits the altar level that actually applies
- Confirmed masteries for multiple heroes plus shared masteries (Dash Attack, Special charges 30% faster, Crit Damage, Barrier Damage, and more)

**Other**
- Adjust scrap, dice, revives, and HP for the current run
- Set active artifact

### Stats tab

**Currency**
- Set available Dreamer Coins and Dragon Coins directly

**Per character**
- Shredder victories, deaths, victories, talismans, and wraps per character

**Boss records**
- Leatherhead, Karai, Bebop & Rocksteady, Shredder (by character and by build), Punk Frog Mech — victories, variants, hard clears

**Global stats**
- Runs, kills, room clears, portal entries, enemy kills broken down by type, miniboss records, arena victories, and more
- Search bar filters all sections
- Advanced / hidden stats toggle

### Upgrades tab
- View Dragon and Dreamer altar upgrades and set levels
- Zero out all upgrades
- Max all upgrades
- Toggle overleveling — uncapped upgrades go as high as level 99, while locked upgrades (inspirations and similar) stay capped at their real in-game max

---

## Notes

- The editor preserves the original save's binary format exactly — header, MD5 checksum, size fields, and zlib compression are all recalculated correctly on export
- Power injection writes the correct `enhancement_symbol` for each power so in-game upgrade rooms display and apply properly
- All buff_syms and enh_syms were sourced from live save files, not decompiles — several decompile IDs were wrong and have been corrected

---

## Changelog

### 2026-05-31 — Tool mechanism, dedup, update check

- **Save slots better display information.** Save slots now match characters in current run. May expand this to include some other staple stats.
- **Tool inject has been disabled for now.** Wasn't working so I made sure to stop it before it breaks stuff.
- **Tweaked updater code.**
- **Fixed CSS to fix the Flask display.**

### 2026-05-31 — Tool mechanism, dedup, update check

- **Tool handling rewritten to match the game.** Confirmed across many live saves that the active tool is the non-default (swapped) tool, with the hero's default kit tool always preserved; swapping replaces the prior swap rather than stacking. Injection now enforces this exactly, in all cases including unknown heroes and saves missing a default entry.
- **Water Sweep** confirmed and added as a proper tool.
- **Metalhead fixes:** corrected an inverted mapping — Landmines is Metalhead's default tool, and Inspiration 1 is now mapped correctly.
- **Mikey and Raph inspirations** now lock at their real altar max even with overleveling enabled, matching the other heroes.
- **Data cleanup:** removed a large batch of duplicate internal entries (deduped to 207 unique), so every entry resolves to the correct definition.
- **Update check:** the editor now notifies you on launch when a newer build is available, with a dismissible banner linking to Releases.
- **Polish:** added a favicon and a version badge, and removed unused dead code.

### 2026-05-30 — Desktop app

- Standalone Windows exe via PyInstaller + pywebview
- Opens as a native app window (no browser tab needed)
- Auto-detects `%appdata%\TMNTSF` save folder
- Slot picker on launch with character names
- Direct save-back to game folder
- Automatic timestamped backups before every write
- Backup viewer and one-click restore
- Closing the window fully exits — no background processes

### 2026-05-29 — Major run editor overhaul

- 132 powers fully mapped with confirmed buff_syms and enh_syms from live saves
- Complete tool coverage confirmed from live saves
- All 14 character inspirations confirmed with altar syms
- Masteries confirmed including hero-specific and shared masteries
- Slot enforcement and conflict detection for all power trees
- Removed stale/wrong decompile IDs (Unknown Ninja C, Unknown Astral Dark B, Unknown Utrom B, wrong Shuriken Breaker/Laser Strike IDs)
- Fixed Frostfire, Bright Spring, and Slippery display (mislabeled or duplicate entries)

---

## Screenshots

<img width="1767" height="1257" alt="TMNT1" src="https://github.com/user-attachments/assets/ec98162f-4367-4ee0-927f-33afe5dd5636" />

---

<img width="1767" height="1257" alt="TMNT2" src="https://github.com/user-attachments/assets/e095634c-3451-4998-857f-d9378cd9fbcb" />

---

<img width="1767" height="1257" alt="TMNT3" src="https://github.com/user-attachments/assets/415b1d4d-e942-4ee3-a1a3-e800396430a0" />

---

<img width="1767" height="1257" alt="TMNT4" src="https://github.com/user-attachments/assets/f66b78fa-34bc-41ae-9ec7-bf7d709f662b" />
