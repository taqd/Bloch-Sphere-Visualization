#Title: Qubit Visualization using a Bloch Sphere
#Author: Tyler Dwyer
#Email: tdwyer@ece.ubc.ca

from __future__ import division, print_function
from visual import *
from numpy import matrix
from numpy import linalg
import wx
import cmath
import math

DEBUG = False
DEBUGU = True

#Qubit transformation matrices
I = matrix([[1+0j,0],[0,1]]) #Inverse
H = 1/math.sqrt(2) * matrix( [[1+0j,1],[1,-1]]) #Hadamard
X = matrix([[0,1+0j],[1,0]]) #PauliX
Y = matrix([[0,-1j],[1j,0]]) #PauliY
Z = matrix([[1+0j,0],[0,-1]]) #PauliZ
S = matrix([[1+0j,0],[0,1j]]) #Phase
T = matrix([[1,0],[0,exp(1j*(pi/4))]]) #PI/8
sN = 1/math.sqrt(2) * matrix( [[1+0j,-1],[1,1]]) #Sqrt Not

#Variable Initialization
r = 100 # Radius
polarCoor = matrix([0.0, 0.0]) #Polar coordinates
qubit = matrix([1+0j, 0+0j]).T #Qubit Amplitudes
   
def setVector(theta,phi): #Sets a qubit to a position
    global polarCoor
    polarCoor[0,0] = theta
    polarCoor[0,1] = phi
    
    #Calculate Cartesian coordinates
    x = ((math.cos(phi) * math.sin(theta)))
    y = ((math.sin(phi) * math.sin(theta)))
    z = ((math.cos(theta)))
    
    #Put world-frame cartesian coordinates back onto bloch sphere frame
    position = vector(x,y,z)
    point.pos = qubitFrame.world_to_frame(position*r)
   
def setAmplitudes(alpha, beta):
    global qubit
    qubit[0] = alpha
    qubit[1] = beta
    
   
def applyTransformation(U):
    global qubit
    #Get Amplitudes
    Q = qubit[:]

    #Apply transformation
    alpha = vdot(U[:,0][0,0],Q[0,0])
    beta = vdot(U[:,1][0,0],Q[0,0])     
    QPrime = matrix([alpha, beta]).T
    
    #Set the new amplitudes
    qubit = QPrime[:]
    
    
def updatePosition():
    #Updates the all positions (arrow & rings) based upon point position
    pointer.axis = point.pos
    
    #Find the point position in world frame
    xPos = qubitFrame.frame_to_world(point.pos).x
    yPos = qubitFrame.frame_to_world(point.pos).y
    zPos = qubitFrame.frame_to_world(point.pos).z
    
    #Move and scale rings accordingly
    xRing.pos.x = xPos
    yRing.pos.y = yPos
    zRing.pos.z = zPos
    try:
        xRing.radius = math.sqrt(r**2 - xPos**2)
        yRing.radius = math.sqrt(r**2 - yPos**2)
        zRing.radius = math.sqrt(r**2 - zPos**2)
    except:
        a=1
    #Find polar angles, Get Amplitudes, and update labels
    theta = math.atan2(xPos,zPos)
    phi = ((2*pi) - math.atan2(yPos,xPos)) % (2*pi)
    setDataLabels(qubit[0],qubit[1], theta, phi)
    #setVector(theta,phi)
        
def setDataLabels(alpha, beta, theta, phi):
    a = str(round(alpha.real,3)) + '+' + str(round(alpha.imag,3)) + 'i' 
    b = str(round(beta.real,3)) + '+' + str(round(beta.imag,3)) + 'i'
    c = str(round((alpha.real**2),3)) + '+' + str(round((alpha.imag**2),3)) + 'i' 
    d = str(round((beta.real**2),3)) + '+' + str(round((beta.imag**2),3)) + 'i'
    label = ('Alpha:   (' + a + ') \nBeta: (' + b + ')')
    dataText1.SetLabel(label)
    label= ('Alpha^2: (' + c + ') \nBeta^2: (' + d + ')')
    dataText1a.SetLabel(label)
    a = str(round(theta.real,3))
    b = str(round(phi.real,3))
    c = str(round(theta.real / pi,3))
    d = str(round(phi.real / pi,3))
    e = str(round(math.degrees(theta.real),0))
    f = str(round(math.degrees(phi.real),0))
    label = ('Theta: ' + a + '\nTheta/Pi: ' + c + '\nTheta(Deg): ' + e)
    dataText2.SetLabel(label)
    label = ('Phi: ' + b + '\nPhi/Pi: ' + d + '\nPhi(Deg): ' + f)
    dataText2a.SetLabel(label)
    
    
