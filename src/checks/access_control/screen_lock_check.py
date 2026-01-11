"""
CIS macOS Benchmark - Screen Lock Check
Control ID: 5.9 - Ensure Screen Lock Timeout is Set
"""

import subprocess
from src.checks.base_check import BaseCheck, CheckStatus, Severity


class ScreenLockCheck(BaseCheck):
    """Check if screen lock timeout is configured"""
    
    def __init__(self):
        super().__init__()
        self.id = "CIS-5.9"
        self.title = "Ensure Screen Lock Timeout is Set to 20 Minutes or Less"
        self.description = "Automatic screen lock prevents unauthorized access when user is away"
        self.category = "Access Control"
        self.severity = Severity.MEDIUM
        self.compliance_frameworks = [
            "CIS_macOS_14",
            "NIST_CSF_PR.AC-7",
            "ISO27001_A.11.2.8"
        ]
        self.remediation = """
To configure screen lock:
1. Open System Settings → Lock Screen
2. Set "Start Screen Saver when inactive" to 20 minutes or less
3. Enable "Require password after screen saver begins"
4. Set password requirement to "immediately"
"""
    
    def check(self):
        """Check screen lock timeout settings"""
        try:
            # Check screen saver idle time (in seconds)
            result = subprocess.run(
                ['defaults', 'read', 'com.apple.screensaver', 'idleTime'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                idle_seconds = int(result.stdout.strip())
                idle_minutes = idle_seconds / 60
                
                # CIS recommends 20 minutes or less (1200 seconds)
                if idle_seconds > 0 and idle_seconds <= 1200:
                    return {
                        'status': CheckStatus.PASS,
                        'finding': f'Screen lock timeout is set to {idle_minutes:.0f} minutes (within recommended 20 minutes)',
                        'evidence': {
                            'timeout_seconds': idle_seconds,
                            'timeout_minutes': idle_minutes,
                            'recommended_max': 20
                        },
                        'risk': 'None'
                    }
                elif idle_seconds > 1200:
                    return {
                        'status': CheckStatus.FAIL,
                        'finding': f'Screen lock timeout is {idle_minutes:.0f} minutes (exceeds recommended 20 minutes)',
                        'evidence': {
                            'timeout_seconds': idle_seconds,
                            'timeout_minutes': idle_minutes,
                            'recommended_max': 20
                        },
                        'risk': 'Extended timeout increases risk of unauthorized access if user leaves workstation unattended'
                    }
                else:
                    return {
                        'status': CheckStatus.FAIL,
                        'finding': 'Screen lock timeout is not configured (set to 0 or never)',
                        'evidence': {
                            'timeout_seconds': idle_seconds,
                            'configured': False
                        },
                        'risk': 'HIGH - Screen will never lock automatically, allowing unauthorized access'
                    }
            else:
                # Setting not found - might be default or not configured
                return {
                    'status': CheckStatus.WARNING,
                    'finding': 'Screen lock timeout setting not found (may be using system default)',
                    'evidence': {
                        'configured': False,
                        'error': result.stderr
                    },
                    'risk': 'Unclear - unable to verify timeout configuration'
                }
                
        except ValueError:
            return {
                'status': CheckStatus.ERROR,
                'finding': 'Could not parse screen lock timeout value',
                'evidence': {'error': 'Invalid timeout value'},
                'risk': 'Unable to verify screen lock configuration'
            }
        except Exception as e:
            return {
                'status': CheckStatus.ERROR,
                'finding': 'Could not check screen lock timeout',
                'evidence': {'error': str(e)},
                'risk': 'Unable to verify screen lock configuration'
            }


if __name__ == "__main__":
    check = ScreenLockCheck()
    result = check.run()
    
    print(f"Check: {result['title']}")
    print(f"Status: {result['status']}")
    print(f"Finding: {result['finding']}")
