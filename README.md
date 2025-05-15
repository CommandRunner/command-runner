# Command Runner for Burp Suite

![image](https://github.com/user-attachments/assets/530ae151-422d-4783-a974-362834a3871e)








**Command Runner** is a Burp Suite extension that enables you to run system commands directly within Burp’s interface. It supports multiple tabs, a command playbook for saved commands, and real-time output display, helping penetration testers integrate OS tools seamlessly into their workflow.

---

## Features

- Execute OS commands from inside Burp Suite (Linux, macOS, Windows)
- Multiple independent command tabs
- Manage a command playbook with save/delete functionality
- Real-time command output display
- Cancel running commands anytime

---

## Installation

1. **Prerequisites:**
   - Burp Suite Professional or Community Edition
   - Jython standalone JAR ([Download here](https://www.jython.org/download))
   - Add the jython jar file to burp. Click on settings > extensions > Python enviroment > add the jython jar file.
   - git clone https://github.com/CommandRunner/command-runner
   - Go to extensions click on Add > Extension type - python > Next.
   - You should see a tab now in burpsuite that says command runner
  
     ![image](https://github.com/user-attachments/assets/e6530413-3856-4a8a-8af4-c11b69449a27)


2. **Prepare Command Playbook**
   - Edit `commands.txt` to add your frequently used commands (one per line)
   - An example format is provided in commands.txt, edit it to your liking.

---

## How to Use

1. **Open the "Command Runner" tab** in Burp Suite after loading the extension.

2. **Manage Tabs:**
   - Click **+ New Tab** to open multiple command runners.
   - Each tab runs commands independently.

3. **Run Commands:**
   - Enter a command in the input field (e.g., `nmap -sV target.com`)
   - Click **Run command** to execute it.
   - View real-time output in the pane below.

4. **Use the Command Playbook:**
   - Select a saved command from the dropdown.
   - Click **Save Command** to add the current command to the playbook.
   - Click **Delete Command** to remove a selected command.
   - Commands persist in `commands.txt` across sessions.

5. **Cancel or Close:**
   - Use **Cancel** to stop a running command.
   - Use **Close Tab** to remove the current tab.

---

## Recommended USage


---

## Security Notice

- Commands run with your local user privileges.
- Avoid running untrusted or dangerous commands.
- Use only on authorized targets.

---

## Contact
feel free to msg me on discord erxc899
---

## License

MIT License

---

## Credits

Developed by Az.  
Inspired by real-world penetration testing workflows.

---

Enjoy automating your Burp Suite workflow with Command Runner!

