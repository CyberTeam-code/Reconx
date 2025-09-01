# #!/usr/bin/env python3
"""
ReconX Complete - Real Working Python-Only Reconnaissance Tool
Author: Security Research Team
Version: 6.0.0 - Real Output Without External Tools
"""

import argparse
import json
import os
import socket
import time
import requests
import urllib3
from urllib.parse import urljoin, urlparse
import re
import concurrent.futures
from datetime import datetime
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DEFAULT_USER_AGENT = "Mozilla/5.0 (ReconX-Complete/6.0.0)"

class ReconXComplete:
    def __init__(self):
        self.results = {}
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': DEFAULT_USER_AGENT})
        self.session.verify = False
        self.timeout = 10

    def print_banner(self):
        banner = r"""
░█████████                                              ░██    ░██ 
░██     ░██                                              ░██  ░██  
░██     ░██  ░███████   ░███████   ░███████  ░████████    ░██░██   
░█████████  ░██    ░██ ░██    ░██ ░██    ░██ ░██    ░██    ░███    
░██   ░██   ░█████████ ░██        ░██    ░██ ░██    ░██   ░██░██   
░██    ░██  ░██        ░██    ░██ ░██    ░██ ░██    ░██  ░██  ░██  
░██     ░██  ░███████   ░███████   ░███████  ░██    ░██ ░██    ░██ 
                                                                   
                                                                   
                                                                   
ReconX Complete v6.0.0 | Real Reconnaissance - No External Tools
Author: Security Research Team
        """
        print(banner)

    # --------------------------
    # REAL URL ENUMERATION - Python Only
    # --------------------------
    def url_enumeration_real(self, domain):
        """Real URL enumeration using Python only"""
        print("[+] Running real URL enumeration...")
        urls = set()
        
        base_url = f"https://{domain}"
        http_url = f"http://{domain}"
        
        # 1. Check common endpoints
        common_endpoints = [
            'robots.txt', 'sitemap.xml', 'sitemap_index.xml',
            'crossdomain.xml', 'clientaccesspolicy.xml',
            '.well-known/security.txt', '.well-known/robots.txt',
            'humans.txt', 'ads.txt', 'security.txt',
            'favicon.ico', 'sitemap.html', 'sitemap.htm'
        ]
        
        for endpoint in common_endpoints:
            for protocol in [base_url, http_url]:
                try:
                    response = self.session.get(f"{protocol}/{endpoint}", timeout=5)
                    if response.status_code == 200:
                        urls.add(f"{protocol}/{endpoint}")
                        print(f" ✅ Found: {protocol}/{endpoint}")
                        
                        # Parse sitemap for more URLs
                        if 'sitemap' in endpoint:
                            from bs4 import BeautifulSoup # type: ignore
                            soup = BeautifulSoup(response.text, 'xml')
                            loc_tags = soup.find_all('loc')
                            for loc in loc_tags:
                                urls.add(loc.text)
                                print(f" ✅ Found in sitemap: {loc.text}")
                                
                except Exception:
                    pass
        
        # 2. Check common API endpoints
        api_endpoints = [
            'api', 'api/v1', 'api/v2', 'rest', 'graphql',
            'swagger', 'swagger.json', 'openapi.json',
            'docs', 'documentation', 'api-docs'
        ]
        
        for endpoint in api_endpoints:
            for protocol in [base_url, http_url]:
                try:
                    response = self.session.get(f"{protocol}/{endpoint}", timeout=5)
                    if response.status_code in [200, 301, 302, 403]:
                        urls.add(f"{protocol}/{endpoint} [{response.status_code}]")
                        print(f" ✅ Found API: {protocol}/{endpoint} [{response.status_code}]")
                except:
                    pass
        
        # 3. Check for backup files
        backup_files = [
            'backup.zip', 'backup.tar.gz', 'site.zip', 'database.sql',
            'config.php.bak', '.env.backup', 'wp-config.php.bak'
        ]
        
        for file in backup_files:
            for protocol in [base_url, http_url]:
                try:
                    response = self.session.get(f"{protocol}/{file}", timeout=5)
                    if response.status_code == 200:
                        urls.add(f"{protocol}/{file} [BACKUP FILE]")
                        print(f" 🚨 Found backup: {protocol}/{file}")
                except:
                    pass
        
        return list(set(urls))

    # --------------------------
    # REAL SUBDOMAIN ENUMERATION - Python Only
    # --------------------------
    def subdomain_enumeration_real(self, domain):
        """Real subdomain enumeration using Python only"""
        print("[+] Running real subdomain enumeration...")
        subdomains = set()
        
        # 1. crt.sh API (real data)
        try:
            url = f"https://crt.sh/?q=%.{domain}&output=json"
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for entry in data:
                    name_value = entry.get('name_value', '')
                    if name_value:
                        for subdomain in name_value.split('\n'):
                            if subdomain.strip() and '*' not in subdomain:
                                subdomains.add(subdomain.strip())
                                print(f" ✅ Found via crt.sh: {subdomain.strip()}")
        except Exception as e:
            print(f" [!] crt.sh error: {e}")
        
        # 2. DNS resolution check for common subdomains
        common_subdomains = [
            'www', 'mail', 'ftp', 'admin', 'api', 'blog', 'dev', 'test',
            'staging', 'app', 'portal', 'secure', 'vpn', 'support', 'help',
            'docs', 'wiki', 'forum', 'chat', 'cdn', 'static', 'assets'
        ]
        
        print("[+] Checking common subdomains...")
        for sub in common_subdomains:
            subdomain = f"{sub}.{domain}"
            try:
                # DNS resolution check
                socket.gethostbyname(subdomain)
                subdomains.add(subdomain)
                print(f" ✅ Found via DNS: {subdomain}")
                
                # HTTP check
                for protocol in [f"https://{subdomain}", f"http://{subdomain}"]:
                    try:
                        response = self.session.get(protocol, timeout=3)
                        if response.status_code < 400:
                            print(f" ✅ Found active: {protocol}")
                    except:
                        pass
                        
            except socket.gaierror:
                pass
        
        # 3. Certificate transparency logs
        try:
            url = f"https://crt.sh/?q={domain}&output=json"
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for entry in data:
                    name = entry.get('name_value', '')
                    if name and domain in name and '*' not in name:
                        subdomains.add(name.strip())
                        print(f" ✅ Found via CT: {name.strip()}")
        except:
            pass
        
        return list(set(subdomains))

    # --------------------------
    # REAL DIRECTORY ENUMERATION - Python Only
    # --------------------------
    def directory_enumeration_real(self, base_url, wordlist):
        """Real directory enumeration using Python only"""
        print("[+] Running real directory enumeration...")
        results = []
        
        paths = ['admin', 'api', 'login', 'config', 'backup']
        
        if os.path.exists(wordlist):
            try:
                with open(wordlist, 'r') as f:
                    custom_paths = [line.strip() for line in f if line.strip()]
                    if custom_paths:
                        paths = custom_paths
            except:
                pass
        
        print(f"[+] Checking {len(paths)} paths...")
        
        def check_path(path):
            for protocol in [f"{base_url}/{path}", f"{base_url.replace('https://', 'http://')}/{path}"]:
                try:
                    response = self.session.get(protocol, timeout=5)
                    if response.status_code in [200, 301, 302, 403, 401, 500]:
                        result = f"{protocol} [{response.status_code}]"
                        print(f" ✅ Found: {result}")
                        return result
                except:
                    pass
            return None
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            future_to_path = {executor.submit(check_path, path): path for path in paths}
            for future in concurrent.futures.as_completed(future_to_path):
                result = future.result()
                if result:
                    results.append(result)
        
        return sorted(list(set(results)))

    # --------------------------
    # REAL GITHUB RECONNAISSANCE
    # --------------------------
    def github_reconnaissance_real(self, domain):
        """Real GitHub reconnaissance using GitHub API"""
        print("[+] Running real GitHub reconnaissance...")
        results = []
        
        github_dorks = [
            f"{domain} api_key", f"{domain} password", f"{domain} secret",
            f"{domain} token", f"{domain} config", f"{domain} database"
        ]
        
        token = os.getenv("GITHUB_TOKEN")
        headers = {"Authorization": f"token {token}"} if token else {}
        
        print("[+] Searching GitHub for sensitive information...")
        for dork in github_dorks:
            try:
                query = dork.replace(" ", "+")
                url = f"https://api.github.com/search/code?q={query}"
                response = self.session.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    items = data.get("items", [])[:3]
                    for item in items:
                        results.append(item["html_url"])
                        print(f" 🚨 Found: {item['html_url']} ({dork})")
                
                time.sleep(1)
                
            except Exception as e:
                print(f" [!] GitHub API error for {dork}: {e}")
        
        return list(set(results))

    # --------------------------
    # EXPORT METHODS - PDF and Excel
    # --------------------------
    def export_to_excel(self, results, filename):
        """Export results to Excel format"""
        try:
            # Create DataFrames for each result type
            dfs = {}
            
            if 'url_enumeration' in results and results['url_enumeration']:
                dfs['URLs'] = pd.DataFrame(results['url_enumeration'], columns=['URL'])
            
            if 'subdomain_enumeration' in results and results['subdomain_enumeration']:
                dfs['Subdomains'] = pd.DataFrame(results['subdomain_enumeration'], columns=['Subdomain'])
            
            if 'github_reconnaissance' in results and results['github_reconnaissance']:
                dfs['GitHub_Findings'] = pd.DataFrame(results['github_reconnaissance'], columns=['GitHub_URL'])
            
            if 'directory_enumeration' in results and results['directory_enumeration']:
                dfs['Directories'] = pd.DataFrame(results['directory_enumeration'], columns=['Directory'])
            
            # Create summary sheet
            summary_data = {
                'Category': ['URLs', 'Subdomains', 'GitHub Findings', 'Directories'],
                'Count': [
                    len(results.get('url_enumeration', [])),
                    len(results.get('subdomain_enumeration', [])),
                    len(results.get('github_reconnaissance', [])),
                    len(results.get('directory_enumeration', []))
                ]
            }
            dfs['Summary'] = pd.DataFrame(summary_data)
            
            # Write to Excel
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                for sheet_name, df in dfs.items():
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            print(f"✅ Excel report saved to: {filename}")
            
        except Exception as e:
            print(f"❌ Error exporting to Excel: {e}")

    def export_to_pdf(self, results, filename):
        """Export results to PDF format"""
        try:
            doc = SimpleDocTemplate(filename, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            # Title
            title = Paragraph("ReconX Complete - Scan Report", styles['Title'])
            story.append(title)
            story.append(Spacer(1, 12))
            
            # Summary
            summary_text = f"""
            Target: {results.get('target', 'N/A')}
            Scan Date: {results.get('started_at', 'N/A')}
            Method: {results.get('method', 'N/A')}
            
            Results Summary:
            - URLs Discovered: {len(results.get('url_enumeration', []))}
            - Subdomains Discovered: {len(results.get('subdomain_enumeration', []))}
            - GitHub Findings: {len(results.get('github_reconnaissance', []))}
            - Directories Discovered: {len(results.get('directory_enumeration', []))}
            """
            summary = Paragraph(summary_text, styles['Normal'])
            story.append(summary)
            story.append(Spacer(1, 12))
            
            # Detailed results tables
            if results.get('url_enumeration'):
                story.append(Paragraph("URLs Discovered:", styles['Heading2']))
                url_data = [['URL']] + [[url] for url in results['url_enumeration'][:50]]  # Limit to 50 URLs
                url_table = Table(url_data)
                url_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                ]))
                story.append(url_table)
                story.append(Spacer(1, 12))
            
            if results.get('subdomain_enumeration'):
                story.append(Paragraph("Subdomains Discovered:", styles['Heading2']))
                subdomain_data = [['Subdomain']] + [[sub] for sub in results['subdomain_enumeration'][:50]]
                subdomain_table = Table(subdomain_data)
                subdomain_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                ]))
                story.append(subdomain_table)
                story.append(Spacer(1, 12))
            
            doc.build(story)
            print(f"✅ PDF report saved to: {filename}")
            
        except Exception as e:
            print(f"❌ Error exporting to PDF: {e}")

    # --------------------------
    # FULL RECON - Real Results
    # --------------------------
    def run_full_recon_real(self, target, base_url, save_path):
        """Run complete reconnaissance with real results"""
        print(f"\n[+] Starting REAL reconnaissance for: {target}")
        print(f"[+] Base URL: {base_url}")
        print(f"[+] Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("[+] Using Python-only methods (no external tools required)\n")
        
        results = {
            "target": target,
            "timestamp": int(time.time()),
            "started_at": datetime.now().isoformat(),
            "method": "Python-only (no external tools)",
            "url_enumeration": self.url_enumeration_real(target),
            "subdomain_enumeration": self.subdomain_enumeration_real(target),
            "github_reconnaissance": self.github_reconnaissance_real(target),
            "directory_enumeration": self.directory_enumeration_real(base_url, "wordlist.txt")
        }
        
        print("\n" + "="*60)
        print("REAL RECONNAISSANCE RESULTS")
        print("="*60)
        print(f"Target: {target}")
        print(f"URLs discovered: {len(results['url_enumeration'])}")
        print(f"Subdomains discovered: {len(results['subdomain_enumeration'])}")
        print(f"GitHub findings: {len(results['github_reconnaissance'])}")
        print(f"Directories discovered: {len(results['directory_enumeration'])}")
        print("="*60)
        
        if results['url_enumeration']:
            print("\n📋 Sample URLs found:")
            for url in results['url_enumeration'][:5]:
                print(f" - {url}")
        
        if results['subdomain_enumeration']:
            print("\n🌐 Sample subdomains found:")
            for subdomain in results['subdomain_enumeration'][:5]:
                print(f" - {subdomain}")
        
        if results['github_reconnaissance']:
            print("\n🔍 Sample GitHub findings:")
            for github in results['github_reconnaissance'][:3]:
                print(f" - {github}")
        
        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, "w") as f:
                json.dump(results, f, indent=2)
            print(f"\n[+] Complete results saved to: {save_path}")
        
        return results

