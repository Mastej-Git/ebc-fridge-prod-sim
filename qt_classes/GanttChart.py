from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class GanttUpdateThread(QThread):
    time_updated = pyqtSignal(float)
    finished_signal = pyqtSignal()

    def __init__(self, max_time, speed=1.0, interval=50, parent=None):
        super().__init__(parent)
        self.max_time = max_time
        self.speed = speed
        self.interval = interval
        self.current_time = 0.0
        self._running = False
        self._paused = False

    def run(self):
        self._running = True
        while self._running and self.current_time < self.max_time:
            if not self._paused:
                self.current_time += self.speed * (self.interval / 1000.0)
                self.time_updated.emit(self.current_time)
            self.msleep(self.interval)
        self.finished_signal.emit()

    def pause(self):
        self._paused = True

    def resume(self):
        self._paused = False

    def stop(self):
        self._running = False
        self.wait()

    def reset(self):
        self.current_time = 0.0

    def set_speed(self, speed):
        self.speed = speed


class GanttChart(QWidget):
    def __init__(self, tasks=None):
        super().__init__()
        self.tasks = tasks or []
        self.current_time = 0.0
        self.max_time = 1.0
        self.update_thread = None

        layout = QVBoxLayout(self)

        self.figure = Figure(figsize=(6, 4), facecolor="#2e2e2e")
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.plot_gantt()

    def start_animation(self, speed=1.0):
        if self.update_thread is not None:
            self.stop_animation()
        
        if self.tasks:
            self.max_time = max(t["end"] for t in self.tasks) + 1
        
        self.current_time = 0.0
        self.update_thread = GanttUpdateThread(self.max_time, speed=speed, interval=50)
        self.update_thread.time_updated.connect(self.on_time_update)
        self.update_thread.finished_signal.connect(self.on_animation_finished)
        self.update_thread.start()

    def stop_animation(self):
        if self.update_thread is not None:
            self.update_thread.stop()
            self.update_thread = None

    def pause_animation(self):
        if self.update_thread is not None:
            self.update_thread.pause()

    def resume_animation(self):
        if self.update_thread is not None:
            self.update_thread.resume()

    def reset_animation(self):
        self.current_time = 0.0
        if self.update_thread is not None:
            self.update_thread.reset()
        self.plot_gantt()

    def set_animation_speed(self, speed):
        if self.update_thread is not None:
            self.update_thread.set_speed(speed)

    def on_time_update(self, time_value):
        self.current_time = time_value
        self.plot_gantt()

    def on_animation_finished(self):
        pass

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
        x=0
        y=0
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

            elif idx == 10:
                x=1
                s, e = x, x+m10
                x=x+m10
                if x>y:
                    y=x

            else:
                y=y+0.5
                s, e = y, y+m11

            tasks.append({"task": f"M{idx}", "start": s, "end": e})
        self.tasks = tasks
        self.max_time = max(t["end"] for t in self.tasks) + 1 if self.tasks else 1.0
        self.current_time = 0.0
        self.plot_gantt()
        self.start_animation(speed=1.0)

    def clear_chart(self):
        self.stop_animation()
        self.tasks = []
        self.current_time = 0.0
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
        
        for i, task in enumerate(self.tasks):
            start = task["start"]
            end = task["end"]
            duration = end - start
            
            if duration <= 0:
                continue
            
            if self.current_time >= end:
                ax.barh(y_labels[i], duration, left=start, color="limegreen", zorder=3)
            elif self.current_time <= start:
                ax.barh(y_labels[i], duration, left=start, color="#555555", zorder=3)
            else:
                completed = self.current_time - start
                remaining = end - self.current_time
                ax.barh(y_labels[i], completed, left=start, color="limegreen", zorder=3)
                ax.barh(y_labels[i], remaining, left=self.current_time, color="#555555", zorder=3)

        ax.axvline(x=self.current_time, color="#ff4444", linewidth=2, linestyle='-', zorder=5, label='Current Time')

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
        ax.set_title(f"Gantt Chart (t = {self.current_time:.1f})", color="#00ffff")

        ax.invert_yaxis()
        ax.grid(True, zorder=1, color="#00ffff", alpha=0.3, linewidth=1.5)

        ax.tick_params(axis='x', colors='#00ffff')
        ax.tick_params(axis='y', colors='#00ffff')
        for spine in ax.spines.values():
            spine.set_color("#00ffff")

        self.canvas.draw()
