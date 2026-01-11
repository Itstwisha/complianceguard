#!/usr/bin/env python3
"""
Test all implemented security checks
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
from rich.console import Console
from rich.table import Table


def main():
    """Run all checks and display results"""
    console = Console()
    
    console.print("\n[bold blue]ComplianceGuard - Running All Checks[/bold blue]\n")
    
    # List of all checks
    checks = [
        SoftwareUpdatesCheck(),
        FirewallCheck(),
        FileVaultCheck(),
        ScreenLockCheck(),
        SSHConfigCheck()
    ]
    
    results = []
    
    # Run each check
    for check in checks:
        console.print(f"🔍 Running: [bold]{check.title}[/bold]")
        result = check.run()
        results.append(result)
        
        # Display status
        status = result['status']
        if status == 'PASS':
            console.print(f"   ✅ {status}: {result['finding']}\n")
        elif status == 'FAIL':
            console.print(f"   ❌ {status}: {result['finding']}\n")
        elif status == 'WARNING':
            console.print(f"   ⚠️  {status}: {result['finding']}\n")
        else:
            console.print(f"   ❓ {status}: {result['finding']}\n")
    
    # Summary table
    console.print("\n[bold]Summary:[/bold]\n")
    
    table = Table(show_header=True, header_style="bold")
    table.add_column("ID", style="cyan")
    table.add_column("Check", style="white")
    table.add_column("Status", style="white")
    table.add_column("Severity", style="yellow")
    
    pass_count = 0
    fail_count = 0
    warning_count = 0
    
    for result in results:
        status = result['status']
        if status == 'PASS':
            status_display = "✅ PASS"
            pass_count += 1
        elif status == 'FAIL':
            status_display = "❌ FAIL"
            fail_count += 1
        elif status == 'WARNING':
            status_display = "⚠️  WARN"
            warning_count += 1
        else:
            status_display = "❓ ERROR"
        
        table.add_row(
            result['id'],
            result['title'][:50] + "..." if len(result['title']) > 50 else result['title'],
            status_display,
            result['severity']
        )
    
    console.print(table)
    
    # Statistics
    total = len(results)
    console.print(f"\n[bold]Results:[/bold]")
    console.print(f"  Total Checks: {total}")
    console.print(f"  ✅ Passed: {pass_count}")
    console.print(f"  ❌ Failed: {fail_count}")
    console.print(f"  ⚠️  Warnings: {warning_count}")
    
    compliance_score = (pass_count / total) * 100 if total > 0 else 0
    console.print(f"\n[bold]Compliance Score: {compliance_score:.1f}%[/bold]\n")


if __name__ == "__main__":
    main()
