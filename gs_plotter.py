__author__ = 'galarius'

import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

def plot_container(data):
    plt.plot(data)
    plt.show()

def plot_containers_substruction(original, modified):
    plt.plot(modified - original)
    plt.show()

def save_plot(data):
    figure = Figure()
    canvas = FigureCanvas(figure)
    axes = figure.add_subplot(1, 1, 1, axisbg='black')
    axes.plot([i for i in range(len(data))], data, 'ro')
    canvas.print_figure('plot.png')

def save_plots(original, modified, separated=False, path='plot.png'):
    figure = Figure()
    figure.set_size_inches(18.5, 10.5)
    canvas = FigureCanvas(figure)
    axes = figure.add_subplot(211, axisbg='white')
    axes.plot(original)
    if separated:
        axes = figure.add_subplot(212, axisbg='white')
        path = "sep_" + path
    axes.plot(modified)
    canvas.print_figure(path, dpi=100)
