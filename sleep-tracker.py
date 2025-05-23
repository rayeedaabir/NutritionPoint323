import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import sqlite3
import matplotlib.pyplot as plt

# Initialize the database and preload data
def init_db():
    conn = sqlite3.connect("sleep_data.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS SleepLog (
            id INTEGER PRIMARY KEY,
            date TEXT,
            sleep_time TEXT,
            wake_time TEXT,
            duration REAL
        )
    """)
    # Preload data (if the table is empty)
    c.execute("SELECT COUNT(*) FROM SleepLog")
    if c.fetchone()[0] == 0:
        sample_data = [
            ("2024-12-20", "22:00", "06:00", 8),
            ("2024-12-21", "23:30", "07:30", 8),
            ("2024-12-22", "00:00", "08:00", 8),
        ]
        c.executemany("INSERT INTO SleepLog (date, sleep_time, wake_time, duration) VALUES (?, ?, ?, ?)", sample_data)
    conn.commit()
    conn.close()

# Add sleep data to the database
def add_entry(sleep_time, wake_time):
    try:
        sleep_dt = datetime.strptime(sleep_time, "%H:%M")
        wake_dt = datetime.strptime(wake_time, "%H:%M")
        if wake_dt < sleep_dt:  # Handle crossing midnight
            wake_dt += timedelta(days=1)
        duration = (wake_dt - sleep_dt).seconds / 3600  # Duration in hours

        conn = sqlite3.connect("sleep_data.db")
        c = conn.cursor()
        c.execute("INSERT INTO SleepLog (date, sleep_time, wake_time, duration) VALUES (?, ?, ?, ?)",
                  (datetime.now().strftime("%Y-%m-%d"), sleep_time, wake_time, duration))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"Entry added: {duration:.2f} hours")
    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {e}")

# Fetch sleep data for graphing
def fetch_data():
    conn = sqlite3.connect("sleep_data.db")
    c = conn.cursor()
    c.execute("SELECT date, duration FROM SleepLog ORDER BY date")
    data = c.fetchall()
    conn.close()
    return data

# Plot sleep data
def show_graph():
    data = fetch_data()
    if not data:
        messagebox.showinfo("No Data", "No sleep data available to display.")
        return

    dates = [d[0] for d in data]
    durations = [d[1] for d in data]

    plt.figure(figsize=(8, 4))
    plt.plot(dates, durations, marker='o', linestyle='-', color='b')
    plt.title("Sleep Duration Over Time")
    plt.xlabel("Date")
    plt.ylabel("Duration (hours)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Main application window
def create_gui():
    root = tk.Tk()
    root.title("Sleep Tracker")

    tk.Label(root, text="Sleep Time (HH:MM):").grid(row=0, column=0)
    sleep_time_entry = tk.Entry(root)
    sleep_time_entry.grid(row=0, column=1)

    tk.Label(root, text="Wake Time (HH:MM):").grid(row=1, column=0)
    wake_time_entry = tk.Entry(root)
    wake_time_entry.grid(row=1, column=1)

    def handle_add_entry():
        sleep_time = sleep_time_entry.get()
        wake_time = wake_time_entry.get()
        add_entry(sleep_time, wake_time)

    add_button = tk.Button(root, text="Add Entry", command=handle_add_entry)
    add_button.grid(row=2, column=0, columnspan=2)

    graph_button = tk.Button(root, text="Show Graph", command=show_graph)
    graph_button.grid(row=3, column=0, columnspan=2)

    root.mainloop()

if __name__ == "__main__":
    init_db()
    create_gui()
