"""
CIS macOS Benchmark - FileVault Disk Encryption Check
Control ID: 2.6.1 - Ensure FileVault Is Enabled
"""

import subprocess
from src.checks.base_check import BaseCheck, CheckStatus, Severity


class FileVaultCheck(BaseCheck):
    """Check if FileVault disk encryption is enabled"""
    
    def __init__(self):
        super().__init__()
        self.id = "CIS-2.6.1"
        self.title = "Ensure FileVault Is Enabled"
        self.description = "FileVault provides full disk encryption to protect data at rest"
        self.category = "Data Protection"
        self.severity = Severity.CRITICAL
        self.compliance_frameworks = [
            "CIS_macOS_14",
            "NIST_CSF_PR.DS-1",
            "ISO27001_A.10.1.1",
            "PCI_DSS_3.4"
        ]
        self.remediation = """
To enable FileVault:
1. Open System Settings → Privacy & Security → FileVault
2. Click "Turn On FileVault"
3. Save recovery key in a secure location
4. Restart the system to begin encryption
5. Or run: sudo fdesetup enable
"""
    
    def check(self):
        """Check FileVault encryption status"""
        try:
            # Check FileVault status
            result = subprocess.run(
                ['fdesetup', 'status'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            output = result.stdout.strip()
            
            if 'FileVault is On' in output:
                return {
                    'status': CheckStatus.PASS,
                    'finding': 'FileVault disk encryption is enabled',
                    'evidence': {
                        'filevault_enabled': True,
                        'status': output
                    },
                    'risk': 'None'
                }
            elif 'FileVault is Off' in output:
                return {
                    'status': CheckStatus.FAIL,
                    'finding': 'FileVault disk encryption is DISABLED',
                    'evidence': {
                        'filevault_enabled': False,
                        'status': output
                    },
                    'risk': 'CRITICAL - Data at rest is not encrypted. If device is lost or stolen, all data is accessible.'
                }
            elif 'Encryption in progress' in output:
                return {
                    'status': CheckStatus.WARNING,
                    'finding': 'FileVault encryption is in progress',
                    'evidence': {
                        'filevault_enabled': True,
                        'encryption_in_progress': True,
                        'status': output
                    },
                    'risk': 'Low - Encryption is being applied but not yet complete'
                }
            else:
                return {
                    'status': CheckStatus.WARNING,
                    'finding': 'FileVault status unclear',
                    'evidence': {
                        'status': output
                    },
                    'risk': 'Unable to determine encryption status'
                }
                
        except Exception as e:
            return {
                'status': CheckStatus.ERROR,
                'finding': 'Could not check FileVault status',
                'evidence': {'error': str(e)},
                'risk': 'Unable to verify disk encryption'
            }


if __name__ == "__main__":
    check = FileVaultCheck()
    result = check.run()
    
    print(f"Check: {result['title']}")
    print(f"Status: {result['status']}")
    print(f"Finding: {result['finding']}")
