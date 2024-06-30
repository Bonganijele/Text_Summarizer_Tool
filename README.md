# Text_Summarizer_Tool
# version 1.0


Text Summarizer Tool

This Python application is a text summarizer tool that leverages the pipeline from the Hugging Face Transformers library to generate concise summaries of longer texts.
Features

    User-Friendly Interface: The tool provides an intuitive GUI using Tkinter, making it easy for users to load text files, view summaries, and save results.
    Model Selection: Users can choose between different pre-trained models such as t5-small and facebook/bart-large-cnn for summarization.
    Character Count: The application displays the character count of the input text to help users understand the size of their content.
    Language Detection: Automatically detects the language of the input text.
    Customizable Summary Length: Users can adjust the length of the summary through a slider, with a maximum limit of 1024 tokens.
    Keyword Highlighting: The tool extracts and highlights keywords in the summarized text for better readability and emphasis.

    Limitations

    Token Limit: The application can only summarize text up to 1024 tokens. If the input text exceeds this limit, 
    the transformer model will truncate the text, which might result in an incomplete summary.
    
    Input Size: The input text needs to have at least 50 words to be effectively summarized.



Installation:

$ git clone https://github.com/yourusername/text-summarizer-tool.git
$ cd text-summarizer-tool

Create a virtual environment (optional but recommended):

$ python -m venv env
$ source env/bin/activate   # On Windows, use `env\Scripts\activate`

Install the required packages:

$ pip install -r requirements.txt

USAGE:

1 Run the application:

$ python3 text_summary_tool.py


2 Load a text file: Use the 'Load file' button to open a text file containing the text you want to summarize.

3 Select a model: Choose a pre-trained summarization model from the dropdown menu.

4 Adjust summary length: Use the slider to set the desired length of the summary as a percentage of the original text.

5 Summarize text: Click the 'Summarize' button to generate a summary of the loaded text.

6 Save the summary: Use the 'Save Summary' button to save the generated summary to a text file.

Keyboard Shortcuts:

    Ctrl+O: Open a text file
    Ctrl+S: Save the summary
    Ctrl+A: Show the 'About' window
    Ctrl+K: View keyboard shortcuts
    Ctrl+F: Open the feedback dialog

    Feedback and Support:

If you encounter any issues or have suggestions for improvements, please feel free to open an issue on the GitHub repository.

Contributing

We welcome contributions to this project! Please fork the repository and submit a pull request with your changes. Ensure that your code follows the existing style and includes appropriate tests.
