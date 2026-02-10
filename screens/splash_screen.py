import tkinter as tk
from PIL import Image, ImageTk
from settings import LOGO_PATH, SPLASH_DURATION_MS


class SplashScreen:
    def __init__(self, root, on_complete):
        self.root = root
        self.on_complete = on_complete
        self.frame = tk.Frame(root, bg="black")
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Load and scale logo
        try:
            img = Image.open(LOGO_PATH)
            screen_w = root.winfo_screenwidth()
            screen_h = root.winfo_screenheight()

            # Scale to fit screen while preserving aspect ratio
            img_ratio = img.width / img.height
            screen_ratio = screen_w / screen_h
            if img_ratio > screen_ratio:
                new_w = screen_w
                new_h = int(screen_w / img_ratio)
            else:
                new_h = screen_h
                new_w = int(screen_h * img_ratio)
            img = img.resize((new_w, new_h), Image.LANCZOS)

            self._photo = ImageTk.PhotoImage(img)
            label = tk.Label(self.frame, image=self._photo, bg="black")
        except Exception:
            self._photo = None
            label = tk.Label(
                self.frame, text="Photon Laser Tag",
                font=("Helvetica", 48, "bold"), fg="white", bg="black",
            )
        label.pack(expand=True)

        self._after_id = root.after(SPLASH_DURATION_MS, self._finish)

    def _finish(self):
        if self.on_complete:
            self.on_complete()

    def destroy(self):
        try:
            self.root.after_cancel(self._after_id)
        except Exception:
            pass
        self.frame.destroy()
