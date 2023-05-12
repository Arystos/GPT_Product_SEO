import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import os
from package.utils import load_file, save_file
from package.generator import generate_text, generate_descriptions
from tqdm import tqdm
from threading import Thread

# Function to create the main GUI window
def create_window():
    window = tk.Tk()
    window.title("Product Description Generator")
    window.geometry("500x400")

    label = tk.Label(window, text="Import a CSV file containing product information")
    label.pack(pady=20)

    products = []  # Placeholder for loaded products
    output_file_path = None

    # Function to handle button click events
    def handle_click():
        nonlocal output_file_path
        file_path = filedialog.askopenfilename(title="Select a CSV file", filetypes=[("CSV Files", "*.csv")])
        if file_path:
            products.clear()  # Clear existing products
            products.extend(load_file(file_path))
            output_file_path = None
            generate_button.config(state=tk.NORMAL)  # Enable the Generate button
            import_button.config(state=tk.DISABLED)  # Disable the Import CSV button

    # Create a button to import the CSV file
    import_button = tk.Button(window, text="Import CSV", command=handle_click, state=tk.DISABLED)
    import_button.pack(pady=10)

    # Function to generate descriptions
    def generate_descriptions_gui():
        if products:
            # Select output file path with .csv extension
            file_options = [('CSV Files', '*.csv')]
            output_file_path = filedialog.asksaveasfilename(title="Save Output CSV", filetypes=file_options,
                                                            defaultextension=".csv")
            if output_file_path:
                progress_bar = tqdm(total=len(products), unit="product", desc="Generating", ncols=60)

                log_text = ScrolledText(window, width=70, height=10)
                log_text.pack(pady=10)

                def generate():
                    generated_products = []
                    for product in tqdm(products, desc="Generating", unit="product", ncols=60, leave=False):
                        cod, nome, breve_descrizione, descrizione = product
                        prompt = f"New {nome} - {breve_descrizione}\n\n{descrizione}\n\n"
                        new_breve_descrizione = generate_text(prompt + "Write a short description for the product.")
                        new_descrizione = generate_text(prompt + "Write a detailed description for the product.")
                        generated_product = (cod, nome, new_breve_descrizione, new_descrizione)
                        generated_products.append(generated_product)
                        progress_bar.update(1)
                        log_text.insert(tk.END, f"Generated description for product '{nome}'\n")
                        log_text.see(tk.END)
                        window.update_idletasks()

                    progress_bar.close()
                    log_text.insert(tk.END, "Generation complete!\n")
                    log_text.see(tk.END)

                    # Save generated products to the output file
                    success = save_file(output_file_path, generated_products)
                    if success:
                        messagebox.showinfo("Generation Complete", "Product descriptions generated successfully!")
                    else:
                        messagebox.showerror("Error", "Failed to save the output file.")

                thread = Thread(target=generate)
                thread.start()

    # Create a button to generate descriptions
    generate_button = tk.Button(window, text="Generate", command=generate_descriptions_gui, state=tk.DISABLED)
    generate_button.pack(pady=10)
    log_text.configure(state=tk.DISABLED)  # Set the text box as read-only

    window.mainloop()

# Function to run the program
def run_gui():
    create_window()
