import tkinter
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import csv
import matplotlib.pyplot as plt
from tkinter import font
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# List to store selected items
selected_items = []
shopping_window = None
shopping_frame = None

# Define the path to your images folder
images_folder = "C:/Users/96659/Desktop/project_images/"

# Define categories and items
categories = [
    ('Fruits', ['','Apple', 'Banana', 'Blueberry', 'Kiwi', 'Mango', 'Orange', 'Pear', 'Raspberry', 'Strawberry']),
    ('Dairy', ['', 'Bread', 'Cheese', 'Eggs', 'Milk', 'Water', 'White Bread', 'Yogurt']),
    ('Vegetable', ['','Carrot', 'Cucumber', 'Eggplant', 'Lettuce', 'Onions', 'Parsley', 'Pepper', 'Potato', 'Tomato']),
    ('Foods', ['','flour', 'ketchup', 'mayonnaise', 'mustard', 'oil', 'pasta', 'rice', 'salt', 'tomato sauce', 'vinegar']),
    ('Frozen', ['','chicken', 'chicken breast', 'fish', 'meat', 'shrimp']),
    ('Sweets', ['','biscuits', 'chocolate', 'gum', 'icecream', 'juice', 'sugar', 'tea']),
    ('Detergent', ['','cloth detergent', 'conditioner', 'face wash', 'hand wash', 'shampoo', 'softener', 'tissues', 'toilet paper', 'toothpaste'])
]

total_amounts = {}

def add_to_cart(category, item):
    selected_month = monthcombo.get()
    selected_week = weekcombo.get()
    selected_items.append((selected_month, selected_week, category, item))
    update_selection_label()
    show_or_hide_start_shopping_button()


def save_cart_to_csv(filename):
    grouped_items = {}

    # Group selected items by (month, week)
    for month, week, category, item in selected_items:
        key = (month, week)
        if key not in grouped_items:
            grouped_items[key] = []
        grouped_items[key].append(f"{category} - {item}")

    # Write grouped items to the CSV
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Month', 'Week', 'Items'])
        for (month, week), items in grouped_items.items():
            item_list = ', '.join(items)
            writer.writerow([month, week, item_list])

def save_total_amount_to_csv(total_amount):
    filename = 'total_amount_file.csv'
    with open(filename, 'a', newline='') as csvfile:  # Use 'w' mode to overwrite file each time
        writer = csv.writer(csvfile)
        # Write a single row with the total amount
        for month, week, category, item in selected_items:
            writer.writerow([month, week, total_amount])


def update_selection_label():
    # Clear previous content
    for widget in selection_frame.winfo_children():
        widget.destroy()

    # Create labels and delete buttons for selected items
    for index, (month, week, category, item) in enumerate(selected_items, start=1):
        label_text = f"{month}, {week}: {category} - {item}"
        selection_label = tkinter.Label(selection_frame, text=label_text, bg='bisque', justify='left', anchor='w')
        selection_label.grid(row=index, column=0, sticky='w', padx=10, pady=5)

        delete_button = tkinter.Button(selection_frame, text='Delete', command=lambda idx=index - 1: delete_item(idx))
        delete_button.grid(row=index, column=1, padx=10, pady=5)
        delete_button.configure(bg='bisque', fg='black', font=('Calibri', 10, 'bold'))


def delete_item(index):
    del selected_items[index]
    update_selection_label()
    show_or_hide_start_shopping_button()


def clear_selection():
    global selected_items
    selected_items = []
    update_selection_label()
    show_or_hide_start_shopping_button()


def remove_shopping_item(index):
    # Remove the widgets associated with the item at the given index to remove the item and go to the next item
    for widget in shopping_frame.grid_slaves():
        if int(widget.grid_info()["row"]) == index:
            widget.grid_forget()


def show_or_hide_start_shopping_button():
    global start_shopping_button
    if selected_items:
        start_shopping_button.config(state='normal')  # Show the button
    else:
        start_shopping_button.config(state='disabled')  # Hide the button


# Helper functions for found and not found buttons
def found_item(item):
    messagebox.showinfo("Item Found", f"{item} was found!")


def not_found_item(item, row_index):
    global shopping_frame

    # Remove the widgets associated with the item at the specified row_index
    for widget in shopping_frame.grid_slaves():
        info = widget.grid_info()
        if info['row'] == row_index:
            widget.grid_forget()

            # Also remove from the selected_items list
            item_to_remove = selected_items[row_index]
            selected_items.remove(item_to_remove)
            remove_shopping_item(row_index)

            messagebox.showinfo("Item Not Found", f"{item} was not found.")

            # Update the selection label after removing the item
            update_selection_label()
            show_or_hide_start_shopping_button()
            break  # Exit the loop after finding and removing the widget


