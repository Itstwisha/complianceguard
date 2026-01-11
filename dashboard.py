"""
ComplianceGuard - Streamlit Dashboard
"""

import streamlit as st
import sys
import os
from datetime import datetime
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.checks.system.software_updates import SoftwareUpdatesCheck
from src.checks.network.firewall_check import FirewallCheck
from src.checks.system.filevault_check import FileVaultCheck
from src.checks.access_control.screen_lock_check import ScreenLockCheck
from src.checks.network.ssh_config_check import SSHConfigCheck


# Page config
st.set_page_config(
    page_title="ComplianceGuard",
    page_icon="🛡️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .score-box {
        text-align: center;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .score-number {
        font-size: 4rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


def run_all_checks():
    """Run all security checks"""
    checks = [
        SoftwareUpdatesCheck(),
        FirewallCheck(),
        FileVaultCheck(),
        ScreenLockCheck(),
        SSHConfigCheck()
    ]
    
    results = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for idx, check in enumerate(checks):
        status_text.text(f"Running: {check.title}...")
        result = check.run()
        results.append(result)
        progress_bar.progress((idx + 1) / len(checks))
    
    status_text.empty()
    progress_bar.empty()
    
    return results


def calculate_stats(results):
    """Calculate statistics"""
    total = len(results)
    passed = sum(1 for r in results if r['status'] == 'PASS')
    failed = sum(1 for r in results if r['status'] == 'FAIL')
    warnings = sum(1 for r in results if r['status'] == 'WARNING')
    
    compliance_score = (passed / total * 100) if total > 0 else 0
    
    return {
        'total': total,
        'passed': passed,
        'failed': failed,
        'warnings': warnings,
        'compliance_score': round(compliance_score, 1)
    }


def get_status_icon(status):
    """Get emoji for status"""
    icons = {
        'PASS': '✅',
        'FAIL': '❌',
        'WARNING': '⚠️',
        'ERROR': '❓'
    }
    return icons.get(status, '❓')


def get_score_color(score):
    """Get color based on score"""
    if score >= 80:
        return "#44dd88"  # Green
    elif score >= 60:
        return "#88dd44"  # Light green
    elif score >= 40:
        return "#ffdd44"  # Yellow
    elif score >= 20:
        return "#ff9944"  # Orange
    else:
        return "#ff4444"  # Red


def main():
    """Main dashboard"""
    
    # Header
    st.markdown('<div class="main-header">🛡️ ComplianceGuard</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Security Compliance Assessment Dashboard</div>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("⚙️ Controls")
    
    if st.sidebar.button("🔍 Run Security Scan", type="primary", use_container_width=True):
        with st.spinner("Running security checks..."):
            st.session_state.scan_run = True
            st.session_state.results = run_all_checks()
            st.session_state.scan_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.info(
        "**ComplianceGuard** automatically checks your system against "
        "CIS Benchmarks and security best practices.\n\n"
        "Framework: CIS macOS Benchmark"
    )
    
    # Main content
    if not hasattr(st.session_state, 'scan_run') or not st.session_state.scan_run:
        st.info("👆 Click 'Run Security Scan' in the sidebar to start")
        
        # Show what will be checked
        st.markdown("### 📋 Security Checks")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **System Security:**
            - ✓ Software Updates
            - ✓ FileVault Encryption
            - ✓ Screen Lock Timeout
            """)
        
        with col2:
            st.markdown("""
            **Network Security:**
            - ✓ Firewall Configuration
            - ✓ SSH Configuration
            """)
        
        st.markdown("---")
        st.markdown("### 🎯 Compliance Frameworks")
        st.markdown("""
        - **CIS macOS Benchmark** - Industry-standard security configuration
        - **NIST Cybersecurity Framework** - Risk management framework
        - **ISO 27001** - Information security management
        """)
        
        return
    
    # Display results
    results = st.session_state.results
    stats = calculate_stats(results)
    
    st.success(f"✅ Scan completed at {st.session_state.scan_time}")
    
    # Compliance Score Display
    score_color = get_score_color(stats['compliance_score'])
    
    st.markdown(f"""
    <div class="score-box" style="background: linear-gradient(135deg, {score_color}22 0%, {score_color}44 100%); border: 3px solid {score_color};">
        <div style="color: #666; font-size: 1.2rem; margin-bottom: 0.5rem;">Overall Compliance Score</div>
        <div class="score-number" style="color: {score_color};">{stats['compliance_score']}%</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Top metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Checks", stats['total'])
    with col2:
        st.metric("✅ Passed", stats['passed'])
    with col3:
        st.metric("❌ Failed", stats['failed'])
    with col4:
        st.metric("⚠️ Warnings", stats['warnings'])
    
    # Results by category
    st.markdown("---")
    st.markdown("## 📊 Detailed Results")
    
    # Group by category
    categories = {}
    for result in results:
        cat = result['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(result)
    
    # Display each category
    for category, checks in categories.items():
        with st.expander(f"**{category}** ({len(checks)} checks)", expanded=True):
            for check in checks:
                status_icon = get_status_icon(check['status'])
                
                # Check header
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"### {status_icon} {check['title']}")
                    st.caption(f"`{check['id']}` | {check['description']}")
                with col2:
                    st.markdown(f"**Status:** {check['status']}")
                    
                    # Color-coded severity
                    severity_colors = {
                        'CRITICAL': '🔴',
                        'HIGH': '🟠',
                        'MEDIUM': '🟡',
                        'LOW': '🔵',
                        'INFO': '⚪'
                    }
                    severity_icon = severity_colors.get(check['severity'], '⚪')
                    st.markdown(f"**Severity:** {severity_icon} {check['severity']}")
                
                # Finding
                if check['status'] == 'PASS':
                    st.success(f"**Finding:** {check['finding']}")
                elif check['status'] == 'FAIL':
                    st.error(f"**Finding:** {check['finding']}")
                else:
                    st.warning(f"**Finding:** {check['finding']}")
                
                # Risk (only for failures)
                if check['status'] == 'FAIL' and check['risk']:
                    with st.container():
                        st.markdown("**⚠️ Risk:**")
                        st.warning(check['risk'])
                
                # Remediation (only for failures)
                if check['status'] == 'FAIL' and check['remediation']:
                    with st.container():
                        st.markdown("**🔧 Remediation:**")
                        st.info(check['remediation'])
                
                st.markdown("---")
    
    # Export options
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📥 Export Results")
    
    # Create DataFrame for export
    df = pd.DataFrame([{
        'ID': r['id'],
        'Title': r['title'],
        'Category': r['category'],
        'Status': r['status'],
        'Severity': r['severity'],
        'Finding': r['finding'],
        'Risk': r.get('risk', 'N/A')
    } for r in results])
    
    csv = df.to_csv(index=False)
    st.sidebar.download_button(
        label="📄 Download CSV Report",
        data=csv,
        file_name=f"compliance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=True
    )


if __name__ == "__main__":
    main()
