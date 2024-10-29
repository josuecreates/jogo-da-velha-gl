from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

# Variáveis globais
game_board = np.zeros((3, 3))  # Tabuleiro 3x3
current_player = 1
light_on = True
camera_pos = [0, 1.5, 5]  # Posição inicial da câmera
current_camera = 0
player_colors = [(1.0, 0, 0), (0, 0, 1.0)]  # Cores dos jogadores (X, O)
sensor_active = False

def reset_game():
    global game_board, current_player
    game_board.fill(0)
    current_player = 1

def check_win():
    for i in range(3):
        if np.all(game_board[i, :] == current_player) or np.all(game_board[:, i] == current_player):
            return True
    if game_board[0, 0] == current_player == game_board[1, 1] == game_board[2, 2] or \
       game_board[0, 2] == current_player == game_board[1, 1] == game_board[2, 0]:
        return True
    return False

def draw_board():
    glColor3f(1.0, 1.0, 1.0)
    for i in range(-1, 2):
        glBegin(GL_LINES)
        glVertex3f(-1.5, 0, i)
        glVertex3f(1.5, 0, i)
        glVertex3f(i, 0, -1.5)
        glVertex3f(i, 0, 1.5)
        glEnd()

def draw_pieces():
    for i in range(3):
        for j in range(3):
            if game_board[i, j] == 1:
                glColor3fv(player_colors[0])
                glPushMatrix()
                glTranslatef(i - 1, 0.1, j - 1)
                glutSolidTorus(0.1, 0.4, 10, 10)
                glPopMatrix()
            elif game_board[i, j] == 2:
                glColor3fv(player_colors[1])
                glPushMatrix()
                glTranslatef(i - 1, 0.1, j - 1)
                glutSolidCube(0.8)
                glPopMatrix()

def switch_camera():
    if current_camera == 0:  # Primeira pessoa
        gluLookAt(*camera_pos, 0, 0, 0, 0, 1, 0)
    elif current_camera == 1:  # Câmera fixa A
        gluLookAt(3, 3, 3, 0, 0, 0, 0, 1, 0)
    else:  # Câmera fixa B
        gluLookAt(-3, 3, 3, 0, 0, 0, 0, 1, 0)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    switch_camera()

    # Luz fixa
    light_position = [1.0, 1.0, 1.0, 0.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    if light_on:
        glEnable(GL_LIGHT1)
    else:
        glDisable(GL_LIGHT1)

    draw_board()
    draw_pieces()

    # Sensor de proximidade
    proximity_sensor()

    glutSwapBuffers()

def keyboard(key, x, y):
    global light_on, current_camera
    if key == b'r': reset_game()
    elif key == b'l': light_on = not light_on
    elif key == b'1': current_camera = 0
    elif key == b'2': current_camera = 1
    elif key == b'3': current_camera = 2
    glutPostRedisplay()

def mouse(button, state, x, y):
    global current_player, sensor_active
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        i = x // (glutGet(GLUT_WINDOW_WIDTH) // 3)
        j = 2 - (y // (glutGet(GLUT_WINDOW_HEIGHT) // 3))  # Invertendo Y para o tabuleiro
        if game_board[i, j] == 0:
            game_board[i, j] = current_player
            if check_win():
                print(f"Player {current_player} wins!")
                reset_game()
            else:
                current_player = 2 if current_player == 1 else 1
                sensor_active = not sensor_active
    glutPostRedisplay()

def init():
    glEnable(GL_DEPTH_TEST)  # Habilita o teste de profundidade
    glEnable(GL_LIGHTING)  # Habilita a iluminação
    glEnable(GL_LIGHT0)  # Habilita a luz 0
    glEnable(GL_COLOR_MATERIAL)  # Habilita a cor do material

    # Definindo a cor de fundo
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Preto

    # Parâmetros da luz
    light_diffuse = [1.0, 1.0, 1.0, 1.0]
    light_position = [0.0, 3.0, 2.0, 1.0]
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

def proximity_sensor():
    global sensor_active
    if sensor_active:
        glColor3f(0.0, 1.0, 0.0)
        glPushMatrix()
        glTranslatef(1.0, 0.1, 1.0)
        glutSolidSphere(0.2, 15, 15)
        glPopMatrix()

def update(value):
    glutPostRedisplay()
    glutTimerFunc(100, update, 0)

# Configuração inicial do GLUT e OpenGL
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(600, 600)
glutCreateWindow("Jogo da Velha 3D em OpenGL")
init()

glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouse)
glutTimerFunc(100, update, 0)

glutMainLoop()