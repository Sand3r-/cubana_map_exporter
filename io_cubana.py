import bpy
import struct
import math

def get_color(obj):
    """Gets the base color from the object's material."""
    color = (1.0, 1.0, 1.0)  # Default to white

    if obj.active_material and obj.active_material.node_tree:
        for node in obj.active_material.node_tree.nodes:
            if node.type == 'BSDF_PRINCIPLED':
                color = node.inputs["Base Color"].default_value[:3]  # Ignore alpha
                break
    return color

def is_close(value, target):
    """Returns True if value is close to target within EPSILON."""
    return abs(value - target) < 0.1

def apply_rotation_and_get_dimensions(obj):
    """Resets rotation and adjusts dimensions accordingly."""
    rot_x, rot_y, rot_z = [math.degrees(angle) % 360 for angle in obj.rotation_euler]
    dim_x, dim_y, dim_z = obj.dimensions.x, obj.dimensions.y, obj.dimensions.z

    if is_close(rot_z, 90) or is_close(rot_z, 270):
        dim_x, dim_y = dim_y, dim_x  # Swap X and Y

    return dim_x, dim_y, dim_z

def get_cubes():
    """Extracts position, dimensions, and color of all selected mesh objects."""
    cubes = []

    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            # Convert Blender coordinates (-Z forward, Y up) to our system
            pos = obj.location
            position = (pos.x, pos.z, -pos.y)  # Convert Y and Z

            # Adjust dimensions for rotation
            size = apply_rotation_and_get_dimensions(obj)

            color = get_color(obj)

            cubes.append((position[0], position[1], position[2], size[0], size[1], size[2], color[0], color[1], color[2]))

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
    """Exports the scene to a .ctm file in an .obj-like format with fixed rotations and coordinate system."""
    with open(filepath, "w") as file:
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH':
                # Object name
                file.write(f"obj {obj.name}\n")

                # Adjusted Position
                pos = obj.location
                file.write(f"pos {pos.x:.6f} {pos.z:.6f} {-pos.y:.6f}\n")  # Convert coordinates

                # Adjusted Dimensions (taking rotation into account)
                dim_x, dim_y, dim_z = apply_rotation_and_get_dimensions(obj)
                file.write(f"dim {dim_x:.6f} {dim_z:.6f} {dim_y:.6f}\n")

                # Color
                color = get_color(obj)
                file.write(f"col {color[0]:.6f} {color[1]:.6f} {color[2]:.6f}\n")
                file.write("\n")  # Separate objects

    print(f"Exported .ctm to {filepath}")
