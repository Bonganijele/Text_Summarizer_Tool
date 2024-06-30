import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox, font
from transformers import pipeline
from load_file import load_txt_file
from save_file import save_txt_file
from nltk.tokenize import sent_tokenize
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords
# import customtkinter
import threading
import ttkbootstrap as tb
from ttkbootstrap import Style
import nltk
import logging
import os
import sys

from langdetect import detect  # Import for language detection
from sklearn.feature_extraction.text import CountVectorizer  # Import for keyword extraction

# Load the required NLTK data files
nltk.download('punkt')
nltk.download('stopwords')

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Ensure that NLTK data is available
try:
    nltk.download('punkt', quiet=True)
except Exception as e:
    logging.error(f"Error downloading NLTK data: {e}")
    sys.exit("Error: NLTK data download failed.")
    

# Handle resource paths for pyinstaller
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Load your NLTK data files using the correct resource path
nltk_data_path = resource_path('nltk_data')
if os.path.exists(nltk_data_path):
    nltk.data.path.append(nltk_data_path)
else:
    logging.warning(f"NLTK data path '{nltk_data_path}' does not exist. Proceeding without it.")

# Summarizer pipeline
try:
    summarizer = pipeline("summarization")
except Exception as e:
    logging.error(f"Error initializing the summarization pipeline: {e}")
    sys.exit("Error: Summarization pipeline initialization failed.")


# Summarizer pipeline
summarizer = pipeline("summarization")

# Function to update the value labels
def update_label(label, var):
    label.config(text=f"{var.get():.2f}")

# Initialize the main window
root = tk.Tk()
style = Style(theme="darkly")  # Set initial theme to dark
menu_bar = tk.Menu(root)
root.title("Text Summarization Tool")
root.geometry("1010x680")

# The function to handle file loading
def handle_load_button_click():
    load_txt_file(text_area)

# The function to handle file saving
def handle_save_button_click():
    save_txt_file(summary_area)

# Function to show About window
def show_about():
    about_text = (
        "Text Summarization Tool\n\n"
        "Version 1.0\n\n"
        "This Text Summarization Tool is a user-friendly application designed to\n provide concise summaries of longer texts."
    )

    # Create a new top-level window
    about_window = tk.Toplevel(root)
    about_window.title("About")
    about_window.geometry("640x450")
    about_window.transient(root)  # Window child of the main window
    about_window.grab_set()  # Focus on this window
    about_window.resizable(False, False)

    # Function to track and move the about window with the main window
    def on_drag(event):
        x = root.winfo_x() + event.x_root - root.winfo_rootx()
        y = root.winfo_y() + event.y_root - root.winfo_rooty()
        about_window.geometry(f"+{x + (root.winfo_width() - 300) // 2}+{y + (root.winfo_height() - 200) // 2}")

    # Bind the drag event to the main window
    root.bind('<B1-Motion>', on_drag)

    # Center align text
    about_label = tk.Label(
        about_window,
        text=about_text,
        font=('Verdana', 12),
        justify='center'
    )
    about_label.pack(expand=True, fill='both', padx=10, pady=10)
    
# Function that displays the keyboard shortcuts
def show_keyboard_shortcuts():
    about_text = (
        
        "Keyboard shortcuts for Linux\n\n\n"
        "Ctrl+A     Show About window\n"
        "Ctrl+H     Report Issue\n"
        "Ctrl+K     Keyboard Shortcuts Reference\n"
        "Ctrl+F     Feedback\n"
        "Ctrl+O     Open File\n"
        "Ctrl+S     Save File"
    )

    # Create a new top-level window
    keyboard_shortcuts_shortcut_window = tk.Toplevel(root)
    keyboard_shortcuts_shortcut_window.title("Keyboard Shortcuts")
    keyboard_shortcuts_shortcut_window.geometry("640x450")
    keyboard_shortcuts_shortcut_window.transient(root)  # Window child of the main window
    keyboard_shortcuts_shortcut_window.grab_set()  # Focus on this window
    keyboard_shortcuts_shortcut_window.resizable(False, False)

    # Function to track and move the about window with the main window
    def on_drag(event):
        x = root.winfo_x() + event.x_root - root.winfo_rootx()
        y = root.winfo_y() + event.y_root - root.winfo_rooty()
        keyboard_shortcuts_shortcut_window.geometry(f"+{x + (root.winfo_width() - 300) // 2}+{y + (root.winfo_height() - 200) // 2}")

    # Bind the drag event to the main window
    root.bind('<B1-Motion>', on_drag)

    # Center align text
    shortcut_label = tk.Label(
        keyboard_shortcuts_shortcut_window,
        text=about_text,
        font=('Verdana', 12),
        justify='left',  # Align the text to the left
        pady=4
    )
    shortcut_label.pack(expand=True, fill='both', padx=5, pady=5)




