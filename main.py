import math
from tkinter import *
from tkinter.ttk import Combobox
from PIL import Image


def clicked():
    update_button("white", "black", "Stitching...")
    update_status("This might take a minute")
    chip_name = id_entry.get().upper()
    file_path = path_entry.get() + "/"
    x_images = int(x_size_entry.get())
    y_images = int(y_size_entry.get())
    picture_format = pic_formats.get()
    index_of_first_image = int(index_entry.get())
    generate_collage(chip_name, file_path, x_images, y_images, picture_format, index_of_first_image)
    update_button("black", "white", "Stitch")
    window.after(5000, update_status("Done!"))
    update_status("")


def update_button(bg, fg, new_text):
    btn["bg"] = bg
    btn["fg"] = fg
    btn["text"] = new_text
    btn.update()


def update_status(updated_text):
    status["text"] = updated_text
    status.update()


def generate_collage(chip_name, file_path, x_images, y_images, picture_format, index_of_first_image):
    inspection_images = [Image.open(f) for f in file_locations(x_images, y_images, file_path, index_of_first_image)]
    collage = paste_pictures(x_images, y_images, inspection_images)
    collage.save(file_path + chip_name + "." + picture_format)


def paste_pictures(x_images, y_images, inspection_images):
    collage = generate_blank_image(inspection_images[0], x_images, y_images)
    x_step = inspection_images[0].size[0]
    y_position = 0
    x_position = 0

    # Determine the starting location and direction based on th\e radio button
    # if top_left_radio is clicked, getvar() will give 1 so we start in the top left
    # if top_right_radio is clicked, top_left_radio is not clicked so getvar() will give 0
    if start_position.get() == 0:
        x_position = 0
    else:
        x_position = inspection_images[0].size[0] * (x_images - 1)
        x_step *= -1

    # paste all of the images into the collage in the correct location
    for pic in inspection_images:
        collage.paste(pic, (x_position, y_position))
        x_position += x_step
        # when the next picture would be out of bounds (too big or small), start a new row and reverse direction
        if x_position > pic.size[0] * (x_images - 1) or x_position < 0:
            x_step *= -1
            x_position += x_step
            y_position += pic.size[1]
    return collage


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
window.geometry('525x200')

fp_row = 0
file_path_lbl = Label(window, text="File Path", anchor="e")
file_path_lbl.grid(column=0, row=fp_row)

path_entry = Entry(window, width=60)
path_entry.grid(column=1, row=fp_row, columnspan=3)
path_entry.insert(END, "E:/Inspection Images")

id_row = fp_row + 1
id_lbl = Label(window, text="CMUT ID")
id_lbl.grid(column=0, row=id_row)

id_entry = Entry(window)
id_entry.grid(column=1, row=id_row)
id_entry.insert(END, "SM20B-R01-L128-H1")

xsize_row = id_row + 1
x_size_lbl = Label(window, text="Pictures in the x-direction", anchor="w")
x_size_lbl.grid(column=0, row=xsize_row)

x_size_entry = Entry(window)
x_size_entry.grid(column=1, row=xsize_row)
x_size_entry.insert(END, 27)

y_size_row = xsize_row + 1
y_size_lbl = Label(window, text="Pictures in the y-direction", anchor="w")
y_size_lbl.grid(column=0, row=y_size_row)

y_size_entry = Entry(window)
y_size_entry.grid(column=1, row=y_size_row)
y_size_entry.insert(END, 9)

first_image_row = y_size_row + 1
first_image_lbl = Label(window, text="Index of the first image")
first_image_lbl.grid(column=0, row=first_image_row)

index_entry = Entry(window)
index_entry.grid(column=1, row=first_image_row)
index_entry.insert(END, 1)

number_of_chips_row = first_image_row + 1
number_of_chips_lbl = Label(window, text="Number of CMUTs")
number_of_chips_lbl.grid(column=0, row=number_of_chips_row)

number_of_chips_entry = Entry(window)
number_of_chips_entry.grid(column=1, row=number_of_chips_row)
number_of_chips_entry.insert(END, 1)

format_row = number_of_chips_row + 1
pic_formats = Combobox(window, width=17)
pic_formats.grid(column=1, row=format_row)
pic_formats['values'] = ('png', 'jpg', 'tiff', 'bmp')
pic_formats.current(1)

formats_lbl = Label(window, text="Picture Format", anchor="w")
formats_lbl.grid(column=0, row=format_row)

position_row = format_row + 1
left_right_lbl = Label(window, text="Starting Position")
left_right_lbl.grid(column=0, row=position_row)

start_position = IntVar()
top_left_radio = Radiobutton(window, text="Top Left", variable=start_position, value=0)
top_left_radio.grid(column=1, row=position_row)

top_right_radio = Radiobutton(window, text="Top Right", variable=start_position, value=1)
top_right_radio.grid(column=3, row=position_row)

btn_row = position_row + 1
btn = Button(window, text="Stitch", bg="black", fg="white", width=20, command=clicked)
btn.grid(column=3, row=btn_row)

status_row = btn_row + 1
status = Label(window, text="")
status.grid(column=3, row=format_row)

window.mainloop()
