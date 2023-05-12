import csv

# Function to load products from a CSV file
def load_file(file_path):
    products = []
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            products.append(tuple(row))
    return products

# Function to save products to a CSV file
def save_file(file_path, products):
    try:
        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["COD", "Nome", "Breve Descrizione", "Descrizione"])
            writer.writerows(products)
        return True
    except Exception as e:
        print(f"Failed to save the file: {e}")
        return False
