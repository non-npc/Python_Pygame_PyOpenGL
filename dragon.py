import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from stl import mesh

def load_stl(file_name):
    try:
        mesh_data = mesh.Mesh.from_file(file_name)
        vertices = mesh_data.vectors.reshape(-1, 3)
        return vertices
    except Exception as e:
        print(f"Error loading STL file: {e}")
        return None

def create_vbo(vertices):
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    return vbo

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

def create_rainbow_gradient_colors(vertices):
    center = np.mean(vertices, axis=0)
    max_distance = np.max(np.linalg.norm(vertices - center, axis=1))

    colors = []
    for vertex in vertices:
        distance = np.linalg.norm(vertex - center)
        hue = distance / max_distance
        color = hsv_to_rgb(hue, 1, 1)
        colors.extend(color)

    return np.array(colors, dtype=np.float32)

def create_color_vbo(colors):
    color_vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, color_vbo)
    glBufferData(GL_ARRAY_BUFFER, colors.nbytes, colors, GL_STATIC_DRAW)
    return color_vbo

def draw_stl(vbo, color_vbo, vertex_count):
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)

    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glVertexPointer(3, GL_FLOAT, 0, None)

    glBindBuffer(GL_ARRAY_BUFFER, color_vbo)
    glColorPointer(3, GL_FLOAT, 0, None)

    glDrawArrays(GL_TRIANGLES, 0, vertex_count)

    glDisableClientState(GL_COLOR_ARRAY)
    glDisableClientState(GL_VERTEX_ARRAY)

def draw_rainbow_rectangle(x, y, width, height, hue):
    glBegin(GL_QUADS)
    for i in range(int(width)):
        color = hsv_to_rgb((hue + i/width) % 1, 1, 1)
        glColor3f(*color)
        glVertex2f(x + i, y)
        glVertex2f(x + i, y + height)
        glVertex2f(x + i + 1, y + height)
        glVertex2f(x + i + 1, y)
    glEnd()

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
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -20)

    glEnable(GL_DEPTH_TEST)

    clock = pygame.time.Clock()
    hue = 0

    stl_vertices = load_stl('cutedragon2.stl')
    if stl_vertices is None:
        print("Failed to load STL file. Exiting.")
        pygame.quit()
        quit()

    center = np.mean(stl_vertices, axis=0)
    max_dimension = np.max(np.max(stl_vertices, axis=0) - np.min(stl_vertices, axis=0))
    scale = 10.0 / max_dimension

    stl_vertices = (stl_vertices - center) * scale
    vbo = create_vbo(stl_vertices.astype(np.float32))
    vertex_count = len(stl_vertices)

    gradient_colors = create_rainbow_gradient_colors(stl_vertices)
    color_vbo = create_color_vbo(gradient_colors)

    rotation_x, rotation_y = 0, 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        # Draw 3D STL model
        glPushMatrix()
        glRotatef(rotation_x, 1, 0, 0)
        glRotatef(rotation_y, 0, 1, 0)
        draw_stl(vbo, color_vbo, vertex_count)
        glPopMatrix()

        rotation_x += 0.5
        rotation_y += 0.5

        # Switch to 2D mode for drawing rainbow rectangles
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, display[0], display[1], 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        # Draw rainbow rectangles
        rect_width = display[0] * 0.9
        rect_height = 50
        rect_x = (display[0] - rect_width) / 2

        draw_rainbow_rectangle(rect_x, 0, rect_width, rect_height, hue)
        draw_rainbow_rectangle(rect_x, display[1] - rect_height, rect_width, rect_height, hue)

        # Return to 3D mode
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

        pygame.display.flip()

        hue = (hue + 0.002) % 1
        clock.tick(60)

if __name__ == "__main__":
    main()