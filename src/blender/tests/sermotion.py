import bpy

bl_info = {
    "name": "Sermotions",
    "author": "Serdar Eyüp ALTIN",
    "version": (1, 0),
    "blender": (2, 93, 0),
    "location": "View3D > Toolbar > Sermotion",
    "description": "Imu sensor motion tracking",
    "warning": "",
    "wiki_url": "",
    "category": "Motion Tracking",
}


class MyProperties(bpy.types.PropertyGroup):
    my_string: bpy.props.StringProperty(name="Enter Text")
    my_float: bpy.props.FloatProperty(
        name="Enter Value", soft_min=0, soft_max=1000)
    my_enum: bpy.props.EnumProperty(
        name="Enumerator / Dropdown",
        description="sample text",
        items=[('OP1', "This is Option 1", ""),
               ('OP1', "This is Option 1", ""),
               ('OP1', "This is Option 1", "")
               ]
    )


class SERMOTIONS_PT_main(bpy.types.Panel):
    bl_category = "Sermotions2"
    bl_idname = "SERMOTIONS_PT_main"
    bl_label = "Server Configuration"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        obj = context.object

        layout.prop(mytool, "my_enum")
        layout.prop(mytool, "my_string")
        layout.prop(mytool, "my_float")

        row = layout.row()
        row.operator("sermotions.myop_operator")


class SERMOTIONS_OT_my_op(bpy.types.Operator):
    bl_label = "Operator"
    bl_idname = "sermotions.myop_operator"

    def execute(self, context):
        return {"FINISHED"}


classes = (
    MyProperties,
    SERMOTIONS_PT_main,
    SERMOTIONS_OT_my_op,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=MyProperties)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
