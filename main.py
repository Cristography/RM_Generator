import os
import customtkinter as ctk  # Replaced tkinter with customtkinter
# These are still used for system dialogs
from tkinter import filedialog, messagebox
import colorsys
import random
import threading
from PIL import Image

# ==============================================================================
# PART 1: THE ADVANCED COLOR PALETTE GENERATOR (No changes here)
# ==============================================================================


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb_color):
    return '#{:02x}{:02x}{:02x}'.format(*rgb_color)


def generate_palette(base_color=None, harmony="analogous", num_colors=5, temperature=0.1, seed=None):
    if seed is not None:
        random.seed(seed)
    if base_color:
        try:
            r, g, b = [x / 255.0 for x in hex_to_rgb(base_color)]
        except (ValueError, TypeError):
            base_color = None
    if not base_color:
        base_h, base_s, base_l = random.random(), random.uniform(
            0.6, 1.0), random.uniform(0.4, 0.6)
    else:
        base_h, base_l, base_s = colorsys.rgb_to_hls(r, g, b)
    palette_hsl = [(base_h, base_l, base_s)]
    harmony_rules = {
        'analogous': [30/360, -30/360], 'complementary': [180/360],
        'split_complementary': [150/360, -150/360], 'triadic': [120/360, 240/360],
        'tetradic': [90/360, 180/360, 270/360]
    }
    hue_shifts = harmony_rules.get(harmony, [])
    current_colors = 1
    while current_colors < num_colors:
        source_h, source_l, source_s = random.choice(palette_hsl)
        hue_shift = random.choice(hue_shifts) if hue_shifts else 0
        new_h = (source_h + hue_shift) % 1.0
        h_jitter, s_jitter, l_jitter = [
            (random.uniform(-0.5, 0.5) * temperature) for _ in range(3)]
        new_h = (new_h + h_jitter) % 1.0
        new_s = max(0.2, min(0.95, source_s + s_jitter))
        new_l = max(0.2, min(0.9, source_l + l_jitter))
        palette_hsl.append((new_h, new_l, new_s))
        current_colors += 1
    final_palette = []
    for h, l, s in palette_hsl:
        r, g, b = [int(x * 255) for x in colorsys.hls_to_rgb(h, l, s)]
        final_palette.append(rgb_to_hex((r, g, b)))
    return final_palette

# ==============================================================================
# PART 2: THE IMAGE PROCESSING LOGIC (No changes here)
# ==============================================================================


def colorize_layer(image, color_rgb):
    colorized_image = Image.new('RGBA', image.size)
    r, g, b = color_rgb
    for x in range(image.width):
        for y in range(image.height):
            pixel = image.getpixel((x, y))
            if pixel[0] < 50 and pixel[1] < 50 and pixel[2] < 50 and pixel[3] > 0:
                colorized_image.putpixel((x, y), (r, g, b, pixel[3]))
            else:
                colorized_image.putpixel((x, y), pixel)
    return colorized_image


def generate_art(params, status_var):
    try:
        status_var.set("Starting...")
        image_files = sorted([f for f in os.listdir(
            params['input_dir']) if f.lower().endswith(('.png', '.jpg'))])
        if not image_files:
            messagebox.showerror(
                "Error", f"No image files found in:\n{params['input_dir']}")
            status_var.set("Idle.")
            return
        for i in range(params['num_to_generate']):
            status_var.set(
                f"Generating image {i + 1} of {params['num_to_generate']}...")
            palette = generate_palette(
                base_color=params['base_color'], harmony=params['harmony'],
                num_colors=len(image_files), temperature=params['temperature'],
                seed=None if not params['seed'] else int(params['seed']) + i
            )
            colorized_layers = []
            for idx, filename in enumerate(image_files):
                file_path = os.path.join(params['input_dir'], filename)
                layer_image = Image.open(file_path).convert('RGBA')
                color_hex = palette[idx % len(palette)]
                colorized_layers.append(colorize_layer(
                    layer_image, hex_to_rgb(color_hex)))
            if not colorized_layers:
                continue
            base_image = Image.new('RGBA', colorized_layers[0].size)
            for layer in colorized_layers:
                base_image.paste(layer, (0, 0), layer)
            output_path = os.path.join(
                params['output_dir'], f"{params['basename']}_{i + 1}.png")
            base_image.save(output_path)
        status_var.set(
            f"Success! Generated {params['num_to_generate']} images.")
        messagebox.showinfo(
            "Success", f"Finished generating all images in:\n{params['output_dir']}")
    except Exception as e:
        status_var.set("Error!")
        messagebox.showerror("An Error Occurred", str(e))

# ==============================================================================
# PART 3: THE CUSTOMTKINTER GRAPHICAL USER INTERFACE (GUI)
# ==============================================================================


