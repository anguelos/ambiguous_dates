#!/usr/bin/env python3


from tkinter import Misc, DoubleVar, Entry, Label, Frame, Button, Tk

from typing import Any
from typing_extensions import Literal
from RangeSlider.RangeSlider import RangeSliderH

# from tkinter import *
import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

from typing import Any, Union, Dict, Literal, Tuple
import sys

t_pixel_value = Union[int, float]


class DateRangeSlider(Frame):
    def show_small_form(self):
        if self.large_form:
            self.large_form = False
            self.update_btn.config(text='Edit')
            self.curve_frame.pack_forget()
            self.rs1.pack_forget()
            self.mode_frame.pack_forget()
            self.comment_frame.pack_forget()
            self.txtbox_from.config(state='readonly')
            self.txtbox_to.config(state='readonly')
            self.update()

    def show_large_form(self):
        if not self.large_form:
            self.large_form = True
            self.update_btn.config(text='Set')
            self.curve_frame.pack(side="top", anchor="w",
                                  fill='x', expand=True)
            self.rs1.pack()

            self.mode_frame.pack(anchor="w", fill='x', expand=True)
            self.comment_frame.pack(anchor="w", fill='x', expand=True)

            self.txtbox_from.config(state='normal')
            self.txtbox_to.config(state='normal')
            self.update()

    def toggle_form(self):
        if self.large_form:
            self.show_small_form()
        else:
            self.show_large_form()

    def update_curve(self, *args):
        if "counter" not in self.__dict__.keys():
            self.counter = 0
        else:
            self.counter += 1

        self.ax.clear()
        self.ax.set_xlim(self.earliest_date[0], self.latest_date[0]+1)

        from_val = float(self.from_Var.get())
        to_val = float(self.to_Var.get())
        uniform = (self.years >= from_val).astype(np.double) * \
            (self.years <= to_val).astype(np.double)
        g_mean = (from_val + to_val) / 2
        g_variance = (to_val - from_val) ** 2 / (12 * np.log(2))
        gaussian = np.exp(-((self.years - g_mean)**2)/(2*g_variance))
        if not self.is_plausibillity_mode:  # is a PDF
            uniform = uniform / np.sum(uniform)
            gaussian = gaussian / np.sum(gaussian)

        self.ax.set_ylim(0, 1.5*max(np.max(uniform), np.max(gaussian)))
        if self.mode_var.get() == "Uniform":
            unif_strokewidth = 3
            gauss_strokewidth = 1
        elif self.mode_var.get() == "Gaussian":
            unif_strokewidth = 1
            gauss_strokewidth = 3
        else:
            raise ValueError(
                f"Unknown mode_var value: {self.mode_var.get()}")
        self.ax.plot(self.years, uniform, linewidth=unif_strokewidth)
        self.ax.plot(self.years, gaussian, linewidth=gauss_strokewidth)
        self.canvas.draw()

    def get_comment(self):
        return self.comment_text.get("1.0", "end-1c")

    def get_to(self):
        return self.from_Var.get()

    def get_from(self):
        return self.from_Var.get()

    def get_around(self):
        return (self.to_Var.get() + self.from_Var.get())/2

    def get_giveortake(self):
        return (self.to_Var.get() - self.from_Var.get())/2

    def __init__(self, earliest_date: Tuple[int, int, int] = (0, 0, 0),
                 latest_date: Tuple[int, int, int] = (2023, 0, 0),
                 density_mode: Literal['probabillity',
                                       'plausibillity'] = 'plausibillity',
                 master: Misc = None,
                 cnf: Union[Dict[str, Any], None] = None,
                 *, background: str = ..., bd: t_pixel_value = ..., bg: str = ...,
                 border: t_pixel_value = ...,
                 borderwidth: t_pixel_value = ...,
                 class_: str = ...,
                 colormap: Union[Misc, Literal['new', '']] = ...,
                 container: bool = ..., cursor: Any = ..., height: t_pixel_value = ...,
                 highlightbackground: str = ..., highlightcolor: str = ...,
                 highlightthickness: t_pixel_value = ..., name: str = ..., padx: t_pixel_value = ...,
                 pady: t_pixel_value = ..., relief: Any = ..., takefocus: Any = ...,
                 visual: Union[str, Tuple[str, int]] = ..., width: t_pixel_value = 500
                 ) -> None:
        super().__init__(master, highlightthickness=1, highlightbackground="darkgrey"
                         # cnf,
                         # background=background, bd=bd, bg=bg, border=border,
                         # borderwidth=borderwidth, class_=class_, colormap=colormap,
                         # container=container, cursor=cursor, height=height, highlightbackground=highlightbackground,
                         # highlightcolor=highlightcolor, highlightthickness=highlightthickness,
                         # name=name, padx=padx, pady=pady, relief=relief, takefocus=takefocus, visual=visual, width=width
                         )
        self.is_plausibillity_mode = density_mode == 'plausibillity'
        self.earliest_date = earliest_date
        self.latest_date = latest_date
        self.years = np.arange(earliest_date[0], latest_date[0]+1)
        self.fig = Figure(figsize=(((width)/100), 1), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.curve_frame = Frame(self)
        self.curve_frame.pack()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.curve_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side="left", anchor="w")

        self.mode_var = tk.StringVar()
        self.mode_var.set("Uniform")

        self.from_Var = DoubleVar()  # left handle variable
        self.from_Var.trace_add('write', self.update_curve)
        self.to_Var = DoubleVar()  # delay=100)  # left handle variable
        self.to_Var.trace_add('write', self.update_curve)

        self.rs1 = RangeSliderH(self, [self.from_Var, self.to_Var], Width=width, Height=65, padX=60, min_val=self.earliest_date[0],
                                max_val=self.latest_date[0]+1, show_value=True)
        self.rs1.pack()

        self.comment_frame = tk.Frame(self)
        self.comment_frame.pack()
        self.comment_label = tk.Label(self.comment_frame, text="Comment:")
        self.comment_label.pack(side="top", anchor="w")
        self.comment_text = tk.Text(self.comment_frame, height=5, width=50)
        self.comment_text.pack(side="top", anchor="w", fill='x', expand=True)

        self.from_to_frame = Frame(self)
        self.from_to_frame.pack(anchor="w", fill='x', expand=True)
        self.update_btn = Button(
            self.from_to_frame, text="Set", command=self.toggle_form)
        self.update_btn.pack(side="left")
        Label(self.from_to_frame, text="From Year:").pack(side="left")
        self.txtbox_from = Entry(
            self.from_to_frame, textvariable=self.from_Var, width=10)
        self.txtbox_from.pack(side="left")
        self.txtbox_from.bind("<KeyRelease>", self.update_curve)

        Label(self.from_to_frame, text="To Year:").pack(side="left")
        self.txtbox_to = Entry(
            self.from_to_frame, textvariable=self.to_Var, width=10)
        self.txtbox_to.bind("<KeyRelease>", self.update_curve)

        self.txtbox_to.pack(side="left")

        self.mode_frame = tk.Frame(self)
        self.mode_frame.pack(anchor="w", fill='x', expand=True)

        self.mode_uniform_button = tk.Radiobutton(
            self.mode_frame, text="From - To", variable=self.mode_var, value="Uniform", command=self.update_curve)
        self.mode_uniform_button.pack(side="left", anchor="w")

        self.mode_gaussian_button = tk.Radiobutton(
            self.mode_frame, text="Give or Take", variable=self.mode_var, value="Gaussian", command=self.update_curve)
        self.mode_gaussian_button.pack(side="left", anchor="w")

        self.large_form = True
        self.show_small_form()
        self.update_curve()
