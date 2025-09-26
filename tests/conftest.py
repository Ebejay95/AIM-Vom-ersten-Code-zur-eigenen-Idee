import pytest
import sys
import os
from io import StringIO
from unittest.mock import patch

# Aufgaben-Ordner zum Python Path hinzufügen
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

class TestHelper:
    @staticmethod
    def capture_output(func, *args, **kwargs):
        """Fängt die Ausgabe einer Funktion ab."""
        captured_output = StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured_output
        
        try:
            result = func(*args, **kwargs)
            output = captured_output.getvalue()
            return output, result
        finally:
            sys.stdout = old_stdout
    
    @staticmethod
    def import_aufgabe(aufgabe_name):
        """Importiert eine Aufgabe dynamisch."""
        try:
            module = __import__(f'aufgaben.{aufgabe_name}', fromlist=[aufgabe_name])
            return module
        except ImportError as e:
            pytest.fail(f"Aufgabe {aufgabe_name} konnte nicht importiert werden: {e}")
    
    @staticmethod
    def run_with_input(aufgabe_module, inputs):
        """Führt eine Aufgabe mit Mock-Inputs aus."""
        with patch('builtins.input', side_effect=inputs):
            if hasattr(aufgabe_module, 'main'):
                return TestHelper.capture_output(aufgabe_module.main)
            else:
                pytest.fail(f"Aufgabe hat keine main() Funktion")

@pytest.fixture
def helper():
    """Stellt Test-Helper zur Verfügung."""
    return TestHelper
