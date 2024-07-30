import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

def create_pyramid():
    vertices = [
        ( 0,  1,  0),  # top
        (-1, -1, -1),  # front left
        ( 1, -1, -1),  # front right
        ( 1, -1,  1),  # back right
        (-1, -1,  1)   # back left
    ]
    edges = [
        (0, 1), (0, 2), (0, 3), (0, 4),  # edges from top to base
        (1, 2), (2, 3), (3, 4), (4, 1)   # base edges
    ]
    return vertices, edges

def draw_pyramid(vertices, edges):
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def hsv_to_rgb(h, s, v):
    h_i = int(h*6)
    f = h*6 - h_i
    p = v * (1 - s)
    q = v * (1 - f*s)
    t = v * (1 - (1 - f) * s)
    if h_i == 0: r, g, b = v, t, p
    elif h_i == 1: r, g, b = q, v, p
    elif h_i == 2: r, g, b = p, v, t
    elif h_i == 3: r, g, b = p, q, v
    elif h_i == 4: r, g, b = t, p, v
    else: r, g, b = v, p, q
    return r, g, b

def draw_rainbow_rectangle_with_border(x, y, width, height, hue):
    # Draw filled rectangle
    glBegin(GL_QUADS)
    for i in range(int(width)):
        color = hsv_to_rgb((hue + i/width) % 1, 1, 1)
        glColor3f(*color)
        glVertex2f(x + i, y)
        glVertex2f(x + i, y + height)
        glVertex2f(x + i + 1, y + height)
        glVertex2f(x + i + 1, y)
    glEnd()

    # Draw border
    glLineWidth(2)
    glBegin(GL_LINE_LOOP)
    for i, vertex in enumerate([(x, y), (x + width, y), (x + width, y + height), (x, y + height)]):
        color = hsv_to_rgb((hue + i/4) % 1, 1, 1)
        glColor3f(*color)
        glVertex2f(*vertex)
    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    screen = pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    pygame.display.set_caption("Rotating Pyramid with Rainbow Borders")

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    clock = pygame.time.Clock()
    hue = 0

    # Create pyramid vertices and edges
    pyramid_vertices, pyramid_edges = create_pyramid()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        # Draw the rotating pyramid
        glColor3f(1, 1, 1)  # Set color to white
        draw_pyramid(pyramid_vertices, pyramid_edges)

        # Set up 2D drawing
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, display[0], display[1], 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        rect_width = display[0] * 0.9  # 90% of window width
        rect_height = 50
        rect_x = (display[0] - rect_width) / 2  # Center horizontally

        # Draw the rainbow rectangle with border at the top
        draw_rainbow_rectangle_with_border(rect_x, 0, rect_width, rect_height, hue)

        # Draw the matching rainbow rectangle with border at the bottom
        draw_rainbow_rectangle_with_border(rect_x, display[1] - rect_height, rect_width, rect_height, hue)

        # Restore 3D drawing
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

        pygame.display.flip()

        # Update hue for next frame
        hue = (hue + 0.002) % 1  # Slow down the color transition

        clock.tick(60)  # Limit to 60 FPS

if __name__ == "__main__":
    main()