import fitz
import datetime
import traceback
import os
from PIL import Image
from PyPDF2 import PdfMerger


version = "0.0.2"
last_update = datetime.date.fromisoformat("2023-03-03")
debugMode = False


def set_debugMode(mode: bool = False):
  """This function sets the debugMode to True or False.
  
     Args:
         mode(bool): debugMode (default False).
  
      Returns:
          nothing:
  """
  global debugMode
  if mode == True:
    debugMode = mode
  else:
    debugMode = False


def info():
  """This function provides information about the entire library."""
  print("""
  \033[32mPDFLib2 by Rosario Moscato (rosario.moscato@outlook.com)\033[0m
  PDFLib2 version: {} 
  Relies on PyMuPDF >= 1.21.1 and PyPDF2 >= 3.0.1 
  Last Update: {}
  License: MIT""".format(version, last_update))


def is_encrypted(pdf_file):
  """This function checks if a pdf file is encrypted.
  
      Args:
          pdf_file(str): pdf file name (with path if needed).
  
      Returns:
          (bool): True if pdf file is encrypted
  """
  try:
    pdf=fitz.Document(pdf_file)
    return pdf.is_encrypted
  except Exception:
    print("ERROR: Unable to load pdf file")
    if debugMode:
      print(traceback.format_exc())


def get_uncrypted(pdf_file, password: str):
  """This function decrypts a pdf file.
  
      Args:
          pdf_file(str): pdf file name (with path if needed).
          password(str): pdf file's password.
  
      Returns:
          nothing: this function creates an uncrypted pdf file.
  """
  try:
    if is_encrypted(pdf_file):
      pdf=fitz.open(pdf_file)
      if pdf.authenticate(password):
        filename = os.path.splitext(pdf_file)[0]
        output_filename = f"{filename}_uncrypted.pdf"
        pdf.save(output_filename)
      pdf.close()
  except Exception:
    print("ERROR: Unable to load pdf file")
    if debugMode:
      print(traceback.format_exc())


def get_encrypted(pdf_file, password: str):
  """This function encrypts a pdf file.
  
      Args:
          pdf_file(str): pdf file name (with path if needed).
          password(str): pdf file's password.
  
      Returns:
          nothing: this function creates an encrypted pdf file.
  """
  try:
    if is_encrypted(pdf_file) == False:
      pdf=fitz.open(pdf_file)
      perm = int(
        fitz.PDF_PERM_ACCESSIBILITY # always use this
        | fitz.PDF_PERM_PRINT # permit printing
        | fitz.PDF_PERM_COPY # permit copying
        | fitz.PDF_PERM_ANNOTATE # permit annotating
      )
      encrypt_meth = fitz.PDF_ENCRYPT_AES_256
      filename = os.path.splitext(pdf_file)[0]
      output_filename = f"{filename}_encrypted.pdf"
      pdf.save(output_filename, encryption=encrypt_meth, user_pw=password, permissions=perm)
      pdf.close()
  except Exception:
    print("ERROR: Unable to load pdf file")
    if debugMode:
      print(traceback.format_exc())


def get_metadata(pdf_file):
  """This function gets all metadata from a pdf file.
     It's possible to print them one by one with [author], [title], etc.
  
      Args:
          pdf_file(str): pdf file name (with path if needed).
  
      Returns:
          metadata(dict): dictionay of pdf metadata (author, title, etc.)
  """
  try:
    pdf=fitz.open(pdf_file)
    metadata = pdf.metadata
    pdf.close()
    return metadata
  except Exception:
    print("ERROR: Unable to load pdf file")
    if debugMode:
      print(traceback.format_exc())


def get_pagecount(pdf_file):
  """This function gets the number of pages a pdf file.
     It's possible to print them one by one with [author], [title], etc.
  
      Args:
          pdf_file(str): pdf file name (with path if needed).
  
      Returns:
          pages(int): document's number of pages.
  """
  try:
    pdf=fitz.open(pdf_file)
    pages = pdf.page_count
    pdf.close()
    return pages
  except Exception:
    print("ERROR: Unable to load pdf file")
    if debugMode:
      print(traceback.format_exc())


def get_toc(pdf_file):
  """This function gets the table of contents of a pdf file.
     It's possible to print them one by one with [author], [title], etc.
  
      Args:
          pdf_file(str): pdf file name (with path if needed).
  
      Returns:
          toc(int): list of lists containing [chapter, title, page].
  """
  try:
    pdf=fitz.open(pdf_file)
    toc = pdf.get_toc()
    pdf.close()
    return toc
  except Exception:
    print("ERROR: Unable to load pdf file")
    if debugMode:
      print(traceback.format_exc())


