import tkinter as tk
import random

# Global flags
auto_generating = fast_auto_generating = False
gradient_reversed = background_invisible = False

# Function to generate and display a random number with color
def generate_random_number(event=None):
    number = random.randint(1, 100)
    color = get_color_for_number(number)
    result_label.config(text=str(number), fg=color)

# Function to calculate color based on the number and gradient direction
def get_color_for_number(number):
    if gradient_reversed:
        red = int(number * (255 / 99))
        green = 255 - int((number - 1) * (255 / 99))
    else:
        red = 255 - int((number - 1) * (255 / 99))
        green = int(number * (255 / 99))
    return f'#{red:02x}{green:02x}00'  # Hex format color

# Toggle functions
def toggle_auto_generation():
    global auto_generating
    auto_generating = not auto_generating
    if auto_generating:
        auto_generate_numbers()

def toggle_fast_auto_generation():
    global fast_auto_generating
    fast_auto_generating = not fast_auto_generating
    if fast_auto_generating:
        fast_auto_generate_numbers()

def stop_generations():
    global auto_generating, fast_auto_generating
    auto_generating = fast_auto_generating = False

def toggle_gradient():
    global gradient_reversed
    gradient_reversed = not gradient_reversed
    generate_random_number()

def toggle_background_visibility():
    global background_invisible
    background_invisible = not background_invisible
    app.wm_attributes('-transparentcolor', '#1e1f22' if background_invisible else '')

# Auto generation functions
def auto_generate_numbers():
    if auto_generating:
        generate_random_number()
        app.after(3000, auto_generate_numbers)

def fast_auto_generate_numbers():
    if fast_auto_generating:
        generate_random_number()
        app.after(1500, fast_auto_generate_numbers)

# Close app function
def close_app():
    app.destroy()

# Window drag functions
def start_move(event):
    app.x_offset, app.y_offset = event.x, event.y

def on_move(event):
    app.geometry(f"+{app.winfo_pointerx() - app.x_offset}+{app.winfo_pointery() - app.y_offset}")

# Resize functions
def start_resize(event):
    app.bind("<B1-Motion>", resize)

def resize(event):
    new_width, new_height = event.x_root - app.winfo_rootx(), event.y_root - app.winfo_rooty()
    if new_width >= 200 and new_height >= 150:
        app.geometry(f"{new_width}x{new_height}")

def stop_resize(event):
    app.unbind("<B1-Motion>")

# Create main app window
app = tk.Tk()
app.title("Random Number Generator")
app.geometry("400x300")
app.configure(bg='#1e1f22')
app.attributes('-topmost', 1)
app.overrideredirect(True)

# Add draggable top bar
top_bar = tk.Frame(app, bg='#1e1f22', height=30)
top_bar.pack(fill=tk.X, side=tk.TOP)
top_bar.bind("<Button-1>", start_move)
top_bar.bind("<B1-Motion>", on_move)

# Add buttons to the top bar
tk.Button(top_bar, text="X", command=close_app, bg='#1e1f22', fg="white", font=("Arial", 10), borderwidth=0).pack(side=tk.RIGHT, padx=5)
menu_button = tk.Button(top_bar, text="⋮", bg='#1e1f22', fg="white", font=("Arial", 12), borderwidth=0)
menu_button.pack(side=tk.RIGHT, padx=5)

# Create menu
menu = tk.Menu(app, tearoff=0, bg='#2c2f38', fg="white", font=("Arial", 12))
menu.add_command(label="Auto", command=toggle_auto_generation)
menu.add_command(label="Fast Auto", command=toggle_fast_auto_generation)
menu.add_command(label="Stop", command=stop_generations)
menu.add_command(label="Change Gradient", command=toggle_gradient)
menu.add_command(label="Toggle Background", command=toggle_background_visibility)

# Show menu on button click
menu_button.bind("<Button-1>", lambda e: menu.post(e.x_root, e.y_root))

# Add result label and initialize it with a random number
initial_number = random.randint(1, 100)
initial_color = get_color_for_number(initial_number)
result_label = tk.Label(app, text=str(initial_number), font=("Arial", 72), fg=initial_color, bg='#1e1f22')
result_label.pack(pady=20, expand=True)

# Bind mouse click to generate numbers
app.bind("<Button-1>", generate_random_number)

# Add resize icon
resize_icon = tk.Label(app, text="↔", font=("Arial", 14), fg="white", bg='#1e1f22', cursor="sizing")
resize_icon.place(relx=1.0, rely=1.0, x=-15, y=-15, anchor="se")
resize_icon.bind("<ButtonPress-1>", start_resize)
resize_icon.bind("<ButtonRelease-1>", stop_resize)

# Run app
app.mainloop()
