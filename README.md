Write your p5js sketches with python and automatically launch them in a new window just by running your script.
* no html
* no javascript
* just python

Also included: autoreload on save!

# Usage
```import p5Launcher

def setup():
    createCanvas(windowWidth, windowHeight)
    stroke(100, 100, 100, 100)
    noFill()


def draw():
    background(100)
    ellipse(mouseX, mouseY, 30, 30)
```


# How does it work?
this package just wraps the library pyp5js which itself uses transcrypt to compile python to javascript