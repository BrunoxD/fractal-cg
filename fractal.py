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
MAX_DEPTH=3
FRAC_DEPTH=2
ANCHORS=[]
SIZES=[]

# Desenha as legendas na tela.
def drawSubtitles():
	text = 'Subtitles'  +\
		'\nl: +x_angle' +\
		'\nk: +y_angle' +\
		'\no: +z_angle' +\
		'\nj: -x_angle' +\
		'\ni: -y_angle' +\
		'\nu: -z_angle' +\
		'\nw: +depth' 	+\
		'\ns: -depth' 	+\
		'\n+: +zoom' 	+\
		'\n-: -zoom' 	+\
		'\nr: RESET' 	+\
		'\nESC: exit' 	+\
		'\n\nParameters:' +\
		'\nDepth: ('+ str(FRAC_DEPTH) + '/' + str(MAX_DEPTH) + ')' +\
		'\nX_Angle=' + str(round(X_ANGLE, 2)) +\
		'\nY_Angle=' + str(round(Y_ANGLE, 2)) +\
		'\nZ_Angle=' + str(round(Z_ANGLE, 2)) +\
		'\nZoom=' + str(round(SCALE*100)) + '%'
	glColor3f(0.75, 0.75, 0.10)
	glLoadIdentity()
	
	yPos = 0.90
	yInc = 30.0/600
	glRasterPos2f(-0.98, yPos)
	for ch in text:
		if ch != '\n':
			glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(ch))
		else:
			yPos -= yInc
			glRasterPos2f(-0.98, yPos)

# Captura os eventos do teclado.
def keyPressEvent(key, x, y) :		
	global X_ANGLE, Y_ANGLE, Z_ANGLE	
	global SCALE, FRAC_DEPTH, ANCHORS, SIZES

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

	# Nível de profundidade.
	elif key == b'w':
		FRAC_DEPTH = min(FRAC_DEPTH + 1, MAX_DEPTH)		
		regenerate()
	elif key == b's':
		FRAC_DEPTH = max(FRAC_DEPTH-1, 0)
		regenerate()
	
	# Reset da interface.
	elif key == b'r':
		X_ANGLE=Y_ANGLE=Z_ANGLE=30.0		
		SCALE=SCALE_X=SCALE_Y=SCALE_Z=1.0 				
		SCALE=1.0	
		FRAC_DEPTH=2
		regenerate()
	
	# Exit (ESC).
	elif key == b'\x1b': 		
		print('Saindo do programa...')
		exit(0)

	# Redesenha o objeto.
	glutPostRedisplay()	

# Regera as dimensões do cubo para uma nova profundidade.
def regenerate():
	ANCHORS.clear()
	SIZES.clear()
	generate(FRAC_DEPTH, 1.5, [0, 0, 0])

# Desenha cada um dos cubos armazenados.
def drawFractal():
	for i in range(len(ANCHORS)): 
		drawCube(i) 			

# Gera dimensões dos cubos via recursão.
def generate(depth, size, anchor):
	if(depth <= 0):
		ANCHORS.append(anchor) # Lista de vetores de origens.
		SIZES.append(size) # Lista de deslocamentos.
		return		
	for i in range(3):
		for j in range(3):
			for k in range(3):
				if([i, j] != [1, 1] and [i, k] != [1, 1] and [j, k] != [1, 1]):
					generate(depth-1, size/3, [anchor[0]+(i-1)*size/3, anchor[1]+(j-1)*size/3, anchor[2]+(k-1)*size/3])

