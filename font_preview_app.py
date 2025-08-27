import tkinter as tk
from tkinter import font
from tkinter import ttk
import platform

# --- Initialize root window first ---
root = tk.Tk()
root.title("Font Picker")
root.geometry("800x900")

# --- Tkinter Variables ---
font_size = tk.IntVar(value=16)
use_bold = tk.BooleanVar()
use_italic = tk.BooleanVar()
is_dark_mode = tk.BooleanVar(value=False)
selected_fonts = []

# --- Entry field (defined early so it's available in functions) ---
entry = tk.Entry(root, font=('Arial', 14), width=50)
entry.insert(0, "The quick brown fox jumps over the lazy dog.")
entry.pack(pady=10)

# --- Helper Functions ---

def get_font_style():
    style = []
    if use_bold.get():
        style.append("bold")
    if use_italic.get():
        style.append("italic")
    return " ".join(style) if style else "normal"

def toggle_selection(font_name, var):
    if var.get():
        if font_name not in selected_fonts:
            selected_fonts.append(font_name)
    else:
        if font_name in selected_fonts:
            selected_fonts.remove(font_name)
    update_compare_button_state()  # ← Always run this after change

def apply_theme(window=None):
    if window is None:
        window = root
    
    # Determine the theme (dark or light)
    theme = "dark" if is_dark_mode.get() else "light"
    
    # Set background and foreground colors
    bg_color = "#1e1e1e" if theme == "dark" else "#ffffff"
    fg_color = "#ffffff" if theme == "dark" else "#000000"
    
    # Apply theme to the root window
    window.configure(bg=bg_color)

    # Create a new ttk Style object
    style = ttk.Style()
    style.theme_use("default")

    # Button style
    style.configure("Custom.TButton",
                    background=bg_color,
                    foreground=fg_color,
                    borderwidth=1,
                    focusthickness=3,
                    focuscolor="none")
    style.map("Custom.TButton",
              background=[('active', bg_color)],
              foreground=[('active', fg_color)])

    # Apply dark/light mode to all widgets, including ttk widgets
    def update_widget_colors(widget):
        # Handle tkinter (tk) widgets with bg property
        if isinstance(widget, (tk.Frame, tk.LabelFrame)):
            widget.configure(bg=bg_color)
        elif isinstance(widget, tk.Label):
            widget.configure(bg=bg_color, fg=fg_color)
        elif isinstance(widget, tk.Entry):
            widget.configure(bg=bg_color, fg=fg_color, insertbackground=fg_color)
        elif isinstance(widget, tk.Checkbutton):
            widget.configure(bg=bg_color, fg=fg_color, selectcolor=bg_color)
        elif isinstance(widget, tk.Scale):
            widget.configure(bg=bg_color, fg=fg_color)
        elif isinstance(widget, tk.Canvas):
            widget.configure(bg=bg_color)
        
        # Handle ttk widgets (no bg property, use style)
        elif isinstance(widget, ttk.Button):
            widget.configure(style="Custom.TButton")
        elif isinstance(widget, ttk.Checkbutton):
            style.configure("TCheckbutton",
                            background=bg_color,
                            foreground=fg_color,
                            selectcolor=bg_color)
        elif isinstance(widget, ttk.Entry):
            style.configure("TEntry",
                            fieldbackground=bg_color,
                            foreground=fg_color)
        elif isinstance(widget, ttk.Combobox):
            style.configure("TCombobox",
                            fieldbackground=bg_color,
                            foreground=fg_color)

        # Apply the update recursively to child widgets
        for child in widget.winfo_children():
            update_widget_colors(child)

    update_widget_colors(window)  # Start the theme update from the window


def compare_selected():
    if not selected_fonts:
        return

    top = tk.Toplevel(root)  # Create the top-level window
    top.title("Font Comparison")
    top.geometry("700x700")

    # Pass the current theme mode to the comparison window
    top.is_dark_mode = is_dark_mode.get()  # Store the current theme state in the top-level window

    sentence = entry.get()

    # Create widgets inside the new window first, before applying the theme
    compare_canvas = tk.Canvas(top)
    scrollbar = ttk.Scrollbar(top, orient="vertical", command=compare_canvas.yview)
    compare_frame = ttk.Frame(compare_canvas)

    compare_frame.bind(
        "<Configure>",
        lambda e: compare_canvas.configure(scrollregion=compare_canvas.bbox("all"))
    )

    compare_canvas.create_window((0, 0), window=compare_frame, anchor="nw")
    compare_canvas.configure(yscrollcommand=scrollbar.set)

    compare_canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Add font previews
    for f in selected_fonts:
        try:
            font_block = tk.Frame(compare_frame)
            font_block.pack(fill='x', pady=15, padx=20, anchor='w')

            font_name_label = tk.Label(font_block, text=f, font=('Arial', 12, 'bold'), fg='#222')
            font_name_label.pack(anchor='w', pady=(0, 5))

            font_preview = tk.Label(
                font_block,
                text=sentence,
                font=(f, font_size.get(), get_font_style()),
                wraplength=650,
                justify='left'
            )
            font_preview.pack(anchor='w')
        except:
            pass

    # Apply the theme to the comparison window based on its dark mode state
    apply_theme(top)

