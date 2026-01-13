# Hotmail Checker & Validator

Script Python untuk mengecek dan memvalidasi email Hotmail/Outlook/Live secara langsung ke server Microsoft.

## Fitur

- ✅ Validasi format email
- ✅ **Pengecekan terdaftar di Microsoft** menggunakan login.microsoftonline.com (REKOMENDASI)
- ✅ Pengecekan langsung ke SMTP server Microsoft
- ✅ Support untuk semua domain Microsoft: hotmail.com, outlook.com, live.com, msn.com, outlook.sg, dll
- ✅ Single email checking
- ✅ Bulk email checking dari file
- ✅ Export hasil ke JSON
- ✅ Delay antar pengecekan untuk menghindari rate limiting
- ✅ Retry mechanism untuk handling timeout
- ✅ Timeout yang dapat dikonfigurasi

## Instalasi

Script ini menggunakan library standar Python saja, tidak memerlukan instalasi package tambahan.

**Persyaratan:**
- Python 3.6 atau lebih baru

## Penggunaan

### Single Email Checking

```bash
python hotmail_checker.py email@hotmail.com
```

### Bulk Checking dari File

Buat file `emails.txt` dengan format satu email per baris:
```
user1@hotmail.com
user2@outlook.com
user3@live.com
```

Kemudian jalankan:
```bash
python hotmail_checker.py -f emails.txt
```

### Opsi Lainnya

```bash
# Metode Microsoft (REKOMENDASI - cek terdaftar di Microsoft)
python hotmail_checker.py -f emails.txt -o results.json --method microsoft

# Simpan hasil ke file tertentu
python hotmail_checker.py -f emails.txt -o results.json

# Set timeout dan delay
python hotmail_checker.py -f emails.txt --timeout 15 --delay 2

# Gunakan metode format (cepat, hanya validasi format & domain)
python hotmail_checker.py email@hotmail.com --method format

# Gunakan metode SMTP (lebih akurat tapi mungkin timeout)
python hotmail_checker.py email@hotmail.com --method smtp

# Jangan simpan hasil ke file
python hotmail_checker.py -f emails.txt --no-save
```

## Opsi Command Line

- `email` - Alamat email yang akan dicek (untuk single check)
- `-f, --file` - File berisi list email (satu per baris)
- `-o, --output` - File output untuk menyimpan hasil (JSON)
- `-m, --method` - Metode pengecekan: `microsoft` (cek terdaftar), `smtp` (SMTP verification), `vrfy` (VRFY command), `format` (format & domain only) (default: microsoft)
- `-t, --timeout` - Timeout koneksi dalam detik (default: 10)
- `-d, --delay` - Delay antar pengecekan dalam detik (default: 1.0)
- `-r, --retry` - Jumlah retry jika timeout (default: 2)
- `--no-save` - Jangan simpan hasil ke file

## Metode Pengecekan

### 1. Microsoft (Default - REKOMENDASI)
Mengecek apakah email terdaftar di Microsoft menggunakan API login.microsoftonline.com. Metode ini paling akurat dan dapat mendeteksi semua domain Microsoft termasuk outlook.sg, outlook.co.id, dll.

```bash
python hotmail_checker.py email@hotmail.com --method microsoft
```

### 2. Format
Hanya validasi format email dan domain Microsoft. Sangat cepat, tidak perlu koneksi internet.

```bash
python hotmail_checker.py email@hotmail.com --method format
```

### 3. SMTP
Pengecekan menggunakan SMTP server. Lebih akurat tapi mungkin timeout karena server membatasi akses.

```bash
python hotmail_checker.py email@hotmail.com --method smtp
```

### 4. VRFY
Menggunakan VRFY command (biasanya dinonaktifkan untuk keamanan).

```bash
python hotmail_checker.py email@hotmail.com --method vrfy
```

## Format Output

Hasil pengecekan disimpan dalam format JSON:

```json
[
  {
    "email": "user@hotmail.com",
    "timestamp": "2024-01-01T12:00:00",
    "valid": true,
    "message": "Email terdaftar di Microsoft",
    "domain": "hotmail.com",
    "method": "microsoft"
  }
]
```

## Catatan Penting

1. **Metode Microsoft**: Metode `microsoft` adalah yang paling direkomendasikan karena dapat mengecek apakah email benar-benar terdaftar di Microsoft dengan akurat. Gunakan delay minimal 2 detik untuk menghindari rate limiting.

2. **Rate Limiting**: Microsoft mungkin membatasi jumlah request. Gunakan delay yang cukup antar pengecekan (minimal 2 detik untuk metode microsoft).

3. **Akurasi**: 
   - Metode `microsoft`: Sangat akurat, dapat mendeteksi semua domain Microsoft
   - Metode `smtp`: Akurat tapi mungkin timeout karena server membatasi akses
   - Metode `format`: Hanya validasi format dan domain, tidak mengecek apakah email benar-benar terdaftar

4. **Legal**: Pastikan Anda memiliki izin untuk mengecek email yang akan divalidasi. Jangan gunakan untuk spam atau aktivitas ilegal.

5. **Network**: Script memerlukan koneksi internet yang stabil untuk menghubungi server Microsoft (kecuali metode `format`).

## Contoh Output

```
Mengecek email: test@hotmail.com

Email: test@hotmail.com
Domain: hotmail.com
Status: ✓ VALID
Pesan: Email valid dan aktif
```

Untuk bulk checking:
```
Memulai pengecekan 3 email...

[1/3] Mengecek: user1@hotmail.com... ✓ VALID - Email valid dan aktif
[2/3] Mengecek: user2@outlook.com... ✗ INVALID - Email tidak valid atau tidak ada
[3/3] Mengecek: user3@live.com... ✓ VALID - Email valid dan aktif

==================================================
RINGKASAN HASIL
==================================================
Total email dicek: 3
Valid: 2 (66.7%)
Invalid: 1 (33.3%)
==================================================

Hasil disimpan ke: results_20240101_120000.json
```

## License

Script ini disediakan "as is" untuk keperluan edukasi dan validasi yang legal.
