bl_info = {
    "name": "Sermotion",
    "author": "Serdar Eyüp ALTIN",
    "version": (1,0),
    "blender": (2,93,0),
    "location": "View3D > Toolbar > Sermotion",
    "description": "Imu sensor motion tracking",
    "warning": "",
    "wiki_url": "",
    "category": "Motion Tracking",
}

import bpy

class ServerConfiguration(bpy.types.Panel):
    bl_label = "Server Configuration"
    bl_idname = "P_Server_Configuration"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Sermotion"
    
    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.label(text="Add an object", icon = "OBJECT_DATAMODE")
        row = layout.row()
        
        row.operator("bpy.ops.font.textbox_add", icon = "CUBE")
        row = layout.row()
        row.operator("mesh.primitive_uv_sphere_add", icon = "SPHERE")

        
        
def register():
    bpy.utils.register_class(ServerConfiguration)

def unregister():
    bpy.utils.unregister_class(ServerConfiguration)
    

if __name__ == "__main__":
    register()