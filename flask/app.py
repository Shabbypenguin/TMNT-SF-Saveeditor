import os
import sys
import zlib
import json
import shutil
import struct
import hashlib
import threading
from datetime import datetime
from pathlib import Path
from flask import Flask, jsonify, request, send_file

# ---------------------------------------------------------------------------
# Locate index.html
# ---------------------------------------------------------------------------

if getattr(sys, 'frozen', False):
    base_dir   = Path(sys._MEIPASS)
    INDEX_HTML = base_dir / 'index.html'
else:
    base_dir   = Path(__file__).parent
    INDEX_HTML = (base_dir / '..' / 'index.html').resolve()

if not INDEX_HTML.exists():
    raise FileNotFoundError(f'Could not find index.html at {INDEX_HTML}')

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Serve index.html and media
# ---------------------------------------------------------------------------

@app.route('/')
def index():
    return send_file(INDEX_HTML)

@app.route('/media/<path:filename>')
def media(filename):
    return send_file(INDEX_HTML.parent / 'media' / filename)

# ---------------------------------------------------------------------------
# Save file location
# ---------------------------------------------------------------------------

def get_save_dir():
    if sys.platform == 'win32':
        base = os.environ.get('APPDATA', '')
        candidate = Path(base) / 'TMNTSF'
        if candidate.exists():
            return candidate
    elif sys.platform == 'darwin':
        candidate = Path.home() / 'Library' / 'Application Support' / 'TMNTSF'
        if candidate.exists():
            return candidate
    else:
        candidate = Path.home() / '.local' / 'share' / 'TMNTSF'
        if candidate.exists():
            return candidate
        steam = Path.home() / '.steam' / 'steam' / 'steamapps' / 'compatdata'
        if steam.exists():
            for app_dir in steam.iterdir():
                probe = app_dir / 'pfx' / 'drive_c' / 'users' / 'steamuser' / 'AppData' / 'Roaming' / 'TMNTSF'
                if probe.exists():
                    return probe
    return None


def get_backup_dir():
    if getattr(sys, 'frozen', False):
        base = Path(sys.executable).parent
    else:
        base = Path(__file__).parent
    d = base / 'TMNTSF_backups'
    d.mkdir(exist_ok=True)
    return d

# ---------------------------------------------------------------------------
# zlib helpers
# ---------------------------------------------------------------------------

def find_zlib_offset(data: bytes) -> int:
    for i in range(len(data) - 1):
        if data[i] == 0x78 and data[i+1] in (0x9c, 0xda, 0x01):
            return i
    return -1


def md5_upper(s: str) -> str:
    return hashlib.md5(s.encode('utf-8')).hexdigest().upper()


def decompress_save(path: Path):
    raw = path.read_bytes()
    off = find_zlib_offset(raw)
    if off == -1:
        raise ValueError('No zlib stream found in save file')
    js = zlib.decompress(raw[off:]).decode('utf-8').rstrip('\x00')
    return json.loads(js), raw, off


def repack_save(save_obj: dict, raw_buf: bytes, zlib_off: int) -> bytes:
    js = json.dumps(save_obj, separators=(',', ':')) + '\x00'
    jb = js.encode('utf-8')
    compressed = zlib.compress(jb, level=6)
    hdr = bytearray(raw_buf[:zlib_off])
    hdr[8:40] = md5_upper(js).encode('ascii')
    struct.pack_into('<I', hdr, 41, len(jb))
    struct.pack_into('<I', hdr, 45, len(compressed))
    return bytes(hdr) + compressed

# ---------------------------------------------------------------------------
# API routes
# ---------------------------------------------------------------------------

@app.route('/api/savedir')
def api_savedir():
    d = get_save_dir()
    return jsonify({'path': str(d) if d else None, 'found': d is not None})


