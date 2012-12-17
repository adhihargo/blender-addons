# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "LodToggle",
    "description": "Control panel for activating "
    "the cameras available in a scene",
    "author": "Francesco Siddi",
    "version": (0, 5),
    "blender": (2, 63, 5),
    "location": "Properties Panel",
    "warning": "",  # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "",
    "category": "3D View"}

import bpy
from bpy.props import (FloatProperty, BoolProperty, 
FloatVectorProperty, StringProperty, EnumProperty)


scene = bpy.context.scene

cameras = set()

def ListCameras():
    for ob in bpy.data.objects:
        if ob.type == 'CAMERA':
            print (ob.name)
            cameras.add(ob)
            
ListCameras()

class CameraSelectorPanel(bpy.types.Panel):
    bl_label = "Camera Selector"
    bl_idname = "SCENE_PT_cameraselector"
    bl_context = "scene"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        if len(cameras) > 0:
            for camera in cameras:
                row = layout.row()
                btn = row.operator("cameraselector.set_scene_camera", 
                text=camera.name, icon='OUTLINER_DATA_CAMERA')
                btn.chosen_camera = camera.name
        else:
            layout.label("No cameras in this scene") 
        
        row = layout.row()
        btn = row.operator("cameraselector.reload_camera_list", 
        text="Reload Camera List", icon='FILE_REFRESH')
        

class SetSceneCamera(bpy.types.Operator):
    bl_idname = "cameraselector.set_scene_camera"
    bl_label = "Make this object a camera"
    bl_description = "Make this object a camera"
    chosen_camera = bpy.props.StringProperty()

    def execute(self, context):
        
        chosen_camera = self.chosen_camera
    
        try: 
            scene.camera = bpy.data.objects[chosen_camera]
            #print (chosen_camera)
        except:
            #self.report({'WARNING'}, "Group %s not found" % new_group.upper())
            self.report({'WARNING'}, "Fail")

        return {'FINISHED'}


class ReloadCameraList(bpy.types.Operator):
    bl_idname = "cameraselector.reload_camera_list"
    bl_label = "Reload camera list"
    bl_description = "Refresh camera list for the current scene"

    def execute(self, context):

        try: 
            ListCameras()
        except:
            self.report({'WARNING'}, "Fail, something went wrong")

        return {'FINISHED'}



def register():
    bpy.utils.register_class(ReloadCameraList)
    bpy.utils.register_class(SetSceneCamera)
    bpy.utils.register_class(CameraSelectorPanel)
    
def unregister():
    bpy.utils.unregister_class(ReloadCameraList)
    bpy.utils.unregister_class(SetSceneCamera)
    bpy.utils.unregister_class(CameraSelectorPanel)
    
if __name__ == "__main__":
    register()