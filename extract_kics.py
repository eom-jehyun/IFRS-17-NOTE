# -*- coding: utf-8 -*-
import fitz
import os

SRC = r"C:\Users\엄제현\Desktop\최신보험수리학\新지급여력제도(K-ICS) 해설서.pdf"
OUT_DIR = r"C:\Users\엄제현\Desktop\ifrs17-site-web\images\kics"
os.makedirs(OUT_DIR, exist_ok=True)

doc = fitz.open(SRC)
mat = fitz.Matrix(2.0, 2.0)
for i in range(len(doc)):
    out_path = os.path.join(OUT_DIR, f"{i:04d}.jpg")
    if os.path.exists(out_path):
        continue
    pix = doc[i].get_pixmap(matrix=mat)
    pix.save(out_path, jpg_quality=82)
print(f"done: {len(doc)} pages")
