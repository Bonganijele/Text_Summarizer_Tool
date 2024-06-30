import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
# from tkinter import scrolledtext, filedialog, messagebox

def save_txt_file(summary_area):
    summary = summary_area.get("1.0", tk.END).strip()
    if not summary:
        messagebox.showerror("Error", "No summary to save.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("Word Documents", "*.doc")]
    )
    
    if file_path:
        # Ensure the file path has the correct extension
        if not file_path.endswith(('.txt', '.doc')):
            messagebox.showerror("Error", "Invalid file type selected.")
            return
        
        if file_path.endswith(".txt"):
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(summary)
                messagebox.showinfo("Success", "Summary saved successfully as a .txt file")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while saving the file: {e}")
        elif file_path.endswith(".doc"):
            try:
                import docx
                doc = docx.Document()
                doc.add_paragraph(summary)
                doc.save(file_path)
                messagebox.showinfo("Success", "Summary saved successfully as a .doc file")
            except ImportError:
                messagebox.showerror("Error", "docx module is not installed. Please install it to save as .doc files.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while saving the file: {e}")
