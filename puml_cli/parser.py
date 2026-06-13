import os
import textwrap
from .i18n import t

SUPPORTED_EXTENSIONS = ['.puml', '.wsd', '.plantuml']

def get_puml_files():
    """Scan the current working directory for PlantUML files."""
    files = []
    for f in os.listdir('.'):
        if os.path.isfile(f) and any(f.lower().endswith(ext) for ext in SUPPORTED_EXTENSIONS):
            files.append(f)
    return sorted(files)

def get_internal_diagram_name(puml_file):
    """
    Parse the PlantUML file to find any custom name specified
    on the @startuml line.
    """
    base = os.path.splitext(os.path.basename(puml_file))[0]
    try:
        with open(puml_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('@startuml'):
                    parts = line.split()
                    if len(parts) > 1 and not parts[1].startswith('@') and not parts[1].startswith('-') and not parts[1].startswith('/'):
                        name = parts[1]
                        # Sanitize Windows invalid characters in name
                        for char in ['"', "'", '<', '>', ':', '|', '?', '*', '/', '\\']:
                            name = name.replace(char, '')
                        name = name.strip()
                        if name:
                            return name
    except Exception:
        pass
    return base

def get_output_base_name(puml_file):
    """Get the base name of a file without the extension."""
    return os.path.splitext(os.path.basename(puml_file))[0]

def sanitize_and_save_pasted_code(code, has_rich, console, prompt_class):
    """
    Clean, format, and save pasted PlantUML code.
    If the diagram lacks a name, prompt the user for it.
    """
    # 1. Dedent to remove common leading indentation
    code = textwrap.dedent(code)
    
    # 2. Split and clean individual lines (strip trailing spaces/tabs)
    lines = [line.rstrip() for line in code.split('\n')]
    
    # 3. Clean consecutive empty lines inside the diagram
    cleaned_lines = []
    prev_empty = False
    for line in lines:
        is_empty = not line.strip()
        if is_empty:
            if not prev_empty:
                cleaned_lines.append("")
                prev_empty = True
        else:
            cleaned_lines.append(line)
            prev_empty = False
    lines = cleaned_lines
    
    # 4. Strip leading/trailing empty lines
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
        
    if not lines:
        lines = ["@startuml", "@enduml"]
        
    # Fix comments starting with '%%' to PlantUML style "'"
    for idx, line in enumerate(lines):
        if line.strip().startswith('%%'):
            lines[idx] = line.replace('%%', "'", 1)
            
    # 5. Find and normalize @startuml
    start_line_idx = -1
    for idx, line in enumerate(lines):
        if '@startuml' in line.lower():
            start_line_idx = idx
            break
            
    if start_line_idx == -1:
        lines.insert(0, "@startuml")
        start_line_idx = 0
    else:
        orig = lines[start_line_idx].strip()
        if orig.lower().startswith('@startuml'):
            lines[start_line_idx] = orig
            
    # Check if there's a name after @startuml
    start_line = lines[start_line_idx]
    parts = start_line.split()
    
    has_name = len(parts) > 1 and not parts[1].startswith('@') and not parts[1].startswith('-') and not parts[1].startswith('/')
    
    if has_name:
        diag_name = " ".join(parts[1:])
        for char in ['"', "'", '<', '>', ':', '|', '?', '*', '/', '\\']:
            diag_name = diag_name.replace(char, '')
        diag_name = diag_name.strip()
        if not diag_name:
            has_name = False
            
    if not has_name:
        # Prompt user for diagram name since it is not defined
        print(f"\n[INFO] {t('missing_name_info')}")
        if has_rich:
            diag_name = prompt_class.ask(t("enter_name_prompt"), default="diagram")
        else:
            diag_name = input(f"{t('enter_name_prompt')} [diagram]: ").strip()
        
        if not diag_name:
            diag_name = "diagram"
            
        # Sanitize diagram name
        for char in ['"', "'", '<', '>', ':', '|', '?', '*', '/', '\\']:
            diag_name = diag_name.replace(char, '')
        diag_name = diag_name.strip()
        if not diag_name:
            diag_name = "diagram"
            
    # Force the name in the @startuml line
    lines[start_line_idx] = f"@startuml {diag_name}"
    
    # 6. Ensure @enduml at the end is normalized
    enduml_idx = -1
    for idx, line in enumerate(lines):
        if '@enduml' in line.lower():
            enduml_idx = idx
            break
            
    if enduml_idx == -1:
        lines.append("@enduml")
    else:
        orig_end = lines[enduml_idx].strip()
        if orig_end.lower().startswith('@enduml'):
            lines[enduml_idx] = "@enduml"
            
    # 7. Fix repeat-while syntax without repeat block
    has_repeat_while = any("repeat while" in l for l in lines)
    has_repeat = any(l.strip() == "repeat" for l in lines)
    if has_repeat_while and not has_repeat:
        inserted = False
        # Try to put 'repeat' after 'start'
        for idx, line in enumerate(lines):
            if line.strip() == "start":
                lines.insert(idx + 1, "repeat")
                inserted = True
                break
        if not inserted:
            lines.insert(start_line_idx + 1, "repeat")
            
    # Assemble final code and write to file
    final_code = "\n".join(lines)
    filename = f"{diag_name}.puml"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(final_code)
        
    return filename
