from PyPDF2 import PdfFileReader
pdf = open('<-------PDF Path---------->','rb')

pdf_reader = PdfFileReader(pdf)
pdf_reader.numPages
page = pdf_reader.getPage(18)

print(page.extractText())