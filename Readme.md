<p align="center">
  <img src="icon.png" alt="GoW Texture Editor" width="160">
</p>

<h1 align="center">GoW Texture Editor</h1>

<p align="center">
  Replace the <b>textures</b> inside <b>God of War 1 &amp; 2 (PS2)</b> <code>.WAD</code> files.<br>
  Windows · Wine · Winlator &nbsp;|&nbsp; by <b>Nicho</b>
</p>

<p align="center">
  <a href="#english">English</a> ·
  <a href="#bahasa-indonesia">Bahasa Indonesia</a> ·
  <a href="#português-brasil">Português (Brasil)</a>
</p>

---

## English

### What is it?
A PC tool that edits **textures only** inside God of War 1 and God of War 2 (PS2) WAD files. Export a texture as PNG, edit it in any image / pixel-art editor, put it back, save. The WAD size never changes, and nothing else inside the WAD is touched.

The app has its own language selector: **Bahasa Indonesia, English, Português (Brasil)**.

### Features
- Open a **GoW 1 / GoW 2 ISO** (PART1.PAK / PART2.PAK → WAD list via `GODOFWAR.TOC`), a single **WAD**, or a **folder of WADs**.
- Only WADs are shown; **VPK, VAG, PSS/PSW** and other files are hidden.
- Texture list with search and live **preview**.
- **Export PNG** / **Replace from PNG** (with transparency).
- 8-bit (256 colors) and 4-bit (16 colors) PS2 textures, with automatic palette conversion.
- **SAVE** straight into the ISO (every copy of the WAD, with a `.texbak` backup) + **Restore ISO**; for loose WADs a `.bak` copy is kept. **Save As** too.

### Coverage (from the WADs scanned by the author)
| Game | WADs | Linked textures | Editable |
|------|-----:|----------------:|---------:|
| GoW 1 | 216 | 6,623 | 6,591 |
| GoW 2 | 292 | 8,427 | 8,327 |

The rest use other color formats or non-standard sizes and are shown as *unsupported*. WADs that were never scanned cannot be guaranteed.

### Download
- **Actions artifact:** open the *Actions* tab → latest run → artifact **Texture Editor**.
- **Releases:** push a tag like `v1.0` and the workflow publishes `Texture Editor.zip`.

The package contains the readme / information files in 3 languages and the folder **`Texture Editor`** (`Texture_Editor.exe` + DLLs).
> ⚠️ Keep the **whole** `Texture Editor` folder together; do not move the `.exe` alone.

### How to use
1. Run `Texture_Editor.exe` (the first launch asks for a language).
2. **Open ISO / Open WAD / Open WAD folder**.
3. Click a WAD in the **Source** tree, then a texture in the list.
4. **Export PNG** → edit it (keep the same size) → **Replace from PNG**.
5. **SAVE**.

### Important notes
- **ISO / PAK:** click the `>` next to `PART1.PAK` / `PART2.PAK` to list the WADs. Saving writes the WAD in place at **every** copy location after checking the WAD marker, and keeps the original bytes in `NAME.iso.texbak` (button **Restore ISO**). Work on a **copy** of the ISO.
- **Colors:** at most 256 (8-bit) or 16 (4-bit) colors per texture. Textures whose palette is shared with others, or that have a dual palette, keep their **original palette** (your image is mapped to it) so nothing else breaks.
- **Image size** must match the original (the tool can resize with *nearest*).
- **Not tested on a real ISO / in-game yet.** Automated tests: 14,918 textures read → written back **byte-identical**; PNG round trips without differences; the ISO/TOC reader was verified on simulated ISOs built from the real GoW 1 / GoW 2 `GODOFWAR.TOC` and real WADs.

### Out of scope
Anything other than textures inside a WAD (3D models, audio, text), standalone VPK/VAG/PSS/PSW files, loose `PART*.PAK` files outside an ISO, and rebuilding ISOs.

### Run from source / build
```bash
python gow_texture_tool.py          # Python 3.8+, no extra libraries
```
Windows build: run `build.bat`, or let **GitHub Actions** (`.github/workflows/build.yml`) build `Texture Editor.zip` for you (folder build, Python 3.10, works on Wine/Winlator).

### Reporting bugs
The app writes errors to `texture_tool_error.txt` (next to the exe) and shows the location in the error window. Send that text plus the names of the WAD and texture you opened.

### Legal
No game files are included. Use it only with your own copy of the game. Fan project, not affiliated with Sony or Santa Monica Studio. *God of War* is a trademark of its owners. Provided as is, without warranty.

### Credits
Made by **Nicho**. Thanks to the **God of War Browser** project and to **AssetForge**, which helped in understanding the file structure and the workflow.

---

## Bahasa Indonesia

### Apa ini?
Tool PC untuk mengedit **tekstur saja** di dalam file WAD God of War 1 dan God of War 2 (PS2). Export tekstur jadi PNG, edit di aplikasi gambar / pixel art apa saja, masukkan lagi, lalu simpan. Ukuran WAD tidak pernah berubah, dan tidak ada yang lain di dalam WAD yang disentuh.

