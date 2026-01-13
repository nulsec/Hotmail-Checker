HOTMAIL CHECKER - VERSI RINGAN
================================

Script Python untuk mengecek email terdaftar di Microsoft

CARA MENGGUNAKAN:
-----------------

1. Cek email dari file:
   python hotmail_checker_clean.txt -f test_emails.txt -o hasil.json --delay 2

2. Cek single email:
   python hotmail_checker_clean.txt email@hotmail.com

3. Pisahkan hasil menjadi 2 file (valid & invalid):
   python extract_leads_clean.txt hasil.json --split

OPSI:
-----
-f, --file      File berisi list email (satu per baris)
-o, --output    File output JSON
-d, --delay     Delay antar pengecekan (detik, default: 1.0)
-t, --timeout   Timeout koneksi (detik, default: 10)
-r, --retry     Jumlah retry jika timeout (default: 2)
-v, --verbose   Tampilkan detail koneksi
--no-save       Jangan simpan hasil ke file

CONTOH WORKFLOW:
----------------
1. python hotmail_checker_clean.txt -f emails.txt -o hasil.json --delay 2
2. python extract_leads_clean.txt hasil.json --split
   
   Hasil:
   - valid_emails.txt (email terdaftar)
   - invalid_emails.txt (email tidak terdaftar)

CATATAN:
--------
- Gunakan delay minimal 2 detik untuk menghindari rate limiting
- Script mengecek langsung ke Microsoft API
- Hanya support domain Microsoft (hotmail.com, outlook.com, live.com, msn.com, dll)
