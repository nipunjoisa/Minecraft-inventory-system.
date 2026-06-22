import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
import os


class Node:
    """Represents a slot in the inventory."""
    def __init__(self, item, quantity):
        self.item = item
        self.quantity = quantity
        self.next = None


class Inventory:
    """Linked List to manage the inventory."""
    def __init__(self):
        self.head = None

    def add_item(self, item, quantity):
        """Add an item to the inventory."""
        current = self.head
        while current:
            if current.item == item:
                current.quantity += quantity
                return f"Updated {item}: New Quantity = {current.quantity}"
            current = current.next

        new_node = Node(item, quantity)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        return f"Added {item}: Quantity = {quantity}"

    def remove_item(self, item, quantity):
        """Remove a specific quantity of an item."""
        current = self.head
        prev = None

        while current:
            if current.item == item:
                if current.quantity >= quantity:
                    current.quantity -= quantity
                    return f"Removed {quantity} {item}(s): Remaining = {current.quantity}"
                else:
                    if prev:
                        prev.next = current.next
                    else:
                        self.head = current.next
                    return f"Removed all {item}(s)."
            prev = current
            current = current.next

        return f"{item} not found in the inventory."

    def display_inventory(self):
        """Return all items in the inventory."""
        items = []
        current = self.head
        while current:
            items.append((current.item, current.quantity))
            current = current.next
        return items

    def has_enough_items(self, required_items):
        """Check if the inventory has enough materials for crafting."""
        current = self.head
        for item, qty in required_items:
            found = False
            while current:
                if current.item == item and current.quantity >= qty:
                    found = True
                    break
                current = current.next
            if not found:
                return False
        return True

    def can_craft(self, crafted_item, required_items):
        """Calculate how many items can be crafted based on the available materials."""
        min_craftable = float('inf')

        for item, qty in required_items:
            current = self.head
            while current:
                if current.item == item:
                    craftable_qty = current.quantity // qty
                    min_craftable = min(min_craftable, craftable_qty)
                    break
                current = current.next
        return min_craftable if min_craftable != float('inf') else 0

    def craft_item(self, crafted_item, required_items, quantity):
        """Craft an item and remove materials from inventory."""
        if self.has_enough_items(required_items):
            for item, qty in required_items:
                self.remove_item(item, qty * quantity)
            self.add_item(crafted_item, quantity)
            return f"Crafted {quantity} {crafted_item}(s)!"
        else:
            return "Not enough materials to craft this item."


