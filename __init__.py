bl_info = {
    "name": "Cubana Map Exporter",
    "author": "Michał Gallus",
    "version": (1, 0, 0),
    "blender": (4, 2, 0),
    "location": "File > Export",
    "description": "Exports current scene to Cubana Map format (.cbm / .ctm)",
    "category": "Import-Export",
}

import bpy
from .export_cubana import EXPORT_OT_CubanaCBM, EXPORT_OT_CubanaCTM

def menu_func_export(self, context):
    self.layout.operator(EXPORT_OT_CubanaCBM.bl_idname, text="Cubana Binary Map (.cbm)")
    self.layout.operator(EXPORT_OT_CubanaCTM.bl_idname, text="Cubana Textual Map (.ctm)")

def register():
    bpy.utils.register_class(EXPORT_OT_CubanaCBM)
    bpy.utils.register_class(EXPORT_OT_CubanaCTM)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)

def unregister():
    bpy.utils.unregister_class(EXPORT_OT_CubanaCBM)
    bpy.utils.unregister_class(EXPORT_OT_CubanaCTM)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)

if __name__ == "__main__":
    register()
