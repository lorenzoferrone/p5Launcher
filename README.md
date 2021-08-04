Write your p5js sketches with python and automatically launch them in a new window just by running your script.
* no html
* no javascript
* just python

Also included: autoreload on save!

# Installation
`pip3 install p5Launcher` or `pip install p5Launcher` dependending on your python configuration (requires python3, only tested on >= 3.8)

# Usage

open your favourite editor and create a new file `<script.py>` and save it wherever you want

```
import p5Launcher

def setup():
    createCanvas(windowWidth, windowHeight)
    stroke(100, 100, 100, 100)
    noFill()


def draw():
    background(100)
    ellipse(mouseX, mouseY, 30, 30)
```

open a terminal, move to the folder where you saved the script and run it with `python3 <script.py>` or just use your editor "run" button if available.

A new window should popup with your sketch!

Bonus: try changing your code and saving, the changes should automatically be reflected in the sketch.

# How does it work?
This package just wraps the library pyp5js which itself leverages transcrypt to compile python to javascript.
