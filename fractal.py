#!/usr/bin/python3

# Bruno Mendes da Costa - 9779433
# Josué Grâce Kabongo Kalala - 9770382

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

SCALE=SCALE_X=SCALE_Y=SCALE_Z=1.0
X_ANGLE=Y_ANGLE=Z_ANGLE=30.0
SCALE_INC=0.05
SCALE_MAX=1.0
SCALE_MIN=0.025	
ROTATION_INC=2.0

# Captura os eventos do teclado.
def keyPressEvent(key, x, y) :		
	global X_ANGLE, Y_ANGLE, Z_ANGLE	
	global SCALE, ENABLE_RENDER

	# Comandos de Escala.
	if key == b'+':
		SCALE = min(SCALE_MAX, SCALE + SCALE_INC)
	elif key == b'-':
		SCALE = max(SCALE_MIN, SCALE - SCALE_INC)

	# Comandos de Rotação.
	elif key == b'l':
		X_ANGLE = (X_ANGLE + ROTATION_INC) % 360
	elif key == b'j':
		X_ANGLE = (X_ANGLE - ROTATION_INC) % 360
	elif key == b'k':
		Y_ANGLE = (Y_ANGLE + ROTATION_INC) % 360
	elif key == b'i':
		Y_ANGLE = (Y_ANGLE - ROTATION_INC) % 360
	elif key == b'o':
		Z_ANGLE = (Z_ANGLE + ROTATION_INC) % 360
	elif key == b'u':
		Z_ANGLE = (Z_ANGLE - ROTATION_INC) % 360
	
	# Reset da interface.
	elif key == b'r':
		X_ANGLE=Y_ANGLE=Z_ANGLE=30.0		
		SCALE=SCALE_X=SCALE_Y=SCALE_Z=1.0 		
		SCALE=1.0	
	
	# Exit (ESC).
	elif key == b'\x1b': 		
		print('Saindo do programa...')
		exit(0)

	# Redesenha o objeto.
	glutPostRedisplay()	

def display():    
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	# Define a matriz de projeção ortogonal.
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(-2, 2, -2, 2, -2, 100)
	
	# Operação de Rotação.
	glRotatef(X_ANGLE, 1, 0, 0)
	glRotatef(Y_ANGLE, 0, 1, 0)
	glRotatef(Z_ANGLE, 0, 0, 1)

	# Operação de Escala.
	glScalef(SCALE_X * SCALE, SCALE_Y * SCALE, SCALE_Z * SCALE)
	
	# Define uma cor para o cubo.
	glColor3f(1,1,1)

	# Desenha o cubo.
	#glutSolidCube(1)
	glutWireCube(1)

	# Troca os buffers.
	glutSwapBuffers()

def init():	
	# Utilização de 2 buffers.
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH) 
	# Define as dimensões da janela.
	glutInitWindowSize(800, 600)    
	# Define posição inicial da janela na tela.
	glutInitWindowPosition(250, 100)
	glutCreateWindow("Fractal")    
	glEnable(GL_DEPTH_TEST);
	glClearColor(0, 0, 0, 0);

if __name__ == '__main__':    
	glutInit()
	init()		
	glutDisplayFunc(display)
	glutKeyboardFunc(keyPressEvent)   	
	glutMainLoop()