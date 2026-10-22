import subprocess
def check_sudo_permissions():
    """Check cached sudo privileges without prompting."""
    try:
        result = subprocess.run(
            ["sudo", "-n", "-l"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False
        )
        return {
            "return_code": result.returncode,
            "output": result.stdout.strip(),
            "error": result.stderr.strip()
        }
    except subprocess.TimeoutExpired:
        return {
            "return_code": -1,
            "output": "",
            "error": "Sudo check timed out."
        }
    except OSError as error:
        return {
            "return_code": -1,
            "output": "",
            "error": str(error)
        }
def display_results(result):
    print("\n===== SUDO CONFIGURATION ANALYSIS =====")
    if result["return_code"] == 0:
        print("Sudo permissions retrieved successfully.")
        if result["output"]:
            print("\n" + result["output"])
        if "NOPASSWD:" in result["output"]:
            print("\nReview: NOPASSWD rule detected.")
        else:
            print("\nNo NOPASSWD rule detected in output.")
    else:
        print("Sudo permissions could not be retrieved.")
        if result["error"]:
            print("Details:", result["error"])
        print("This does not confirm that sudo access is absent.")
if __name__ == "__main__":
    result = check_sudo_permissions()
    display_results(result)
