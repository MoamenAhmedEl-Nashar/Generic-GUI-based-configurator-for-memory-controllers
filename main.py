from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk
from scrframe import *
from pyparsing import Word, alphas, nums, cStyleComment, pyparsing_common, \
Regex, ZeroOrMore, Literal


class Root(Tk):

    # class attributes (same for all instances of a class)
    Ident = pyparsing_common.identifier
    Primary = pyparsing_common.signed_integer
    ParameterAssignment = Ident.setResultsName("name", listAllMatches=True) + "=" + Primary.setResultsName("value", listAllMatches=True)
    parameter_declaration = Literal("parameter ") + ParameterAssignment + ZeroOrMore(("," + ParameterAssignment))
    parameter_declaration.ignore(cStyleComment) 
    parameter_declaration.ignore(Regex(r"//.*\n"))
    parameter_declaration.ignore(" ")  
    
    # instance attributes (different for every instance of a class.)
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.parameters = {}
        self.entries = []
        self.edit_param = []
        self.file_path = ""
        
        self.style = ttk.Style()
        self.style.configure("TFrame",
                        padding=9,
                        relief="flat",
                        bg="LightBlue4",
                        fg="gray15")
        self.style.configure("TButton", padding=9, relief="raised", font=("Helvetica ", 20))
        self.title('Generic GUI-based configurator')
        #w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        #self.geometry("%dx%d+0+0" % (w, h))

        self.frame_left = VerticalScrolledFrame(self, borderwidth=4)
        self.frame_right = ttk.Frame(self, borderwidth=4)
        self.frame_bottom = ttk.Frame(self, borderwidth=4)

        self.upload_button = ttk.Button(
        	self.frame_bottom,
        	text="upload",
        	command=lambda: self.read_file()
        )
        self.save_button = ttk.Button(
        	self.frame_bottom,
        	text="save",
        	command=lambda: self.save_file()
        )

        ### grid ###
        self.frame_left.grid(row=0, column=0, sticky="nsew")
        self.frame_right.grid(row=0, column=1, sticky="nsew")
        self.frame_bottom.grid(row=1, column=0, sticky="nsew")

        ## frame bottom
        self.upload_button.grid(row=0, column=0, sticky="nsew")
        self.save_button.grid(row=0, column=1, sticky="nsew")

    # methods
    

    def read_file(self):
        # resetting
        self.parameters.clear()
        self.entries.clear()
        self.edit_param.clear()
        self.file_path = ""
        self.parameter_declaration.setParseAction()
        for child in self.frame_left.interior.winfo_children():
            child.destroy()
        self.frame_left.interior.grid_forget()

        self.file_path = filedialog.askopenfilename()
        
        self.file_path = self.file_path
        # input sv file reading
        with open(self.file_path, "r") as input_file:
            self.source_code = input_file.read()

        # search input code to get self.parameters 
                
        token = self.parameter_declaration.scanString(self.source_code)
        for t,s,e in token:
            l_name = t.name.asList()
            l_value = t.value.asList()
            for name, value in zip(l_name, l_value):
                self.parameters[name] = value
        
        # given a list of self.parameters, build the frame_left self.parameters input with scrollbar
        r=0
        
        for name, value in self.parameters.items():
            param_label = ttk.Label(self.frame_left.interior, text=name, font=("Courier", 20))
            param_entry = ttk.Entry(self.frame_left.interior)
            param_entry.insert(END, value)
           
            self.entries.append(param_entry)
            param_label.grid(row=r, column=0)
            param_entry.grid(row=r, column=1)
            r+=1
        
    def replace_param(self, s, loks, toks):
        for i in range(3, len(toks), 4):
            toks[i] = self.parameters[toks[i-2]]

    def save_file(self):
        i = 0
        for name in self.parameters.keys():
            self.parameters[name] = self.entries[i].get()
            i+=1
        ## modify input file
        input_file = open(self.file_path, "w") 

        self.parameter_declaration.setParseAction(self.replace_param)
        new_code = self.parameter_declaration.transformString(self.source_code)

        input_file.write(new_code)
        input_file.close()
        
root = Root()
root.mainloop()