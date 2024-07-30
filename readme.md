# 3D Cube with Rainbow Borders

This project demonstrates a 3D rotating cube with rainbow-colored borders using Pygame Community Edition and OpenGL.

This is a personal project to test the functionality of Pygame and PyOpenGL.

![project Screenshot](screenshot.png)

## Features

- 3D rotating cube rendered with OpenGL
- Rainbow-colored rectangles at the top and bottom of the window
- Smooth color transitions in the rainbow borders

## Requirements

- Python 3.x
- Pygame Community Edition
- PyOpenGL

## Installation

1. Clone this repository or download the source code.
2. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

## Usage

Run the script using Python:

```
python cube.py
```

## Controls

- Close the window to exit the program

## How it works

The program uses Pygame Community Edition to create a window and handle events, and OpenGL for 3D rendering. The main components are:

1. A 3D cube that rotates continuously
2. Two rainbow-colored rectangles at the top and bottom of the window
3. Color transitions that create a moving rainbow effect

The cube is defined by its vertices and edges, and drawn using OpenGL lines. The rainbow effect is achieved by calculating HSV colors and converting them to RGB.

## Customization

You can modify various aspects of the program:

- Adjust the window size by changing the `display` tuple in the `main()` function
- Modify the cube's rotation speed by changing the values in the `glRotatef()` call
- Adjust the rainbow effect speed by modifying the hue increment value

## LICENSE

[CC0 1.0 Universal](LICENSE)