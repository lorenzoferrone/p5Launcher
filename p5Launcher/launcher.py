'''questo è il file che viene lanciato quando il modulo viene importato
e lo sketch (python) viene eseguito con python3 sketch_name.py
'''
import webview
import asyncio
from pathlib import Path
import threading, inspect, sys, glob
from livereload import Server, shell

from .compiler import _compile



def launch_server(path, loop):

    sketch_folder = path.parent

    package_dir = Path(__file__).parent.resolve()

    asyncio.set_event_loop(loop)
    server = Server()

    exclude = set(glob.glob(f'{sketch_folder}/{path.stem}/**/*.py', recursive=True))
    include = set(glob.glob(f'{sketch_folder}/**/*.py', recursive=True))

    for file in set(include) - set(exclude): 
        server.watch(file, shell(f'python3 compiler.py {path}', cwd=package_dir))
    
    server.serve(root=path.stem, liveport=35729)  


def launch_window(sketch_name, width=1100, height=700):
    webview.create_window(sketch_name, url='http://127.0.0.1:5500', width=width, height=height)        
    webview.start(debug=True)          


def _setup(width=1100, height=700):

    # read command line args and configuration
    try:
        width = int(sys.argv[1])
        height = int(sys.argv[2])
    except:
        print('no or invalid parameters')
    
    # read sketch path/name from import stack anc convert to pathlib for easier manipulation
    sketch_path = Path(inspect.stack()[-1].filename)
    
    # compilo il codice
    _compile(sketch_path)

    # creo un eventloop
    loop = asyncio.new_event_loop()

    # lancio il server di livereload
    t = threading.Thread(target=launch_server, args=(sketch_path, loop))
    t.setDaemon(True)
    t.start()

    # creo una finestra e lancio il webview
    launch_window(sketch_path.name, width, height)
    

_setup()