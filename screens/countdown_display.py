import os
import tkinter as tk
from PIL import Image, ImageTk
from settings import COUNTDOWN_DIR, COUNTDOWN_SECONDS


class CountdownDisplay:
    def __init__(self, root, on_complete):
        self.root = root
        self.on_complete = on_complete
        self._current = COUNTDOWN_SECONDS
        self._after_id = None
        self._alert_visible = False

        # Get screen dimensions
        self.screen_w = root.winfo_screenwidth()
        self.screen_h = root.winfo_screenheight()

        # Create fullscreen overlay
        self.overlay = tk.Toplevel(root)
        self.overlay.attributes("-fullscreen", True)
        self.overlay.configure(bg="black")
        self.overlay.lift()
        self.overlay.focus_set()

        self.canvas = tk.Canvas(
            self.overlay, width=self.screen_w, height=self.screen_h,
            bg="black", highlightthickness=0,
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Preload images
        self._images = {}
        self._load_images()

        # Draw background
        if "background" in self._images:
            self.canvas.create_image(
                self.screen_w // 2, self.screen_h // 2,
                image=self._images["background"],
            )

        # Number display
        self._number_id = self.canvas.create_image(
            self.screen_w // 2, self.screen_h // 2, image=None,
        )

        # Alert overlay (flashing)
        self._alert_id = None
        if "alert-on" in self._images:
            self._alert_id = self.canvas.create_image(
                self.screen_w // 2, self.screen_h // 2,
                image=self._images["alert-on"], state="hidden",
            )

        # Start ticking
        self._tick()

    def _load_images(self):
        for i in range(COUNTDOWN_SECONDS + 1):
            path = os.path.join(COUNTDOWN_DIR, f"{i}.tif")
            self._load_image(str(i), path)

        bg_path = os.path.join(COUNTDOWN_DIR, "background.tif")
        self._load_image("background", bg_path)

        alert_path = os.path.join(COUNTDOWN_DIR, "alert-on.tif")
        self._load_image("alert-on", alert_path)

    def _load_image(self, key, path):
        if not os.path.isfile(path):
            return
        try:
            img = Image.open(path)
            img = img.resize((self.screen_w, self.screen_h), Image.LANCZOS)
            self._images[key] = ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Could not load countdown image {path}: {e}")

    def _tick(self):
        if self._current < 0:
            self._finish()
            return

        # Update number image
        key = str(self._current)
        if key in self._images:
            self.canvas.itemconfig(self._number_id, image=self._images[key])

        # Toggle alert flash
        if self._alert_id is not None:
            self._alert_visible = not self._alert_visible
            state = "normal" if self._alert_visible else "hidden"
            self.canvas.itemconfig(self._alert_id, state=state)

        self._current -= 1
        self._after_id = self.root.after(1000, self._tick)

    def _finish(self):
        try:
            self.overlay.destroy()
        except Exception:
            pass
        if self.on_complete:
            self.on_complete()

    def destroy(self):
        if self._after_id:
            try:
                self.root.after_cancel(self._after_id)
            except Exception:
                pass
        try:
            self.overlay.destroy()
        except Exception:
            pass
