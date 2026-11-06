"""
Gow Language Editor by Nicho (texture editor)
God of War 1 & 2 (PS2): replace the TEXTURES inside .WAD files (nothing else).
Open an ISO (or a WAD / a folder of WADs) -> pick a WAD -> pick a texture ->
Export PNG / Replace from PNG -> SAVE.
Languages: Bahasa Indonesia, English, Português (Brasil).

Run:  python gow_texture_tool.py      (Python 3.8+, no extra libraries)
"""
import base64
import json
import os
import shutil
import struct
import sys
import tempfile
import traceback
import zlib
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

APP_NAME = "Gow Language Editor by Nicho"  # judul jendela (ubah di sini bila perlu)
SETTINGS_FILE = "texture_tools_settings.json"
LANGS = (("id", "Bahasa Indonesia"), ("en", "English"), ("pt", "Português (Brasil)"))
LANG = "en"
_LI = {"id": 0, "en": 1, "pt": 2}

# kunci: (Indonesia, English, Português-BR)
I18N = {
    "btn_iso": ("Buka ISO", "Open ISO", "Abrir ISO"),
    "btn_wad": ("Buka WAD", "Open WAD", "Abrir WAD"),
    "btn_dir": ("Buka folder WAD", "Open WAD folder", "Abrir pasta de WADs"),
    "btn_save": ("SIMPAN", "SAVE", "SALVAR"),
    "btn_save_as": ("Simpan sebagai", "Save As", "Salvar como"),
    "lbl_lang": ("Bahasa:", "Language:", "Idioma:"),
    "lbl_search": ("Cari tekstur:", "Search textures:", "Pesquisar texturas:"),
    "tree_head": ("Sumber", "Source", "Fonte"),
    "c_name": ("Nama", "Name", "Nome"),
    "c_size": ("Ukuran", "Size", "Tamanho"),
    "c_colors": ("Warna", "Colors", "Cores"),
    "c_status": ("Status", "Status", "Status"),
    "st_ok": ("bisa diedit", "editable", "editável"),
    "st_keep": ("palet asli dipertahankan", "original palette kept", "paleta original mantida"),
    "st_no": ("tidak didukung", "unsupported", "não suportado"),
    "btn_export": ("Export PNG", "Export PNG", "Exportar PNG"),
    "btn_replace": ("Replace dari PNG", "Replace from PNG", "Substituir por PNG"),
    "lbl_preview": ("Pratinjau", "Preview", "Pré-visualização"),
    "pick_tex": ("Pilih satu tekstur dulu.", "Select a texture first.", "Selecione uma textura primeiro."),
    "info": ("Info", "Info", "Info"),
    "err_title": ("Error", "Error", "Erro"),
    "status_none": (
        "Buka ISO, WAD, atau folder WAD dulu.",
        "Open an ISO, a WAD, or a WAD folder first.",
        "Abra primeiro uma ISO, um WAD ou uma pasta de WADs."),
    "wad_info": (
        "%s [%s]: %d tekstur, %d bisa diedit",
        "%s [%s]: %d textures, %d editable",
        "%s [%s]: %d texturas, %d editáveis"),
    "not_wad": ("Bukan WAD", "Not a WAD", "Não é um WAD"),
    "not_gow": (
        "File ini tidak dikenali sebagai WAD God of War.",
        "This file is not recognized as a God of War WAD.",
        "Este arquivo não é reconhecido como um WAD de God of War."),
    "too_big": (
        "File ini %d MB, terlalu besar untuk sebuah WAD (kemungkinan PAK atau ISO).\nUntuk ISO pakai tombol Buka ISO.",
        "This file is %d MB, too large for a WAD (probably a PAK or an ISO).\nFor an ISO use the Open ISO button.",
        "Este arquivo tem %d MB, grande demais para um WAD (provavelmente PAK ou ISO).\nPara uma ISO use o botão Abrir ISO."),
    "dir_none": (
        "Tidak ada file WAD God of War di folder itu.",
        "No God of War WAD files in that folder.",
        "Nenhum arquivo WAD de God of War nessa pasta."),
    "dir_info": ("%s: %d WAD", "%s: %d WADs", "%s: %d WADs"),
    "iso_bad": (
        "File ini bukan ISO9660 yang bisa dibaca (tidak ada penanda CD001).",
        "This file is not a readable ISO9660 image (no CD001 marker).",
        "Este arquivo não é uma imagem ISO9660 legível (sem o marcador CD001)."),
    "iso_info": ("%s: %d PAK", "%s: %d PAKs", "%s: %d PAKs"),
    "iso_nopak": (
        "ISO ini tidak berisi file PAK.",
        "This ISO contains no PAK files.",
        "Esta ISO não contém arquivos PAK."),
    "btn_restore": ("Kembalikan ISO", "Restore ISO", "Restaurar ISO"),
    "toc_missing": (
        "GODOFWAR.TOC tidak ditemukan di ISO ini, jadi isi PAK tidak bisa dibaca.",
        "GODOFWAR.TOC was not found in this ISO, so the PAK contents cannot be read.",
        "O GODOFWAR.TOC não foi encontrado nesta ISO, então o conteúdo do PAK não pode ser lido."),
    "toc_bad": (
        "GODOFWAR.TOC tidak bisa dibaca (format tidak dikenali) atau lokasinya tidak cocok dengan isi PAK.",
        "GODOFWAR.TOC could not be read (unknown format) or its locations do not match the PAK contents.",
        "Não foi possível ler o GODOFWAR.TOC (formato desconhecido) ou suas posições não correspondem ao conteúdo do PAK."),
    "pak_err": (
        "(daftar WAD tidak bisa dibaca)", "(the WAD list could not be read)", "(não foi possível ler a lista de WADs)"),
    "pak_empty": ("(tidak ada WAD di PAK ini)", "(no WADs in this PAK)", "(nenhum WAD neste PAK)"),
    "pak_loading": ("Membaca daftar WAD ...", "Reading the WAD list ...", "Lendo a lista de WADs ..."),
    "pak_info": (
        "%s: %d WAD (%s)",
        "%s: %d WADs (%s)",
        "%s: %d WADs (%s)"),
    "iso_wad_fail": (
        "Tidak bisa membaca WAD dari ISO: %s",
        "Could not read the WAD from the ISO: %s",
        "Não foi possível ler o WAD da ISO: %s"),
    "iso_check_fail": (
        "Lokasi WAD di ISO tidak cocok (penanda WAD tidak ditemukan di %s). Tidak ada yang ditulis.",
        "The WAD location in the ISO does not match (no WAD marker found at %s). Nothing was written.",
        "A posição do WAD na ISO não confere (marcador de WAD não encontrado em %s). Nada foi gravado."),
    "iso_saved": (
        "WAD ditulis ke ISO di %d lokasi:\n%s\n\nBackup isi asli (untuk Kembalikan ISO):\n%s",
        "WAD written into the ISO at %d location(s):\n%s\n\nBackup of the original content (for Restore ISO):\n%s",
        "WAD gravado na ISO em %d local(is):\n%s\n\nBackup do conteúdo original (para Restaurar ISO):\n%s"),
    "restore_ask": (
        "Kembalikan semua perubahan tekstur di ISO ini ke kondisi asli (dari backup)?",
        "Restore every texture change in this ISO to the original state (from the backup)?",
        "Restaurar todas as alterações de textura desta ISO ao estado original (a partir do backup)?"),
    "restore_none": (
        "Tidak ada file backup untuk ISO ini.",
        "There is no backup file for this ISO.",
        "Não há arquivo de backup para esta ISO."),
    "restore_ok": (
        "ISO dikembalikan: %d bagian dipulihkan dari backup.",
        "ISO restored: %d region(s) recovered from the backup.",
        "ISO restaurada: %d trecho(s) recuperado(s) do backup."),
    "restore_pick": (
        "Pilih ISO yang sudah dibuka di pohon kiri dulu.",
        "Select an opened ISO in the left tree first.",
        "Selecione primeiro uma ISO aberta na árvore à esquerda."),
    "iso_busy": ("Menulis ke ISO ...", "Writing to the ISO ...", "Gravando na ISO ..."),
    "no_unsup": (
        "Tekstur ini tidak didukung untuk diedit (%s).",
        "This texture cannot be edited (%s).",
        "Esta textura não pode ser editada (%s)."),
    "why_format": ("format warna lain", "other color format", "outro formato de cor"),
    "why_palette": ("palet khusus", "special palette", "paleta especial"),
    "why_layout": ("ukuran tidak standar", "non-standard size", "tamanho fora do padrão"),
    "why_size": ("ukuran data tidak cocok", "data size mismatch", "tamanho dos dados incompatível"),
    "why_header": ("header rusak", "damaged header", "cabeçalho danificado"),
    "exp_title": ("Simpan PNG", "Save PNG", "Salvar PNG"),
    "exp_ok": ("Export OK: %s (%dx%d)", "Exported: %s (%dx%d)", "Exportado: %s (%dx%d)"),
    "ask_png": ("PNG pengganti", "Replacement PNG", "PNG de substituição"),
    "ft_png": ("Gambar PNG", "PNG image", "Imagem PNG"),
    "ft_all": ("Semua file", "All files", "Todos os arquivos"),
    "e_png": (
        "PNG tidak bisa dibaca. Simpan ulang sebagai PNG biasa (tanpa interlace).",
        "The PNG could not be read. Save it again as a regular (non-interlaced) PNG.",
        "Não foi possível ler o PNG. Salve novamente como PNG comum (sem entrelaçamento)."),
    "e_png_interlace": (
        "PNG dengan interlace tidak didukung. Simpan ulang tanpa interlace.",
        "Interlaced PNGs are not supported. Save it again without interlacing.",
        "PNGs entrelaçados não são suportados. Salve novamente sem entrelaçamento."),
    "resize_t": ("Ukuran berbeda", "Different size", "Tamanho diferente"),
    "resize_q": (
        "PNG-mu %dx%d, tekstur aslinya %dx%d.\nSesuaikan ukuran otomatis (nearest, cocok untuk pixel art)?",
        "Your PNG is %dx%d, the original texture is %dx%d.\nResize automatically (nearest, good for pixel art)?",
        "Seu PNG tem %dx%d, a textura original tem %dx%d.\nRedimensionar automaticamente (nearest, bom para pixel art)?"),
    "rep_ok": (
        "%s diganti (palet baru: %d warna). Klik SIMPAN.",
        "%s replaced (new palette: %d colors). Click SAVE.",
        "%s substituída (nova paleta: %d cores). Clique em SALVAR."),
    "rep_keep": (
        "%s diganti memakai palet aslinya (palet dipakai bersama atau ganda), supaya aman. Klik SIMPAN.",
        "%s replaced using its original palette (shared or dual palette) to stay safe. Click SAVE.",
        "%s substituída usando a paleta original (compartilhada ou dupla) para ficar seguro. Clique em SALVAR."),
    "rep_fail": ("Gagal mengganti", "Replace failed", "Falha ao substituir"),
    "saved_t": ("Tersimpan", "Saved", "Salvo"),
    "saved_status": ("Tersimpan: %s", "Saved: %s", "Salvo: %s"),
    "saved_text": (
        "Hasil edit ditulis ke:\n%s\n\n%s",
        "The edited result was written to:\n%s\n\n%s",
        "O resultado editado foi gravado em:\n%s\n\n%s"),
    "bak_new": (
        "Salinan WAD asli (sebelum diedit) disimpan di:\n%s",
        "A copy of the original WAD (before editing) was saved at:\n%s",
        "Uma cópia do WAD original (antes da edição) foi salva em:\n%s"),
    "bak_old": (
        "Backup lama tetap dipakai (tidak ditimpa):\n%s",
        "The existing backup was kept (not overwritten):\n%s",
        "O backup existente foi mantido (não sobrescrito):\n%s"),
    "saved_as": (
        "Hasil edit ditulis ke:\n%s\n\nWAD asli tidak diubah.",
        "The edited result was written to:\n%s\n\nThe original WAD was not changed.",
        "O resultado editado foi gravado em:\n%s\n\nO WAD original não foi alterado."),
    "save_none": ("Belum ada perubahan untuk disimpan.", "There are no changes to save.", "Não há alterações para salvar."),
    "save_fail": ("Gagal simpan", "Save failed", "Falha ao salvar"),
    "saveas_title": ("Simpan WAD sebagai", "Save WAD as", "Salvar WAD como"),
    "saveas_pick": ("Pilih WAD dulu.", "Select a WAD first.", "Selecione um WAD primeiro."),
    "open_fail": ("Gagal membuka", "Failed to open", "Falha ao abrir"),
    "logged": ("\n\nTercatat di: %s", "\n\nLogged at: %s", "\n\nRegistrado em: %s"),
    "start_fail": ("Gagal start", "Failed to start", "Falha ao iniciar"),
    "lang_pick": (
        "Pilih bahasa\nChoose your language\nEscolha o idioma",
        "Pilih bahasa\nChoose your language\nEscolha o idioma",
        "Pilih bahasa\nChoose your language\nEscolha o idioma"),
}


