#!/usr/bin/env python3
import os
import glob
import re
import json

def list_tasks():
    print("\n📚 Verfügbare Aufgaben:")
    
    # Score-Datei laden
    scores = {}
    if os.path.exists('.scores.json'):
        try:
            with open('.scores.json', 'r') as f:
                scores = json.load(f)
        except:
            pass
    
    aufgaben = []
    if os.path.exists('aufgaben'):
        for file in glob.glob('aufgaben/a*.py'):
            name = os.path.basename(file)[:-3]
            match = re.match(r'a(\d+)_(.+)', name)
            if match:
                num = int(match.group(1))
                title = match.group(2).replace('_', ' ').title()
                has_test = os.path.exists(f'tests/{name}.py')
                solved = scores.get(name, {}).get('solved', False)
                attempts = scores.get(name, {}).get('attempts', 0)
                aufgaben.append((num, name, title, has_test, solved, attempts))
    
    aufgaben.sort()
    
    # Statistik
    total = len(aufgaben)
    solved_count = sum(1 for _, _, _, _, solved, _ in aufgaben if solved)
    
    print(f"\n📊 Fortschritt: {solved_count}/{total} Aufgaben bestanden")
    if total > 0:
        percentage = int((solved_count / total) * 100)
        bar_length = 30
        filled = int((percentage / 100) * bar_length)
        bar = '█' * filled + '░' * (bar_length - filled)
        print(f"[{bar}] {percentage}%")
    
    print()
    
    for i, (num, name, title, has_test, solved, attempts) in enumerate(aufgaben, 1):
        # Status-Symbole
        solved_indicator = '✅' if solved else '❌'
        test_indicator = '🧪' if has_test else '  '
        
        # Versuche anzeigen (falls vorhanden)
        attempt_text = f" ({attempts}x)" if attempts > 0 else ""
        
        print(f'  {i:2d}. {solved_indicator} {test_indicator} {name} - {title}{attempt_text}')
    
    print()
    print("Legende:")
    print("  ✅ = Bestanden    ❌ = Noch offen    🧪 = Test verfügbar    (Nx) = Anzahl Versuche")
    print()

if __name__ == "__main__":
    list_tasks()