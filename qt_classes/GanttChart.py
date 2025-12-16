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
                    ha='center', va='center', transform=ax.transAxes, color="#00ffff")
            self.canvas.draw()
            return

        y_labels = [t["task"] for t in self.tasks]
        start_times = [t["start"] for t in self.tasks]
        durations = [t["end"] - t["start"] for t in self.tasks]

        ax.barh(y_labels, durations, left=start_times, color="white", zorder=3)
        ax.set_xlabel("Time", color="#00ffff")
        ax.set_ylabel("Task", color="#00ffff")
        ax.set_title("Gantt Chart", color="#00ffff")

        ax.invert_yaxis()
        ax.grid(True, zorder=1, color="#00ffff", alpha=0.3, linewidth=1.5)

        ax.tick_params(axis='x', colors='#00ffff')
        ax.tick_params(axis='y', colors='#00ffff')
        for spine in ax.spines.values():
            spine.set_color("#00ffff")

        self.canvas.draw()
