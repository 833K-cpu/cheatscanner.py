import os
import sys
import zipfile

# === Highly Specialized Minecraft Cheat Client/Mod keywords ===
CHEAT_KEYWORDS = [
    # Major client identifiers
    "meteorclient", "net.wurst", "wurstclient", "aristois", "futureclient", "rusherhack", "xenon",
    "liquidbounce", "riseclient", "novoline", "kwerk", "pulsive", "orcaclient", "wurst", "meteor",
    "onyx", "vape", "ares", "aids hack", "aristoris", "francium", "skligga", "platinium", "achilles",
    # Strings and functions often seen in clients/hacks
    "gettargetmargian", "gettoargetmargain", "gettargetm", "bad at the game? try lumina client (luminaclient.com)",
    "geteventbutton", "hitboxes", "self d", "self de", "coffe", "noweakattack", "nursultan", "florens",
    # File and class signatures
    "/net/wurstclient/hacks/chattranslatorhack.class", "st/mixin/keyboardmixin", ".lattia", "bleachhack_outline",
    # Hex/fragments/patterns (likely obfuscation, see your list)
    "3m!", "s)b!", "jc]hdyo", "tsek$", "hyx%j", "nxw]s", "6jc]ku", "p~,r", "b6&@", "rm &%", "e `9cz",
    "vewimwc", "988697", "guqd$", "ypbc", "]ue8", "yzwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
    "#]!",
    # Cheat mod fragments (combat, movement, macros)
    "killaura", "crystalaura", "autoclick", "triggerbot", "aimassist", "velocity", "scaffold", "flyhack", "nofall",
    "autocrystal", "anchormacro"
]

def print_result(msg, color_code=None):
    if color_code:
        print(f"{color_code}{msg}\033[0m")
    else:
        print(msg)

def scan_jar(jar_path):
    found_something = False
    try:
        with zipfile.ZipFile(jar_path, 'r') as jar:
            for jar_file in jar.namelist():
                # Scan the file name itself
                for keyword in CHEAT_KEYWORDS:
                    if keyword.lower() in jar_file.lower():
                        print_result(
                            f"[CHEAT MOD DETECTED] '{keyword}' in archive member name: {jar_path} -> {jar_file}",
                            "\033[91m"
                        )
                        found_something = True
                # Try to read and scan the content if it's plausible text/class
                try:
                    if any(jar_file.lower().endswith(ext) for ext in [".class", ".txt", ".json", ".md", ".yml", ".xml", ".cfg", ""]):
                        content = jar.read(jar_file)
                        content_lower = content.lower()
                        for keyword in CHEAT_KEYWORDS:
                            if keyword.lower().encode() in content_lower:
                                print_result(
                                    f"[CHEAT MOD DETECTED] '{keyword}' in file content: {jar_path} -> {jar_file}",
                                    "\033[91m"
                                )
                                found_something = True
                except Exception:
                    # Non-readable or binary file in zip
                    continue
        return found_something
    except zipfile.BadZipFile:
        print_result(f"[WARN] {jar_path} is not a valid zip/jar file.", "\033[93m")
        return False
    except Exception as e:
        print_result(f"[ERROR] Scanning failed for {jar_path}: {e}", "\033[93m")
        return False

def scan_folder(folder_path):
    total = 0
    suspicious = 0
    found_files = []
    for root, dirs, files in os.walk(folder_path):
        for f in files:
            if f.endswith(('.jar', '.zip', '.mod')):
                total += 1
                file_path = os.path.join(root, f)
                if scan_jar(file_path):
                    found_files.append(file_path)
                    suspicious += 1
    print_result(f"\nScan complete! {total} archive(s) scanned.", "\033[96m")
    if suspicious:
        print_result(f"[RESULTS] {suspicious} suspicious mod(s) detected.\n", "\033[91m")
        for path in found_files:
            print(" -", path)
    else:
        print_result("[RESULTS] No known cheat clients found.", "\033[92m")

def main():
    if len(sys.argv) < 2:
        print("Usage: cheatscanner.exe <folder_or_jar>")
        sys.exit(1)
    path = sys.argv[1]
    if os.path.isdir(path):
        scan_folder(path)
    elif path.endswith(('.jar', '.zip', '.mod')):
        scan_jar(path)
    else:
        print_result("Not a folder or supported archive file.", "\033[93m")

if __name__ == "__main__":
    main()
