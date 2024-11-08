import tkinter as tk
from tkinter import messagebox
import requests

# Constants for OpenWeatherMap API
API_KEY = "YOUR_API_KEY_HERE"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Window configuration
        self.title("Weather App")
        self.geometry("400x500")
        self.configure(bg="#ADD8E6")

        # Search bar
        self.city_entry = tk.Entry(self, font=("Arial", 16), justify="center")
        self.city_entry.pack(pady=20)
        self.city_entry.insert(0, "Enter city name")

        # Search and refresh buttons
        self.search_button = tk.Button(self, text="Search", command=self.get_weather, font=("Arial", 14), bg="#3498db", fg="white")
        self.search_button.pack(pady=10)

        self.refresh_button = tk.Button(self, text="Refresh", command=self.clear_results, font=("Arial", 14), bg="#27ae60", fg="white")
        self.refresh_button.pack(pady=5)

        # Results frame for displaying weather data
        self.result_frame = tk.Frame(self, bg="#ADD8E6")
        self.result_frame.pack(pady=20)

        # Labels for weather data
        self.weather_label = tk.Label(self.result_frame, font=("Arial", 16), bg="#ADD8E6")
        self.weather_label.pack(pady=10)
        self.temp_label = tk.Label(self.result_frame, font=("Arial", 14), bg="#ADD8E6")
        self.temp_label.pack(pady=5)
        self.humidity_label = tk.Label(self.result_frame, font=("Arial", 14), bg="#ADD8E6")
        self.humidity_label.pack(pady=5)
        self.description_label = tk.Label(self.result_frame, font=("Arial", 14), bg="#ADD8E6")
        self.description_label.pack(pady=5)

    def get_weather(self):
        """Fetch and display weather data for the specified city."""
        city_name = self.city_entry.get().strip()
        if not city_name:
            messagebox.showwarning("Warning", "Please enter a city name.")
            return

        try:
            # API request
            params = {"q": city_name, "appid": API_KEY, "units": "metric"}
            response = requests.get(BASE_URL, params=params)
            weather_data = response.json()

            if weather_data["cod"] == 200:
                self.display_weather(weather_data)
            else:
                messagebox.showerror("Error", f"City {city_name} not found.")
        except requests.RequestException as e:
            messagebox.showerror("Error", "Failed to fetch weather data.")

    def display_weather(self, data):
        """Update labels with fetched weather data."""
        city = data["name"]
        country = data["sys"]["country"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"]

        # Set label text
        self.weather_label.config(text=f"Weather in {city}, {country}")
        self.temp_label.config(text=f"Temperature: {temp}°C")
        self.humidity_label.config(text=f"Humidity: {humidity}%")
        self.description_label.config(text=f"Description: {description.capitalize()}")

    def clear_results(self):
        """Clear the result labels."""
        self.city_entry.delete(0, tk.END)
        self.weather_label.config(text="")
        self.temp_label.config(text="")
        self.humidity_label.config(text="")
        self.description_label.config(text="")

if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()