def calculate_total_item_button(row_index):
    global shopping_frame

    try:
        # Find price entry, quantity combo, and total item price entry
        price_entry = shopping_frame.grid_slaves(row=row_index, column=6)[0]  # Assuming price entry is in column 6
        quantity_combo = shopping_frame.grid_slaves(row=row_index, column=9)[0]  # Assuming quantity combo is in column 9
        total_item_price_entry = shopping_frame.grid_slaves(row=row_index, column=11)[0]  # Assuming total item price entry is in column 11

        # Get values from widgets
        price_text = price_entry.get().strip('$')
        quantity = int(quantity_combo.get())
        price = float(price_text)

        # Calculate total item price
        total_item_price = price * quantity

        # Update total item price entry
        total_item_price_entry.delete(0, tkinter.END)
        total_item_price_entry.insert(0, f"${total_item_price:.2f}")
    except IndexError:
        print(f"No widgets found for row {row_index}")
    except ValueError:
        print(f"Error processing row {row_index}: invalid value")

    # Save updated cart data to CSV
    save_cart_to_csv('cart_data.csv')


def calculate_total_amount():
    global shopping_frame, shopping_window, selected_items

    total_amount = 0.0

    # Iterate over all selected items
    for row_index, (selected_month, selected_week, category, item) in enumerate(selected_items):
        try:
            # Find the total item price entry
            total_item_price_entry = None
            for widget in shopping_frame.grid_slaves():
                if int(widget.grid_info()["row"]) == row_index and int(widget.grid_info()["column"]) == 11:
                    total_item_price_entry = widget
                    break

            if total_item_price_entry:
                # Get the total item price as a float
                total_item_price_text = total_item_price_entry.get().strip('$')
                total_item_price = float(total_item_price_text)

                # Add the total item price to the total amount
                total_amount += total_item_price
            else:
                print(f"No total item price entry found for row {row_index}")
        except ValueError as e:
            print(f"Error processing row {row_index}: {e}")

    # Display the total amount in a popup box
    messagebox.showinfo("Total Amount", f"Total Amount: ${total_amount:.2f}")

    # Save the total amount to a CSV file
    save_total_amount_to_csv(total_amount)


def exit_shopping_window():
    global shopping_window
    if messagebox.askokcancel("Exit", "Are you sure you want to exit shopping?"):

        shopping_window.destroy()
