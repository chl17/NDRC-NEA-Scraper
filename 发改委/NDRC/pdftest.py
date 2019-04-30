import pdfminer
import subprocess
from 发改委.NDRC.pdf2txt import extract_text


def readPDF(file_paths):
    for file_path in file_paths:
        subprocess.Popen(['python', r'C:\Users\haoli\PycharmProjects\SRT\发改委\NDRC\pdf2txt.py', file_path])


if __name__ == '__main__':
    file_list = [r"C:\Users\haoli\PycharmProjects\SRT\发改委\NDRC\test_files\test.pdf"]
    readPDF(file_list)
