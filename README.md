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

    Token Limit: The application can only summarize text up to 1024 tokens. If the input text exceeds this limit, the transformer model will truncate the text, which might result in an incomplete summary.
    Input Size: The input text needs to have at least 50 words to be effectively summarized.



