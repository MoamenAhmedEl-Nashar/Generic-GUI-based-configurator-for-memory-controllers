from tkinter import *
import tkinter.ttk as ttk


class VerticalScrolledFrame(Frame):

    def __init__(self, parent, *args, **kw):
        self.style = ttk.Style()
        self.style.configure("TFrame", padding=9,
                             relief="flat", bg="LightBlue4", fg="gray15")
        ttk.Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = ttk.Scrollbar(self, orient=VERTICAL)
        canvas = Canvas(self, yscrollcommand=vscrollbar.set, height=400, width=400)
        canvas.configure(scrollregion=canvas.bbox("all"))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        canvas.grid(row=0, column=0, sticky="nsew")
        vscrollbar.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it

        self.interior = ttk.Frame(canvas, width=700)
        interior_id = canvas.create_window(0, 0, window=self.interior,
                                           anchor=NW)


                                    
        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if self.interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=self.interior.winfo_reqwidth())
        self.interior.bind('<Configure>', _configure_interior)

        def _bound_to_mousewheel(event):
            self.interior.bind_all("<MouseWheel>", _on_mousewheel)   
        
        def _unbound_to_mousewheel( event):
            self.interior.unbind_all("<MouseWheel>") 

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        self.interior.bind('<Enter>', _bound_to_mousewheel)
        self.interior.bind('<Leave>', _unbound_to_mousewheel)
        self.interior.bind('<MouseWheel>', _on_mousewheel)

        def _configure_canvas(event):
            if self.interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)
        

