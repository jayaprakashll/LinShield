# LinShield

LinShield is an advanced Linux system hardening toolkit designed to automate security measures and improve the resilience of your Linux system. It provides a set of utilities to configure firewalls, disable unnecessary services, secure SSH configurations, and generate reports of potential vulnerabilities.

## Features

- **Automated Firewall Configuration**: Configures `ufw` with default deny-all policies and custom rules.
- **Service Optimization**: Stops and disables unnecessary services to minimize attack surfaces.
- **SSH Hardening**: Applies secure configurations to the SSH server.
- **Vulnerability Scanning**: Integrates with `lynis` for comprehensive system security audits.
- **Log and Reporting**: Generates detailed logs and summary reports for all actions performed.
- **Rollback Support**: Safely reverts changes in case of issues.

## Prerequisites

- Python 3.6+
- `ufw` (Uncomplicated Firewall)
- `lynis` (Optional, for vulnerability scans)

Install dependencies using:

```bash
sudo apt update && sudo apt install ufw lynis -y
```

## Installation

Clone the repository:

```bash
git clone https://github.com/jayaprakashll/linshield.git
cd linshield
```

## Usage

Run the toolkit with:

```bash
python3 linshield.py
```

### Actions Performed

1. Detects your Linux distribution.
2. Configures firewall rules defined in `config/default_rules.json`.
3. Stops and disables services listed as unnecessary.
4. Secures the SSH configuration based on provided settings.
5. Performs a vulnerability scan (if `lynis` is installed).
6. Generates a summary report in the `reports/` directory.

### Log Files

All actions are logged in a timestamped file under the `reports/` directory for easy tracking.

## Example Output

```plaintext
[+] Starting Advanced Linux System Hardening Toolkit
[2024-12-26 10:00:00] Toolkit Execution Start: Initiated
[2024-12-26 10:00:05] Linux Distribution Detected: Ubuntu 22.04
[2024-12-26 10:00:10] Firewall Setup: Success
[2024-12-26 10:00:15] Remove Unnecessary Services: Success
[2024-12-26 10:00:20] SSH Hardening: Success
[2024-12-26 10:00:30] Vulnerability Scan: Completed
[2024-12-26 10:00:35] Toolkit Execution End: Completed
[+] Hardening Completed. Logs saved at: reports/report_20241226_100000.log
```

## Contributing

Contributions are welcome! Feel free to fork the repository and submit a pull request.

