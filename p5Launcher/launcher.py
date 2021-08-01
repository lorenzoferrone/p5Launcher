'''questo è il file che viene lanciato quando il modulo viene importato
e lo sketch (python) viene eseguito con python3 sketch_name.py
'''

import webview
import asyncio
import pathlib
import os,  threading, inspect
from livereload import Server, shell

from .compiler import _compile


def launch_server(folder, name, loop):

    package_dir = pathlib.Path(__file__).parent.resolve()

    asyncio.set_event_loop(loop)
    server = Server()
    server.watch(f'{folder}/*.py', shell(f'python3 compiler.py {folder} {name}', cwd=package_dir))
    root = name.replace('.py', '')
    server.serve(root=root, liveport=35729)        


if __name__ != '__main__':

    # trovo il nome della cartella che ospita QUESTO package
    package_dir = pathlib.Path(__file__).parent.resolve()

    # trovo il nome del file .py (compresa l'estensione) che importa questo script
    # ispeziono lo stack delle chiamate e trovo il file con nome diverso dall'init di questo package
    # e il cui nome non inizi con "<"
    for frame in inspect.stack()[1:]:
        sketch_name = frame.filename
        if sketch_name[0] != '<' and sketch_name != f'{package_dir}/__init__.py':
            break
    
    # get the folder from which the main script is imported
    sketch_folder = os.getcwd()
    
    # compilo il codice
    _compile(sketch_folder, sketch_name)

    # creo un eventloop
    loop = asyncio.new_event_loop()

    # lancio il server di livereload
    t = threading.Thread(target=launch_server, args=(sketch_folder, sketch_name, loop))
    t.setDaemon(True)
    t.start()

    # creo una finestra e lancio il webview
    window = webview.create_window(sketch_name, url='http://127.0.0.1:5500', width=1100, height=700)        
    webview.start(debug=True) 
    