# Function to show feedback dialog
def show_feedback_dialog():
    feedback_window = tk.Toplevel(root)
    feedback_window.title("Feedback")
    feedback_window.geometry("600x500")
    feedback_window.grab_set()
    feedback_window.attributes("-topmost", True)  # Ensure it stays on top
    # feedback_window.attributes('-toolwindow', True)  # Remove maximize and minimize buttons
    
    feedback_label = ttk.Label(feedback_window, text="We appreciate your feedback!")
    feedback_label.pack(pady=10)
    
    feedback_text = scrolledtext.ScrolledText(feedback_window, wrap=tk.WORD, width=80, height=20)
    feedback_text.pack(padx=20, pady=10)
    
    submit_feedback_btn = ttk.Button(feedback_window, text="Submit Feedback", command=submit_feedback)
    submit_feedback_btn.pack(pady=10)
    
    # Function to track and move the feedback window with the main window
    def on_drag(event):
        x = root.winfo_x() + event.x_root - root.winfo_rootx()
        y = root.winfo_y() + event.y_root - root.winfo_rooty()
        feedback_window.geometry(f"+{x + (root.winfo_width() - 300) // 2}+{y + (root.winfo_height() - 200) // 2}")

    # Bind the drag event to the main window
    root.bind('<B1-Motion>', on_drag)

# Function to submit feedback
def submit_feedback():
    feedback = feedback_text.get("1.0", tk.END).strip()
    # Logic to handle feedback submission (e.g., save to file or database)
    messagebox.showinfo("Feedback Submitted", "Thank you for your feedback!")
    feedback_window.destroy()  # Close the feedback window after submission
 
# File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Open..", command=handle_load_button_click, accelerator="Ctrl+O")
file_menu.add_command(label="Save File", command=handle_save_button_click, accelerator="Ctrl+S")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)


# Help Menu
help_ = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Help', menu=help_)
help_.add_command(label='Keyboard Shortcuts Reference', command=show_keyboard_shortcuts, accelerator="Ctrl+K")
help_.add_command(label='Feedback', command=show_feedback_dialog, accelerator='Ctrl+F')
help_.add_separator()
help_.add_command(label='About (Ctrl+A)', command=show_about, accelerator="Ctrl+A")


# Set the menu
root.config(menu=menu_bar)

    
# Define a function to handle the keyboard shortcut
def open_file(event):
    handle_load_button_click()
    
def save_file(event):
    handle_save_button_click()
    
def about_shortcut(event):
    show_about()


def keyboard_shortcuts_shortcut(event):
    show_keyboard_shortcuts()
    
def feedback_shortcut(event):
    show_feedback_dialog()
    

# Bind the keyboard shortcuts to the functions
root.bind_all("<Control-o>", open_file)
root.bind_all("<Control-s>", save_file)
root.bind_all("<Control-a>", about_shortcut)
root.bind_all("<Control-k>", keyboard_shortcuts_shortcut)
root.bind_all("<Control-f>", feedback_shortcut)

# Custom fonts & size
custom_font = font.Font(family='Verdana', size=12)
custom_font_logo = font.Font(family='Verdana', size=14)

# Side panel frame
side_panel = ttk.Frame(root)
side_panel.pack(side='left', fill='both')

# Logo for side panel frame
label = ttk.Label(side_panel, text="Text Summarizer Tool", font=custom_font_logo)
label.pack(pady=20)

# Load file button
load_file_button = ttk.Button(side_panel, text="Load file", width=20, command=handle_load_button_click)
load_file_button.pack(pady=10, padx=5)

# Save button for summary
save_btn = ttk.Button(side_panel, text="Save Summary", width=20, command=lambda: save_txt_file(summary_area) )
save_btn.pack(pady=10, padx=5)

# Function to toggle theme
def toggle_theme():
    current_theme = style.theme_use()
    new_theme = "darkly" if current_theme == "flatly" else "flatly"
    style.theme_use(new_theme)
    change_theme_btn.config(text="Light mode" if new_theme == "darkly" else "Dark mode")

