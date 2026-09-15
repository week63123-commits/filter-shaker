"""
Filter Shaker - Image Filter Application with GUI
A Python application to apply various filters to images
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
import os
from filters import ImageFilters


class FilterShakerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Filter Shaker 🖼️")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        self.current_image = None
        self.original_image = None
        self.image_path = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Top frame for title
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        title_frame.pack(fill=tk.X, padx=0, pady=0)
        
        title_label = tk.Label(
            title_frame,
            text="Filter Shaker 🖼️",
            font=("Arial", 24, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        title_label.pack(pady=10)
        
        # Main container
        main_container = tk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Controls
        left_panel = tk.Frame(main_container, bg="#ecf0f1", width=250)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        
        # Right panel - Image display
        right_panel = tk.Frame(main_container, bg="white")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Controls in left panel
        self.setup_controls(left_panel)
        
        # Image display in right panel
        self.setup_image_display(right_panel)
    
    def setup_controls(self, parent):
        """Setup control panel"""
        control_label = tk.Label(
            parent,
            text="Controls",
            font=("Arial", 14, "bold"),
            bg="#ecf0f1"
        )
        control_label.pack(pady=10)
        
        # Select Image Button
        select_btn = tk.Button(
            parent,
            text="📁 Select Image",
            command=self.select_image,
            font=("Arial", 11),
            bg="#3498db",
            fg="white",
            padx=20,
            pady=10,
            relief=tk.RAISED,
            cursor="hand2"
        )
        select_btn.pack(pady=10, padx=15, fill=tk.X)
        
        # Filter Selection
        filter_label = tk.Label(
            parent,
            text="Filter Type:",
            font=("Arial", 10, "bold"),
            bg="#ecf0f1"
        )
        filter_label.pack(pady=(20, 5), padx=15, anchor=tk.W)
        
        self.filter_var = tk.StringVar(value="blur")
        filters = [
            ("Blur", "blur"),
            ("Gaussian Blur", "gaussian_blur"),
            ("Sharpen", "sharpen"),
            ("Edge Detection", "edge_detection"),
            ("Grayscale", "grayscale"),
            ("Sepia", "sepia"),
            ("Brightness", "brightness"),
            ("Contrast", "contrast"),
            ("Invert", "invert"),
            ("Emboss", "emboss"),
        ]
        
        for text, value in filters:
            rb = tk.Radiobutton(
                parent,
                text=text,
                variable=self.filter_var,
                value=value,
                font=("Arial", 9),
                bg="#ecf0f1",
                cursor="hand2"
            )
            rb.pack(anchor=tk.W, padx=20, pady=2)
        
        # Intensity/Parameter slider
        param_label = tk.Label(
            parent,
            text="Intensity:",
            font=("Arial", 10, "bold"),
            bg="#ecf0f1"
        )
        param_label.pack(pady=(20, 5), padx=15, anchor=tk.W)
        
        self.intensity_var = tk.DoubleVar(value=1.5)
        self.intensity_slider = tk.Scale(
            parent,
            from_=0.5,
            to=3.0,
            orient=tk.HORIZONTAL,
            variable=self.intensity_var,
            bg="#ecf0f1",
            fg="#2c3e50",
            length=200
        )
        self.intensity_slider.pack(padx=15, pady=5, fill=tk.X)
        
        # Apply Filter Button
        apply_btn = tk.Button(
            parent,
            text="✨ Apply Filter",
            command=self.apply_filter,
            font=("Arial", 11, "bold"),
            bg="#27ae60",
            fg="white",
            padx=20,
            pady=10,
            relief=tk.RAISED,
            cursor="hand2"
        )
        apply_btn.pack(pady=20, padx=15, fill=tk.X)
        
        # Reset Button
        reset_btn = tk.Button(
            parent,
            text="🔄 Reset",
            command=self.reset_image,
            font=("Arial", 11),
            bg="#e74c3c",
            fg="white",
            padx=20,
            pady=10,
            relief=tk.RAISED,
            cursor="hand2"
        )
        reset_btn.pack(pady=5, padx=15, fill=tk.X)
        
        # Save Button
        save_btn = tk.Button(
            parent,
            text="💾 Save Image",
            command=self.save_image,
            font=("Arial", 11),
            bg="#9b59b6",
            fg="white",
            padx=20,
            pady=10,
            relief=tk.RAISED,
            cursor="hand2"
        )
        save_btn.pack(pady=5, padx=15, fill=tk.X)
    
    def setup_image_display(self, parent):
        """Setup image display area"""
        self.image_label = tk.Label(
            parent,
            bg="white",
            text="No image selected\n\nClick 'Select Image' to begin",
            font=("Arial", 14),
            fg="#95a5a6"
        )
        self.image_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def select_image(self):
        """Select an image file"""
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"), ("All files", "*.*")]
        )
        
        if file_path:
            self.image_path = file_path
            self.original_image = cv2.imread(file_path)
            self.current_image = self.original_image.copy()
            self.display_image(self.current_image)
    
    def display_image(self, image):
        """Display image in GUI"""
        if image is None:
            return
        
        # Convert BGR to RGB for display
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Resize for display if too large
        height, width = image_rgb.shape[:2]
        max_width, max_height = 600, 500
        
        if width > max_width or height > max_height:
            ratio = min(max_width / width, max_height / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            image_rgb = cv2.resize(image_rgb, (new_width, new_height))
        
        # Convert to PIL Image
        pil_image = Image.fromarray(image_rgb)
        photo = ImageTk.PhotoImage(pil_image)
        
        # Update label
        self.image_label.config(image=photo, text="")
        self.image_label.image = photo
    
    def apply_filter(self):
        """Apply selected filter"""
        if self.current_image is None:
            messagebox.showwarning("Warning", "Please select an image first!")
            return
        
        try:
            filter_name = self.filter_var.get()
            intensity = self.intensity_var.get()
            
            filters = ImageFilters()
            
            if filter_name == "blur":
                self.current_image = filters.blur(self.original_image, int(intensity * 10 + 5))
            elif filter_name == "gaussian_blur":
                kernel_size = int(intensity * 10 + 5)
                if kernel_size % 2 == 0:
                    kernel_size += 1
                self.current_image = filters.gaussian_blur(self.original_image, kernel_size)
            elif filter_name == "sharpen":
                self.current_image = filters.sharpen(self.original_image, intensity)
            elif filter_name == "edge_detection":
                self.current_image = filters.edge_detection(self.original_image)
            elif filter_name == "grayscale":
                self.current_image = filters.grayscale(self.original_image)
            elif filter_name == "sepia":
                self.current_image = filters.sepia(self.original_image)
            elif filter_name == "brightness":
                self.current_image = filters.brightness(self.original_image, intensity)
            elif filter_name == "contrast":
                self.current_image = filters.contrast(self.original_image, intensity)
            elif filter_name == "invert":
                self.current_image = filters.invert(self.original_image)
            elif filter_name == "emboss":
                self.current_image = filters.emboss(self.original_image)
            
            self.display_image(self.current_image)
            messagebox.showinfo("Success", "Filter applied successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error applying filter: {str(e)}")
    
    def reset_image(self):
        """Reset to original image"""
        if self.original_image is not None:
            self.current_image = self.original_image.copy()
            self.display_image(self.current_image)
            messagebox.showinfo("Success", "Image reset to original!")
    
    def save_image(self):
        """Save the current filtered image"""
        if self.current_image is None:
            messagebox.showwarning("Warning", "No image to save!")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                cv2.imwrite(file_path, self.current_image)
                messagebox.showinfo("Success", f"Image saved successfully!\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Error saving image: {str(e)}")


def main():
    root = tk.Tk()
    app = FilterShakerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
