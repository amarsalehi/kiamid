import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np

processed_image = None
contours_image = None

def calculate_leaf_area(reference_path, leaf_path, reference_length_cm, reference_width_cm, reference_length_pixels, reference_width_pixels):
    # Load the reference image (calibration)
    reference_image = cv2.imread(reference_path)

    # Calculate the conversion factors for length and width
    length_conversion_factor = reference_length_cm / reference_length_pixels
    width_conversion_factor = reference_width_cm / reference_width_pixels

    # Convert the reference image to grayscale
    reference_gray = cv2.cvtColor(reference_image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to segment the reference paper from the background
    _, reference_threshold = cv2.threshold(reference_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Find contours of the reference paper
    reference_contours, _ = cv2.findContours(reference_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Load the leaf image
    leaf_image = cv2.imread(leaf_path)

    # Convert the leaf image to grayscale
    leaf_gray = cv2.cvtColor(leaf_image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to segment the leaf from the background
    _, leaf_threshold = cv2.threshold(leaf_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Find contours of the leaf
    leaf_contours, _ = cv2.findContours(leaf_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize the total leaf area
    total_area = 0

    # Calculate the area of each contour and add it to the total
    for contour in leaf_contours:
        area = cv2.contourArea(contour)
        total_area += area

    # Calculate the actual leaf area
    actual_area = total_area * length_conversion_factor * width_conversion_factor

    return actual_area

def process_leaf_image(image_path):
    # This function can be customized to apply any image processing techniques as needed.
    # For demonstration purposes, we'll just return the original image path without any processing.
    return image_path

def draw_leaf_contours(leaf_path):
    leaf_image = cv2.imread(leaf_path)
    leaf_gray = cv2.cvtColor(leaf_image, cv2.COLOR_BGR2GRAY)
    _, leaf_threshold = cv2.threshold(leaf_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    leaf_contours, _ = cv2.findContours(leaf_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contours_image = np.zeros_like(leaf_image)
    cv2.drawContours(contours_image, leaf_contours, -1, (0, 255, 0), 2)

    return contours_image

def browse_reference_photo():
    reference_path = filedialog.askopenfilename(title="Select Reference Photo", filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
    if reference_path:
        entry_reference.delete(0, tk.END)
        entry_reference.insert(0, reference_path)

def show_processed_photo(image_path):
    global processed_image
    img = Image.open(image_path)
    img = img.resize((200, 200))
    processed_image = ImageTk.PhotoImage(img)
    label_leaf_image.config(image=processed_image)

def show_contours_photo(image):
    global contours_image
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img = img.resize((200, 200))
    contours_image = ImageTk.PhotoImage(img)
    label_contours_image.config(image=contours_image)

def clear_images():
    global processed_image, contours_image
    processed_image = None
    contours_image = None
    label_leaf_image.config(image=None)
    label_contours_image.config(image=None)

def start_processing():
    try:
        clear_images()
        reference_path = entry_reference.get()
        leaf_path = entry_leaf.get()
        reference_length_cm = float(entry_ref_length_cm.get())
        reference_width_cm = float(entry_ref_width_cm.get())
        reference_length_pixels = float(entry_ref_length_pixels.get())
        reference_width_pixels = float(entry_ref_width_pixels.get())

        leaf_area = calculate_leaf_area(reference_path, leaf_path, reference_length_cm, reference_width_cm, reference_length_pixels, reference_width_pixels)
        label_result.config(text=f"Leaf area: {leaf_area:.2f} cm^2")

        processed_leaf_path = process_leaf_image(leaf_path)
        show_processed_photo(processed_leaf_path)

        contours_image = draw_leaf_contours(processed_leaf_path)
        show_contours_photo(contours_image)

    except Exception as e:
        messagebox.showerror("Error", str(e))

def browse_leaf_photo():
    leaf_path = filedialog.askopenfilename(title="Select Leaf Photo", filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
    if leaf_path:
        entry_leaf.delete(0, tk.END)
        entry_leaf.insert(0, leaf_path)
        show_original_photo(leaf_path)

def show_original_photo(image_path):
    global processed_image
    img = Image.open(image_path)
    img = img.resize((200, 200))
    processed_image = ImageTk.PhotoImage(img)
    label_leaf_image.config(image=processed_image)

# Create the main window
root = tk.Tk()
root.title("Kiamid Leaf Area Calculator")
root.geometry("800x600")

# Create a frame for the left column
left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH)  # <-- Set fill to BOTH

# Create labels and entry fields in the left column
label_reference = tk.Label(left_frame, text="Reference Photo:")
label_reference.grid(row=0, column=0, sticky="w")

entry_reference = tk.Entry(left_frame, width=40)
entry_reference.grid(row=0, column=1, padx=10, pady=5, columnspan=2, sticky="w")

button_browse_reference = tk.Button(left_frame, text="Browse", command=browse_reference_photo)
button_browse_reference.grid(row=0, column=3, padx=10, pady=5, sticky="w")

label_leaf = tk.Label(left_frame, text="Leaf Photo:")
label_leaf.grid(row=1, column=0, sticky="w")

entry_leaf = tk.Entry(left_frame, width=40)
entry_leaf.grid(row=1, column=1, padx=10, pady=5, columnspan=2, sticky="w")

button_browse_leaf = tk.Button(left_frame, text="Browse", command=browse_leaf_photo)
button_browse_leaf.grid(row=1, column=3, padx=10, pady=5, sticky="w")

label_ref_length_cm = tk.Label(left_frame, text="Reference Length (cm):")
label_ref_length_cm.grid(row=2, column=0, sticky="w")

entry_ref_length_cm = tk.Entry(left_frame, width=10)
entry_ref_length_cm.grid(row=2, column=1, padx=10, pady=5, sticky="w")

label_ref_width_cm = tk.Label(left_frame, text="Reference Width (cm):")
label_ref_width_cm.grid(row=3, column=0, sticky="w")

entry_ref_width_cm = tk.Entry(left_frame, width=10)
entry_ref_width_cm.grid(row=3, column=1, padx=10, pady=5, sticky="w")

label_ref_length_pixels = tk.Label(left_frame, text="Reference Length (pixels):")
label_ref_length_pixels.grid(row=4, column=0, sticky="w")

entry_ref_length_pixels = tk.Entry(left_frame, width=10)
entry_ref_length_pixels.grid(row=4, column=1, padx=10, pady=5, sticky="w")

label_ref_width_pixels = tk.Label(left_frame, text="Reference Width (pixels):")
label_ref_width_pixels.grid(row=5, column=0, sticky="w")

entry_ref_width_pixels = tk.Entry(left_frame, width=10)
entry_ref_width_pixels.grid(row=5, column=1, padx=10, pady=5, sticky="w")

button_start = tk.Button(left_frame, text="Start Processing", command=start_processing)
button_start.grid(row=6, column=0, padx=10, pady=20, columnspan=2, sticky="w")

button_exit = tk.Button(left_frame, text="Exit", command=root.quit)
button_exit.grid(row=6, column=2, padx=10, pady=20, columnspan=2, sticky="w")

label_result = tk.Label(left_frame, font=("Helvetica", 14, "bold"))
label_result.grid(row=7, column=0, columnspan=4, padx=10, pady=5)

label_copyright = tk.Label(left_frame, text="Kiamid Co.")
label_copyright.grid(row=8, column=0, sticky="w")

label_mail = tk.Label(left_frame, text="Contact info: amar.salehi@gmail.com")
label_mail.grid(row=8, column=2, sticky="w")

# Create a frame for the right column
right_frame = tk.Frame(root)
right_frame.pack(side=tk.LEFT, padx=20, pady=20)  # <-- Do not set fill to BOTH

# Create labels for showing the main leaf photo and contours photo in the right column
label_leaf_image_title = tk.Label(right_frame, text="Your Original Photo:")
label_leaf_image_title.grid(row=0, column=0, sticky="w")

label_leaf_image = tk.Label(right_frame)
label_leaf_image.grid(row=1, column=0, padx=20, pady=20)

label_contours_image_title = tk.Label(right_frame, text="Processed Photo:")
label_contours_image_title.grid(row=2, column=0, sticky="w")

label_contours_image = tk.Label(right_frame)
label_contours_image.grid(row=3, column=0, padx=20, pady=20)

# Start the GUI event loop
root.mainloop()
