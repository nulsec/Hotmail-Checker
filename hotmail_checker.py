#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hotmail Checker & Validator
Script untuk mengecek dan memvalidasi email Hotmail/Outlook/Live
"""

import smtplib
import socket
import re
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
from email.utils import parseaddr
from typing import Tuple, Optional
import argparse
import json
from datetime import datetime

class HotmailChecker:
    """Class untuk mengecek validitas email Hotmail"""
    
    # SMTP servers untuk Microsoft email services
    SMTP_SERVERS = {
        'hotmail.com': ('smtp-mail.outlook.com', 587),
        'outlook.com': ('smtp-mail.outlook.com', 587),
        'live.com': ('smtp-mail.outlook.com', 587),
        'msn.com': ('smtp-mail.outlook.com', 587),
    }
    
    # MX records untuk Microsoft domains
    MX_RECORDS = {
        'hotmail.com': 'mx4.hotmail.com',
        'outlook.com': 'mx4.hotmail.com',
        'live.com': 'mx4.hotmail.com',
        'msn.com': 'mx4.hotmail.com',
    }
    
    def __init__(self, timeout: int = 10, delay: float = 1.0, retry: int = 2, verbose: bool = False):
        """
        Initialize HotmailChecker
        
        Args:
            timeout: Timeout untuk koneksi (detik)
            delay: Delay antar pengecekan (detik)
            retry: Jumlah retry jika gagal (default: 2)
            verbose: Tampilkan detail koneksi ke Microsoft (default: False)
        """
        self.timeout = timeout
        self.delay = delay
        self.retry = retry
        self.verbose = verbose
    
    def is_valid_email_format(self, email: str) -> bool:
        """
        Validasi format email
        
        Args:
            email: Alamat email yang akan divalidasi
            
        Returns:
            True jika format valid, False jika tidak
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def extract_domain(self, email: str) -> Optional[str]:
        """
        Ekstrak domain dari email
        
        Args:
            email: Alamat email
            
        Returns:
            Domain atau None jika tidak valid
        """
        if not self.is_valid_email_format(email):
            return None
        
        _, addr = parseaddr(email)
        if '@' in addr:
            domain = addr.split('@')[1].lower()
            return domain
        return None
    
    def is_microsoft_domain(self, domain: str) -> bool:
        """
        Cek apakah domain adalah Microsoft email domain
        
        Args:
            domain: Domain yang akan dicek
            
        Returns:
            True jika domain Microsoft, False jika tidak
        """
        microsoft_domains = ['hotmail.com', 'outlook.com', 'live.com', 'msn.com']
        return domain in microsoft_domains
    
    def check_email_format_only(self, email: str) -> Tuple[bool, str]:
        """
        Cek email hanya berdasarkan format dan domain (cepat, tidak perlu koneksi)
        
        Args:
            email: Alamat email yang akan dicek
            
        Returns:
            Tuple (is_valid, message)
        """
        if not self.is_valid_email_format(email):
            return False, "Format email tidak valid"
        
        domain = self.extract_domain(email)
        if not domain:
            return False, "Tidak dapat mengekstrak domain"
        
        if not self.is_microsoft_domain(domain):
            return False, f"Domain {domain} bukan domain Microsoft (Hotmail/Outlook/Live)"
        
        return True, "Format dan domain valid (Microsoft domain terdeteksi)"
    
    def check_email_microsoft(self, email: str) -> Tuple[bool, str]:
        """
        Cek apakah email terdaftar di Microsoft menggunakan login.microsoftonline.com
        
        Args:
            email: Alamat email yang akan dicek
            
        Returns:
            Tuple (is_registered, message)
        """
        # STEP 1: Validasi format email
        if not self.is_valid_email_format(email):
            return False, "Format email tidak valid"
        
        # STEP 2: Validasi domain Microsoft
        domain = self.extract_domain(email)
        if not domain:
            return False, "Tidak dapat mengekstrak domain"
        
        # Cek apakah domain adalah domain Microsoft yang didukung
        # Support domain Microsoft: hotmail.com, outlook.com, live.com, msn.com
        # Dan juga custom domain Microsoft seperti outlook.sg, outlook.co.id, dll
        # Untuk custom domain, kita perlu cek ke Microsoft API
        
        # Untuk domain Microsoft standar, validasi dulu
        is_ms_standard_domain = self.is_microsoft_domain(domain)
        
        # Jika bukan domain Microsoft standar, cek apakah mungkin custom domain Microsoft
        # (kita akan cek ke API Microsoft untuk memastikan)
        
        try:
            # Endpoint Microsoft untuk mengecek credential type
            url = "https://login.microsoftonline.com/common/GetCredentialType"
            
            if self.verbose:
                print(f"  [DEBUG] Menghubungi Microsoft: {url}")
                print(f"  [DEBUG] Mengecek email: {email}")
            
            # Data yang dikirim sesuai format Microsoft
            data = {
                "Username": email,
                "isOtherIdpSupported": True,
                "checkPhones": False,
                "isRemoteNGCSupported": True,
                "isCookieBannerShown": False,
                "isFidoSupported": False,
                "originalRequest": "",
                "country": "ID",
                "forceotclogin": False,
                "isExternalFederationDisallowed": False,
                "isRemoteConnectSupported": False,
                "federationFlags": 0,
                "isSignup": False,
                "flowToken": "",
                "isAccessPassSupported": False
            }
            
            # Encode data
            data_encoded = json.dumps(data).encode('utf-8')
            
            # Buat request dengan headers yang tepat
            req = urllib.request.Request(
                url,
                data=data_encoded,
                headers={
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Origin': 'https://login.microsoftonline.com',
                    'Referer': 'https://login.microsoftonline.com/'
                }
            )
            
            # Kirim request dengan timeout
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as response:
                    if self.verbose:
                        print(f"  [DEBUG] Response status: {response.getcode()}")
                    response_text = response.read().decode('utf-8')
                    response_data = json.loads(response_text)
                    
                    if self.verbose:
                        print(f"  [DEBUG] Response data: {json.dumps(response_data, indent=2)[:200]}...")
                    
                    # Cek hasil response - IfExistsResult adalah kunci utama
                    # Interpretasi yang benar:
                    # 0 = Account does not exist (email tidak terdaftar)
                    # 1 = Account exists but is federated (bukan Microsoft account) 
                    #     UNTUK DOMAIN MICROSOFT: status 1 berarti email TIDAK TERDAFTAR
                    # 2 = Account exists and is Microsoft account (managed)
                    # 5 = Account exists and is Microsoft account (custom domain seperti outlook.sg)
                    
                    if 'IfExistsResult' in response_data:
                        exists_result = response_data['IfExistsResult']
                        
                        if self.verbose:
                            print(f"  [DEBUG] IfExistsResult: {exists_result}")
                            print(f"  [DEBUG] Domain: {domain}, Is MS Standard Domain: {is_ms_standard_domain}")
                            if 'Credentials' in response_data:
                                print(f"  [DEBUG] Credentials: {json.dumps(response_data['Credentials'], indent=2)}")
                        
                        # Status 0: Email tidak terdaftar
                        if exists_result == 0:
                            return False, "Email tidak terdaftar di Microsoft"
                        
                        # Status 1: Untuk domain Microsoft standar = TIDAK TERDAFTAR
                        # Status 1 berarti account tidak ada atau federated
                        # Domain Microsoft standar tidak bisa federated, jadi status 1 = tidak terdaftar
                        elif exists_result == 1:
                            if is_ms_standard_domain:
                                # Domain Microsoft standar dengan status 1 = tidak terdaftar
                                # (Microsoft tidak mengizinkan federated untuk domain standar)
                                return False, "Email tidak terdaftar di Microsoft"
                            else:
                                # Domain non-Microsoft dengan status 1 = federated (bukan Microsoft account)
                                return False, "Email terdaftar tapi bukan Microsoft account (federated)"
                        
                        # Status 2: Email terdaftar di Microsoft (managed account)
                        elif exists_result == 2:
                            return True, "Email terdaftar di Microsoft"
                        
                        # Status 5: Bisa berarti terdaftar ATAU placeholder/test account
                        # Perlu cek lebih detail di Credentials untuk memastikan
                        elif exists_result == 5:
                            # Cek Credentials untuk memastikan email benar-benar terdaftar
                            if 'Credentials' in response_data:
                                creds = response_data['Credentials']
                                if creds:
                                    # Cek apakah ada password (indikasi akun aktif)
                                    has_password = creds.get('HasPassword', False)
                                    
                                    # Untuk domain Microsoft standar dengan status 5:
                                    # - Jika HasPassword = True: Email terdaftar dan aktif
                                    # - Jika HasPassword = False: Bisa jadi placeholder/test account (tidak terdaftar)
                                    if is_ms_standard_domain:
                                        if has_password:
                                            return True, "Email terdaftar di Microsoft"
                                        else:
                                            # Status 5 tanpa password untuk domain standar = tidak terdaftar (placeholder)
                                            return False, "Email tidak terdaftar di Microsoft"
                                    else:
                                        # Custom domain dengan status 5 = terdaftar (custom domain Microsoft)
                                        return True, "Email terdaftar di Microsoft (custom domain)"
                            
                            # Jika tidak ada Credentials detail:
                            # - Untuk domain standar dengan status 5 tanpa Credentials = tidak terdaftar
                            # - Untuk custom domain dengan status 5 = terdaftar
                            if is_ms_standard_domain:
                                return False, "Email tidak terdaftar di Microsoft (tidak ada credential)"
                            else:
                                return True, "Email terdaftar di Microsoft (custom domain)"
                        
                        # Status lainnya: cek Credentials sebagai fallback
                        else:
                            # Cek apakah ada Credentials yang menunjukkan email terdaftar
                            if 'Credentials' in response_data:
                                creds = response_data['Credentials']
                                # Jika ada PrefCredential atau HasPassword, berarti email terdaftar
                                if creds and (creds.get('PrefCredential') or creds.get('HasPassword')):
                                    return True, "Email terdaftar di Microsoft"
                            
                            # Jika tidak ada indikasi terdaftar, anggap tidak terdaftar
                            return False, f"Email tidak terdaftar (status: {exists_result})"
                    
                    # Alternatif: cek ThrottleStatus
                    if 'ThrottleStatus' in response_data:
                        throttle = response_data['ThrottleStatus']
                        if throttle == 1:
                            return False, "Rate limit - terlalu banyak request"
                    
                    # Cek apakah ada Credentials yang menunjukkan email terdaftar
                    if 'Credentials' in response_data:
                        creds = response_data['Credentials']
                        if creds and len(creds) > 0:
                            return True, "Email terdaftar di Microsoft"
                    
                    # Jika tidak ada indikasi email terdaftar
                    return False, "Email tidak terdaftar di Microsoft"
                    
            except urllib.error.HTTPError as e:
                error_body = ""
                try:
                    error_body = e.read().decode('utf-8')
                except:
                    pass
                
                if e.code == 400:
                    # Bad request - biasanya berarti format tidak valid atau tidak terdaftar
                    return False, "Email tidak terdaftar atau format tidak valid"
                elif e.code == 429:
                    return False, "Rate limit - terlalu banyak request, coba lagi nanti"
                elif e.code == 403:
                    return False, "Akses ditolak oleh server"
                else:
                    return False, f"HTTP Error {e.code}: {error_body[:100] if error_body else str(e)}"
            except urllib.error.URLError as e:
                if 'timeout' in str(e).lower() or isinstance(e.reason, socket.timeout):
                    return False, "Timeout - server tidak merespon"
                return False, f"URL Error: {str(e)}"
            except socket.timeout:
                return False, "Timeout - server tidak merespon"
            except json.JSONDecodeError as e:
                return False, f"Error parsing response: {str(e)}"
                
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def check_email_smtp(self, email: str) -> Tuple[bool, str]:
        """
        Cek email menggunakan SMTP verification
        
        Args:
            email: Alamat email yang akan dicek
            
        Returns:
            Tuple (is_valid, message)
        """
        if not self.is_valid_email_format(email):
            return False, "Format email tidak valid"
        
        domain = self.extract_domain(email)
        if not domain:
            return False, "Tidak dapat mengekstrak domain"
        
        if not self.is_microsoft_domain(domain):
            return False, f"Domain {domain} bukan domain Microsoft (Hotmail/Outlook/Live)"
        
        try:
            # Gunakan MX record untuk verifikasi
            mx_host = self.MX_RECORDS.get(domain, 'mx4.hotmail.com')
            
            # Connect ke SMTP server
            server = smtplib.SMTP(timeout=self.timeout)
            server.set_debuglevel(0)
            
            try:
                server.connect(mx_host, 25)
                server.helo(server.local_hostname)
                server.mail('test@example.com')
                
                # Cek apakah email ada
                code, message = server.rcpt(email)
                server.quit()
                
                # 250 = success, email valid
                if code == 250:
                    return True, "Email valid dan aktif"
                else:
                    return False, f"Email tidak valid atau tidak ada: {message.decode()}"
                    
            except smtplib.SMTPRecipientsRefused:
                server.quit()
                return False, "Email ditolak - tidak valid"
            except smtplib.SMTPServerDisconnected:
                return False, "Server memutus koneksi"
            except Exception as e:
                if hasattr(server, 'quit'):
                    try:
                        server.quit()
                    except:
                        pass
                return False, f"Error SMTP: {str(e)}"
                
        except socket.timeout:
            return False, "Timeout - server tidak merespon (server mungkin membatasi akses SMTP)"
        except socket.gaierror:
            return False, "Tidak dapat menghubungi server"
        except Exception as e:
            error_msg = str(e).lower()
            if 'timeout' in error_msg or 'timed out' in error_msg:
                return False, "Timeout - server tidak merespon (server mungkin membatasi akses SMTP)"
            return False, f"Error koneksi: {str(e)}"
    
    def check_email_vrfy(self, email: str) -> Tuple[bool, str]:
        """
        Cek email menggunakan VRFY command (alternatif)
        
        Args:
            email: Alamat email yang akan dicek
            
        Returns:
            Tuple (is_valid, message)
        """
        if not self.is_valid_email_format(email):
            return False, "Format email tidak valid"
        
        domain = self.extract_domain(email)
        if not domain or not self.is_microsoft_domain(domain):
            return False, "Domain tidak didukung"
        
        try:
            mx_host = self.MX_RECORDS.get(domain, 'mx4.hotmail.com')
            server = smtplib.SMTP(timeout=self.timeout)
            server.connect(mx_host, 25)
            server.helo(server.local_hostname)
            
            # VRFY command (biasanya dinonaktifkan untuk keamanan)
            code, message = server.verify(email)
            server.quit()
            
            if code == 250:
                return True, "Email valid"
            else:
                return False, f"Email tidak valid: {message.decode()}"
                
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def check_email(self, email: str, method: str = 'smtp') -> dict:
        """
        Cek email dengan metode yang dipilih
        
        Args:
            email: Alamat email yang akan dicek
            method: Metode pengecekan ('smtp', 'vrfy', atau 'format')
            
        Returns:
            Dictionary dengan hasil pengecekan
        """
        result = {
            'email': email,
            'timestamp': datetime.now().isoformat(),
            'valid': False,
            'message': '',
            'domain': None,
            'method': method
        }
        
        domain = self.extract_domain(email)
        result['domain'] = domain
        
        # Retry mechanism untuk metode SMTP dan Microsoft
        if method == 'smtp':
            valid, message = False, ""
            for attempt in range(self.retry):
                valid, message = self.check_email_smtp(email)
                if valid or 'timeout' not in message.lower():
                    break
                if attempt < self.retry - 1:
                    time.sleep(self.delay)
        elif method == 'microsoft':
            # Untuk metode Microsoft, validasi domain terlebih dahulu
            domain = self.extract_domain(email)
            if domain:
                # Cek apakah domain Microsoft standar atau mungkin custom domain Microsoft
                # Domain Microsoft standar: hotmail.com, outlook.com, live.com, msn.com
                # Custom domain Microsoft: outlook.sg, outlook.co.id, dll (perlu cek ke API)
                is_ms_standard = self.is_microsoft_domain(domain)
                
                # Jika bukan domain Microsoft standar, tetap cek ke API karena bisa jadi custom domain
                # Tapi kita bisa skip jika jelas bukan domain Microsoft (misalnya gmail.com)
                # Untuk sekarang, kita cek semua ke API Microsoft untuk akurasi maksimal
                pass
            
            valid, message = False, ""
            for attempt in range(self.retry):
                valid, message = self.check_email_microsoft(email)
                if valid or ('timeout' not in message.lower() and 'rate limit' not in message.lower()):
                    break
                if attempt < self.retry - 1:
                    time.sleep(self.delay * 2)  # Delay lebih lama untuk Microsoft API
        elif method == 'vrfy':
            valid, message = self.check_email_vrfy(email)
        elif method == 'format':
            valid, message = self.check_email_format_only(email)
        else:
            valid, message = False, f"Metode '{method}' tidak dikenal"
        
        result['valid'] = valid
        result['message'] = message
        
        return result
    
    def check_bulk(self, emails: list, method: str = 'smtp') -> list:
        """
        Cek banyak email sekaligus
        
        Args:
            emails: List alamat email
            method: Metode pengecekan
            
        Returns:
            List hasil pengecekan
        """
        results = []
        total = len(emails)
        
        print(f"\nMemulai pengecekan {total} email...\n")
        
        for idx, email in enumerate(emails, 1):
            print(f"[{idx}/{total}] Mengecek: {email}...", end=' ', flush=True)
            
            result = self.check_email(email.strip(), method)
            results.append(result)
            
            status = "[VALID]" if result['valid'] else "[INVALID]"
            print(f"{status} - {result['message']}")
            
            # Delay antar pengecekan untuk menghindari rate limiting
            if idx < total:
                time.sleep(self.delay)
        
        return results


