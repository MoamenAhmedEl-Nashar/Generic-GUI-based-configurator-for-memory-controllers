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
    Optional, Group, delimitedList, Keyword, Forward, SkipTo, PrecededBy
# import pyparsing to parse verilog grammar


class Root(ThemedTk):
    """The main class of the program frontend and backend"""
    # class attributes (same for all instances of a class)

    ## general
    identifier = pyparsing_common.identifier
    hexnums = nums + "abcdefABCDEF" + "_?"
    base = Regex("'[bBoOdDhH]")
    basedNumber = Combine(Optional(Word(nums + "_")) +
                          base + Word(hexnums+"xXzZ"))
    number = (basedNumber | Regex(
        r"[+-]?[0-9_]+(\.[0-9_]*)?([Ee][+-]?[0-9_]+)?"))
    Primary = number
    Range = "[" + Primary + ":" + Primary + "]"
    ## parameter
    ParameterAssignment = identifier.setResultsName("name", listAllMatches=True) + \
        Optional(Range) + "=" + \
        Primary.setResultsName("value", listAllMatches=True)
    parameter_declaration = Keyword("parameter") + ParameterAssignment + \
        ZeroOrMore(("," + ParameterAssignment))
    parameter_declaration.ignore(cStyleComment)
    parameter_declaration.ignore(Regex(r"//.*\n"))
    parameter_declaration.ignore(" ")
    ## module instance
    # search for the second identifier inside ()
    namedPortConnection = "." + identifier + "(" + identifier + ")"
    # in parsing test benches: we don't care about the parameter in the design file of the module definition
    modulePortConnection = identifier

    instanceArgs = "(" + (delimitedList(namedPortConnection) |
                          delimitedList(modulePortConnection)) + ")"
    # parameterValueAssignment = Literal("#") + instanceArgs("y")

    moduleInstance = identifier + instanceArgs
    moduleInstantiation = identifier("module_name") + Optional(Literal("#") + "(" + (delimitedList("." + identifier + "(" + identifier.setResultsName(
        "name", listAllMatches=True) + ")") | delimitedList(identifier)) + ")") + delimitedList(moduleInstance) + ";"
    moduleInstantiation.ignore(cStyleComment)
    moduleInstantiation.ignore(Regex(r"//.*\n"))
    moduleInstantiation.ignore(" ")
    ## `ifdef
    ifdef = Forward()
    stmt = SkipTo(Keyword("`else")) | SkipTo(Keyword("`endif"))
    ifdef << Keyword("`ifdef") + identifier("def_name") + (ifdef | stmt.suppress()) + Optional(
        Keyword("`else") + (ifdef | stmt.suppress())) + Keyword("`endif")
    ifdef.ignore(cStyleComment)
    ifdef.ignore(Regex(r"//.*\n"))
    ifdef.ignore(" ")
    ## `define
    define = Keyword("`define") + \
        identifier.setResultsName("def_name", listAllMatches=True)
    define.ignore(ifdef)
    define.ignore(cStyleComment)
    define.ignore(Regex(r"//.*\n"))
    define.ignore(" ")
    # instance attributes (different for every instance of a class.)

    def __init__(self, *args, **kwargs):
        ThemedTk.__init__(self, *args, **kwargs, theme="arc")
        self.parameters = {}
        self.defines = {}
        self.param_entries = []
        self.define_entries = []
        self.edit_param = []
        self.file_path = ""
        self.module_parameter_names = []

        self.style = ttk.Style()
        self.style.configure("TFrame", padding=9, relief="raised")
        self.style.configure("TButton", padding=9,
                             relief="raised", font=("Helvetica ", 20))
        self.style.configure("TEntry", padding=9,
                             relief="raised", font=("Helvetica ", 15))
        self.style.configure("TRadiobutton", padding=9,
                             relief="raised", font=("Helvetica ", 15))
        self.title('Generic GUI-based configurator')
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry("%dx%d+0+0" % (w, h))

        self.frame_left = VerticalScrolledFrame(self, borderwidth=4)
        self.frame_right = VerticalScrolledFrame(self, borderwidth=4)
        self.frame_bottom = ttk.Frame(self, borderwidth=4)
        self.frame_mid = ttk.Frame(self, borderwidth=4)
        self.frame_top = ttk.Frame(self, borderwidth=4)

        # labels
        self.defines_label = ttk.Label(
            self.frame_top, text="defines section", font=(10))
        self.parameters_label = ttk.Label(
            self.frame_top, text="parameters section", font=(10))
        # main buttons
        self.upload_button = ttk.Button(
            self.frame_bottom, text="upload", command=lambda: self.read_file())
        self.save_button = ttk.Button(
            self.frame_bottom, text="save", command=lambda: self.save_file())
        self.update_defines_button = ttk.Button(
            self.frame_mid, text="update ->", command=lambda: self.save_defines())

        # radio buttons (desgin or test file)
        self.select_design_or_test = IntVar()
        self.select_design_or_test.set(2)  # default is test
        self.design_radio = ttk.Radiobutton(
            self.frame_bottom, text="design file", variable=self.select_design_or_test, value=1)
        self.test_radio = ttk.Radiobutton(
            self.frame_bottom, text="test file", variable=self.select_design_or_test, value=2)
        self.info_label = ttk.Label(
            self.frame_bottom, text="Please select mode before uploading.", font=(10))

        # grid
        # to make widgets propagate (fit) its parent
        self.columnconfigure(0, weight=1)
        # to make widgets propagate (fit) its parent
        self.rowconfigure(0, weight=1)
        # to make widgets propagate (fit) in its parent
        self.frame_left.interior.columnconfigure(0, weight=1)
        # to make widgets propagate (fit) in its parent
        self.frame_left.interior.rowconfigure(0, weight=1)
        self.frame_left.grid(row=1, column=2, sticky="nsew")
        # to make widgets propagate (fit) in its parent
        self.frame_right.interior.columnconfigure(0, weight=1)
        # to make widgets propagate (fit) in its parent
        self.frame_right.interior.rowconfigure(0, weight=1)
        self.frame_right.grid(row=1, column=0, sticky="nsew")
        self.frame_bottom.grid(row=2, column=0, padx=5, pady=5)
        self.frame_mid.grid(row=1, column=1, padx=5, pady=5)
        self.frame_top.grid(row=0, column=0, padx=5, pady=5)

        # frame_top
        self.parameters_label.grid(
            row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.defines_label.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        #frame_mid
        self.update_defines_button.grid(
            row=0, column=0, sticky="nsew", padx=5, pady=5)

        # frame bottom
        self.upload_button.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.save_button.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # radio buttons
        self.info_label.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.test_radio.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.design_radio.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)

    # methods

    def read_file(self):
        """read the input file and parse its contents,
           called on clicking upload button."""

        ## resetting
        self.parameters.clear()
        self.defines.clear()
        self.param_entries.clear()
        self.define_entries.clear()
        self.module_parameter_names.clear()
        self.edit_param.clear()
        self.file_path = ""
        self.parameter_declaration.setParseAction()
        for child in self.frame_left.interior.winfo_children():
            child.destroy()
        self.frame_left.interior.grid_forget()
        for child in self.frame_right.interior.winfo_children():
            child.destroy()
        self.frame_right.interior.grid_forget()
        self.file_path = filedialog.askopenfilename()

        self.file_path = self.file_path
        ## input sv file reading
        with open(self.file_path, "r") as input_file:
            self.source_code = input_file.read()

        ## search input code to get `ifdefs
        def_tree = self.ifdef.scanString(self.source_code)
        for t, s, e in def_tree:
            d = t.def_name
            self.defines[d] = 0
        ## Knowing defines is defined or not
        define_tokens = self.define.scanString(self.source_code)
        for t, s, e in define_tokens:
            self.defines[t.def_name] = 1
        ## given a list of defines, build the frame_right defines
        r = 0
        for name, value in self.defines.items():
            define_label = ttk.Label(
                self.frame_right.interior, text=name, font=("Courier", 20))
            define_entry = ttk.Entry(
                self.frame_right.interior, font=("Helvetica ", 15))
            define_entry.insert(END, value)
            self.define_entries.append(define_entry)
            define_label.grid(row=r, column=0, padx=5, pady=5)
            define_entry.grid(row=r, column=1, padx=5, pady=5)
            r += 1
        if r == 0:  # no defines
            define_label = ttk.Label(
                self.frame_right.interior, text="No defines found, Click update to see parameters", font=("Courier", 20))
            define_label.grid(row=0, column=0, padx=5, pady=5)

    def show_parameters(self):
        """search input code to get parameters"""

        ## resetting
        self.parameters.clear()
        self.param_entries.clear()
        self.module_parameter_names.clear()
        self.module_name = ""
        self.edit_param.clear()
        for child in self.frame_left.interior.winfo_children():
            child.destroy()
        self.frame_left.interior.grid_forget()
        self.parameter_declaration = Keyword("parameter") + self.ParameterAssignment + \
            ZeroOrMore(("," + self.ParameterAssignment))
        self.parameter_declaration.ignore(cStyleComment)
        self.parameter_declaration.ignore(Regex(r"//.*\n"))
        self.parameter_declaration.ignore(" ")
        self.moduleInstantiation = self.identifier("module_name") + Optional(Literal("#") + "(" + (delimitedList("." + self.identifier + "(" + self.identifier.setResultsName(
            "name", listAllMatches=True) + ")") | delimitedList(self.identifier)) + ")") + delimitedList(self.moduleInstance) + ";"
        self.moduleInstantiation.ignore(cStyleComment)
        self.moduleInstantiation.ignore(Regex(r"//.*\n"))
        self.moduleInstantiation.ignore(" ")
        ## modifying parameter_declaration according to defines
        ifdef_non_rec = Keyword("`ifdef") + self.identifier("def_name") + self.stmt("ifstmt") + Optional(
            Keyword("`else") + self.stmt("elsestmt")) + Keyword("`endif")
        ifdef_non_rec.ignore(cStyleComment)
        ifdef_non_rec.ignore(Regex(r"//.*\n"))
        ifdef_non_rec.ignore(" ")
        specific_token = ifdef_non_rec.scanString(self.source_code)
        for t, s, e in specific_token:
            if self.defines[t.def_name] == "1":  # defined
                temp_parse = Keyword("`ifdef") + Keyword(t.def_name)
                temp_parse2 = PrecededBy(t.ifstmt.strip()) + Keyword("`endif")
                temp_parse3 = Keyword("`else") + \
                    Keyword(t.elsestmt) + Keyword("`endif")
            elif self.defines[t.def_name] == "0":  # not defined
                temp_parse = Keyword("`ifdef") + \
                    Keyword(t.def_name) + Keyword(t.ifstmt)
                temp_parse2 = PrecededBy(t.elsestmt.strip()) + Keyword("`endif")
                temp_parse3 = PrecededBy(t.ifstmt.strip()) + Keyword("`else")
            self.parameter_declaration.ignore(temp_parse)
            self.parameter_declaration.ignore(temp_parse2)
            self.parameter_declaration.ignore(temp_parse3)
            self.moduleInstantiation.ignore(temp_parse)
            self.moduleInstantiation.ignore(temp_parse2)
            self.moduleInstantiation.ignore(temp_parse3)

        ## parse input file to get parameters
        token = self.parameter_declaration.scanString(self.source_code)
        for t, s, e in token:
            l_name = t.name.asList()
            l_value = t.value.asList()
            for name, value in zip(l_name, l_value):
                self.parameters[name] = value

        ## scan for module instance only in test files
        if self.select_design_or_test.get() == 2:  # test file
            module_token = self.moduleInstantiation.scanString(
                self.source_code)
            for t, s, e in module_token:
                self.module_parameter_names = t.name.asList()
                self.module_name = t.module_name

        if self.select_design_or_test.get() == 2:  # test file
            param_label = ttk.Label(
                self.frame_left.interior, text="module: "+self.module_name, font=("Courier", 20))
            param_label.grid(row=0, column=0, padx=5, pady=5)

        ## given a list of parameters, build the frame_left parameters
        r = 1
        for name, value in self.parameters.items():
            if name in self.module_parameter_names or self.select_design_or_test.get() == 1:  # design file
                param_label = ttk.Label(
                    self.frame_left.interior, text=name, font=("Courier", 20))
                param_entry = ttk.Entry(
                    self.frame_left.interior, font=("Helvetica ", 15))
                param_entry.insert(END, value)

                self.param_entries.append(param_entry)
                param_label.grid(row=r, column=0, padx=5, pady=5)
                param_entry.grid(row=r, column=1, padx=5, pady=5)
                r += 1

    def replace_param(self, s, loks, toks):
        """replace values of parameters with the new one"""

        for i in range(3, len(toks), 4):
            toks[i] = self.parameters[toks[i-2]]
        return " ".join(toks)  # to put spaces between tokens

    def undefine_it(self, s, loks, toks):
        """remove `define"""
        toks = ""
        return toks

    def define_it(self, toks, name):
        """remove `define"""
        s = "\n `define " + name + "\n"
        toks.append(s)
        return " ".join(toks)

    def save_defines(self):
        """update defines dictionary"""
        ## save the new defines values
        i = 0
        for name in self.defines.keys():
            self.defines[name] = self.define_entries[i].get()
            i += 1

        self.show_parameters()

    def save_file(self):
        """save the new file back after parsing and replacing"""

        ## save the new defines values if the user doesn't click update
        if len(self.parameters) == 0:
            i = 0
            for name in self.defines.keys():
                self.defines[name] = self.define_entries[i].get()
                i += 1

        ## save the new parameters values
        i = 0
        for name in self.parameters.keys():
            if name in self.module_parameter_names or self.select_design_or_test.get() == 1:  # design file:
                self.parameters[name] = self.param_entries[i].get()
                i += 1

        # modify input file
        input_file = open(self.file_path, "w")
        ## modify defines
        new_code = self.source_code
        for name, value in self.defines.items():
            define_specific = Keyword(
                "`define") + Keyword(name).setResultsName("def_name", listAllMatches=True)
            define_specific.ignore(self.ifdef)
            define_specific.ignore(cStyleComment)
            define_specific.ignore(Regex(r"//.*\n"))
            define_specific.ignore(" ")
            define_specific_token = define_specific.scanString(new_code)
            try:
                # check the generator is empty or not
                next(define_specific_token)
                # defined
                if value == '0':  # must be not defined
                    define_specific.setParseAction(self.undefine_it)
                    new_code = define_specific.transformString(new_code)
            except:
                # not defined
                if value == '1':  # must be defined
                    # if the verilog file has at least one define statement
                    # - put the new define statement after it
                    dummy_define = Keyword("`define") + self.identifier
                    dummy_define.ignore(self.ifdef)
                    dummy_define.ignore(cStyleComment)
                    dummy_define.ignore(Regex(r"//.*\n"))
                    dummy_define.ignore(" ")
                    dummy_define.setParseAction(
                        lambda toks: self.define_it(toks, name))
                    define_tokens = dummy_define.scanString(
                        new_code, maxMatches=1)
                    try:
                        # check the generator is empty or not
                        next(define_tokens)
                        new_code = dummy_define.transformString(new_code)

                    except:
                        # if there are no define statements
                        # - put the new define statement at first line
                        s = "\n `define " + name + "\n"
                        new_code = s + new_code

        ## modify parameters

        self.parameter_declaration.setParseAction(self.replace_param)
        new_code = self.parameter_declaration.transformString(new_code)

        input_file.write(new_code)
        input_file.close()


root = Root()
root.mainloop()
