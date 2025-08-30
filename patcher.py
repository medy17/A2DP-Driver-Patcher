import os
import shutil
import sys

def patch_file(target_path, signature_hex, patch_hex, patch_offset):
    """
    Searches for a signature in a target file, creates a backup, and applies a patch in-place.
    Offers to restore from backup if the file is already patched.
    """
    backup_path = target_path + ".bak"

    # --- 1. Check for existing backups (already patched?) ---
    if os.path.exists(backup_path):
        print(f"[INFO] Backup file found for {os.path.basename(target_path)}. The file is likely already patched.")
        choice = input("Choose an action: (R)estore from backup, (S)kip, (A)bort patcher: ").lower()

        if choice == 'r':
            try:
                shutil.copy2(backup_path, target_path)
                print(f"[SUCCESS] Restored original file from {os.path.basename(backup_path)}.\n")
                return "restored"
            except Exception as e:
                print(f"[ERROR] Could not restore from backup: {e}\n")
                return False
        elif choice == 's':
            print("[INFO] Skipping patch for this file.\n")
            return "skipped"
        else:
            print("[INFO] Aborting patcher as requested.\n")
            sys.exit()

    # --- 2. Check if the target file exists ---
    if not os.path.exists(target_path):
        print(f"[ERROR] Target file not found: {target_path}\n")
        return False

    print(f"--- Patching {os.path.basename(target_path)} ---")

    # --- 3. Create backup before reading/writing ---
    try:
        shutil.copy2(target_path, backup_path)
        print(f"Created backup: {os.path.basename(backup_path)}")
    except Exception as e:
        print(f"[ERROR] Could not create backup file: {e}")
        print("Please ensure you have write permissions in this directory.\n")
        return False

    # --- 4. Read the original file data ---
    try:
        with open(target_path, 'rb') as f:
            file_data = bytearray(f.read())
            print(f"Read {len(file_data)} bytes from original file.")
    except IOError as e:
        print(f"[ERROR] Could not read file: {e}\n")
        return False

    # --- (Your robust AOB scanning logic remains here, it's perfect) ---
    signature_parts = signature_hex.split(' ')
    signature_bytes = bytearray()
    wildcards = set()
    for i, part in enumerate(signature_parts):
        if part == '??': wildcards.add(i); signature_bytes.append(0)
        else: signature_bytes.append(int(part, 16))
    patch_bytes = bytearray.fromhex(patch_hex.replace(' ', ''))

    found_offset = -1
    for i in range(len(file_data) - len(signature_bytes) + 1):
        if all(file_data[i + j] == signature_bytes[j] for j in range(len(signature_bytes)) if j not in wildcards):
            found_offset = i
            break

    # --- 5. Apply the patch ---
    if found_offset != -1:
        print(f"[SUCCESS] Signature found at offset: {hex(found_offset)}")
        patch_location = found_offset + patch_offset
        original_bytes = file_data[patch_location:patch_location + len(patch_bytes)]

        print(f"Original bytes at {hex(patch_location)}: {' '.join(f'{b:02X}' for b in original_bytes)}")
        print(f"Patching with bytes: {' '.join(f'{b:02X}' for b in patch_bytes)}")

        # Check if already patched
        if original_bytes == patch_bytes:
            print("[INFO] Bytes are already patched. No changes made.\n")
            return "skipped"

        for k in range(len(patch_bytes)):
            file_data[patch_location + k] = patch_bytes[k]

        # --- 6. Write the patched data back to the original file ---
        try:
            with open(target_path, 'wb') as f:
                f.write(file_data)
            print(f"[SUCCESS] Successfully patched {os.path.basename(target_path)}.\n")
            return True
        except PermissionError:
            print(f"[FATAL ERROR] Permission denied while writing to {target_path}.")
            print("Please re-run this script with Administrator privileges.\n")
            # We should restore the backup since the patch failed mid-way
            shutil.copy2(backup_path, target_path)
            return False
        except IOError as e:
            print(f"[ERROR] Could not write to output file: {e}\n")
            return False
    else:
        print("[FAILURE] Signature not found. The file may be an incompatible version.\n")
        # Clean up the unnecessary backup file
        os.remove(backup_path)
        return False

def main():
    """ Main function to define and run the patching tasks. """
    print("=====================================================")
    print("=      Alternative A2DP Driver Patcher            =")
    print("=====================================================")
    print("This script must be run from the root installation directory of the driver.")
    print("e.g., C:\\Program Files\\Luculent Systems\\AltA2DP")
    print("!!! IMPORTANT: Please run this script as an Administrator! !!!\n")

    patch_tasks = [
        {
            "file": "AltA2dpConfig.exe",
            "signature": "41 83 F9 07 0F 87 ?? ?? ?? ??",
            "patch_offset": 4,
            "patch_data": "0F 86",
        },
        {
            # Use os.path.join to correctly build the path to the driver
            "file": os.path.join('Driver', 'AltA2DP.sys'),
            "signature": "33 D2 48 8B CB E8 ?? ?? ?? ?? 83 F8 06",
            "patch_offset": 5,
            "patch_data": "B8 06 00 00 00",
        }
    ]

    patched_count = 0
    skipped_count = 0
    restored_count = 0
    failed_count = 0

    for task in patch_tasks:
        result = patch_file(task["file"], task["signature"], task["patch_data"], task["patch_offset"])
        if result is True:
            patched_count += 1
        elif result == "skipped":
            skipped_count += 1
        elif result == "restored":
            restored_count += 1
        else: # False
            failed_count += 1

    print("--- Patcher Finished ---")
    print(f"Summary: {patched_count} file(s) patched, {restored_count} restored, {skipped_count} skipped, {failed_count} failed.")
    if failed_count > 0:
        print("One or more files could not be patched. Please check the errors above.")
    else:
        print("All operations completed successfully.")

if __name__ == "__main__":
    main()
