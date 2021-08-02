import subprocess
import os, ast
import sys


def add_import_to_file(input_path, output_path, line_to_skip=None, line_to_write=None):
    with open(input_path) as input_file, open(output_path, 'w') as output_file:
        lines = input_file.readlines()
    
        # cerco l'indice della prima riga del file che contiene la riga da skippare
        if line_to_skip:
            for i, line in enumerate(lines):
                if line_to_skip in line:
                    starting_index = i + 1
                    break
        else:
            starting_index = 0
        # la prima riga che copio è l'import di pyp5js
        if line_to_write:
            output_file.write(line_to_write)
        
        output_file.writelines(lines[starting_index:])


def get_files_to_import(sketch_path):
    '''legge il file presente <path> e identifica i file (nella stessa cartella) 
    che vengono importati'''

    # TODO: implementare il resolve di moduli che non sono necessariamente
    # nella stessa cartella (magari stanno dentro altre sottocartelle) 
       
    with open(sketch_path) as f:
        code = f.read()
    
    nodes = ast.parse(code)

    # cerco i file da importare
    imports = []
    for node in ast.walk(nodes):
        if type(node) == ast.ImportFrom:
            import_file = f"{node.module}.py"
            imports.append(import_file)
        if type(node) == ast.Import:   # multiple imports, like "import module1, module2"
            for _import in node.names:
                import_file = f"{_import.name}.py"
                imports.append(import_file)
   
    for import_file in imports:
        # controllo esista veramente
        if os.path.isfile(import_file):
            yield import_file


def _compile(sketch_folder, sketch_name):
    '''compile the python code found in <sketch_folder>/<sketch_name>.py
    and also all the python code imported by that file
    '''
    
    env = os.environ
    env["SKETCHBOOK_DIR"] = sketch_folder

    sketch_path = f"{sketch_folder}/{sketch_name}"    
    
    # rimuovo l'estensione .py da sketch_name
    name = sketch_name.replace('.py', '')

    # la folder che conterrà il codice js compilato
    js_folder = f'{sketch_folder}/{name}'

    # creo il progetto se non è gia presente:
    if not os.path.isdir(js_folder):
        subprocess.call(f'pyp5js new -i transcrypt {name}', env=env, shell=True)

    # poi ci copio dentro il file main 
    # (a cui levo le prime righe, che servono per lanciare questo script, e aggiungo l'import della
    # libreria pyp5js che fa funzionare il tutto)
    add_import_to_file(
        input_path=sketch_path, 
        output_path=f'{js_folder}/{sketch_name}', 
        line_to_skip='p5Launcher', 
        line_to_write='from pyp5js import *\n'
    )

    # faccio il parsing dell'ast per trovare anche i file da imporate
    # e copio anch'essi nella cartella
    imports = get_files_to_import(sketch_path)
    for file_to_import in imports:
        input_path = f"{sketch_folder}/{file_to_import}"
        output_path = f"{js_folder}/{file_to_import}"
        add_import_to_file(input_path, output_path, 
            line_to_write='from pyp5js import *\n'
        )

    # infine lancio il processo di transcrypting di tutta la folder
    subprocess.call(f'pyp5js compile {name}', env=env, shell=True)



if __name__ == '__main__':
    folder, name = sys.argv[1:]
    _compile(folder, name)