def render_fonts():
    sentence = entry.get()
    for widget in display_frame.winfo_children():
        widget.destroy()

    for f in font.families():
        try:
            font_frame = tk.Frame(display_frame)
            font_frame.pack(fill='x', pady=5)

            var = tk.BooleanVar()
            checkbox = tk.Checkbutton(
                font_frame,
                variable=var,
                command=lambda f=f, v=var: toggle_selection(f, v)
            )
            checkbox.pack(side='left', padx=(10, 5))

            name_label = tk.Label(font_frame, text=f, font=('Arial', 10, 'bold'), fg='#555')
            name_label.pack(side='left')

            preview_label = tk.Label(
                font_frame,
                text=sentence,
                font=(f, font_size.get(), get_font_style()),
                anchor='w'
            )
            preview_label.pack(anchor='w', padx=40)
        except:
            pass

def update_compare_button_state():
    if selected_fonts:
        compare_button.config(state=tk.NORMAL)
    else:
        compare_button.config(state=tk.DISABLED)


# --- UI Elements ---

# Buttons
button = ttk.Button(root, text="Render in All Fonts", command=render_fonts)
button.pack(pady=5)

compare_button = ttk.Button(root, text="Compare Selected Fonts", command=compare_selected, state=tk.DISABLED)  # Start disabled
compare_button.pack(pady=5)

# Font size slider
scale_frame = tk.Frame(root)
scale_frame.pack(pady=5)

tk.Label(scale_frame, text="Font Size:").pack(side='left', padx=(0, 5))

font_scale = tk.Scale(
    scale_frame,
    from_=8,
    to=72,
    orient='horizontal',
    variable=font_size,
    command=lambda x: render_fonts()  # ← only triggers font re-rendering
)
font_scale.pack(side='left')


# Bold/Italic checkboxes
style_frame = tk.Frame(root)
tk.Label(style_frame, text="Style:").pack(side='left', padx=(0, 5))
tk.Checkbutton(style_frame, text="Bold", variable=use_bold, command=render_fonts).pack(side='left')
tk.Checkbutton(style_frame, text="Italic", variable=use_italic, command=render_fonts).pack(side='left')
style_frame.pack(pady=5)

# Scrollable preview area
container = ttk.Frame(root)
canvas = tk.Canvas(container)
scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Dark mode toggle
theme_frame = tk.Frame(root)
theme_frame.pack(pady=5)

tk.Checkbutton(
    theme_frame,
    text="Dark Mode",
    variable=is_dark_mode,
    command=apply_theme  # ← call directly, no lambda or arguments
).pack()


# Create a main frame that will hold all widgets (buttons, scales, etc.)
main_frame = ttk.Frame(scrollable_frame)
main_frame.pack(fill='both', expand=True)

# Place the main_frame widgets here
main_frame.pack()

container.pack(fill='both', expand=True, padx=10, pady=10)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

display_frame = scrollable_frame

# --- Trackpad scrolling functions ---
def _on_mousewheel(event):
    # Windows/Linux behavior
    canvas.yview_scroll(-1 * int(event.delta / 120), "units")

def _on_mac_scroll(event):
    # macOS specific behavior
    canvas.yview_scroll(-1 * int(event.delta), "units")

def bind_mousewheel(widget):
    if platform.system() == 'Darwin':
        widget.bind("<MouseWheel>", _on_mac_scroll)
    else:
        widget.bind("<MouseWheel>", _on_mousewheel)
        widget.bind("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # Linux scroll up
        widget.bind("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))   # Linux scroll down

# Bind mousewheel scrolling to both canvas and scrollable_frame
bind_mousewheel(canvas)
bind_mousewheel(scrollable_frame)

apply_theme()


# Launch app
root.mainloop()
