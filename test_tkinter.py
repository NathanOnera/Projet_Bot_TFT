
import tkinter as tk
import tkinter.ttk # separator

root = tk.Tk()
frame1 = tk.Frame(root)
frame2 = tk.Frame(root)
label1 = tk.Label(frame1, text = 'test1')
label1b = tk.Label(frame1, text = 'test1')
label1t = tk.Label(frame1, text = 'test1')
label2 = tk.Label(frame2, text = 'test2')
sep = tkinter.ttk.Separator(frame1, orient='horizontal')
sep2 = tkinter.ttk.Separator(root, orient='vertical')

frame1.grid(row = 0, column = 0)
frame2.grid(row = 0, column = 2)
label1.grid(row = 0, column = 0)
label1b.grid(row = 0, column = 1)
label1t.grid(row = 0, column = 2)
label2.grid()
sep.grid(row = 1, columnspan = 200,sticky='ew')
sep2.grid(row = 0, column = 1, sticky = 'ns')

root.mainloop()
