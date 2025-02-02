import bpy
import os
from bpy_extras.io_utils import ExportHelper
from .io_cubana import export_to_cbm, export_to_ctm

class EXPORT_OT_CubanaCBM(bpy.types.Operator, ExportHelper):
    """Export Cubana Binary Map (.cbm)"""
    bl_idname = "export_scene.cubana_cbm"
    bl_label = "Export Cubana Binary Map"
    filename_ext = ".cbm"

    def execute(self, context):
        export_to_cbm(self.filepath)
        return {'FINISHED'}

class EXPORT_OT_CubanaCTM(bpy.types.Operator, ExportHelper):
    """Export Cubana Textual Map (.ctm)"""
    bl_idname = "export_scene.cubana_ctm"
    bl_label = "Export Cubana Textual Map"
    filename_ext = ".ctm"

    def execute(self, context):
        export_to_ctm(self.filepath)
        return {'FINISHED'}
