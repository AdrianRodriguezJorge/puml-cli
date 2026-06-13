import os
import sys
import json
import winreg
import ctypes

# Simple i18n for the uninstaller
TRANSLATIONS = {
    "en": {
        "title": "PLANTUML LOCAL CLI TOOLBOX - UNINSTALLER",
        "starting": "Starting uninstallation process...",
        "path_removing": "Removing '{path}' from your User PATH registry...",
        "path_not_found": "Project directory was not found in the user PATH. No changes made.",
        "path_success": "User PATH updated successfully! Environmental changes broadcasted.",
        "path_failed": "Failed to modify User PATH registry key.",
        "jar_found": "PlantUML JAR file detected at: {path}",
        "jar_prompt": "Do you want to delete this PlantUML JAR file? (y/n) [n]: ",
        "jar_deleted": "JAR file deleted successfully.",
        "jar_skipped": "JAR file deletion skipped.",
        "config_deleted": "Configuration file (config.json) deleted successfully.",
        "finish_header": "UNINSTALLATION SUCCESSFUL!",
        "finish_body": "The toolbox has been successfully unregistered from your system.\nYou can now safely delete the project folder.",
        "press_enter": "Press Enter to exit..."
    },
    "es": {
        "title": "CAJA DE HERRAMIENTAS PLANTUML - DESINSTALADOR",
        "starting": "Iniciando el proceso de desinstalación...",
        "path_removing": "Eliminando '{path}' del PATH de tu usuario en el registro...",
        "path_not_found": "El directorio del proyecto no se encontró en el PATH del usuario. No se realizaron cambios.",
        "path_success": "¡PATH de usuario actualizado con éxito! Se han propagado los cambios de entorno.",
        "path_failed": "Error al modificar la clave de registro del PATH de usuario.",
        "jar_found": "Archivo JAR de PlantUML detectado en: {path}",
        "jar_prompt": "¿Deseas eliminar este archivo JAR de PlantUML? (s/n) [n]: ",
        "jar_deleted": "Archivo JAR eliminado con éxito.",
        "jar_skipped": "Se omitió la eliminación del archivo JAR.",
        "config_deleted": "Archivo de configuración (config.json) eliminado con éxito.",
        "finish_header": "¡DESINSTALACIÓN COMPLETADA CON ÉXITO!",
        "finish_body": "La herramienta ha sido dada de baja correctamente de tu sistema.\nAhora puedes eliminar la carpeta del proyecto de forma segura.",
        "press_enter": "Presiona Enter para salir..."
    }
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_lang():
    """Load configuration language if config.json exists."""
    config_path = "config.json"
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get("language", "en")
        except Exception:
            pass
    return "en"

def remove_from_user_path(script_dir, lang, t):
    """Safely remove the project folder from the Windows User PATH registry variable."""
    script_dir = os.path.abspath(script_dir)
    print(f"\n>>> {t['path_removing'].format(path=script_dir)}")
    
    try:
        # Open User Environment Registry key
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_ALL_ACCESS)
        try:
            try:
                current_path, _ = winreg.QueryValueEx(key, "Path")
            except FileNotFoundError:
                current_path = ""
            
            # Split paths and filter empty
            paths = [p.strip() for p in current_path.split(';') if p.strip()]
            
            # Find the path in user PATH (case-insensitive)
            initial_count = len(paths)
            paths = [p for p in paths if p.lower() != script_dir.lower()]
            
            if len(paths) == initial_count:
                print(f"[INFO] {t['path_not_found']}")
                return True
            
            # Join and update registry value
            new_path = ';'.join(paths)
            winreg.SetValueEx(key, "Path", 0, winreg.REG_SZ, new_path)
            
            # Broadcast changes to environment variables
            HWND_BROADCAST = 0xFFFF
            WM_SETTINGCHANGE = 0x001A
            result = ctypes.c_ulong()
            ctypes.windll.user32.SendMessageTimeoutW(
                HWND_BROADCAST,
                WM_SETTINGCHANGE,
                0,
                "Environment",
                2,  # SMTO_ABORTIFHUNG
                1000,
                ctypes.byref(result)
            )
            
            print(f"[INFO] {t['path_success']}")
            return True
        finally:
            winreg.CloseKey(key)
    except Exception as e:
        print(f"[ERROR] {t['path_failed']}: {e}")
        return False

def handle_jar_deletion(lang, t):
    """Search for the configured or downloaded JAR files and conditionally delete them."""
    jar_file = None
    config_path = "config.json"
    
    # 1. Read JAR path from config if possible
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                jar_path = config.get("jar_path", "")
                if jar_path:
                    full_path = jar_path if os.path.isabs(jar_path) else os.path.join(os.getcwd(), jar_path)
                    if os.path.exists(full_path):
                        jar_file = full_path
        except Exception:
            pass
            
    # 2. Fall back to searching local directory for plantuml.jar
    if not jar_file:
        fallback = os.path.join(os.getcwd(), "plantuml.jar")
        if os.path.exists(fallback):
            jar_file = fallback
            
    # 3. If found, prompt for deletion
    if jar_file and os.path.exists(jar_file):
        print(f"\n[INFO] {t['jar_found'].format(path=jar_file)}")
        ans = input(t["jar_prompt"]).strip().lower()
        if ans in ['y', 'yes', 's', 'si']:
            try:
                os.remove(jar_file)
                print(f"[INFO] {t['jar_deleted']}")
            except Exception as e:
                print(f"[ERROR] Could not delete JAR file: {e}")
        else:
            print(f"[INFO] {t['jar_skipped']}")

def main():
    clear_screen()
    
    lang = load_lang()
    t = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    
    print("=" * 80)
    print(f"  {t['title']}")
    print("=" * 80)
    print(t["starting"])
    
    # 1. Remove from PATH registry
    remove_from_user_path(os.getcwd(), lang, t)
    
    # 2. Handle JAR deletion prompt
    handle_jar_deletion(lang, t)
    
    # 3. Delete config.json
    config_path = "config.json"
    if os.path.exists(config_path):
        try:
            os.remove(config_path)
            print(f"[INFO] {t['config_deleted']}")
        except Exception as e:
            print(f"[ERROR] Could not delete config.json: {e}")
            
    # 4. Finish
    print("\n" + "=" * 80)
    print(f"  {t['finish_header']}")
    print("=" * 80)
    print(t["finish_body"])
    print("=" * 80)
    
    input(f"\n{t['press_enter']}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nUninstallation aborted / Desinstalación abortada.")
