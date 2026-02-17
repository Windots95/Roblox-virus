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
MB_ICONQUESTION = 0x20
IDYES = 6

SRCCOPY = 0x00CC0020
NOTSRCCOPY = 0x00330008

VK_Q = 0x51
VK_CONTROL = 0x11
VK_SHIFT = 0x10

# =============================
# Startup Prompt
# =============================
if user32.MessageBoxW(
    0,
    "Do you want to run this program?\nThis program contains a lot of flashing lights and visual chaos.\nIt is NOT malware and will not destroy your computer.",
    "Ultimate 8-Bit Chaos Final v13",
    MB_YESNO | MB_ICONQUESTION
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
# Shape Engine
# =============================
def shapes(intensity, size_min=40, size_max=80):
    count = 8 + intensity * 2
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

# =============================
# Core Distortions
# =============================
def invert(): gdi32.BitBlt(hdc,0,0,width,height,hdc,0,0,NOTSRCCOPY)
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

# =============================
# Zoom & Spin Effects
# =============================
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

# =============================
# Super Combos
# =============================
def super_combo_one(intensity):
    tunnel(); wave(time.time()*5); shapes(intensity)
def super_combo_two(intensity):
    mega_stretch(); slice_scramble(); pixelate(); shapes(intensity)
    if chance(0.5): invert()

# =============================
# Random Move Effects
# =============================
def firewall_effect(): 
    bar_width=random.randint(20,60)
    for x in range(0,width,bar_width*2):
        brush=gdi32.CreateSolidBrush(rainbow_color())
        gdi32.SelectObject(hdc,brush)
        gdi32.Rectangle(hdc,x,0,x+bar_width,height)
        gdi32.DeleteObject(brush)
    for y in range(0,height,bar_width*2):
        brush=gdi32.CreateSolidBrush(rainbow_color())
        gdi32.SelectObject(hdc,brush)
        gdi32.Rectangle(hdc,0,y,width,y+bar_width)
        gdi32.DeleteObject(brush)

def bounce_effect(intensity): 
    for _ in range(5+intensity):
        size=random.randint(30,70)
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

def slowly_spinning_circle():
    cx,cy=width//2,height//2
    radius=random.randint(100,250)
    angle=time.time()%(2*math.pi)
    for i in range(8):
        theta=angle+i*math.pi/4
        x=int(cx+math.cos(theta)*radius)
        y=int(cy+math.sin(theta)*radius)
        size=random.randint(30,50)
        gdi32.Rectangle(hdc,x,y,x+size,y+size)

def new_bits_effects():
    for _ in range(50):
        x=random.randint(0,width); y=random.randint(0,height)
        brush=gdi32.CreateSolidBrush(eight_bit_color())
        gdi32.SelectObject(hdc,brush)
        gdi32.Rectangle(hdc,x,y,x+5,y+5)
        gdi32.DeleteObject(brush)

def flashing_rectangles():
    for _ in range(10):
        x=random.randint(0,width-60); y=random.randint(0,height-60)
        w=random.randint(30,60); h=random.randint(30,60)
        brush=gdi32.CreateSolidBrush(eight_bit_color())
        gdi32.SelectObject(hdc,brush)
        gdi32.Rectangle(hdc,x,y,x+w,y+h)
        gdi32.DeleteObject(brush)

def diagonal_lines():
    for i in range(0,width,50):
        gdi32.MoveToEx(hdc,i,0,None)
        gdi32.LineTo(hdc,(i+height)%width,height)

def rotating_squares():
    cx,cy=width//2,height//2
    for i in range(6):
        angle=time.time()*i
        size=40+10*i
        x=int(cx+math.cos(angle)*100)
        y=int(cy+math.sin(angle)*100)
        gdi32.Rectangle(hdc,x,y,x+size,y+size)

def expanding_circles():
    cx,cy=width//2,height//2
    r=int((time.time()*100)%300)
    for i in range(5):
        gdi32.Ellipse(hdc,cx-r,cy-r,cx+r,cy+r)

# =============================
# System32 Icons
# =============================
SYSTEM32_ICONS = [
    r"C:\Windows\System32\notepad.exe",
    r"C:\Windows\System32\calc.exe",
    r"C:\Windows\System32\mspaint.exe",
    r"C:\Windows\System32\write.exe",
]

def spawn_system32_icons():
    for icon in SYSTEM32_ICONS:
        if os.path.exists(icon):
            os.startfile(icon)
            time.sleep(0.5)

# =============================
# Sequential Mini-Effects Stages (Fixed)
# =============================
def mini_effect_stage(stage_num, intensity):
    stage_cycle = stage_num % 30
    if stage_cycle == 0: shapes(intensity)
    elif stage_cycle == 1: wave(time.time()*3)
    elif stage_cycle == 2: slice_scramble()
    elif stage_cycle == 3: tunnel()
    elif stage_cycle == 4: mega_stretch()
    elif stage_cycle == 5: pixelate()
    elif stage_cycle == 6: scanlines()
    elif stage_cycle == 7: super_combo_one(intensity)
    elif stage_cycle == 8: super_combo_two(intensity)
    elif stage_cycle == 9: firewall_effect()
    elif stage_cycle == 10: bounce_effect(intensity)
    elif stage_cycle == 11: move_and_bounce(intensity)
    elif stage_cycle == 12: slowly_spinning_circle()
    elif stage_cycle == 13: new_bits_effects()
    elif stage_cycle == 14: flashing_rectangles()
    elif stage_cycle == 15: diagonal_lines()
    elif stage_cycle == 16: rotating_squares()
    elif stage_cycle == 17: expanding_circles()
    elif stage_cycle == 18: zoom_in()
    elif stage_cycle == 19: zoom_out()
    elif stage_cycle == 20: spin_effect()
    elif stage_cycle == 21: shapes(intensity,50,80)
    elif stage_cycle == 22: bounce_effect(intensity)
    elif stage_cycle == 23: move_and_bounce(intensity)
    elif stage_cycle == 24: firewall_effect()
    elif stage_cycle == 25: rotating_squares()
    elif stage_cycle == 26: expanding_circles()
    elif stage_cycle == 27: zoom_in()
    elif stage_cycle == 28: zoom_out()
    elif stage_cycle == 29: spin_effect()

# =============================
# Intensity & Speed Scaling
# =============================
intensity=1; last_scale=time.time()
frame_delay=0.08
def scale_intensity_speed():
    global intensity,last_scale,frame_delay
    if time.time()-last_scale>10:
        intensity=min(intensity+1,10)
        frame_delay=max(frame_delay*0.85,0.005)
        last_scale=time.time()

# =============================
# Windows Sound Effects
# =============================
WIN_SOUNDS = [
    r"C:\Windows\Media\Windows Exclamation.wav",
    r"C:\Windows\Media\Windows Notify.wav",
    r"C:\Windows\Media\Windows Ding.wav",
    r"C:\Windows\Media\Windows Error.wav",
    r"C:\Windows\Media\Windows Startup.wav",
    r"C:\Windows\Media\Windows Shutdown.wav"
]

def play_random_sound():
    if chance(0.15):
        try:
            winsound.PlaySound(random.choice(WIN_SOUNDS), winsound.SND_ASYNC)
        except: pass

# =============================
# Main Loop
# =============================
print("Running 8-bit chaos v13 FINAL... (Hidden exit: CTRL + SHIFT + Q)")
spawn_system32_icons()  # spawn icons at start
stage_counter=0
while True:
    if (user32.GetAsyncKeyState(VK_Q) and
        user32.GetAsyncKeyState(VK_CONTROL) and
        user32.GetAsyncKeyState(VK_SHIFT)):
        break

    scale_intensity_speed()
    t=time.time()*3

    shapes(intensity)

    effect=stage_counter%9
    if effect==0: tunnel()
    elif effect==1: wave(t)
    elif effect==2: slice_scramble()
    elif effect==3: pixelate()
    elif effect==4: scanlines()
    elif effect==5: super_combo_one(intensity)
    elif effect==6: super_combo_two(intensity)
    elif effect==7: zoom_in()
    elif effect==8: zoom_out()

    mini_effect_stage(stage_counter,intensity)
    play_random_sound()

    stage_counter+=1
    time.sleep(frame_delay)

user32.ReleaseDC(0,hdc)
os._exit(0)