# Change Theme Button
change_theme_btn = ttk.Button(side_panel, text="Light mode", width=20, command=toggle_theme)
change_theme_btn.pack(side="bottom", pady=12, padx=5)

# Main content frame
main_frame = ttk.Frame(root)
main_frame.pack(side='left', fill='both', expand=True)

# Grid layout for the main_frame
main_frame.columnconfigure(1, weight=1)
main_frame.columnconfigure(3, weight=1)

# Frame to group model selection and top choices sampling
options_frame = ttk.Frame(main_frame)
options_frame.grid(row=0, column=0, columnspan=4, padx=10, pady=7, sticky='w')

# Dropdown for model selection
model_options = [ "t5-small","facebook/bart-large-cnn"]
model_var = tk.StringVar(root)
model_var.set(model_options[0])  # The default model

model_label = ttk.Label(options_frame, text="Model:", font=custom_font)
model_label.grid(row=0, column=0, padx=(0, 5), pady=6, sticky='w')

model_menu = ttk.OptionMenu(options_frame, model_var, model_options[0], *model_options)
model_menu.grid(row=0, column=1, padx=(0, 20), pady=6, sticky='w')

# Summary scale
label_summary_scale = ttk.Label(options_frame, text="Summary Length %:", font=custom_font)
label_summary_scale.grid(row=0, column=2, padx=(20, 5), pady=6, sticky='w')

summary_scale_var = tk.IntVar()
summary_scale = tb.Scale(options_frame, from_=120, to=300, orient=tk.HORIZONTAL, length=120, variable=summary_scale_var)
summary_scale.set(140)  # Default value
summary_scale.grid(row=0, column=3, padx=(5, 20), pady=6, sticky='w')

summary_value_label = ttk.Label(options_frame, text=f"{summary_scale_var.get()}", font=custom_font)
summary_value_label.grid(row=0, column=4, padx=(5, 20), pady=6, sticky='w')

# Updating the label when scale changes
summary_scale_var.trace("w", lambda name, index, mode, var=summary_scale_var: update_label(summary_value_label, var))


# Create a label to display the text length
length_label = ttk.Label(options_frame, text="Character Count: 0", font=custom_font)
length_label.grid(row=0, column=5, padx=(5, 20), pady=6, sticky='w')



# # Bind text entry changes to the update function
# text_entry = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=20)
# text_entry.grid(row=1, column=0, columnspan=4, padx=10, pady=5, sticky='nsew')


# Configure column weights to ensure proper spacing and alignment
options_frame.grid_columnconfigure(0, weight=1)
options_frame.grid_columnconfigure(1, weight=1)
options_frame.grid_columnconfigure(2, weight=1)
options_frame.grid_columnconfigure(3, weight=1)
options_frame.grid_columnconfigure(4, weight=1)

# Function to show context menu
def show_context_menu(event, text_widget):
    context_menu.tk_popup(event.x_root, event.y_root)
    # Set focus to the text widget where the right-click occurred
    text_widget.focus()

def cut_text():
    text_area.event_generate("<<Cut>>")

def copy_text():
    text_area.event_generate("<<Copy>>")

def paste_text():
    text_area.event_generate("<<Paste>>")
    

# Function to update character count
def update_character_count(event=None):
    text = text_area.get("1.0", "end-1c").strip()  # Remove leading and trailing whitespace
    text_length = len(text)
    length_label.config(text=f"Character Count: {text_length}")

# Text input area
text_area = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=13)
text_area.grid(row=1, column=0, columnspan=4, padx=10, pady=5, sticky='nsew')
text_area.bind("<KeyRelease>", update_character_count)


# Context menu for copy-paste operations
context_menu = tk.Menu(root, tearoff=0)
context_menu.add_command(label="Cut", command=cut_text)
context_menu.add_command(label="Copy", command=copy_text)
context_menu.add_command(label="Paste", command=paste_text)

# Bind the right-click event to show the context menu
text_area.bind("<Button-3>", lambda event: show_context_menu(event, text_area))


summary_area = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=10, state=tk.NORMAL)
summary_area.grid(row=3, column=0, columnspan=4, padx=10, pady=5, sticky='nsew')
summary_area.bind("<Button-3>", lambda event: show_context_menu(event, summary_area))



# Progress bar frame
progress_frame = ttk.Frame(main_frame)
progress_frame.grid(row=4, column=0, columnspan=4, padx=10, pady=10, sticky='ew')

# Progress bar label
progress_bar_label = ttk.Label(progress_frame, text="Progress:", font=custom_font)
progress_bar_label.grid(row=0, column=0, padx=(0, 5), pady=6, sticky='w')