def tr(key, *args):
    t = I18N[key][_LI.get(LANG, 1)]
    return t % args if args else t


def _settings_dirs():
    base = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, "frozen", False)
                                           else __file__))
    return [base, tempfile.gettempdir()]


def load_lang():
    for d in _settings_dirs():
        try:
            with open(os.path.join(d, SETTINGS_FILE), encoding="utf-8") as f:
                code = json.load(f).get("lang")
            if code in _LI:
                return code
        except (OSError, ValueError):
            continue
    return None


def save_lang(code):
    for d in _settings_dirs():
        try:
            with open(os.path.join(d, SETTINGS_FILE), "w", encoding="utf-8") as f:
                json.dump({"lang": code}, f)
            return True
        except OSError:
            continue
    return False


def log_error(text):
    for d in _settings_dirs():
        try:
            path = os.path.join(d, "texture_tool_error.txt")
            with open(path, "a", encoding="utf-8") as f:
                f.write(text + "\n" + "-" * 60 + "\n")
            return path
        except OSError:
            continue
    return None


# ======================= WAD (GoW 1 dan GoW 2) =======================
HDR = 0x20
ALIGN = 0x10
MAX_WAD_SIZE = 128 * 1024 * 1024
GAMES = {
    1: {"name": "GoW 1", "first_tag": 0x378, "file_tag": 0x1E, "nodata": (0x18, 0x28, 0x32, 0x3E7, 0x29A)},
    2: {"name": "GoW 2", "first_tag": 0x15, "file_tag": 0x01, "nodata": (0x00, 0x02, 0x03, 0x13, 0x16)},
}


def detect_game(head):
    """1 = GoW 1, 2 = GoW 2, 0 = bukan WAD GoW."""
    if len(head) < HDR or head[8:12] != b"WAD_":
        return 0
    tag = struct.unpack_from("<I", head, 0)[0] & 0xFFFF
    for g, d in GAMES.items():
        if tag == d["first_tag"]:
            return g
    return 0


