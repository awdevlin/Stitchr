import math
from tkinter import *
from tkinter.ttk import Combobox
from PIL import Image


def clicked():
    status = Label(text="Stitching...")
    status.grid(column=2, row=btn_row)
    status.update()
    chip_name = id_entry.get()
    file_path = path_entry.get() + "/"
    x_images = int(x_size_entry.get())
    y_images = int(y_size_entry.get())
    picture_format = pic_formats.get()
    index_of_first_image = int(index_entry.get())
    generate_collage(chip_name, file_path, x_images, y_images, picture_format, index_of_first_image)
    status["text"] = "Done!"


def generate_collage(chip_name, file_path, x_images, y_images, picture_format, index_of_first_image):
    inspection_images = [Image.open(f) for f in file_locations(x_images, y_images, file_path, index_of_first_image)]
    collage = generate_blank_image(inspection_images[0], x_images, y_images)

    x_position = 0
    y_position = 0
    x_step = inspection_images[0].size[0]

    # paste all of the images into the collage in the correct location
    for pic in inspection_images:
        collage.paste(pic, (x_position, y_position))
        x_position += x_step
        # when the next picture would be out of bounds (too big or small), start a new row and reverse direction
        if x_position > pic.size[0] * (x_images - 1) or x_position < 0:
            x_step *= -1
            x_position += x_step
            y_position += pic.size[1]

    collage.save(file_path + chip_name + "." + picture_format)


def file_locations(x_images, y_images, file_path, index_of_first_image):
    image_name_list = []
    number_of_images = x_images * y_images

    for i in range(number_of_images):
        image_id = file_path

        # add leading zeroes to the file name that were assigned by the image captures software
        for j in range(3 - int(math.log(i + index_of_first_image) / math.log(10))):
            image_id = image_id + "0"

        image_name_list.append(image_id + str(i + index_of_first_image) + ".png")
    return image_name_list


def generate_blank_image(first_image, x_images, y_images):
    # create a blank image with the proper dimensions
    width, height = first_image.size
    total_width = width * x_images
    total_height = height * y_images
    return Image.new('RGB', (total_width, total_height))


window = Tk()
window.title("Stitchr")
window.geometry('525x175')

fp_row = 0
file_path_lbl = Label(window, text="File Path", anchor="e")
file_path_lbl.grid(column=0, row=fp_row)

path_entry = Entry(window, width=60)
path_entry.grid(column=1, row=fp_row, columnspan=3)
path_entry.insert(END, "C:/Users/Sonus User/Documents/ToupView/")

id_row = fp_row + 1
id_lbl = Label(window, text="CMUT ID")
id_lbl.grid(column=0, row=id_row)

id_entry = Entry(window)
id_entry.grid(column=1, row=id_row)
id_entry.insert(END, "SM21A-R07-L128-H1")

xsize_row = id_row + 1
x_size_lbl = Label(window, text="Pictures in the x-direction", anchor="w")
x_size_lbl.grid(column=0, row=xsize_row)

x_size_entry = Entry(window)
x_size_entry.grid(column=1, row=xsize_row)
x_size_entry.insert(END, 7)

ysize_row = xsize_row + 1
y_size_lbl = Label(window, text="Pictures in the y-direction", anchor="w")
y_size_lbl.grid(column=0, row=ysize_row)

y_size_entry = Entry(window)
y_size_entry.grid(column=1, row=ysize_row)
y_size_entry.insert(END, 36)

y_size_row = ysize_row + 1
first_image_lbl = Label(window, text="Index of the first image")
first_image_lbl.grid(column=0, row=y_size_row)

index_entry = Entry(window)
index_entry.grid(column=1, row=y_size_row)
index_entry.insert(END, 1)

format_row = y_size_row + 1
pic_formats = Combobox(window, width=17)
pic_formats.grid(column=1, row=format_row)
pic_formats['values'] = ('png', 'jpg', 'tiff', 'bmp')
pic_formats.current(0)

formats_lbl = Label(window, text="Picture Format", anchor="w")
formats_lbl.grid(column=0, row=format_row)

btn_row = format_row + 1
btn = Button(window, text="Stitch", bg="black", fg="white", width=20, command=clicked)
btn.grid(column=3, row=btn_row)

window.mainloop()