#Gates
def setHadamard(evt):
    print('Hadamard') 
    applyTransformation(H)
    for i in range(0,128):
        rate(128)
        qubitFrame.rotate(axis=(1/math.sqrt(2),0,1/math.sqrt(2)), angle=pi/128) 
        updatePosition()        
    
def setPauliX(evt):
    print('Pauli X')
    applyTransformation(X)
    for i in range(0,128):
        rate(128)
        qubitFrame.rotate(axis=(1,0,0), angle=pi/128) 
        updatePosition()  

    

def setPauliY(evt):
    print('Pauli Y')
    applyTransformation(Y)
    for i in range(0,128):
        rate(128)
        qubitFrame.rotate(axis=(0,1,0), angle=(pi)/128)
        updatePosition()  
 

def setPauliZ(evt):
    print('Pauli Z')
    applyTransformation(Z)
    for i in range(0,128):
       rate(128)
       qubitFrame.rotate(axis=(0,0,1), angle=pi/128) 
       updatePosition()  
       

def setPhase(evt):
    print('Phase')
    applyTransformation(S)
    for i in range(0,128):
        rate(128)
        qubitFrame.rotate(axis=(0,0,1), angle=-1*(pi/2)/128) 
        updatePosition()

def setPI8(evt):
    print('PI 8')
    applyTransformation(T)
    for i in range(0,128):
        rate(128)
        qubitFrame.rotate(axis=(0,0,1), angle=-1*(pi/4)/128) 
        updatePosition()

def setsNot(evt):
    print('sqrt Not')
    applyTransformation(sN)
    for i in range(0,128):
        rate(128)
        qubitFrame.rotate(axis=(0,1,0), angle=1*(pi/4)/128) 
        updatePosition() 
        

def setTheta(evt):
    thetaValue = thetaSlider.GetValue()
    thetaSliderLab.SetLabel('Theta (Deg): ' + str(thetaValue))
    setVector(math.radians(thetaValue),polarCoor[0,1])
    setAmplitudes(0,0)
    updatePosition()
    
    
def setPhi(evt):
    phiValue = phiSlider.GetValue()
    phiSliderLab.SetLabel('Phi (Deg): ' + str(phiValue))
    setVector(polarCoor[0,0],math.radians(phiValue))
    setAmplitudes(0,0)
    updatePosition()
    
def setqZero(evt):
    setVector(0,0.0)
    setAmplitudes(1,0)
    applyTransformation(I)
    updatePosition()
    
def setqOne(evt):
    setVector(pi,0)
    setAmplitudes(0,1)
    applyTransformation(I)
    updatePosition()
    
def setqPos(evt):
    setqZero(wx.EVT_SHOW)
    setHadamard(wx.EVT_SHOW)
    
def setqNeg(evt):
    setqOne(wx.EVT_SHOW)
    setHadamard(wx.EVT_SHOW)


#The window
wWidth = 310
wHeight = 725
M = 720
L = 10
d = 20
Top = 40
TopB = 15 


#w = window(width=wWidth, height=wHeight,menus=True, title='Bloch Sphere')
#display(window=w, x=d, y=d, width=L-2*d, height=L-2*d, forward=(1,-1,0))
#display(x=1024, y=0, width=M, height=M, forward=(-1,-.5,-.5))

w = window(width=wWidth, height=wHeight,menus=True, title='Bloch Sphere')
#disp = display(window=w,width=2*d, height=2*d, forward=(1,-1,0))
disp = display(window=w,x=d, y=d, width=M, height=M, forward=(-1,-.5,-.5))
disp2 = display(x=0, y=0, width=M, height=M, forward=(-1,-.5,-.5))

local_light(pos=(r*2,r*2,0), color=color.white)
local_light(pos=(r*-2,r*2,0), color=color.white)
local_light(pos=(r*2,r*-2,0), color=color.white)
local_light(pos=(r*-2,r*-2,0), color=color.white)

#Buttons, Text, Window Setup
bSize = 50;
p = w.panel
title = wx.StaticText(p, pos=(L*2,0), size=(300,25), label='Qubit Bloch Sphere',style=wx.ALIGN_CENTRE)
title.SetFont(wx.Font(14, wx.MODERN, wx.NORMAL, wx.BOLD))

about1 = wx.StaticText(p, pos=(L,wHeight-150), size=(400,25), label='Created By: Tyler Dwyer',style=wx.ALIGN_LEFT)
about1.SetFont(wx.Font(8, wx.MODERN, wx.NORMAL, wx.NORMAL))

