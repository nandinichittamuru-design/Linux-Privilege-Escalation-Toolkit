import os
import stat
def scan_file_permissions(directory="/usr/bin"):
    """Identify world-writable regular files."""
    findings = []
    errors = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            try:
                file_info = os.stat(
                    file_path,
                    follow_symlinks=False
                )
                if not stat.S_ISREG(file_info.st_mode):
                    continue
                if file_info.st_mode & stat.S_IWOTH:
                    findings.append({
                        "path": file_path,
                        "permissions": stat.filemode(
                            file_info.st_mode
                        )
                    })
            except OSError as error:
                errors.append(str(error))
    return findings, errors
def display_results(findings, errors):
    print("\n===== FILE PERMISSION ANALYSIS =====")
    if findings:
        for item in findings:
            print(
                f"{item['permissions']}  {item['path']}"
            )
    else:
        print("No world-writable files found.")
    print(f"\nTotal findings: {len(findings)}")
    if errors:
        print(f"Files not inspected: {len(errors)}")
if __name__ == "__main__":
    findings, errors = scan_file_permissions(
        "/usr/bin"
    )
    display_results(findings, errors)
