# FreeCAD Macro to build a SINGLE, ASSEMBLED probe
# This design follows the "no joints" table and is NOT MANUFACTURABLE.
# VERSION 7: Adds color to the copper parts.

import FreeCAD as App
import Part
from FreeCAD import Base

def make_tube_shape(od, id, height):
    """Helper function to create a tube shape using a boolean cut."""
    outer_cyl = Part.makeCylinder(od / 2, height)
    inner_cyl = Part.makeCylinder(id / 2, height)
    tube_shape = outer_cyl.cut(inner_cyl)
    return tube_shape

# ==============================================================================
# --- MAIN EXECUTION ---
# ==============================================================================
if __name__ == "__main__":
    
    doc = App.newDocument("Probe_Assembled")
    App.Console.PrintMessage("Creating new document 'Probe_Assembled'...\n")

    # --- Part 1: Create Flange at origin ---
    flange_height = 5.0
    flange_shape = make_tube_shape(55.0, 41.0, flange_height)
    flange_obj = Part.show(flange_shape, "Flange")
    # Set Flange color to Stainless Steel (light gray)
    flange_obj.ViewObject.ShapeColor = (0.75, 0.75, 0.75)
    flange_obj.ViewObject.DiffuseColor = (0.75, 0.75, 0.75)
    App.Console.PrintMessage("Flange created.\n")

    # --- Part 2: Create SS Tube ---
    ss_tube_height = 500.0
    ss_tube_shape = make_tube_shape(42.2, 39.2, ss_tube_height)
    ss_tube_obj = Part.show(ss_tube_shape, "SS_Tube")
    
    # Set SS Tube color to Stainless Steel (light gray)
    ss_tube_obj.ViewObject.ShapeColor = (0.75, 0.75, 0.75)
    ss_tube_obj.ViewObject.DiffuseColor = (0.75, 0.75, 0.75)
    
    # Placement
    ss_tube_obj.Placement = App.Placement(App.Vector(0, 0, -ss_tube_height), App.Rotation(0, 0, 0, 1))
    App.Console.PrintMessage("SS Tube created and placed.\n")

    # --- Part 3: Create Cu Tube ---
    cu_tube_height = 300.0
    cu_tube_shape = make_tube_shape(42.2, 39.2, cu_tube_height)
    cu_tube_obj = Part.show(cu_tube_shape, "Cu_Tube")
    
    # *** SET COPPER COLOR ***
    # RGB color (214, 125, 64) normalized to (0-1)
    copper_color = (0.84, 0.49, 0.25)
    cu_tube_obj.ViewObject.ShapeColor = copper_color
    cu_tube_obj.ViewObject.DiffuseColor = copper_color
    
    # Placement
    cu_tube_obj.Placement = App.Placement(App.Vector(0, 0, -ss_tube_height - cu_tube_height), App.Rotation(0, 0, 0, 1))
    App.Console.PrintMessage("Cu Tube created and placed.\n")

    # --- Part 4: Create Cap ---
    cap_height = 1.5
    cap_shape = Part.makeCylinder(42.2 / 2, cap_height)
    cap_obj = Part.show(cap_shape, "Cu_Cap")
    
    # *** SET COPPER COLOR ***
    cap_obj.ViewObject.ShapeColor = copper_color
    cap_obj.ViewObject.DiffuseColor = copper_color
    
    # Placement
    cap_obj.Placement = App.Placement(App.Vector(0, 0, -ss_tube_height - cu_tube_height - cap_height), App.Rotation(0, 0, 0, 1))
    App.Console.PrintMessage("Cu Cap created and placed.\n")
    
    doc.recompute()
    App.Gui.ActiveDocument.ActiveView.fitAll()
    App.Console.PrintMessage("============================================\n")
    App.Console.PrintMessage("SUCCESS! Your colored probe is on the screen.\n")
