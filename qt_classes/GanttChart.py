from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import colorsys


class GanttUpdateThread(QThread):
    time_updated = pyqtSignal(float)

    def __init__(self, speed=1.0, interval=100, parent=None):
        super().__init__(parent)
        self.speed = speed
        self.interval = interval
        self.current_time = 0.0
        self._running = False
        self._paused = False

    def run(self):
        self._running = True
        while self._running:
            if not self._paused:
                self.current_time += self.speed * (self.interval / 1000.0)
                self.time_updated.emit(self.current_time)
            self.msleep(self.interval)

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
        self.fridge_tasks = []
        self.current_time = 0.0
        self.view_window = 30.0
        self.update_thread = None
        self.fridge_colors = {}
        self.color_index = 0
        self.task_gap = 1.0
        self.machine_available_time = {f"M{i}": 0.0 for i in range(1, 12)}

        layout = QVBoxLayout(self)

        self.figure = Figure(figsize=(6, 4), facecolor="#2e2e2e")
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.plot_gantt()

    def _generate_color(self, fridge_id):
        if fridge_id in self.fridge_colors:
            return self.fridge_colors[fridge_id]
        
        hue = (self.color_index * 0.618033988749895) % 1.0
        saturation = 0.7
        value = 0.9
        rgb = colorsys.hsv_to_rgb(hue, saturation, value)
        color = '#{:02x}{:02x}{:02x}'.format(int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
        self.fridge_colors[fridge_id] = color
        self.color_index += 1
        return color

    def start_animation(self, speed=1.0):
        if self.update_thread is not None:
            return
        
        self.update_thread = GanttUpdateThread(speed=speed, interval=100)
        self.update_thread.time_updated.connect(self.on_time_update)
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
        self.fridge_tasks = []
        self.fridge_colors = {}
        self.color_index = 0
        self.machine_available_time = {f"M{i}": 0.0 for i in range(1, 12)}
        self.plot_gantt()

    def set_animation_speed(self, speed):
        if self.update_thread is not None:
            self.update_thread.set_speed(speed)

    def on_time_update(self, time_value):
        self.current_time = time_value
        self.plot_gantt()

    def _calculate_tasks_for_fridge(self, item, base_time):
        raw_tasks = []
        x = 0
        y = 0
        m1 = 4
        m2 = 4
        m3 = 3
        m4 = 4
        m5 = 3
        m6 = 7
        m7 = 4
        m8 = 5
        m9 = 3
        m10 = 6
        m11 = 5

        for i in range(11):
            idx = i + 1
            if idx == 1:
                x = 1
                s, e = x, x + m4
                x = x + m4

            elif idx == 2:
                x = x + 0.5
                s, e = x, x + m2
                x = x + m2
                if x > y:
                    y = x

            elif idx == 3:
                x = 1
                s, e = x, x + m3
                x = x + m3

            elif idx == 4:
                x = x + 0.5
                s, e = x, x + m4
                x = x + m4

            elif idx == 5:
                x = x + 0.5
                front_panel = False
                if isinstance(item, dict):
                    front_panel = item.get('body', {}).get('doors', {}).get('front_panel', False)
                else:
                    front_panel = getattr(getattr(item, 'doors', None), 'front_panel', False)
                if front_panel is True:
                    s, e = x, x + m5
                    x = x + m5
                else:
                    s, e = x, x
                if x > y:
                    y = x

            elif idx == 6:
                adjustable = False
                if isinstance(item, dict):
                    adjustable = item.get('body', {}).get('shelves', {}).get('adjustable_height', False)
                else:
                    adjustable = getattr(getattr(item, 'shelves', None), 'adjustable', False)
                if adjustable is True:
                    x = m6 + 1.5
                else:
                    x = m6
                s, e = 1, x + 0.5
                x = x + 0.5
                if x > y:
                    y = x

            elif idx == 7:
                x = 1
                s, e = x, x + m4
                x = x + m4

            elif idx == 8:
                x = x + 0.5
                s, e = x, x + m5
                x = x + m5

            elif idx == 9:
                x = x + 0.5
                s, e = x, x + m9
                x = x + m9
                if x > y:
                    y = x

            elif idx == 10:
                x = 1
                s, e = x, x + m10
                x = x + m10
                if x > y:
                    y = x

            else:
                y = y + 0.5
                s, e = y, y + m11

            raw_tasks.append({
                "machine": f"M{idx}",
                "relative_start": s,
                "relative_end": e,
                "duration": e - s
            })

        scheduled_tasks = []
        for task in raw_tasks:
            machine = task["machine"]
            duration = task["duration"]
            
            if duration <= 0:
                scheduled_tasks.append({
                    "machine": machine,
                    "start": base_time + task["relative_start"],
                    "end": base_time + task["relative_end"]
                })
                continue

            earliest_start = base_time + task["relative_start"]
            machine_ready = self.machine_available_time.get(machine, 0.0)
            actual_start = max(earliest_start, machine_ready + self.task_gap)
            actual_end = actual_start + duration

            self.machine_available_time[machine] = actual_end

            scheduled_tasks.append({
                "machine": machine,
                "start": actual_start,
                "end": actual_end
            })

        return scheduled_tasks

    def add_fridge(self, fridge_item, fridge_id=None):
        if fridge_id is None:
            if isinstance(fridge_item, dict):
                fridge_id = fridge_item.get('id')
                if fridge_id is None:
                    body = fridge_item.get('body')
                    if isinstance(body, dict):
                        fridge_id = body.get('id')
            else:
                fridge_id = getattr(fridge_item, 'id', None) or getattr(fridge_item, 'id', None)

        if fridge_id is None:
            fridge_id = len(self.fridge_tasks) + 1

        base_time = self.current_time

        color = self._generate_color(fridge_id)
        tasks = self._calculate_tasks_for_fridge(fridge_item, base_time)

        self.fridge_tasks.append({
            "fridge_id": fridge_id,
            "color": color,
            "tasks": tasks,
            "start_time": base_time
        })

        if self.update_thread is None:
            self.start_animation(speed=1.0)

        self.plot_gantt()

    def update_from_fridges(self, fridges, selected_index: int = 0):
        if not fridges:
            return

        if 1 <= selected_index <= len(fridges):
            idx = selected_index - 1
        elif 0 <= selected_index < len(fridges):
            idx = selected_index
        else:
            idx = 0

        item = fridges[idx]
        self.add_fridge(item)

    def clear_chart(self):
        self.stop_animation()
        self.fridge_tasks = []
        self.current_time = 0.0
        self.fridge_colors = {}
        self.color_index = 0
        self.machine_available_time = {f"M{i}": 0.0 for i in range(1, 12)}
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
        self.canvas.draw_idle()

    def plot_gantt(self):
        self.figure.clf()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor("#2e2e2e")

        if not self.fridge_tasks:
            ax.set_title("")
            ax.set_xlabel("")
            ax.set_ylabel("")
            ax.set_xticks([])
            ax.set_yticks([])
            for spine in ax.spines.values():
                spine.set_visible(False)
            self.canvas.draw_idle()
            return

        machines = [f"M{i}" for i in range(1, 12)]
        machine_positions = {m: i for i, m in enumerate(machines)}

        view_left = self.current_time - self.view_window
        view_right = self.current_time

        active_fridges = []
        for fridge_data in self.fridge_tasks:
            fridge_end = max(t["end"] for t in fridge_data["tasks"])
            if fridge_end >= view_left:
                active_fridges.append(fridge_data)

        self.fridge_tasks = active_fridges

        for fridge_data in self.fridge_tasks:
            color = fridge_data["color"]
            for task in fridge_data["tasks"]:
                start = task["start"]
                end = task["end"]
                duration = end - start

                if duration <= 0:
                    continue

                if end < view_left or start > view_right:
                    continue

                visible_start = max(start, view_left)
                visible_end = min(end, view_right)
                visible_duration = visible_end - visible_start

                if visible_duration <= 0:
                    continue

                machine = task["machine"]
                y_pos = machine_positions.get(machine, 0)

                if self.current_time >= end:
                    bar_color = color
                elif self.current_time <= start:
                    bar_color = "#555555"
                else:
                    completed_end = min(self.current_time, visible_end)
                    completed_start = max(visible_start, start)
                    if completed_end > completed_start:
                        ax.barh(y_pos, completed_end - completed_start, left=completed_start,
                               color=color, zorder=3, height=0.6)
                    
                    pending_start = max(self.current_time, visible_start)
                    pending_end = visible_end
                    if pending_end > pending_start:
                        ax.barh(y_pos, pending_end - pending_start, left=pending_start,
                               color="#555555", zorder=3, height=0.6)
                    continue

                ax.barh(y_pos, visible_duration, left=visible_start, color=bar_color, zorder=3, height=0.6)

        ax.axvline(x=self.current_time, color="#ff4444", linewidth=2, linestyle='-', zorder=5)

        ax.set_xlim(left=view_left, right=view_right)
        ax.set_ylim(-0.5, len(machines) - 0.5)

        ax.set_yticks(range(len(machines)))
        ax.set_yticklabels(machines)

        ax.set_xlabel("Time", color="#00ffff")
        ax.set_ylabel("Machine", color="#00ffff")
        ax.set_title(f"Production Timeline (t = {self.current_time:.1f})", color="#00ffff")

        ax.invert_yaxis()
        ax.grid(True, zorder=1, color="#00ffff", alpha=0.3, linewidth=1.5)

        ax.tick_params(axis='x', colors='#00ffff')
        ax.tick_params(axis='y', colors='#00ffff')
        for spine in ax.spines.values():
            spine.set_color("#00ffff")

        self.canvas.draw_idle()
