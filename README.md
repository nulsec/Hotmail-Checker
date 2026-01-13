<div align="center">

# 📧 Hotmail Checker & Validator

![Python](https://img.shields.io/badge/Python-3.6+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-blue?style=for-the-badge)
![Microsoft](https://img.shields.io/badge/Microsoft-API-0078D4?style=for-the-badge&logo=microsoft&logoColor=white)

**🔍 Tool powerful untuk memvalidasi email Hotmail/Outlook/Live langsung ke server Microsoft**

[Fitur](#-fitur) •
[Instalasi](#-instalasi) •
[Penggunaan](#-penggunaan) •
[Dokumentasi](#-metode-pengecekan)

---

</div>

## ⚡ Quick Start

```bash
# Clone repository
git clone https://github.com/nulsec/Hotmail-Checker.git
cd Hotmail-Checker

# Cek single email
python hotmail_checker.py email@hotmail.com

# Bulk checking
python hotmail_checker.py -f emails.txt
```

---

## ✨ Fitur

<table>
<tr>
<td>

### 🎯 Core Features
- ✅ Validasi format email
- ✅ **Pengecekan terdaftar di Microsoft** 
- ✅ Pengecekan SMTP server
- ✅ Single & Bulk checking

</td>
<td>

### 🌐 Supported Domains
- 📬 hotmail.com
- 📬 outlook.com  
- 📬 live.com
- 📬 msn.com
- 📬 outlook.sg, dll

</td>
<td>

### 🛡️ Advanced
- 🔄 Retry mechanism
- ⏱️ Configurable timeout
- 💾 Export ke JSON
- 🚦 Rate limiting protection

</td>
</tr>
</table>

---

## 📦 Instalasi

> **Note:** Script ini menggunakan library standar Python saja!

### Persyaratan
| Requirement | Version |
|------------|---------|
| Python | 3.6+ |
| OS | Windows / Linux / macOS |

```bash
# Clone repo
git clone https://github.com/nulsec/Hotmail-Checker.git
cd Hotmail-Checker

# Siap digunakan! 🎉
```

---

## 🚀 Penggunaan

### 📝 Single Email Check

```bash
python hotmail_checker.py email@hotmail.com
```

### 📋 Bulk Checking

Buat file `emails.txt`:
```
user1@hotmail.com
user2@outlook.com
user3@live.com
```

Jalankan:
```bash
python hotmail_checker.py -f emails.txt
```

### 🎛️ Opsi Lanjutan

```bash
# 🏆 Metode Microsoft (REKOMENDASI)
python hotmail_checker.py -f emails.txt -o results.json --method microsoft

# ⏱️ Custom timeout & delay
python hotmail_checker.py -f emails.txt --timeout 15 --delay 2

# 🚀 Metode cepat (format only)
python hotmail_checker.py email@hotmail.com --method format

# 📡 Metode SMTP
python hotmail_checker.py email@hotmail.com --method smtp

# 🚫 Tanpa menyimpan hasil
python hotmail_checker.py -f emails.txt --no-save
```

---

## 📖 Command Line Options

| Option | Deskripsi | Default |
|--------|-----------|---------|
| `email` | Email untuk single check | - |
| `-f, --file` | File list email | - |
| `-o, --output` | Output file (JSON) | Auto-generated |
| `-m, --method` | Metode: `microsoft`, `smtp`, `vrfy`, `format` | `microsoft` |
| `-t, --timeout` | Timeout (detik) | `10` |
| `-d, --delay` | Delay antar cek (detik) | `1.0` |
| `-r, --retry` | Jumlah retry | `2` |
| `--no-save` | Tidak menyimpan hasil | `False` |

---

## 🔬 Metode Pengecekan

### 1️⃣ Microsoft (Default - ⭐ REKOMENDASI)

> Menggunakan API `login.microsoftonline.com` - **Paling Akurat!**

```bash
python hotmail_checker.py email@hotmail.com --method microsoft
```

| Kelebihan | Kekurangan |
|-----------|------------|
| ✅ Sangat akurat | ⚠️ Perlu delay 2 detik |
| ✅ Semua domain Microsoft | ⚠️ Rate limiting |
| ✅ Deteksi email terdaftar | |

### 2️⃣ Format (Tercepat ⚡)

```bash
python hotmail_checker.py email@hotmail.com --method format
```

> Hanya validasi format & domain. **Tidak perlu internet!**

### 3️⃣ SMTP

```bash
python hotmail_checker.py email@hotmail.com --method smtp
```

> Pengecekan via SMTP server. Akurat tapi mungkin timeout.

### 4️⃣ VRFY

```bash
python hotmail_checker.py email@hotmail.com --method vrfy
```

> Menggunakan VRFY command (biasanya dinonaktifkan).

---

## 📊 Format Output

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

---

## 🖥️ Contoh Output

### Single Check
```
Mengecek email: test@hotmail.com

📧 Email  : test@hotmail.com
🌐 Domain : hotmail.com
✅ Status : VALID
💬 Pesan  : Email valid dan aktif
```

### Bulk Check
```
🚀 Memulai pengecekan 3 email...

[1/3] Mengecek: user1@hotmail.com... ✅ VALID
[2/3] Mengecek: user2@outlook.com... ❌ INVALID  
[3/3] Mengecek: user3@live.com... ✅ VALID

══════════════════════════════════════════════════
📊 RINGKASAN HASIL
══════════════════════════════════════════════════
📬 Total email  : 3
✅ Valid        : 2 (66.7%)
❌ Invalid      : 1 (33.3%)
══════════════════════════════════════════════════

💾 Hasil disimpan ke: results_20240101_120000.json
```

---

## ⚠️ Catatan Penting

> **🔴 Legal Disclaimer:** Pastikan Anda memiliki izin untuk mengecek email. Jangan gunakan untuk spam atau aktivitas ilegal!

| ⚡ Tips | Deskripsi |
|--------|-----------|
| 🕐 Rate Limiting | Gunakan delay minimal **2 detik** untuk metode microsoft |
| 🌐 Network | Memerlukan koneksi internet stabil (kecuali metode format) |
| 🎯 Akurasi | Metode `microsoft` paling akurat untuk semua domain Microsoft |

---

## 📜 License

```
MIT License - Script ini disediakan "as is" untuk keperluan edukasi dan validasi yang legal.
```

---

<div align="center">

**Made with ❤️ by [nulsec](https://github.com/nulsec)**

⭐ Star repo ini jika bermanfaat!

</div>
