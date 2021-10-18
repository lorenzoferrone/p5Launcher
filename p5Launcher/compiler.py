import subprocess
import sys, os, ast
from pathlib import Path


def add_import_to_file(input_path, output_path, line_to_skip=None, line_to_write=None):

    os.makedirs(output_path.parent, exist_ok=True)
    with open(input_path) as input_file, open(output_path, 'w') as output_file:
        lines = input_file.readlines()

        if line_to_write:
            output_file.write(line_to_write)

        if line_to_skip:
            lines = [line for line in lines if line_to_skip not in line]
     
        output_file.writelines(lines)


def get_modules_to_import(sketch_path):
    '''legge il file <path> e identifica i moduli da importare'''

    with open(sketch_path) as f:
        code = f.read()

    # cerco gli import parsando il file
    nodes = ast.parse(code)
    for node in ast.walk(nodes):
        if type(node) == ast.ImportFrom:
            yield node.module
        if type(node) == ast.Import:   # multiple imports, like "import module1, module2"
            for _import in node.names:
                yield _import.name


def get_files_to_import(sketch_path):
    '''legge il file <path> e identifica i file (nella stessa cartella) 
    che vengono importati'''

    sketch_folder = sketch_path.parent
    modules = get_modules_to_import(sketch_path)

    # dai nomi trovo i file veri e propri, tenendo solo quelli nella stessa cartella
    for import_file in modules:
        spec = Path(import_file.replace(".", "/")).with_suffix('.py')
        spec = sketch_folder / spec
        if sketch_folder in spec.parents:
            if os.path.isfile(spec):
                yield spec.relative_to(sketch_folder)

    

def _compile(sketch_path):
    '''compile the python code found in <sketch_path>
    and also all the python code imported by that file
    '''

    sketch_name = sketch_path.name      # name + extension
    sketch_folder = sketch_path.parent  # containing folder
    name = sketch_path.stem             # name without extension
    
    env = os.environ
    env["SKETCHBOOK_DIR"] = str(sketch_folder)
    
    # la folder che conterrà il codice js compilato
    js_folder = sketch_folder / name

    # creo il progetto se non è gia presente:
    if not os.path.isdir(js_folder):
        subprocess.call(f'pyp5js new -i transcrypt {name}', env=env, shell=True)

    # poi ci copio dentro il file main 
    # (a cui levo le prime righe, che servono per lanciare questo script, e aggiungo l'import della
    # libreria pyp5js che fa funzionare il tutto)
    add_import_to_file(input_path=sketch_path, output_path=js_folder / sketch_name, line_to_skip='p5Launcher')

    # faccio il parsing dell'ast per trovare anche i file da imporate
    # e copio anch'essi nella cartella
    imports = get_files_to_import(sketch_path)

    for file_to_import in imports:
        input_path = sketch_folder / file_to_import
        output_path = js_folder / file_to_import.parent / file_to_import.name
        add_import_to_file(input_path, output_path, line_to_write='from pyp5js import *\n')

    # infine lancio il processo di transcrypting di tutta la folder
    subprocess.run(f'pyp5js compile {name}', env=env, shell=True, capture_output=True)



if __name__ == '__main__':
    path = sys.argv[1]
    _compile(Path(path))
