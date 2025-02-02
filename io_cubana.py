import bpy
import struct

def get_color(obj):
    # Default color (white) if no material is found
    color = (1.0, 1.0, 1.0)
    # Get base colour from Principled BSDF
    if obj.active_material and obj.active_material.node_tree \
        and obj.active_material.node_tree.nodes \
        and "Principled BSDF" in obj.active_material.node_tree.nodes:
        node = obj.active_material.node_tree.nodes["Principled BSDF"]
        color = node.inputs["Base Color"].default_value[:3] # Ignore alpha
    return color

def get_cubes():
    """Extracts position, dimensions, and color of all selected mesh objects."""
    cubes = []

    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            pos = obj.location
            size = obj.dimensions
            color = get_color(obj)

            cubes.append((pos.x, pos.y, pos.z, size.x, size.y, size.z, color[0], color[1], color[2]))

    return cubes

def export_to_cbm(filepath):
    """Exports the selected cubes to a .cbm (binary format)."""
    cubes = get_cubes()

    with open(filepath, "wb") as f:
        f.write(struct.pack("I", len(cubes)))  # Store number of cubes
        for cube in cubes:
            f.write(struct.pack("fffffffff", *cube))  # 9 floats per cube

    print(f"Exported {len(cubes)} cubes to {filepath}")

def export_to_ctm(filepath):
    """Exports the scene to a .ctm file in an .obj-like format."""
    with open(filepath, "w") as file:
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH':
                # Object name
                file.write(f"obj {obj.name}\n")

                # Position
                pos = obj.location
                file.write(f"pos {pos.x:.6f} {pos.y:.6f} {pos.z:.6f}\n")

                # Dimensions
                dim = obj.dimensions
                file.write(f"dim {dim.x:.6f} {dim.y:.6f} {dim.z:.6f}\n")

                # Color
                color = get_color(obj)
                file.write(f"col {color[0]:.6f} {color[1]:.6f} {color[2]:.6f}\n")
                file.write("\n")  # Separate objects

    print(f"Exported .ctm to {filepath}")
