import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext, filedialog, messagebox

# Function to load text from file

def load_txt_file(text_area):
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt",), ("Word Documents", "*.doc")])
    if file_path:
        with open(file_path, "r", encoding='utf-8') as file:
            text = file.read()
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.END, text)


# import nltk
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
# from nltk.probability import FreqDist

# # Sample text for demonstration
# text = "Natural Language Processing (NLP) is a subfield of artificial intelligence and linguistics concerned with the interactions between computers and human language."

# # Tokenize the text into words
# words = word_tokenize(text)

# # Remove stopwords
# stop_words = set(stopwords.words('english'))
# filtered_words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]

# # Calculate frequency distribution
# freq_dist = FreqDist(filtered_words)

# # Get the 5 most common keywords
# top_keywords = freq_dist.most_common(5)

# # Extract keywords from the frequency distribution
# keywords = [word for word, freq in top_keywords]

# print("Keywords:", keywords)
