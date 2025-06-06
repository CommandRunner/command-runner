
![image](https://github.com/user-attachments/assets/530ae151-422d-4783-a974-362834a3871e)








**Command Runner** is a Burp Suite extension that enables you to run system commands directly within Burp’s interface. It supports multiple tabs, a command playbook to save commands, and real-time output display, helping penetration testers integrate OS tools seamlessly into burpsuite.

---

## Features

- Execute OS commands from inside Burp Suite (Kali Linux)
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

   - It’s recommended to edit commands.txt directly to organize your saved commands more effectively. Using the save command function will simply add the new command to the bottom of the list, which can make organization harder.
   - Edit `commands.txt` to add your frequently used commands (one per line)
   - An example format is provided in commands.txt, edit it to your liking.

     ![image](https://github.com/user-attachments/assets/20966310-44fc-4d39-960d-4e2405f67c99)

   - The commands.txt file should be in the same directory as the script otherwise it won't load your commands.
   - Now you should be easily able to run the commands you need just change up the target.
     
     ![image](https://github.com/user-attachments/assets/c36ce7ff-19cf-4491-960c-60b081cf3b76)


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

6. **Resizing**
   - click on the small arrows to resize 
     
     ![image](https://github.com/user-attachments/assets/b382bff0-f217-4d3f-bc3f-dd5621d786b6)


---

## Security Notice

- Commands run with your local user privileges.
- Avoid running untrusted or dangerous commands.
- Use only on authorized targets.

---