class InventoryApp:
    """GUI Application for the inventory system."""
    def __init__(self, root):
        self.inventory = Inventory()
        self.root = root
        self.root.title("Inventory System")
        
        # Minecraft item list (Wood, Iron, Gold, Stone, Redstone, Diamond, Coal)
        self.minecraft_items = ["Wood", "Iron", "Gold", "Stone", "Redstone", "Diamond", "Coal"]

        self.item_images = {}  # Dictionary to store loaded item images
        self.image_path = r"C:\Users\nipun\Desktop\Nipun\DSA PROJECT"  # Update path
        self.load_images()
        # Add "All Recipes" button
        

        # Add item section
        self.add_frame = tk.Frame(root)
        self.add_frame.pack(pady=10)

        tk.Label(self.add_frame, text="Item:").grid(row=0, column=0, padx=5)
        self.item_dropdown = Combobox(self.add_frame, values=self.minecraft_items, state="readonly")
        self.item_dropdown.grid(row=0, column=1, padx=5)
        self.item_dropdown.set("Select Item")

        tk.Label(self.add_frame, text="Quantity:").grid(row=0, column=2, padx=5)
        self.quantity_entry = tk.Entry(self.add_frame)
        self.quantity_entry.grid(row=0, column=3, padx=5)

        tk.Button(self.add_frame, text="Add Item", command=self.add_item).grid(row=0, column=4, padx=5)

        # Crafting section
        self.crafting_frame = tk.Frame(root)
        self.crafting_frame.pack(pady=10)

        tk.Label(self.crafting_frame, text="Craft Item:").grid(row=0, column=0, padx=5)
        self.crafting_dropdown = Combobox(self.crafting_frame, values=["Wooden Pickaxe", "Stone Pickaxe", "Iron Pickaxe", 
                                                                      "Gold Pickaxe", "Diamond Pickaxe",
                                                                      "Wooden Sword", "Stone Sword", "Iron Sword", 
                                                                      "Gold Sword", "Diamond Sword",
                                                                      "Stick", "Torch"], state="readonly")
        self.crafting_dropdown.grid(row=0, column=1, padx=5)
        self.crafting_dropdown.set("Select Item to Craft")

        self.crafting_slider = tk.Scale(self.crafting_frame, from_=1, to=1, orient="horizontal")  # Placeholder for slider
        self.crafting_slider.grid(row=0, column=2, padx=5)
        
        tk.Button(self.crafting_frame, text="Craft", command=self.craft_item).grid(row=0, column=3, padx=5)

        # Recipe Book Button
        tk.Button(self.crafting_frame, text="Recipe Book", command=self.view_recipe_book).grid(row=0, column=4, padx=5)
        tk.Button(self.crafting_frame, text="All Recipes", command=self.view_all_recipes).grid(row=0, column=5, padx=5)
        # Inventory display area
        self.inventory_frame = tk.Frame(root, bg="#333333", bd=5, relief=tk.RIDGE)
        self.inventory_frame.pack(pady=20, padx=10, fill=tk.BOTH, expand=True)

        self.refresh_inventory_display()

    def load_images(self):
        """Load images for items from the specified folder."""
        item_images = {
            "Torch": "torch.jpg",
            "Stone Sword": "stonesword.jpg",
            "Stone Pickaxe": "stonepickaxe.jpg",
            "Wooden Pickaxe": "woodenpickaxe.jpg",
            "Wooden Sword": "woodensword.jpg",
            "Stick": "stick.jpg",
            "Coal": "coal.jpg",
            "Iron Sword": "ironsowrd.jpg",
            "Iron Pickaxe": "ironpickaxe.jpg",
            "Diamond Sword": "diamondsword.jpg",
            "Diamond Pickaxe": "diamonpickaxe.jpg",
            "Gold Sword": "goldsword.jpg",
            "Gold Pickaxe": "goldpickaxe.jpg",
            "Gold": "gold.jpg",
            "Stone": "stone.jpg",
            "Redstone": "redstone.jpg",
            "Diamond": "diamond.jpg",
            "Wood": "wood.jpg",
            "Iron": "iron.jpg"
        }

        for item, image_name in item_images.items():
            try:
                img_path = os.path.join(self.image_path, image_name)
                img = Image.open(img_path)
                img = img.resize((50, 50), Image.ANTIALIAS)
                self.item_images[item] = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Error loading image for {item}: {e}")
                self.item_images[item] = None  # Use a placeholder if image is missing

    def add_item(self):
        """Handle adding an item via GUI."""
        item = self.item_dropdown.get().strip()
        quantity = self.quantity_entry.get().strip()

        if item == "Select Item" or not quantity.isdigit():
            messagebox.showerror("Error", "Please select a valid item and enter a valid quantity.")
            return

        quantity = int(quantity)
        message = self.inventory.add_item(item, quantity)
        self.show_message(message)

    def craft_item(self):
        """Handle crafting an item."""
        crafted_item = self.crafting_dropdown.get().strip()

        if crafted_item == "Select Item to Craft":
            messagebox.showerror("Error", "Please select an item to craft.")
            return

        # Define crafting recipes (Wood, Iron, Gold, Stone, Redstone, Diamond)
        crafting_recipes = {
            "Wooden Sword": [("Wood", 2), ("Stick", 1)],
            "Stone Sword": [("Stone", 2), ("Stick", 1)],
            "Iron Sword": [("Iron", 2), ("Stick", 1)],
            "Gold Sword": [("Gold", 2), ("Stick", 1)],
            "Diamond Sword": [("Diamond", 2), ("Stick", 1)],

            "Wooden Pickaxe": [("Wood", 3), ("Stick", 2)],
            "Stone Pickaxe": [("Stone", 3), ("Stick", 2)],
            "Iron Pickaxe": [("Iron", 3), ("Stick", 2)],
            "Gold Pickaxe": [("Gold", 3), ("Stick", 2)],
            "Diamond Pickaxe": [("Diamond", 3), ("Stick", 2)],

            "Stick": [("Wood", 1)],
            "Torch": [("Wood", 1), ("Coal", 1)]
        }

        # Check if crafting is possible
        required_items = crafting_recipes.get(crafted_item, [])
        max_craftable = self.inventory.can_craft(crafted_item, required_items)

        if max_craftable <= 0:
            messagebox.showerror("Error", "Not enough materials to craft this item.")
            return

        self.crafting_slider.config(from_=1, to=max_craftable, label=f"Quantity (Max: {max_craftable})")
        quantity = self.crafting_slider.get()

        if quantity <= 0:
            messagebox.showerror("Error", "You must select a quantity greater than zero.")
            return

        message = self.inventory.craft_item(crafted_item, required_items, quantity)
        self.show_message(message)

    def show_message(self, message):
        """Show a popup message and refresh the inventory display."""
        messagebox.showinfo("Inventory Update", message)
        self.refresh_inventory_display()

    def view_recipe_book(self):
        """Show recipe book."""
        recipes = {
            "Wooden Sword": [("Wood", 2), ("Stick", 1)],
            "Stone Sword": [("Stone", 2), ("Stick", 1)],
            "Iron Sword": [("Iron", 2), ("Stick", 1)],
            "Gold Sword": [("Gold", 2), ("Stick", 1)],
            "Diamond Sword": [("Diamond", 2), ("Stick", 1)],

            "Wooden Pickaxe": [("Wood", 3), ("Stick", 2)],
            "Stone Pickaxe": [("Stone", 3), ("Stick", 2)],
            "Iron Pickaxe": [("Iron", 3), ("Stick", 2)],
            "Gold Pickaxe": [("Gold", 3), ("Stick", 2)],
            "Diamond Pickaxe": [("Diamond", 3), ("Stick", 2)],

            "Stick": [("Wood", 1)],
            "Torch": [("Wood", 1), ("Coal", 1)]
        }

        recipe_text = "\n".join([f"{item} => {qty} {item}" for item, qty in recipes.get(self.crafting_dropdown.get(), [])])
        messagebox.showinfo("Recipe Book", recipe_text)
    
    def view_all_recipes(self):
        """Show all crafting recipes with images."""
        crafting_recipes = {
            "Wooden Sword": [("Wood", 2), ("Stick", 1)],
            "Stone Sword": [("Stone", 2), ("Stick", 1)],
            "Iron Sword": [("Iron", 2), ("Stick", 1)],
            "Gold Sword": [("Gold", 2), ("Stick", 1)],
            "Diamond Sword": [("Diamond", 2), ("Stick", 1)],
    
            "Wooden Pickaxe": [("Wood", 3), ("Stick", 2)],
            "Stone Pickaxe": [("Stone", 3), ("Stick", 2)],
            "Iron Pickaxe": [("Iron", 3), ("Stick", 2)],
            "Gold Pickaxe": [("Gold", 3), ("Stick", 2)],
            "Diamond Pickaxe": [("Diamond", 3), ("Stick", 2)],
    
            "Stick": [("Wood", 1)],
            "Torch": [("Wood", 1), ("Coal", 1)]
        }
    
        # Create a new window for the recipes
        recipe_window = tk.Toplevel(self.root)
        recipe_window.title("All Recipes")
        recipe_window.geometry("600x400")
    
        canvas = tk.Canvas(recipe_window)
        scrollbar = tk.Scrollbar(recipe_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
    
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
    
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
    
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
        tk.Label(scrollable_frame, text="All Crafting Recipes", font=("Arial", 16, "bold")).pack(pady=10)
    
        for crafted_item, materials in crafting_recipes.items():
            # Recipe container
            recipe_frame = tk.Frame(scrollable_frame, bg="#f5f5f5", bd=2, relief=tk.GROOVE)
            recipe_frame.pack(fill="x", padx=10, pady=5)
    
            # Display crafted item's image and name
            if crafted_item in self.item_images and self.item_images[crafted_item]:
                tk.Label(recipe_frame, image=self.item_images[crafted_item], bg="#f5f5f5").pack(side="left", padx=10, pady=5)
            else:
                tk.Label(recipe_frame, text="[Image Missing]", bg="#f5f5f5", fg="red").pack(side="left", padx=10, pady=5)
    
            # Display recipe text
            recipe_text = f"{crafted_item} requires: " + ", ".join([f"{qty} {item}" for item, qty in materials])
            tk.Label(recipe_frame, text=recipe_text, bg="#f5f5f5", fg="black", font=("Arial", 12), anchor="w", justify="left").pack(side="left", padx=10, pady=5)


    
    
    def refresh_inventory_display(self):
        """Refresh the inventory display with items and their remove buttons."""
        # Clear existing widgets in the inventory frame
        for widget in self.inventory_frame.winfo_children():
            widget.destroy()
    
        # Create a canvas to allow scrolling
        canvas = tk.Canvas(self.inventory_frame)
        scrollbar = tk.Scrollbar(self.inventory_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
    
        # Create a frame inside the canvas to hold the inventory items
        inventory_frame = tk.Frame(canvas, bg="#333333")
        canvas.create_window((0, 0), window=inventory_frame, anchor="nw")
    
        # Add items to the inventory frame
        items = self.inventory.display_inventory()
    
        if not items:
            tk.Label(inventory_frame, text="Inventory is empty.", bg="#333333", fg="white", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10)
        else:
            # Calculate the number of columns based on available space (3 columns)
            columns = 7 # You can increase this value for more items per row
            
            # Adjust row and column configurations to take full space
            inventory_frame.grid_rowconfigure(0, weight=1)
            inventory_frame.grid_columnconfigure(0, weight=1)
    
            for idx, (item, quantity) in enumerate(items):
                row = idx // columns
                column = idx % columns
    
                item_frame = tk.Frame(inventory_frame, bg="#444444", bd=2, relief=tk.GROOVE)
                item_frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
    
                # Allow grid cells to expand and fill available space
                inventory_frame.grid_rowconfigure(row, weight=1, minsize=100)
                inventory_frame.grid_columnconfigure(column, weight=1, minsize=100)
    
                if item in self.item_images and self.item_images[item]:
                    tk.Label(item_frame, image=self.item_images[item], bg="#444444").pack(pady=5)
    
                tk.Label(item_frame, text=item, bg="#444444", fg="white", font=("Arial", 12)).pack(pady=5)
                tk.Label(item_frame, text=f"Quantity: {quantity}", bg="#444444", fg="#aaffaa", font=("Arial", 10)).pack(pady=5)
    
                remove_button = tk.Button(
                    item_frame,
                    text="Remove",
                    command=lambda i=item, q=quantity: self.show_remove_slider(i, q),
                    bg="#ff5555",
                    fg="white",
                    font=("Arial", 10)
                )
                remove_button.pack(pady=5)
    
        # Update the canvas scrollable region
        inventory_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
    
        # Pack the canvas and scrollbar inside the frame
        canvas.pack(side="left", fill=tk.BOTH, expand=True)
        scrollbar.pack(side="right", fill="y")
    
        # Update the canvas viewable area
        self.inventory_frame.update_idletasks()




    def show_remove_slider(self, item, max_quantity):
        """Show a slider to choose the quantity to remove."""
        slider_window = tk.Toplevel(self.root)
        slider_window.title(f"Remove {item}")

        tk.Label(slider_window, text=f"Select quantity to remove from {item}").pack(pady=10)

        remove_slider = tk.Scale(slider_window, from_=1, to=max_quantity, orient="horizontal")
        remove_slider.pack(pady=10)

        tk.Button(slider_window, text="Remove", command=lambda: self.remove_item(item, remove_slider.get(), slider_window)).pack(pady=10)

    def remove_item(self, item, quantity, window):
        """Remove the selected quantity of the item and close the slider window."""
        message = self.inventory.remove_item(item, quantity)
        self.show_message(message)
        window.destroy()


# Run the GUI application
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")  # Set window size
    app = InventoryApp(root)
    root.mainloop()