about2 = wx.StaticText(p, pos=(L,wHeight-130), size=(400,25), label='Email: tdwyer@sfu.ca',style=wx.ALIGN_LEFT)
about2.SetFont(wx.Font(8, wx.MODERN, wx.NORMAL, wx.NORMAL))
about3 = wx.StaticText(p, pos=(L,wHeight-110), size=(400,25), label='Web: www.sfu.ca\~tdwyer',style=wx.ALIGN_LEFT)
about3.SetFont(wx.Font(8, wx.MODERN, wx.NORMAL, wx.NORMAL))

about3 = wx.StaticText(p, pos=(wWidth/2-110,wHeight-90), size=(400,25), label='Simon Fraser University',style=wx.ALIGN_LEFT)
about3.SetFont(wx.Font(8, wx.MODERN, wx.NORMAL, wx.NORMAL))


#Row Zero/One
wx.StaticText(p, pos=(L+0*bSize,0*bSize+Top), label='Base States:',style=wx.ALIGN_LEFT)
qZero = wx.Button(p, label='|0>', pos=(L+0*bSize,1*bSize+TopB), size=(bSize,bSize))
qOne = wx.Button(p, label='|1>', pos=(L+1*bSize,1*bSize+TopB), size=(bSize,bSize))

wx.StaticText(p, pos=(L+3*bSize,0*bSize+Top), label='Superposition:',style=wx.ALIGN_LEFT)
qPos = wx.Button(p, label='|+>', pos=(L+3*bSize,1*bSize+TopB), size=(bSize,bSize))
qNeg = wx.Button(p, label='|->', pos=(L+4*bSize,1*bSize+TopB), size=(bSize,bSize))

#Row Two/Three
wx.StaticText(p, pos=(L+0*bSize,2*bSize+Top), label='Hadamard',style=wx.ALIGN_LEFT)
hadamard = wx.Button(p, label='H', pos=(L+0*bSize,3*bSize+TopB), size=(bSize,bSize))

wx.StaticText(p, pos=(L+2*bSize,2*bSize+Top), label='Pauli',style=wx.ALIGN_LEFT)
pauliX = wx.Button(p, label='X', pos=(L+2*bSize,3*bSize+TopB), size=(bSize,bSize))
pauliY = wx.Button(p, label='Y', pos=(L+3*bSize,3*bSize+TopB), size=(bSize,bSize))
pauliZ = wx.Button(p, label='Z', pos=(L+4*bSize,3*bSize+TopB), size=(bSize,bSize))

#Row Four/Five
wx.StaticText(p, pos=(L+0*bSize,4*bSize+Top), label='Phase',style=wx.ALIGN_LEFT)
phase = wx.Button(p, label='S', pos=(L+0*bSize,5*bSize+TopB), size=(bSize,bSize))

wx.StaticText(p, pos=(L+2*bSize,4*bSize+Top), label='Pi/8',style=wx.ALIGN_LEFT)
pi8 = wx.Button(p, label='T', pos=(L+2*bSize,5*bSize+TopB), size=(bSize,bSize))

wx.StaticText(p, pos=(L+4*bSize,4*bSize+Top), label='Sqrt(Not)',style=wx.ALIGN_LEFT)
sNot = wx.Button(p, label='sN', pos=(L+4*bSize,5*bSize+TopB), size=(bSize,bSize))

#Row Six/Seven
thetaSliderLab = wx.StaticText(p, pos=(L+0*bSize,6*bSize+Top), label='Theta (Deg):',style=wx.ALIGN_LEFT)
thetaSlider = wx.Slider(p, pos=(L+0*bSize,7*bSize+TopB), size=(5*bSize,20), minValue=0, maxValue=179)
thetaSlider.Bind(wx.EVT_SCROLL, setTheta)

phiSliderLab = wx.StaticText(p, pos=(L+0*bSize,7*bSize+Top), label='Phi (Deg):',style=wx.ALIGN_LEFT)
phiSlider = wx.Slider(p, pos=(L+0*bSize,8*bSize+TopB), size=(5*bSize,20), minValue=0, maxValue=359)
phiSlider.Bind(wx.EVT_SCROLL, setPhi)

#Row Eight/Nine
dataText1 = wx.StaticText(p, pos=(L,8*bSize+Top), label='Loading ...',style=wx.ALIGN_LEFT)
dataText2 = wx.StaticText(p, pos=(L,9*bSize+Top), label='Loading ...',style=wx.ALIGN_LEFT)
dataText1a = wx.StaticText(p, pos=(L+2.75*bSize,8*bSize+Top), label='Loading ...',style=wx.ALIGN_LEFT)
dataText2a = wx.StaticText(p, pos=(L+2.75*bSize,9*bSize+Top), label='Loading ...',style=wx.ALIGN_LEFT)

