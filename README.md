# GPT3-pdf_summarizer
This is my first attempt to summarize large amounts of text uisng gpt3.

Just a simple tkiner app with two buttons. 
- One to allow the user to select the PDF file to be converted to text file
- One to break the text up into tokens for gpt3 once broken into tokens they are iterated over with by using a multiprocessing Pool which processes prompt request and responces from gpt3.


To use it just add your api key to the openai.api_key = "" on line 7