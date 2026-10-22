import io
from contextlib import redirect_stdout
from modules.system_info import collect_system_info
from modules.suid_sgid_scan import scan_suid_sgid
from modules.file_permission_analysis import scan_file_permissions
from modules.sudo_check import check_sudo_permissions
from modules.cron_service_analysis import (
    analyze_cron_jobs,
    analyze_services
)
from reports.report_generator import generate_report
def capture_output(function):
    """Collect output printed by a module."""
    buffer = io.StringIO()
    try:
        with redirect_stdout(buffer):
            function()
        return buffer.getvalue().strip()
    except Exception as error:
        return f"Module error: {error}"
def main():
    print("=" * 50)
    print("LINUX PRIVILEGE ESCALATION AUTOMATION TOOLKIT")
    print("=" * 50)
    findings = {}
    print("\n[1/6] System Information Collection")
    try:
        findings["System Information"] = collect_system_info()
    except Exception as error:
        findings["System Information"] = {"error": str(error)}
    print("[2/6] SUID and SGID File Detection")
    try:
        files, warning = scan_suid_sgid("/usr/bin")
        findings["SUID and SGID File Detection"] = {
            "directory": "/usr/bin",
            "files": files,
            "total": len(files),
            "warning": warning
        }
    except Exception as error:
        findings["SUID and SGID File Detection"] = {
            "error": str(error)
        }
    print("[3/6] File Permission Analysis")
    try:
        files, errors = scan_file_permissions("/usr/bin")
        findings["File Permission Analysis"] = {
            "directory": "/usr/bin",
            "world_writable_files": files,
            "total": len(files),
            "errors": errors
        }
    except Exception as error:
        findings["File Permission Analysis"] = {
            "error": str(error)
        }
    print("[4/6] Sudo Configuration Analysis")
    try:
        findings["Sudo Configuration Analysis"] = (
            check_sudo_permissions()
        )
    except Exception as error:
        findings["Sudo Configuration Analysis"] = {
            "error": str(error)
        }
    print("[5/6] Cron Job and Service Analysis")
    findings["Cron Job Analysis"] = capture_output(
        analyze_cron_jobs
    )
    findings["Service Analysis"] = capture_output(
        analyze_services
    )
    print("[6/6] Security Report Generation")
    try:
        txt_file, json_file = generate_report(findings)
        print("\n===== SCAN COMPLETED =====")
        print("Text Report:", txt_file)
        print("JSON Report:", json_file)
    except Exception as error:
        print("Report generation error:", error)
if __name__ == "__main__":
    main()

