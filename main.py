import tkinter as tk
from tkinter import messagebox, filedialog
import pyfiglet
import random
from PIL import Image, ImageDraw, ImageFont

# --- State Variables ---
# To store the current logo and font so "Save" uses what's displayed
current_logo_text = ""
current_font_name = ""

# --- Core Functions ---

def get_font():
    """Gets the selected font, handling random selection or user input."""
    if random_font_var.get():
        figlet_instance = pyfiglet.Figlet()
        fonts = figlet_instance.getFonts()
        return random.choice(fonts)
    else:
        selected_font = font_entry.get()
        if not selected_font:
            messagebox.showwarning("Font Error", "Please enter a font name or check 'Use Random Font'.")
            return None
            
        figlet_instance = pyfiglet.Figlet()
        if selected_font not in figlet_instance.getFonts():
            messagebox.showwarning("Font Error", f"Font '{selected_font}' not found!")
            return None
        return selected_font

def generate_and_show_logo():
    """Generates the logo from user input and displays it in the GUI."""
    global current_logo_text, current_font_name
    
    user_text = entry.get()
    if not user_text:
        messagebox.showwarning("Input Error", "Please enter some text to generate a logo!")
        return

    selected_font = get_font()
    if not selected_font:
        return

    # Store the generated logo and font name globally
    current_font_name = selected_font
    current_logo_text = pyfiglet.figlet_format(user_text, font=current_font_name)
    
    # Update GUI
    logo_text.config(state=tk.NORMAL)
    logo_text.delete(1.0, tk.END)
    logo_text.insert(tk.END, current_logo_text)
    logo_text.config(state=tk.DISABLED)
    
    font_label.config(text=f"Selected Font: {current_font_name}")
    # If a random font was used, show its name in the entry box
    if random_font_var.get():
        font_entry.config(state=tk.NORMAL)
        font_entry.delete(0, tk.END)
        font_entry.insert(0, current_font_name)
        font_entry.config(state=tk.DISABLED)


def copy_to_clipboard():
    """Copies the displayed logo text to the clipboard."""
    if current_logo_text:
        root.clipboard_clear()
        root.clipboard_append(current_logo_text)
        messagebox.showinfo("Copied", "Logo copied to clipboard!")
    else:
        messagebox.showwarning("Copy Error", "There is no logo to copy!")

def save_as_png():
    """Saves the currently displayed logo as a high-quality PNG image."""
    if not current_logo_text:
        messagebox.showwarning("Save Error", "Please generate a logo before saving!")
        return

    # Ask user for save location
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
    )
    if not file_path:
        return # User cancelled the save dialog

    try:
        # Use a common monospace font. Adjust size as needed.
        # This is crucial for preserving the ASCII art's alignment.
        try:
            # Use a high-quality monospace font if available
            font = ImageFont.truetype("cour.ttf", 10)
        except IOError:
            # Fallback to a default font if Courier is not found
            font = ImageFont.load_default()

        # Dynamically calculate the image size based on the text dimensions
        temp_draw = ImageDraw.Draw(Image.new("RGB", (0, 0)))
        left, top, right, bottom = temp_draw.textbbox((0, 0), current_logo_text, font=font)
        text_width = right - left
        text_height = bottom - top
        
        padding = 20
        image_size = (text_width + 2 * padding, text_height + 2 * padding)

        # Create the image
        image = Image.new("RGB", image_size, color="white")
        draw = ImageDraw.Draw(image)
        
        # Draw the text onto the image
        draw.text((padding, padding), current_logo_text, font=font, fill="black")

        # Save the final image
        image.save(file_path)
        messagebox.showinfo("Saved", f"Logo successfully saved as {file_path}")

    except Exception as e:
        messagebox.showerror("Save Error", f"An error occurred while saving the image:\n{e}")

def toggle_font_entry():
    """Enables or disables the font entry box based on the checkbox state."""
    if random_font_var.get():
        font_entry.config(state=tk.DISABLED)
    else:
        font_entry.config(state=tk.NORMAL)


# --- GUI Setup ---
root = tk.Tk()
root.title("ASCII Art Logo Generator")
root.geometry("700x650")
root.configure(bg="#f0f0f0")

# --- Widgets ---
title_label = tk.Label(root, text="ASCII Art Logo Generator", font=("Arial", 20, "bold"), bg="#f0f0f0")
title_label.pack(pady=10)

entry_label = tk.Label(root, text="Enter your text:", font=("Arial", 12), bg="#f0f0f0")
entry_label.pack(pady=5)
entry = tk.Entry(root, font=("Arial", 12), width=50)
entry.pack(pady=5)

random_font_var = tk.BooleanVar()
random_font_check = tk.Checkbutton(
    root, 
    text="Use Random Font", 
    variable=random_font_var, 
    font=("Arial", 12), 
    bg="#f0f0f0",
    command=toggle_font_entry  # Add command to toggle entry box
)
random_font_check.pack(pady=5)

font_entry_label = tk.Label(root, text="Or enter font name:", font=("Arial", 12), bg="#f0f0f0")
font_entry_label.pack(pady=5)
font_entry = tk.Entry(root, font=("Arial", 12), width=50)
font_entry.pack(pady=5)

generate_button = tk.Button(root, text="Generate Logo", command=generate_and_show_logo, font=("Arial", 14), bg="#4CAF50", fg="white")
generate_button.pack(pady=15)

font_label = tk.Label(root, text="Selected Font: None", font=("Arial", 12, "italic"), bg="#f0f0f0")
font_label.pack(pady=5)

logo_text = tk.Text(root, font=("Courier New", 10), width=80, height=15, wrap=tk.WORD, bg="#ffffff", state=tk.DISABLED)
logo_text.pack(pady=10, padx=10)

# Frame for buttons
button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack(pady=10)

copy_button = tk.Button(button_frame, text="Copy to Clipboard", command=copy_to_clipboard, font=("Arial", 12), bg="#2196F3", fg="white")
copy_button.pack(side=tk.LEFT, padx=10)

save_button = tk.Button(button_frame, text="Save as PNG", command=save_as_png, font=("Arial", 12), bg="#FF9800", fg="white")
save_button.pack(side=tk.LEFT, padx=10)

# --- Main Loop ---
root.mainloop()