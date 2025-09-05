import gradio as gr
from pathlib import Path
filepath= gr.File()
output = gr.Textbox()
def upload(filepath):
    filename = Path(filepath)
    list1 = ['.txt','.csv']
    if filename.suffix.lower() in list1:
        with open(filepath, 'r') as file:
            contents = file.read()
        return(contents)
    else:
        print('Only ".txt" and ".csv" file are allowed.')


gr.Interface(upload, filepath, output).launch()