Aplikasinya punya pilihan bahasa sendiri: **Bahasa Indonesia, English, Português (Brasil)**.

### Fitur
- Buka **ISO GoW 1 / GoW 2** (PART1.PAK / PART2.PAK → daftar WAD lewat `GODOFWAR.TOC`), satu **WAD**, atau **folder WAD**.
- Hanya WAD yang tampil; **VPK, VAG, PSS/PSW** dan file lain disembunyikan.
- Daftar tekstur dengan pencarian dan **pratinjau**.
- **Export PNG** / **Replace dari PNG** (mendukung transparansi).
- Tekstur PS2 8-bit (256 warna) dan 4-bit (16 warna), palet diubah otomatis.
- **SIMPAN** langsung ke ISO (semua salinan WAD, dengan backup `.texbak`) + **Kembalikan ISO**; untuk WAD lepas disimpan salinan `.bak`. Ada juga **Simpan sebagai**.

### Cakupan (dari WAD yang dipindai pembuat)
| Game | WAD | Tekstur terhubung | Bisa diedit |
|------|----:|------------------:|------------:|
| GoW 1 | 216 | 6.623 | 6.591 |
| GoW 2 | 292 | 8.427 | 8.327 |

Sisanya berformat warna lain atau ukuran tidak standar dan ditandai *tidak didukung*. WAD yang belum pernah dipindai tidak bisa dijamin.

### Unduh
- **Artifact Actions:** tab *Actions* → run terbaru → artifact **Texture Editor**.
- **Releases:** push tag seperti `v1.0`, workflow akan menerbitkan `Texture Editor.zip`.

Paketnya berisi file readme / informasi tiga bahasa dan folder **`Texture Editor`** (`Texture_Editor.exe` + DLL).
> ⚠️ Bawa **seluruh** folder `Texture Editor`; jangan memindahkan `.exe`-nya saja.

### Cara pakai
1. Jalankan `Texture_Editor.exe` (pertama kali diminta memilih bahasa).
2. **Buka ISO / Buka WAD / Buka folder WAD**.
3. Klik sebuah WAD di pohon **Sumber**, lalu sebuah tekstur di daftar.
4. **Export PNG** → edit (ukuran harus sama) → **Replace dari PNG**.
5. **SIMPAN**.

### Catatan penting
- **ISO / PAK:** klik `>` di sebelah `PART1.PAK` / `PART2.PAK` untuk melihat daftar WAD. Saat menyimpan, WAD ditulis di tempatnya ke **semua** lokasi salinan setelah penanda WAD diperiksa, dan isi aslinya disimpan di `NAMA.iso.texbak` (tombol **Kembalikan ISO**). Kerjakan di **salinan** ISO.
- **Warna:** maksimal 256 (8-bit) atau 16 (4-bit) warna per tekstur. Tekstur dengan palet bersama atau palet ganda tetap memakai **palet aslinya** (gambarmu dipetakan ke palet itu) supaya tidak ada yang rusak.
- **Ukuran gambar** harus sama dengan aslinya (tool bisa menyesuaikan dengan *nearest*).
- **Belum diuji di ISO asli / di game.** Uji otomatis: 14.918 tekstur dibaca → ditulis ulang **identik byte demi byte**; PNG bolak-balik tanpa selisih; pembaca ISO/TOC diverifikasi pada ISO tiruan dari `GODOFWAR.TOC` asli GoW 1 / GoW 2 dan WAD asli.

### Di luar cakupan
Apa pun selain tekstur di dalam WAD (model 3D, suara, teks), file VPK/VAG/PSS/PSW yang berdiri sendiri, file `PART*.PAK` lepas di luar ISO, dan membangun ulang ISO.

### Menjalankan dari kode sumber / build
```bash
python gow_texture_tool.py          # Python 3.8+, tanpa library tambahan
```
Build Windows: jalankan `build.bat`, atau biarkan **GitHub Actions** (`.github/workflows/build.yml`) membuat `Texture Editor.zip` (build folder, Python 3.10, jalan di Wine/Winlator).

### Melaporkan bug
Aplikasi mencatat error ke `texture_tool_error.txt` (di samping exe) dan menampilkan lokasinya di jendela error. Kirim teks itu beserta nama WAD dan tekstur yang kamu buka.

### Hukum
Tidak memuat file game. Gunakan hanya dengan salinan game milikmu sendiri. Proyek penggemar, tidak berafiliasi dengan Sony atau Santa Monica Studio. *God of War* adalah merek dagang pemiliknya. Disediakan apa adanya, tanpa jaminan.

### Kredit
Dibuat oleh **Nicho**. Terima kasih kepada proyek **God of War Browser** dan **AssetForge** yang membantu memahami struktur file dan alur kerja.

---

## Português (Brasil)

