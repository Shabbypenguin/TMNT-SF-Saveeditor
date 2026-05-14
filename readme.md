# TMNT: Splintered Fate — Save Editor

A browser-based save editor for TMNT: Splintered Fate Steam or Epic. This was made with the help of claude, the game softlocked me out of a few artifacts and there was no way to try and get them without restarting progress. I saw no one else had made one so I wanted to make one.

## Usage

https://shabbypenguin.github.io/TMNT-SF-Saveeditor/

https://tmntsf.shabbygames.club/

### Loading a save
Drag and drop a save file onto the drop zone, or click to browse. Save files are named:
```
saveSlot_GameState0_cloud.json
saveSlot_GameState1_cloud.json
```
Located in the game's local data folder. On windows that is %appdata%\TMNTSF, be sure to make copies of your save before any edits.

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

---

## Notes

- The editor preserves the original save's binary format exactly — header, MD5 checksum, size fields, and float serialization are all recalculated correctly on export
