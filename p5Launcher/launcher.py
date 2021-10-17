'''questo è il file che viene lanciato quando il modulo viene importato
e lo sketch (python) viene eseguito con python3 sketch_name.py
'''
import webview
import asyncio
import pathlib
import os, threading, inspect, sys, glob
from livereload import Server, shell

from .compiler import _compile



def launch_server(folder, name, loop):

    print(f"{folder=}, {name=}")

    name_without_ext = name.replace('.py', '')
    package_dir = pathlib.Path(__file__).parent.resolve()

    asyncio.set_event_loop(loop)
    server = Server()

    exclude = set(glob.glob(f'{folder}/{name_without_ext}/**/**/*.py'))
    include = set(glob.glob(f'{folder}/**/**/*.py'))

    print(include - exclude)

    server.watch(f'{folder}/**/!({name_without_ext})/**/*.py', shell(f'python3 compiler.py {folder} {name}', cwd=package_dir))
    root = name.replace('.py', '')
    server.serve(root=root, liveport=35729)  

def launch_window(sketch_name, width=1100, height=700):
    webview.create_window(sketch_name, url='http://127.0.0.1:5500', width=width, height=height)        
    webview.start(debug=True)          


def _setup(width=1100, height=700):

    try:
        width = int(sys.argv[1])
        height = int(sys.argv[2])
    except:
        print('no or invalid parameters')
    
    sketch_name = inspect.stack()[-1].filename

    if "/" in sketch_name:
        sketch_name = sketch_name.split("/")[-1]
        
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
    # window = webview.create_window(sketch_name, url='http://127.0.0.1:5500', width=1100, height=700)        
    # webview.start(debug=True) 
    launch_window(sketch_name, width, height)
    

_setup()