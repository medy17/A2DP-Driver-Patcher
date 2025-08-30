# AltA2DP Driver Patcher

## Overview

A simple AoB patcher for Alternative A2DP by Luculent. Modifies both `AltA2dpConfig.exe` and `AltA2DP.sys` to bypass license checks and make the program free to use beyond the trial period.

**Disclaimer:** I am not responsible for any corruption or fuckups you make.

## Features

*   **Automated Patching:** Simplifies the patching process, eliminating manual hex editing.
*   **Signature-Based:** Uses AOB (Array of Bytes) signatures to locate the code to be patched, making the patcher more resilient to minor driver version changes.
*   **In-Place Patching:** Patches the original files directly.
*   **Automatic Backups:** Creates `.bak` backup files before patching, allowing easy restoration.
*   **Safety Checks:**
    *   Detects existing backups and prompts the user to restore, skip, or abort to prevent accidental double-patching.
    *   Includes a check for administrator privileges and warns the user if they are not running with sufficient permissions.
*   **Error Handling:** Provides informative error messages to guide troubleshooting.
*   **Clear Output:** Displays a summary of the patching process, including successes, skips, and failures.

## Prerequisites

*   **Python 3.x:** You need Python 3 installed on your system if you will be running the python script instead of the release binary. You can download it from [https://www.python.org/downloads/](https://www.python.org/downloads/)
*   **Original Driver Files:** The script must be run in the root installation directory of the Alternative A2DP Driver.

## How to Use

### For the Release Binary (`.exe`) - Recommended Method

1.  **Download:** Go to the [Releases](https://github.com/medy17/A2DP-Driver-Patcher/releases) page and download the latest `.exe` file.
2.  2.  **Place the Patcher:** Copy the downloaded `.exe` into the root installation directory of the driver (typically `C:\Program Files\Luculent Systems\AltA2DP`).
3.  **Run as Administrator:** Right-click on the `.exe` file and select **"Run as administrator"**. This is required to modify files in the `Program Files` directory.
4.  **Follow Prompts:** The patcher will guide you through the rest of the process.

### For the Python Script (`.py`)

1.  **Prerequisites:** Ensure you have [Python 3](https://www.python.org/downloads/) installed.
2.  **Download:** Download the `patcher.py` script from the repository.
3.  **Place the Script:** Copy `patcher.py` into the driver's root installation directory.
4.  **Open an Admin Terminal:** Open Command Prompt or PowerShell **as an Administrator**.
5.  **Run the Script:** Navigate to the installation directory in the terminal and run the script using the command: `python patcher.py`

## How to Restore the Original Driver

If something goes wrong or you want to revert the changes, you can restore the original driver from the backup files:

1.  Locate the `.bak` files in the installation directory (e.g., `AltA2dpConfig.exe.bak` and `AltA2DP.sys.bak` in the `Driver` subfolder).
2.  Delete the patched files (`AltA2dpConfig.exe` and `AltA2DP.sys`).
3.  Rename the `.bak` files to remove the `.bak` extension. For example, rename `AltA2dpConfig.exe.bak` to `AltA2dpConfig.exe`.

## Troubleshooting

*   **"Permission denied" error:** This means you are not running the script as an administrator. Right-click on the binary and select "Run as administrator" or make sure the cmd window/powershell window from which you ran `patcher.py` was also ran as an administrator.
*   **"Signature not found" error:** This indicates that the script could not find the expected code pattern in the file. This can happen if:
    *   The original files have already been patched. Try restoring from the `.bak` files first.
    *   You are using a different version of the Alternative A2DP Driver than the script is designed for.
*   **Script does not create .bak file** - This is due to a permission error where the script lacks access to create files in the installation directory. Running as an admin will usually resolve this issue.

## License

This project is provided under the MIT License.

## Credits

*   This script was developed by medy17
*   Special thanks to u/Dan3436 who located the AoB a while ago. This patch simply creates and applies a more robust signature method which will work for any version of the app.

## Support

For questions or issues, please open an issue.
