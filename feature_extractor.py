#!/usr/bin/python3

import os
import pandas as pd
from subprocess import Popen, PIPE
import re

def run_pdfid(pdf_path):
    cmd = f"./pdfid.py {pdf_path}"
    try:
        stdout = Popen(cmd, shell=True, stdout=PIPE).stdout
        output = stdout.readlines()
        output = [item.decode('utf-8').strip() for item in output]
        return output
    except Exception as e:
        print(f"An error occurred: {e}")

def feature_extraction(output):
    obj = []
    endobj = []
    stream = []
    endstream = []
    xref = []
    trailer = []
    startxref = []
    Page = []
    Encrypt = []
    ObjStm = []
    JS = []
    Javascript = []
    AA = []
    OpenAction = []
    AcroForm = []
    JBIG2Decode = []
    RichMedia = []
    Launch = []
    EmbeddedFile = []
    XFA = []
    Colors = []
    Malicious = []

    obj.append(int(re.search(r'\d+', output[2]).group()))
    endobj.append(int(re.search(r'\d+', output[3]).group()))
    stream.append(int(re.search(r'\d+', output[4]).group()))
    endstream.append(int(re.search(r'\d+', output[5]).group()))
    xref.append(int(re.search(r'\d+', output[6]).group()))
    trailer.append(int(re.search(r'\d+', output[7]).group()))
    startxref.append(int(re.search(r'\d+', output[8]).group()))
    Page.append(int(re.search(r'\d+', output[9]).group()))
    Encrypt.append(int(re.search(r'\d+', output[10]).group()))
    ObjStm.append(int(re.search(r'\d+', output[11]).group()))
    JS.append(int(re.search(r'\d+', output[12]).group()))
    Javascript.append(int(re.search(r'\d+', output[13]).group()))
    AA.append(int(re.search(r'\d+', output[14]).group()))
    OpenAction.append(int(re.search(r'\d+', output[15]).group()))
    AcroForm.append(int(re.search(r'\d+', output[16]).group()))
    JBIG2Decode.append(int(output[17].split()[-1]))
    RichMedia.append(int(re.search(r'\d+', output[18]).group()))
    Launch.append(int(re.search(r'\d+', output[19]).group()))
    EmbeddedFile.append(int(re.search(r'\d+', output[20]).group()))
    XFA.append(int(re.search(r'\d+', output[21]).group()))
    Colors.append(int(output[22].split()[-1]))
    Malicious.append(False)

    df = pd.DataFrame({
        'obj': obj,
        'endobj': endobj,
        'stream': stream,
        'endstream': endstream,
        'xref': xref,
        'trailer': trailer,
        'startxref': startxref,
        'Page': Page,
        'Encrypt': Encrypt,
        'ObjStm': ObjStm,
        'JS': JS,
        'Javascript': Javascript,
        'AA': AA,
        'OpenAction': OpenAction,
        'AcroForm': AcroForm,
        'JBIG2Decode': JBIG2Decode,
        'RichMedia': RichMedia,
        'Launch': Launch,
        'EmbeddedFile': EmbeddedFile,
        'XFA': XFA,
        'Colors': Colors,
        'Malicious': Malicious
    })
    return df.iloc[0].values

def process_folder(folder_path, malicious=False):
    data = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            output = run_pdfid(pdf_path)
            if output:
                features = feature_extraction(output)
                features[-1] = malicious
                data.append(features)

    df = pd.DataFrame(data, columns=['obj', 'endobj', 'stream', 'endstream', 'xref', 'trailer', 'startxref', 'Page',
                                     'Encrypt', 'ObjStm', 'JS', 'Javascript', 'AA', 'OpenAction', 'AcroForm',
                                     'JBIG2Decode', 'RichMedia', 'Launch', 'EmbeddedFile', 'XFA', 'Colors', 'Malicious'])
    return df

# Process clean PDFs
clean_df = process_folder('./cleanpdfs', malicious=False)
clean_df.to_csv('cleanpdfs_features.csv', index=False)

# Process malicious PDFs
malicious_df = process_folder('./malpdfs', malicious=True)
malicious_df.to_csv('malpdfs_features.csv', index=False)


