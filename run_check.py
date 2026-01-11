#!/usr/bin/env python3
"""
Helper script to run individual checks
"""

import sys
import os

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.checks.system.software_updates import SoftwareUpdatesCheck
from src.checks.network.firewall_check import FirewallCheck
from src.checks.system.filevault_check import FileVaultCheck
from src.checks.access_control.screen_lock_check import ScreenLockCheck
from src.checks.network.ssh_config_check import SSHConfigCheck


def run_single_check(check_name):
    """Run a single check by name"""
    checks = {
        'updates': SoftwareUpdatesCheck,
        'firewall': FirewallCheck,
        'filevault': FileVaultCheck,
        'screenlock': ScreenLockCheck,
        'ssh': SSHConfigCheck
    }
    
    if check_name not in checks:
        print(f"Unknown check: {check_name}")
        print(f"Available checks: {', '.join(checks.keys())}")
        return
    
    check_class = checks[check_name]
    check = check_class()
    result = check.run()
    
    print("="*60)
    print(f"Check: {result['title']}")
    print(f"ID: {result['id']}")
    print(f"Category: {result['category']}")
    print(f"Severity: {result['severity']}")
    print("="*60)
    print(f"Status: {result['status']}")
    print(f"Finding: {result['finding']}")
    print(f"Evidence: {result['evidence']}")
    print(f"Risk: {result['risk']}")
    print("="*60)
    
    if result['remediation']:
        print(f"\nRemediation:\n{result['remediation']}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 run_check.py <check_name>")
        print("\nAvailable checks:")
        print("  updates    - Software Updates Check")
        print("  firewall   - Firewall Status Check")
        print("  filevault  - FileVault Encryption Check")
        print("  screenlock - Screen Lock Timeout Check")
        print("  ssh        - SSH Configuration Check")
        sys.exit(1)
    
    check_name = sys.argv[1].lower()
    run_single_check(check_name)
