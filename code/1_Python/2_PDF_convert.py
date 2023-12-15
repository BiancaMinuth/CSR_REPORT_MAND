# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 14:22:02 2022

@author: bianca
"""


# pip install pdfplumber

import pip
import pdfplumber
import os
import re

class Pdf_Convertor():
    def __init__(self):
        pass

    def test_function(self, name):
        self.pdf2txt(f"{name}.pdf")
        if os.path.isfile(f"{name}.txt"):
           with open(f"{name}.txt", "r", encoding="utf-8") as f:
               content = f.read()
           with open(f"{name}(Erwartung).txt", "r", encoding="utf-8") as f:
               test_text = f.read()        
           if test_text == content:
                return True
           else:
                return False
        else:
            return False

    def prepare_path(self, path):
        if path:
            if os.path.isfile(path):
                name, extention = os.path.splitext(path)
                try:
                    if re.match("\.pdf", extention, re.IGNORECASE):
                        return name
                    else:
                        print("The selected file is not a pdf! Error Code 01")
                except Exception:
                    print("Internal Error: Error Code 02")
            else:
                print(f' The file "{path}" cannot be found! Error Code 03')
        else:
            print("No input file found. Error Code 04")

            
    def pdf2txt(self, path):
        name = self.prepare_path(path)
        if name:
            with pdfplumber.open(path) as pdf:
                seiten = pdf.pages
                if os.path.exists(f"{name}.txt"):
                    #antwort = input(f"Die Datei {name}.txt exsistiert schon. Soll sie überschrieben werden? J/N ")
                    antwort = "j"
                    if antwort == "j" or "J":
                        with open(f"{name}.txt", "w", encoding="utf-8") as f:
                            f.write("")
                    else:
                        name = f"{name}(1)"
                for seite in seiten:
                    text = seite.extract_text()
                    with open(f"{name}.txt", "a", encoding="utf-8") as f:
                        f.write(text)
                        f.write("\n")
    
    def convert(self, path):
        test = self.test_function("TestDatei")
        if test:
            self.pdf2txt(path)
        else:
            print("Internal error. Error Code 05")

def main():
    # Als Beispiel
    path = ("./A_PDF_convert_Python/data_S&P500/")
    
    filenames = os.listdir(path)
    
    for filename in filenames:
        file = Pdf_Convertor()
        # convert only the files that are PDF, otherwise continue with next
        try: 
            file.convert(path+filename)
        except:
            # continue with next 
            with open("Not_pfd_files_2.txt", "a") as myfile:
               myfile.write(filename + "\n")
            continue



if __name__ == "__main__":
    main()