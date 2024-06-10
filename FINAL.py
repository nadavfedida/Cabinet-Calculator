import csv
import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime
import os

class Component:
    def __init__(self, width, height, quantity=1, component_type="Component", material="16mm Melamine"):
        self.width = width
        self.height = height
        self.quantity = quantity
        self.component_type = component_type
        self.material = material

    def __str__(self):
        return f"Width: {self.width}, Height: {self.height}, Quantity: {self.quantity}"

class Door(Component):
    def __init__(self, width, height, quantity=1):
        super().__init__(width, height, quantity, "Door", "18mm Melamine")

class Drawer(Component):
    def __init__(self, width, height, quantity=1):
        super().__init__(width, height, quantity, "Drawer", "18mm Melamine")

class EndPanel(Component):
    def __init__(self, width, height, quantity=1, custom_name="End Panel"):
        super().__init__(width, height, quantity, custom_name, "18mm Melamine")

class Cabinet:
    def __init__(self, width, depth, height, cabinet_type, door_bottom_height=None, end_panel_name=None):
        self.width = width
        self.depth = depth
        self.height = height
        self.cabinet_type = cabinet_type
        self.components = []
        self.thickness = 16  
        self.door_thickness = 18  
        self.door_bottom_height = door_bottom_height
        self.end_panel_name = end_panel_name
        self.calculate_components()

    def calculate_components(self):
        if self.cabinet_type == "Tall Boy with 2 Doors and 3 Drawers" and self.door_bottom_height is not None:
            self.calculate_tall_boy_with_doors_and_drawers()
        elif self.cabinet_type == "End Panel":
            self.calculate_end_panel()
        else:
            calculations = {
                "Undermount Cabinet with 2 Doors": self.calculate_undermount_cabinet_with_2_doors,
                "Undermount Cabinet with 1 Door": self.calculate_undermount_cabinet_with_1_door,
                "Undermount Cabinet with 3 Drawers": self.calculate_undermount_cabinet_with_3_drawers,
                "Undermount Cabinet with 4 Drawers": self.calculate_undermount_cabinet_with_4_drawers,
                "Tall Boy with Full Length Doors": self.calculate_tall_boy_with_full_length_doors,
                "Overhead Cabinet with 1 Door": self.calculate_overhead_cabinet_with_1_door,
                "Overhead Cabinet with 2 Doors": self.calculate_overhead_cabinet_with_2_doors,
            }

            if self.cabinet_type in calculations:
                calculations[self.cabinet_type]()
        
        if self.cabinet_type != "End Panel":
            if "Tall Boy" in self.cabinet_type:
                shelf_quantity = 3 
            else:
                shelf_quantity = 1  
            self.add_component(Component(self.width - 2 * self.thickness, self.depth - self.thickness, shelf_quantity, "Shelf"))

    def add_component(self, component):
        self.components.append(component)

    def calculate_undermount_cabinet_with_2_doors(self):
        self.add_component(Component(self.width - 2 * self.thickness, 100, 2, "Top"))
        self.add_component(Component(self.width - 2 * self.thickness, self.depth - self.thickness, 1, "Bottom"))
        self.add_component(Component(self.width, self.height, 1, "Back"))
        self.add_component(Component(self.depth - self.thickness, self.height, 2, "Side"))
        self.add_component(Door((self.width - 1.5 - 1.5 - 3) / 2, self.height - 3, 2))

    def calculate_undermount_cabinet_with_1_door(self):
        self.add_component(Component(self.width - 2 * self.thickness, 100, 2, "Top"))
        self.add_component(Component(self.width - 2 * self.thickness, self.thickness, 1, "Bottom"))
        self.add_component(Component(self.width, self.height, 1, "Back"))
        self.add_component(Component(self.depth - self.thickness, self.height, 2, "Side"))
        self.add_component(Door(self.width - 3, self.height - 3))

    def calculate_undermount_cabinet_with_3_drawers(self):
        self.add_component(Component(self.width - 2 * self.thickness, 100, 2, "Top"))
        self.add_component(Component(self.width - 2 * self.thickness, self.depth - self.thickness, 1, "Bottom"))
        self.add_component(Component(self.width, self.height, 1, "Back"))
        self.add_component(Component(self.depth - self.thickness, self.height, 2, "Side"))
        self.add_component(Drawer(self.width - 5, (self.depth - self.thickness - 9) / 3, 3))

    def calculate_undermount_cabinet_with_4_drawers(self):
        self.add_component(Component(self.width - 2 * self.thickness, 100, 2, "Top"))
        self.add_component(Component(self.width - 2 * self.thickness, self.depth - self.thickness, 1, "Bottom"))
        self.add_component(Component(self.width, self.height, 1, "Back"))
        self.add_component(Component(self.depth - self.thickness, self.height, 2, "Side"))
        self.add_component(Drawer(self.width - 5, (self.depth - self.thickness - 12) / 4, 4))

    def calculate_tall_boy_with_full_length_doors(self):
        self.add_component(Component(self.width - 2 * self.thickness, self.depth - self.thickness, 1, "Top"))
        self.add_component(Component(self.width - 2 * self.thickness, self.depth - self.thickness, 1, "Bottom"))
        self.add_component(Component(self.width, self.height, 1, "Back"))
        self.add_component(Component(self.depth - self.thickness, self.height - 2 * self.thickness, 2, "Side"))
        self.add_component(Door((self.width - 2 * self.thickness - 3) / 2, self.height - 2, 2))

    def calculate_tall_boy_with_doors_and_drawers(self):
        self.add_component(Component(self.width - 2 * self.thickness, self.depth - self.thickness, 1, "Top"))
        self.add_component(Component(self.width - 2 * self.thickness, self.depth - self.thickness, 1, "Bottom"))
        self.add_component(Component(self.width, self.height, 1, "Back"))
        self.add_component(Component(self.depth - self.thickness, self.height - 2 * self.thickness, 2, "Side"))
        self.add_component(Door((self.width - 5) / 2, self.height - self.door_bottom_height))
        self.add_component(Drawer(self.width - 5, (self.door_bottom_height - 9) / 3, 3))

    def calculate_overhead_cabinet_with_1_door(self):
        self.add_component(Component(self.width - 2 * self.thickness, self.depth - self.thickness, 1, "Top"))
        self.add_component(Component(self.width - 2 * self.thickness, self.depth - self.thickness, 1, "Bottom"))
        self.add_component(Component(self.width, self.height, 1, "Back "))
        self.add_component(Component(self.depth - self.thickness, self.height - 2 * self.thickness, 2, "Side"))
        self.add_component(Door(self.width - 2 * self.thickness - 3, self.height+ 28))

    def calculate_overhead_cabinet_with_2_doors(self):
        self.add_component(Component(self.width - 2 * self.thickness, self.depth - self.thickness, 1, "Top"))
        self.add_component(Component(self.width - 2 * self.thickness, self.depth - self.thickness, 1, "Bottom"))
        self.add_component(Component(self.width, self.height, 1, "Back"))
        self.add_component(Component(self.depth - self.thickness, self.height - 2 * self.thickness, 2, "Side"))
        self.add_component(Door((self.width - 2 * self.thickness - 4) / 2, self.height + 28, 2))

    def calculate_end_panel(self):
        if self.end_panel_name:
            self.add_component(EndPanel(self.width, self.height, custom_name=self.end_panel_name))
        else:
            self.add_component(EndPanel(self.width, self.height))

