# PlantUML Local CLI Toolbox

A modular, object-oriented interactive Command Line Interface (CLI) toolbox to easily convert PlantUML diagram files (`.puml`, `.wsd`, `.plantuml`) to images, documents, and interactive class structures locally, without relying on external web servers.

---

## Architecture

This project is structured according to clean, modular design principles. The monolithic codebase has been refactored into a cohesive Python package:

* **`puml_cli/`**: Core package containing all application modules.
  * **`config.py`**: Manages loading and saving configuration profiles in `config.json` with a robust fallback system.
  * **`i18n.py`**: Handles translation maps for internationalization, allowing bilingual interaction in English (`en`) and Spanish (`es`) dynamically.
  * **`parser.py`**: Resolves local diagram scanning and sanitizes pasted PlantUML script code.
  * **`exporter.py`**: Handles shell execution of the Java PlantUML compiler, performs file renaming alignment, and automatically previews output.
  * **`cli.py`**: Controls the user experience, rich rendering of tables/menus, and language selection.
* **`install.py` / `install.bat`**: The automated installer that manages dependencies, downloads the required `.jar`, and registers the project directory to the system PATH.
* **`puml_toolbox.py`**: A thin execution wrapper that acts as the entry point.
* **`puml.bat`**: A command line shortcut for executing the toolbox on Windows.

---

## Features

1. **Automation Installer**: Installs global package dependencies, downloads PlantUML, and appends the folder to the user `PATH` registry key safely (avoiding duplicate entries).
2. **Multi-Format Export**: Supports PNG, SVG, EPS, TXT, UTXT, HTML (interactive classes), VDX (Visio XML), and XMI.
3. **Advanced Flow Controls**: Skips resolution (DPI) and theme selection menus if configured, speeding up standard conversions.
4. **Bilingual interface**: Instantly toggle the tool language between Spanish and English inside the CLI interface. Your preferences are saved immediately in `config.json`.
5. **Interactive Pasting**: Paste raw PlantUML code from clipboard, automatically sanitizing syntax errors, formatting tags, and naming files dynamically.
6. **Automatic Overwrite Backup**: Backs up existing files automatically with incremented suffixes (e.g. `diagram_1.png`) to prevent accidental data loss.

---

## Installation

We provide an interactive script to automate the setup process.

### Automated Setup (Recommended)
1. Open your terminal in the project directory.
2. Run the installer batch file:
   ```cmd
   install.bat
   ```
3. Follow the CLI wizard:
   * **Language Selection**: Choose your preferred interface language (English or Spanish).
   * **Dependencies**: The installer will run `pip install -r requirements.txt` system-wide.
   * **PlantUML JAR Download**: If a local JAR is not found, the script will prompt you to automatically download the official stable version of PlantUML (`plantuml.jar`) with a progress bar.
   * **PATH Setup**: The script will append this folder path to your user environment registry keys.

4. **Start using it**: Open a **NEW** terminal window to load the new PATH, and type:
   ```cmd
   puml
   ```

### Manual Setup
If you prefer to configure everything manually:
1. Install dependencies from `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
2. Download the official PlantUML `.jar` file from [PlantUML Official Site](https://plantuml.com/download) and place it in the project root directory.
3. Create a `config.json` file in the root directory and specify the name/path of the JAR file (see Configuration details below).
4. Run the program directly using Python:
   ```bash
   python puml_toolbox.py
   ```

---

## Configuration (`config.json`)

On first execution, a `config.json` configuration file is generated in the root directory. You can customize the behavior of the toolbox here:

```json
{
    "jar_path": "plantuml.jar",
    "enable_theme_selection": false,
    "enable_dpi_selection": false,
    "default_dpi": 600,
    "default_theme": null,
    "language": "en"
}
```

### Parameters:
* **`jar_path`** (string): The path to your PlantUML jar executable (e.g. `"plantuml.jar"`). Can be relative or absolute.
* **`enable_theme_selection`** (boolean): Set to `true` to show the theme selection menu at export. If `false`, it applies the `default_theme`.
* **`enable_dpi_selection`** (boolean): Set to `true` to show the quality (DPI) menu at export. If `false`, it applies the `default_dpi`.
* **`default_dpi`** (integer): The resolution scale applied to exports when `enable_dpi_selection` is `false` (e.g. `600` for high-quality printing).
* **`default_theme`** (string / null): The default PlantUML theme applied when `enable_theme_selection` is `false` (e.g. `"spacelab"`). Set to `null` to use the standard default PlantUML style.
* **`language`** (string): Active language interface. Choose `"en"` for English or `"es"` for Spanish. Can be changed dynamically inside the app by pressing `L` in the menu.
