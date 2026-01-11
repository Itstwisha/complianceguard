"""
Base class for all security checks
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime
from enum import Enum


class CheckStatus(Enum):
    """Status of a security check"""
    PASS = "PASS"
    FAIL = "FAIL"
    WARNING = "WARNING"
    ERROR = "ERROR"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class Severity(Enum):
    """Severity levels for findings"""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


class BaseCheck(ABC):
    """
    Base class for all security compliance checks
    
    All checks must inherit from this class and implement the check() method
    """
    
    def __init__(self):
        self.id: str = ""
        self.title: str = ""
        self.description: str = ""
        self.category: str = ""
        self.severity: Severity = Severity.MEDIUM
        self.compliance_frameworks: list = []
        self.remediation: str = ""
    
    @abstractmethod
    def check(self) -> Dict[str, Any]:
        """
        Perform the security check
        
        Returns:
            Dictionary with check results:
            {
                'status': CheckStatus,
                'finding': str (description of finding),
                'evidence': Any (supporting data),
                'risk': str (risk explanation),
                'remediation': str (how to fix)
            }
        """
        pass
    
    def run(self) -> Dict[str, Any]:
        """
        Execute the check and return formatted result
        
        Returns:
            Complete check result with metadata
        """
        try:
            result = self.check()
            
            return {
                'id': self.id,
                'title': self.title,
                'description': self.description,
                'category': self.category,
                'severity': self.severity.value,
                'compliance_frameworks': self.compliance_frameworks,
                'status': result.get('status', CheckStatus.ERROR).value,
                'finding': result.get('finding', 'No finding recorded'),
                'evidence': result.get('evidence'),
                'risk': result.get('risk', ''),
                'remediation': result.get('remediation', self.remediation),
                'timestamp': datetime.now().isoformat(),
                'error': None
            }
            
        except Exception as e:
            return {
                'id': self.id,
                'title': self.title,
                'description': self.description,
                'category': self.category,
                'severity': self.severity.value,
                'status': CheckStatus.ERROR.value,
                'finding': 'Check execution failed',
                'evidence': None,
                'risk': '',
                'remediation': '',
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            }
    
    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.id} - {self.title}>"
