import os

def patch_file(input_path, output_path, signature_hex, patch_hex, patch_offset):
    """
    Searches for a signature in a file and applies a patch, creating a new file.

    Args:
        input_path (str): The path to the original file.
        output_path (str): The path where the patched file will be saved.
        signature_hex (str): The AOB signature with ?? for wildcards.
        patch_hex (str): The hex string of the bytes to write.
        patch_offset (int): The offset from the start of the signature to apply the patch.

    Returns:
        bool: True if patching was successful, False otherwise.
    """
    print(f"--- Patching {os.path.basename(input_path)} ---")

    # 1. Read the original file
    try:
        with open(input_path, 'rb') as f:
            file_data = bytearray(f.read())
            print(f"Read {len(file_data)} bytes from original file.")
    except FileNotFoundError:
        print(f"[ERROR] File not found: {input_path}")
        return False

    # 2. Parse the signature string into bytes and wildcards
    signature_parts = signature_hex.split(' ')
    signature_bytes = bytearray()
    wildcards = set()
    for i, part in enumerate(signature_parts):
        if part == '??':
            wildcards.add(i)
            signature_bytes.append(0)  # Placeholder byte
        else:
            try:
                signature_bytes.append(int(part, 16))
            except ValueError:
                print(f"[ERROR] Invalid hex value in signature: {part}")
                return False

    # 3. Convert patch hex string to bytes and validate
    try:
        patch_bytes = bytearray.fromhex(patch_hex.replace(' ', ''))
    except ValueError:
        print(f"[ERROR] Invalid hex data in patch: {patch_hex}")
        return False

    # 4. Scan the file for the signature
    found_offset = -1
    for i in range(len(file_data) - len(signature_bytes) + 1):
        match = True
        for j in range(len(signature_bytes)):
            if j in wildcards:
                continue
            if file_data[i + j] != signature_bytes[j]:
                match = False
                break
        if match:
            found_offset = i
            break

    # 5. If found, validate and apply the patch
    if found_offset != -1:
        print(f"[SUCCESS] Signature found at offset: {hex(found_offset)}")

        # Calculate the precise location to write the patch
        patch_location = found_offset + patch_offset

        # Boundary check
        if patch_location + len(patch_bytes) > len(file_data):
            print(f"[ERROR] Patch would extend beyond file bounds. File size: {len(file_data)}, "
                  f"patch end: {patch_location + len(patch_bytes)}")
            return False

        # Show what we're about to overwrite
        original_bytes = file_data[patch_location:patch_location + len(patch_bytes)]
        print(f"Original bytes at {hex(patch_location)}: {' '.join(f'{b:02X}' for b in original_bytes)}")
        print(f"Patching with {len(patch_bytes)} bytes: {' '.join(f'{b:02X}' for b in patch_bytes)}")

        # Confirm the patch makes sense (basic validation)
        if len(patch_bytes) == 0:
            print("[ERROR] Patch data is empty")
            return False

        # Apply the patch
        for k in range(len(patch_bytes)):
            file_data[patch_location + k] = patch_bytes[k]

        # 6. Write the new, patched file
        try:
            with open(output_path, 'wb') as f:
                f.write(file_data)
            print(f"[SUCCESS] Patched file created: {output_path}")

            # Verify the patch was applied
            verify_bytes = file_data[patch_location:patch_location + len(patch_bytes)]
            print(f"Verification - bytes at {hex(patch_location)}: {' '.join(f'{b:02X}' for b in verify_bytes)}")
            print()
            return True
        except IOError as e:
            print(f"[ERROR] Could not write to output file: {e}\n")
            return False

    else:
        print("[FAILURE] Signature not found. The file may be an incompatible version or already patched.\n")
        return False

def main():
    """
    Main function to define and run the patching tasks.
    """
    patch_tasks = [
        {
            "file": "AltA2dpConfig.exe",
            "signature": "41 83 F9 07 0F 87 ?? ?? ?? ??",
            "patch_offset": 4,  # This targets the "0F 87" (JA instruction)
            "patch_data": "0F 86",  # Changes to "0F 86" (JBE instruction)
            "description": "Change JA (Jump if Above) to JBE (Jump if Below or Equal)"
        },
        {
            "file": "AltA2DP.sys",
            "signature": "33 D2 48 8B CB E8 ?? ?? ?? ?? 83 F8 06",
            "patch_offset": 5,  # This targets the CALL instruction
            "patch_data": "B8 06 00 00 00",  # MOV EAX, 6 (5 bytes)
            "description": "Replace function call with MOV EAX, 6"
        }
    ]

    print("=== Binary Patcher ===")
    print("IMPORTANT: Make sure you have backups of your original files!")
    print()

    success_count = 0
    for i, task in enumerate(patch_tasks, 1):
        print(f"Task {i}: {task['description']}")

        # Create the output filename
        base, ext = os.path.splitext(task["file"])
        output_file = f"{base}.patched{ext}"

        if patch_file(task["file"], output_file, task["signature"], task["patch_data"], task["patch_offset"]):
            success_count += 1

    print("--- Patcher Finished ---")
    if success_count == len(patch_tasks):
        print("All files patched successfully!")
    else:
        print(f"{len(patch_tasks) - success_count} file(s) could not be patched.")
        print("Check that the original files exist and are the expected version.")


if __name__ == "__main__":
    main()