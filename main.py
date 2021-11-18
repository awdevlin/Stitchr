import tkinter
from tkinter import *
from tkinter.ttk import Combobox
from PIL import Image


def clicked():
    update_button("white", "black", "Stitching...")
    generate_collage()
    update_next_index()
    update_button("black", "white", "Stitch")


def update_next_index():
    x_images = int(x_size_entry.get())
    y_images = int(y_size_entry.get())
    total_images = x_images * (y_images - 1)
    next_index["text"] = total_images + int(index_entry.get())


def update_button(bg, fg, new_text):
    btn["bg"] = bg
    btn["fg"] = fg
    btn["text"] = new_text
    btn.update()


def generate_collage():
    x_images = int(x_size_entry.get())
    y_images = int(y_size_entry.get())
    chip_name = id_entry.get().upper()
    file_path = path_entry.get() + "/"
    picture_format = pic_formats.get()
    index_of_first_image = int(index_entry.get())

    inspection_images = [Image.open(f) for f in file_locations(x_images, y_images, file_path, index_of_first_image)]
    collage = paste_pictures(x_images, y_images, inspection_images)
    collage.save(file_path + chip_name + "." + picture_format)


def paste_pictures(x_images, y_images, inspection_images):
    # Pastes the pictures next to each other, one by one, in a serpentine pattern

    collage = generate_blank_image(inspection_images[0], x_images, y_images)
    x_step, y_step = inspection_images[0].size
    x_position = 0
    y_position = 0

    # Determine the starting location and direction based on the radio button
    # by default, top_left_radio is clicked, start_position gives 0, and we start in the top left
    # If the radio button is changed to top_right_radio, start position will give 1, and we start in the top right
    if start_position.get() == 1:
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
            y_position += y_step
    return collage


def file_locations(x_images, y_images, file_path, index_of_first_image):
    # Create a list of file names which point to the names of the batch of images

    image_name_list = []
    number_of_images = x_images * y_images

    for i in range(number_of_images):
        image_id = file_path

        # add leading zeroes to the file name that were assigned by the image captures software
        if i + index_of_first_image < 10:
            image_id = image_id + "0"
        if i + index_of_first_image < 100:
            image_id = image_id + "0"
        if i + index_of_first_image < 1000:
            image_id = image_id + "0"

        image_name_list.append(image_id + str(i + index_of_first_image) + ".png")
    return image_name_list


def generate_blank_image(first_image, x_images, y_images):
    # create a blank image with the proper dimensions

    width, height = first_image.size
    total_width = width * x_images
    total_height = height * y_images
    return Image.new('RGB', (total_width, total_height))


# GUI for inputting information about images and starting the stitching of the collage
window = Tk()
window.title("Stitchr")
window.geometry('450x225')

fp_row = 0
file_path_lbl = Label(window, text="File Path")
file_path_lbl.grid(column=0, row=fp_row, sticky="E")

path_entry = Entry(window, width=50)
path_entry.grid(column=1, row=fp_row, columnspan=3)
path_entry.insert(END, "E:/Raw Images/")

id_row = fp_row + 1
id_lbl = Label(window, text="CMUT ID")
id_lbl.grid(column=0, row=id_row, sticky="E")

id_entry = Entry(window)
id_entry.grid(column=1, row=id_row, sticky="W")
id_entry.insert(END, "SM21A-R09-L128H1")

x_size_row = id_row + 1
x_size_lbl = Label(window, text="Pictures in the x-direction", anchor="w")
x_size_lbl.grid(column=0, row=x_size_row, sticky="E")

x_size_entry = Entry(window)
x_size_entry.grid(column=1, row=x_size_row, sticky="W")
x_size_entry.insert(END, 26)

y_size_row = x_size_row + 1
y_size_lbl = Label(window, text="Pictures in the y-direction")
y_size_lbl.grid(column=0, row=y_size_row, sticky="E")

y_size_entry = Entry(window)
y_size_entry.grid(column=1, row=y_size_row, sticky="W")
y_size_entry.insert(END, 9)

first_image_row = y_size_row + 1
first_image_lbl = Label(window, text="Index of the first image")
first_image_lbl.grid(column=0, row=first_image_row, sticky="E")

index_entry = Entry(window)
index_entry.grid(column=1, row=first_image_row, sticky="W")
index_entry.insert(END, 1)

next_index_row = first_image_row + 1
next_index_lbl = Label(window, text="Index of next CMUT")
next_index_lbl.grid(column=0, row=next_index_row, sticky="E")

next_index = Label(window, text="")
next_index.grid(column=1, row=next_index_row, sticky="W")

format_row = next_index_row + 1
formats_lbl = Label(window, text="Picture Format")
formats_lbl.grid(column=0, row=format_row, sticky="E")

pic_formats = Combobox(window, width=4)
pic_formats.grid(column=1, row=format_row, sticky="W")
pic_formats['values'] = ('png', 'jpg', 'tiff', 'bmp')
pic_formats.current(1)

position_row = format_row + 1
left_right_lbl = Label(window, text="Starting Position")
left_right_lbl.grid(column=0, row=position_row, sticky="E")

start_position = IntVar()
top_left_radio = Radiobutton(window, text="Top Left", variable=start_position, value=0)
top_left_radio.grid(column=1, row=position_row)

top_right_radio = Radiobutton(window, text="Top Right", variable=start_position, value=1)
top_right_radio.grid(column=2, row=position_row, sticky="W")

btn_row = position_row + 1
btn = Button(window, text="Stitch", bg="black", fg="white", width=20, height=2, command=clicked)
btn.grid(column=1, row=btn_row, columnspan=2, sticky="W")

window.mainloop()