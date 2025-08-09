from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 480, 202  # Tamaño más grande, igual que la imagen subida

# Colores
BG_COLOR = (20, 30, 35)
EYE_COLOR = (150, 255, 255)
TEXT_COLOR = (106, 191, 210)

# Crear imagen de fondo
img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
draw = ImageDraw.Draw(img)

# Dibuja la forma principal (ovalo tipo "cabeza")
draw.ellipse([0, 0, WIDTH, HEIGHT*2], fill=BG_COLOR)  # Hace una cabeza "aplanada" abajo

# Dibuja los ojos
eye_radius = 45
eye_y = 110
left_eye_x = 145
right_eye_x = 285
draw.pieslice([left_eye_x-eye_radius, eye_y-eye_radius, left_eye_x+eye_radius, eye_y+eye_radius+30], 180, 360, fill=EYE_COLOR)
draw.pieslice([right_eye_x-eye_radius, eye_y-eye_radius, right_eye_x+eye_radius, eye_y+eye_radius+30], 180, 360, fill=EYE_COLOR)

# Dibuja el texto "SG DIMSOR" en la esquina inferior izquierda
try:
    font = ImageFont.truetype("arialbd.ttf", 23)
except:
    font = ImageFont.load_default()
draw.text((40, HEIGHT-35), "SG DIMSOR", font=font, fill=TEXT_COLOR)

img.show()
img.save("robot_eyes_logo.png")