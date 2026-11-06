========================================================================
 GOW TEXTURE EDITOR (Gow Language Editor by Nicho)  -  v1.0
 Texture editor for God of War 1 & 2 (PS2) WAD files
========================================================================

PACKAGE CONTENTS
  Readme-Eng.txt         : these instructions (English)
  Information-Eng.txt    : what the tool can and cannot do
  Readme-Indo.txt / Informasi-Indo.txt      : Bahasa Indonesia version
  Leia-me-Br.txt / Informacoes-Br.txt       : Português (Brasil) version
  Texture Editor\        : the program folder (Texture_Editor.exe + support files)

IMPORTANT: do not move Texture_Editor.exe alone to another place. It needs the DLLs
and files next to it. Keep the WHOLE "Texture Editor" folder together.

WHAT IS IT?
A PC tool (Windows and Wine/Winlator) that replaces the TEXTURES inside God of War 1
and God of War 2 (PS2) WAD files. Textures only: the tool does not change any other
file inside the WAD, and it does not change the WAD size.

HOW TO USE
  1. Run Texture_Editor.exe. On the first launch you choose a language
     (Indonesia / English / Português); you can change it any time in the main window.
  2. Open a source:
       Open ISO         : reads a God of War ISO; click > on PART1.PAK / PART2.PAK to see the WADs.
       Open WAD         : opens a single .WAD file.
       Open WAD folder  : lists every .WAD in a folder.
     Other files (VPK, VAG, PSS/PSW, and so on) are hidden.
  3. Click a WAD in the "Source" tree (left). The texture list appears on the right.
     Type in "Search textures" to filter. Select a texture to see its preview.
  4. "Export PNG" saves the texture as a PNG image. Edit that PNG in your favorite
     image / pixel-art editor (do not change its size).
  5. "Replace from PNG" puts your edited PNG into that texture.
  6. Click SAVE. The result is written to the original WAD and a copy of the untouched
     WAD is kept once as NAME.WAD.bak. "Save As" writes to another file.

ISO AND PAK
  Open ISO reads a God of War 1 or 2 ISO and shows PART1.PAK and PART2.PAK. Click the >
  next to one to see the WADs inside (read through GODOFWAR.TOC in the ISO; VPK, VAG,
  PSS/PSW files are not shown). Pick a WAD, edit its textures, then SAVE: the edited WAD is
  written straight into the ISO, at EVERY copy location (GoW 2 stores some WADs in more
  than one place). Because the WAD size never changes, nothing shifts.
  Before writing, the tool checks the WAD marker at each location and saves the original
  content to NAME.iso.texbak. The "Restore ISO" button recovers everything from that backup.
  IMPORTANT: work on a COPY of the ISO, and close other programs that use that ISO.

ABOUT THE IMAGE
  - The PNG must have the same size as the original texture. If it differs, the tool
    offers to resize it automatically (nearest, good for pixel art).
  - PS2 textures use a palette: at most 256 colors (8-bit textures) or 16 colors
    (4-bit textures). The tool converts your PNG colors to the palette automatically.
    Pixel art with few colors comes out exact; full-color images get reduced.
  - Textures whose palette is shared with other textures, or that have a dual palette,
    are marked "original palette kept": your image colors are mapped to the original
    palette so other textures / the second palette are not broken.
  - PNG transparency is supported (PS2 alpha is scaled 0 to 128).

BEGINNER TIPS
  - Always work on a COPY. Keep your original ISO / PAK.
  - Change one texture per test, then try it in the game.
  - Do not change the image size and do not add many colors unless needed.

IF YOU FIND AN ERROR / BUG
The tool logs errors to texture_tool_error.txt (next to the exe) and shows the location
in the error window. Send that error text (or a photo) with the names of the WAD and
texture you opened to the tool's author.

WINLATOR / WINE
Use this folder version (not a single-file exe). If the file dialog misbehaves, move the
WAD to an easy-to-reach folder and use Open WAD folder.

========================================================================
 Gow Language Editor by Nicho
========================================================================
