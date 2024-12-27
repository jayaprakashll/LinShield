import os
import subprocess
import platform
import datetime
import json
from pathlib import Path
from tkinter import Tk, Button, Label, Text, Scrollbar, END, filedialog, messagebox

# Global Variables
LOG_DIR = "reports"
CONFIG_DIR = "config"
DEFAULT_RULES_FILE = os.path.join(CONFIG_DIR, "default_rules.json")
LOG_FILE = os.path.join(LOG_DIR, f"report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

# Create necessary directories
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(CONFIG_DIR, exist_ok=True)

# Load default rules
default_rules = {
    "unnecessary_services": ["ftp", "telnet", "samba"],
    "ssh_hardening": {
        "PermitRootLogin": "no",
        "PasswordAuthentication": "no"
    },
    "firewall_rules": [
        {"action": "allow", "port": "22"},
        {"action": "deny", "port": "80"}
    ]
}
if not Path(DEFAULT_RULES_FILE).exists():
    with open(DEFAULT_RULES_FILE, "w") as f:
        json.dump(default_rules, f, indent=4)

def log_action(action, status):
    """Log actions and their status to a log file."""
    with open(LOG_FILE, "a") as log:
        log.write(f"[{datetime.datetime.now()}] {action}: {status}\n")

def display_log(log_display):
    """Display log content in the GUI."""
    log_display.delete(1.0, END)
    try:
        with open(LOG_FILE, "r") as log:
            log_display.insert(END, log.read())
    except FileNotFoundError:
        log_display.insert(END, "No logs available.")

def setup_firewall():
    """Automate firewall setup."""
    try:
        with open(DEFAULT_RULES_FILE) as f:
            rules = json.load(f)
        subprocess.run(['sudo', 'ufw', 'reset'], check=True)
        subprocess.run(['sudo', 'ufw', 'default', 'deny', 'incoming'], check=True)
        subprocess.run(['sudo', 'ufw', 'default', 'allow', 'outgoing'], check=True)
        for rule in rules["firewall_rules"]:
            action = rule["action"]
            port = rule["port"]
            subprocess.run(['sudo', 'ufw', action, port], check=True)
        subprocess.run(['sudo', 'ufw', 'enable'], check=True)
        log_action("Firewall Setup", "Success")
        messagebox.showinfo("Success", "Firewall setup completed successfully.")
    except Exception as e:
        log_action("Firewall Setup", f"Failed - {e}")
        messagebox.showerror("Error", f"Firewall setup failed: {e}")

def remove_unnecessary_services():
    """Disable unnecessary services."""
    try:
        with open(DEFAULT_RULES_FILE) as f:
            rules = json.load(f)
        for service in rules["unnecessary_services"]:
            subprocess.run(['sudo', 'systemctl', 'stop', service], stderr=subprocess.PIPE)
            subprocess.run(['sudo', 'systemctl', 'disable', service], stderr=subprocess.PIPE)
        log_action("Remove Unnecessary Services", "Success")
        messagebox.showinfo("Success", "Unnecessary services removed successfully.")
    except Exception as e:
        log_action("Remove Unnecessary Services", f"Failed - {e}")
        messagebox.showerror("Error", f"Failed to remove services: {e}")

def secure_ssh():
    """Harden SSH configurations."""
    try:
        with open(DEFAULT_RULES_FILE) as f:
            rules = json.load(f)
        ssh_config_path = "/etc/ssh/sshd_config"
        with open(ssh_config_path, "r") as file:
            lines = file.readlines()
        with open(ssh_config_path, "w") as file:
            for line in lines:
                for key, value in rules["ssh_hardening"].items():
                    if line.startswith(key):
                        line = f"{key} {value}\n"
                file.write(line)
        subprocess.run(['sudo', 'systemctl', 'restart', 'ssh'], check=True)
        log_action("SSH Hardening", "Success")
        messagebox.showinfo("Success", "SSH configuration hardened successfully.")
    except Exception as e:
        log_action("SSH Hardening", f"Failed - {e}")
        messagebox.showerror("Error", f"SSH hardening failed: {e}")

def backup_configuration():
    """Backup current configuration to a file."""
    try:
        backup_file = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")],
            title="Save Backup File"
        )
        if not backup_file:
            return  # User canceled the save dialog

        with open(DEFAULT_RULES_FILE, "r") as config_file:
            config_data = json.load(config_file)

        with open(backup_file, "w") as backup:
            json.dump(config_data, backup, indent=4)

        log_action("Backup Configuration", "Success")
        messagebox.showinfo("Success", "Configuration backup completed successfully.")
    except Exception as e:
        log_action("Backup Configuration", f"Failed - {e}")
        messagebox.showerror("Error", f"Failed to backup configuration: {e}")

def restore_configuration():
    """Restore configuration from a backup file."""
    try:
        backup_file = filedialog.askopenfilename(
            filetypes=[("JSON Files", "*.json")],
            title="Select Backup File"
        )
        if not backup_file:
            return  # User canceled the open dialog

        with open(backup_file, "r") as backup:
            config_data = json.load(backup)

        with open(DEFAULT_RULES_FILE, "w") as config_file:
            json.dump(config_data, config_file, indent=4)

        log_action("Restore Configuration", "Success")
        messagebox.showinfo("Success", "Configuration restored successfully.")
    except Exception as e:
        log_action("Restore Configuration", f"Failed - {e}")
        messagebox.showerror("Error", f"Failed to restore configuration: {e}")

def generate_report():
    """Generate a summary report."""
    try:
        with open(LOG_FILE, "r") as log:
            report = log.read()
        messagebox.showinfo("Report", report)
    except FileNotFoundError:
        messagebox.showwarning("Warning", "No logs available to generate report.")

def main_gui():
    """Main GUI function."""
    root = Tk()
    root.title("Linux Hardening Toolkit")
    root.geometry("800x600")

    # Widgets
    Label(root, text="Linux Hardening Toolkit", font=("Arial", 20)).pack(pady=10)
    Button(root, text="Setup Firewall", command=setup_firewall, width=30).pack(pady=5)
    Button(root, text="Remove Unnecessary Services", command=remove_unnecessary_services, width=30).pack(pady=5)
    Button(root, text="Secure SSH", command=secure_ssh, width=30).pack(pady=5)
    Button(root, text="Backup Configuration", command=backup_configuration, width=30).pack(pady=5)
    Button(root, text="Restore Configuration", command=restore_configuration, width=30).pack(pady=5)
    Button(root, text="Generate Report", command=generate_report, width=30).pack(pady=5)

    Label(root, text="Logs", font=("Arial", 14)).pack(pady=10)
    log_display = Text(root, wrap="word", height=15)
    log_display.pack(expand=True, fill="both", padx=10)
    display_log(log_display)

    root.mainloop()

if __name__ == "__main__":
    main_gui()
