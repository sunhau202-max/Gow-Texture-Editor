========================================================================
 GOW TEXTURE EDITOR (Gow Language Editor by Nicho)  -  v1.0
 Editor tekstur untuk file WAD God of War 1 & 2 (PS2)
========================================================================

ISI PAKET
  Readme-Indo.txt        : petunjuk ini (Bahasa Indonesia)
  Informasi-Indo.txt     : apa yang bisa dan tidak bisa dilakukan tool ini
  Readme-Eng.txt / Information-Eng.txt      : versi English
  Leia-me-Br.txt / Informacoes-Br.txt       : versi Português (Brasil)
  Texture Editor\        : folder programnya (Texture_Editor.exe + file pendukung)

PENTING: jangan memindahkan Texture_Editor.exe saja ke tempat lain. Exe ini butuh
DLL dan file lain di sebelahnya. Bawa dan simpan SELURUH folder "Texture Editor".

APA ITU?
Tool PC (Windows dan Wine/Winlator) untuk mengganti TEKSTUR di dalam file WAD
God of War 1 dan God of War 2 (PS2). Hanya tekstur: tool ini tidak mengubah file
lain di dalam WAD, dan tidak mengubah ukuran WAD.

CARA PAKAI
  1. Jalankan Texture_Editor.exe. Saat pertama dibuka kamu memilih bahasa
     (Indonesia / English / Português); bisa diganti kapan saja di jendela utama.
  2. Buka sumbernya:
       Buka ISO         : membaca ISO God of War; klik > di PART1.PAK / PART2.PAK untuk melihat WAD.
       Buka WAD         : membuka satu file .WAD.
       Buka folder WAD  : menampilkan semua .WAD di sebuah folder.
     File lain (VPK, VAG, PSS/PSW, dan sebagainya) disembunyikan.
  3. Klik sebuah WAD di pohon "Sumber" (kiri). Daftar tekstur muncul di kanan.
     Ketik di kolom "Cari tekstur" untuk menyaring. Pilih satu tekstur untuk melihat
     pratinjaunya.
  4. "Export PNG" menyimpan tekstur sebagai gambar PNG. Edit PNG itu di aplikasi
     gambar / pixel art favoritmu (jangan ubah ukurannya).
  5. "Replace dari PNG" memasukkan PNG hasil editanmu ke tekstur itu.
  6. Klik SIMPAN. Hasil ditulis ke WAD aslinya dan salinan WAD asli disimpan sekali
     sebagai NAMA.WAD.bak. "Simpan sebagai" menyimpan ke file lain.

ISO DAN PAK
  Buka ISO membaca ISO God of War 1 atau 2 lalu menampilkan PART1.PAK dan PART2.PAK. Klik
  tanda > di sebelahnya untuk melihat daftar WAD di dalamnya (dibaca lewat GODOFWAR.TOC di
  ISO; file VPK, VAG, PSS/PSW tidak ditampilkan). Pilih WAD, edit teksturnya, lalu SIMPAN:
  WAD hasil edit ditulis langsung ke ISO, ke SEMUA lokasi salinannya (GoW 2 menyimpan sebagian
  WAD di lebih dari satu tempat). Karena ukuran WAD tidak berubah, tidak ada yang bergeser.
  Sebelum menulis, tool memeriksa penanda WAD di tiap lokasi dan menyimpan isi aslinya ke
  NAMA.iso.texbak. Tombol "Kembalikan ISO" memulihkan semuanya dari backup itu.
  PENTING: kerjakan di SALINAN ISO, dan tutup program lain yang sedang memakai ISO itu.

TENTANG GAMBAR
  - Ukuran PNG harus sama dengan tekstur aslinya. Kalau beda, tool menawarkan
    menyesuaikan otomatis (nearest, cocok untuk pixel art).
  - Tekstur PS2 memakai palet: maksimal 256 warna (tekstur 8-bit) atau 16 warna
    (tekstur 4-bit). Tool mengubah warna PNG-mu ke palet otomatis. Gambar pixel art
    dengan sedikit warna hasilnya persis; gambar penuh warna dikurangi warnanya.
  - Tekstur yang palet-nya dipakai bersama tekstur lain, atau yang punya palet ganda,
    ditandai "palet asli dipertahankan": warna gambarmu dipetakan ke warna palet
    aslinya supaya tekstur lain / palet kedua tidak rusak.
  - Transparansi PNG didukung (alpha PS2 berskala 0 sampai 128).

TIPS UNTUK PEMULA
  - Selalu kerja di SALINAN. Simpan ISO / PAK aslimu.
  - Ubah satu tekstur per percobaan, lalu tes di game.
  - Jangan ubah ukuran gambar dan jangan menambah banyak warna kalau tidak perlu.

JIKA ADA ERROR / BUG
Tool mencatat error ke texture_tool_error.txt (di samping exe) dan menampilkan
lokasinya di jendela error. Kirim teks error (atau fotonya) beserta nama WAD dan
tekstur yang kamu buka ke pembuat tool.

WINLATOR / WINE
Pakai versi folder ini (bukan exe satu file). Kalau dialog file bermasalah, pindahkan
WAD ke folder yang mudah dijangkau lalu pakai Buka folder WAD.

========================================================================
 Gow Language Editor by Nicho
========================================================================