# Frente, Traseira, Direita, Esquerda, Topo, Base
def drawCube(n):
	pos=SIZES[n]/2 # Variável auxiliar para o posicionamento dos vetores

	# Lado multicolorido - FRENTE
	glBegin(GL_POLYGON); 	
	glColor3f(1.0, 0.0, 0.0) # P1 é vermelho
	glVertex3f(ANCHORS[n][0]+pos, ANCHORS[n][1]-pos, ANCHORS[n][2]-pos)      	
	glColor3f(0.0, 1.0, 0.0) # P2 é verde
	glVertex3f(ANCHORS[n][0]+pos, ANCHORS[n][1]+pos, ANCHORS[n][2]-pos)      	
	glColor3f(0.0, 0.0, 1.0) # P3 é azul
	glVertex3f(ANCHORS[n][0]-pos, ANCHORS[n][1]+pos, ANCHORS[n][2]-pos)      	
	glColor3f(1.0, 0.0, 1.0) # P4 é roxo
	glVertex3f(ANCHORS[n][0]-pos, ANCHORS[n][1]-pos, ANCHORS[n][2]-pos)
	glEnd();

	# Lado branco - TRASEIRA
	glBegin(GL_POLYGON);
	glColor3f(1.0,  1.0, 1.0);
	glVertex3f(ANCHORS[n][0]+pos, ANCHORS[n][1]-pos, ANCHORS[n][2]+pos);
	glVertex3f(ANCHORS[n][0]+pos, ANCHORS[n][1]+pos, ANCHORS[n][2]+pos);
	glVertex3f(ANCHORS[n][0]-pos, ANCHORS[n][1]+pos, ANCHORS[n][2]+pos);
	glVertex3f(ANCHORS[n][0]-pos, ANCHORS[n][1]-pos, ANCHORS[n][2]+pos);
	glEnd();

	# Lado roxo - DIREITA
	glBegin(GL_POLYGON);
	glColor3f(1.0,  0.0,  1.0);
	glVertex3f(ANCHORS[n][0]+pos, ANCHORS[n][1]-pos, ANCHORS[n][2]-pos);
	glVertex3f(ANCHORS[n][0]+pos, ANCHORS[n][1]+pos, ANCHORS[n][2]-pos);
	glVertex3f(ANCHORS[n][0]+pos, ANCHORS[n][1]+pos, ANCHORS[n][2]+pos);
	glVertex3f(ANCHORS[n][0]+pos, ANCHORS[n][1]-pos, ANCHORS[n][2]+pos);
	glEnd();

	# Lado verde - ESQUERDA
	glBegin(GL_POLYGON);
	glColor3f(0.0,  1.0,  0.0);
	glVertex3f(ANCHORS[n][0]-pos, ANCHORS[n][1]-pos, ANCHORS[n][2]+pos);
	glVertex3f(ANCHORS[n][0]-pos, ANCHORS[n][1]+pos, ANCHORS[n][2]+pos);
	glVertex3f(ANCHORS[n][0]-pos, ANCHORS[n][1]+pos, ANCHORS[n][2]-pos);
	glVertex3f(ANCHORS[n][0]-pos, ANCHORS[n][1]-pos, ANCHORS[n][2]-pos);
	glEnd();

	# Lado azul - TOPO
	glBegin(GL_POLYGON);
	glColor3f(0.0,  0.0,  1.0);
	glVertex3f(ANCHORS[n][0]+pos,  ANCHORS[n][1]+pos, ANCHORS[n][2]+pos);
	glVertex3f(ANCHORS[n][0]+pos,  ANCHORS[n][1]+pos, ANCHORS[n][2]-pos);
	glVertex3f(ANCHORS[n][0]-pos,  ANCHORS[n][1]+pos, ANCHORS[n][2]-pos);
	glVertex3f(ANCHORS[n][0]-pos,  ANCHORS[n][1]+pos, ANCHORS[n][2]+pos);
	glEnd();

	# Lado vermelho - BASE
	glBegin(GL_POLYGON);
	glColor3f(1.0,  0.0,  0.0);
	glVertex3f(ANCHORS[n][0]+pos, ANCHORS[n][1]-pos, ANCHORS[n][2]-pos);
	glVertex3f(ANCHORS[n][0]+pos, ANCHORS[n][1]-pos, ANCHORS[n][2]+pos);
	glVertex3f(ANCHORS[n][0]-pos, ANCHORS[n][1]-pos, ANCHORS[n][2]+pos);
	glVertex3f(ANCHORS[n][0]-pos, ANCHORS[n][1]-pos, ANCHORS[n][2]-pos);
	glEnd();

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
	drawFractal()

	# Desenha as legendas.
	drawSubtitles()

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
	generate(FRAC_DEPTH, 1.5, [0, 0, 0])
	glutInit()
	init()		
	glutDisplayFunc(display)	
	glutKeyboardFunc(keyPressEvent)   	
	glutMainLoop()