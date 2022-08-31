from tkinter import *
from tkinter import ttk

#Create window object
app = Tk()

def load_settings():
	print('Loading Settings')
	

def clear_inputs():
	print('Clearing Inputs')

def load_ROIs():
	print('Load ROIs')

vline_sep = ttk.Separator(app, orient='vertical')
vline_sep.grid(row = 0, column = 2, rowspan=20, sticky = 'ns')

#Experiment Name
ExpName_text = StringVar() 
ExpName_label = Label(app, text = 'Experiment Name', font = ('bold', 14), padx = 10, pady=0)
ExpName_label.grid(row = 0, column = 0, sticky = W)
ExpName_entry = Entry(app, textvariable=ExpName_text)
ExpName_entry.grid(row=0, column=1)

#Path
path_text = StringVar() 
path_label = Label(app, text = 'Path to image folder', font = ('bold', 14), padx = 10, pady=0)
path_label.grid(row = 1, column = 0, sticky = W)
path_entry = Entry(app, textvariable=path_text)
path_entry.grid(row=1, column=1)


#Buttons
load_btn = Button(app, text='Load Settings', width =10, command=load_settings)
load_btn.grid(row = 0, column = 3, sticky = E, rowspan = 2)

clear_btn = Button(app, text='Clear', width =10, command= clear_inputs)
clear_btn.grid(row = 0, column = 4, sticky = W, rowspan = 2)

loadROI_btn = Button(app, text='Load ROIs', width =10, command= load_ROIs)
loadROI_btn.grid(row = 12, column = 3, rowspan = 1, )

#Channel Settings
hlineChan_sep = ttk.Separator(app, orient='horizontal')
hlineChan_sep.grid(row = 2, column = 0, sticky = EW)

ChannelTitle_label = Label(app, text = 'Channel Settings', font = ('bold', 18),padx = 10)
ChannelTitle_label.grid(row = 2, column = 0, rowspan = 2, sticky=W)

Channel1_text = StringVar() 
Channel1_label = Label(app, text = 'Channel 1 Title', font = ('bold', 14), padx = 10, pady=0)
Channel1_label.grid(row = 4, column = 0)
Channel1_entry = Entry(app, textvariable=Channel1_text)
Channel1_entry.grid(row=4, column=1)

Channel2_text = StringVar() 
Channel2_label = Label(app, text = 'Channel 2 Title', font = ('bold', 14), padx = 10, pady=0)
Channel2_label.grid(row = 5, column = 0)
Channel2_entry = Entry(app, textvariable=Channel2_text)
Channel2_entry.grid(row=5, column=1)

Channel3_text = StringVar() 
Channel3_label = Label(app, text = 'Channel 3 Title', font = ('bold', 14), padx = 10, pady=0)
Channel3_label.grid(row = 6, column = 0)
Channel3_entry = Entry(app, textvariable=Channel3_text)
Channel3_entry.grid(row=6, column=1)

Channel4_text = StringVar() 
Channel4_label = Label(app, text = 'Channel 4 Title', font = ('bold', 14), padx = 10, pady=0)
Channel4_label.grid(row = 7, column = 0)
Channel4_entry = Entry(app, textvariable=Channel4_text)
Channel4_entry.grid(row=7, column=1)

ChannelOptions = ["Channel 1", "Channel 2", "Channel 3", "Channel 4"]
NucleiChan_Choice = StringVar() 
NucleiChan_Choice.set(ChannelOptions[0])
NucleiChan_label = Label(app, text = 'Nuclei Count \n Channel', font = ('bold', 14), padx = 10, pady=0)
NucleiChan_label.grid(row = 8, column = 0)
NucleiChan_menu = OptionMenu(app, NucleiChan_Choice, *ChannelOptions)
NucleiChan_menu.grid(row=8, column=1, sticky = W)

#Image Settings
ImageSettings_label = Label(app, text = 'Image Settings', font = ('bold', 18),padx = 10)
ImageSettings_label.grid(row = 3, column = 3, rowspan = 2, sticky=W)

MagOptions = ["4x", "10x", "20x", "40x", "60x"]
Mag_Choice = StringVar() 
Mag_Choice.set(MagOptions[0])
ImageMag_label = Label(app, text = 'Image Magnification', font = ('bold', 14), padx = 10, pady=0)
ImageMag_label.grid(row = 5, column = 3, sticky=W)
Mag_menu = OptionMenu(app, Mag_Choice, *MagOptions)
Mag_menu.grid(row=5, column=4, sticky = W)
""" Old Code for radio buttons for magnifications
v = IntVar()
v.set(1)  # initializing the choice, i.e. Python
ImageMag_choices = [('4x',101), ('10x',102), ('20x',103), ('60x',104)]
def ShowChoice():
    print(v.get())
columnint = 4 
for ImageMag_choices, val in ImageMag_choices:
	Radiobutton(app, text=ImageMag_choices, padx = 0, variable=v, command=ShowChoice,value=val).grid(row = 4, column = columnint, sticky=W)
	print(columnint)
	columnint = columnint +1
	"""

Or_label = Label(app, text = 'OR', font = ('bold', 14), padx = 10, pady=0)
Or_label.grid(row = 6, column = 3)

SpecifyScale_text = StringVar() 
SpecifyScale_label = Label(app, text = 'Specify Scale', font = ('bold', 14), padx = 10, pady=0)
SpecifyScale_label.grid(row = 7, column = 3)
SpecifyScale_entry = Entry(app, textvariable=SpecifyScale_text)
SpecifyScale_entry.grid(row=7, column=4)

#ROIs settings
ROISettings_label = Label(app, text = 'ROI Settings', font = ('bold', 18),padx = 10)
ROISettings_label.grid(row = 8, column = 3, rowspan = 2, sticky=W)

ROInum_text = StringVar() 
ROInum_label = Label(app, text = 'Number of ROIs', font = ('bold', 14), padx = 10, pady=0)
ROInum_label.grid(row = 10, column = 3)
ROInum_entry = Entry(app, textvariable=Channel4_text)
ROInum_entry.grid(row=10, column=4)

Or_label2 = Label(app, text = 'OR', font = ('bold', 14), padx = 10, pady=0)
Or_label2.grid(row = 11, column = 3)

app.title('AutoCounter2.0')
app.geometry('800x350')

#Start program
app.mainloop()