import tkinter as tk
from tkinter import messagebox

# Configuration
WORK_MINUTES = 25
SHORT_BREAK_MINUTES = 5
LONG_BREAK_MINUTES = 15
CYCLES_BEFORE_LONG_BREAK = 4

class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("400x400")
        self.root.config(bg="#FFF9E3")  # Background color for a softer look
        
        self.sessions_completed = 0
        self.timer_running = False
        self.timer_paused = False
        self.time_remaining = WORK_MINUTES * 60

        # Title
        self.title_label = tk.Label(self.root, text="Pomodoro Timer", font=("Arial", 24, "bold"), bg="#FFF9E3", fg="#333")
        self.title_label.pack(pady=20)

        # Timer display
        self.time_left = tk.StringVar()
        self.time_left.set(f"{WORK_MINUTES:02}:00")
        self.timer_label = tk.Label(self.root, textvariable=self.time_left, font=("Arial", 48), bg="#FFF9E3", fg="#333")
        self.timer_label.pack(pady=20)

        # Start button
        self.start_button = tk.Button(self.root, text="Start Focus", command=self.start_focus, font=("Arial", 14), bg="#4CAF50", fg="white", width=12)
        self.start_button.pack(pady=10)

        # Pause/Resume button
        self.pause_button = tk.Button(self.root, text="Pause", state=tk.DISABLED, command=self.toggle_pause, font=("Arial", 14), bg="#F44336", fg="white", width=12)
        self.pause_button.pack(pady=10)

        # Reset button
        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset_timer, font=("Arial", 14), bg="#757575", fg="white", width=12)
        self.reset_button.pack(pady=10)

        # Break button (for breaks after work sessions)
        self.break_button = tk.Button(self.root, text="Start Break", state=tk.DISABLED, command=self.start_break, font=("Arial", 14), bg="#FF9800", fg="white", width=12)
        self.break_button.pack(pady=10)

    def start_focus(self):
        """Start a focus session."""
        if not self.timer_running and not self.timer_paused:
            self.sessions_completed += 1
            self.timer_running = True
            self.update_timer(WORK_MINUTES * 60)
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL, text="Pause")
            self.break_button.config(state=tk.DISABLED)

    def start_break(self):
        """Start a short or long break depending on the session cycle."""
        if not self.timer_running:
            if self.sessions_completed % CYCLES_BEFORE_LONG_BREAK == 0:
                self.update_timer(LONG_BREAK_MINUTES * 60)
                messagebox.showinfo("Long Break", "Time for a 15-minute long break!")
            else:
                self.update_timer(SHORT_BREAK_MINUTES * 60)
                messagebox.showinfo("Short Break", "Time for a 5-minute short break!")
            self.break_button.config(state=tk.DISABLED)

    def update_timer(self, remaining_seconds):
        """Update the timer display and countdown."""
        self.time_remaining = remaining_seconds
        if remaining_seconds > 0 and self.timer_running:
            mins, secs = divmod(remaining_seconds, 60)
            self.time_left.set(f"{mins:02}:{secs:02}")
            self.root.after(1000, self.update_timer, remaining_seconds - 1)
        elif remaining_seconds == 0:
            self.timer_running = False
            self.pause_button.config(state=tk.DISABLED)
            self.break_button.config(state=tk.NORMAL)
            messagebox.showinfo("Timer Done", "The session is over!")

    def toggle_pause(self):
        """Pause or resume the timer."""
        if self.timer_running:
            # Pause the timer
            self.timer_running = False
            self.pause_button.config(text="Resume")
        else:
            # Resume the timer
            self.timer_running = True
            self.pause_button.config(text="Pause")
            self.update_timer(self.time_remaining)

    def reset_timer(self):
        """Reset the timer to the starting work period."""
        self.timer_running = False
        self.timer_paused = False
        self.time_remaining = WORK_MINUTES * 60
        self.time_left.set(f"{WORK_MINUTES:02}:00")
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED, text="Pause")
        self.break_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()
