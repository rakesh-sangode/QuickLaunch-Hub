import winreg
import os


class SystemApps:
    @staticmethod
    def _get_registry_value(key, name):
        """
        Safely get a registry value
        """
        try:
            value = winreg.QueryValueEx(key, name)[0]
            return value if value and isinstance(value, str) else ""
        except (WindowsError, KeyError, TypeError):
            return ""

    @staticmethod
    def _get_apps_from_key(key_path, hive=winreg.HKEY_LOCAL_MACHINE, flags=0):
        """
        Helper method to get apps from a specific registry key
        """
        apps = []
        try:
            print(f"Trying to open registry key: {key_path}")
            key = winreg.OpenKey(hive, key_path, 0, winreg.KEY_READ | flags)
            try:
                num_subkeys = winreg.QueryInfoKey(key)[0]
                print(f"Found {num_subkeys} subkeys in {key_path}")
                
                for i in range(num_subkeys):
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        subkey = winreg.OpenKey(key, subkey_name)
                        try:
                            # Get the display name first
                            name = SystemApps._get_registry_value(subkey, "DisplayName")
                            if not name:  # Skip if no display name
                                continue

                            # Skip Windows Updates
                            if any(x in name.lower() for x in ["security update", "update for", "service pack", "hotfix", "kb"]):
                                continue

                            print(f"Found application: {name}")

                            # Get executable path
                            exe_path = ""
                            
                            # Try DisplayIcon
                            display_icon = SystemApps._get_registry_value(subkey, "DisplayIcon")
                            if display_icon:
                                icon_path = display_icon.split(",")[0].strip('"').strip()
                                if icon_path.endswith('.exe') and os.path.exists(icon_path):
                                    exe_path = icon_path

                            # If no exe_path yet, try InstallLocation
                            if not exe_path:
                                install_location = SystemApps._get_registry_value(subkey, "InstallLocation")
                                if install_location and os.path.exists(install_location):
                                    for root, _, files in os.walk(install_location):
                                        for file in files:
                                            if file.endswith('.exe'):
                                                potential_path = os.path.join(root, file)
                                                if os.path.exists(potential_path):
                                                    exe_path = potential_path
                                                    break
                                        if exe_path:
                                            break

                            # If still no exe_path, try UninstallString
                            if not exe_path:
                                uninstall_string = SystemApps._get_registry_value(subkey, "UninstallString")
                                if uninstall_string:
                                    parts = uninstall_string.split()
                                    if parts:
                                        potential_path = parts[0].strip('"')
                                        if potential_path.endswith('.exe') and os.path.exists(potential_path):
                                            exe_path = potential_path

                            # Get other details
                            version = SystemApps._get_registry_value(subkey, "DisplayVersion")
                            vendor = SystemApps._get_registry_value(subkey, "Publisher")
                            install_date = SystemApps._get_registry_value(subkey, "InstallDate")
                            install_location = SystemApps._get_registry_value(subkey, "InstallLocation")

                            apps.append({
                                'name': name.strip(),
                                'version': version.strip(),
                                'vendor': vendor.strip(),
                                'install_date': install_date.strip(),
                                'install_location': install_location.strip(),
                                'exe_path': exe_path.strip()
                            })
                        finally:
                            winreg.CloseKey(subkey)
                    except WindowsError as e:
                        print(f"Error accessing subkey {i}: {str(e)}")
                        continue
            finally:
                winreg.CloseKey(key)
        except WindowsError as e:
            print(f"Error opening registry key {key_path}: {str(e)}")
        return apps

    @staticmethod
    def get_installed_apps():
        """
        Get installed applications using Windows Registry
        Returns a list of dictionaries containing application information
        """
        apps = []
        
        # Registry paths to check
        registry_paths = [
            # HKEY_LOCAL_MACHINE paths for 64-bit apps
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", winreg.KEY_WOW64_64KEY),
            # HKEY_LOCAL_MACHINE paths for 32-bit apps
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall", winreg.KEY_WOW64_64KEY),
            # HKEY_CURRENT_USER paths
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", 0),
        ]

        print("Starting to fetch installed applications...")
        
        # Get apps from each registry path
        for hive, path, flags in registry_paths:
            try:
                new_apps = SystemApps._get_apps_from_key(path, hive, flags)
                print(f"Found {len(new_apps)} applications in {path}")
                apps.extend(new_apps)
            except Exception as e:
                print(f"Error reading from {path}: {str(e)}")
                continue

        print(f"Total applications found: {len(apps)}")

        # Remove duplicates based on name and version
        unique_apps = {}
        for app in apps:
            key = f"{app['name']}_{app['version']}".lower()
            if key not in unique_apps or (app['exe_path'] and not unique_apps[key]['exe_path']):
                unique_apps[key] = app

        # Return sorted list by application name
        sorted_apps = sorted(unique_apps.values(), key=lambda x: x['name'].lower())
        print(f"Final unique applications count: {len(sorted_apps)}")
        return sorted_apps