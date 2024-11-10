import winreg
import os
from win32com.client import Dispatch
import pythoncom
import win32gui
import win32ui
import win32con
import win32api
from PIL import Image
import io

class SystemApps:
    @staticmethod
    def get_app_icon(file_path):
        try:
            large, small = win32gui.ExtractIconEx(file_path, 0)
            if large:
                win32gui.DestroyIcon(large[0])
            if small:
                # Convert icon to PIL Image
                ico_x = win32api.GetSystemMetrics(win32con.SM_CXSMICON)
                ico_y = win32api.GetSystemMetrics(win32con.SM_CYSMICON)
                
                hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
                hbmp = win32ui.CreateBitmap()
                hbmp.CreateCompatibleBitmap(hdc, ico_x, ico_y)
                hdc = hdc.CreateCompatibleDC()
                
                hdc.SelectObject(hbmp)
                hdc.DrawIcon((0, 0), small[0])
                
                bmpstr = hbmp.GetBitmapBits(True)
                img = Image.frombuffer(
                    'RGBA', (ico_x, ico_y),
                    bmpstr, 'raw', 'BGRA', 0, 1
                )
                
                win32gui.DestroyIcon(small[0])
                return img
        except:
            pass
        return None

    @staticmethod
    def get_installed_apps():
        apps = []
        
        # Get apps from Program Files and Program Files (x86)
        program_paths = [
            os.environ["ProgramFiles"],
            os.environ.get("ProgramFiles(x86)", "")
        ]
        
        for program_path in program_paths:
            if os.path.exists(program_path):
                for root, dirs, files in os.walk(program_path):
                    for file in files:
                        if file.endswith('.exe'):
                            full_path = os.path.join(root, file)
                            app_name = os.path.splitext(file)[0]
                            icon = SystemApps.get_app_icon(full_path)
                            apps.append({
                                'name': app_name,
                                'path': full_path,
                                'icon': icon
                            })

        # Get apps from Start Menu
        start_menu_paths = [
            os.path.join(os.environ["ProgramData"], "Microsoft", "Windows", "Start Menu", "Programs"),
            os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs")
        ]

        for start_menu in start_menu_paths:
            if os.path.exists(start_menu):
                for root, dirs, files in os.walk(start_menu):
                    for file in files:
                        if file.endswith('.lnk'):
                            try:
                                shell = Dispatch("WScript.Shell")
                                shortcut = shell.CreateShortCut(os.path.join(root, file))
                                target_path = shortcut.Targetpath
                                if target_path.endswith('.exe'):
                                    app_name = os.path.splitext(file)[0]
                                    icon = SystemApps.get_app_icon(target_path)
                                    apps.append({
                                        'name': app_name,
                                        'path': target_path,
                                        'icon': icon
                                    })
                            except:
                                continue

        # Get UWP apps
        uwp_apps = {
            "Calculator": "Microsoft.WindowsCalculator_8wekyb3d8bbwe!App",
            "Microsoft Store": "Microsoft.WindowsStore_8wekyb3d8bbwe!App",
            "Settings": "Windows.ImmersiveControlPanel_cw5n1h2txyewy!microsoft.windows.immersivecontrolpanel",
            "Photos": "Microsoft.Windows.Photos_8wekyb3d8bbwe!App",
            "Notepad": "Microsoft.WindowsNotepad_8wekyb3d8bbwe!App",
            "Microsoft Teams": "MicrosoftTeams_8wekyb3d8bbwe!Teams"
        }

        # Add UWP apps
        for name, app_id in uwp_apps.items():
            apps.append({
                'name': name,
                'path': f"UWP:{app_id}",
                'icon': None  # UWP icons need different handling
            })

        # Remove duplicates based on path and sort by name
        unique_apps = {}
        for app in apps:
            if app['path'] not in unique_apps:
                unique_apps[app['path']] = app
        
        return sorted(unique_apps.values(), key=lambda x: x['name'].lower())