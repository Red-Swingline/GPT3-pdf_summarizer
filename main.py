import PyPDF2
import tkinter as tk
from tkinter import filedialog
import openai
import multiprocessing

openai.api_key = ""


def convert_pdf_to_text():
    """
    Convert a selected PDF file to text using PyPDF2 and save the text to a file.
    """
    pdf_file_path = filedialog.askopenfilename(
        title="Select a PDF file", filetypes=[("PDF Files", "*.pdf")]
    )

    with open(pdf_file_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        with open("output.txt", "w") as txt_file:
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                txt_file.write(page_text)

    tk.messagebox.showinfo(
        "Conversion Complete", "The PDF file has been converted to text!"
    )


def break_text_file_into_strings(text):
    """
    Break the text file into smaller strings of a maximum length.
    """
    max_length = 2500 * 4  # 1 token = 4 characters
    strings = []
    while text:
        if len(text) <= max_length:
            strings.append(text)
            break
        last_space = text[:max_length].rfind(" ")
        if last_space == -1:
            last_space = max_length
        string = text[:last_space]
        strings.append(string)
        text = text[last_space + 1 :]
    return strings


def summarize_text(text):
    """
    Generate a summary of the text using the OpenAI API.
    """
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Return a summary of this text \n {text}",
        temperature=0.7,
        max_tokens=250,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response["choices"][0]["text"]


def summarize_parallel(strings):
    """
    Generate summaries of the text using the OpenAI API in parallel.
    """
    with multiprocessing.Pool() as pool:
        summaries = pool.map(summarize_text, strings)
        print(summaries)
    return summaries


def summarize_document():
    """
    Generate a summary of the text using the OpenAI API.
    """
    with open("output.txt", "r") as text_file:
        text = text_file.read()
    strings = break_text_file_into_strings(text)
    summaries = summarize_parallel(strings)

    with open("summary.txt", "w") as out_file:
        for r in summaries:
            out_file.write(r)
            out_file.write("\n\n")

    tk.messagebox.showinfo("Summarization Complete", "The text has been summarized!")


if __name__ == "__main__":
    # Create a Tkinter window
    window = tk.Tk()
    window.title("PDF to Text Converter")
    window.geometry("400x100")

    # Create a "Select PDF" button
    select_pdf_button = tk.Button(
        window, text="Select PDF", command=convert_pdf_to_text
    )
    select_pdf_button.pack(pady=10)

    # Create a "Summarize" button
    summarize_button = tk.Button(window, text="Summarize", command=summarize_document)
    summarize_button.pack(pady=10)

    window.mainloop()
