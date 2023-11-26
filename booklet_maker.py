#!/usr/bin/env python3
import math
import sys
import os
from PyPDF4 import PdfFileWriter, PdfFileReader

import PySimpleGUI as sg


class Sheet(object):
    def __init__(self):
        self.front = PrintPage()
        self.back = PrintPage()


class PrintPage(object):
    def __init__(self):
        self.left = PageContainer()
        self.right = PageContainer()


class PageContainer(object):
    def __init__(self):
        self.page = None


def build_booklet(pages):
    # Double sized page, with double-sided printing, fits 4 of the original.
    sheet_count = int(math.ceil(len(pages) / 4.0))

    booklet = [Sheet() for i in range(0, sheet_count)]

    # Assign input pages to sheets

    # This is the core algo. To understand it:
    # * pick up 3 A4 sheets, landscape
    # * number the sheets from 1 to 3, starting with bottom one
    # * fold the stack in the middle to form an A5 booklet
    # * work out what order you need to use the front left,
    #   front right, back left and back right sides.

    def containers():
        # Yields parts of the booklet in the order they should be used.
        for sheet in booklet:
            yield sheet.back.right
            yield sheet.front.left

        for sheet in reversed(booklet):
            yield sheet.front.right
            yield sheet.back.left

    for c, p in zip(containers(), pages):
        c.page = p

    return booklet


def add_double_page(writer, page_size, print_page):
    width, height = page_size
    p = writer.insertBlankPage(width=width, height=height, index=writer.getNumPages())

    # Merge the left page
    l_page = print_page.left.page
    if l_page is not None:
        p.mergePage(l_page)

    # Merge the right page with translation
    r_page = print_page.right.page
    if r_page is not None:
        p.mergeTranslatedPage(r_page, width / 2, 0)


def print_instructions(sheets):
    instructions = """
Print pages %d to %d (however many copies you need).
Put them back in, rotated/flipped in order to print on the other side.
Print pages %d to %d.
""" % (1, len(sheets), len(sheets) + 1, len(sheets) * 2)
    return instructions
    print(instructions)


def make_booklet(input_name, output_name,window, blanks=0 ):
    reader = PdfFileReader(open(input_name, "rb"))
    pages = [reader.getPage(p) for p in range(0, reader.getNumPages())]
    for i in range(0, blanks):
        pages.insert(0, None)

    sheets = build_booklet(pages)

    writer = PdfFileWriter()
    p0 = reader.getPage(0)
    input_width = p0.mediaBox.getWidth()
    output_width = input_width * 2
    input_height = p0.mediaBox.getHeight()
    output_height = input_height

    page_size = (output_width, output_height)
    # We want to group fronts and backs together.
    i = 0
    for sheet in sheets:
        window['-PBAR-'].update(current_count=(i + (1/reader.getNumPages()*100)))
        add_double_page(writer, page_size, sheet.back)
        i+=1

    for sheet in sheets:
        window['-PBAR-'].update(current_count=i + (1/reader.getNumPages()*100))
        add_double_page(writer, page_size, sheet.front)
        i+=1
    writer.write(open(output_name, "wb"))
    
    return print_instructions(sheets)


USAGE = """
Converts a PDF document into a booklet form, by re-ordering pages and
combining into double sized pages suitable for double-sided printing.

Usage:

booklet_maker.py input.pdf output.pdf [blank pages to insert at start]
"""


if __name__ == '__main__':
    # All the stuff inside your window.
    layout = [  
                [sg.Text('Input pdf        '), sg.InputText(key="input_pdf"), sg.FilesBrowse()],
                [sg.Text('Output Folder'), sg.InputText(key="output_folder"), sg.FolderBrowse()],
                [sg.Text('Blanks'), sg.Input(4,key='-BLANKS-',size=5)],
                [sg.Button('Ok'), sg.Button('Cancel')],
                [sg.ProgressBar(100, orientation='h', expand_x=True, size=(20, 20),  key='-PBAR-', bar_color=("green","white"))], ]

    # Create the Window
    window = sg.Window('Booklet maker', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == 'Ok':
            inputpdf = values["input_pdf"]
            filename = os.path.split(inputpdf)[-1]
            outputfolder = values["output_folder"]
            blanks = values["-BLANKS-"]
            instructions = make_booklet(inputpdf, os.path.join(outputfolder,"booklet_"+filename),window ,int(blanks))
            sg.popup("Book successfully converted to booklet\n"+instructions)
            window['-PBAR-'].update(current_count=0)
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break
       
    window.close()
