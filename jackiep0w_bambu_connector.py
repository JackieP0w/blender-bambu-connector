import bpy
import subprocess
import os
import sys

bl_info = {
    "name": "JackieP0w's Bambu Connector",
    "author": "JackieP0w",
    "version": (1, 8),
    "blender": (3, 6, 0),
    "location": "View3D > Sidebar > 3D Print",
    "description": "Sending your cute models to the slicer with love! ✨",
    "category": "Import-Export",
}

# --- KAWAII ASCII ART ---
KAWAII_ART = r"""
      (\(\ 
     ( • .•)  ✨ "Ready to print!"
     o__(" )(" ) 
    
    ✧*。JackieP0w's Slicer Magic ✧*。
"""

def get_default_path():
    if sys.platform == "darwin":
        return "/Applications/BambuStudio.app/Contents/MacOS/BambuStudio"
    return r"C:\Program Files\Bambu Studio\bambu-studio.exe"

class BambuConnectorPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    
    executable_path: bpy.props.StringProperty(
        name="Slicer Path 🌸",
        subtype='FILE_PATH',
        default=get_default_path(),
        description="Where does your slicer live? (OrcaSlicer works too!)"
    )

    def draw(self, context):
        layout = self.layout
        
        # Super cute header
        box = layout.box()
        col = box.column(align=True)
        for line in KAWAII_ART.split('\n'):
            col.label(text=line)
            
        layout.separator()
        layout.prop(self, "executable_path")
        
        # Friendly instructions
        box = layout.box()
        box.label(text="Quick Setup Guide 🐾", icon='HEART')
        col = box.column(align=True)
        col.label(text="• Windows: Find your .exe file! (Usually in Program Files)")
        col.label(text="• macOS: Peek inside the .app bundle (Contents/MacOS/BambuStudio)")
        col.label(text="• To stay in one window: Enable 'Keep only one instance' in Slicer Prefs! ✨")

class OBJECT_OT_SendToBambu(bpy.types.Operator):
    bl_idname = "object.send_to_bambu"
    bl_label = "Send to Slicer"
    
    use_visible: bpy.props.BoolProperty(default=False)

    def execute(self, context):
        prefs = context.preferences.addons[__name__].preferences
        slicer_path = prefs.executable_path
        
        if not os.path.exists(slicer_path):
            self.report({'ERROR'}, "Oh no! Slicer not found... check the path! ｡ﾟ･ (>﹏<) ･ﾟ｡")
            return {'CANCELLED'}

        temp_file = os.path.join(bpy.app.tempdir, "jackiep0w_kawaii_export.3mf")

        try:
            # Scale 1000.0 makes the model big and happy for the slicer!
            bpy.ops.wm.wm_3mf_export(
                filepath=temp_file,
                export_selected=not self.use_visible,
                global_scale=1000.0 
            )
        except:
            temp_file = temp_file.replace(".3mf", ".stl")
            bpy.ops.wm.stl_export(filepath=temp_file, export_selected_objects=not self.use_visible, global_scale=1000.0)

        try:
            subprocess.Popen([slicer_path, temp_file])
            self.report({'INFO'}, "Model sent to Slicer with love! (〃＾▽＾〃) ✨")
        except Exception as e:
            self.report({'ERROR'}, f"Something went wrong... {str(e)} (╥﹏╥)")

        return {'FINISHED'}

class VIEW3D_PT_BambuPanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = '3D Print'
    bl_label = "JackieP0w's Slicer ✨"

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.scale_y = 1.4
        
        # Cute button icons
        op_sel = col.operator("object.send_to_bambu", text="Send Selected 🎀", icon='SELECT_SET')
        op_sel.use_visible = False
        
        op_vis = col.operator("object.send_to_bambu", text="Send All Visible 🌸", icon='HIDE_OFF')
        op_vis.use_visible = True

def register():
    bpy.utils.register_class(BambuConnectorPreferences)
    bpy.utils.register_class(OBJECT_OT_SendToBambu)
    bpy.utils.register_class(VIEW3D_PT_BambuPanel)

def unregister():
    bpy.utils.unregister_class(BambuConnectorPreferences)
    bpy.utils.unregister_class(OBJECT_OT_SendToBambu)
    bpy.utils.unregister_class(VIEW3D_PT_BambuPanel)

if __name__ == "__main__":
    register()