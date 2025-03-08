import tkinter as tk

# Function to save text to a file
def save_to_file():
    text = text_box.get("1.0", tk.END)  # Get all text from the text box
    with open("savefile.txt", "w") as file:
        file.write(text.strip())  # Write text to file, stripping trailing newlines

# Create the main window
root = tk.Tk()
root.title("Text Box Example")

# Create a Text Box
text_box = tk.Text(root, height=5, width=40)
text_box.pack()

# Insert text into the Text Box
text_box.insert("1.0", "example")  # "1.0" means line 1, character 0 (start of the text box)

# Create a "Save to file" Button
save_button = tk.Button(root, text="Save to file", command=save_to_file)
save_button.pack()

# Run the application
root.mainloop()

