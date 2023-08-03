# kiamid Leaf Area Calculator

## Description
The Kiamid Leaf Area Calculator is a Python application designed to accurately estimate the leaf area of various plant leaves. The program follows a straightforward method using a reference image and size information to calculate the leaf area.

## How it Works
- Prepare a Reference Image:
Create a reference image with specific dimensions. For example, place a black square with a size of 100 x 100 pixels on a white background. This image will serve as a calibration reference for the leaf area calculation.

- Capture Reference and Leaf Images:
Capture a photo of the reference image and the leaves with a white background from a specific height. Ensure that both the reference image and the leaf images are taken from the same height.

- Provide Reference Image Size:
Specify the actual size of the printed square in centimeters, representing the dimensions of the reference image.

- Run the Kiamid Leaf Area Calculator:
Use the provided Python script, named leaf_area_calculator.py, to process the reference image and leaf images.

- Calculate Leaf Area:
The script will automatically calculate the leaf area for each leaf based on the reference image's size and the captured leaf images.

## How to Use

```
python leaf_area_calculator.py
```

The application will open a graphical user interface (GUI) where you can select the reference and leaf images and enter the required reference image size information.
Click the "Start Processing" button to calculate the leaf area.
The estimated leaf area for each leaf will be displayed, along with the original leaf image and a processed image showing the leaf contours.

## Example
Here's a step-by-step example of how to use the Kiamid Leaf Area Calculator:
1. Run the program.
2. Upload the reference photo **reference_image.jpg** and the leaf photo **leaf.jpg**.
3. Enter the Reference Length in cm **(This example is 15 cm)** and Reference Width in cm **(This example is 15 cm)**.
4. Enter the Reference Length in pixels **(This example is 1183 pixels)** and Reference Width in pixels **(This example is 1183 pixels)**.
5. Click on Start Processing.

## Important Notes
The accuracy of the leaf area estimation depends on properly capturing the reference image and leaf images from the same height and providing accurate reference image size information.
Ensure that the leaf images have a white background and are of good quality with sufficient lighting for accurate results.

## Contributing
If you find any issues or want to improve this project, feel free to create an issue or submit a pull request. Your contributions are highly appreciated!