class CabinetCalculator:
    def __init__(self, master):
        self.master = master
        self.master.title("Cabinet Calculator")

        self.job_name_label = tk.Label(master, text="Job Name:")
        self.job_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.job_name_entry = tk.Entry(master)
        self.job_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.menu_label = tk.Label(master, text="Select Cabinet Type:", font=('Arial', 12))
        self.menu_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.cabinet_type_var = tk.StringVar()
        self.cabinet_type_var.set("Undermount Cabinet with 2 Doors")
        self.cabinet_types = [
            "Undermount Cabinet with 2 Doors",
            "Undermount Cabinet with 1 Door",
            "Undermount Cabinet with 3 Drawers",
            "Undermount Cabinet with 4 Drawers",
            "Tall Boy with Full Length Doors",
            "Tall Boy with 2 Doors and 3 Drawers",
            "Overhead Cabinet with 1 Door",
            "Overhead Cabinet with 2 Doors",
            "End Panel"
        ]
        self.cabinet_menu = tk.OptionMenu(master, self.cabinet_type_var, *self.cabinet_types)
        self.cabinet_menu.grid(row=1, column=1, padx=10, pady=5)

        self.height_label = tk.Label(master, text="Height (mm):")
        self.height_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.height_entry = tk.Entry(master)
        self.height_entry.grid(row=2, column=1, padx=10, pady=5)

        self.width_label = tk.Label(master, text="Width (mm):")
        self.width_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.width_entry = tk.Entry(master)
        self.width_entry.grid(row=3, column=1, padx=10, pady=5)

        self.depth_label = tk.Label(master, text="Depth (mm):")
        self.depth_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.depth_entry = tk.Entry(master)
        self.depth_entry.grid(row=4, column=1, padx=10, pady=5)

        self.add_button = tk.Button(master, text="Add Cabinet", command=self.add_cabinet)
        self.add_button.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        self.cabinet_listbox = tk.Listbox(master, width=50)
        self.cabinet_listbox.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

        self.preview_text = tk.Text(master, height=40, width=80)
        self.preview_text.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

        self.export_button = tk.Button(master, text="Export to CSV", command=self.export_to_csv)
        self.export_button.grid(row=8, column=0, columnspan=2, padx=10, pady=5)

        self.cabinets = []

    def add_cabinet(self):
        try:
            width = float(self.width_entry.get())
            depth = float(self.depth_entry.get()) if self.cabinet_type_var.get() != "End Panel" else 0
            height = float(self.height_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numerical values for width, depth, and height.")
            return

        cabinet_type = self.cabinet_type_var.get()
        door_bottom_height = None
        end_panel_name = None
        
        if cabinet_type == "Tall Boy with 2 Doors and 3 Drawers":
            door_bottom_height = self.ask_door_bottom_height()
            if door_bottom_height is None:
                return  

        if cabinet_type == "End Panel":
            end_panel_name = self.ask_end_panel_name()
            if end_panel_name is None:
                return

        cabinet = Cabinet(width, depth, height, cabinet_type, door_bottom_height, end_panel_name)
        self.cabinets.append(cabinet)
        self.update_cabinet_listbox()
        self.update_preview()

    def ask_end_panel_name(self):
        panel_name = simpledialog.askstring("Input", "Enter the name for the end panel:")
        return panel_name
             
   
    def ask_door_bottom_height(self):
        door_bottom_height = simpledialog.askfloat("Tall Boy with Doors and Drawers", "Enter the height to the bottom of the doors (mm):")
        return door_bottom_height

    def update_cabinet_listbox(self):
        self.cabinet_listbox.delete(0, tk.END)
        for i, cabinet in enumerate(self.cabinets, start=1):
            self.cabinet_listbox.insert(tk.END, f"Cabinet {i}: {cabinet.cabinet_type}")

    def update_preview(self):
        self.preview_text.delete(1.0, tk.END)  
        self.preview_text.insert(tk.END, "MF RENOVATIONS\n")
        job_name = self.job_name_entry.get()
        if job_name:
            self.preview_text.insert(tk.END, f"JOB NAME: {job_name}\n")
        self.preview_text.insert(tk.END, "Cabinet,Component,Quantity,Length,Width,Material\n")

        for i, cabinet in enumerate(self.cabinets, start=1):
            for component in cabinet.components:
                self.preview_text.insert(tk.END, f"Unit {i},{component.component_type},{component.quantity},{component.width},{component.height},{component.material}\n")

    def export_to_csv(self):
        if not self.cabinets:
            messagebox.showwarning("Warning", "No cabinets added yet.")
            return

        job_name = self.job_name_entry.get()  

        timestamp = datetime.now().strftime("%d-%m-%y_%H-%M")

        data_folder = os.path.join(os.path.dirname(__file__), "DATA")

        if not os.path.exists(data_folder):
            os.makedirs(data_folder)

        filename = os.path.join(data_folder, f"{job_name}_cabinets_{timestamp}.csv")

        with open(filename, 'w', newline='') as csvfile:
            csvfile.write("MF RENOVATIONS\n")  
            if job_name:
                csvfile.write(f"JOB NAME: {job_name}\n") 

            fieldnames = ['Unit', 'Component', 'Quantity', 'Length', 'Width', 'Material']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for i, cabinet in enumerate(self.cabinets, start=1):
                for component in cabinet.components:
                    length = f"{component.width}"
                    width = f"{component.height}"
                    material = f"{component.material}"
                    
                    if component.component_type == "Top":
                        length += " X"

                    elif component.component_type == "Bottom":
                        length += " X"

                    elif component.component_type == "Side":
                        width += " X"

                    elif component.component_type == "Door":
                        length += " XX"
                        width += " XX"

                    elif component.component_type == "Drawer":
                        length += " XX"
                        width += " XX"

                    elif component.component_type == "Shelf":
                        length += " X"

                    elif component.component_type != "Back" :
                        length += " XX"
                        width += " XX"



                    writer.writerow({'Unit': f'Unit {i}', 'Component': component.component_type, 'Quantity': component.quantity, 'Length': length, 'Width': width, 'Material': material})

        messagebox.showinfo("Success", f"Cabinet data exported to '{filename}'.")
        self.master.destroy() 

def main():
    root = tk.Tk()
    app = CabinetCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()


