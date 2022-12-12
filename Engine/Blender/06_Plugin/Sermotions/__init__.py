import bpy
import json
import os

bl_info = {
    "name": "Sermotions",
    "author": "Serdar Eyüp ALTIN",
    "version": (1, 0, 0),
    "version_type": "alpha",
    "blender": (3, 40, 0),
    "location": "View3D > Toolbar > Sermotion",
    "description": "Imu sensor motion tracking",
    "warning": "",
    "wiki_url": "",
    "category": "Motion Tracking",
}


class Preset(object):
    preset = {
        'file': {
            'config': 'config.conf'
        }
    }

    def __init__(self):
        self.file = self.File(self.preset['file'])

    def __repr__(self):
        return repr(self.preset)

    class File(object):

        def __init__(self, value):
            self.file = value

        def __repr__(self) -> str:
            return repr(self.file)

        @property
        def config(self):
            return self.file['config']


preset = Preset()


class Config(object):
    config = {
        'server': {
            'ip': '0.0.0.0',
            'port': '4455'
        }
    }
    config_file = preset.file.config

    def __init__(self):
        self.read()
        self.server = self.Server(self.config['server'])

    def __repr__(self):
        return repr(self.config)

    class Server(object):

        def __init__(self, value):
            self.server = value

        def __repr__(self):
            return repr(self.server)

        @property
        def ip(self):
            return self.server['ip']

        @ip.setter
        def ip(self, value):
            self.server['ip'] = value

        @property
        def port(self):
            return self.server['port']

        @port.setter
        def port(self, value):
            self.server['port'] = value

    def write(self):
        with open(self.config_file, "w") as outfile:
            outfile.write(json.dumps(self.config, indent=4))

    def read(self):
        if os.path.exists(self.config_file) == False or open(self.config_file, "r").read() == "":
            self.config_write(self)
        with open(self.config_file, "r") as openfile:
            self.config = json.load(openfile)
        return repr(self.config)


config = Config()


class SERMOTIONS_PT_main(bpy.types.Panel):
    bl_category = "Sermotions"
    bl_idname = "SERMOTIONS_PT_main"
    bl_label = "Sermotions v{major}.{minor}.{patch}-{type}".format(
        major=bl_info['version'][0],
        minor=bl_info['version'][1],
        patch=bl_info['version'][2],
        type=bl_info['version_type']
    )
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.props
        obj = context.object

        box = layout.box()
        box.label(text="Motiron Tracking System")


class SERMOTIONS_PT_server(SERMOTIONS_PT_main, bpy.types.Panel):
    bl_idname = "SERMOTIONS_PT_server"
    bl_label = "Server Configuration"

    bpy.types.Scene.server_status = bpy.props.StringProperty()
    bpy.types.Scene.server_status = ""

    def __init__(self):
        super().__init__()
        try:
            bpy.utils.register_class(self.OT_save)
            bpy.utils.register_class(self.OT_start)
        except:
            pass

        bpy.types.Scene.props = bpy.props.PointerProperty(
            type=self.PT)

    class PT(bpy.types.PropertyGroup):

        def __init__(self):
            super().__init__()
            self.info = "..."

        def get_ip(self):
            return config.server.ip

        def set_ip(self, value):
            config.server.ip = value

        ip: bpy.props.StringProperty(
            name="IP",
            default=config.server.ip,
            maxlen=16,
            get=get_ip,
            set=set_ip
        )

        def get_port(self):
            return config.server.port

        def set_port(self, value):
            config.server.port = value

        port: bpy.props.StringProperty(
            name="Port",
            default=config.server.port,
            maxlen=5,
            get=get_port,
            set=set_port
        )

    def draw(self, context):
        info = bpy.types.Scene.server_status

        layout = self.layout
        scene = context.scene
        props = scene.props

        layout.prop(props, "ip")
        layout.prop(props, "port")

        box = layout.box()
        box.label(text="{info}".format(
            info=info), icon='INFO')

        row = layout.row()
        col = row.column()
        col.operator("sermotions.start")
        col = row.column()
        col.operator("sermotions.save")

    def status_print(self, context="..."):
        from datetime import datetime
        time = datetime.now().strftime("%H:%M:%S")
        bpy.types.Scene.server_status = "{time}: {context}".format(
            time=time,
            context=context
        )

    class OT_save(bpy.types.Operator):
        bl_label = "Save"
        bl_idname = "sermotions.save"

        def execute(self, context):
            config.write()
            SERMOTIONS_PT_server.status_print(
                self, "Server configuration is saved.")
            return {"FINISHED"}

    class OT_start(bpy.types.Operator):
        bl_label = "Start"
        bl_idname = "sermotions.start"

        def execute(self, context):
            SERMOTIONS_PT_server.status_print(
                self, "start button test")
            return {"FINISHED"}


classes = (
    # Properties.Server,
    SERMOTIONS_PT_main,
    SERMOTIONS_PT_server,
    SERMOTIONS_PT_server.PT,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


def print_debug(_context="", _type="Info"):
    print("{type}: {datetime} {context}".format(
        type=_type,
        datetime="-",
        context=_context
    ))


if __name__ == "Sermotions":
    # register()
    pass
