import subprocess
def scan_suid_sgid(directory="/usr/bin"):
    """Find files with SUID or SGID permissions."""
    command = [
        "find",
        directory,
        "-type", "f",
        "-perm", "/6000"
    ]
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False
        )
        files = sorted(
            line.strip()
            for line in result.stdout.splitlines()
            if line.strip()
        )
        return files, result.stderr.strip()
    except OSError as error:
        return [], str(error)
def display_results(files, errors=""):
    print("\n===== SUID AND SGID FILE SCAN =====")
    if files:
        for file_path in files:
            print(file_path)
        print(f"\nTotal files found: {len(files)}")
    else:
        print("No matching files found.")
    if errors:
        print("\nScan warning:", errors)
if __name__ == "__main__":
    files, errors = scan_suid_sgid()
    display_results(files, errors)
