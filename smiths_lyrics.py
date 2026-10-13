import tkinter as tk
import time
import math

LYRICS = [
    (1.0, "And if a double-decker bus"),
    (3.5, "Crashes into us"),
    (6.0, "To die by your side"),
    (9.0, "Is such a heavenly way"),
    (11.5, "To dieee"),
]

BOX_W, BOX_H = 350, 300
FONT = ("Helvetica", 25, "bold")

# خلفية سوداء وكتابة زرقاء
BG_COLOR = "#000000"
FG_COLOR = "#0088FF"

RISE_SPEED = 110
BOTTOM_SPAWN_OFFSET = 150
STACK_SPACING = 20

class LyricCard:
    def __init__(self, parent, text, x, y, creation_time):
        self.win = tk.Toplevel(parent)
        self.win.overrideredirect(True) 
        self.win.attributes("-topmost", True)
        self.win.configure(bg=BG_COLOR)
        self.win.geometry(f"{BOX_W}x{BOX_H}+{int(x)}+{int(y)}")
        self.win.resizable(False, False)
        
        self.full_text = text
        self.label = tk.Label(
            self.win,
            text="",
            font=FONT,
            bg=BG_COLOR,
            fg=FG_COLOR,
            wraplength=BOX_W - 25,
            justify="center"
        )
        self.label.pack(expand=True, fill="both", padx=15, pady=15)
        
        self.typewriter_index = 0
        self.typewriter()
        
        self.base_x = x  # الموقع الأفقي الأساسي
        self.x = x
        self.y = float(y)
        self.birth_time = creation_time

    def update_pos(self, dy, current_time):
        # صعود للأعلى
        self.y -= dy
        
        # حركة تموجية أفقية باستخدام دالة الجيب (Sine Wave)
        age = current_time - self.birth_time
        amplitude = 30   # مدى التموج يمين ويسار (كلما زاد الرقم زاد عرض التموج)
        frequency = 2.5  # سرعة اهتزاز التموج
        self.x = self.base_x + amplitude * math.sin(age * frequency)
        
        self.win.geometry(f"{BOX_W}x{BOX_H}+{int(self.x)}+{int(self.y)}")

    def is_offscreen(self):
        return self.y + BOX_H < -50
    
    def typewriter(self):
        if self.typewriter_index <= len(self.full_text):
            self.label.config(text=self.full_text[:self.typewriter_index])
            self.typewriter_index += 1
            self.win.after(70, self.typewriter)

class LyricFloatApp:
    def __init__(self, root):
        self.root = root
        self.screen_w = root.winfo_screenwidth()
        self.screen_h = root.winfo_screenheight()
        self.next_lyric_idx = 0
        self.boxes = []
        self.last_frame_time = None
        self.current_side = "left"
        self.start()

    def random_safe_x(self):
        center_x = self.screen_w // 2
        spacing = BOX_W + 60
        left_x = center_x - spacing
        right_x = center_x + 60
        if self.current_side == "left":
            self.current_side = "right"
            return left_x
        else:
            self.current_side = "left"
            return right_x

    def lowest_y(self):
        if not self.boxes:
            return self.screen_h - BOX_H - BOTTOM_SPAWN_OFFSET
        return max(box.y for box in self.boxes) + BOX_H + STACK_SPACING

    def start(self):
        self.root.iconify()  
        self.start_time = time.time()
        self.last_frame_time = self.start_time
        self.tick()

    def tick(self):
        now = time.time()
        elapsed = now - self.start_time
        dt = now - self.last_frame_time
        self.last_frame_time = now
        
        while (self.next_lyric_idx < len(LYRICS) and
               LYRICS[self.next_lyric_idx][0] <= elapsed):
            t, text = LYRICS[self.next_lyric_idx]
            x = self.random_safe_x()
            y = self.lowest_y()
            box = LyricCard(self.root, text, x, y, now)
            self.boxes.append(box)
            self.next_lyric_idx += 1
            
        dy = RISE_SPEED * dt
        for box in self.boxes:
            box.update_pos(dy, now)
            
        still_visible = []
        for box in self.boxes:
            if box.is_offscreen():
                try:
                    box.win.destroy()
                except tk.TclError:
                    pass
            else:
                still_visible.append(box)
        self.boxes = still_visible
        
        if self.next_lyric_idx < len(LYRICS) or self.boxes:
            self.root.after(16, self.tick)

if __name__ == "__main__":
    root = tk.Tk()
    app = LyricFloatApp(root)
    root.mainloop()