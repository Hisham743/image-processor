import os

import tkinter as tk
from tkinter import ttk, filedialog
from ttkthemes import ThemedTk

from PIL import ImageTk, Image, ImageOps

FONT = ("Helvetica", 20)
BASE_DIR = r"C:\Users\hp\PycharmProjects\image-processor"


class ImageProcessor:
    def __init__(self, root: ThemedTk):
        self.root = root
        self.root.title("Image Processor")
        self.root.configure(padx=25, pady=25)

        self.placeholder_image = ImageTk.PhotoImage(
            file=os.path.join(BASE_DIR, "placeholder_image.png")
        )

        self.canvas = tk.Canvas(self.root, width=500, height=500)
        self.placeholder_id = self.canvas.create_image(
            0, 0, anchor=tk.NW, image=self.placeholder_image
        )
        self.canvas.grid(row=0, column=0, padx=(0, 50))

        self.canvas.bind("<Button-1>", self.upload_image)

        self.first_click = True

        self.file_path = None
        self.image = None
        self.image_tk = None
        self.image_id = None

        self.options_frame = ttk.Frame(self.root)
        self.options_frame.grid(row=0, column=1)

        font_style = ttk.Style()
        font_style.configure(".", font=FONT)

        row0_frame = ttk.Frame(self.options_frame)
        row0_frame.grid(row=0, column=0, sticky=tk.W)

        self.format_label = ttk.Label(row0_frame, text="File Format: ")
        self.format_label.grid(row=0, column=0)
        self.format = tk.StringVar()
        self.format_list = ttk.Combobox(
            row0_frame, width=5, textvariable=self.format, font=FONT, state="disabled"
        )
        self.format_list["values"] = (
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".bmp",
            ".tiff",
            ".ico",
            ".webp",
            ".pdf",
        )
        self.format_list.grid(row=0, column=1)

        row1_frame = ttk.Frame(self.options_frame)
        row1_frame.grid(row=1, column=0, pady=(30, 0))

        self.width_label = ttk.Label(row1_frame, text="Width: ")
        self.width_label.grid(row=0, column=0)
        self.width_box = PixelSpinBox(
            row1_frame, state="disabled", command=self.change_height
        )
        self.width_box.grid(row=0, column=1, padx=(0, 20))
        self.width_box.bind("<KeyRelease>", self.change_height)

        self.height_label = ttk.Label(row1_frame, text="Height: ")
        self.height_label.grid(row=0, column=2)
        self.height_box = PixelSpinBox(
            row1_frame, state="disabled", command=self.change_width
        )
        self.height_box.grid(row=0, column=3)
        self.height_box.bind("<KeyRelease>", self.change_width)

        row2_frame = ttk.Frame(self.options_frame)
        row2_frame.grid(row=2, column=0, pady=(30, 0))

        self.rotate_left_button_img = ImageTk.PhotoImage(
            Image.open(os.path.join(BASE_DIR, "button-icons/rotate-left.png")).resize(
                (50, 50)
            )
        )
        self.rotate_left_button = ttk.Button(
            row2_frame,
            image=self.rotate_left_button_img,
            state="disabled",
            command=lambda: self.rotate(90),
        )
        self.rotate_left_button.grid(row=0, column=0, padx=(0, 20))

        self.rotate_right_button_img = ImageTk.PhotoImage(
            Image.open(os.path.join(BASE_DIR, "button-icons/rotate-right.png")).resize(
                (50, 50)
            )
        )
        self.rotate_right_button = ttk.Button(
            row2_frame,
            image=self.rotate_right_button_img,
            state="disabled",
            command=lambda: self.rotate(-90),
        )
        self.rotate_right_button.grid(row=0, column=1, padx=(0, 20))

        self.flip_horizontal_button_img = ImageTk.PhotoImage(
            Image.open(
                os.path.join(BASE_DIR, "button-icons/flip-horizontal.png")
            ).resize((50, 50))
        )
        self.flip_horizontal_button = ttk.Button(
            row2_frame,
            image=self.flip_horizontal_button_img,
            state="disabled",
            command=self.flip_horizontal,
        )
        self.flip_horizontal_button.grid(row=0, column=2, padx=(0, 20))

        self.flip_vertical_button_img = ImageTk.PhotoImage(
            Image.open(os.path.join(BASE_DIR, "button-icons/flip-vertical.png")).resize(
                (50, 50)
            )
        )
        self.flip_vertical_button = ttk.Button(
            row2_frame,
            image=self.flip_vertical_button_img,
            state="disabled",
            command=self.flip_vertical,
        )
        self.flip_vertical_button.grid(row=0, column=3, padx=(0, 20))

        self.grayscale = tk.BooleanVar()
        self.grayscale_checkbox = tk.Checkbutton(
            self.options_frame,
            text="Convert to grayscale",
            state="disabled",
            font=FONT,
            variable=self.grayscale,
        )
        self.grayscale_checkbox.grid(row=3, column=0, pady=(30, 0))

        row4_frame = ttk.Frame(self.options_frame)
        row4_frame.grid(row=4, column=0, pady=(30, 0))

        self.save_button = ttk.Button(
            row4_frame, text="Save", state="disabled", command=self.save
        )
        self.save_button.grid(row=0, column=0, padx=(0, 20))

        self.save_as_button = ttk.Button(
            row4_frame, text="Save as...", state="disabled", command=self.save_as
        )
        self.save_as_button.grid(row=0, column=1)

    def upload_image(self, event):
        if self.first_click:
            self.file_path = filedialog.askopenfilename(
                filetypes=[("Image files", "*" + " ".join(self.format_list["values"]))]
            )

            self.image = Image.open(self.file_path)
            self.display_image()

            self.format_list.current(
                self.format_list["values"].index(
                    os.path.splitext(self.file_path)[1].lower()
                )
            )

            self.width_box.set(f"{self.image.width}px")
            self.height_box.set(f"{self.image.height}px")

            self.grayscale_checkbox.configure(state="normal")
            for row_frame in self.options_frame.winfo_children():
                for widget in row_frame.winfo_children():
                    widget.configure(state="normal")

            self.first_click = False

    def change_height(self, event=None):
        width = int(self.width_box.get().rstrip("px"))
        self.height_box.set(f"{round(self.image.height / self.image.width * width)}px")

    def change_width(self, event=None):
        height = int(self.height_box.get().rstrip("px"))
        self.width_box.set(f"{round(self.image.width / self.image.height * height)}px")

    def display_image(self):
        if self.image.width > self.image.height:
            display_image = self.image.resize(
                (500, round(self.image.height / self.image.width * 500))
            )
        elif self.image.width < self.image.height:
            display_image = self.image.resize(
                (round(self.image.width / self.image.height * 500), 500)
            )
        else:
            display_image = self.image.resize((500, 500))

        self.image_tk = ImageTk.PhotoImage(display_image)
        self.canvas.delete(self.placeholder_id)

        self.image_id = self.canvas.create_image(
            (500 - self.image_tk.width()) / 2,
            (500 - self.image_tk.height()) / 2,
            anchor=tk.NW,
            image=self.image_tk,
        )

    def rotate(self, angle):
        self.image = self.image.rotate(angle, expand=True)

        self.width_box.set(f"{self.image.width}px")
        self.height_box.set(f"{self.image.height}px")

        self.display_image()

    def flip_horizontal(self):
        self.image = ImageOps.mirror(self.image)
        self.display_image()

    def flip_vertical(self):
        self.image = ImageOps.flip(self.image)
        self.display_image()

    def save(self, file_path=None):
        file_format = self.format.get()

        if file_format in (".jpg", ".jpeg"):
            self.image = self.image.convert("RGB")
        if self.grayscale.get():
            self.image = self.image.convert("L")

        self.image = self.image.resize(
            (
                int(self.width_box.get().rstrip("px")),
                int(self.height_box.get().rstrip("px")),
            )
        )

        if file_path:
            self.image.save(file_path)
        else:
            self.image.save(os.path.splitext(self.file_path)[0] + file_format)

        self.restart()

    def save_as(self):
        file_format = self.format.get()

        save_path = filedialog.asksaveasfilename(
            filetypes=[
                ("Supported file formats", "*" + " ".join(self.format_list["values"]))
            ],
            defaultextension=file_format,
        )

        if save_path:
            self.save(save_path)

    def restart(self):
        self.canvas.delete(self.image_id)
        self.placeholder_id = self.canvas.create_image(
            0, 0, anchor=tk.NW, image=self.placeholder_image
        )

        self.first_click = True

        self.file_path = None
        self.image = None
        self.image_tk = None
        self.image_id = None

        self.grayscale.set(False)
        self.format.set("")
        self.width_box.set("")
        self.height_box.set("")

        self.grayscale_checkbox.configure(state="disabled")
        for row_frame in self.options_frame.winfo_children():
            for widget in row_frame.winfo_children():
                widget.configure(state="disabled")


class PixelSpinBox(ttk.Spinbox):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(
            font=FONT,
            from_=0,
            to=float("inf"),
            format="%.0fpx",
            width=5,
            foreground="black",
        )


if __name__ == "__main__":
    window = ThemedTk(theme="black", themebg=True)
    app = ImageProcessor(window)
    window.mainloop()