def get_text(pdf_file):
  """This function extracts all the text from a pdf file.
  
     Args:
         pdf_file(str): pdf file name (with path if needed).
  
     Returns:
         text(str): all text contained in the pdf file.
  """
  try:
    pdf=fitz.open(pdf_file)
    result = []
    for i in range (0, pdf.page_count):
        page = pdf.load_page(i)
        text = page.get_text('text')
        result.append(text.replace('\t',' '))
    pdf.close()  
    return ' '.join(result)
  except Exception:
    print("ERROR: Unable to load pdf file")
    if debugMode:
      print(traceback.format_exc())


def get_fromto(pdf_file, start_page: int = 1, stop_page: int = 1):
  """This function puts all the pages from selected starting and ending page
     into a unique new pdf file.
     
     Args:
         pdf_file(str): pdf file name (with path if needed).
         start_page(int): starting page of the splitting.
         stop_page(int): ending page of the splitting.
  
     Returns:
         nothing: this function creates a pdf file from starting to ending page.      
  """
  try:
    pdf=fitz.open(pdf_file)
    pdf2=fitz.open()
    pdf2.insert_pdf(pdf, from_page = start_page-1, to_page = stop_page-1)
    filename = os.path.splitext(pdf_file)[0]
    output_filename = f"{filename}_from_{start_page}_to_{stop_page}.pdf"
    pdf2.save(output_filename)
    pdf.close()
    pdf2.close()
  except Exception:
    print("ERROR: pls check your arguments")
    if debugMode:
      print(traceback.format_exc())


def get_lastpage(pdf_file):
  """This function gets the last page of a pdf file.
  
     Args:
         pdf_file(str): pdf file name (with path if needed).
  
     Returns:
         nothing: this function creates a pdf containing only last page of original document.  
  """
  try:
    pdf=fitz.open(pdf_file)
    pdf2=fitz.open()
    pdf2.insert_pdf(pdf, from_page = pdf.page_count-1, to_page = pdf.page_count-1)
    filename = os.path.splitext(pdf_file)[0]
    output_filename = f"{filename}_last_page.pdf"
    pdf2.save(output_filename)
    pdf.close()
    pdf2.close()
  except Exception:
    print("ERROR: pls check your arguments")
    if debugMode:
      print(traceback.format_exc())


def pdf2img(pdf_file, start_page: int = 1, stop_page: int = 1):
  """This function converts a pdf into jpg files.
  
     Args:
         pdf_file(str): pdf file name (with path if needed).
         start_page(int): first page to be converted.
         stop_page(int): last page to be converted.  
  
     Returns:
         nothing: this function creates as many png file as many pages of the pdf file.  
  """
  try:
    pdf=fitz.open(pdf_file)
    for i in range (start_page-1, stop_page):
        page = pdf.load_page(i)
        pix = page.get_pixmap()
        filename = os.path.splitext(pdf_file)[0]
        output_filename = f"{filename}_{i+1}.jpg"
        pix.save(output_filename)
    pdf.close()    
  except Exception:
    print("ERROR: Unable to load image file")
    if debugMode:
      print(traceback.format_exc())


def img2pdf(image_file):
  """This function converts an image into a pdf file.
  
     Args:
         image_file(str): image file name (with path if needed).
  
     Returns:
         nothing: this function creates a pdf file of the specified image.  
  """
  try:
    img = Image.open(image_file)
    img = img.convert("RGB")
    filename = f"{os.path.splitext(image_file)[0]}.pdf"
    img.save(filename)
  except Exception:
    print("ERROR: Unable to load image file")
    if debugMode:
      print(traceback.format_exc())


def get_rotated(pdf_file, start_page: int = 1, stop_page: int = 1, rotation: int = 90):
  """This function rotate specific pages of a pdf file with a specific angle.
  
     Args:
         pdf_file(str): pdf file name (with path if needed).
         start_page(int): first page to be rotated.
         stop_page(int): last page to be rotated.
         rotation(int): degrees of rotation.
  
     Returns:
         nothing: this function creates a pdf file with the selected page rotated.     
  """
  try:
    pdf = fitz.open(pdf_file)
    pdf2 = fitz.open()
    pdf2.insert_pdf(pdf, from_page = start_page-1, to_page = stop_page-1, rotate=rotation)
    filename = os.path.splitext(pdf_file)[0]
    output_filename = f"{filename}_{start_page}_{stop_page}_{rotation}.pdf"
    pdf2.save(output_filename)
    pdf.close()
    pdf2.close()
  except Exception:
    print("ERROR: pls check your arguments")
    if debugMode:
      print(traceback.format_exc())


