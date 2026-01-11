"""
CIS macOS Benchmark - SSH Configuration Check
Control ID: 4.2 - Ensure SSH Configuration is Secure
"""

import subprocess
import os
from src.checks.base_check import BaseCheck, CheckStatus, Severity


class SSHConfigCheck(BaseCheck):
    """Check SSH configuration for security best practices"""
    
    def __init__(self):
        super().__init__()
        self.id = "CIS-4.2"
        self.title = "Ensure SSH Server Is Configured Securely"
        self.description = "SSH should be disabled if not needed, or configured securely if required"
        self.category = "Network Security"
        self.severity = Severity.HIGH
        self.compliance_frameworks = [
            "CIS_macOS_14",
            "NIST_CSF_PR.AC-4",
            "ISO27001_A.13.1.1"
        ]
        self.remediation = """
To secure or disable SSH:
1. If SSH not needed: System Settings → General → Sharing → Remote Login OFF
2. If SSH needed, configure /etc/ssh/sshd_config:
   - PermitRootLogin no
   - PasswordAuthentication no (use keys only)
   - PermitEmptyPasswords no
   - Protocol 2
3. Restart SSH: sudo launchctl unload -w /System/Library/LaunchDaemons/ssh.plist
"""
    
    def check(self):
        """Check SSH service and configuration"""
        try:
            # Check if SSH (Remote Login) is enabled
            result = subprocess.run(
                ['sudo', 'systemsetup', '-getremotelogin'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            ssh_enabled = 'On' in result.stdout
            
            if not ssh_enabled:
                return {
                    'status': CheckStatus.PASS,
                    'finding': 'SSH Remote Login is disabled (recommended if not needed)',
                    'evidence': {
                        'ssh_enabled': False,
                        'status': result.stdout.strip()
                    },
                    'risk': 'None'
                }
            
            # SSH is enabled - check configuration
            issues = []
            config_path = '/etc/ssh/sshd_config'
            
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config_content = f.read()
                
                # Check for insecure settings
                if 'PermitRootLogin yes' in config_content:
                    issues.append('Root login is permitted')
                
                if 'PasswordAuthentication yes' in config_content:
                    issues.append('Password authentication is enabled (keys recommended)')
                
                if 'PermitEmptyPasswords yes' in config_content:
                    issues.append('Empty passwords are permitted')
                
                if issues:
                    return {
                        'status': CheckStatus.FAIL,
                        'finding': f'SSH is enabled with {len(issues)} security issue(s)',
                        'evidence': {
                            'ssh_enabled': True,
                            'issues': issues,
                            'config_checked': True
                        },
                        'risk': 'SSH configuration allows insecure practices that could lead to unauthorized access'
                    }
                else:
                    return {
                        'status': CheckStatus.PASS,
                        'finding': 'SSH is enabled with secure configuration',
                        'evidence': {
                            'ssh_enabled': True,
                            'issues': [],
                            'config_checked': True
                        },
                        'risk': 'Low - SSH is configured with security best practices'
                    }
            else:
                return {
                    'status': CheckStatus.WARNING,
                    'finding': 'SSH is enabled but configuration file not found',
                    'evidence': {
                        'ssh_enabled': True,
                        'config_path': config_path,
                        'config_found': False
                    },
                    'risk': 'Unable to verify SSH security configuration'
                }
                
        except PermissionError:
            return {
                'status': CheckStatus.WARNING,
                'finding': 'Insufficient permissions to check SSH configuration (needs sudo)',
                'evidence': {'error': 'Permission denied'},
                'risk': 'Unable to verify SSH security configuration'
            }
        except Exception as e:
            return {
                'status': CheckStatus.ERROR,
                'finding': 'Could not check SSH configuration',
                'evidence': {'error': str(e)},
                'risk': 'Unable to verify SSH security'
            }


if __name__ == "__main__":
    check = SSHConfigCheck()
    result = check.run()
    
    print(f"Check: {result['title']}")
    print(f"Status: {result['status']}")
    print(f"Finding: {result['finding']}")
