import tkinter as tk
from tkinter import ttk, messagebox

class CurrencyConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Main window setup
        self.title("Currency Converter")
        self.geometry("500x400")
        self.config(bg="#f0f4f7")
        self.resizable(False, False)

        # Title label
        title = tk.Label(self, text="Currency Converter", font=("Arial", 24, "bold"), fg="#004aad", bg="#f0f4f7")
        title.pack(pady=20)

        # Conversion frame
        convert_frame = tk.Frame(self, bg="#ffffff", bd=2, relief="solid")
        convert_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Input Amount
        input_label = tk.Label(convert_frame, text="Amount:", font=("Arial", 14), bg="#ffffff")
        input_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.amount_entry = tk.Entry(convert_frame, font=("Arial", 14), width=15, relief="flat", bd=2)
        self.amount_entry.grid(row=0, column=1, padx=10, pady=10)

        # From Currency
        from_label = tk.Label(convert_frame, text="From:", font=("Arial", 14), bg="#ffffff")
        from_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.from_currency = ttk.Combobox(convert_frame, font=("Arial", 14), values=list(self.get_currency_list()), state="readonly", width=10)
        self.from_currency.grid(row=1, column=1, padx=10, pady=10)
        self.from_currency.current(0)

        # To Currency
        to_label = tk.Label(convert_frame, text="To:", font=("Arial", 14), bg="#ffffff")
        to_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.to_currency = ttk.Combobox(convert_frame, font=("Arial", 14), values=list(self.get_currency_list()), state="readonly", width=10)
        self.to_currency.grid(row=2, column=1, padx=10, pady=10)
        self.to_currency.current(1)

        # Convert Button
        convert_button = tk.Button(self, text="Convert", font=("Arial", 16, "bold"), bg="#004aad", fg="white", command=self.convert_currency)
        convert_button.pack(pady=20)

        # Output Label
        self.result_label = tk.Label(self, text="Converted Amount: -", font=("Arial", 16), fg="#333333", bg="#f0f4f7")
        self.result_label.pack(pady=10)

    def get_currency_list(self):
        # Mock currency list (add more as needed or fetch from an API)
        return ["USD", "EUR", "GBP", "INR", "JPY", "CAD", "AUD"]

    def convert_currency(self):
        try:
            amount = float(self.amount_entry.get())
            from_curr = self.from_currency.get()
            to_curr = self.to_currency.get()

            if from_curr == to_curr:
                messagebox.showinfo("Info", "Select different currencies for conversion.")
                return

            # Conversion rates (use an API for real-time rates)
            conversion_rates = {
                "USD": {"EUR": 0.85, "GBP": 0.75, "INR": 74.0, "JPY": 109.5, "CAD": 1.25, "AUD": 1.3},
                "EUR": {"USD": 1.18, "GBP": 0.88, "INR": 87.0, "JPY": 129.2, "CAD": 1.47, "AUD": 1.53},
                "GBP": {"USD": 1.34, "EUR": 1.14, "INR": 99.0, "JPY": 149.0, "CAD": 1.68, "AUD": 1.74},
                # Add more as needed
            }

            if from_curr in conversion_rates and to_curr in conversion_rates[from_curr]:
                rate = conversion_rates[from_curr][to_curr]
                converted_amount = amount * rate
                result_text = f"Converted Amount: {converted_amount:.2f} {to_curr}"
                self.result_label.config(text=result_text)
            else:
                messagebox.showwarning("Warning", "Conversion rate not available for selected currencies.")
        
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for amount.")

if __name__ == "__main__":
    app = CurrencyConverterApp()
    app.mainloop()