def get_individual_pages(pdf_file):
  """This function splits a pdf file into many different files,
      each of them from a single page.
      
     Args:
         pdf_file(str): pdf file name (with path if needed).
  
     Returns:
         nothing: this function creates a different pdf file for each starting page.    
      
  """
  try:
    pdf=fitz.open(pdf_file)
    num_pages = pdf.page_count
    for i in range(0,num_pages):
      pdf2=fitz.open()
      pdf2.insert_pdf(pdf, from_page = i, to_page = i)
      filename = os.path.splitext(pdf_file)[0]
      output_filename = f"{filename}_{i+1}.pdf"
      pdf2.save(output_filename)
      pdf2.close()
    pdf.close()
  except Exception:
    print("ERROR: Unable to load pdf file")
    if debugMode:
      print(traceback.format_exc())


def pdf_files_collector(parent_folder: str):
  """This function gets all pdf files in a defined folder.
  
     Args:
         parent_folder(str): folder name (with path if needed).
  
     Returns:
         target_files(list): a list of all pdf files in the specified folder.
  """
  try:
    target_files = []
    for path, subdirs, files in os.walk(parent_folder):
      for name in files:
        if name.endswith(".pdf"):
          target_files.append(os.path.join(path, name))
    return target_files
  except Exception:
    print("ERROR: pls check your arguments")
    if debugMode:
      print(traceback.format_exc())


def pdf_list_merger(pdfs_list, output_filename = "merged_file.pdf"):
  """This function merges all pdf files from a list into a unique final pfd file.
  
     Args:
         pdfs_list(list): a list of pdf files to be merged.
         output_filename(str): the name of the output file (default="merged_file.pdf").
  
     Returns:
         nothing: this function merges all the starting files into a unique final pdf.  
  """
  try:
    merger = PdfMerger()
    with open(output_filename, 'wb') as f:
      for file in pdfs_list:
        merger.append(file)
      merger.write(f)
  except Exception:
    print("ERROR: pls check your arguments")
    if debugMode:
      print(traceback.format_exc())


def pdf_folder_merger(parent_folder, output_filename = "merged_file.pdf"):
  """This function merges all pdf files contained in a folder into a unique final pfd file.
  
     Args:
         parent_folder(str): folder name (with path if needed).
         output_filename(str): the name of the output file (default="merged_file.pdf").
  
     Returns:
         nothing: this function merges all the starting files into a unique final pdf.  
  """
  try:
    pdfs_list = pdf_files_collector(parent_folder)
    merger = PdfMerger()
    with open(output_filename, 'wb') as f:
      for file in pdfs_list:
        merger.append(file)
      merger.write(f)
  except Exception:
    print("ERROR: pls check your arguments")
    if debugMode:
      print(traceback.format_exc())   


def get_watermarked(pdf_file, img_file):
  """This function adds a watermark to a pdf file.
  
     Args:
         pdf_file(str): pdf file name (with path if needed).
         img_file(str): image file to be used as watermark.
  
     Returns:
         nothing: this function adds a watermark to the original pdf.  
  """
  try:
    pdf=fitz.open(pdf_file)
    coords = (220, 220, 400, 400) 
    for i in range (0, pdf.page_count):
      page = pdf.load_page(i)
      page.insert_image(coords,filename=img_file, rotate=90, overlay=False)
    filename = os.path.splitext(pdf_file)[0]
    output_filename = f"{filename}_watermarked.pdf"
    pdf.save(output_filename)
    pdf.close()  
  except Exception:
    print("ERROR: Unable to load pdf file")
    if debugMode:
      print(traceback.format_exc())


def get_images(pdf_file):
  """This function gets all images from a pdf file.
  
     Args:
         pdf_file(str): pdf file name (with path if needed).
  
     Returns:
         nothing: this function creates a sigle file for each image in the original pdf.  
  """
  try:
    pdf=fitz.open(pdf_file)
    for i in range (0, pdf.page_count):
      image_list = pdf.get_page_images(i)
      for im in image_list:
        print(f"Width: {im[2]}, Height: {im[3]}, Name: {im[7]}")
        xref = im[0]
        pix = fitz.Pixmap(pdf,xref)
        if pix.n < 5:
          pix.save(f'{xref}.png')
        else:
          pix1 = fitz.open(fitz.csRGB,pix)
          pix1.save(f'{xref}.png')
          pix1=None
        pix=None
    pdf.close()  
  except Exception:
    print("ERROR: Unable to load pdf file")
    if debugMode:
      print(traceback.format_exc())

