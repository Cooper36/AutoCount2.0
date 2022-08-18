from tkinter import *

#Create window object
app = Tk()



#Experiment Name
ExpName_text = StringVar() 
ExpName_label = Label(app, text = 'Experiment Name', font = ('bold', 14), padx = 20, pady=20)
ExpName_label.grid(row = 0, column = 0, sticky=W)
ExpName_entry = Entry(app, textvariable=ExpName_text)
ExpName_entry.grid(row=0, column=1)

#Path
path_text = StringVar() 
path_label = Label(app, text = 'Path to image folder', font = ('bold', 14), padx = 20, pady=0)
path_label.grid(row = 1, column = 0, sticky=W)
path_entry = Entry(app, textvariable=path_text)
path_entry.grid(row=1, column=1)

#Channel Settings

ChannelTitle_label = Label(app, text = 'Channel Settings', font = ('bold', 18),padx = 10, pady=10)
ChannelTitle_label.grid(row = 3, column = 0, sticky=W)

Channel1_text = StringVar() 
Channel1_label = Label(app, text = 'Channel 1 Title', font = ('bold', 14), padx = 20, pady=0)
Channel1_label.grid(row = 4, column = 0, sticky=W)
Channel1_entry = Entry(app, textvariable=Channel1_text)
Channel1_entry.grid(row=4, column=1)

Channel2_text = StringVar() 
Channel2_label = Label(app, text = 'Channel 2 Title', font = ('bold', 14), padx = 20, pady=0)
Channel2_label.grid(row = 5, column = 0, sticky=W)
Channel2_entry = Entry(app, textvariable=Channel2_text)
Channel2_entry.grid(row=5, column=1)

Channel3_text = StringVar() 
Channel3_label = Label(app, text = 'Channel 3 Title', font = ('bold', 14), padx = 20, pady=0)
Channel3_label.grid(row = 6, column = 0, sticky=W)
Channel3_entry = Entry(app, textvariable=Channel3_text)
Channel3_entry.grid(row=6, column=1)

Channel4_text = StringVar() 
Channel4_label = Label(app, text = 'Channel 4 Title', font = ('bold', 14), padx = 20, pady=0)
Channel4_label.grid(row = 7, column = 0, sticky=W)
Channel4_entry = Entry(app, textvariable=Channel4_text)
Channel4_entry.grid(row=7, column=1)






app.title('AutoCounter2.0')
app.geometry('700x350')

#Start program
app.mainloop()