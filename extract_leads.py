#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract Leads dari hasil JSON
Mengambil email yang valid dari hasil pengecekan dan menyimpannya dalam format list sederhana
"""

import json
import sys
import argparse
from pathlib import Path


def extract_leads(json_file: str, output_file: str = None, valid_only: bool = True, split_files: bool = False):
    """
    Ekstrak email dari hasil JSON
    
    Args:
        json_file: File JSON hasil pengecekan
        output_file: File output untuk menyimpan leads (default: leads.txt)
        valid_only: Hanya ambil email yang valid (default: True)
        split_files: Pisahkan menjadi 2 file (valid dan invalid) (default: False)
    """
    try:
        # Baca file JSON
        with open(json_file, 'r', encoding='utf-8') as f:
            results = json.load(f)
        
        # Pisahkan email valid dan invalid
        valid_emails = []
        invalid_emails = []
        
        for result in results:
            email = result.get('email', '')
            is_valid = result.get('valid', False)
            
            if is_valid:
                valid_emails.append(email)
            else:
                invalid_emails.append(email)
        
        # Jika split_files = True, simpan ke 2 file terpisah
        if split_files:
            # Tentukan nama file output
            if output_file is None:
                valid_file = 'valid_emails.txt'
                invalid_file = 'invalid_emails.txt'
            else:
                # Jika output_file diberikan, gunakan sebagai prefix
                base_name = output_file.replace('.txt', '')
                valid_file = f'{base_name}_valid.txt'
                invalid_file = f'{base_name}_invalid.txt'
            
            # Simpan email valid
            with open(valid_file, 'w', encoding='utf-8') as f:
                for email in valid_emails:
                    f.write(email + '\n')
            
            # Simpan email invalid
            with open(invalid_file, 'w', encoding='utf-8') as f:
                for email in invalid_emails:
                    f.write(email + '\n')
            
            print(f"\nBerhasil memisahkan hasil:")
            print(f"  Email VALID: {len(valid_emails)} email -> {valid_file}")
            print(f"  Email INVALID: {len(invalid_emails)} email -> {invalid_file}")
            
            # Tampilkan preview
            if valid_emails:
                print(f"\nPreview Email Valid (5 pertama):")
                for i, email in enumerate(valid_emails[:5], 1):
                    print(f"  {i}. {email}")
                if len(valid_emails) > 5:
                    print(f"  ... dan {len(valid_emails) - 5} email lainnya")
            
            if invalid_emails:
                print(f"\nPreview Email Invalid (5 pertama):")
                for i, email in enumerate(invalid_emails[:5], 1):
                    print(f"  {i}. {email}")
                if len(invalid_emails) > 5:
                    print(f"  ... dan {len(invalid_emails) - 5} email lainnya")
            
            return valid_emails, invalid_emails
        
        # Jika tidak split, gunakan logika lama
        else:
            # Ekstrak email sesuai valid_only
            leads = []
            for result in results:
                if valid_only:
                    if result.get('valid', False):
                        leads.append(result['email'])
                else:
                    leads.append(result['email'])
            
            # Tentukan nama file output
            if output_file is None:
                output_file = 'leads.txt'
            
            # Simpan ke file
            with open(output_file, 'w', encoding='utf-8') as f:
                for email in leads:
                    f.write(email + '\n')
            
            print(f"Berhasil mengekstrak {len(leads)} email")
            print(f"Hasil disimpan ke: {output_file}")
            
            # Tampilkan preview
            if leads:
                print("\nPreview (5 pertama):")
                for i, email in enumerate(leads[:5], 1):
                    print(f"  {i}. {email}")
                if len(leads) > 5:
                    print(f"  ... dan {len(leads) - 5} email lainnya")
            
            return leads
        
    except FileNotFoundError:
        print(f"Error: File '{json_file}' tidak ditemukan")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: File JSON tidak valid - {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Extract Leads dari hasil JSON pengecekan email',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Contoh penggunaan:
  python extract_leads.py hasil_test_final.json
  python extract_leads.py hasil_test_final.json -o valid_emails.txt
  python extract_leads.py hasil_test_final.json --all -o all_emails.txt
        """
    )
    
    parser.add_argument('json_file', help='File JSON hasil pengecekan')
    parser.add_argument('-o', '--output', help='File output untuk menyimpan leads (default: leads.txt atau prefix untuk split)')
    parser.add_argument('--all', action='store_true', 
                       help='Ambil semua email (valid dan invalid), bukan hanya yang valid')
    parser.add_argument('--split', action='store_true',
                       help='Pisahkan menjadi 2 file: valid_emails.txt dan invalid_emails.txt')
    
    args = parser.parse_args()
    
    extract_leads(args.json_file, args.output, valid_only=not args.all, split_files=args.split)


if __name__ == '__main__':
    main()
