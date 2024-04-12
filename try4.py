import tkinter
from tkinter import ttk
from tkinter import messagebox
import csv

# Global list to store selected items
selected_items = []


def add_to_cart(category, selected_item):
    selected_items.append((category, selected_item))
    update_selection_label()


def update_selection_label():
    # Clear previous content
    for widget in selection_frame.winfo_children():
        widget.destroy()

    # Create labels and delete buttons for selected items
    for index, (category, item) in enumerate(selected_items, start=1):
        label_text = f"{category}: {item}"
        selection_label = tkinter.Label(selection_frame, text=label_text, bg='light green', justify='left', anchor='w')
        selection_label.grid(row=index, column=0, sticky='w', padx=10, pady=5)

        delete_button = tkinter.Button(selection_frame, text='Delete', command=lambda idx=index-1: delete_item(idx))
        delete_button.grid(row=index, column=1, padx=10, pady=5)


def delete_item(index):
    del selected_items[index]  # Remove item at the specified index
    update_selection_label()  # Update the display to reflect the changes


def clear_selection():
    global selected_items
    selected_items = []  # Clear the selected items list
    update_selection_label()  # Update the display to reflect the changes


def export_to_csv():
    if selected_items:
        file_path = "cart_items.csv"
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Category", "Item"])
            for category, item in selected_items:
                writer.writerow([category, item])
        messagebox.showinfo("Export Complete", f"Items exported to {file_path}")
    else:
        messagebox.showwarning("Empty Cart", "No items selected to export.")


# Main window
window = tkinter.Tk()
window.title('My Cart')
window.configure(bg='purple')

# Main frame for layout
frame = tkinter.Frame(window, bg='light green')
frame.pack(fill='both', expand=True, padx=10, pady=5)

# Shopping information frame
cartinfoframe = tkinter.LabelFrame(frame, text='Shopping Information', bg='light green')
cartinfoframe.pack(fill='both', expand=True, padx=10, pady=5)

# Month label and combobox
tkinter.Label(cartinfoframe, text='Month', bg='light green').grid(row=0, column=0, padx=10, pady=5)
monthtypecombo = ttk.Combobox(cartinfoframe,
                              values=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                                      'September', 'October', 'November', 'December'], width=15)
monthtypecombo.grid(row=1, column=0, padx=10, pady=5)

# Week label and combobox
tkinter.Label(cartinfoframe, text='Week', bg='light green').grid(row=0, column=1, padx=10, pady=5)
weektypecombo = ttk.Combobox(cartinfoframe, values=['Week 1', 'Week 2', 'Week 3', 'Week 4'], width=15)
weektypecombo.grid(row=1, column=1, padx=10, pady=5)

# My Cart label frame
purchase_frame = tkinter.LabelFrame(frame, text='My Cart', bg='light green')
purchase_frame.pack(fill='both', expand=True, padx=10, pady=10)

# Widgets for selecting items in each category
categories = [
    ('Fruits', ['Apple', 'Banana', 'Blueberry', 'Kiwi', 'Mango', 'Orange', 'Pear', 'Raspberry', 'Strawberry']),
    ('Dairy', ['Bread', 'Cheese', 'Eggs', 'Milk', 'Water', 'White Bread', 'Yogurt']),
    ('Vegetable', ['Carrot', 'Cucumber', 'Eggplant', 'Lettuce', 'Onions', 'Parsley', 'Pepper', 'Potato', 'Tomato']),
    ('Foods', ['flour', 'ketchup', 'mayonnaise', 'mustard', 'oil', 'pasta', 'rice', 'salt', 'tomato sauce', 'vinegar']),
    ('Frozen', ['chicken', 'chicken breast', 'fish', 'meat', 'shrimp']),
    ('Sweets', ['biscuits', 'chocolate', 'gum', 'icecream', 'juice', 'sugar', 'tea']),
    ('Detergent',
     ['cloth detergent', 'conditioner', 'face wash', 'hand wash', 'shampoo', 'softener', 'tissues', 'toilet paper',
      'toothpaste'])
]

row_index = 1
for category, items in categories:
    purchasenamelabel = tkinter.Label(purchase_frame, text=category, bg='light green')
    purchasenamelabel.grid(row=row_index, column=0, padx=10, pady=5)

    item_combo = ttk.Combobox(purchase_frame, values=items, width=15)
    item_combo.grid(row=row_index, column=1, padx=10, pady=5)

    add_button = tkinter.Button(purchase_frame, text='Add to cart',
                                command=lambda c=category, ic=item_combo: add_to_cart(c, ic.get()))
    add_button.grid(row=row_index, column=2, padx=10, pady=5)

    row_index += 1

# My Selection label frame
my_selection_frame = tkinter.LabelFrame(frame, text='My Selection', bg='light green')
my_selection_frame.pack(fill='both', expand=True, padx=10, pady=20)

# Scrollable canvas for displaying selected items
canvas = tkinter.Canvas(my_selection_frame, bg='light green', highlightthickness=0)
canvas.pack(fill='both', expand=True, padx=10, pady=10)

scrollbar = ttk.Scrollbar(my_selection_frame, orient='vertical', command=canvas.yview)
scrollbar.pack(side='right', fill='y')

canvas.configure(yscrollcommand=scrollbar.set)

# Frame inside canvas to hold selection labels
selection_frame = tkinter.Frame(canvas, bg='light green')
canvas.create_window((0, 0), window=selection_frame, anchor='nw')

# Bind canvas to scroll region
selection_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Clear button
clear_button = tkinter.Button(my_selection_frame, text='Clear Selection', command=clear_selection)
clear_button.pack(side='left', padx=10, pady=10)

# Export button
export_button = tkinter.Button(my_selection_frame, text='Export to CSV', command=export_to_csv)
export_button.pack(side='left', padx=10, pady=10)

window.mainloop()