def load_emails_from_file(filename: str) -> list:
    """Load email dari file (satu per baris)"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            emails = [line.strip() for line in f if line.strip()]
        return emails
    except FileNotFoundError:
        print(f"Error: File '{filename}' tidak ditemukan")
        sys.exit(1)
    except Exception as e:
        print(f"Error membaca file: {str(e)}")
        sys.exit(1)


def save_results(results: list, filename: str = None):
    """Simpan hasil ke file JSON"""
    if filename is None:
        filename = f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\nHasil disimpan ke: {filename}")
    except Exception as e:
        print(f"Error menyimpan hasil: {str(e)}")


def print_summary(results: list):
    """Print ringkasan hasil"""
    total = len(results)
    valid = sum(1 for r in results if r['valid'])
    invalid = total - valid
    
    print("\n" + "="*50)
    print("RINGKASAN HASIL")
    print("="*50)
    print(f"Total email dicek: {total}")
    print(f"Valid: {valid} ({valid/total*100:.1f}%)" if total > 0 else "Valid: 0")
    print(f"Invalid: {invalid} ({invalid/total*100:.1f}%)" if total > 0 else "Invalid: 0")
    print("="*50)


def main():
    parser = argparse.ArgumentParser(
        description='Hotmail Checker & Validator - Cek validitas email Hotmail/Outlook/Live',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Contoh penggunaan:
  python hotmail_checker.py email@hotmail.com
  python hotmail_checker.py -f emails.txt
  python hotmail_checker.py -f emails.txt -o results.json --delay 2
        """
    )
    
    parser.add_argument('email', nargs='?', help='Alamat email yang akan dicek')
    parser.add_argument('-f', '--file', help='File berisi list email (satu per baris)')
    parser.add_argument('-o', '--output', help='File output untuk menyimpan hasil (JSON)')
    parser.add_argument('-m', '--method', choices=['smtp', 'vrfy', 'format', 'microsoft'], default='microsoft',
                       help='Metode pengecekan: microsoft (cek terdaftar di Microsoft), smtp (SMTP verification), vrfy (VRFY command), format (format & domain only) (default: microsoft)')
    parser.add_argument('-t', '--timeout', type=int, default=10,
                       help='Timeout koneksi dalam detik (default: 10)')
    parser.add_argument('-d', '--delay', type=float, default=1.0,
                       help='Delay antar pengecekan dalam detik (default: 1.0)')
    parser.add_argument('-r', '--retry', type=int, default=2,
                       help='Jumlah retry jika timeout (default: 2)')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Tampilkan detail koneksi ke Microsoft')
    parser.add_argument('--no-save', action='store_true',
                       help='Jangan simpan hasil ke file')
    
    args = parser.parse_args()
    
    # Initialize checker
    checker = HotmailChecker(timeout=args.timeout, delay=args.delay, retry=args.retry, verbose=args.verbose)
    
    results = []
    
    if args.file:
        # Bulk checking dari file
        emails = load_emails_from_file(args.file)
        results = checker.check_bulk(emails, method=args.method)
    elif args.email:
        # Single email checking
        print(f"Mengecek email: {args.email}\n")
        result = checker.check_email(args.email, method=args.method)
        results = [result]
        
        # Print hasil
        print(f"Email: {result['email']}")
        print(f"Domain: {result['domain']}")
        print(f"Status: {'[VALID]' if result['valid'] else '[INVALID]'}")
        print(f"Pesan: {result['message']}")
    else:
        parser.print_help()
        sys.exit(1)
    
    # Print summary
    if len(results) > 1:
        print_summary(results)
    
    # Save results
    if not args.no_save and results:
        output_file = args.output or (None if args.email else None)
        save_results(results, output_file)


if __name__ == '__main__':
    main()
