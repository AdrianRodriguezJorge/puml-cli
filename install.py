import os
import sys
import json
import subprocess
import urllib.request
import winreg
import ctypes

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_or_create_config():
    """Load config.json or create a default one if it doesn't exist."""
    config_path = "config.json"
    default_config = {
        "jar_path": "plantuml.jar",
        "enable_theme_selection": False,
        "enable_dpi_selection": false,
        "default_dpi": 600,
        "default_theme": None,
        "language": "en"
    }
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return default_config
    else:
        return default_config

def save_config(config):
    """Save the configuration dictionary to config.json."""
    config_path = "config.json"
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        print(f"[ERROR] Could not save config.json: {e}")

def run_pip_install(lang):
    """Install dependencies from requirements.txt system-wide."""
    msg_installing = (
        "Installing Python dependencies system-wide from requirements.txt..."
        if lang == 'en' else
        "Instalando dependencias de Python a nivel de sistema desde requirements.txt..."
    )
    msg_success = (
        "Dependencies installed successfully!"
        if lang == 'en' else
        "¡Dependencias instaladas con éxito!"
    )
    msg_failed = (
        "Failed to install dependencies via pip. Please verify your pip installation."
        if lang == 'en' else
        "Error al instalar dependencias mediante pip. Verifica tu instalación de pip."
    )

    print(f"\n>>> {msg_installing}")
    try:
        # Run pip install system-wide (no environment)
        # Use sys.executable to ensure we run pip on the active python environment
        cmd = [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if process.returncode == 0:
            print(f"[INFO] {msg_success}")
            return True
        else:
            print(f"[ERROR] {msg_failed}")
            print(process.stderr)
            return False
    except Exception as e:
        print(f"[ERROR] {msg_failed}: {e}")
        return False

def download_jar(dest_path, lang):
    """Download the official stable PlantUML JAR file with a progress bar."""
    url = "https://github.com/plantuml/plantuml/releases/download/v1.2024.5/plantuml-1.2024.5.jar"
    
    msg_downloading = (
        f"Downloading PlantUML JAR from:\n{url}\nTo destination:\n{dest_path}..."
        if lang == 'en' else
        f"Descargando el JAR de PlantUML desde:\n{url}\nHacia el destino:\n{dest_path}..."
    )
    msg_success = "Download complete successfully!" if lang == 'en' else "¡Descarga completada con éxito!"
    msg_failed = "Download failed." if lang == 'en' else "Error al descargar."

    print(f"\n>>> {msg_downloading}")
    
    # Progress hook callback
    def reporthook(blocknum, blocksize, totalsize):
        readsofar = blocknum * blocksize
        if totalsize > 0:
            percent = readsofar * 1e2 / totalsize
            # Print text-based progress bar
            sys.stdout.write(f"\r[{percent:5.1f}%] {readsofar / (1024*1024):.2f} MB / {totalsize / (1024*1024):.2f} MB")
            sys.stdout.flush()
        else:
            sys.stdout.write(f"\rDownloaded {readsofar / (1024*1024):.2f} MB")
            sys.stdout.flush()

    try:
        urllib.request.urlretrieve(url, dest_path, reporthook)
        print(f"\n[INFO] {msg_success}")
        return True
    except Exception as e:
        print(f"\n[ERROR] {msg_failed}: {e}")
        return False

def add_to_user_path(script_dir, lang):
    """Safely add the project folder to the Windows User PATH registry variable."""
    script_dir = os.path.abspath(script_dir)
    
    msg_already_in_path = (
        "Project directory is already configured in the user PATH."
        if lang == 'en' else
        "El directorio del proyecto ya está configurado en el PATH del usuario."
    )
    msg_adding = (
        f"Adding '{script_dir}' to your User PATH registry..."
        if lang == 'en' else
        f"Agregando '{script_dir}' al PATH de usuario en el registro..."
    )
    msg_success = (
        "User PATH updated successfully! Environmental changes broadcasted."
        if lang == 'en' else
        "¡PATH de usuario actualizado con éxito! Se han propagado los cambios de entorno."
    )
    msg_failed = (
        "Failed to modify User PATH registry key."
        if lang == 'en' else
        "Error al modificar la clave de registro del PATH de usuario."
    )

    print(f"\n>>> {msg_adding}")
    
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
            
            # Check for case-insensitive duplicate
            if script_dir.lower() in [p.lower() for p in paths]:
                print(f"[INFO] {msg_already_in_path}")
                return True
            
            # Append and update registry value
            paths.append(script_dir)
            new_path = ';'.join(paths)
            winreg.SetValueEx(key, "Path", 0, winreg.REG_SZ, new_path)
            
            # Broadcast changes to Environment
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
            
            print(f"[INFO] {msg_success}")
            return True
        finally:
            winreg.CloseKey(key)
    except Exception as e:
        print(f"[ERROR] {msg_failed}: {e}")
        return False

def main():
    clear_screen()
    
    # 1. Load configuration or default
    config = load_or_create_config()
    current_lang = config.get("language", "en")
    
    # Display installer header
    print("=" * 80)
    print("  PLANTUML LOCAL CLI TOOLBOX - INSTALLER & CONFIGURATION")
    print("=" * 80)
    print(f"Current language configured / Idioma actual configurado: [{current_lang.upper()}]")
    print("-" * 80)
    
    # 2. Select language
    print("Choose installation and tool language / Elige el idioma de instalación y la herramienta:")
    print(" [1] English (EN)")
    print(" [2] Español (ES)")
    print("-" * 80)
    lang_choice = input("Select an option / Selecciona una opción (1-2) [1]: ").strip()
    
    lang = "en"
    if lang_choice == "2":
        lang = "es"
    
    # Persist the selected language in config
    config["language"] = lang
    save_config(config)
    
    # Welcome messages in selected language
    msg_welcome = (
        "Starting installation process..." if lang == 'en' else "Iniciando el proceso de instalación..."
    )
    print(f"\n[INFO] {msg_welcome}")
    
    # 3. Install Python Dependencies
    run_pip_install(lang)
    
    # 4. Check for PlantUML JAR
    jar_path = config.get("jar_path", "plantuml.jar")
    # Resolve relative to current directory if not absolute
    full_jar_path = jar_path if os.path.isabs(jar_path) else os.path.join(os.getcwd(), jar_path)
    
    jar_exists = os.path.exists(full_jar_path)
    
    # If the configured JAR doesn't exist, search the current directory for any plantuml*.jar
    if not jar_exists:
        found_jars = [f for f in os.listdir('.') if f.lower().startswith("plantuml") and f.lower().endswith(".jar")]
        if found_jars:
            # Pick the first matching jar
            selected_jar = found_jars[0]
            config["jar_path"] = selected_jar
            save_config(config)
            full_jar_path = os.path.join(os.getcwd(), selected_jar)
            jar_exists = True
            
            msg_found_local = (
                f"Found local JAR '{selected_jar}' and updated configuration."
                if lang == 'en' else
                f"Se encontró el archivo JAR local '{selected_jar}' y se actualizó la configuración."
            )
            print(f"[INFO] {msg_found_local}")
            
    if not jar_exists:
        # Prompt user to download
        prompt_download = (
            "PlantUML JAR was not found. Download it automatically? (y/n) [y]: "
            if lang == 'en' else
            "El archivo JAR de PlantUML no se encuentra. ¿Descargarlo automáticamente? (s/n) [s]: "
        )
        ans = input(prompt_download).strip().lower()
        if ans in ['', 'y', 'yes', 's', 'si']:
            dest_jar_name = "plantuml.jar"
            dest_path = os.path.join(os.getcwd(), dest_jar_name)
            success = download_jar(dest_path, lang)
            if success:
                config["jar_path"] = dest_jar_name
                save_config(config)
            else:
                msg_err = (
                    "Could not download JAR automatically. Please place it manually."
                    if lang == 'en' else
                    "No se pudo descargar el JAR automáticamente. Por favor, colócalo de forma manual."
                )
                print(f"[WARNING] {msg_err}")
        else:
            msg_manual = (
                "Remember to place your PlantUML JAR in this directory and update config.json."
                if lang == 'en' else
                "Recuerda colocar tu archivo JAR de PlantUML en esta carpeta y actualizar config.json."
            )
            print(f"[INFO] {msg_manual}")
    else:
        msg_jar_ok = (
            f"PlantUML JAR is correctly configured at: {full_jar_path}"
            if lang == 'en' else
            f"El JAR de PlantUML está configurado correctamente en: {full_jar_path}"
        )
        print(f"[INFO] {msg_jar_ok}")
        
    # 5. Add to PATH
    add_to_user_path(os.getcwd(), lang)
    
    # 6. Output final instructions
    msg_finish_header = (
        "INSTALLATION SUCCESSFUL!" if lang == 'en' else "¡INSTALACIÓN COMPLETADA CON ÉXITO!"
    )
    msg_finish_body = (
        "To start using the tool:\n"
        " 1. Open a NEW terminal window (Command Prompt or PowerShell) to load the updated PATH.\n"
        " 2. Run the tool from ANY folder by executing:\n"
        "      puml\n"
        "    Or run it directly using the file wrapper:\n"
        "      puml_toolbox.py"
        if lang == 'en' else
        "Para comenzar a usar la herramienta:\n"
        " 1. Abre una NUEVA ventana de terminal (Símbolo del sistema o PowerShell) para cargar el PATH actualizado.\n"
        " 2. Ejecuta la herramienta desde CUALQUIER carpeta escribiendo:\n"
        "      puml\n"
        "    O ejecútala directamente usando el envoltorio:\n"
        "      puml_toolbox.py"
    )
    
    print("\n" + "=" * 80)
    print(f"  {msg_finish_header}")
    print("=" * 80)
    print(msg_finish_body)
    print("=" * 80)
    
    # Pause so user can read before terminal closes
    input("\nPress Enter to exit / Presiona Enter para salir..." if lang == 'en' else "\nPresiona Enter para salir...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInstallation aborted / Instalación abortada.")
