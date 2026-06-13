# Translation dictionary for internationalization (i18n)
# Supporting English (en) and Spanish (es)

TRANSLATIONS = {
    "en": {
        "title": "PLANTUML LOCAL CLI TOOLBOX",
        "working_dir": "Working Directory: {dir}",
        "info": "INFO",
        "success": "SUCCESS",
        "error": "ERROR",
        "warning": "WARNING",
        "detected_files": "Detected PlantUML Files",
        "col_option": "Option",
        "col_filename": "File Name",
        "col_size": "Size (Bytes)",
        "all_files": "All files",
        "paste_code_option": "Paste PlantUML code",
        "change_lang_option": "Change Language (Cambiar Idioma)",
        "exit_option": "Go back / Exit",
        "no_diagrams": "No diagram files detected",
        "select_file_prompt": "Select a file",
        "select_option_prompt_no_all": "Select an option (0-P, L)",
        "select_option_prompt_all": "Select an option (0-A/P, L)",
        "available_formats": "Available Export Formats",
        "col_id": "ID",
        "col_format": "Format",
        "col_desc": "Description",
        "select_format_prompt": "Select the output format",
        "dpi_config": "Resolution / Quality Configuration (DPI)",
        "col_resolution": "Resolution",
        "select_dpi_prompt": "Select quality / DPI",
        "custom_dpi_prompt": "Enter custom DPI value (e.g., 72, 200, 450)",
        "integrated_themes": "PlantUML Integrated Themes",
        "col_theme": "Theme",
        "custom_theme_option": "Write another custom theme...",
        "select_theme_prompt": "Select a theme",
        "custom_theme_prompt": "Enter the theme name (e.g. sketchy-outline, cerulean-outline)",
        "paste_instructions_header": "Paste your PlantUML code below.",
        "paste_instructions_footer": "To finish and confirm, write '@enduml' or write 'FIN' on a new line and press Enter:",
        "no_code_warning": "No code entered. Returning to menu...",
        "file_generated_success": "File generated successfully: {file}",
        "missing_name_info": "The pasted code does not define a diagram name after @startuml.",
        "enter_name_prompt": "Enter a name for the diagram (without extension)",
        "processing_all": "Processing all files in the directory...",
        "processing_single": "Processing file: {file}",
        "exist_rename": "Existing file renamed to: {file}",
        "exist_rename_error": "Could not rename existing file {file}: {err}",
        "conversion_success": "Diagram successfully generated in [bold green]{format}[/bold green] format and saved in [bold cyan]{dest}[/bold cyan]!",
        "conversion_error_header": "An error occurred while executing PlantUML:",
        "error_details_title": "Error Details",
        "continue_confirm": "Do you want to perform another conversion?",
        "exit_toolbox": "Goodbye! Exiting the toolbox...",
        "jar_not_found": "Could not find any plantuml*.jar file in the directory.",
        "jar_placement_info": "Make sure to place your PlantUML JAR file in this folder or configure it in config.json.",
        "enter_custom_jar": "Or enter the absolute path to the JAR file",
        "no_jar_abort": "Cannot proceed without the PlantUML JAR file.",
        "jar_detected": "JAR file detected: {path}",
        "lang_changed": "Language changed to English.",
        "press_enter": "Press Enter to continue...",
        "resolution_warning": "PlantUML requires Apache FOP and Batik external libraries to export to PDF.\nTo enable offline PDF export:\n 1. Download Apache FOP (includes fop.jar, batik-all.jar, etc.).\n 2. Place these .jar files in the same folder as PlantUML.\nAlternative: Export to SVG/PNG and print/save to PDF from there.",
        "auto_open_error": "Could not open the generated file automatically: {err}",
        
        # Formats Descriptions
        "f_png_name": "PNG (Standard image)",
        "f_png_desc": "Rasterized image for web or documents",
        "f_svg_name": "SVG (Vector graphics)",
        "f_svg_desc": "Scalable vector, ideal for web or viewing",
        "f_eps_name": "EPS (Encapsulated PostScript)",
        "f_eps_desc": "Vector format, ideal for LaTeX documents",
        "f_txt_name": "TXT (Plain ASCII art)",
        "f_txt_desc": "Diagram in simple ASCII text",
        "f_utxt_name": "UTXT (Unicode ASCII art)",
        "f_utxt_desc": "Diagram in text with stylized Unicode characters",
        "f_html_name": "HTML (Interactive classes)",
        "f_html_desc": "Interactive HTML page (available for class diagrams)",
        "f_vdx_name": "VDX (Visio XML)",
        "f_vdx_desc": "Microsoft Visio compatible file format",
        "f_xmi_name": "XMI (UML Interchange)",
        "f_xmi_desc": "XML interchange format for class diagrams",
        
        # DPI Descriptions
        "dpi_default": "Default (Normal DPI)",
        "dpi_low": "Low resolution (96 DPI)",
        "dpi_screen": "Screen resolution (120 DPI)",
        "dpi_medium": "Medium resolution (150 DPI)",
        "dpi_high": "High resolution / Print (300 DPI)",
        "dpi_ultra": "Ultra resolution (600 DPI)",
        "dpi_custom": "Custom...",
        
        # Themes Descriptions
        "theme_none": "None (Default PlantUML)"
    },
    "es": {
        "title": "CAJA DE HERRAMIENTAS - CONVERSOR LOCAL PLANTUML",
        "working_dir": "Directorio de trabajo: {dir}",
        "info": "INFO",
        "success": "ÉXITO",
        "error": "ERROR",
        "warning": "ADVERTENCIA",
        "detected_files": "Archivos PlantUML Detectados",
        "col_option": "Opción",
        "col_filename": "Nombre del Archivo",
        "col_size": "Tamaño (Bytes)",
        "all_files": "Todos los archivos",
        "paste_code_option": "Pegar código PlantUML",
        "change_lang_option": "Cambiar Idioma (Change Language)",
        "exit_option": "Volver al menú anterior / Salir",
        "no_diagrams": "No se detectaron archivos de diagrama",
        "select_file_prompt": "Selecciona un archivo",
        "select_option_prompt_no_all": "Selecciona una opción (0-P, L)",
        "select_option_prompt_all": "Selecciona una opción (0-A/P, L)",
        "available_formats": "Formatos de Exportación Disponibles",
        "col_id": "ID",
        "col_format": "Formato",
        "col_desc": "Descripción",
        "select_format_prompt": "Selecciona el formato de salida",
        "dpi_config": "Configuración de Resolución / Calidad (DPI)",
        "col_resolution": "Resolución",
        "select_dpi_prompt": "Selecciona la calidad / DPI",
        "custom_dpi_prompt": "Escribe el valor de DPI personalizado (ej. 72, 200, 450)",
        "integrated_themes": "Temas Integrados de PlantUML",
        "col_theme": "Tema",
        "custom_theme_option": "Escribir otro tema personalizado...",
        "select_theme_prompt": "Selecciona un tema",
        "custom_theme_prompt": "Escribe el nombre del tema (ej. sketchy-outline, cerulean-outline)",
        "paste_instructions_header": "Pega tu código PlantUML a continuación.",
        "paste_instructions_footer": "Para finalizar y confirmar, escribe '@enduml' o escribe 'FIN' en una nueva línea y presiona Enter:",
        "no_code_warning": "No se ingresó código. Volviendo al menú...",
        "file_generated_success": "Archivo generado con éxito: {file}",
        "missing_name_info": "El código pegado no tiene un nombre de diagrama definido después de @startuml.",
        "enter_name_prompt": "Ingresa el nombre para el diagrama (sin extensión)",
        "processing_all": "Procesando todos los archivos del directorio...",
        "processing_single": "Procesando archivo: {file}",
        "exist_rename": "Archivo existente renombrado a: {file}",
        "exist_rename_error": "No se pudo renombrar el archivo existente {file}: {err}",
        "conversion_success": "¡Diagrama generado con éxito en formato [bold green]{format}[/bold green] y guardado en [bold cyan]{dest}[/bold cyan]!",
        "conversion_error_header": "Ocurrió un error al ejecutar PlantUML:",
        "error_details_title": "Detalles del Error",
        "continue_confirm": "¿Deseas realizar otra conversión?",
        "exit_toolbox": "¡Hasta luego! Saliendo de la caja de herramientas...",
        "jar_not_found": "No se pudo encontrar ningún archivo plantuml*.jar en el directorio.",
        "jar_placement_info": "Asegúrate de colocar tu archivo JAR de PlantUML en esta carpeta o configurarlo en config.json.",
        "enter_custom_jar": "O ingresa la ruta absoluta al archivo JAR",
        "no_jar_abort": "No se puede proceder sin el JAR de PlantUML.",
        "jar_detected": "Archivo JAR detectado: {path}",
        "lang_changed": "Idioma cambiado a Español.",
        "press_enter": "Presiona Enter para continuar...",
        "resolution_warning": "PlantUML requiere de las librerías externas de Apache FOP y Batik para exportar a PDF.\nPara habilitarlo offline:\n 1. Descarga Apache FOP (que incluye fop.jar, batik-all.jar, etc.).\n 2. Coloca dichos archivos .jar en la misma carpeta que PlantUML.\nComo alternativa inmediata, puedes exportar a formato SVG o PNG y abrirlo/imprimirlo a PDF.",
        "auto_open_error": "No se pudo abrir el archivo automáticamente: {err}",
        
        # Formats Descriptions
        "f_png_name": "PNG (Imagen estándar)",
        "f_png_desc": "Imagen rasterizada para web o documentos",
        "f_svg_name": "SVG (Gráficos vectoriales)",
        "f_svg_desc": "Vectorial escalable, ideal para web o visor",
        "f_eps_name": "EPS (PostScript encapsulado)",
        "f_eps_desc": "Vectorial, ideal para incluir en documentos LaTeX",
        "f_txt_name": "TXT (Arte ASCII plano)",
        "f_txt_desc": "Diagrama en texto ASCII simple",
        "f_utxt_name": "UTXT (Arte ASCII con Unicode)",
        "f_utxt_desc": "Diagrama en texto con caracteres Unicode estilizados",
        "f_html_name": "HTML (Clases interactivo)",
        "f_html_desc": "Página HTML interactiva (disponible para diagramas de clases)",
        "f_vdx_name": "VDX (XML de Visio)",
        "f_vdx_desc": "Archivo compatible con Microsoft Visio",
        "f_xmi_name": "XMI (Intercambio UML)",
        "f_xmi_desc": "Formato XML de intercambio para diagramas de clases",
        
        # DPI Descriptions
        "dpi_default": "Por defecto (DPI normal)",
        "dpi_low": "Baja resolución (96 DPI)",
        "dpi_screen": "Resolución de pantalla (120 DPI)",
        "dpi_medium": "Resolución media (150 DPI)",
        "dpi_high": "Alta resolución / Impresión (300 DPI)",
        "dpi_ultra": "Ultra resolución (600 DPI)",
        "dpi_custom": "Personalizado...",
        
        # Themes Descriptions
        "theme_none": "Ninguno (Por defecto de PlantUML)"
    }
}

# Active language
_lang = "en"

def set_language(lang_code):
    """Set the active translation language."""
    global _lang
    if lang_code in TRANSLATIONS:
        _lang = lang_code

def get_language():
    """Get the active translation language."""
    return _lang

def t(key, **kwargs):
    """
    Get the translated string for the given key in the active language.
    Pass kwargs to format variables inside the string.
    """
    translation_set = TRANSLATIONS.get(_lang, TRANSLATIONS["en"])
    template = translation_set.get(key, TRANSLATIONS["en"].get(key, key))
    try:
        return template.format(**kwargs)
    except Exception:
        return template
