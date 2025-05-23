# File: nutrition_point.py
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime, timedelta
import json
import os
import csv


class NutritionPoint:
    def __init__(self, root):
        self.root = root
        self.root.title("Nutrition Point")
        self.root.geometry("500x500")
        self.root.configure(bg="#f2f2f2")

        tk.Label(self.root, text="Welcome to Nutrition Point!", font=("Helvetica", 28, "bold"), bg="#f2f2f2").pack(pady=20)
        tk.Label(self.root, text="Your One-Stop Solution for Health Management", font=("Helvetica", 16), bg="#f2f2f2").pack(pady=10)

        tk.Button(self.root, text="Sleep Tracker", font=("Helvetica", 14), bg="#84d4a4", fg="white", width=20, height=2,
                  command=self.open_sleep_tracker).pack(pady=10)
        tk.Button(self.root, text="Calorie Tracker", font=("Helvetica", 14), bg="#84a4d4", fg="white", width=20, height=2,
                  command=self.open_calorie_tracker).pack(pady=10)
        tk.Button(self.root, text="Recipe Database", font=("Helvetica", 14), bg="#d4a484", fg="white", width=20, height=2,
                  command=self.open_recipe_database).pack(pady=10)

        tk.Label(self.root, text="Track your sleep, calories, and meals effortlessly!", font=("Helvetica", 12, "italic"),
                 bg="#f2f2f2").pack(side="bottom", pady=20)

    def open_sleep_tracker(self):
        SleepTracker()

    def open_calorie_tracker(self):
        CalorieTracker()

    def open_recipe_database(self):
        RecipeDatabase()