#Button Bindings
hadamard.Bind(wx.EVT_BUTTON, setHadamard)
pauliX.Bind(wx.EVT_BUTTON, setPauliX)
pauliY.Bind(wx.EVT_BUTTON, setPauliY)
pauliZ.Bind(wx.EVT_BUTTON, setPauliZ)
phase.Bind(wx.EVT_BUTTON, setPhase)
pi8.Bind(wx.EVT_BUTTON, setPI8)
sNot.Bind(wx.EVT_BUTTON, setsNot)
qZero.Bind(wx.EVT_BUTTON, setqZero)
qOne.Bind(wx.EVT_BUTTON, setqOne)
qPos.Bind(wx.EVT_BUTTON, setqPos)
qNeg.Bind(wx.EVT_BUTTON, setqNeg)

#The Qubit
sceneFrame = frame()
qubitFrame = frame(frame = sceneFrame)
#floor = box (pos=(0,-r,0), length=r*2, height=r/1000, width=r*2, color=color.cyan)
ball = sphere (frame = qubitFrame, pos=(0,0,0), radius=r, material=materials.earth, opacity=.5)
pointer = arrow(frame = qubitFrame, pos=(0,0,0), axis=(0,0,r), shaftwidth=r/25, color=color.red)
point = sphere (frame = qubitFrame, pos=(0,0,r), radius=r/25, color=color.red) 
xRing = ring(frame = sceneFrame, pos=(1,0,0),axis=(1,0,0), radius=r, thickness=r/100, color=color.green)
yRing = ring(frame = sceneFrame, pos=(0,1,0),axis=(0,1,0), radius=r, thickness=r/100, color=color.blue)
zRing = ring(frame = sceneFrame, pos=(0,0,1),axis=(0,0,1), radius=r, thickness=r/100, color=color.yellow)
rodx = cylinder(frame = sceneFrame, pos=((r*2.5)/-2,0,0),axis=(r*2.5,0,0), radius=r/100, color=color.green)
rody = cylinder(frame = sceneFrame, pos=(0,(r*2.5)/-2,0),axis=(0,r*2.5,0), radius=r/100, color=color.blue)
rodz = cylinder(frame = sceneFrame, pos=(0,0,(r*2.5)/-2),axis=(0,0,r*2.5), radius=r/100, color=color.yellow)
#Labels
zero = text(frame = sceneFrame, text='0', pos=(0,0,r*1.5), height=r*.25, align='center', depth=r*-0.03, color=color.green, axis=(0,0,1))
one = text(frame = sceneFrame, text='1', pos=(0,0,r*-1.5), height=r*.25, align='center', depth=r*-0.03, color=color.green, axis=(0,0,1))

xtext = text(frame = sceneFrame, text='x', pos=(r*.5,0,0), height=r*.15, align='center', depth=r*-0.02, color=color.green, axis=(0,0,1))
ytext = text(frame = sceneFrame, text='y', pos=(0,r*.5,0), height=r*.15, align='center', depth=r*-0.02, color=color.blue, axis=(0,0,1))
ztext = text(frame = sceneFrame, text='z', pos=(0,0,r*.5), height=r*.15, align='center', depth=r*-0.02, color=color.yellow, axis=(0,0,1))

#Setting up qubit
setVector(0,0.0)

#Initial scene/camera rotations
sceneFrame.rotate(axis=(1,0,0), angle=-1*pi/2) 
zero.rotate(axis=(1,0,0), angle=-1*pi/2)
one.rotate(axis=(1,0,0), angle=-1*pi/2)
ball.rotate(axis=(1,0,0), angle=1*pi/2)
ball.rotate(axis=(0,0,1), angle=2*pi/2)
ztext.rotate(axis=(1,0,0), angle=1*pi/2)
ytext.rotate(axis=(1,0,0), angle=1*pi/2)
xtext.rotate(axis=(1,0,0), angle=1*pi/2)

  
setqZero(wx.EVT_SHOW)
#setPauliX(wx.EVT_SHOW)
#setHadamard(wx.EVT_SHOW)
#setPauliY(wx.EVT_SHOW)
#setPauliY(wx.EVT_SHOW)
#setPauliZ(wx.EVT_SHOW)
#setPauliZ(wx.EVT_SHOW)
#setHadamard(wx.EVT_SHOW)
#Main running loop
while 1:
    rate (128)
    #Keep things updated
    #updatePosition()