def start_shopping():
    global shopping_window, shopping_frame

    # Create the shopping window as a transient window of the main window
    shopping_window = tkinter.Toplevel(window)
    shopping_window.title("Shopping")
    shopping_window.geometry("1000x900")
    shopping_window.transient(window)  # Set shopping_window as a transient window of the main window

    shopping_frame = tkinter.Frame(shopping_window, bg='teal')
    shopping_frame.pack(fill='both', expand=True, padx=10, pady=10)

    # Track the row index for placing widgets
    row_index = 0

    for (selected_month, selected_week, category, item) in selected_items:
        label_text = f"{selected_month}, {selected_week}: {category} - {item}"

        # Create a label with the item information and image
        shopping_label = tkinter.Label(shopping_frame, text=label_text, bg='salmon')
        shopping_label.grid(row=row_index, column=1, sticky='w', padx=10, pady=5)

        # Load the item image if available
        item_image_path = os.path.join(images_folder, f"{item.lower()}.jpg")
        if os.path.exists(item_image_path):
            item_image = Image.open(item_image_path)
            item_image = item_image.resize((60, 60), Image.LANCZOS)
            item_photo = ImageTk.PhotoImage(item_image)
            shopping_label.config(image=item_photo, compound='left')
            shopping_label.image = item_photo  # Keep a reference to the image to prevent garbage collection

        # Create a button to indicate item found
        found_button = tkinter.Button(shopping_frame, text='Yes, I Found Item', command=lambda i=item: found_item(i))
        found_button.grid(row=row_index, column=3, padx=10, pady=5)
        found_button.configure(bg='salmon', fg='black', font=('Calibri', 10, 'bold'))

        # Create a button to indicate item not found
        not_found_button = tkinter.Button(shopping_frame, text='Not Found',
                                          command=lambda i=item, idx=row_index: not_found_item(i, idx))
        not_found_button.grid(row=row_index, column=4, padx=10, pady=5)
        not_found_button.configure(bg='salmon', fg='black', font=('Calibri', 10, 'bold'))

        # Add a label "Price:" before each price entry box
        price_label = tkinter.Label(shopping_frame, text='Price:', bg='salmon')
        price_label.grid(row=row_index, column=5, padx=5, pady=5)

        # Price entry box
        price_entry = tkinter.Entry(shopping_frame, width=8)
        price_entry.grid(row=row_index, column=6, padx=10, pady=5)
        # Sample dollar sign after price entry box
        sample_dollar_sign = tkinter.Label(shopping_frame, text='$', bg='salmon')
        sample_dollar_sign.grid(row=row_index, column=7, padx=5, pady=5)

        # Quantity label
        quantity_label = tkinter.Label(shopping_frame, text='Quantity:', bg='salmon')
        quantity_label.grid(row=row_index, column=8, padx=5, pady=5)

        # Quantity combobox
        quantity_values = [str(i) for i in range(1, 101)]  # Generate values from 1 to 100
        quantity_combo = ttk.Combobox(shopping_frame, values=quantity_values, width=5)
        quantity_combo.grid(row=row_index, column=9, padx=5, pady=5)

        # Total Item Price button
        calculate_total_item_btn = tkinter.Button(shopping_frame, text='Total Item Price',
                                                  command=lambda idx=row_index: calculate_total_item_button(idx))
        calculate_total_item_btn.grid(row=row_index, column=10, pady=10)
        calculate_total_item_btn.configure(bg='salmon', fg='black', font=('Calibri', 10, 'bold'))

        # Total Item Price entry
        total_item_price_entry = tkinter.Entry(shopping_frame, width=8)
        total_item_price_entry.grid(row=row_index, column=11, padx=10, pady=5)

        # Sample dollar sign after price entry box
        sample_dollar_sign = tkinter.Label(shopping_frame, text='$', bg='salmon')
        sample_dollar_sign.grid(row=row_index, column=12, padx=5, pady=5)

        row_index += 1

    # Create a button to calculate the total amount
    total_amount_button = tkinter.Button(shopping_frame, text='Calculate Total Amount', command=calculate_total_amount)
    total_amount_button.grid(row=row_index, column=0, columnspan=2, pady=10)
    total_amount_button.configure(bg='salmon', fg='black', font=('Calibri', 10, 'bold'))

    # Create an Exit button to close the shopping window
    exit_button = tkinter.Button(shopping_frame, text='Exit', command=exit_shopping_window)
    exit_button.grid(row=row_index + 1, column=1, columnspan=4, pady=10)
    exit_button.configure(bg='salmon', fg='black', font=('Calibri', 10, 'bold'))

    # Keep the shopping window open
    shopping_window.mainloop()

def explore_csv_file():
    filename = 'total_amount_file.csv'
    if os.path.exists(filename):
        try:
            os.startfile(filename)  # Open the CSV file using the default application
        except OSError as e:
            messagebox.showerror("Error", f"Failed to open CSV file: {e}")
    else:
        messagebox.showerror("Error", f"CSV file '{filename}' not found.")


# Function to check if weekly expense exceeds $200 and show alarm if so
def check_weekly_expense():
    filename = 'total_amount_file.csv'
    week_total = 0

    # Read data from the CSV file
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # Check if the row has at least 3 elements (month, week, amount)
            if len(row) >= 3:
                try:
                    amount = float(row[2])
                    week_total += amount
                except ValueError:
                    print(f"Error converting amount to float: {row[2]}")

    # Check if weekly total exceeds $200
    if week_total > 200:
        messagebox.showwarning("Weekly Expense Alert", f"You've exceeded your weekly budget of $200 \nCurrent Total: ${week_total:.2f}")


def plot_bar_chart():
    filename = 'total_amount_file.csv'
    month_data = {}
    budget = 200  # Weekly budget

    # Check weekly expense before displaying the chart
    check_weekly_expense()

    # Read data from the CSV file
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            month = row[0]
            week = row[1]
            amount = float(row[2])

            # Accumulate the total amount for each month and week
            key = (month, week)
            if key in month_data:
                month_data[key] += amount
            else:
                month_data[key] = amount

    # Prepare data for plotting
    months = list(month_data.keys())
    amounts = [month_data[key] for key in months]

    colors = ['blue', 'red', 'green', 'orange']  # Add more colors as needed

    # Create the bar chart
    plt.figure(figsize=(10, 6))
    for i, (month, week) in enumerate(months):
        plt.bar(f"{month}\n{week}", amounts[i], color=colors[i % len(colors)], alpha=0.8)

        # Add a horizontal line for the weekly budget
    plt.axhline(y=budget, color='r', linestyle='--', label='Weekly Budget ($200)')

    plt.xlabel('Month, Week')
    plt.ylabel('Total Amount ($)')
    plt.title('Total Amount Spent by Month and Week')
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    # Show the chart
    plt.show()


