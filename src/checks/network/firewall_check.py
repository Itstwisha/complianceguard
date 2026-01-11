"""
CIS macOS Benchmark - Firewall Check
Control ID: 2.1.1 - Ensure Firewall Is Enabled
"""

import subprocess
from src.checks.base_check import BaseCheck, CheckStatus, Severity


class FirewallCheck(BaseCheck):
    """Check if macOS firewall is enabled"""
    
    def __init__(self):
        super().__init__()
        self.id = "CIS-2.1.1"
        self.title = "Ensure Firewall Is Enabled"
        self.description = "The macOS Application Firewall provides protection against network-based attacks"
        self.category = "Network Security"
        self.severity = Severity.HIGH
        self.compliance_frameworks = [
            "CIS_macOS_14",
            "NIST_CSF_PR.AC-5",
            "ISO27001_A.13.1.1"
        ]
        self.remediation = """
To enable the firewall:
1. Open System Settings → Network → Firewall
2. Toggle Firewall to ON
3. Click Options to configure firewall settings
4. Or run: sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on
"""
    
    def check(self):
        """Check firewall status"""
        try:
            # Check firewall status
            result = subprocess.run(
                ['/usr/libexec/ApplicationFirewall/socketfilterfw', '--getglobalstate'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            output = result.stdout.strip().lower()
            
            if 'enabled' in output:
                # Also check stealth mode
                stealth_result = subprocess.run(
                    ['/usr/libexec/ApplicationFirewall/socketfilterfw', '--getstealthmode'],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                stealth_enabled = 'enabled' in stealth_result.stdout.lower()
                
                return {
                    'status': CheckStatus.PASS,
                    'finding': 'Firewall is enabled',
                    'evidence': {
                        'firewall_enabled': True,
                        'stealth_mode': stealth_enabled,
                        'output': result.stdout
                    },
                    'risk': 'None'
                }
            else:
                return {
                    'status': CheckStatus.FAIL,
                    'finding': 'Firewall is DISABLED',
                    'evidence': {
                        'firewall_enabled': False,
                        'output': result.stdout
                    },
                    'risk': 'System is vulnerable to network-based attacks. Unauthorized network connections can be established.'
                }
                
        except Exception as e:
            return {
                'status': CheckStatus.ERROR,
                'finding': 'Could not check firewall status',
                'evidence': {'error': str(e)},
                'risk': 'Unable to verify firewall configuration'
            }


if __name__ == "__main__":
    check = FirewallCheck()
    result = check.run()
    
    print(f"Check: {result['title']}")
    print(f"Status: {result['status']}")
    print(f"Finding: {result['finding']}")
