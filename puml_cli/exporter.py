import os
import sys
import glob
import subprocess
from .i18n import t
from .parser import get_output_base_name, get_internal_diagram_name

def run_conversion(jar_path, target_file, format_flag, dpi, theme, output_dir, files=None, has_rich=False, console=None):
    """
    Constructs the PlantUML command line arguments, handles existing file backups,
    runs the Java process, performs name alignment post-processing, and opens the result.
    """
    files_to_process = []
    if target_file == "all":
        if files:
            files_to_process = files
        else:
            files_to_process = glob.glob("*.puml")
    else:
        files_to_process = [target_file]

    # Map flags to extensions
    ext_map = {
        "--png": ".png",
        "--svg": ".svg",
        "--eps": ".eps",
        "--txt": ".txt",
        "--utxt": ".utxt",
        "--html": ".html",
        "--vdx": ".vdx",
        "--xmi": ".xmi"
    }
    ext = ext_map.get(format_flag, ".png")
    
    # 1. Back up existing files by renaming them with numeric suffixes
    for f in files_to_process:
        base_out = get_output_base_name(f)
        out_dir = output_dir if output_dir else ""
        output_path = os.path.join(out_dir, f"{base_out}{ext}")
        if os.path.exists(output_path):
            counter = 1
            while True:
                candidate_name = f"{base_out}_{counter}{ext}"
                candidate_path = os.path.join(out_dir, candidate_name)
                if not os.path.exists(candidate_path):
                    break
                counter += 1
            try:
                os.rename(output_path, candidate_path)
                msg_renamed = t("exist_rename", file=candidate_name)
                if has_rich:
                    console.print(f"[bold yellow]{t('warning')}:[/bold yellow] {msg_renamed}")
                else:
                    print(f"[{t('warning')}] {msg_renamed}")
            except Exception as e:
                msg_err = t("exist_rename_error", file=output_path, err=e)
                if has_rich:
                    console.print(f"[bold red]{t('error')}:[/bold red] {msg_err}")
                else:
                    print(f"[{t('error')}] {msg_err}")

    # 2. Build Java Command
    args = ["java", "-jar", jar_path, "-charset", "UTF-8"]
    
    # Add format flag
    args.append(format_flag)
    
    # Add DPI if specified
    if dpi:
        args.extend(["-dpi", str(dpi)])
        
    # Add Theme if specified
    if theme:
        args.extend(["-theme", theme])
        
    # Add Output Directory if specified
    if output_dir:
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except Exception as e:
                msg_mkdir_err = f"Could not create folder {output_dir}: {e}"
                if has_rich:
                    console.print(f"[bold red]{t('error')}:[/bold red] {msg_mkdir_err}")
                else:
                    print(f"[{t('error')}] {msg_mkdir_err}")
        args.extend(["--output-dir", output_dir])
        
    # Add target files
    if target_file == "all":
        if files:
            args.extend(files)
        else:
            args.append("*.puml")
    else:
        args.append(target_file)
        
    # Print execution command log
    msg_executing = f"{t('processing_single', file=' '.join(args))}"
    if has_rich:
        console.print(f"[bold cyan]{t('info')}:[/bold cyan] Running: {cmd_to_string(args)}")
    else:
        print(f"[{t('info')}] Running: {cmd_to_string(args)}")
    
    # 3. Run Subprocess
    success = False
    error_msg = ""
    
    try:
        if has_rich:
            status_text = "[bold green]Generating diagram with PlantUML...[/bold green]" if t("info") == "INFO" else "[bold green]Generando diagrama con PlantUML...[/bold green]"
            with console.status(status_text):
                process = execute_process(args)
        else:
            print("Generating..." if t("info") == "INFO" else "Generando...")
            process = execute_process(args)
                
        if process.returncode == 0:
            success = True
            
            # 4. Post-processing: rename outputs if internal @startuml name differs from file name
            for f in files_to_process:
                base_out = get_output_base_name(f)
                internal_name = get_internal_diagram_name(f)
                if internal_name != base_out:
                    out_dir = output_dir if output_dir else ""
                    gen_path = os.path.join(out_dir, f"{internal_name}{ext}")
                    target_path = os.path.join(out_dir, f"{base_out}{ext}")
                    if os.path.exists(gen_path):
                        try:
                            if os.path.exists(target_path):
                                os.remove(target_path)
                            os.rename(gen_path, target_path)
                        except Exception as e:
                            msg_rename_warning = f"Could not rename internal name generated file {gen_path} to {target_path}: {e}"
                            if has_rich:
                                console.print(f"[bold yellow]{t('warning')}:[/bold yellow] {msg_rename_warning}")
                            else:
                                print(f"[{t('warning')}] {msg_rename_warning}")
        else:
            success = False
            error_msg = process.stderr or process.stdout
            if error_msg and "UnsupportedOperationException: PDF" in error_msg:
                error_msg += f"\n\n{t('resolution_warning')}"
    except Exception as e:
        success = False
        error_msg = str(e)
        
    # 5. Auto-open output file
    if success and target_file != "all" and len(files_to_process) == 1:
        f = files_to_process[0]
        base_out = get_output_base_name(f)
        out_dir = output_dir if output_dir else ""
        output_path = os.path.join(out_dir, f"{base_out}{ext}")
        if os.path.exists(output_path):
            try:
                abs_path = os.path.abspath(output_path)
                if os.name == 'nt':
                    os.startfile(abs_path)
                elif sys.platform == 'darwin':
                    subprocess.run(["open", abs_path], check=False)
                else:
                    subprocess.run(["xdg-open", abs_path], check=False)
            except Exception as e:
                msg_open_warning = t("auto_open_error", err=e)
                if has_rich:
                    console.print(f"[bold yellow]{t('warning')}:[/bold yellow] {msg_open_warning}")
                else:
                    print(f"[{t('warning')}] {msg_open_warning}")

    return success, error_msg

def cmd_to_string(args):
    """Safely format command line arguments for printing."""
    return " ".join(f'"{a}"' if ' ' in a or '(' in a or ')' in a else a for a in args)

def execute_process(args):
    """Run process adapting to Windows cmd wrapper rules."""
    if os.name == 'nt':
        cmd_str = cmd_to_string(args)
        # Always run with cmd.exe /c to ensure termination and compatibility with global rules
        return subprocess.run(f'cmd.exe /c "{cmd_str}"', stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    else:
        return subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
