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

    def update_from_fridges(self, fridges, selected_index: int = 0):
        self.figure.clf()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor("#2e2e2e")
        self.canvas.draw()

        if not fridges:
            self.tasks = []
            return

        if 1 <= selected_index <= len(fridges):
            idx = selected_index - 1
        elif 0 <= selected_index < len(fridges):
            idx = selected_index
        else:
            idx = 0

        item = fridges[idx]

        fridge_id = None
        if isinstance(item, dict):
            fridge_id = item.get('id')
            if fridge_id is None:
                body = item.get('body')
                if isinstance(body, dict):
                    fridge_id = body.get('id')
        else:
            fridge_id = getattr(item, 'body_id', None) or getattr(item, 'id', None)

        if fridge_id is None:
            fridge_id = idx + 1

        tasks = []
        #variable for tracking time for components
        x=0
        y=0
        #variables to define time for each machine
        m1=4
        m2=4
        m3=3
        m4=4
        m5=3
        m6=7
        m7=4
        m8=5
        m9=3
        m10=6
        m11=5
        for i in range(11):
            idx = i + 1
            #cover
            if idx == 1:
                x=1 
                s, e = x, x+m4
                x=x+m4

            elif idx == 2:
                x=x+0.5
                s, e = x, x+m2
                x=x+m2
                if x>y:
                    y=x
                    
            #doors
            elif idx == 3:
                x=1
                s, e = x, x+m3
                x=x+m3

            elif idx == 4:
                x=x+0.5
                s, e = x, x+m4
                x=x+m4

            elif idx == 5:
                x=x+0.5
                front_panel = False
                if isinstance(item, dict):
                    front_panel = item.get('body', {}).get('doors', {}).get('front_panel', False)
                else:
                    front_panel = getattr(getattr(item, 'doors', None), 'front_panel', False)
                if front_panel == True:
                    s, e = x, x+m5
                    x=x+m5
                else:
                    s, e = x, x
                if x>y:
                    y=x

            #shelves
            elif idx == 6:
                adjustable = False
                if isinstance(item, dict):
                    adjustable = item.get('body', {}).get('shelves', {}).get('adjustable_height', False)
                else:
                    adjustable = getattr(getattr(item, 'shelves', None), 'adjustable', False)
                if adjustable == True:
                    x=m6+1.5
                else:
                    x=m6
                s, e = 1, x+0.5
                x=x+0.5
                if x>y:
                    y=x

            #Cooling system
            elif idx == 7:
                x=1
                s, e = x, x+m4
                x=x+m4

            elif idx == 8:
                x=x+0.5
                s, e = x, x+m5
                x=x+m5
            
            elif idx == 9:
                x=x+0.5
                s, e = x, x+m9
                x=x+m9
                if x>y:
                    y=x
            
            #Lighting
            elif idx == 10:
                x=1
                s, e = x, x+m10
                x=x+m10
                if x>y:
                    y=x
            
            #Assembly
            else:
                y=y+0.5
                s, e = y, y+m11

            tasks.append({"task": f"M{idx}", "start": s, "end": e})
        self.tasks = tasks
        self.plot_gantt()

    def clear_chart(self):
        self.tasks = []
        self.figure.clf()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor("#2e2e2e")
        ax.set_title("")
        ax.set_xlabel("")
        ax.set_ylabel("")
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
        self.canvas.draw()

    def plot_gantt(self):
        self.figure.clf()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor("#2e2e2e")
        if not self.tasks:
            ax.set_title("")
            ax.set_xlabel("")
            ax.set_ylabel("")
            ax.set_xticks([])
            ax.set_yticks([])
            for spine in ax.spines.values():
                spine.set_visible(False)
            try:
                ax.set_xlim(left=0, right=1)
            except Exception:
                pass
            self.canvas.draw()
            return

        y_labels = [t["task"] for t in self.tasks]
        start_times = [t["start"] for t in self.tasks]
        durations = [t["end"] - t["start"] for t in self.tasks]

        ax.barh(y_labels, durations, left=start_times, color="limegreen", zorder=3)
        try:
            max_end = max(t["end"] for t in self.tasks)
            ax.set_xlim(left=0, right=max_end + 1)
        except Exception:
            try:
                ax.set_xlim(left=0)
            except Exception:
                pass
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
