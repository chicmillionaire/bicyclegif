import math
from PIL import Image, ImageDraw

images = []

zoom = 0.5
width = int(860*zoom)
height = int(630*zoom)

def draw_frame(draw):
    points = [(165,465),(317,220),(400,465),(600,220),(695,465)]
    line_fill = (200,150,155)
    line_width = int(15*zoom)
    
    draw.line(xy=(points[0][0]*zoom, points[0][1]*zoom, points[1][0]*zoom, points[1][1]*zoom), 
    fill=line_fill,width=line_width)
    
    draw.line(xy=(points[0][0]*zoom, points[0][1]*zoom, points[2][0]*zoom, points[2][1]*zoom),
    fill=line_fill,width=line_width)

    draw.line(xy=(points[1][0]*zoom, points[1][1]*zoom, points[2][0]*zoom, points[2][1]*zoom),
    fill=line_fill,width=line_width)

    draw.line(xy=(points[1][0]*zoom, points[1][1]*zoom, points[3][0]*zoom, points[3][1]*zoom),
    fill=line_fill,width=line_width)

    draw.line(xy=(points[2][0]*zoom, points[2][1]*zoom, points[3][0]*zoom, points[3][1]*zoom),
    fill=line_fill,width=line_width)

    draw.line(xy=(points[3][0]*zoom, points[3][1]*zoom, points[4][0]*zoom, points[4][1]*zoom),
    fill=line_fill,width=line_width)

    for p in points:
        draw.ellipse((p[0]*zoom-line_width/2, p[1]*zoom-line_width/2,
        p[0]*zoom+line_width/2, p[1]*zoom+line_width/2), fill=line_fill)

def draw_saddle(draw):
    line_fill = (200,150,155)
    line_width = int(10*zoom)

    points = [(315,225), (300,176), (236,176), (246,143), (363,161),
    (363,176), (300,176)]

    for i in range(len(points)-1):
        draw.line(xy=(points[i][0]*zoom, points[i][1]*zoom, points[i+1][0]*zoom, points[i+1][1]*zoom),
        fill=line_fill,width=line_width)

    for p in points:
        draw.ellipse((p[0]*zoom-line_width/2, p[1]*zoom-line_width/2,
        p[0]*zoom+line_width/2, p[1]*zoom+line_width/2), fill=line_fill,width=1)

def draw_handlebar(draw):
    line_fill = (200,150,155)
    line_width = int(10*zoom)
    points = [(605,220),
              (582,147),
              (707,140),
              (737,158),
              (749,185),
              (741,222),
              (717,246),
              (689,251)]
    
    for i in range(len(points)-1):
        draw.line(xy=(points[i][0]*zoom, points[i][1]*zoom,
        points[i+1][0]*zoom, points[i+1][1]*zoom),fill=line_fill,width=line_width)

    for p in points:
        draw.ellipse((p[0]*zoom-line_width/3, p[1]*zoom-line_width/3,
                      p[0]*zoom + line_width/3, p[1]*zoom + line_width/3), 
                      fill=line_fill,width=1)

def draw_wheels(draw,offset):
    line_fill = (0,0,0)
    line_width = int(10*zoom)
    points = [(165,465),(695,465)]
    r = 150*zoom
    
    for i in range(len(points)):
        x,y = points[i][0]*zoom, points[i][1]*zoom
        draw.ellipse((x-r, y-r,
                       x+r, y+r),
                       outline=line_fill,width=line_width)
        draw.ellipse((x-r, y-r,
                      x+r, y+r),
                      outline=line_fill,width=line_width)
        for k in range(0,int(math.pi*2*100),30):
            draw.line((x,y,
                      x+math.cos(k/100+offset)*r,
                      y+math.sin(k/100+offset)*r), fill=line_fill)

        x1 = x+math.cos(offset)*r*5/8
        y1 = y+math.sin(offset)*r*5/8
        r1 = 15*zoom
        draw.ellipse((x1-r1, y1-r1,
                      x1+r1, y1+r1),
                      fill=(0,255,255))

        x1 = x+math.cos(offset+math.pi)*r*5/8
        y1 = y+math.sin(offset+math.pi)*r*5/8
        draw.ellipse((x1-r1,y1-r1,
                      x1+r1,y1+r1),
                      fill=(0,255,255))
        offset += math.pi/2  
    
def draw_pedal(draw, offset, back=False):
    x,y = 400*zoom,465*zoom
    r = 70*zoom
    x1 = x+math.cos(offset)*r
    y1 = x+math.sin(offset)*r
    line_fill = (200,200,25)
    line_width = int(10*zoom)
    draw.ellipse((x-40*zoom,y-40*zoom,x+40*zoom,y+40*zoom),
                    fill=(30,70,80), width=1)
        
    draw.ellipse((x-10*zoom,y-10*zoom,x+10*zoom,y+10*zoom),
                    fill=line_fill, width=1)
    if back:
        draw.ellipse((x1-25*zoom, y1-25*zoom,x1+25*zoom,y1+25*zoom),
                        fill=(0,0,0))
        draw.line((x,y,x1,y1), fill=line_fill, width=line_width)
        draw.ellipse((x1-line_width/2, y1-line_width/2,x1+line_width/2, y1+line_width/2),
                        fill=line_fill)
    else:
        draw.line((x,y,x1,y1),fill=line_fill,width=line_width)
        draw.ellipse((x1-line_width/2,y1-line_width/2,x1+line_width/2,y1+line_width/2),
                        fill=line_fill,width=1)
        draw.ellipse((x1-25*zoom,y1-25*zoom,x1+25*zoom,y1+25*zoom),
                        fill=(0,0,0))        
        
pedal_angle = math.pi/2       
for i in range(314):
    im = Image.new('RGB', (width, height), (255,255,255))
    if i < 314/4 or 314/2 < i < 314*3/4:
        pedal_angle += 1/5
    draw = ImageDraw.Draw(im)
    draw_frame(draw)
    draw_wheels(draw,i/8)
    draw_pedal(draw, pedal_angle, back=True)
    draw_saddle(draw)
    draw_pedal(draw, pedal_angle+math.pi)
    draw_handlebar(draw)
    images.append(im)

images[0].save('bicycle.gif', save_all=True, append_images=images[1:],
    optimiize=False, duration=20, loop=0)
