# FreeCAD Macro to build a SINGLE, ASSEMBLED probe
# This design follows the "no joints" table and is NOT MANUFACTURABLE.
# VERSION 11: Builds the 3D model and PRINTS a summary of all dimensions.

import FreeCAD as App
import Part
from FreeCAD import Base

def make_tube_shape(od, id, height):
    """Helper function to create a tube shape using a boolean cut."""
    if id > 0:
        outer_cyl = Part.makeCylinder(od / 2, height)
        inner_cyl = Part.makeCylinder(id / 2, height)
        tube_shape = outer_cyl.cut(inner_cyl)
    else:
        # Solid cylinder if ID is 0
        tube_shape = Part.makeCylinder(od / 2, height)
    return tube_shape

# ==============================================================================
# --- MAIN EXECUTION ---
# ==============================================================================
if __name__ == "__main__":
    
    doc = App.newDocument("Probe_Assembled")
    App.Console.PrintMessage("Creating new document 'Probe_Assembled'...\n")

    # --- Part 1: Create Flange at origin ---
    flange_height = 5.0
    flange_od = 55.0
    flange_id = 41.0
    flange_shape = make_tube_shape(flange_od, flange_id, flange_height)
    flange_obj = Part.show(flange_shape, "Flange")
    flange_obj.ViewObject.ShapeColor = (0.75, 0.75, 0.75) # SS Color
    App.Console.PrintMessage("Flange created.\n")

    # --- Part 2: Create SS Tube ---
    ss_tube_height = 500.0
    ss_tube_od = 42.2
    ss_tube_id = 39.2 # 42.2 - 2 * 1.5
    ss_tube_shape = make_tube_shape(ss_tube_od, ss_tube_id, ss_tube_height)
    ss_tube_obj = Part.show(ss_tube_shape, "SS_Tube")
    ss_tube_obj.ViewObject.ShapeColor = (0.75, 0.75, 0.75) # SS Color
    ss_tube_obj.Placement = App.Placement(App.Vector(0, 0, -ss_tube_height), App.Rotation(0, 0, 0, 1))
    App.Console.PrintMessage("SS Tube created and placed.\n")

    # --- Part 3: Create Cu Tube ---
    cu_tube_height = 300.0
    cu_tube_od = 42.2
    cu_tube_id = 39.2 # 42.2 - 2 * 1.5
    cu_tube_shape = make_tube_shape(cu_tube_od, cu_tube_id, cu_tube_height)
    cu_tube_obj = Part.show(cu_tube_shape, "Cu_Tube")
    copper_color = (0.84, 0.49, 0.25) # (214, 125, 64)
    cu_tube_obj.ViewObject.ShapeColor = copper_color
    cu_tube_obj.Placement = App.Placement(App.Vector(0, 0, -ss_tube_height - cu_tube_height), App.Rotation(0, 0, 0, 1))
    App.Console.PrintMessage("Cu Tube created and placed.\n")

    # --- Part 4: Create Cap ---
    cap_height = 1.5
    cap_od = 42.2
    cap_shape = make_tube_shape(cap_od, 0, cap_height) # ID = 0 for solid
    cap_obj = Part.show(cap_shape, "Cu_Cap")
    cap_obj.ViewObject.ShapeColor = copper_color
    cap_obj.Placement = App.Placement(App.Vector(0, 0, -ss_tube_height - cu_tube_height - cap_height), App.Rotation(0, 0, 0, 1))
    App.Console.PrintMessage("Cu Cap created and placed.\n")
    
    doc.recompute()
    App.Gui.ActiveDocument.ActiveView.fitAll()
    
    App.Console.PrintMessage("============================================\n")
    App.Console.PrintMessage("SUCCESS! Your assembled probe is on the screen.\n")
    App.Console.PrintMessage("============================================\n\n")
    App.Console.PrintMessage("--- FINAL PROBE DIMENSIONS (mm) ---\n\n")
    
    # Print all dimensions
    App.Console.PrintMessage(f"1. KF 40 FLANGE\n   OD: {flange_od}, ID: {flange_id}, Length: {flange_height}\n")
    App.Console.PrintMessage(f"2. SS TUBE\n   OD: {ss_tube_od}, ID: {ss_tube_id}, Length: {ss_tube_height}\n")
    App.Console.PrintMessage(f"3. CU TUBE\n   OD: {cu_tube_od}, ID: {cu_tube_id}, Length: {cu_tube_height}\n")
    App.Console.PrintMessage(f"4. CU CAP\n   OD: {cap_od}, ID: 0.0, Length: {cap_height}\n")
    total_length = flange_height + ss_tube_height + cu_tube_height + cap_height
    App.Console.PrintMessage(f"--------------------------------------------\n   TOTAL PROBE LENGTH: {total_length} mm\n")
