import ctypes
import random
import time
import os
import math
import winsound

# =============================
# Windows Setup
# =============================
user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

MB_YESNO = 0x04
MB_ICONEXCLAMATION = 0x30
IDYES = 6

SRCCOPY = 0x00CC0020
NOTSRCCOPY = 0x00330008

VK_Q = 0x51
VK_CONTROL = 0x11
VK_SHIFT = 0x10

# =============================
# Startup Messages
# =============================
if user32.MessageBoxW(
    0,
    "WARNING:\nThis program contains extreme flashing lights,\nrandom rotations, zoom-ins, zoom-outs, spins, and chaotic visual effects.\nIt is NOT malware and will not harm your computer.",
    "Ultimate 8-Bit Chaos v17",
    MB_YESNO | MB_ICONEXCLAMATION
) != IDYES:
    os._exit(0)

if user32.MessageBoxW(
    0,
    "FINAL WARNING:\n"
    "Prepare for the most intense 8-bit chaos ever.\n"
    "This program will flood your screen with colors, shapes, rotations, zoom-ins and outs, spins, flashes, and random distortions.\n"
    "Expect extreme visual stimulation for several minutes.\n"
    "This is a demonstration of advanced chaos visuals.\n"
    "It is NOT malware.\n"
    "CTRL + SHIFT + Q is the emergency exit.\n"
    "Enjoy the rainbow madness and multiple layers of chaotic effects.",
    "Ultimate 8-Bit Chaos v17 - FINAL WARNING",
    MB_YESNO | MB_ICONEXCLAMATION
) != IDYES:
    os._exit(0)

# =============================
# Screen Info
# =============================
width = user32.GetSystemMetrics(0)
height = user32.GetSystemMetrics(1)
hdc = user32.GetDC(0)

# =============================
# Utilities
# =============================
def chance(p): return random.random() < p

def eight_bit_color():
    levels = [0, 85, 170, 255]
    r = random.choice(levels)
    g = random.choice(levels)
    b = random.choice(levels)
    return r | (g << 8) | (b << 16)

def rainbow_color(t=None):
    t = t or time.time()
    r = int((math.sin(t*2)+1)*127)
    g = int((math.sin(t*2+2)+1)*127)
    b = int((math.sin(t*2+4)+1)*127)
    return r | (g << 8) | (b << 16)

# =============================
# Effects
# =============================
def shapes(intensity, size_min=40, size_max=80):
    count = 10 + intensity * 3
    for _ in range(count):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(size_min, size_max)
        brush = gdi32.CreateSolidBrush(eight_bit_color())
        gdi32.SelectObject(hdc, brush)
        t = random.randint(0, 2)
        if t == 0: gdi32.Rectangle(hdc, x, y, x+size, y+size)
        elif t == 1: gdi32.Ellipse(hdc, x, y, x+size, y+size)
        else: gdi32.RoundRect(hdc, x, y, x+size, y+size, 10, 10)
        gdi32.DeleteObject(brush)

def tunnel(): 
    s=random.randint(10,60)
    gdi32.StretchBlt(hdc,s,s,width-2*s,height-2*s,hdc,0,0,width,height,SRCCOPY)

def wave(t): 
    for i in range(0,height,30):
        o=int(math.sin(t+i*0.05)*25)
        gdi32.BitBlt(hdc,o,i,width,30,hdc,0,i,SRCCOPY)

def slice_scramble(): 
    for i in range(0,height,50):
        o=random.randint(-40,40)
        gdi32.BitBlt(hdc,o,i,width,50,hdc,0,i,SRCCOPY)

def mega_stretch(): 
    sx=random.uniform(0.6,1.4)
    sy=random.uniform(0.6,1.4)
    nw=int(width*sx); nh=int(height*sy)
    ox=random.randint(-100,100); oy=random.randint(-100,100)
    gdi32.StretchBlt(hdc,ox,oy,nw,nh,hdc,0,0,width,height,SRCCOPY)