# Progress bar widget
progress = ttk.Progressbar(progress_frame, orient=tk.HORIZONTAL, length=120, mode='determinate')
progress.grid(row=0, column=1, padx=10, pady=6, sticky='w')

# Language detection label
lang_label = ttk.Label(main_frame, text="Detected Language: N/A", font=custom_font)
lang_label.grid(row=5, column=0, padx=10, pady=6, sticky='w')

# Configure columns to expand and shrink
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)
main_frame.grid_columnconfigure(2, weight=1)
main_frame.grid_columnconfigure(3, weight=1)

# Configure rows to expand and shrink
main_frame.grid_rowconfigure(1, weight=1)
main_frame.grid_rowconfigure(2, weight=1)
main_frame.grid_rowconfigure(3, weight=1)
main_frame.grid_rowconfigure(4, weight=0)  # Progress frame should not expand

def update_summary_area(summary_text):
    summary_area.config(state=tk.NORMAL)
    summary_area.delete("1.0", tk.END)
    summary_area.insert(tk.END, summary_text)
    summary_area.config(state=tk.DISABLED)

def detect_language(text):
    try:
        print("Detecting language...")
        language = detect(text)
        print("Language detected:", language)
    except Exception as e:
        print(f"Language detection error: {e}")
        language = "N/A"
    finally:
        print("Updating language label...")
        lang_label.config(text=f"Detected Language: {language}")


# Function to extract keywords using NLTK FreqDist
def extract_keywords(text):
    words = word_tokenize(text)  # Tokenize the input text
    stop_words = set(stopwords.words('english'))
    filtered_words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]
    freq_dist = FreqDist(filtered_words)
    top_keywords = freq_dist.most_common(5)
    keywords = [word for word, freq in top_keywords]
    return keywords

# Function to highlight keywords in the summary area
def highlight_keywords(keywords):
    summary_text = summary_area.get("1.0", tk.END)
    summary_area.tag_remove('keyword', '1.0', tk.END)
    
    for keyword in keywords:
        start_index = '1.0'
        while True:
            start_index = summary_area.search(keyword, start_index, stopindex=tk.END)
            if not start_index:
                break
            end_index = f"{start_index}+{len(keyword)}c"
            summary_area.tag_add('keyword', start_index, end_index)
            start_index = end_index

    summary_area.tag_config('keyword', foreground='yellow', underline=False)

# Function to perform summarization
def summarize_text():
    input_text = text_area.get("1.0", tk.END).strip()
    
    # Check if the input text is too short for summarization
    if len(input_text.split()) < 50:
        update_summary_area("Text too short for summarization.")
        return
    
    # Start progress indicator
    progress.start()
    root.update_idletasks()  # Update the UI
    
    # Function to perform summarization
    def perform_summarization():
        try:
            # Detect language
            language = detect(input_text)
            lang_label.config(text=f"Detected Language: {language}")
            
            # Define the summarizer model based on the language
            summarizer_model = model_var.get()
            
            summarizer_pipeline = pipeline("summarization", model=summarizer_model)

            # Update max_length parameter
            max_length = summary_scale_var.get()
            if max_length > 1024:
                max_length = 1024  # Ensure max_length does not exceed the model's maximum
            summarizer_pipeline.model.config.max_length = max_length
            
            # Perform summarization
            summary = summarizer_pipeline(input_text, max_length=max_length, min_length=100, do_sample=False)
            summary_text = summary[0]['summary_text']
            update_summary_area(summary_text)
            
            # Extract keywords and highlight them in the summary area
            keywords = extract_keywords(input_text)
            highlight_keywords(keywords)

        except Exception as e:
            update_summary_area(f"Error: {str(e)}")
        
        finally:
            progress.stop()

    # Start summarization in a separate thread
    threading.Thread(target=perform_summarization).start()

# Function to update summary area with text
def update_summary_area(text):
    summary_area.config(state=tk.NORMAL)
    summary_area.delete("1.0", tk.END)
    summary_area.insert(tk.END, text)
    summary_area.config(state=tk.DISABLED)

# Summarize button
# summarize_btn = ttk.Button(side_panel, text="Summarize Text", width=20, command=summarize_text)
# summarize_btn.pack(pady=10, padx=5)

summary_btn = ttk.Button(main_frame, text="Summarize", command=summarize_text)
summary_btn.grid(row=2, column=0, columnspan=4, pady=14)


# Run the application
root.mainloop()