class ArtGeneratorApp(ctk.CTk):  # Inherit from ctk.CTk
    def __init__(self):
        super().__init__()

        # --- Basic App Setup ---
        self.title("Harmonized Art Generator")
        self.geometry("550x580")
        ctk.set_appearance_mode("System")  # Options: "System", "Dark", "Light"
        ctk.set_default_color_theme("blue")

        # Configure the main grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Main Frame ---
        # Instead of ttk.Frame, we use ctk.CTkFrame
        main_frame = ctk.CTkFrame(
            self, corner_radius=0, fg_color="transparent")
        main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        main_frame.grid_columnconfigure(1, weight=1)

        # --- Variables (These are standard tkinter variables, ctk uses them) ---
        self.input_dir = ctk.StringVar()
        self.output_dir = ctk.StringVar()
        self.num_to_generate = ctk.StringVar(value="10")
        self.basename = ctk.StringVar(value="Art")
        self.base_color = ctk.StringVar(value="#3498db")
        self.harmony = ctk.StringVar(value="analogous")
        self.temperature = ctk.DoubleVar(value=0.1)
        self.seed = ctk.StringVar(value="")
        self.status_var = ctk.StringVar(
            value="Idle. Please select folders and click Generate.")

        self._create_widgets(main_frame)

    def _create_widgets(self, parent):
        # Create a bold font for headings
        heading_font = ctk.CTkFont(size=12, weight="bold")

        # --- Folder Selection ---
        ctk.CTkLabel(parent, text="1. Select Folders", font=heading_font).grid(
            row=0, column=0, columnspan=2, sticky='w', pady=(0, 5))
        ctk.CTkButton(parent, text="Input Folder (Image Layers)", command=self._select_input).grid(
            row=1, column=0, sticky='ew', padx=(0, 10))
        ctk.CTkEntry(parent, textvariable=self.input_dir,
                     state='disabled').grid(row=1, column=1, sticky='ew')
        ctk.CTkButton(parent, text="Output Folder (Saved Art)", command=self._select_output).grid(
            row=2, column=0, sticky='ew', padx=(0, 10), pady=(5, 0))
        ctk.CTkEntry(parent, textvariable=self.output_dir, state='disabled').grid(
            row=2, column=1, sticky='ew', pady=(5, 0))

        # --- Generation Settings ---
        ctk.CTkLabel(parent, text="2. Generation Settings", font=heading_font).grid(
            row=3, column=0, columnspan=2, sticky='w', pady=(20, 5))
        ctk.CTkLabel(parent, text="Number to Generate:").grid(
            row=4, column=0, sticky='w')
        ctk.CTkEntry(parent, textvariable=self.num_to_generate,
                     width=120).grid(row=4, column=1, sticky='w')
        ctk.CTkLabel(parent, text="Output Filename Base:").grid(
            row=5, column=0, sticky='w', pady=(5, 0))
        ctk.CTkEntry(parent, textvariable=self.basename).grid(
            row=5, column=1, sticky='w', pady=(5, 0))

        # --- Color Palette Settings ---
        ctk.CTkLabel(parent, text="3. Color Palette Settings", font=heading_font).grid(
            row=6, column=0, columnspan=2, sticky='w', pady=(20, 5))
        ctk.CTkLabel(parent, text="Base Color (Hex, or empty):").grid(
            row=7, column=0, sticky='w')
        ctk.CTkEntry(parent, textvariable=self.base_color).grid(
            row=7, column=1, sticky='w')

        ctk.CTkLabel(parent, text="Color Harmony:").grid(
            row=8, column=0, sticky='w', pady=(5, 0))
        harmonies = ['analogous', 'complementary',
                     'split_complementary', 'triadic', 'tetradic']
        ctk.CTkComboBox(parent, variable=self.harmony, values=harmonies,
                        state='readonly').grid(row=8, column=1, sticky='w', pady=(5, 0))

        ctk.CTkLabel(parent, text="Temperature (Boldness):").grid(
            row=9, column=0, sticky='w', pady=(5, 0))
        # ttk.Scale is replaced by ctk.CTkSlider
        ctk.CTkSlider(parent, from_=0.0, to=1.0, variable=self.temperature).grid(
            row=9, column=1, sticky='ew', pady=(5, 0))

        ctk.CTkLabel(parent, text="Seed (Optional):").grid(
            row=10, column=0, sticky='w', pady=(5, 0))
        ctk.CTkEntry(parent, textvariable=self.seed).grid(
            row=10, column=1, sticky='w', pady=(5, 0))

        # --- Action Button ---
        # The styling is now done with direct parameters
        generate_button = ctk.CTkButton(
            parent, text="Generate Art", command=self._start_generation,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#0078D7", hover_color="#005a9e"
        )
        generate_button.grid(row=11, column=0, columnspan=2,
                             sticky='ew', pady=(30, 10))

        # --- Status Bar ---
        ctk.CTkLabel(parent, textvariable=self.status_var, anchor='w').grid(
            row=12, column=0, columnspan=2, sticky='ew', pady=(10, 0))

    def _select_input(self):
        path = filedialog.askdirectory(
            title="Select Input Folder with Image Layers")
        if path:
            self.input_dir.set(path)

    def _select_output(self):
        path = filedialog.askdirectory(
            title="Select Folder to Save Generated Art")
        if path:
            self.output_dir.set(path)

    def _start_generation(self):
        params = {
            'input_dir': self.input_dir.get(), 'output_dir': self.output_dir.get(),
            'num_to_generate': int(self.num_to_generate.get()), 'basename': self.basename.get(),
            'base_color': self.base_color.get() or None, 'harmony': self.harmony.get(),
            'temperature': self.temperature.get(), 'seed': self.seed.get() or None
        }
        if not params['input_dir'] or not params['output_dir']:
            messagebox.showwarning(
                "Warning", "Please select both an input and output folder.")
            return
        thread = threading.Thread(
            target=generate_art, args=(params, self.status_var))
        thread.daemon = True
        thread.start()


if __name__ == '__main__':
    app = ArtGeneratorApp()
    app.mainloop()
