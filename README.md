# AltA2DP Driver Patcher

## Overview

This Python script automates the patching of the Alternative A2DP Driver for Windows, modifying both `AltA2dpConfig.exe` and `AltA2DP.sys` to achieve a specific modification (e.g., bypassing a check).

**Disclaimer:** Modifying system files can be risky. Use this script at your own risk. Always back up your system before running any patching tools. The author(s) are not responsible for any damage caused by the use of this script.

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

*   **Python 3.x:** You need Python 3 installed on your system. You can download it from [https://www.python.org/downloads/](https://www.python.org/downloads/)
*   **Original Driver Files:** The script must be run in the root installation directory of the Alternative A2DP Driver.

## Installation

1.  **Download:** Download the `patcher.py` script.
2.  **Locate Driver Installation Folder:** Find the root installation directory of the Alternative A2DP Driver. This is typically `C:\Program Files\Luculent Systems\AltA2DP`.
3.  **Place Script:** Place the `patcher.py` script in the root directory (e.g., `C:\Program Files\Luculent Systems\AltA2DP`).

## Usage

1.  **Run as Administrator:** Right-click on `patcher.py` and select "Run as administrator". Administrator privileges are required to modify system files.
2.  **Follow the Prompts:** The script will guide you through the process. If existing `.bak` files are found, you will be prompted to restore, skip, or abort.
3.  **Verify:** After the script completes, check the output to confirm that the files were patched successfully.

## How to Restore the Original Driver

If something goes wrong or you want to revert the changes, you can restore the original driver from the backup files:

1.  Locate the `.bak` files in the installation directory (e.g., `AltA2dpConfig.exe.bak` and `AltA2DP.sys.bak` in the `Driver` subfolder).
2.  Delete the original files (`AltA2dpConfig.exe` and `AltA2DP.sys`).
3.  Rename the `.bak` files to remove the `.bak` extension. For example, rename `AltA2dpConfig.exe.bak` to `AltA2dpConfig.exe`.

## Troubleshooting

*   **"Permission denied" error:** This means you are not running the script as an administrator. Right-click on `patcher.py` and select "Run as administrator".
*   **"Signature not found" error:** This indicates that the script could not find the expected code pattern in the file. This can happen if:
    *   The original files have already been patched. Try restoring from the `.bak` files first.
    *   You are using a different version of the Alternative A2DP Driver than the script is designed for.
*   **Script does not create .bak file** - This is due to a permission error where the script lacks access to create files in the installation directory. Running as an admin will usually resolve this issue.

## Signature Information

The script uses the following AOB signatures to locate the code to be patched:

*   **AltA2dpConfig.exe:** `41 83 F9 07 0F 87 ?? ?? ?? ??`
*   **AltA2DP.sys:** `33 D2 48 8B CB E8 ?? ?? ?? ?? 83 F8 06`

The patch data and offsets are embedded within the script.

## License

This project is provided under the MIT License. See the `LICENSE` file for details. (You can create a LICENSE file if you wish).

## Credits

*   This script was developed by \[Your Name/Nickname]
*   Reverse engineering and signature research: \[Your Name/Nickname]
*   Special thanks to \[Anyone who helped you]

## Support

For questions or issues, please open an issue on \[Your GitHub/Forum Link (Optional)]
