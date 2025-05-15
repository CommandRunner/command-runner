
![image](https://github.com/user-attachments/assets/530ae151-422d-4783-a974-362834a3871e)








**Command Runner** is a Burp Suite extension that enables you to run system commands directly within Burp’s interface. It supports multiple tabs, a command playbook to save commands, and real-time output display, helping penetration testers integrate OS tools seamlessly into their workflow.

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
     
     ![image](https://github.com/user-attachments/assets/556934aa-ccdf-4b32-bd07-cafa5bc318c9)

   - git clone https://github.com/CommandRunner/command-runner
   - Go to extensions click on Add > Extension type - python > Next.
   - You should see a tab now in burpsuite that says command runner
  
     ![image](https://github.com/user-attachments/assets/e6530413-3856-4a8a-8af4-c11b69449a27)


2. **Prepare Command Playbook**
   - Edit `commands.txt` to add your frequently used commands (one per line)
   - An example format is provided in commands.txt, edit it to your liking.
   - The commands.txt file should be in the same directory as the script otherwise it won't load your commands.

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
   - Make sure all the tools you'd like to use are already installed on your system and on path.

4. **Use the Command Playbook:**
   - Select a saved command from the dropdown.
   - Click **Save Command** to add the current command to the playbook.
   - Click **Delete Command** to remove a selected command.
   - Commands persist in `commands.txt` across sessions.

5. **Cancel or Close:**
   - Use **Cancel** to stop a running command.
   - Use **Close Tab** to remove the current tab.

6. **Increase/decrease the pane sizing**
   - click on the small arrows to increase or decrease the pane size to easily read the output.

---

## Recommended Usage

- Edit the commands you'd like to save directly in commands.txt so you can organize everything properly. If you dont care about organization then go ahead and use the save command funciton directly.
- Share your playbooks with people to get different ideas.


---

## Security Notice

- Commands run with your local user privileges.
- Avoid running untrusted or dangerous commands.
- Use only on authorized targets.

---
## Questions?

Feel free to msg me on discord erxc899

---

Developed by Az.  
Inspired by real-world penetration testing workflows.
Enjoy making your workflow seamless with Command Runner!