# Main window
window = tkinter.Tk()
window.title('My Cart')
window.title('My Cart')
window.configure(bg='teal')


# Configure resizing behavior
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)

frame = tkinter.Frame(window, bg='teal')
frame.pack(fill='both', expand=True, padx=10, pady=5)

cartframe = tkinter.LabelFrame(frame, text='Shopping Information', bg='salmon')
cartframe.pack(fill='x', padx=10, pady=5)

tkinter.Label(cartframe, text='Month', bg='bisque').grid(row=0, column=0, padx=10, pady=5)
monthcombo = ttk.Combobox(cartframe, values=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], width=15)
monthcombo.grid(row=0, column=1, padx=10, pady=5)

tkinter.Label(cartframe, text='Week', bg='bisque').grid(row=0, column=2, padx=10, pady=5)
weekcombo = ttk.Combobox(cartframe, values=['Week 1', 'Week 2', 'Week 3', 'Week 4'], width=15)
weekcombo.grid(row=0, column=3, padx=10, pady=5)

purchase_frame = tkinter.LabelFrame(frame, text='My Cart', bg='salmon')
purchase_frame.pack(fill='both', expand=True, padx=10, pady=10)

for row_index, (category, items) in enumerate(categories):
    tkinter.Label(purchase_frame, text=category, bg='salmon').grid(row=row_index, column=0, padx=10, pady=5)
    item_combo = ttk.Combobox(purchase_frame, values=items, width=15)
    item_combo.grid(row=row_index, column=1, padx=10, pady=5)

    # Create a styled "Add to Cart" button
    add_button = tkinter.Button(purchase_frame, text='Add to Cart',
                                command=lambda c=category, ic=item_combo: add_to_cart(c, ic.get()))
    add_button.grid(row=row_index, column=2, padx=10, pady=5)

    add_button.configure(bg='bisque', fg='black', font=('Calibri', 10, 'bold'))

my_selection_frame = tkinter.LabelFrame(frame, text='My Selection', bg='salmon')
my_selection_frame.pack(fill='both', expand=True, padx=10, pady=20)

canvas = tkinter.Canvas(my_selection_frame, bg='salmon', highlightthickness=0)
canvas.pack(fill='both', expand=True, padx=10, pady=10)

scrollbar = ttk.Scrollbar(my_selection_frame, orient='vertical', command=canvas.yview)
scrollbar.pack(side='right', fill='y')

canvas.configure(yscrollcommand=scrollbar.set)

selection_frame = tkinter.Frame(canvas, bg='salmon')
canvas.create_window((0, 0), window=selection_frame, anchor='nw')

selection_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

clear_button = tkinter.Button(my_selection_frame, text='Clear Selection', command=clear_selection)
clear_button.pack(side='left', padx=10, pady=10)
clear_button.configure(bg='bisque', fg='black', font=('Calibri', 10, 'bold'))

explore_csv_button = tkinter.Button(my_selection_frame, text='Explore CSV', command=explore_csv_file)
explore_csv_button.pack(side='left', padx=10, pady=10)
explore_csv_button.configure(bg='bisque', fg='black', font=('Calibri', 10, 'bold'))

start_shopping_button = tkinter.Button(frame, text='Start Shopping', command=start_shopping, state='disabled')
start_shopping_button.pack(side='left', padx=5, pady=5)
start_shopping_button.configure(bg='bisque', fg='black', font=('Calibri', 10, 'bold'))

# Add a button to show the chart
show_chart_button = tkinter.Button(frame, text='Show Chart', command=plot_bar_chart)
show_chart_button.pack(side='left', padx=5, pady=5)
show_chart_button.configure(bg='bisque', fg='black', font=('Calibri', 10, 'bold'))

# Create an Exit button to exit the entire program
def exit_program():
    global shopping_window
    if shopping_window:
        shopping_window.destroy()  # Close the shopping window if it's open

    # Close the main window upon confirmation
    if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
        window.destroy()  # Close the main w

exit_button = tkinter.Button(frame, text='Exit Program', command=exit_program)
exit_button.pack(side='left', padx=5, pady=5)
exit_button.configure(bg='bisque', fg='black', font=('Calibri', 10, 'bold'))


window.mainloop()
