import os
import subprocess
def run_command(command):
    """Execute a read-only Linux command."""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=15,
            check=False
        )
        return (
            result.stdout.strip(),
            result.stderr.strip(),
            result.returncode
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        return "", str(error), -1
def analyze_cron_jobs():
    print("\n===== CRON JOB ANALYSIS =====")
    output, error, code = run_command(
        ["crontab", "-l"]
    )
    print("\nCurrent User Cron Jobs:")
    if code == 0:
        print(output if output else "No entries found.")
    else:
        print(error or "Unable to retrieve cron jobs.")
    print("\nSystem-Wide Cron Configuration:")
    cron_file = "/etc/crontab"
    try:
        with open(cron_file, "r") as file:
            print(file.read().strip())
    except (OSError, UnicodeError) as error:
        print(f"Unable to read {cron_file}: {error}")
    print("\nCron Directories:")
    for directory in [
        "/etc/cron.d",
        "/etc/cron.daily",
        "/etc/cron.hourly",
        "/etc/cron.weekly",
        "/etc/cron.monthly"
    ]:
        if os.path.isdir(directory):
            print(f"\n{directory}")
            try:
                for filename in sorted(os.listdir(directory)):
                    print(" -", filename)
            except OSError as error:
                print("Access error:", error)
def analyze_services():
    print("\n===== SYSTEM SERVICE ANALYSIS =====")
    output, error, code = run_command([
        "systemctl",
        "list-units",
        "--type=service",
        "--state=running",
        "--no-pager",
        "--no-legend"
    ])
    if code == 0:
        print(output if output else "No running services found.")
    else:
        print(error or "Unable to retrieve services.")
if __name__ == "__main__":
    analyze_cron_jobs()
    analyze_services()