### O que é?
Uma ferramenta de PC que edita **somente texturas** dentro dos arquivos WAD de God of War 1 e God of War 2 (PS2). Exporte uma textura como PNG, edite em qualquer editor de imagem / pixel art, coloque de volta e salve. O tamanho do WAD nunca muda, e nada mais dentro do WAD é tocado.

O app tem seu próprio seletor de idioma: **Bahasa Indonesia, English, Português (Brasil)**.

### Recursos
- Abra uma **ISO de GoW 1 / GoW 2** (PART1.PAK / PART2.PAK → lista de WADs via `GODOFWAR.TOC`), um único **WAD** ou uma **pasta de WADs**.
- Só os WADs aparecem; **VPK, VAG, PSS/PSW** e outros arquivos ficam ocultos.
- Lista de texturas com pesquisa e **pré-visualização**.
- **Exportar PNG** / **Substituir por PNG** (com transparência).
- Texturas PS2 de 8 bits (256 cores) e 4 bits (16 cores), com conversão automática de paleta.
- **SALVAR** direto na ISO (todas as cópias do WAD, com backup `.texbak`) + **Restaurar ISO**; para WADs avulsos fica uma cópia `.bak`. Também há **Salvar como**.

### Cobertura (dos WADs varridos pelo autor)
| Jogo | WADs | Texturas vinculadas | Editáveis |
|------|-----:|--------------------:|----------:|
| GoW 1 | 216 | 6.623 | 6.591 |
| GoW 2 | 292 | 8.427 | 8.327 |

As demais usam outros formatos de cor ou tamanhos fora do padrão e aparecem como *não suportado*. WADs nunca varridos não podem ser garantidos.

### Download
- **Artifact do Actions:** aba *Actions* → última execução → artifact **Texture Editor**.
- **Releases:** faça push de uma tag como `v1.0` e o workflow publica `Texture Editor.zip`.

O pacote contém os arquivos de leia-me / informações em 3 idiomas e a pasta **`Texture Editor`** (`Texture_Editor.exe` + DLLs).
> ⚠️ Mantenha a pasta `Texture Editor` **inteira** junta; não mova só o `.exe`.

### Como usar
1. Execute `Texture_Editor.exe` (na primeira vez ele pede o idioma).
2. **Abrir ISO / Abrir WAD / Abrir pasta de WADs**.
3. Clique em um WAD na árvore **Fonte** e depois em uma textura da lista.
4. **Exportar PNG** → edite (mantenha o mesmo tamanho) → **Substituir por PNG**.
5. **SALVAR**.

### Notas importantes
- **ISO / PAK:** clique no `>` ao lado de `PART1.PAK` / `PART2.PAK` para listar os WADs. Ao salvar, o WAD é gravado no mesmo lugar em **todas** as cópias, depois de conferir o marcador do WAD, e os bytes originais ficam em `NOME.iso.texbak` (botão **Restaurar ISO**). Trabalhe em uma **cópia** da ISO.
- **Cores:** no máximo 256 (8 bits) ou 16 (4 bits) cores por textura. Texturas com paleta compartilhada ou paleta dupla mantêm a **paleta original** (sua imagem é mapeada para ela) para nada quebrar.
- **O tamanho da imagem** deve ser igual ao original (a ferramenta pode redimensionar com *nearest*).
- **Ainda não testado em uma ISO real / no jogo.** Testes automáticos: 14.918 texturas lidas → gravadas de volta **idênticas byte a byte**; PNG de ida e volta sem diferenças; o leitor de ISO/TOC foi verificado em ISOs simuladas feitas com os `GODOFWAR.TOC` reais de GoW 1 / GoW 2 e WADs reais.

### Fora do escopo
Qualquer coisa além de texturas dentro de um WAD (modelos 3D, áudio, texto), arquivos VPK/VAG/PSS/PSW avulsos, arquivos `PART*.PAK` soltos fora de uma ISO e reconstruir ISOs.

### Executar a partir do código / build
```bash
python gow_texture_tool.py          # Python 3.8+, sem bibliotecas extras
```
Build para Windows: execute `build.bat`, ou deixe o **GitHub Actions** (`.github/workflows/build.yml`) gerar o `Texture Editor.zip` (build em pasta, Python 3.10, funciona no Wine/Winlator).

### Reportar bugs
O app grava os erros em `texture_tool_error.txt` (ao lado do exe) e mostra o local na janela de erro. Envie esse texto junto com os nomes do WAD e da textura abertos.

### Aviso legal
Não inclui arquivos do jogo. Use somente com a sua própria cópia do jogo. Projeto de fã, sem vínculo com a Sony ou a Santa Monica Studio. *God of War* é marca registrada de seus donos. Fornecido como está, sem garantia.

### Créditos
Feito por **Nicho**. Obrigado ao projeto **God of War Browser** e ao **AssetForge**, que ajudaram a entender a estrutura dos arquivos e o fluxo de trabalho.
