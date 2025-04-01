# app/modules/ingestion.py

import os

try:
    import pywavefront  # For parsing OBJ files (pip install PyWavefront)
except ImportError:
    pywavefront = None

try:
    import ifcopenshell  # For parsing IFC files (pip install ifcopenshell)
except ImportError:
    ifcopenshell = None


class ModelIngestion:
    """
    Loads and parses 3D building models from various formats (e.g., OBJ, IFC).
    For demonstration, only minimal stubs are shown.
    In practice, you'd store geometry, materials, or semantic data (rooms, walls, etc.).
    """

    def __init__(self):
        """
        Optionally configure details (e.g., default formats to handle).
        """
        pass

    def load_model(self, filepath):
        """
        Load a 3D building model from the given filepath. This function supports
        different file formats based on the extension. (OBJ, IFC, etc.)

        :param filepath: Path to the 3D model file.
        :return: A Python data structure representing the building model,
                 e.g. {
                   "geometry": ...,
                   "objects": [...],
                   "semantic_data": ...
                 }
        """

        if not os.path.exists(filepath):
            print(f"[ModelIngestion] File not found: {filepath}")
            return {"geometry": None, "objects": []}

        ext = os.path.splitext(filepath)[1].lower()

        if ext in [".obj"]:
            return self._load_obj(filepath)
        elif ext in [".ifc"]:
            return self._load_ifc(filepath)
        else:
            # Default or unsupported file
            print(f"[ModelIngestion] Unsupported file format: {ext}")
            return {"geometry": None, "objects": []}

    def _load_obj(self, filepath):
        """
        Use PyWavefront to load a .obj file. 
        This library can parse vertices, faces, materials, etc.
        """
        if pywavefront is None:
            print("[ModelIngestion] PyWavefront not installed. Returning stub.")
            return {"geometry": None, "objects": []}

        print(f"[ModelIngestion] Loading OBJ model from: {filepath}")
        scene = pywavefront.Wavefront(filepath, collect_faces=True)
        # scene.mesh_list contains the meshes. You can iterate and extract geometry.
        # For demonstration, let's say we store raw data in 'geometry'.

        # Example data structure:
        model_data = {
            "geometry": {
                "vertices": [],
                "faces": []
            },
            "objects": [],
            "format": "OBJ"
        }

        # Extracting vertices and faces from the wavefront scene (simplified approach)
        for name, mesh in scene.meshes.items():
            # mesh.vertices is a 1D list of floats [x1, y1, z1, x2, y2, z2, ...]
            vertices = []
            for i in range(0, len(mesh.vertices), 3):
                x = mesh.vertices[i]
                y = mesh.vertices[i + 1]
                z = mesh.vertices[i + 2]
                vertices.append((x, y, z))

            # If faces are collected, mesh.faces is a list of indices
            faces = mesh.faces  # Each is a tuple of vertex indices (e.g., (0, 1, 2))

            # We might store them in a sub-list
            model_data["geometry"]["vertices"].extend(vertices)
            model_data["geometry"]["faces"].extend(faces)

            # We can also track "objects" if the OBJ is subdivided by groups
            model_data["objects"].append({"name": name, "mesh": mesh})

        print(f"[ModelIngestion] OBJ loading complete. Found {len(scene.mesh_list)} mesh(es).")
        return model_data

    def _load_ifc(self, filepath):
        """
        Use ifcopenshell to load a .ifc (Industry Foundation Classes) file.
        IFC is a common format for architectural/engineering models.
        """
        if ifcopenshell is None:
            print("[ModelIngestion] ifcopenshell not installed. Returning stub.")
            return {"geometry": None, "objects": []}

        print(f"[ModelIngestion] Loading IFC model from: {filepath}")
        ifc_model = ifcopenshell.open(filepath)

        # IFC data can be very semantic (walls, windows, doors, etc.).
        # Typically, you'd traverse the IFC product hierarchy to extract geometry or metadata.
        # This is a minimal example:

        geometry_data = []
        objects_data = []

        # For example, let's iterate over building elements:
        for product in ifc_model.by_type("IfcProduct"):
            # product.is_a() might be 'IfcWall', 'IfcDoor', etc.
            # We could fetch geometry via ifcopenshell.geom.create_shape(settings, product),
            # if we have ifcopenshell's geometry module. For now, we'll store a stub.
            objects_data.append({
                "type": product.is_a(),
                "global_id": product.GlobalId,
                "name": product.Name
            })

        model_data = {
            "geometry": geometry_data,
            "objects": objects_data,
            "format": "IFC"
        }

        print(f"[ModelIngestion] IFC loading complete. Found {len(objects_data)} product(s).")
        return model_data
