# TMNT: Splintered Fate — Save Editor

A browser-based save editor for TMNT: Splintered Fate Steam or Epic. This was made with the help of claude, the game softlocked me out of a few artifacts and there was no way to try and get them without restarting progress. I saw no one else had made one so I wanted to make one.

## Usage

https://shabbypenguin.github.io/TMNT-SF-Saveeditor/

https://tmntsf.shabbygames.club/ - Beta newer changes get pushed here first.

### Loading a save
Drag and drop a save file onto the drop zone, or click to browse. Save files are named:
```
saveSlot_GameState0_cloud.json
saveSlot_GameState1_cloud.json
```
Located in the game's local data folder. On Windows that is `%appdata%\TMNTSF`. Make copies of your saves before editing.

### Exporting
Click **EXPORT SAVE** and drop the downloaded file back into your TMNTSF save folder, replacing the original.

---

## What you can edit

### Artifacts tab
- **Add** any artifact to your inventory (starts at Lv 1)
- **Remove** an artifact by decreasing its level below 1
- **Adjust level** between 1 and the artifact's max level using +/−

### Stats tab

**Currency**
- Set available Dreamer Coins (light) and Dragon Coins (dark) directly

**Per character**
- Shredder victories, deaths, victories, talismans, and wraps per character

**Global stats**
- Runs, kills, room clears, portal entries, enemy kills broken down by type, miniboss and boss records, arena victories, and more
- Search bar filters across all stat sections
- Advanced / hidden stats toggle for internal fields

### Current Run tab
- View and inject any power from the full power grid (all trees, all tiers)
- Set power levels (Lv 1–3)
- Select active tool from all confirmed tools
- Set current artifact
- Adjust scrap, dice, revives, and health for this run
- Add and adjust inspirations and masteries
- SELECT ALL / DESELECT, MAX ALL, ZERO ALL bulk controls
- Per-tree SELECT TREE toggle
- Conflict detection — shows which powers will be replaced in a given slot

### Upgrades Tab
- View Dragon and Dreamer altar upgrades and set levels
- Zero out all upgrades
- Max level all upgrades
- Toggle overleveling (some upgrades can go as high as level 99)

---

## Notes

- The editor preserves the original save's binary format exactly — header, MD5 checksum, size fields, and zlib compression are all recalculated correctly on export
- Power injection writes the correct `enhancement_symbol` for each power so upgrades apply properly in-game
- Tool injection sets the correct per-tool `kit_sym` in `run.stats.equipped` so the game recognises the active tool

---

## Changelog

### 2026-05-29 — Major run editor overhaul

**Power system**
- All **132 powers** fully mapped with confirmed buff_syms and enh_syms, sourced from live saves
- All 7 power trees (Flame, Water, Ooze, Ninja, Utrom, Robotics, Astral Light/Dark) plus Legendary, Dash, and cross-tree powers
- Slot enforcement: selecting a Strike/Abilities/Dash/Charged power removes the conflicting one
- Throwing Arts Ricochet ↔ Chakram mutual exclusion
- Powers without a confirmed enh_sym are blocked from injection (prevents broken upgrades)
- Conflict indicator shows which power will be replaced before you commit

**Tools**
- All pool tools now injectable with correct enh_sym and per-tool kit_sym:
  - Shuriken Storm, Ooze Shuriken, Smoke Bomb, Fireball, Meteor Storm, Ride the Wave all confirmed
  - Default tools (Leo Shuriken, Utrom Drone, Raphael Turtle Line, Michelangelo Taunt, Casey Juice, Donatello Hardened Shell, Alopex Kunai, Utrom Rod) all confirmed
  - Water Sweep ID unconfirmed — hidden from list until resolved
- Each pool tool uses its own `kit_sym` key (Ride the Wave = `1002778670`; all others share `-751219635`)

**Inspirations & Masteries**
- All 14 character inspirations confirmed with altar syms and enh_syms (Mikey, Leo, Raph, Don, Casey, Metalhead, Alopex — both slots each)
- 19 masteries confirmed with enh_syms including shared masteries (Dash Attack, Special charges 30% faster, Barrier Damage, Crit Damage) and character-specific ones for Leo, Alopex, and others
- Altar level display synced from run kit_sym to lifetime altar stat

**Bug fixes**
- Removed stale/wrong decompile IDs that were blocking correct powers (Unknown Ninja C, Unknown Astral Dark B, Unknown Utrom B, wrong Shuriken Breaker/Laser Strike IDs)
- Fixed Frostfire and Bright Spring display (duplicate ENHANCEMENTS entries caused wrong name lookup)
- Slippery correctly identified (was mislabeled as Spontaneous Combustion)
- JS syntax corruption from simultaneous insertion at same position — added post-edit syntax verification

---

## Screenshots

<img width="1767" height="1257" alt="TMNT1" src="https://github.com/user-attachments/assets/ec98162f-4367-4ee0-927f-33afe5dd5636" />

---

<img width="1767" height="1257" alt="TMNT2" src="https://github.com/user-attachments/assets/e095634c-3451-4998-857f-d9378cd9fbcb" />

---

<img width="1767" height="1257" alt="TMNT3" src="https://github.com/user-attachments/assets/415b1d4d-e942-4ee3-a1a3-e800396430a0" />

---

<img width="1767" height="1257" alt="TMNT4" src="https://github.com/user-attachments/assets/f66b78fa-34bc-41ae-9ec7-bf7d709f662b" />