@app.route('/api/slots')
def api_slots():
    d = get_save_dir()
    if not d:
        return jsonify({'error': 'Save folder not found', 'slots': []})
    slots = []
    for i in range(3):
        fname = f'saveSlot.GameState{i}.cloud.json'
        p = d / fname
        if p.exists():
            try:
                save, _, _ = decompress_save(p)
                # Enrich with run summary (hero/chapter/slot powers) for the slot picker.
                # Names are resolved client-side; we send raw IDs only.
                hero = None
                chapter = None
                slot_powers = {}
                try:
                    state = save.get('state', {}) or {}
                    run = state.get('run', {}) or {}
                    lvl = state.get('level', {}) or {}
                    enh = run.get('enhancements', []) or []
                    # A run is "active" only if there are run enhancements (hero is meaningful)
                    if enh:
                        hero = run.get('hero')
                        chapter = lvl.get('current_chapter')
                        # buff_symbols occupying each slot (strike/abilities/dash); first match wins
                        SLOTS = {
                            'strike':    {-54411067, -1068283913, -27946384, -1936580441, 85174008, 65597839},
                            'abilities': {1212610709, -549683561, -1569557381, -1516693114, -312114001, -1400563463},
                            'dash':      {-1364872862, -1917187826, 1938928338, 1765260001, 1357762756, -519913461},
                        }
                        for e in enh:
                            bs = e.get('buff_symbol')
                            for sname, syms in SLOTS.items():
                                if bs in syms and sname not in slot_powers:
                                    slot_powers[sname] = bs
                except Exception:
                    pass
                slots.append({'slot': i, 'filename': fname,
                               'handle': save.get('handle', ''),
                               'player_id': save.get('player_id', ''),
                               'hero': hero, 'chapter': chapter,
                               'slot_powers': slot_powers, 'exists': True})
            except Exception as e:
                slots.append({'slot': i, 'filename': fname, 'exists': True, 'error': str(e)})
        else:
            slots.append({'slot': i, 'filename': fname, 'exists': False})
    return jsonify({'slots': slots})


@app.route('/api/load/<int:slot>')
def api_load(slot):
    d = get_save_dir()
    if not d:
        return jsonify({'error': 'Save folder not found'}), 404
    p = d / f'saveSlot.GameState{slot}.cloud.json'
    if not p.exists():
        return jsonify({'error': f'Slot {slot} not found'}), 404
    try:
        save, _, _ = decompress_save(p)
        return jsonify({'save': save, 'slot': slot})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/save/<int:slot>', methods=['POST'])
def api_save(slot):
    d = get_save_dir()
    if not d:
        return jsonify({'error': 'Save folder not found'}), 404
    p = d / f'saveSlot.GameState{slot}.cloud.json'
    if not p.exists():
        return jsonify({'error': f'Slot {slot} not found'}), 404
    data = request.get_json()
    if not data or 'save' not in data:
        return jsonify({'error': 'No save data provided'}), 400
    try:
        backup_dir = get_backup_dir()
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f'saveSlot.GameState{slot}.cloud_{ts}.json'
        shutil.copy2(p, backup_dir / backup_name)
    except Exception as e:
        return jsonify({'error': f'Backup failed: {e}'}), 500
    try:
        _, raw, off = decompress_save(p)
        p.write_bytes(repack_save(data['save'], raw, off))
        return jsonify({'success': True, 'backup': backup_name})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/backups/<int:slot>')
def api_backups(slot):
    backup_dir = get_backup_dir()
    prefix = f'saveSlot.GameState{slot}.cloud_'
    backups = sorted(
        [f.name for f in backup_dir.iterdir() if f.name.startswith(prefix)],
        reverse=True
    )
    return jsonify({'backups': backups})


@app.route('/api/restore/<int:slot>/<backup_name>', methods=['POST'])
def api_restore(slot, backup_name):
    d = get_save_dir()
    if not d:
        return jsonify({'error': 'Save folder not found'}), 404
    backup_dir = get_backup_dir()
    src = backup_dir / backup_name
    if not src.exists():
        return jsonify({'error': 'Backup not found'}), 404
    if not backup_name.startswith(f'saveSlot.GameState{slot}.cloud_'):
        return jsonify({'error': 'Slot mismatch'}), 400
    shutil.copy2(src, d / f'saveSlot.GameState{slot}.cloud.json')
    return jsonify({'success': True})

# ---------------------------------------------------------------------------
# Entry point — Flask in thread, pywebview as the window
# ---------------------------------------------------------------------------

def run_flask():
    app.run(host='127.0.0.1', port=5173, debug=False, use_reloader=False)


if __name__ == '__main__':
    import webview

    # Start Flask in background thread
    t = threading.Thread(target=run_flask, daemon=True)
    t.start()

    # Small delay to let Flask bind
    import time
    time.sleep(0.5)

    # Open pywebview window — closing it exits the process
    webview.create_window(
        'TMNT: Splintered Fate — Save Editor',
        'http://127.0.0.1:5173/?mode=desktop',
        width=1400,
        height=900,
        min_size=(900, 600),
    )
    webview.start()
