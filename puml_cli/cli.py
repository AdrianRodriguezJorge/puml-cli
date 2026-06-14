import os
import sys
import glob

# Try to import rich for beautiful UI
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.prompt import Prompt, IntPrompt, Confirm
    from rich.text import Text
    HAS_RICH = True
    console = Console()
except ImportError:
    HAS_RICH = False

# Import modular local dependencies
from .config import load_config, save_config
from .i18n import t, set_language, get_language
from .parser import (
    get_puml_files,
    sanitize_and_save_pasted_code
)
from .exporter import run_conversion

# Integrated themes supported
THEMES = [
    "spacelab",
    "sandstone",
    "amiga",
    "sketchy",
    "cerulean",
    "cyborg",
    "minty",
    "united",
    "slate",
    "materia",
    "yeti",
    "lumen",
    "solarized-dark",
    "solarized-light",
    "black-knight"
]

def clear_screen():
    """Clear console screen based on operating system."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(working_dir):
    """Print the toolbox header."""
    title_text = t("title")
    subtitle_text = t("working_dir", dir=working_dir)
    
    if HAS_RICH:
        console.print(Panel(
            Text(title_text, style="bold white", justify="center"),
            style="bold blue",
            subtitle=subtitle_text,
            subtitle_align="center"
        ))
    else:
        print("=" * 80)
        print(f"  {title_text}")
        print(f"  {subtitle_text}")
        print("=" * 80)

def print_message(text, style_type="info"):
    """Helper to log styled message to terminal."""
    if HAS_RICH:
        if style_type == "info":
            console.print(f"[bold cyan]{t('info')}:[/bold cyan] {text}")
        elif style_type == "success":
            console.print(f"[bold green]{t('success')}:[/bold green] {text}")
        elif style_type == "error":
            console.print(f"[bold red]{t('error')}:[/bold red] {text}")
        elif style_type == "warning":
            console.print(f"[bold yellow]{t('warning')}:[/bold yellow] {text}")
    else:
        print(f"[{t(style_type).upper()}] {text}")

def select_file(files):
    """Render file selection menu and return choice."""
    if HAS_RICH:
        table = Table(title=t("detected_files"), show_header=True, header_style="bold magenta", expand=True)
        table.add_column(t("col_option"), style="bold cyan", width=8, justify="center")
        table.add_column(t("col_filename"), style="bold white")
        table.add_column(t("col_size"), style="bold yellow", justify="right")
        
        if files:
            for idx, f in enumerate(files, 1):
                table.add_row(str(idx), f, f"{os.path.getsize(f):,}")
            table.add_row("A", f"[bold green]{t('all_files')}[/bold green]", "-")
        else:
            table.add_row("-", f"[italic dim white]{t('no_diagrams')}[/italic dim white]", "-")
            
        table.add_row("P", f"[bold yellow]{t('paste_code_option')}[/bold yellow]", "-")
        table.add_row("L", f"[bold cyan]{t('change_lang_option')}[/bold cyan]", "-")
        table.add_row("0", f"[bold red]{t('exit_option')}[/bold red]", "-")
        
        console.print(table)
        
        choices = [str(i) for i in range(len(files) + 1)] + ['P', 'p', 'L', 'l']
        if files:
            choices += ['A', 'a']
        choice = Prompt.ask(t("select_file_prompt"), choices=choices, default="0")
        
        if choice in ['P', 'p']:
            return "paste"
        elif choice in ['L', 'l']:
            return "language"
        elif choice in ['A', 'a'] and files:
            return "all"
        elif choice == "0":
            return None
        else:
            return files[int(choice) - 1]
    else:
        print(f"\n{t('detected_files')}:")
        if files:
            for idx, f in enumerate(files, 1):
                print(f" [{idx}] {f} ({os.path.getsize(f)} bytes)")
            print(f" [A] {t('all_files')}")
        else:
            print(f"  ({t('no_diagrams')})")
        print(f" [P] {t('paste_code_option')}")
        print(f" [L] {t('change_lang_option')}")
        print(f" [0] {t('exit_option')}")
        print("-" * 80)
        
        choices_prompt = t("select_option_prompt_all") if files else t("select_option_prompt_no_all")
        choice = input(f"{choices_prompt}: ").strip()
        
        if choice.lower() == 'p':
            return "paste"
        elif choice.lower() == 'l':
            return "language"
        elif choice.lower() == 'a' and files:
            return "all"
        elif choice == '0' or not choice.isdigit():
            return None
        
        idx = int(choice) - 1
        if files and 0 <= idx < len(files):
            return files[idx]
        return None

def get_formats():
    """Format configurations."""
    return {
        1: {"name": t("f_png_name"), "flag": "--png", "desc": t("f_png_desc")},
        2: {"name": t("f_svg_name"), "flag": "--svg", "desc": t("f_svg_desc")},
        3: {"name": t("f_eps_name"), "flag": "--eps", "desc": t("f_eps_desc")},
        4: {"name": t("f_txt_name"), "flag": "--txt", "desc": t("f_txt_desc")},
        5: {"name": t("f_utxt_name"), "flag": "--utxt", "desc": t("f_utxt_desc")},
        6: {"name": t("f_html_name"), "flag": "--html", "desc": t("f_html_desc")},
        7: {"name": t("f_vdx_name"), "flag": "--vdx", "desc": t("f_vdx_desc")},
        8: {"name": t("f_xmi_name"), "flag": "--xmi", "desc": t("f_xmi_desc")}
    }

def select_format():
    """Render export format selection menu."""
    formats = get_formats()
    if HAS_RICH:
        table = Table(title=t("available_formats"), show_header=True, header_style="bold magenta", expand=True)
        table.add_column(t("col_id"), style="bold cyan", width=6, justify="center")
        table.add_column(t("col_format"), style="bold white", width=25)
        table.add_column(t("col_desc"), style="bold yellow")
        
        for fid, fdetails in formats.items():
            table.add_row(str(fid), fdetails["name"], fdetails["desc"])
            
        console.print(table)
        
        choice = IntPrompt.ask(t("select_format_prompt"), choices=[str(i) for i in formats.keys()], default=1)
        return formats[choice]
    else:
        print(f"\n{t('available_formats')}:")
        for fid, fdetails in formats.items():
            print(f" [{fid}] {fdetails['name']:<25} - {fdetails['desc']}")
        print("-" * 80)
        choice = input(f"{t('select_format_prompt')} (1-{len(formats)}) [1]: ").strip()
        if not choice.isdigit():
            return formats[1]
        fid = int(choice)
        return formats.get(fid, formats[1])

def get_dpi_options():
    """DPI configurations."""
    return {
        1: {"name": t("dpi_default"), "value": None},
        2: {"name": t("dpi_low"), "value": 96},
        3: {"name": t("dpi_screen"), "value": 120},
        4: {"name": t("dpi_medium"), "value": 150},
        5: {"name": t("dpi_high"), "value": 300},
        6: {"name": t("dpi_ultra"), "value": 600},
        7: {"name": t("dpi_custom"), "value": "custom"}
    }

def select_dpi():
    """Render resolution / quality selection menu."""
    options = get_dpi_options()
    if HAS_RICH:
        table = Table(title=t("dpi_config"), show_header=True, header_style="bold magenta", expand=True)
        table.add_column(t("col_option"), style="bold cyan", width=8, justify="center")
        table.add_column(t("col_resolution"), style="bold white")
        
        for opid, opdetails in options.items():
            table.add_row(str(opid), opdetails["name"])
            
        console.print(table)
        choice = IntPrompt.ask(t("select_dpi_prompt"), choices=[str(i) for i in options.keys()], default=1)
        
        selected = options[choice]
        if selected["value"] == "custom":
            dpi_val = IntPrompt.ask(t("custom_dpi_prompt"), default=300)
            return dpi_val
        return selected["value"]
    else:
        print(f"\n{t('dpi_config')}:")
        for opid, opdetails in options.items():
            print(f" [{opid}] {opdetails['name']}")
        print("-" * 80)
        choice = input(f"{t('select_dpi_prompt')} (1-{len(options)}) [1]: ").strip()
        if not choice.isdigit():
            return None
        opid = int(choice)
        selected = options.get(opid, options[1])
        if selected["value"] == "custom":
            try:
                return int(input(f"{t('custom_dpi_prompt')}: "))
            except ValueError:
                return 300
        return selected["value"]

def select_theme():
    """Render theme selection menu."""
    if HAS_RICH:
        table = Table(title=t("integrated_themes"), show_header=True, header_style="bold magenta", expand=True)
        table.add_column(t("col_id"), style="bold cyan", width=6, justify="center")
        table.add_column(t("col_theme"), style="bold white")
        
        # None option
        table.add_row("0", t("theme_none"))
        # Render themes
        for idx, theme in enumerate(THEMES, 1):
            table.add_row(str(idx), theme)
                
        # Custom option
        table.add_row("C", t("custom_theme_option"))
        
        console.print(table)
        choices = [str(i) for i in range(len(THEMES) + 1)] + ['C', 'c']
        choice = Prompt.ask(t("select_theme_prompt"), choices=choices, default="0")
        
        if choice in ['C', 'c']:
            return Prompt.ask(t("custom_theme_prompt"))
        
        idx = int(choice)
        if idx == 0:
            return None
        return THEMES[idx - 1]
    else:
        print(f"\n{t('integrated_themes')}:")
        print(f" [0] {t('theme_none')}")
        for idx, theme in enumerate(THEMES, 1):
            print(f" [{idx}] {theme}")
        print(f" [C] {t('custom_theme_option')}")
        print("-" * 80)
        choice = input(f"{t('select_theme_prompt')} (0-{len(THEMES)} / C) [0]: ").strip()
        if choice.lower() == 'c':
            return input(f"{t('custom_theme_prompt')}: ").strip()
        if not choice.isdigit():
            return None
        idx = int(choice)
        if 0 < idx <= len(THEMES):
            return THEMES[idx - 1]
        return None

def get_pasted_code():
    """Handle interactive pasting of PlantUML code."""
    print_message(t("paste_instructions_header"), "info")
    print(t("paste_instructions_footer"))
    print("-" * 60)
    lines = []
    while True:
        try:
            line = input()
            lines.append(line)
            if line.strip().lower() == 'fin' or '@enduml' in line:
                break
        except EOFError:
            break
        except KeyboardInterrupt:
            return None
    print("-" * 60)
    
    code = "\n".join(lines)
    if not code.strip():
        return None
        
    return code

def select_options():
    """Output Options wrapper (preserved from legacy structure)."""
    return None

def toggle_language(config):
    """Toggle language setting, save configuration, and update active language."""
    new_lang = "es" if get_language() == "en" else "en"
    config["language"] = new_lang
    save_config(config)
    set_language(new_lang)
    print_message(t("lang_changed"), "success")
    if HAS_RICH:
        Prompt.ask(f"\n{t('press_enter')}")
    else:
        input(f"\n{t('press_enter')}")

def main():
    """Main execution loop for the CLI toolbox."""
    while True:
        # 1. Load config and language
        config = load_config()
        set_language(config.get("language", "en"))
        
        clear_screen()
        print_header(os.getcwd())
        
        # 2. Check PlantUML JAR
        jar_path = config.get("jar_path", "")
        # Resolve path relative to the toolbox installation folder
        INSTALL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        full_jar_path = jar_path if os.path.isabs(jar_path) else os.path.join(INSTALL_DIR, jar_path)
        
        if not (jar_path and os.path.isfile(full_jar_path)):
            print_message(t("jar_not_found"), "error")
            print_message(t("jar_placement_info"), "info")
            if HAS_RICH:
                custom_jar = Prompt.ask(t("enter_custom_jar"), default="")
            else:
                custom_jar = input(f"{t('enter_custom_jar')}: ").strip()
                
            if custom_jar and os.path.exists(custom_jar):
                abs_custom_jar = os.path.abspath(custom_jar)
                config["jar_path"] = abs_custom_jar
                save_config(config)
                full_jar_path = abs_custom_jar
            else:
                print_message(t("no_jar_abort"), "error")
                break
        else:
            print_message(t("jar_detected", path=full_jar_path), "success")
            
        # Scan folder for diagrams
        files = get_puml_files()
        
        # 3. File Selection Menu
        target_file = select_file(files)
        if not target_file:
            print_message(t("exit_toolbox"), "info")
            break
            
        # Language switch flow
        if target_file == "language":
            toggle_language(config)
            continue
            
        # Paste code flow
        if target_file == "paste":
            code = get_pasted_code()
            if not code:
                print_message(t("no_code_warning"), "warning")
                if HAS_RICH:
                    Prompt.ask(f"\n{t('press_enter')}")
                else:
                    input(f"\n{t('press_enter')}")
                continue
            
            created_file = sanitize_and_save_pasted_code(
                code=code,
                has_rich=HAS_RICH,
                console=console if HAS_RICH else None,
                prompt_class=Prompt if HAS_RICH else None
            )
            print_message(t("file_generated_success", file=created_file), "success")
            target_file = created_file
            files.append(created_file)
            
        # 4. Select Format Menu
        clear_screen()
        print_header(os.getcwd())
        format_info = select_format()
        
        # 5. DPI Selection (Interactive if enabled, else uses default_dpi)
        dpi = config.get("default_dpi", 600)
        if config.get("enable_dpi_selection", False):
            clear_screen()
            print_header(os.getcwd())
            dpi = select_dpi()
        
        # 6. Theme Selection (Interactive if enabled, else uses default_theme)
        theme = config.get("default_theme", None)
        if config.get("enable_theme_selection", False):
            clear_screen()
            print_header(os.getcwd())
            theme = select_theme()
        
        # 7. Select Options (Output Dir)
        clear_screen()
        print_header(os.getcwd())
        output_dir = select_options()
        
        # 8. Conversion Execution
        clear_screen()
        print_header(os.getcwd())
        
        if target_file == "all":
            print_message(t("processing_all"), "info")
        else:
            print_message(t("processing_single", file=target_file), "info")
            
        success, error_msg = run_conversion(
            jar_path=full_jar_path,
            target_file=target_file,
            format_flag=format_info["flag"],
            dpi=dpi,
            theme=theme,
            output_dir=output_dir,
            files=files,
            has_rich=HAS_RICH,
            console=console if HAS_RICH else None
        )
        
        # Log success/failure details
        if success:
            dest = output_dir if output_dir else "current directory" if get_language() == 'en' else "el directorio actual"
            print_message(t("conversion_success", format=format_info['name'], dest=dest), "success")
        else:
            print_message(t("conversion_error_header"), "error")
            if HAS_RICH:
                console.print(Panel(error_msg, title=t("error_details_title"), border_style="red"))
            else:
                print("=" * 80)
                print(f"{t('error_details_title')}:")
                print(error_msg)
                print("=" * 80)
                
        # 9. Continue or Exit Prompt
        if HAS_RICH:
            cont = Confirm.ask(f"\n{t('continue_confirm')}", default=True)
            if not cont:
                print_message(t("exit_toolbox"), "info")
                break
        else:
            cont_resp = input(f"\n{t('continue_confirm')} (s/n) [s]: ").strip().lower()
            if cont_resp == 'n' or cont_resp == 'no':
                print(t("exit_toolbox"))
                break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{t('exit_toolbox')}")
        sys.exit(0)
