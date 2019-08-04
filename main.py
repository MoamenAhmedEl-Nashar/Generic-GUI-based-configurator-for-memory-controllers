from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk
from scrframe import *
from pyparsing import Word, alphas, nums, cStyleComment, pyparsing_common, Regex


class Root(Tk):

    # class attributes (same for all instances of a class)
    
    parameter_declaration = "parameter" + pyparsing_common.identifier("name") + "=" + Word(nums)("value")
    parameter_declaration.ignore(cStyleComment) 
    parameter_declaration.ignore(Regex(r"//.*\n")) 

    # parameter_declaration = Lark("""
    # start:"parameter" WORD "=" NUMBER  
    # WORD:/ [a-zA-Z][a-zA-Z_0-9]* /
    # COMMENT: ("/*" /.*/ "*/") | "//" / .* /
    # IGNORED: " " | NEWLINE | COMMENT
    # %import common.NUMBER
    # %import common.NEWLINE
    # %ignore IGNORED
    # """
    # )
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
    
        self.file_path = filedialog.askopenfilename()
        
        self.file_path = self.file_path
        # input sv file reading
        with open(self.file_path, "r") as input_file:
            self.source_code = input_file.read()

        # search input code to get self.parameters 
        st_index = 0
        self.edit_param = []
        for statement in self.source_code.split(";"):
            try:
                token = self.parameter_declaration.parseString(statement)
                name = token.name
                value = token.value
                self.parameters[name] = value
                self.edit_param.append(st_index)
                st_index += 1
                print(name, value)
            except:
                st_index += 1
                continue
        
        self.edit_param = self.edit_param
        print(self.edit_param)
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
        
    def save_file(self):
        i = 0
        for name in self.parameters.keys():
            self.parameters[name] = self.entries[i].get()
            i+=1
        ## modify input file
        input_file = open(self.file_path, "w") 
        statements = self.source_code.split(";")
        
        for i in range(len(self.edit_param)):
            statement = statements[self.edit_param[i]]
            token = self.parameter_declaration.parseString(statement)
            name = token.name
            value = token.value
            new_statement = statement.replace(value, self.parameters[name])
            statements[self.edit_param[i]] = new_statement
        new_code = ";".join(statements)
        input_file.write(new_code)
        input_file.close()
        
root = Root()
root.mainloop()