class SleepTracker:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Sleep Tracker")
        self.window.geometry("400x400")

        self.sleep_data_file = "sleep_data.json"
        self.sleep_logs = self.load_sleep_data()

        tk.Label(self.window, text="Log your sleep time", font=("Helvetica", 16)).pack(pady=10)
        tk.Label(self.window, text="Sleep Time (HH:MM)").pack()
        self.sleep_time_entry = tk.Entry(self.window)
        self.sleep_time_entry.pack(pady=5)

        tk.Label(self.window, text="Wake-up Time (HH:MM)").pack()
        self.wake_time_entry = tk.Entry(self.window)
        self.wake_time_entry.pack(pady=5)

        tk.Button(self.window, text="Calculate Sleep Duration", command=self.calculate_duration).pack(pady=10)
        self.result_label = tk.Label(self.window, text="", font=("Helvetica", 12))
        self.result_label.pack(pady=10)

        tk.Button(self.window, text="Export to CSV", command=self.export_to_csv).pack(pady=10)

        self.analytics_label = tk.Label(self.window, text="Weekly Average Sleep: N/A", font=("Helvetica", 12))
        self.analytics_label.pack(pady=10)

        self.calculate_weekly_average()

    def load_sleep_data(self):
        if os.path.exists(self.sleep_data_file):
            with open(self.sleep_data_file, "r") as file:
                return json.load(file)
        return []

    def save_sleep_data(self):
        with open(self.sleep_data_file, "w") as file:
            json.dump(self.sleep_logs, file, indent=4)

    def calculate_duration(self):
        try:
            sleep_time = datetime.strptime(self.sleep_time_entry.get(), "%H:%M")
            wake_time = datetime.strptime(self.wake_time_entry.get(), "%H:%M")
            if wake_time < sleep_time:
                wake_time += timedelta(days=1)

            duration = wake_time - sleep_time
            self.result_label.config(text=f"Sleep Duration: {duration}")

            log = {"date": datetime.now().strftime("%Y-%m-%d"), "sleep_time": self.sleep_time_entry.get(),
                   "wake_time": self.wake_time_entry.get(), "duration": str(duration)}
            self.sleep_logs.append(log)
            self.save_sleep_data()
            self.calculate_weekly_average()
        except ValueError:
            messagebox.showerror("Error", "Enter valid time in HH:MM format")

    def calculate_weekly_average(self):
        total_minutes = 0
        count = 0
        for log in self.sleep_logs:
            duration = datetime.strptime(log["duration"], "%H:%M:%S") - datetime(1900, 1, 1)
            total_minutes += duration.seconds // 60
            count += 1
        if count > 0:
            avg_minutes = total_minutes // count
            avg_hours = avg_minutes // 60
            avg_minutes %= 60
            self.analytics_label.config(text=f"Weekly Average Sleep: {avg_hours}h {avg_minutes}m")
        else:
            self.analytics_label.config(text="Weekly Average Sleep: N/A")

    def export_to_csv(self):
        with open("sleep_data.csv", "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["date", "sleep_time", "wake_time", "duration"])
            writer.writeheader()
            writer.writerows(self.sleep_logs)
        messagebox.showinfo("Export", "Sleep data exported to sleep_data.csv")


class CalorieTracker:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Calorie Tracker")
        self.window.geometry("600x700")

        # Predefined Meal Chart
        self.meal_chart = [
            {"meal": "Grilled Chicken", "calories": 300},
            {"meal": "Boiled Egg", "calories": 78},
            {"meal": "Rice (1 cup)", "calories": 206},
            {"meal": "French Fries (medium)", "calories": 365},
            {"meal": "Tomato Soup", "calories": 150},
            {"meal": "Omelette", "calories": 154}
        ]

        # Export Meal Chart to CSV
        self.export_meal_chart()

        # Calorie Data Persistence
        self.calorie_data_file = "calories_data.json"
        self.calories_logs = self.load_calories_data()

        # Widgets
        tk.Label(self.window, text="Log your meals and calories", font=("Helvetica", 16)).pack(pady=10)

        # Combobox for Predefined Meals
        tk.Label(self.window, text="Select a Meal").pack()
        self.meal_combobox = ttk.Combobox(self.window, state="readonly", width=30)
        self.meal_combobox["values"] = [f'{meal["meal"]} - {meal["calories"]} cal' for meal in self.meal_chart]
        self.meal_combobox.pack(pady=5)
        tk.Button(self.window, text="Add Selected Meal", command=self.add_selected_meal).pack(pady=5)

        # Manual Entry
        tk.Label(self.window, text="Or Enter Meal Details").pack()
        tk.Label(self.window, text="Meal Name").pack()
        self.meal_entry = tk.Entry(self.window)
        self.meal_entry.pack(pady=5)

        tk.Label(self.window, text="Calories").pack()
        self.calorie_entry = tk.Entry(self.window)
        self.calorie_entry.pack(pady=5)

        tk.Button(self.window, text="Add Meal", command=self.add_meal).pack(pady=10)

        # Treeview to display meal logs
        self.tree = ttk.Treeview(self.window, columns=("Meal", "Calories"), show="headings")
        self.tree.heading("Meal", text="Meal")
        self.tree.heading("Calories", text="Calories")
        self.tree.pack(pady=20)

        # Buttons for editing and deleting meals
        tk.Button(self.window, text="Edit Selected Meal", command=self.edit_meal).pack(pady=5)
        tk.Button(self.window, text="Delete Selected Meal", command=self.delete_meal).pack(pady=5)

        # Calorie Goal
        tk.Label(self.window, text="Set a Daily Calorie Goal").pack(pady=10)
        self.calorie_goal_entry = tk.Entry(self.window)
        self.calorie_goal_entry.pack(pady=5)
        tk.Button(self.window, text="Set Goal", command=self.set_calorie_goal).pack(pady=5)
        self.goal_status_label = tk.Label(self.window, text="No goal set", font=("Helvetica", 12))
        self.goal_status_label.pack(pady=10)

        # Total Calories
        self.total_calories_label = tk.Label(self.window, text="Total Calories: 0", font=("Helvetica", 12))
        self.total_calories_label.pack(pady=10)

        # Export Button
        tk.Button(self.window, text="Export to CSV", command=self.export_to_csv).pack(pady=10)

        # Load Existing Data
        self.load_meal_logs()
        self.calculate_total_calories()

    def export_meal_chart(self):
        """Exports the predefined meal chart to a CSV file."""
        with open("meal_chart.csv", "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["meal", "calories"])
            writer.writeheader()
            writer.writerows(self.meal_chart)

    def load_calories_data(self):
        """Loads calorie data from a JSON file."""
        if os.path.exists(self.calorie_data_file):
            with open(self.calorie_data_file, "r") as file:
                return json.load(file)
        return []

    def save_calories_data(self):
        """Saves calorie data to a JSON file."""
        with open(self.calorie_data_file, "w") as file:
            json.dump(self.calories_logs, file, indent=4)

    def load_meal_logs(self):
        """Loads meal logs into the Treeview."""
        for log in self.calories_logs:
            self.tree.insert("", "end", values=(log["meal"], log["calories"]))

    def add_selected_meal(self):
        """Adds the selected meal from the combobox to the table."""
        selected = self.meal_combobox.get()
        if selected:
            meal, calories = selected.split(" - ")
            calories = int(calories.split()[0])  # Extract numeric calories
            self.add_meal_to_table({"meal": meal, "calories": calories})

    def add_meal(self):
        """Adds a meal manually entered by the user."""
        try:
            meal = self.meal_entry.get()
            calories = int(self.calorie_entry.get())
            self.add_meal_to_table({"meal": meal, "calories": calories})
        except ValueError:
            messagebox.showerror("Error", "Enter valid numeric calories")

    def add_meal_to_table(self, meal_data):
        """Adds a meal to the table and updates the data."""
        self.calories_logs.append(meal_data)
        self.save_calories_data()
        self.tree.insert("", "end", values=(meal_data["meal"], meal_data["calories"]))
        self.calculate_total_calories()

    def calculate_total_calories(self):
        """Calculates and displays the total calories."""
        total_calories = sum(log["calories"] for log in self.calories_logs)
        self.total_calories_label.config(text=f"Total Calories: {total_calories}")
        self.update_goal_status(total_calories)

    def update_goal_status(self, total_calories):
        """Updates the goal progress based on the total calories."""
        if hasattr(self, "calorie_goal"):
            remaining = self.calorie_goal - total_calories
            if remaining > 0:
                self.goal_status_label.config(text=f"{remaining} calories remaining to reach your goal")
            else:
                self.goal_status_label.config(text=f"Goal reached! You've exceeded by {-remaining} calories")

    def set_calorie_goal(self):
        """Sets a daily calorie goal."""
        try:
            self.calorie_goal = int(self.calorie_goal_entry.get())
            self.calculate_total_calories()
        except ValueError:
            messagebox.showerror("Error", "Enter a valid numeric calorie goal")

    def edit_meal(self):
        """Edits the selected meal in the table."""
        selected_item = self.tree.selection()
        if selected_item:
            meal_data = self.tree.item(selected_item, "values")
            meal_name = meal_data[0]
            calories = meal_data[1]

            # Populate entry fields with current values
            self.meal_entry.delete(0, tk.END)
            self.meal_entry.insert(0, meal_name)
            self.calorie_entry.delete(0, tk.END)
            self.calorie_entry.insert(0, calories)

            # Delete the selected meal
            self.delete_meal()

    def delete_meal(self):
        """Deletes the selected meal from the table."""
        selected_item = self.tree.selection()
        if selected_item:
            meal_data = self.tree.item(selected_item, "values")
            meal_name = meal_data[0]
            self.tree.delete(selected_item)

            # Remove from logs
            self.calories_logs = [log for log in self.calories_logs if log["meal"] != meal_name]
            self.save_calories_data()
            self.calculate_total_calories()

    def export_to_csv(self):
        """Exports the calorie data to a CSV file."""
        with open("calories_data.csv", "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["meal", "calories"])
            writer.writeheader()
            writer.writerows(self.calories_logs)
        messagebox.showinfo("Export", "Calorie data exported to calories_data.csv")



class RecipeDatabase:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Recipe Database")
        self.window.geometry("400x400")

        self.recipes = {
            "chicken": ["Grilled Chicken", "Chicken Curry", "Chicken Salad"],
            "potato": ["Mashed Potato", "French Fries", "Potato Soup"],
            "egg": ["Omelette", "Boiled Egg", "Egg Curry"],
            "rice": ["Fried Rice", "Rice Pudding", "Rice Soup"],
            "tomato": ["Tomato Soup", "Tomato Salad", "Tomato Pasta"]
        }

        tk.Label(self.window, text="Search Recipes by Ingredient", font=("Helvetica", 16)).pack(pady=10)
        self.ingredient_entry = tk.Entry(self.window)
        self.ingredient_entry.pack(pady=5)
        tk.Button(self.window, text="Search", command=self.search_recipes).pack(pady=10)

        self.tree = ttk.Treeview(self.window, columns=("Recipe"), show="headings")
        self.tree.heading("Recipe", text="Recipe")
        self.tree.pack(pady=20)

    def search_recipes(self):
        ingredient = self.ingredient_entry.get().lower()
        recipes = self.recipes.get(ingredient, [])
        for item in self.tree.get_children():
            self.tree.delete(item)
        for recipe in recipes:
            self.tree.insert("", "end", values=(recipe))


if __name__ == "__main__":
    root = tk.Tk()
    app = NutritionPoint(root)
    root.mainloop()
