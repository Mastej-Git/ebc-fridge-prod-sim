from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class GanttChart(QWidget):
    def __init__(self, tasks=None):
        super().__init__()
        self.tasks = tasks or []

        layout = QVBoxLayout(self)

        self.figure = Figure(figsize=(6, 4), facecolor="#2e2e2e")
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.plot_gantt()

    def plot_gantt(self):
        ax = self.figure.add_subplot(111)
        ax.clear()
        ax.set_facecolor("#2e2e2e")

        if not self.tasks:
            ax.text(0.5, 0.5, "No data to plot",
                    ha='center', va='center', transform=ax.transAxes, color="white")
            self.canvas.draw()
            return

        y_labels = [t["task"] for t in self.tasks]
        start_times = [t["start"] for t in self.tasks]
        durations = [t["end"] - t["start"] for t in self.tasks]

        ax.barh(y_labels, durations, left=start_times, color="#87CEFA")
        ax.set_xlabel("Time", color="white")
        ax.set_ylabel("Task", color="white")
        ax.set_title("Gantt Chart", color="white")

        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        for spine in ax.spines.values():
            spine.set_color("white")

        self.canvas.draw()