# --------------------------
# MAIN - Interactive Menu Version
# --------------------------
def main():
    recon = ReconXComplete()
    recon.print_banner()
    
    print("\n" + "="*60)
    print("RECONX COMPLETE - INTERACTIVE MENU")
    print("="*60)
    
    # Get target domain
    target = input("\n🎯 Enter target domain (e.g., example.com): ").strip()
    if not target:
        print("❌ Target domain is required!")
        return
    
    # Get base URL
    base_url_input = input(f"🌐 Enter base URL (press Enter for https://{target}): ").strip()
    base_url = base_url_input if base_url_input else f"https://{target}"
    
    # Show menu options
    print("\n" + "="*60)
    print("SELECT RECONNAISSANCE TYPE:")
    print("="*60)
    print("1. Full Reconnaissance (Complete scan)")
    print("2. URL Enumeration only")
    print("3. Subdomain Enumeration only")
    print("4. GitHub Reconnaissance only")
    print("5. Directory Enumeration only")
    print("="*60)
    
    # Get scan choice
    try:
        choice = int(input("\n🔢 Enter your choice (1-5): ").strip())
    except ValueError:
        print("❌ Please enter a valid number (1-5)")
        return
    
    # Results will be displayed on screen
    save_path = None
    
    # Execute selected scan
    results = {}
    
    if choice == 1:
        print(f"\n🚀 Starting FULL RECONNAISSANCE on {target}...")
        results = recon.run_full_recon_real(target, base_url, save_path)
        
    elif choice == 2:
        print(f"\n🔗 Starting URL ENUMERATION on {target}...")
        results = {"url_enumeration": recon.url_enumeration_real(target)}
        
    elif choice == 3:
        print(f"\n🌐 Starting SUBDOMAIN ENUMERATION on {target}...")
        results = {"subdomain_enumeration": recon.subdomain_enumeration_real(target)}
        
    elif choice == 4:
        print(f"\n🐙 Starting GITHUB RECONNAISSANCE for {target}...")
        results = {"github_reconnaissance": recon.github_reconnaissance_real(target)}
        
    elif choice == 5:
        print(f"\n📁 Starting DIRECTORY ENUMERATION on {base_url}...")
        results = {"directory_enumeration": recon.directory_enumeration_real(base_url, "wordlist.txt")}
        
    else:
        print("❌ Invalid choice! Please select 1-5.")
        return
    
    # Display results if not saved to file
    if not save_path and results:
        print("\n" + "="*60)
        print("SCAN RESULTS:")
        print("="*60)
        print(json.dumps(results, indent=2))
    
    # Ask if user wants to export to PDF or Excel
    if results:
        print("\n" + "="*60)
        print("EXPORT OPTIONS:")
        print("="*60)
        print("1. Export to PDF")
        print("2. Export to Excel")
        print("3. Export to both PDF and Excel")
        print("4. Skip export")
        
        try:
            export_choice = int(input("\n🔢 Choose export option (1-4): ").strip())

            if export_choice in [1, 2, 3]:
                base_filename = input("💾 Enter base filename (without extension): ").strip()
                if not base_filename:
                    base_filename = f"reconx_{target}_{int(time.time())}"

                if export_choice in [1, 3]:
                    pdf_filename = f"{base_filename}.pdf"
                    recon.export_to_pdf(results, pdf_filename)

                if export_choice in [2, 3]:
                    excel_filename = f"{base_filename}.xlsx"
                    recon.export_to_excel(results, excel_filename)

            elif export_choice == 4:
                pass

            else:
                print("❌ Invalid export choice! Please select 1-4.")

        except ValueError:
            print("❌ Please enter a valid number (1-4)")

if __name__ == "__main__":
    main()
