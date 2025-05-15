# -*- coding: utf-8 -*-
from burp import IBurpExtender, ITab
import subprocess
import threading
import sys
import os
import uuid
import re

from javax.swing import (JPanel, JButton, JTextField, JLabel, JScrollPane,
                        JTextArea, JSplitPane, SwingUtilities, Box,
                        JTabbedPane, JComboBox, UIManager, BorderFactory,
                        BoxLayout, ImageIcon)
from java.awt import BorderLayout, Dimension, Font, FlowLayout
from javax.swing.text import DefaultCaret
from javax.swing.border import EmptyBorder, CompoundBorder, TitledBorder

COMMANDS_FILE = "commands.txt"

class BurpExtender(IBurpExtender, ITab):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        callbacks.setExtensionName("Command Runner")

        sys.stdout = callbacks.getStdout()
        sys.stderr = callbacks.getStderr()

        self._commands = []
        self._load_commands()
        self._tabs = {}
        SwingUtilities.invokeLater(self._create_ui)

    def _create_ui(self):
        self._main_panel = JPanel(BorderLayout())
        self._main_panel.setBorder(EmptyBorder(10, 10, 10, 10))

        header_panel = JPanel(BorderLayout())
        header_label = JLabel("Command Runner", JLabel.CENTER)
        header_label.setFont(Font("Sans-Serif", Font.BOLD, 14))
        header_label.setBorder(EmptyBorder(8, 10, 8, 10))
        header_panel.add(header_label, BorderLayout.CENTER)

        self._tabbed_pane = JTabbedPane()
        self._tabbed_pane.setBorder(EmptyBorder(10, 0, 0, 0))

        add_tab_button = JButton("+ New Tab")
        add_tab_button.setBorder(BorderFactory.createEmptyBorder(8, 15, 8, 15))
        add_tab_button.addActionListener(self._add_tab)

        button_panel = JPanel(FlowLayout(FlowLayout.RIGHT))
        button_panel.add(add_tab_button)
        header_panel.add(button_panel, BorderLayout.EAST)

        self._main_panel.add(header_panel, BorderLayout.NORTH)
        self._main_panel.add(self._tabbed_pane, BorderLayout.CENTER)

        self._main_panel.setPreferredSize(Dimension(800, 600))
        self._add_tab(None)
        self._callbacks.addSuiteTab(self)

    def _add_tab(self, event):
        tab_id = str(uuid.uuid4())
        panel = JPanel(BorderLayout())
        panel.setBorder(EmptyBorder(10, 10, 10, 10))

        command_panel = JPanel()
        command_panel.setLayout(BoxLayout(command_panel, BoxLayout.Y_AXIS))
        command_panel.setBorder(CompoundBorder(
            TitledBorder(BorderFactory.createLineBorder(UIManager.getColor("TitledBorder.border")), "Command Configuration"),
            EmptyBorder(10, 10, 10, 10)
        ))

        cmd_input_panel = JPanel(BorderLayout())
        cmd_label = JLabel("Command:")
        cmd_label.setFont(Font("Sans-Serif", Font.PLAIN, 12))
        cmd_input_panel.add(cmd_label, BorderLayout.WEST)
        cmd_input = JTextField("echo Hello from tab")
        cmd_input.setFont(Font("Monospaced", Font.PLAIN, 12))
        cmd_input.setBorder(BorderFactory.createCompoundBorder(
            BorderFactory.createLineBorder(UIManager.getColor("TextField.border")),
            BorderFactory.createEmptyBorder(5, 5, 5, 5)
        ))
        cmd_input_panel.add(cmd_input, BorderLayout.CENTER)
        command_panel.add(cmd_input_panel)

        command_panel.setMinimumSize(Dimension(100, 150))
        command_panel.add(Box.createRigidArea(Dimension(0, 10)))

        saved_commands_panel = JPanel(BorderLayout())
        saved_commands_panel.add(JLabel("Saved Commands:"), BorderLayout.WEST)

        cmd_combo = JComboBox(self._commands)
        cmd_combo.setFont(Font("Sans-Serif", Font.PLAIN, 12))
        cmd_combo.setEditable(False)
        cmd_combo.setPreferredSize(Dimension(300, 30))
        cmd_combo.addActionListener(lambda e, ci=cmd_input, cc=cmd_combo: ci.setText(cc.getSelectedItem()) if cc.getSelectedItem() else None)
        saved_commands_panel.add(cmd_combo, BorderLayout.CENTER)

        cmd_button_panel = JPanel(FlowLayout(FlowLayout.RIGHT))
        save_button = self._create_styled_button("Save Command", lambda e, ci=cmd_input, cc=cmd_combo: self._save_command(ci.getText(), cc))
        delete_button = self._create_styled_button("Delete Command", lambda e, cc=cmd_combo: self._delete_command(cc))
        cmd_button_panel.add(save_button)
        cmd_button_panel.add(delete_button)
        saved_commands_panel.add(cmd_button_panel, BorderLayout.EAST)

        command_panel.add(saved_commands_panel)
        command_panel.add(Box.createRigidArea(Dimension(0, 10)))

        action_panel = JPanel(FlowLayout(FlowLayout.RIGHT))
        run_button = self._create_styled_button("Run command", lambda e: self._run_command(tab_id))
        cancel_button = self._create_styled_button("Cancel", lambda e: self._cancel_command(tab_id))
        cancel_button.setEnabled(False)
        close_button = self._create_styled_button("Close Tab", lambda e: self._close_tab(tab_id))

        action_panel.add(run_button)
        action_panel.add(cancel_button)
        action_panel.add(close_button)
        command_panel.add(action_panel)

        output_panel = JPanel(BorderLayout())
        output_panel.setBorder(CompoundBorder(
            TitledBorder(BorderFactory.createLineBorder(UIManager.getColor("TitledBorder.border")), "Command Output"),
            EmptyBorder(10, 10, 10, 10)
        ))

        output = JTextArea()
        output.setEditable(False)
        output.setFont(Font("Monospaced", Font.PLAIN, 13))
        output.setBorder(BorderFactory.createEmptyBorder(5, 5, 5, 5))
        caret = output.getCaret()
        caret.setUpdatePolicy(DefaultCaret.ALWAYS_UPDATE)
        output_scroll = JScrollPane(output)
        output_scroll.setMinimumSize(Dimension(100, 100))
        output_scroll.setPreferredSize(Dimension(100, 400))
        output_scroll.setBorder(BorderFactory.createLineBorder(UIManager.getColor("ScrollPane.border")))

        output_panel.add(output_scroll, BorderLayout.CENTER)

        # Add input field and send button for interactive input
        input_panel = JPanel(BorderLayout())
        input_field = JTextField()
        input_field.setFont(Font("Monospaced", Font.PLAIN, 12))
        send_button = self._create_styled_button("Send Input", None)
        input_panel.add(input_field, BorderLayout.CENTER)
        input_panel.add(send_button, BorderLayout.EAST)
        output_panel.add(input_panel, BorderLayout.SOUTH)

        split_pane = JSplitPane(JSplitPane.VERTICAL_SPLIT, command_panel, output_panel)
        split_pane.setResizeWeight(0.3)
        split_pane.setOneTouchExpandable(True)
        split_pane.setBorder(None)
        split_pane.setDividerSize(8)

        output_panel.setMinimumSize(Dimension(100, 100))
        output_panel.setPreferredSize(Dimension(100, 400))

        panel.add(split_pane, BorderLayout.CENTER)

        self._tabs[tab_id] = {
            "panel": panel,
            "cmd_input": cmd_input,
            "cmd_combo": cmd_combo,
            "run_button": run_button,
            "cancel_button": cancel_button,
            "close_button": close_button,
            "output": output,
            "process": None,
            "input_field": input_field,
            "send_button": send_button
        }

        # Hook up send_button to send input to process
        def send_input_action(event, tab_id=tab_id):
            tab = self._tabs.get(tab_id)
            process = tab["process"]
            if process and process.stdin:
                user_input = tab["input_field"].getText()
                try:
                    process.stdin.write((user_input + "\n").encode('utf-8'))
                    process.stdin.flush()
                    SwingUtilities.invokeLater(lambda: tab["output"].append("> " + user_input + "\n"))
                    tab["input_field"].setText("")
                except Exception as e:
                    SwingUtilities.invokeLater(lambda: tab["output"].append("\nError sending input: {}\n".format(str(e))))
            else:
                SwingUtilities.invokeLater(lambda: tab["output"].append("\nNo running process to send input to.\n"))
        send_button.addActionListener(send_input_action)

        self._tabbed_pane.addTab("Tab", panel)
        index = self._tabbed_pane.indexOfComponent(panel)
        self._tabbed_pane.setTitleAt(index, "Tab " + str(index + 1))
        self._tabbed_pane.setSelectedIndex(index)

    def _create_styled_button(self, text, action_listener):
        button = JButton(text)
        button.setFont(Font("Sans-Serif", Font.PLAIN, 12))
        button.setBorder(BorderFactory.createEmptyBorder(6, 12, 6, 12))
        if action_listener:
            button.addActionListener(action_listener)
        return button

    def _close_tab(self, tab_id):
        tab_data = self._tabs.get(tab_id)
        if tab_data:
            panel = tab_data["panel"]
            index = self._tabbed_pane.indexOfComponent(panel)
            if index != -1:
                self._tabbed_pane.remove(index)
            self._cancel_command(tab_id)
            del self._tabs[tab_id]

    def _save_command(self, cmd, combo):
        cmd = cmd.strip()
        if cmd and cmd not in self._commands:
            self._commands.append(cmd)
            for tab_data in self._tabs.values():
                tab_data["cmd_combo"].addItem(cmd)
            self._save_commands()

    def _delete_command(self, combo):
        idx = combo.getSelectedIndex()
        if 0 <= idx < len(self._commands):
            cmd_to_delete = combo.getItemAt(idx)
            del self._commands[idx]
            for tab_data in self._tabs.values():
                tab_data["cmd_combo"].removeItem(cmd_to_delete)
            self._save_commands()

    def _load_commands(self):
        self._commands = []
        if os.path.exists(COMMANDS_FILE):
            try:
                with open(COMMANDS_FILE, "r") as f:
                    for line in f:
                        cmd = line.strip()
                        if cmd and cmd not in self._commands:
                            self._commands.append(cmd)
                print("[Command Runner] Loaded commands from file")
            except Exception as e:
                print("[Command Runner] Error loading commands:", e)

    def _save_commands(self):
        try:
            with open(COMMANDS_FILE, "w") as f:
                for cmd in self._commands:
                    f.write(cmd + "\n")
            print("[Command Runner] Commands saved to file")
        except Exception as e:
            print("[Command Runner] Error saving commands:", e)

    def _run_command(self, tab_id):
        tab = self._tabs.get(tab_id)
        if not tab:
            return

        ansi_escape = re.compile(r'\x1b\[[0-9;]*[mK]')

        def run():
            cmd_text = tab["cmd_input"].getText().strip()
            if not cmd_text:
                return
            try:
                SwingUtilities.invokeLater(lambda: tab["output"].setText("> Running: " + cmd_text + "\n\n"))
                SwingUtilities.invokeLater(lambda: tab["run_button"].setEnabled(False))
                SwingUtilities.invokeLater(lambda: tab["cancel_button"].setEnabled(True))

                if os.name == 'nt':
                    # Windows: run command as before
                    process = subprocess.Popen(["cmd.exe", "/c", cmd_text],
                                               stdin=subprocess.PIPE,
                                               stdout=subprocess.PIPE,
                                               stderr=subprocess.STDOUT,
                                               universal_newlines=False)
                else:
                    # Unix/Linux/macOS: wrap command in `script` to simulate PTY
                    wrapped_cmd = 'script -q -c "{}" /dev/null'.format(cmd_text.replace('"', '\\"'))
                    process = subprocess.Popen(wrapped_cmd,
                                               shell=True,
                                               stdin=subprocess.PIPE,
                                               stdout=subprocess.PIPE,
                                               stderr=subprocess.STDOUT,
                                               universal_newlines=False)

                tab["process"] = process

                # --- KEY FIX: read output byte by byte, so prompts (like [Y/n]) show up instantly ---
                buffer = b""
                while True:
                    out = process.stdout.read(1)
                    if not out:
                        break
                    buffer += out
                    if out in b"\r\n":
                        line = buffer.decode('utf-8', errors='replace')
                        clean_line = ansi_escape.sub('', line)
                        SwingUtilities.invokeLater(lambda l=clean_line: tab["output"].append(l))
                        buffer = b""
                    else:
                        # If buffer contains a prompt (like '[Y/n]'), flush it for display
                        if buffer.endswith(b"[Y/n] ") or buffer.endswith(b"? "):
                            line = buffer.decode('utf-8', errors='replace')
                            clean_line = ansi_escape.sub('', line)
                            SwingUtilities.invokeLater(lambda l=clean_line: tab["output"].append(l))
                            buffer = b""

                # Flush any remaining buffer
                if buffer:
                    line = buffer.decode('utf-8', errors='replace')
                    clean_line = ansi_escape.sub('', line)
                    SwingUtilities.invokeLater(lambda l=clean_line: tab["output"].append(l))

                process.stdout.close()
                process.wait()

                status_msg = "\nCommand exited with code: {}\n".format(process.returncode)
                SwingUtilities.invokeLater(lambda: tab["output"].append(status_msg))
            except Exception as e:
                SwingUtilities.invokeLater(lambda: tab["output"].append("\nError: {}\n".format(str(e))))
            finally:
                tab["process"] = None
                SwingUtilities.invokeLater(lambda: tab["run_button"].setEnabled(True))
                SwingUtilities.invokeLater(lambda: tab["cancel_button"].setEnabled(False))

        threading.Thread(target=run).start()

    def _cancel_command(self, tab_id):
        tab = self._tabs.get(tab_id)
        if tab and tab["process"]:
            try:
                tab["process"].terminate()
                tab["output"].append("\nCommand was cancelled\n")
            except Exception as e:
                tab["output"].append("\nError cancelling command: {}\n".format(str(e)))
            finally:
                tab["process"] = None
                tab["run_button"].setEnabled(True)
                tab["cancel_button"].setEnabled(False)

    def getTabCaption(self):
        return "Command Runner"

    def getUiComponent(self):
        return self._main_panel
