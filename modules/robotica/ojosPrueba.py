from PIL import Image, ImageDraw, ImageFont, ImageTk
import tkinter as tk

WIDTH, HEIGHT = 479, 202

# Colores
BG_COLOR = (20, 30, 35)
EYE_COLOR = (150, 255, 255)
TEXT_COLOR = (106, 191, 210)

def draw_robot_face(left_eye_x, right_eye_x, eye_y, eye_radius):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    # Cabeza-ovalo (más aplanada abajo, más realista)
    draw.ellipse([0, 0, WIDTH, HEIGHT*2], fill=BG_COLOR)
    # Ojos semicirculares (pieslice en vez de ellipse para base plana)
    draw.pieslice([left_eye_x-eye_radius, eye_y-eye_radius, left_eye_x+eye_radius, eye_y+eye_radius+45], 180, 360, fill=EYE_COLOR)
    draw.pieslice([right_eye_x-eye_radius, eye_y-eye_radius, right_eye_x+eye_radius, eye_y+eye_radius+45], 180, 360, fill=EYE_COLOR)
    # Letras "SG DIMSOR"
    try:
        font = ImageFont.truetype("arialbd.ttf", 23)
    except:
        font = ImageFont.load_default()
    draw.text((40, HEIGHT-35), "SG DIMSOR", font=font, fill=TEXT_COLOR)
    return img

class RobotEyesApp:
    def __init__(self, master):
        self.master = master
        master.title("Simulación Ojos Robot - SG DIMSOR")
        self.label = tk.Label(master)
        self.label.pack()
        self.frame = 0
        self.animate()

    def animate(self):
        # Animación de ojos: se mueven horizontalmente y regresan
        if self.frame < 20:
            left_eye_x = 145 + self.frame*2
            right_eye_x = 285 + self.frame*2
        else:
            left_eye_x = 145 + (39-self.frame)*2
            right_eye_x = 285 + (39-self.frame)*2
        img = draw_robot_face(left_eye_x, right_eye_x, 110, 45)
        tk_img = ImageTk.PhotoImage(img)
        self.label.imgtk = tk_img
        self.label.configure(image=tk_img)
        self.frame = (self.frame + 1) % 40
        self.master.after(80, self.animate)  # 80 ms por frame

if __name__ == "__main__":
    root = tk.Tk()
    app = RobotEyesApp(root)
    root.mainloop()