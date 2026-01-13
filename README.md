<div align="center">

# 📧 Hotmail Checker & Validator

![Python](https://img.shields.io/badge/Python-3.6+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-blue?style=for-the-badge)
![Microsoft](https://img.shields.io/badge/Microsoft-API-0078D4?style=for-the-badge&logo=microsoft&logoColor=white)

**🔍 Powerful tool to validate Hotmail/Outlook/Live emails directly to Microsoft servers**

[Features](#-features) •
[Installation](#-installation) •
[Usage](#-usage) •
[Documentation](#-checking-methods)

---

</div>

## ⚡ Quick Start

```bash
# Clone repository
git clone https://github.com/nulsec/Hotmail-Checker.git
cd Hotmail-Checker

# Check single email
python hotmail_checker.py email@hotmail.com

# Bulk checking
python hotmail_checker.py -f emails.txt
```

---

## ✨ Features

<table>
<tr>
<td>

### 🎯 Core Features
- ✅ Email format validation
- ✅ **Check if registered with Microsoft** 
- ✅ SMTP server checking
- ✅ Single & Bulk checking

</td>
<td>

### 🌐 Supported Domains
- 📬 hotmail.com
- 📬 outlook.com  
- 📬 live.com
- 📬 msn.com
- 📬 outlook.sg, etc.

</td>
<td>

### 🛡️ Advanced
- 🔄 Retry mechanism
- ⏱️ Configurable timeout
- 💾 Export to JSON
- 🚦 Rate limiting protection

</td>
</tr>
</table>

---

## 📦 Installation

> **Note:** This script uses only standard Python libraries!

### Requirements
| Requirement | Version |
|------------|---------|
| Python | 3.6+ |
| OS | Windows / Linux / macOS |

```bash
# Clone repo
git clone https://github.com/nulsec/Hotmail-Checker.git
cd Hotmail-Checker

# Ready to use! 🎉
```

---

## 🚀 Usage

### 📝 Single Email Check

```bash
python hotmail_checker.py email@hotmail.com
```

### 📋 Bulk Checking

Create `emails.txt` file:
```
user1@hotmail.com
user2@outlook.com
user3@live.com
```

Run:
```bash
python hotmail_checker.py -f emails.txt
```

### 🎛️ Advanced Options

```bash
# 🏆 Microsoft Method (RECOMMENDED)
python hotmail_checker.py -f emails.txt -o results.json --method microsoft

# ⏱️ Custom timeout & delay
python hotmail_checker.py -f emails.txt --timeout 15 --delay 2

# 🚀 Fast method (format only)
python hotmail_checker.py email@hotmail.com --method format

# 📡 SMTP Method
python hotmail_checker.py email@hotmail.com --method smtp

# 🚫 Without saving results
python hotmail_checker.py -f emails.txt --no-save
```

---

## 📖 Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `email` | Email for single check | - |
| `-f, --file` | Email list file | - |
| `-o, --output` | Output file (JSON) | Auto-generated |
| `-m, --method` | Method: `microsoft`, `smtp`, `vrfy`, `format` | `microsoft` |
| `-t, --timeout` | Timeout (seconds) | `10` |
| `-d, --delay` | Delay between checks (seconds) | `1.0` |
| `-r, --retry` | Number of retries | `2` |
| `--no-save` | Don't save results | `False` |

---

## 🔬 Checking Methods

### 1️⃣ Microsoft (Default - ⭐ RECOMMENDED)

> Using `login.microsoftonline.com` API - **Most Accurate!**

```bash
python hotmail_checker.py email@hotmail.com --method microsoft
```

| Advantages | Disadvantages |
|-----------|------------|
| ✅ Very accurate | ⚠️ Requires 2 second delay |
| ✅ All Microsoft domains | ⚠️ Rate limiting |
| ✅ Detects registered emails | |

### 2️⃣ Format (Fastest ⚡)

```bash
python hotmail_checker.py email@hotmail.com --method format
```

> Only format & domain validation. **No internet needed!**

### 3️⃣ SMTP

```bash
python hotmail_checker.py email@hotmail.com --method smtp
```

> Checking via SMTP server. Accurate but may timeout.

### 4️⃣ VRFY

```bash
python hotmail_checker.py email@hotmail.com --method vrfy
```

> Uses VRFY command (usually disabled).

---

## 📊 Output Format

```json
[
  {
    "email": "user@hotmail.com",
    "timestamp": "2024-01-01T12:00:00",
    "valid": true,
    "message": "Email registered with Microsoft",
    "domain": "hotmail.com",
    "method": "microsoft"
  }
]
```

---

## 🖥️ Output Examples

### Single Check
```
Checking email: test@hotmail.com

📧 Email  : test@hotmail.com
🌐 Domain : hotmail.com
✅ Status : VALID
💬 Message: Email is valid and active
```

### Bulk Check
```
🚀 Starting to check 3 emails...

[1/3] Checking: user1@hotmail.com... ✅ VALID
[2/3] Checking: user2@outlook.com... ❌ INVALID  
[3/3] Checking: user3@live.com... ✅ VALID

══════════════════════════════════════════════════
📊 RESULTS SUMMARY
══════════════════════════════════════════════════
📬 Total emails : 3
✅ Valid       : 2 (66.7%)
❌ Invalid     : 1 (33.3%)
══════════════════════════════════════════════════

💾 Results saved to: results_20240101_120000.json
```

---

## ⚠️ Important Notes

> **🔴 Legal Disclaimer:** Make sure you have permission to check emails. Do not use for spam or illegal activities!

| ⚡ Tips | Description |
|--------|-----------|
| 🕐 Rate Limiting | Use minimum **2 second** delay for microsoft method |
| 🌐 Network | Requires stable internet connection (except format method) |
| 🎯 Accuracy | `microsoft` method is most accurate for all Microsoft domains |

---

## 📜 License

```
MIT License - This script is provided "as is" for educational and legal validation purposes.
```

---

<div align="center">

**Made with ❤️ by [nulsec](https://github.com/nulsec)**

⭐ Star this repo if it's helpful!

</div>
