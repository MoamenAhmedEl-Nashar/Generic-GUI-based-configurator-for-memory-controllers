"""The goal of this GUI program is to make the process of change parameters
in test benches easily, it parses the verilog input file, than extract
parameters for each module instance. Also, it parse `include and `define
to allow the user to control `ifdef that controls module instances or
controls code within them.
"""
from tkinter import *  # the GUI is based on Tkinter
from tkinter import filedialog  # filedialog is to allow uploading any file
import tkinter.ttk as ttk  # ttk to make new styles to old tkiter
from ttkthemes import ThemedTk  # themes
from scrframe import *  # scroll frame class
from pyparsing import Word, alphas, nums, cStyleComment, pyparsing_common, \
    Regex, ZeroOrMore, Literal, replaceWith, originalTextFor, Combine, \
    Optional, Group, delimitedList, Keyword
# import pyparsing to parse verilog grammar


class Root(ThemedTk):
    """The main class of the program frontend and backend"""
    # class attributes (same for all instances of a class)
    Ident = pyparsing_common.identifier
    hexnums = nums + "abcdefABCDEF" + "_?"
    base = Regex("'[bBoOdDhH]")
    basedNumber = Combine(Optional(Word(nums + "_")) +
                          base + Word(hexnums+"xXzZ"))
    number = (basedNumber | Regex(
        r"[+-]?[0-9_]+(\.[0-9_]*)?([Ee][+-]?[0-9_]+)?"))
    Primary = number
    Range = "[" + Primary + ":" + Primary + "]"
    ParameterAssignment = Ident.setResultsName("name", listAllMatches=True) + \
        Optional(Range) + "=" + \
        Primary.setResultsName("value", listAllMatches=True)
    parameter_declaration = Keyword("parameter") + ParameterAssignment + \
        ZeroOrMore(("," + ParameterAssignment))
    parameter_declaration.ignore(cStyleComment)
    parameter_declaration.ignore(Regex(r"//.*\n"))
    parameter_declaration.ignore(" ")

    # instance attributes (different for every instance of a class.)
    def __init__(self, *args, **kwargs):
        ThemedTk.__init__(self, *args, **kwargs, theme="arc")
        self.parameters = {}
        self.entries = []
        self.edit_param = []
        self.file_path = ""

        self.style = ttk.Style()
        self.style.configure("TFrame", padding=9,
                             relief="flat", bg="LightBlue4", fg="gray15")
        self.style.configure("TButton", padding=9,
                             relief="raised", font=("Helvetica ", 20))
        self.title('Generic GUI-based configurator')
        # w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        # self.geometry("%dx%d+0+0" % (w, h))

        self.frame_left = VerticalScrolledFrame(self, borderwidth=4)
        self.frame_right = ttk.Frame(self, borderwidth=4)
        self.frame_bottom = ttk.Frame(self, borderwidth=4)

        self.upload_button = ttk.Button(
            self.frame_bottom, text="upload", command=lambda: self.read_file())
        self.save_button = ttk.Button(
            self.frame_bottom, text="save", command=lambda: self.save_file())

        # grid
        self.frame_left.grid(row=0, column=0, sticky="nsew")
        self.frame_right.grid(row=0, column=1, sticky="nsew")
        self.frame_bottom.grid(row=1, column=0)

        # frame bottom
        self.upload_button.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.save_button.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

    # methods

    def read_file(self):
        """read the input file and parse its contents"""

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

        # search input code to get parameters

        token = self.parameter_declaration.scanString(self.source_code)
        for t, s, e in token:
            l_name = t.name.asList()
            l_value = t.value.asList()
            for name, value in zip(l_name, l_value):
                self.parameters[name] = value

        # given a list of parameters, build the frame_left parameters
        r = 0
        for name, value in self.parameters.items():
            param_label = ttk.Label(
                self.frame_left.interior, text=name, font=("Courier", 20))
            param_entry = ttk.Entry(self.frame_left.interior)
            param_entry.insert(END, value)

            self.entries.append(param_entry)
            param_label.grid(row=r, column=0, padx=5, pady=5)
            param_entry.grid(row=r, column=1, padx=5, pady=5)
            r += 1

    def replace_param(self, s, loks, toks):
        """replace values of parameters with the new one"""

        for i in range(3, len(toks), 4):
            toks[i] = self.parameters[toks[i-2]]
        return " ".join(toks)  # to put spaces between tokens

    def save_file(self):
        """save the new file back after parsing and replacing"""

        i = 0
        for name in self.parameters.keys():
            self.parameters[name] = self.entries[i].get()
            i += 1
        # modify input file
        input_file = open(self.file_path, "w")

        self.parameter_declaration.setParseAction(self.replace_param)
        new_code = self.parameter_declaration.transformString(self.source_code)

        input_file.write(new_code)
        input_file.close()


root = Root()
root.mainloop()
