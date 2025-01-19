import matplotlib
import matplotlib.pyplot as plt
import flet as ft
from flet.matplotlib_chart import MatplotlibChart


matplotlib.use("svg")


class DatasetPlot(MatplotlibChart):

    def __init__(self, dataset, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.dataset = dataset
        self.transparent = True
        self.figure, self.axes = plt.subplots(layout="constrained")

        self.recreate_plot()


    def recreate_plot(self):
        time_points, magnitudes = self.dataset.read()
        self.axes.plot(time_points, magnitudes)


    def handle_add_record(self):
        self.recreate_plot()
        self.update()
