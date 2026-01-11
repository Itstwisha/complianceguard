"""
CIS macOS Benchmark - Software Updates Check
Control ID: 1.1 - Ensure All Apple-Provided Software Is Current
"""

import subprocess
from src.checks.base_check import BaseCheck, CheckStatus, Severity


class SoftwareUpdatesCheck(BaseCheck):
    """Check if macOS software updates are current"""
    
    def __init__(self):
        super().__init__()
        self.id = "CIS-1.1"
        self.title = "Ensure All Apple-Provided Software Is Current"
        self.description = "Software updates often contain security patches for vulnerabilities"
        self.category = "System Updates"
        self.severity = Severity.HIGH
        self.compliance_frameworks = [
            "CIS_macOS_14",
            "NIST_CSF_PR.IP-12",
            "ISO27001_A.12.6.1"
        ]
        self.remediation = """
To install updates:
1. Open System Settings → General → Software Update
2. Install all available updates
3. Or run: sudo softwareupdate -ia --restart
4. Enable automatic updates for security patches
"""
    
    def check(self):
        """Check for available software updates"""
        try:
            # Check for available updates
            result = subprocess.run(
                ['softwareupdate', '-l'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            output = result.stdout.lower()
            
            # Check if system is up to date
            if "no new software available" in output or "no updates available" in output:
                return {
                    'status': CheckStatus.PASS,
                    'finding': 'System is up to date - no pending updates',
                    'evidence': {
                        'updates_available': 0,
                        'output': result.stdout[:200]
                    },
                    'risk': 'None'
                }
            
            # Parse available updates
            updates = self._parse_updates(result.stdout)
            
            # Check if there are recommended/security updates
            has_security_updates = any('security' in u.lower() for u in updates)
            
            if has_security_updates:
                severity_msg = "CRITICAL - Security updates available"
            else:
                severity_msg = f"{len(updates)} update(s) available"
            
            return {
                'status': CheckStatus.FAIL,
                'finding': severity_msg,
                'evidence': {
                    'updates_available': len(updates),
                    'updates': updates[:5],  # Show first 5
                    'has_security_updates': has_security_updates
                },
                'risk': 'Outdated software may contain known vulnerabilities that can be exploited by attackers'
            }
            
        except subprocess.TimeoutExpired:
            return {
                'status': CheckStatus.ERROR,
                'finding': 'Software update check timed out',
                'evidence': {'error': 'Command timeout after 30 seconds'},
                'risk': 'Unable to verify update status'
            }
        except Exception as e:
            return {
                'status': CheckStatus.ERROR,
                'finding': 'Could not check software updates',
                'evidence': {'error': str(e)},
                'risk': 'Unable to verify update status'
            }
    
    def _parse_updates(self, output: str) -> list:
        """Parse update list from softwareupdate output"""
        updates = []
        lines = output.split('\n')
        
        for line in lines:
            line = line.strip()
            # Look for lines with asterisk (update entries)
            if line.startswith('*') or line.startswith('Label:'):
                # Extract update name
                if ':' in line:
                    update_name = line.split(':', 1)[1].strip()
                else:
                    update_name = line.lstrip('* ').strip()
                
                if update_name:
                    updates.append(update_name)
        
        return updates


if __name__ == "__main__":
    # Test this check
    check = SoftwareUpdatesCheck()
    result = check.run()
    
    print(f"Check: {result['title']}")
    print(f"Status: {result['status']}")
    print(f"Finding: {result['finding']}")
    print(f"Evidence: {result['evidence']}")