class Entry:
    def __init__(self, hdr_off, tag, size, name, game):
        self.hdr_off, self.tag, self.size, self.name, self.game = hdr_off, tag, size, name, game
        self.data_off = hdr_off + HDR

    @property
    def is_file(self):
        return (self.tag & 0xFFFF) == GAMES[self.game]["file_tag"] and self.size > 0


def scan(buf):
    game = detect_game(bytes(buf[:HDR]))
    if not game:
        return []
    nodata = GAMES[game]["nodata"]
    out, off, n = [], 0, len(buf)
    while off + HDR <= n:
        tag, size = struct.unpack_from("<II", buf, off)
        dsz = 0 if (tag & 0xFFFF) in nodata else size
        if dsz > n - off - HDR:
            break
        name = bytes(buf[off + 8:off + HDR]).split(b"\0")[0].decode("latin1")
        out.append(Entry(off, tag, dsz, name, game))
        off += HDR + ((dsz + ALIGN - 1) & ~(ALIGN - 1))
    return out


# Ikon jendela (PNG 64 px, base64). Ikon exe dipasang saat build (icon.ico).
ICON_B64 = (
    "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"
)


# ======================= MESIN TEKSTUR GoW (PS2) =======================
# GFX_ : header 24 byte [magic 0xC, w, h, 0, bpp, count] + piksel (8bpp: swizzle GS; 4bpp: linear, nibble rendah dulu)
# PAL_ : header 24 byte + warna RGBA (alpha 0..0x80). 256 warna memakai urutan CSM1 (blok 8..15 <-> 16..23)
# TXR_ : 88 byte [7][nama GFX 24][nama PAL 24][parameter]

_SWZ = {}


def swz_map(w, h):
    """index[p] = posisi byte di data swizzle untuk piksel p=y*w+x. None kalau ukuran tidak didukung."""
    key = (w, h)
    if key in _SWZ:
        return _SWZ[key]
    n = w * h
    idx = [0] * n
    ok = True
    for y in range(h):
        for x in range(w):
            block = (y & ~0xF) * w + (x & ~0xF) * 2
            swap = (((y + 2) >> 2) & 1) * 4
            pos_y = (((y & ~3) >> 1) + (y & 1)) & 7
            col = pos_y * w * 2 + ((x + swap) & 7) * 4
            bn = ((y >> 1) & 1) + ((x >> 2) & 2)
            i = block + col + bn
            if i >= n:
                ok = False
            idx[y * w + x] = i
    if ok and len(set(idx)) != n:
        ok = False
    _SWZ[key] = idx if ok else None
    return _SWZ[key]


def pal_swap(pal):
    """Tukar blok 8..15 <-> 16..23 pada tiap 32 entri (berlaku dua arah)."""
    out = list(pal)
    for base in range(0, len(pal) - 31, 32):
        for i in range(8):
            out[base + 8 + i], out[base + 16 + i] = pal[base + 16 + i], pal[base + 8 + i]
    return out


class Tex:
    def __init__(self, gfx, pal, txr_names):
        self.gfx, self.pal = gfx, pal           # Entry
        self.name = gfx.name[4:]
        self.w = self.h = self.bpp = 0
        self.supported = False
        self.reason = ""
        self.shared = False                     # PAL dipakai lebih dari satu GFX
        self.dual = False                       # PAL berisi 2 palet (2072 byte)
        self.txr_names = txr_names


def list_textures(buf, entries):
    """Daftar tekstur (GFX terhubung ke PAL lewat TXR) di satu WAD."""
    by = {e.name: e for e in entries if e.is_file}
    link, users = {}, {}
    for e in entries:
        if e.is_file and e.name.startswith("TXR_") and e.size == 88 and \
                struct.unpack_from("<I", buf, e.data_off)[0] == 7:
            g = bytes(buf[e.data_off + 4:e.data_off + 28]).split(b"\0")[0].decode("latin1")
            p = bytes(buf[e.data_off + 28:e.data_off + 52]).split(b"\0")[0].decode("latin1")
            if g in by and p in by:
                link.setdefault(g, p)
                users.setdefault(p, set()).add(g)
    out = []
    for g, p in link.items():
        t = Tex(by[g], by[p], g)
        t.shared = len(users[p]) > 1
        try:
            m, w, h, z, bpp, c = struct.unpack_from("<6I", buf, t.gfx.data_off)
            pm, pw, ph, pz, pbpp, pc = struct.unpack_from("<6I", buf, t.pal.data_off)
        except struct.error:
            t.reason = "header"
            out.append(t)
            continue
        t.w, t.h, t.bpp = w, h, bpp
        if c != 1 or bpp not in (4, 8):
            t.reason = "format"
        elif t.gfx.size != 24 + w * h * bpp // 8:
            t.reason = "size"
        elif bpp == 8 and not ((t.pal.size == 1048 and (pw, ph, pbpp, pc) == (16, 16, 32, 1))
                               or (t.pal.size == 2072 and (pw, ph, pbpp, pc) == (16, 32, 32, 2))):
            t.reason = "palette"
        elif bpp == 4 and not (t.pal.size == 88 and (pw, ph, pbpp, pc) == (8, 2, 32, 1)):
            t.reason = "palette"
        elif bpp == 4 and (w * h) % 2:
            t.reason = "size"
        elif bpp == 8 and swz_map(w, h) is None:
            t.reason = "layout"
        else:
            t.supported = True
            t.dual = (t.pal.size == 2072)
        out.append(t)
    out.sort(key=lambda t: t.name.lower())
    return out


def read_palette(buf, t):
    """Palet sebagai list (r,g,b,a) dengan a 0..255 (bukan skala PS2), urutan indeks piksel."""
    n = 256 if t.bpp == 8 else 16
    raw = [tuple(buf[t.pal.data_off + 24 + i * 4:t.pal.data_off + 28 + i * 4]) for i in range(n)]
    if t.bpp == 8:
        raw = pal_swap(raw)
    return [(r, g, b, min(255, a * 2)) for r, g, b, a in raw]