def pixelate(): 
    b=random.randint(8,18)
    gdi32.StretchBlt(hdc,0,0,width//b,height//b,hdc,0,0,width,height,SRCCOPY)
    gdi32.StretchBlt(hdc,0,0,width,height,hdc,0,0,width//b,height//b,SRCCOPY)

def scanlines(): 
    for y in range(0,height,4): gdi32.BitBlt(hdc,0,y,width,1,hdc,0,y,NOTSRCCOPY)

def zoom_in():
    factor = random.uniform(1.05,1.3)
    nw=int(width*factor)
    nh=int(height*factor)
    ox=-random.randint(0,nw-width)
    oy=-random.randint(0,nh-height)
    gdi32.StretchBlt(hdc,ox,oy,nw,nh,hdc,0,0,width,height,SRCCOPY)

def zoom_out():
    factor = random.uniform(0.7,0.95)
    nw=int(width*factor)
    nh=int(height*factor)
    ox=random.randint(0,width-nw)
    oy=random.randint(0,height-nh)
    gdi32.StretchBlt(hdc,ox,oy,nw,nh,hdc,0,0,width,height,SRCCOPY)

def spin_effect():
    cx,cy=width//2,height//2
    temp_hdc = user32.GetDC(0)
    for _ in range(3):
        ox=random.randint(-20,20)
        oy=random.randint(-20,20)
        gdi32.BitBlt(temp_hdc,ox,oy,width,height,hdc,0,0,SRCCOPY)
    user32.ReleaseDC(0,temp_hdc)

def bounce_effect(intensity): 
    for _ in range(10+intensity):
        size=random.randint(20,60)
        x=random.randint(0,width-size)
        y=random.randint(0,height-size)
        dx=random.choice([-15,-10,10,15])
        dy=random.choice([-15,-10,10,15])
        for _ in range(3):
            brush=gdi32.CreateSolidBrush(rainbow_color())
            gdi32.SelectObject(hdc,brush)
            gdi32.Rectangle(hdc,x,y,x+size,y+size)
            gdi32.DeleteObject(brush)
            x+=dx; y+=dy
            if x<0 or x+size>width: dx*=-1
            if y<0 or y+size>height: dy*=-1

def move_and_bounce(intensity): 
    x=random.randint(0,width//2); y=random.randint(0,height//2)
    dx=random.randint(5,15); dy=random.randint(5,15)
    size=random.randint(30,60)
    for _ in range(4):
        brush=gdi32.CreateSolidBrush(rainbow_color())
        gdi32.SelectObject(hdc,brush)
        gdi32.Ellipse(hdc,x,y,x+size,y+size)
        gdi32.DeleteObject(brush)
        x+=dx; y+=dy
        if x<0 or x+size>width: dx*=-1
        if y<0 or y+size>height: dy*=-1

def super_combo_one(intensity):
    tunnel(); wave(time.time()*5); shapes(intensity)

def super_combo_two(intensity):
    mega_stretch(); slice_scramble(); pixelate(); shapes(intensity)
    if chance(0.5): invert()

def invert(): gdi32.BitBlt(hdc,0,0,width,height,hdc,0,0,NOTSRCCOPY)

# =============================
# Sounds - Old + 12 new sounds
# =============================
WIN_SOUNDS = [
    r"C:\Windows\Media\Windows Exclamation.wav",
    r"C:\Windows\Media\Windows Notify.wav",
    r"C:\Windows\Media\Windows Ding.wav",
    r"C:\Windows\Media\Windows Error.wav",
    # new additional sounds
    r"C:\Windows\Media\Windows Unlock.wav",
    r"C:\Windows\Media\Windows Balloon.wav",
    r"C:\Windows\Media\Windows Notify Email.wav",
    r"C:\Windows\Media\Windows Critical Stop.wav",
    r"C:\Windows\Media\Windows Device Connect.wav",
    r"C:\Windows\Media\Windows Device Disconnect.wav",
    r"C:\Windows\Media\Windows Hardware Fail.wav",
    r"C:\Windows\Media\Windows Exclamation 2.wav",
    r"C:\Windows\Media\Windows Notify 2.wav",
    r"C:\Windows\Media\Windows Ding 2.wav",
    r"C:\Windows\Media\Windows Error 2.wav",
    r"C:\Windows\Media\Windows Pop.wav",
    r"C:\Windows\Media\Windows Print.wav",
    r"C:\Windows\Media\Windows Start.wav"
]

def play_random_sound():
    if chance(0.25):
        try:
            winsound.PlaySound(random.choice(WIN_SOUNDS), winsound.SND_ASYNC)
        except: pass

# =============================
# Stage sequencing
# =============================
STAGES = [
    [shapes], [wave], [slice_scramble], [tunnel], [mega_stretch], [pixelate],  
    [scanlines, super_combo_one], [super_combo_two], 
    [zoom_in, zoom_out], [spin_effect], [bounce_effect, move_and_bounce]
]

# =============================
# Intensity & Speed Scaling
# =============================
intensity=1; last_scale=time.time()
frame_delay=0.05
def scale_intensity_speed():
    global intensity,last_scale,frame_delay
    if time.time()-last_scale>10:
        intensity=min(intensity+1,10)
        frame_delay=max(frame_delay*0.85,0.005)
        last_scale=time.time()

# =============================
# Main Loop
# =============================
print("Running 8-bit chaos v17 FINAL (with new sounds)... (Hidden exit: CTRL + SHIFT + Q)")
play_random_sound()

stage_counter=0
while True:
    if (user32.GetAsyncKeyState(VK_Q) and
        user32.GetAsyncKeyState(VK_CONTROL) and
        user32.GetAsyncKeyState(VK_SHIFT)):
        break

    scale_intensity_speed()
    t=time.time()*3

    current_stage = STAGES[stage_counter % len(STAGES)]
    if isinstance(current_stage, list):
        for effect in current_stage:
            effect(intensity) if effect.__code__.co_argcount else effect()
    else:
        current_stage(intensity) if current_stage.__code__.co_argcount else current_stage()

    play_random_sound()
    stage_counter += 1
    time.sleep(frame_delay)

user32.ReleaseDC(0,hdc)
os._exit(0)
