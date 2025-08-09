from PIL import Image, ImageDraw, ImageFont, ImageTk
import tkinter as tk

# Escala aumentada - ventana más grande
WIDTH, HEIGHT = 1280, 640  # Doble de tamaño

# Colores (sin cambios)
BG_COLOR = (20, 30, 35)
EYE_COLOR = (150, 255, 255)
TEXT_COLOR = (106, 191, 210)

def draw_robot_face(left_eye_x, right_eye_x, eye_y, eye_radius, smiling=False, expression="normal"):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    # Cabeza-ovalo (escalada proporcionalmente)
    draw.ellipse([0, 0, WIDTH, HEIGHT*2], fill=BG_COLOR)
    
    # Dibujar según expresión
    if expression == "blink":
        # Parpadeo - líneas horizontales
        draw.rectangle([left_eye_x-eye_radius, eye_y-10, left_eye_x+eye_radius, eye_y+10], fill=EYE_COLOR)
        draw.rectangle([right_eye_x-eye_radius, eye_y-10, right_eye_x+eye_radius, eye_y+10], fill=EYE_COLOR)
    elif expression == "angry":
        # Ojos enojados - más pequeños y triangulares
        angry_radius = eye_radius - 30
        # Triangulos invertidos para expresión enojada
        points_left = [(left_eye_x, eye_y-angry_radius), (left_eye_x-angry_radius, eye_y+angry_radius), (left_eye_x+angry_radius, eye_y+angry_radius)]
        points_right = [(right_eye_x, eye_y-angry_radius), (right_eye_x-angry_radius, eye_y+angry_radius), (right_eye_x+angry_radius, eye_y+angry_radius)]
        draw.polygon(points_left, fill=EYE_COLOR)
        draw.polygon(points_right, fill=EYE_COLOR)
    elif expression == "surprised":
        # Ojos sorprendidos - círculos grandes
        big_radius = eye_radius + 20
        draw.ellipse([left_eye_x-big_radius, eye_y-big_radius, left_eye_x+big_radius, eye_y+big_radius], fill=EYE_COLOR)
        draw.ellipse([right_eye_x-big_radius, eye_y-big_radius, right_eye_x+big_radius, eye_y+big_radius], fill=EYE_COLOR)
    elif expression == "sleepy":
        # Ojos somnolientos - semicírculos muy planos
        draw.rectangle([left_eye_x-eye_radius, eye_y-15, left_eye_x+eye_radius, eye_y+15], fill=EYE_COLOR)
        draw.rectangle([right_eye_x-eye_radius, eye_y-15, right_eye_x+eye_radius, eye_y+15], fill=EYE_COLOR)
    elif smiling:
        # Ojo izquierdo: círculo cuando sonríe
        draw.ellipse([left_eye_x-eye_radius, eye_y-eye_radius, left_eye_x+eye_radius, eye_y+eye_radius], fill=EYE_COLOR)
        # Ojo derecho: siempre semicircular
        draw.pieslice([right_eye_x-eye_radius, eye_y-eye_radius, right_eye_x+eye_radius, eye_y+eye_radius+140], 180, 360, fill=EYE_COLOR)
    else:
        # Ojos normales - semicirculares
        draw.pieslice([left_eye_x-eye_radius, eye_y-eye_radius, left_eye_x+eye_radius, eye_y+eye_radius+140], 180, 360, fill=EYE_COLOR)
        draw.pieslice([right_eye_x-eye_radius, eye_y-eye_radius, right_eye_x+eye_radius, eye_y+eye_radius+140], 180, 360, fill=EYE_COLOR)
    
    # Letras "SG DIMSOR" con tamaño ajustado
    try:
        font = ImageFont.truetype("arialbd.ttf", 45)  # Tamaño ajustado para que no interfiera con ojos
    except:
        font = ImageFont.load_default()
    draw.text((80, HEIGHT-80), "SG DIMSOR", font=font, fill=TEXT_COLOR)
    return img

class RobotEyesApp:
    def __init__(self, master):
        self.master = master
        master.title("Simulación Ojos Robot - SG DIMSOR")
        self.label = tk.Label(master)
        self.label.pack()
        self.frame = 0
        self.smiling = False
        self.smile_frame = 0
        self.current_expression = "normal"
        self.expression_timer = 0
        self.blink_timer = 0
        self.auto_expressions = True
        
        # Bind controles
        master.bind('<space>', self.smile)  # Presiona espacio para la "risa"
        master.bind('<Key>', self.on_key_press)  # Otras teclas para expresiones
        master.focus_set()
        
        # Centrar ventana
        master.geometry(f"{WIDTH}x{HEIGHT}")
        master.resizable(False, False)
        
        self.animate()

    def on_key_press(self, event):
        """Controles de teclado para diferentes expresiones"""
        if event.char == '1':
            self.current_expression = "normal"
        elif event.char == '2':
            self.current_expression = "angry"
        elif event.char == '3':
            self.current_expression = "surprised"
        elif event.char == '4':
            self.current_expression = "sleepy"
        elif event.char == 'b':
            self.trigger_blink()
        elif event.char == 'a':
            self.auto_expressions = not self.auto_expressions

    def smile(self, event):
        self.smiling = True
        self.smile_frame = 0
        self.current_expression = "normal"

    def trigger_blink(self):
        """Parpadeo manual"""
        self.current_expression = "blink"
        self.expression_timer = 8  # Duración del parpadeo

    def animate(self):
        # Animación de movimiento horizontal (escalada proporcionalmente)
        if self.frame < 30:
            left_eye_x = 420 + self.frame*4  # Escalado 2x
            right_eye_x = 860 + self.frame*4  # Escalado 2x
        else:
            left_eye_x = 420 + (59-self.frame)*4  # Escalado 2x
            right_eye_x = 860 + (59-self.frame)*4  # Escalado 2x
        
        eye_y = 260  # Escalado 2x (era 130)
        eye_radius = 140  # Escalado 2x (era 70)
        
        # Control de expresiones automáticas
        if self.auto_expressions and not self.smiling:
            self.expression_timer += 1
            self.blink_timer += 1
            
            # Parpadeo automático cada 120 frames (~10 segundos)
            if self.blink_timer > 120:
                if self.current_expression != "blink":
                    self.current_expression = "blink"
                    self.expression_timer = 8
                self.blink_timer = 0
            
            # Cambiar expresión cada 200 frames
            if self.expression_timer > 200:
                expressions = ["normal", "surprised", "sleepy", "normal", "normal"]  # Normal más frecuente
                import random
                self.current_expression = random.choice(expressions)
                self.expression_timer = 0
            
            # Terminar parpadeo
            if self.current_expression == "blink" and self.expression_timer > 8:
                self.current_expression = "normal"
        
        # Si está sonriendo, el ojo izquierdo es círculo
        if self.smiling:
            img = draw_robot_face(left_eye_x, right_eye_x, eye_y, eye_radius, smiling=True, expression="normal")
            self.smile_frame += 1
            if self.smile_frame > 18:  # ~1.5 segundos
                self.smiling = False
        else:
            img = draw_robot_face(left_eye_x, right_eye_x, eye_y, eye_radius, smiling=False, expression=self.current_expression)
        
        tk_img = ImageTk.PhotoImage(img)
        self.label.imgtk = tk_img
        self.label.configure(image=tk_img)
        self.frame = (self.frame + 1) % 60
        self.master.after(80, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    app = RobotEyesApp(root)
    root.mainloop()