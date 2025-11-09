# FreeCAD Macro to build a SINGLE, ASSEMBLED probe
# This design follows the "no joints" table and is NOT MANUFACTURABLE.
import FreeCAD as App
import Part
from FreeCAD import Base

def build_flange(doc):
    """Creates the simple KF40 flange disk."""
    body = doc.addObject("PartDesign::Body", "Flange_Body")
    sketch = body.addNewObject("Sketcher::Sketch", "Sketch_Flange")
    sketch.Support = (doc.XY_Plane, [""])
    sketch.MapMode = "FlatFace"
    
    # 55mm OD, 41mm ID
    sketch.addGeometry(Part.Circle(Base.Vector(0,0,0), Base.Vector(0,0,1), 55.0/2), False)
    sketch.addGeometry(Part.Circle(Base.Vector(0,0,0), Base.Vector(0,0,1), 41.0/2), False)
    
    pad = body.addNewObject("PartDesign::Pad", "Pad_Flange")
    pad.Profile = sketch
    pad.Length = 5.0  # 5mm thick
    
    return body

def build_ss_tube(doc):
    """Creates the simple SS tube."""
    body = doc.addObject("PartDesign::Body", "SS_Tube_Body")
    sketch = body.addNewObject("Sketcher::Sketch", "Sketch_SS_Tube")
    sketch.Support = (doc.XY_Plane, [""])
    sketch.MapMode = "FlatFace"
    
    # 42.2mm OD, 39.2mm ID (1.5mm thickness)
    sketch.addGeometry(Part.Circle(Base.Vector(0,0,0), Base.Vector(0,0,1), 42.2/2), False)
    sketch.addGeometry(Part.Circle(Base.Vector(0,0,0), Base.Vector(0,0,1), 39.2/2), False)
    
    pad = body.addNewObject("PartDesign::Pad", "Pad_SS_Tube")
    pad.Profile = sketch
    pad.Length = 500.0  # 500mm long
    
    return body

def build_cu_tube(doc):
    """Creates the simple Cu tube."""
    body = doc.addObject("PartDesign::Body", "Cu_Tube_Body")
    sketch = body.addNewObject("Sketcher::Sketch", "Sketch_Cu_Tube")
    sketch.Support = (doc.XY_Plane, [""])
    sketch.MapMode = "FlatFace"
    
    # 42.2mm OD, 39.2mm ID (1.5mm thickness)
    sketch.addGeometry(Part.Circle(Base.Vector(0,0,0), Base.Vector(0,0,1), 42.2/2), False)
    sketch.addGeometry(Part.Circle(Base.Vector(0,0,0), Base.Vector(0,0,1), 39.2/2), False)
    
    pad = body.addNewObject("PartDesign::Pad", "Pad_Cu_Tube")
    pad.Profile = sketch
    pad.Length = 300.0  # 300mm long
    
    return body

def build_cap(doc):
    """Creates the simple solid cap."""
    body = doc.addObject("PartDesign::Body", "Cu_Cap_Body")
    sketch = body.addNewObject("Sketcher::Sketch", "Sketch_Cap")
    sketch.Support = (doc.XY_Plane, [""])
    sketch.MapMode = "FlatFace"
    
    # 42.2mm OD (Solid)
    sketch.addGeometry(Part.Circle(Base.Vector(0,0,0), Base.Vector(0,0,1), 42.2/2), False)
    
    pad = body.addNewObject("PartDesign::Pad", "Pad_Cap")
    pad.Profile = sketch
    pad.Length = 1.5  # 1.5mm thick
    
    return body

# ==============================================================================
# --- MAIN EXECUTION ---
# ==============================================================================
if __name__ == "__main__":
    
    # Create one single document
    doc = App.newDocument("Probe_Assembled")
    App.Console.PrintMessage("Creating new document 'Probe_Assembled'...\n")

    # 1. Create Flange at origin
    flange_body = build_flange(doc)
    flange_body.Placement = App.Placement(App.Vector(0, 0, 0), App.Rotation(0, 0, 0, 1))
    App.Console.PrintMessage("Flange created.\n")

    # 2. Create SS Tube and place it BELOW the flange
    ss_body = build_ss_tube(doc)
    ss_body.Placement = App.Placement(App.Vector(0, 0, -500.0), App.Rotation(0, 0, 0, 1))
    # Move it so its top face touches the flange's bottom face
    ss_body.Placement.Base.z = -5.0 # Flange thickness
    App.Console.PrintMessage("SS Tube created and placed.\n")

    # 3. Create Cu Tube and place it BELOW the SS Tube
    cu_body = build_cu_tube(doc)
    cu_body.Placement = App.Placement(App.Vector(0, 0, -300.0), App.Rotation(0, 0, 0, 1))
    # Move it so its top face touches the SS tube's bottom face
    cu_body.Placement.Base.z = -5.0 - 500.0 # Flange + SS Tube
    App.Console.PrintMessage("Cu Tube created and placed.\n")

    # 4. Create Cap and place it BELOW the Cu Tube
    cap_body = build_cap(doc)
    cap_body.Placement = App.Placement(App.Vector(0, 0, -1.5), App.Rotation(0, 0, 0, 1))
    # Move it so its top face touches the Cu tube's bottom face
    cap_body.Placement.Base.z = -5.0 - 500.0 - 300.0 # Flange + SS + Cu
    App.Console.PrintMessage("Cu Cap created and placed.\n")
    
    doc.recompute()
    App.Gui.ActiveDocument.ActiveView.fitAll()
    App.Console.PrintMessage("============================================\n")
    App.Console.PrintMessage("SUCCESS! Your assembled probe is on the screen.\n")