def read_indices(buf, t):
    base = t.gfx.data_off + 24
    if t.bpp == 8:
        raw = bytes(buf[base:base + t.w * t.h])
        m = swz_map(t.w, t.h)
        return bytes(raw[m[p]] for p in range(t.w * t.h))
    raw = bytes(buf[base:base + t.w * t.h // 2])
    out = bytearray()
    for v in raw:
        out.append(v & 15)
        out.append(v >> 4)
    return bytes(out)


def decode(buf, t):
    """-> (indices, palette, rgba bytes)"""
    ix, pal = read_indices(buf, t), read_palette(buf, t)
    rgba = bytearray(t.w * t.h * 4)
    for p, i in enumerate(ix):
        rgba[p * 4:p * 4 + 4] = bytes(pal[i])
    return ix, pal, bytes(rgba)


def write_indices(buf, t, ix):
    base = t.gfx.data_off + 24
    if t.bpp == 8:
        m = swz_map(t.w, t.h)
        out = bytearray(t.w * t.h)
        for p, i in enumerate(ix):
            out[m[p]] = i
        buf[base:base + t.w * t.h] = out
    else:
        out = bytearray(t.w * t.h // 2)
        for k in range(len(out)):
            out[k] = (ix[2 * k] & 15) | ((ix[2 * k + 1] & 15) << 4)
        buf[base:base + t.w * t.h // 2] = out


def write_palette(buf, t, pal):
    """pal: list (r,g,b,a) a 0..255 -> disimpan skala PS2 (0..128)."""
    n = 256 if t.bpp == 8 else 16
    pal = list(pal) + [(0, 0, 0, 0)] * (n - len(pal))
    ps2 = [(r, g, b, (a * 128 + 127) // 255) for r, g, b, a in pal[:n]]
    if t.bpp == 8:
        ps2 = pal_swap(ps2)
    for i, c in enumerate(ps2):
        buf[t.pal.data_off + 24 + i * 4:t.pal.data_off + 28 + i * 4] = bytes(c)


# ----------------------------- PNG (tanpa library) -----------------------------
_SIG = b"\x89PNG\r\n\x1a\n"


def _chunk(tag, data):
    c = struct.pack(">I", len(data)) + tag + data
    return c + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)


def png_encode_rgba(w, h, rgba):
    raw = bytearray()
    stride = w * 4
    for y in range(h):
        raw.append(0)
        raw += rgba[y * stride:(y + 1) * stride]
    return (_SIG + _chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
            + _chunk(b"IDAT", zlib.compress(bytes(raw), 6)) + _chunk(b"IEND", b""))


def png_encode_indexed(w, h, ix, pal):
    """PNG berpalet (tipe 3). Memudahkan edit di aplikasi pixel art tanpa mengubah palet."""
    n = len(pal)
    raw = bytearray()
    for y in range(h):
        raw.append(0)
        raw += ix[y * w:(y + 1) * w]
    plte = b"".join(bytes(c[:3]) for c in pal)
    trns = bytes(c[3] for c in pal)
    out = _SIG + _chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 3, 0, 0, 0)) + _chunk(b"PLTE", plte)
    if any(a != 255 for a in trns):
        out += _chunk(b"tRNS", trns)
    return out + _chunk(b"IDAT", zlib.compress(bytes(raw), 6)) + _chunk(b"IEND", b"")


def png_decode(data):
    """-> (w, h, rgba bytes). Mendukung PNG tanpa interlace (gray/RGB/palet/+alpha, 1-16 bit)."""
    if data[:8] != _SIG:
        raise ValueError("png")
    pos, idat, plte, trns = 8, b"", None, None
    w = h = depth = ctype = interlace = 0
    while pos < len(data):
        ln, tag = struct.unpack_from(">I4s", data, pos)
        body = data[pos + 8:pos + 8 + ln]
        pos += 12 + ln
        if tag == b"IHDR":
            w, h, depth, ctype, _c, _f, interlace = struct.unpack(">IIBBBBB", body)
        elif tag == b"PLTE":
            plte = body
        elif tag == b"tRNS":
            trns = body
        elif tag == b"IDAT":
            idat += body
        elif tag == b"IEND":
            break
    if interlace:
        raise ValueError("interlace")
    if ctype not in (0, 2, 3, 4, 6) or depth not in (1, 2, 4, 8, 16):
        raise ValueError("png-format")
    ch = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[ctype]
    bpp_bits = ch * depth
    stride = (w * bpp_bits + 7) // 8
    bpb = max(1, bpp_bits // 8)
    raw = zlib.decompress(idat)
    img = bytearray(h * stride)
    prev = bytearray(stride)
    p = 0
    for y in range(h):
        f = raw[p]
        line = bytearray(raw[p + 1:p + 1 + stride])
        p += 1 + stride
        if f == 1:
            for i in range(bpb, stride):
                line[i] = (line[i] + line[i - bpb]) & 255
        elif f == 2:
            for i in range(stride):
                line[i] = (line[i] + prev[i]) & 255
        elif f == 3:
            for i in range(stride):
                a = line[i - bpb] if i >= bpb else 0
                line[i] = (line[i] + ((a + prev[i]) >> 1)) & 255
        elif f == 4:
            for i in range(stride):
                a = line[i - bpb] if i >= bpb else 0
                b = prev[i]
                c = prev[i - bpb] if i >= bpb else 0
                pa, pb, pc = abs(b - c), abs(a - c), abs(a + b - 2 * c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[i] = (line[i] + pr) & 255
        elif f != 0:
            raise ValueError("png-filter")
        img[y * stride:(y + 1) * stride] = line
        prev = line

    def samples(y):
        row = img[y * stride:(y + 1) * stride]
        if depth == 8:
            return list(row)
        if depth == 16:
            return [row[i] for i in range(0, len(row), 2)]
        out = []
        mask = (1 << depth) - 1
        for byte in row:
            for k in range(8 // depth):
                out.append((byte >> (8 - depth * (k + 1))) & mask)
        return out[:w * ch]

    scale = 255 // ((1 << depth) - 1) if depth < 8 and ctype != 3 else 1
    out = bytearray(w * h * 4)
    trns_g = struct.unpack(">H", trns[:2])[0] if (ctype == 0 and trns) else None
    for y in range(h):
        s = samples(y)
        o = y * w * 4
        for x in range(w):
            if ctype == 6:
                r, g, b, a = s[x * 4:x * 4 + 4]
            elif ctype == 2:
                r, g, b = s[x * 3:x * 3 + 3]
                a = 255
            elif ctype == 0:
                r = g = b = s[x] * scale
                a = 0 if (trns_g is not None and s[x] == trns_g) else 255
            elif ctype == 4:
                r = g = b = s[x * 2]
                a = s[x * 2 + 1]
            else:
                i = s[x]
                r, g, b = plte[i * 3:i * 3 + 3]
                a = trns[i] if (trns and i < len(trns)) else 255
            out[o + x * 4:o + x * 4 + 4] = bytes((r, g, b, a))
    return w, h, bytes(out)


# ----------------------------- kuantisasi warna -----------------------------
def quantize(rgba, n):
    """-> (indices bytes, palette list). Warna unik <= n dipetakan persis; selain itu median-cut."""
    cnt = {}
    for p in range(0, len(rgba), 4):
        k = rgba[p:p + 4]
        cnt[k] = cnt.get(k, 0) + 1
    # piksel transparan penuh dianggap satu warna
    uniq = list(cnt)
    if len(uniq) <= n:
        pal = [tuple(k) for k in uniq]
        look = {k: i for i, k in enumerate(uniq)}
    else:
        boxes = [[(tuple(k), cnt[k]) for k in uniq]]
        while len(boxes) < n:
            best, bi, brange = None, -1, 0
            for i, bx in enumerate(boxes):
                if len(bx) < 2:
                    continue
                for ch in range(4):
                    vs = [c[0][ch] for c in bx]
                    r = max(vs) - min(vs)
                    if r > brange:
                        best, bi, brange = ch, i, r
            if bi < 0:
                break
            bx = boxes.pop(bi)
            bx.sort(key=lambda c: c[0][best])
            half, acc, cut = sum(c[1] for c in bx) / 2.0, 0, 1
            for j, c in enumerate(bx):
                acc += c[1]
                if acc >= half:
                    cut = min(max(j + 1, 1), len(bx) - 1)
                    break
            boxes.append(bx[:cut])
            boxes.append(bx[cut:])
        pal, look = [], {}
        for i, bx in enumerate(boxes):
            tot = sum(c[1] for c in bx)
            avg = tuple(int(sum(c[0][ch] * c[1] for c in bx) / tot + 0.5) for ch in range(4))
            pal.append(avg)
            for c in bx:
                look[bytes(c[0])] = i
    ix = bytearray(len(rgba) // 4)
    for p in range(len(ix)):
        ix[p] = look[rgba[p * 4:p * 4 + 4]]
    return bytes(ix), pal


def map_to_palette(rgba, pal):
    """Petakan tiap piksel ke warna terdekat di palet yang sudah ada (aman untuk palet bersama)."""
    cache = {}
    ix = bytearray(len(rgba) // 4)
    for p in range(len(ix)):
        k = rgba[p * 4:p * 4 + 4]
        v = cache.get(k)
        if v is None:
            r, g, b, a = k
            best, bd = 0, 1 << 60
            for i, (pr, pg, pb, pa) in enumerate(pal):
                d = (r - pr) ** 2 + (g - pg) ** 2 + (b - pb) ** 2 + 2 * (a - pa) ** 2
                if d < bd:
                    best, bd = i, d
                    if d == 0:
                        break
            cache[k] = v = best
        ix[p] = v
    return bytes(ix)


def replace_texture(buf, t, rgba, keep_palette=False):
    """Tulis ulang tekstur t dari RGBA (ukuran harus sama). Palet asli dipertahankan bila
    keep_palette, palet bersama (shared), atau palet ganda (dual) -> gambar dipetakan ke warna asli."""
    n = 256 if t.bpp == 8 else 16
    if keep_palette or t.shared or t.dual:
        pal = read_palette(buf, t)
        ix = map_to_palette(rgba, pal)
    else:
        ix, pal = quantize(rgba, n)
        write_palette(buf, t, pal)
    write_indices(buf, t, ix)
    return len(pal)


# ======================= ISO9660 (PS2, sektor 2048 byte) =======================
class Iso9660:
    """Pembaca ISO9660 sederhana: daftar file + baca byte. Tidak memuat ISO ke memori."""
    SECTOR = 2048

    def __init__(self, path):
        self.path = path
        self.f = open(path, "rb")
        self.f.seek(16 * self.SECTOR)
        pvd = self.f.read(self.SECTOR)
        if len(pvd) < self.SECTOR or pvd[1:6] != b"CD001" or pvd[0] != 1:
            self.f.close()
            raise ValueError("iso")
        self.root_lba = struct.unpack_from("<I", pvd, 156 + 2)[0]
        self.root_size = struct.unpack_from("<I", pvd, 156 + 10)[0]

    def close(self):
        self.f.close()

    def read(self, lba, off, n):
        self.f.seek(lba * self.SECTOR + off)
        return self.f.read(n)

    def listdir(self, lba, size):
        """Yield (nama, is_dir, lba, size) untuk isi satu direktori."""
        data = self.read(lba, 0, size)
        pos = 0
        while pos < len(data):
            ln = data[pos]
            if ln == 0:  # sisa sektor kosong -> lompat ke sektor berikutnya
                pos = (pos // self.SECTOR + 1) * self.SECTOR
                continue
            rec = data[pos:pos + ln]
            pos += ln
            if len(rec) < 34:
                continue
            nlen = rec[32]
            raw = rec[33:33 + nlen]
            if raw in (b"\x00", b"\x01"):
                continue
            name = raw.decode("latin1").split(";")[0]
            yield (name, bool(rec[25] & 2), struct.unpack_from("<I", rec, 2)[0],
                   struct.unpack_from("<I", rec, 10)[0])

    def files(self, depth=8):
        """Semua file di ISO: list (path, lba, size)."""
        out = []

        def walk(lba, size, prefix, d):
            for name, is_dir, l, s in self.listdir(lba, size):
                if is_dir:
                    if d > 0:
                        walk(l, s, prefix + name + "/", d - 1)
                else:
                    out.append((prefix + name, l, s))
        walk(self.root_lba, self.root_size, "", depth)
        return out


# ======================= GODOFWAR.TOC + PAK =======================
PART_BASE = 10_000_000   # GoW 2: lokasi >= 10.000.000 berarti PART berikutnya (sektor lokal = nilai - 10.000.000)


class TocEntry:
    def __init__(self, name, size, locs):
        self.name, self.size = name, size
        self.locs = locs            # [(part 0-based, sektor 2048 byte relatif awal PART)]


def _printable(s):
    return bool(s) and all(32 <= ord(c) < 127 for c in s)


def parse_toc(data):
    """Baca GODOFWAR.TOC GoW 1 atau GoW 2 -> (game, [TocEntry]). ValueError kalau tidak dikenali."""
    n = len(data)
    if n >= 40:
        c = struct.unpack_from("<I", data, 0)[0]
        if 0 < c < 100000 and 4 + 36 * c <= n and (n - 4 - 36 * c) % 4 == 0 and \
                _printable(bytes(data[4:28]).split(b"\0")[0].decode("latin1")):
            # GoW 2: [u32 jumlah] + c x [nama 24, ukuran, jumlah salinan, indeks] + tabel u32 lokasi
            tail = struct.unpack_from("<%dI" % ((n - 4 - 36 * c) // 4), data, 4 + 36 * c)
            out = []
            for i in range(c):
                o = 4 + 36 * i
                name = bytes(data[o:o + 24]).split(b"\0")[0].decode("latin1")
                size, copies, idx = struct.unpack_from("<III", data, o + 24)
                if not _printable(name) or copies < 1 or idx + copies > len(tail):
                    continue
                locs = [(tail[idx + k] // PART_BASE, tail[idx + k] % PART_BASE) for k in range(copies)]
                out.append(TocEntry(name, size, locs))
            if out:
                return 2, out
    # GoW 1: rekaman 24 byte = nama 12 + part u32 + ukuran u32 + sektor u32
    out = []
    for i in range(n // 24):
        o = i * 24
        name = bytes(data[o:o + 12]).split(b"\0")[0].decode("latin1")
        part, size, sec = struct.unpack_from("<III", data, o + 12)
        if _printable(name) and "." in name and part < 8:
            out.append(TocEntry(name, size, [(part, sec)]))
    if len(out) >= 10:
        return 1, out
    raise ValueError("toc")


class IsoGame:
    """Satu ISO God of War: ISO9660 + TOC + file PART*.PAK."""

    def __init__(self, path):
        self.path = path
        self.iso = Iso9660(path)
        self.files = self.iso.files()
        self.paks = {}                # part 0-based -> (nama, lba, ukuran)
        self.toc_ents, self.game = None, 0
        found = sorted((n.split("/")[-1], l, s) for n, l, s in self.files if n.upper().endswith(".PAK"))
        for name, l, s in found:
            m = [c for c in name.upper().replace(".PAK", "") if c.isdigit()]
            if name.upper().startswith("PART") and m:
                self.paks[int("".join(m)) - 1] = (name, l, s)
        if not self.paks:             # cadangan: urut abjad
            for i, (name, l, s) in enumerate(found):
                self.paks[i] = (name, l, s)

    def pak_list(self):
        return [(i,) + self.paks[i] for i in sorted(self.paks)]

    def load_toc(self):
        """Parse TOC sekali. Return (game, entries) atau raise ValueError('missing'/'toc')."""
        if self.toc_ents is not None:
            return self.game, self.toc_ents
        toc = [(n, l, s) for n, l, s in self.files if n.split("/")[-1].upper() == "GODOFWAR.TOC"]
        if not toc:
            raise ValueError("missing")
        _n, lba, size = toc[0]
        self.game, self.toc_ents = parse_toc(self.iso.read(lba, 0, size))
        return self.game, self.toc_ents

    def abs_lba(self, part, sector):
        if part not in self.paks:
            raise ValueError("part")
        return self.paks[part][1] + sector

    def wads_in_part(self, part):
        """WAD yang lokasi pertamanya ada di PART ini dan header-nya valid. VPK/VAG/PSS/PSW diabaikan."""
        _g, ents = self.load_toc()
        out = []
        for e in ents:
            if not e.name.upper().endswith(".WAD") or e.locs[0][0] != part:
                continue
            try:
                head = self.iso.read(self.abs_lba(*e.locs[0]), 0, HDR)
            except (ValueError, OSError):
                continue
            if detect_game(head):
                out.append(e)
        return sorted(out, key=lambda e: e.name.upper())

    def read_wad(self, entry):
        return bytearray(self.iso.read(self.abs_lba(*entry.locs[0]), 0, entry.size))

    def close(self):
        self.iso.close()


def backup_path(iso_path):
    return iso_path + ".texbak"


def _read_backup(path):
    """Isi backup: list (offset, bytes)."""
    out = []
    try:
        with open(path, "rb") as f:
            if f.read(8) != b"GOWTXBK1":
                return out
            while True:
                h = f.read(12)
                if len(h) < 12:
                    break
                off, ln = struct.unpack("<QI", h)
                data = f.read(ln)
                if len(data) < ln:
                    break
                out.append((off, data))
    except OSError:
        pass
    return out


def write_wad_to_iso(game, entry, buf):
    """Tulis WAD hasil edit ke SEMUA lokasi di ISO. Backup isi asli ke NAMA.iso.texbak lebih dulu.
    Mengembalikan daftar offset yang ditulis. ValueError('check:<offset>') kalau penanda WAD tidak cocok."""
    if len(buf) != entry.size:
        raise ValueError("size")
    offs = [game.abs_lba(*loc) * Iso9660.SECTOR for loc in entry.locs]
    for o in offs:  # periksa semua lokasi sebelum menulis apa pun
        game.iso.f.seek(o)
        if not detect_game(game.iso.f.read(HDR)):
            raise ValueError("check:%d" % o)
    bak = backup_path(game.path)
    known = {o for o, _d in _read_backup(bak)}
    new = [o for o in offs if o not in known]
    if new:
        with open(bak, "ab") as f:
            if f.tell() == 0:
                f.write(b"GOWTXBK1")
            for o in new:
                game.iso.f.seek(o)
                f.write(struct.pack("<QI", o, entry.size) + game.iso.f.read(entry.size))
            f.flush()
            os.fsync(f.fileno())
    game.iso.close()
    try:
        with open(game.path, "r+b") as f:
            for o in offs:
                f.seek(o)
                f.write(buf)
            f.flush()
            os.fsync(f.fileno())
    finally:
        game.iso = Iso9660(game.path)
    return offs


def restore_backup(iso_path):
    """Kembalikan semua bagian dari backup. Return jumlah bagian, atau None kalau tidak ada backup."""
    bak = backup_path(iso_path)
    recs = _read_backup(bak)
    if not recs:
        return None
    with open(iso_path, "r+b") as f:
        for off, data in recs:
            f.seek(off)
            f.write(data)
        f.flush()
        os.fsync(f.fileno())
    os.remove(bak)
    return len(recs)


# ======================= APLIKASI =======================
class WadDoc:
    def __init__(self, path, buf, src=None):
        self.path, self.buf = path, buf
        self.src = src            # None = file biasa; ("iso", IsoGame, TocEntry) = WAD di dalam ISO
        self.entries = scan(buf)
        self.texs = list_textures(buf, self.entries)
        self.dirty = False
        self.game = self.entries[0].game if self.entries else 0


def resize_nearest(rgba, w, h, nw, nh):
    out = bytearray(nw * nh * 4)
    for y in range(nh):
        sy = y * h // nh
        for x in range(nw):
            sx = x * w // nw
            out[(y * nw + x) * 4:(y * nw + x) * 4 + 4] = rgba[(sy * w + sx) * 4:(sy * w + sx) * 4 + 4]
    return bytes(out)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry("980x600")
        try:
            ttk.Style(self).theme_use("clam")
        except tk.TclError:
            pass
        self.set_icon()
        self.sources = []    # [("iso", path, [pak]), ("wad", path), ("dir", path, [wad])]
        self.docs = {}       # kunci -> WadDoc
        self.isos = {}       # path ISO -> IsoGame
        self.meta = {}       # iid -> dict
        self.cur = None      # WadDoc terpilih
        self.cur_tex = []    # Tex yang tampil di daftar
        self._st = ("status_none", ())
        self._img = None
        self.build_ui()

    def set_icon(self):
        try:
            self._icon = tk.PhotoImage(data=ICON_B64)
            self.iconphoto(True, self._icon)
        except Exception:
            pass

    # ---- tampilan ----
    def build_ui(self):
        bar = ttk.Frame(self)
        bar.pack(fill="x", padx=8, pady=6)
        ttk.Button(bar, text=tr("btn_iso"), command=self.open_iso).pack(side="left")
        ttk.Button(bar, text=tr("btn_wad"), command=self.open_wad).pack(side="left", padx=4)
        ttk.Button(bar, text=tr("btn_dir"), command=self.open_dir).pack(side="left")
        ttk.Button(bar, text=tr("btn_save"), command=self.save).pack(side="left", padx=(12, 4))
        ttk.Button(bar, text=tr("btn_save_as"), command=self.save_as).pack(side="left")
        ttk.Button(bar, text=tr("btn_restore"), command=self.restore_iso).pack(side="left", padx=(4, 0))
        ttk.Label(bar, text=tr("lbl_lang")).pack(side="left", padx=(16, 4))
        self.lang_box = ttk.Combobox(bar, width=18, state="readonly", values=[n for _c, n in LANGS])
        self.lang_box.current([c for c, _n in LANGS].index(LANG))
        self.lang_box.pack(side="left")
        self.lang_box.bind("<<ComboboxSelected>>", lambda e: self.change_language())

        self.status = ttk.Label(self, text="")
        self.status.pack(fill="x", side="bottom", padx=8, pady=6)

        pw = ttk.PanedWindow(self, orient="horizontal")
        pw.pack(fill="both", expand=True, padx=8)
        left = ttk.Frame(pw)
        self.tree = ttk.Treeview(left, show="tree headings", columns=())
        self.tree.heading("#0", text=tr("tree_head"))
        self.tree.column("#0", width=240)
        sb = ttk.Scrollbar(left, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", lambda e: self.on_tree_select())
        self.tree.bind("<<TreeviewOpen>>", lambda e: self.on_tree_open())
        pw.add(left, weight=1)

        right = ttk.Frame(pw)
        srow = ttk.Frame(right)
        srow.pack(fill="x", pady=(0, 4))
        ttk.Label(srow, text=tr("lbl_search")).pack(side="left")
        self.q = tk.StringVar(value="")
        ttk.Entry(srow, textvariable=self.q).pack(side="left", fill="x", expand=True, padx=6)
        self.q.trace_add("write", lambda *a: self.fill_textures())
        cols = ("name", "size", "colors", "status")
        self.tv = ttk.Treeview(right, columns=cols, show="headings", height=9)
        heads = (tr("c_name"), tr("c_size"), tr("c_colors"), tr("c_status"))
        for c, t, w in zip(cols, heads, (220, 80, 60, 150)):
            self.tv.heading(c, text=t)
            self.tv.column(c, width=w)
        sb2 = ttk.Scrollbar(right, orient="vertical", command=self.tv.yview)
        self.tv.configure(yscrollcommand=sb2.set)
        sb2.pack(side="right", fill="y")
        self.tv.pack(fill="both", expand=True)
        self.tv.bind("<<TreeviewSelect>>", lambda e: self.on_tex_select())
        pw.add(right, weight=3)

        bot = ttk.Frame(self)
        bot.pack(fill="x", padx=8, pady=4)
        ttk.Button(bot, text=tr("btn_export"), command=self.export_png).pack(side="left")
        ttk.Button(bot, text=tr("btn_replace"), command=self.replace_png).pack(side="left", padx=6)
        ttk.Label(bot, text=tr("lbl_preview") + ":").pack(side="left", padx=(16, 4))
        self.preview = ttk.Label(bot, text="")
        self.preview.pack(side="left")
        self.render_tree()
        self.fill_textures()
        self.render_status()

    def set_status(self, key, *args):
        self._st = (key, args)
        self.render_status()

    def render_status(self):
        self.status.config(text=tr(self._st[0], *self._st[1]))

    def change_language(self):
        global LANG
        code = LANGS[self.lang_box.current()][0]
        if code == LANG:
            return
        LANG = code
        save_lang(code)
        for w in list(self.winfo_children()):
            w.destroy()
        self.build_ui()

    def report_callback_exception(self, exc, val, tb):
        text = "".join(traceback.format_exception(exc, val, tb))
        path = log_error(text)
        messagebox.showerror(tr("err_title"), text[-1500:] + (tr("logged", path) if path else ""))

    # ---- pohon sumber ----
    def render_tree(self):
        self.tree.delete(*self.tree.get_children())
        self.meta = {}

        def add(parent, text, **m):
            iid = self.tree.insert(parent, "end", text=text)
            self.meta[iid] = m
            return iid
        for src in self.sources:
            if src[0] == "wad":
                add("", os.path.basename(src[1]), kind="wad", path=src[1])
            elif src[0] == "dir":
                top = add("", os.path.basename(src[1].rstrip("/\\")) or src[1], kind="dir")
                for n in src[2]:
                    add(top, n, kind="wad", path=os.path.join(src[1], n))
                self.tree.item(top, open=True)
            elif src[0] == "iso":
                top = add("", os.path.basename(src[1]), kind="iso", path=src[1])
                for name, part in src[2]:
                    pk = add(top, name, kind="pak", path=src[1], part=part, name=name, shown=False)
                    add(pk, "...", kind="note")  # supaya tanda > muncul
                self.tree.item(top, open=True)

    def on_tree_open(self):
        iid = self.tree.focus()
        m = self.meta.get(iid, {})
        if m.get("kind") != "pak" or m.get("shown"):
            return
        game = self.isos.get(m["path"])
        for c in list(self.tree.get_children(iid)):
            self.tree.delete(c)
            self.meta.pop(c, None)
        m["shown"] = True
        try:
            wads = game.wads_in_part(m["part"])
        except ValueError as ex:
            key = "toc_missing" if str(ex) == "missing" else "toc_bad"
            c = self.tree.insert(iid, "end", text=tr("pak_err"))
            self.meta[c] = {"kind": "note"}
            m["shown"] = False
            messagebox.showerror(tr("open_fail"), tr(key))
            return
        except Exception:
            m["shown"] = False
            messagebox.showerror(tr("open_fail"), traceback.format_exc())
            return
        for e in wads:
            c = self.tree.insert(iid, "end", text=e.name)
            self.meta[c] = {"kind": "isowad", "iso": m["path"], "entry": e}
        if not wads:
            c = self.tree.insert(iid, "end", text=tr("pak_empty"))
            self.meta[c] = {"kind": "note"}
        self.set_status("pak_info", m["name"], len(wads), GAMES[game.game]["name"])

    def on_tree_select(self):
        sel = self.tree.selection()
        m = self.meta.get(sel[0], {}) if sel else {}
        doc = None
        if m.get("kind") == "wad":
            doc = self.load_doc(m["path"])
        elif m.get("kind") == "isowad":
            doc = self.load_iso_doc(m["iso"], m["entry"])
        if doc:
            self.cur = doc
            self.fill_textures()
            self.set_status("wad_info", os.path.basename(doc.path), GAMES[doc.game]["name"],
                            len(doc.texs), sum(1 for t in doc.texs if t.supported))

    def load_iso_doc(self, iso_path, entry):
        key = "iso:%s|%s|%s" % (iso_path, entry.name, entry.locs[0])
        if key in self.docs:
            return self.docs[key]
        try:
            game = self.isos[iso_path]
            buf = game.read_wad(entry)
            if not detect_game(bytes(buf[:HDR])):
                raise ValueError(entry.name)
            doc = self.docs[key] = WadDoc(entry.name, buf, ("iso", game, entry))
            return doc
        except Exception as ex:
            messagebox.showerror(tr("open_fail"), tr("iso_wad_fail", str(ex)))
            return None

    # ---- membuka sumber ----
    def load_doc(self, path):
        if path in self.docs:
            return self.docs[path]
        try:
            size = os.path.getsize(path)
            if size > MAX_WAD_SIZE:
                messagebox.showerror(tr("not_wad"), tr("too_big", size // (1024 * 1024)))
                return None
            with open(path, "rb") as f:
                head = f.read(HDR)
                if not detect_game(head):
                    messagebox.showerror(tr("not_wad"), tr("not_gow"))
                    return None
                f.seek(0)
                buf = bytearray(f.read())
            doc = self.docs[path] = WadDoc(path, buf)
            return doc
        except Exception:
            messagebox.showerror(tr("open_fail"), traceback.format_exc())
            return None

    def open_wad(self):
        p = filedialog.askopenfilename(title=tr("btn_wad"), filetypes=[("WAD", "*.wad *.WAD"), (tr("ft_all"), "*.*")])
        if not p:
            return
        if self.load_doc(p):
            if ("wad", p) not in self.sources:
                self.sources.append(("wad", p))
            self.render_tree()
            for iid, m in self.meta.items():
                if m.get("path") == p and m.get("kind") == "wad":
                    self.tree.selection_set(iid)
                    self.on_tree_select()
                    break

    def open_dir(self):
        d = filedialog.askdirectory(title=tr("btn_dir"))
        if not d:
            return
        names = []
        for n in sorted(os.listdir(d), key=str.lower):
            if not n.lower().endswith(".wad"):
                continue  # VPK, VAG, PSS, PSW dan lainnya disembunyikan
            try:
                with open(os.path.join(d, n), "rb") as f:
                    if detect_game(f.read(HDR)):
                        names.append(n)
            except OSError:
                continue
        if not names:
            messagebox.showinfo(tr("info"), tr("dir_none"))
            return
        self.sources.append(("dir", d, names))
        self.render_tree()
        self.set_status("dir_info", os.path.basename(d.rstrip("/\\")) or d, len(names))

    def open_iso(self):
        p = filedialog.askopenfilename(title=tr("btn_iso"), filetypes=[("ISO", "*.iso *.ISO"), (tr("ft_all"), "*.*")])
        if not p:
            return
        try:
            game = IsoGame(p)
        except ValueError:
            messagebox.showerror(tr("open_fail"), tr("iso_bad"))
            return
        except Exception:
            messagebox.showerror(tr("open_fail"), traceback.format_exc())
            return
        paks = [(name, part) for part, name, _l, _s in game.pak_list()]
        if not paks:
            game.close()
            messagebox.showinfo(tr("info"), tr("iso_nopak"))
            return
        if p in self.isos:
            self.isos[p].close()
        self.isos[p] = game
        self.sources = [s for s in self.sources if not (s[0] == "iso" and s[1] == p)]
        self.sources.append(("iso", p, paks))
        self.render_tree()
        self.set_status("iso_info", os.path.basename(p), len(paks))

    # ---- daftar tekstur & pratinjau ----
    def fill_textures(self):
        self.tv.delete(*self.tv.get_children())
        self.cur_tex = []
        if not self.cur:
            return
        q = self.q.get().strip().lower()
        for t in self.cur.texs:
            if q and q not in t.name.lower():
                continue
            st = (tr("st_keep") if (t.shared or t.dual) else tr("st_ok")) if t.supported else tr("st_no")
            self.tv.insert("", "end", iid=str(len(self.cur_tex)), values=(
                t.name, "%dx%d" % (t.w, t.h), 256 if t.bpp == 8 else 16 if t.bpp == 4 else "-", st))
            self.cur_tex.append(t)

    def selected_tex(self):
        sel = self.tv.selection()
        if not sel or not self.cur:
            messagebox.showinfo(tr("info"), tr("pick_tex"))
            return None
        return self.cur_tex[int(sel[0])]

    def on_tex_select(self):
        sel = self.tv.selection()
        if not sel or not self.cur:
            return
        t = self.cur_tex[int(sel[0])]
        if not t.supported:
            self.preview.config(image="", text=tr("no_unsup", tr("why_" + t.reason)))
            return
        self.show_preview(t)

    def show_preview(self, t):
        _ix, _pal, rgba = decode(self.cur.buf, t)
        png = png_encode_rgba(t.w, t.h, rgba)
        img = tk.PhotoImage(data=base64.b64encode(png))
        big = max(t.w, t.h)
        if big < 200:
            img = img.zoom(max(1, 200 // big))
        elif big > 260:
            img = img.subsample(-(-big // 260))
        self._img = img
        self.preview.config(image=img, text="")

    # ---- export / replace ----
    def export_png(self):
        t = self.selected_tex()
        if not t:
            return
        if not t.supported:
            messagebox.showinfo(tr("info"), tr("no_unsup", tr("why_" + t.reason)))
            return
        path = filedialog.asksaveasfilename(title=tr("exp_title"), defaultextension=".png",
                                            initialfile=t.name + ".png", filetypes=[(tr("ft_png"), "*.png")])
        if not path:
            return
        _ix, _pal, rgba = decode(self.cur.buf, t)
        with open(path, "wb") as f:
            f.write(png_encode_rgba(t.w, t.h, rgba))
        self.set_status("exp_ok", os.path.basename(path), t.w, t.h)

    def replace_png(self):
        t = self.selected_tex()
        if not t:
            return
        if not t.supported:
            messagebox.showinfo(tr("info"), tr("no_unsup", tr("why_" + t.reason)))
            return
        path = filedialog.askopenfilename(title=tr("ask_png"), filetypes=[(tr("ft_png"), "*.png"), (tr("ft_all"), "*.*")])
        if not path:
            return
        try:
            with open(path, "rb") as f:
                w, h, rgba = png_decode(f.read())
        except ValueError as ex:
            messagebox.showerror(tr("rep_fail"), tr("e_png_interlace") if str(ex) == "interlace" else tr("e_png"))
            return
        except (zlib.error, struct.error, IndexError, OSError):
            messagebox.showerror(tr("rep_fail"), tr("e_png"))
            return
        if (w, h) != (t.w, t.h):
            if not messagebox.askyesno(tr("resize_t"), tr("resize_q", w, h, t.w, t.h)):
                return
            rgba = resize_nearest(rgba, w, h, t.w, t.h)
        try:
            n = replace_texture(self.cur.buf, t, rgba)
        except Exception:
            messagebox.showerror(tr("rep_fail"), traceback.format_exc())
            return
        self.cur.dirty = True
        self.show_preview(t)
        if t.shared or t.dual:
            self.set_status("rep_keep", t.name)
        else:
            self.set_status("rep_ok", t.name, n)

    # ---- simpan ----
    def _write(self, doc, path, backup):
        made = False
        if backup:
            bak = path + ".bak"
            if not os.path.exists(bak):
                shutil.copy2(path, bak)
                made = True
        with open(path, "wb") as f:
            f.write(doc.buf)
        doc.dirty = False
        return made

    def save(self):
        dirty = [d for d in self.docs.values() if d.dirty]
        if not dirty:
            messagebox.showinfo(tr("info"), tr("save_none"))
            return
        lines = []
        for d in dirty:
            try:
                if d.src:  # WAD di dalam ISO: tulis ke semua lokasi, backup dulu
                    game, entry = d.src[1], d.src[2]
                    offs = write_wad_to_iso(game, entry, d.buf)
                    d.dirty = False
                    lines.append(tr("iso_saved", len(offs), "\n".join("  0x%X" % o for o in offs),
                                    backup_path(game.path)))
                else:
                    made = self._write(d, d.path, True)
                    bak = d.path + ".bak"
                    lines.append(tr("saved_text", d.path, tr("bak_new", bak) if made else tr("bak_old", bak)))
            except ValueError as ex:
                if str(ex).startswith("check:"):
                    messagebox.showerror(tr("save_fail"), tr("iso_check_fail", "0x%X" % int(str(ex)[6:])))
                else:
                    messagebox.showerror(tr("save_fail"), str(ex))
                return
            except Exception:
                messagebox.showerror(tr("save_fail"), traceback.format_exc())
                return
        self.set_status("saved_status", ", ".join(os.path.basename(d.path) for d in dirty))
        messagebox.showinfo(tr("saved_t"), "\n\n".join(lines))

    def restore_iso(self):
        sel = self.tree.selection()
        m = self.meta.get(sel[0], {}) if sel else {}
        path = m.get("path") or m.get("iso")
        if not path or path not in self.isos:
            isos = [s[1] for s in self.sources if s[0] == "iso"]
            path = isos[0] if len(isos) == 1 else None
        if not path:
            messagebox.showinfo(tr("info"), tr("restore_pick"))
            return
        if not os.path.exists(backup_path(path)):
            messagebox.showinfo(tr("info"), tr("restore_none"))
            return
        if not messagebox.askyesno(tr("btn_restore"), tr("restore_ask")):
            return
        try:
            game = self.isos[path]
            game.close()
            n = restore_backup(path)
            self.isos[path] = IsoGame(path)
            for k in [k for k, d in self.docs.items() if d.src and d.src[1].path == path]:
                del self.docs[k]
            if self.cur is not None and self.cur.src and self.cur.src[1].path == path:
                self.cur = None
                self.fill_textures()
            self.set_status("restore_ok", n)
            messagebox.showinfo(tr("saved_t"), tr("restore_ok", n))
        except Exception:
            messagebox.showerror(tr("save_fail"), traceback.format_exc())

    def save_as(self):
        if not self.cur:
            messagebox.showinfo(tr("info"), tr("saveas_pick"))
            return
        try:
            p = filedialog.asksaveasfilename(title=tr("saveas_title"), initialfile=os.path.basename(self.cur.path))
            if not p:
                return
            self._write(self.cur, p, False)
            self.set_status("saved_status", os.path.basename(p))
            messagebox.showinfo(tr("saved_t"), tr("saved_as", p))
        except Exception:
            messagebox.showerror(tr("save_fail"), traceback.format_exc())


def choose_language():
    root = tk.Tk()
    root.title("Language / Bahasa / Idioma")
    root.geometry("340x250")
    chosen = {"v": None}

    def pick(code):
        chosen["v"] = code
        root.destroy()
    ttk.Label(root, text=I18N["lang_pick"][0], justify="center").pack(pady=14)
    for code, name in LANGS:
        ttk.Button(root, text=name, command=lambda c=code: pick(c)).pack(fill="x", padx=50, pady=5)
    root.mainloop()
    return chosen["v"]


def main():
    global LANG
    try:
        code = load_lang()
        if not code:
            code = choose_language() or "en"
            save_lang(code)
        LANG = code
        app = App()
        if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
            app.after(200, lambda: app.sources.append(("wad", sys.argv[1])) or app.render_tree())
        app.mainloop()
    except Exception:
        text = traceback.format_exc()
        path = log_error(text)
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(tr("start_fail"), text[-1500:] + (tr("logged", path) if path else ""))
        except Exception:
            print(text)
        sys.exit(1)


if __name__ == "__main__":
    main()
