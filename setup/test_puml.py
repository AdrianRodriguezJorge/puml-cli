import unittest
import os
import sys
import tempfile
import shutil
import json

# Add project root directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from puml_cli.config import load_config, save_config
from puml_cli.i18n import t, set_language, get_language
from puml_cli.parser import get_puml_files

class TestPumlToolbox(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.old_dir = os.getcwd()
        os.chdir(self.temp_dir)
        
    def tearDown(self):
        os.chdir(self.old_dir)
        shutil.rmtree(self.temp_dir)
        
    def test_config_defaults(self):
        """Verify that default configurations are correctly loaded when config.json is absent."""
        config = load_config("test_config.json")
        self.assertEqual(config["jar_path"], "")
        self.assertEqual(config["default_dpi"], 600)
        self.assertFalse(config["enable_theme_selection"])
        self.assertEqual(config["language"], "en")
        
    def test_config_save_load(self):
        """Verify that user configurations are correctly persisted and reloaded."""
        config_file = "test_config.json"
        config = load_config(config_file)
        config["jar_path"] = "my_custom_plantuml.jar"
        config["language"] = "es"
        save_config(config, config_file)
        
        # Load again and verify values
        loaded = load_config(config_file)
        self.assertEqual(loaded["jar_path"], "my_custom_plantuml.jar")
        self.assertEqual(loaded["language"], "es")
        
    def test_i18n_translation(self):
        """Verify that lookups fetch the correct language strings."""
        # Test English
        set_language("en")
        self.assertEqual(get_language(), "en")
        title_en = t("title")
        self.assertIn("PLANTUML LOCAL", title_en.upper())
        
        # Test Spanish
        set_language("es")
        self.assertEqual(get_language(), "es")
        title_es = t("title")
        self.assertIn("CAJA DE HERRAMIENTAS", title_es.upper())
        
    def test_parser_puml_scan(self):
        """Verify that file scanner matches exactly puml/wsd/plantuml formats."""
        # Create dummy test files
        with open("diagram1.puml", "w") as f:
            f.write("@startuml\nBob -> Alice : hello\n@enduml")
        with open("diagram2.wsd", "w") as f:
            f.write("@startuml\nBob -> Alice : hello\n@enduml")
        with open("diagram3.txt", "w") as f:
            f.write("Plain text file")
            
        files = get_puml_files()
        self.assertIn("diagram1.puml", files)
        self.assertIn("diagram2.wsd", files)
        self.assertNotIn("diagram3.txt", files)

if __name__ == '__main__':
    unittest.main()
