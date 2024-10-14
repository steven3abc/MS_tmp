import sys
from tika import parser
import tika
import glob
from datetime import datetime
from pdfminer.high_level import extract_text
import csv
import numpy as np
import matplotlib.pyplot as plt

# Function to extract text from PDF using pdfminer
def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)

#tika.initVM()
max_length = 4000
sys.path.append("..")

pdf_dir = 'Research/starwberry_file-main/pdf_en'

file_names = glob.glob(pdf_dir + "/*.pdf")

texts = []

current_date = datetime.now()
date_string = current_date.strftime("%Y%m%d")

file = open(str(max_length) + '/paragraph' + date_string + '_' + str(max_length) + '.csv', mode='w', newline='')
writer = csv.writer(file)
writer.writerow(["text", "metadata"])

g = open(str(max_length) + '/too_long' + date_string + '_' + str(max_length) + '.csv', mode='w', newline='')
too_long_writer = csv.writer(g)
too_long_writer.writerow(["text", "metadata"])

h = open(str(max_length) + '/too_short' + date_string + '_' + str(max_length) + '.csv', mode='w', newline='')
too_short_writer = csv.writer(h)
too_short_writer.writerow(["text", "metadata"])

length = []
wrong_file = []
with open('paragraph' + date_string + '.txt', 'w') as fw:
    for file_name in file_names:
        print(file_name)
        text = parser.from_file(file_name)
        #pdf_str = extract_text_from_pdf(file_name)
        pdf_str = text["content"]
        new_str = ""
        for i in range(len(pdf_str)):
            if pdf_str[i] == '-' and pdf_str[i+1] == '\n':
                continue
            if pdf_str[i] != '\n':
                new_str = new_str + pdf_str[i]
                continue
            if i == 0:
                continue
            if pdf_str[i-1] == '.':
                first_letter = str(new_str.split(' ')[-1][0])
                if not first_letter.isupper():
                    new_str = new_str + pdf_str[i]
                continue
        new_list = new_str.split('\n')
        for split_str in new_list:
            texts.append(split_str)    
            if len(split_str) <= max_length and len(split_str) > 15:
                writer.writerow([split_str, file_name.split('\\')[-1]]) 
            elif len(split_str) > max_length:    
                too_long_writer.writerow([split_str, file_name.split('\\')[-1]])
                wrong_file.append(file_name.split('\\')[-1])
                print(file_name.split('\\')[-1], 'may have some wrong')
            else:
                too_short_writer.writerow([split_str, file_name.split('\\')[-1]])
                wrong_file.append(file_name.split('\\')[-1])
                print(file_name.split('\\')[-1], 'may have some wrong')
        
        for text in texts:
            # Writing the data row by row            
            length.append(len(text))
            fw.write(text)
            fw.write('\n')
        texts.clear()
    
    length = np.array(length)
    print(length.max(), np.argmax(length) )
    print()
    
    wrong_file = list(set(wrong_file))
    
    wrong = open(str(max_length) + '_wrong.txt', 'w')
    for i in range(len(wrong_file)):
        print(wrong_file[i])
        wrong.write(wrong_file[i])
        wrong.write('\n')
        
wrong.close()
file.close()
g.close()
h.close()

plt.hist(length, bins=100, edgecolor='black')
plt.show()