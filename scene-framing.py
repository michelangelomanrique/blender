#  Copyright (c) 2013 Michelangelo Manrique
#
#  This program is free software; you can redistribute it and/or modify 
#  it under the terms of the GNU General Public License as published by 
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

bl_addon_info = {
    "name": "Scene Framing",
    "author": "Michelangelo Manrique aka Magicland",
    "version": (0,2),
    "blender": (2, 5, 6),
    "location": "Scene Properties Panel",
    "description": "This script calculates the amount of frames required for any scene according the number of seconds",
    "warning": "",
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.5/Py/"\
        "Scripts/Scene/Scene_Framing",
    "category": "System"}

"""
Rev 0. Initial release
Rev 1. Testing
Rev 2. Implemented with auto RenderSettings.fps variable
       and RenderSettings.fps_base variable
"""

import bpy
from bpy.props import *

nf="0"

class OBJECT_PT_Framing(bpy.types.Panel):
    bl_label="Scene Framing"
    bl_space_type="PROPERTIES"
    bl_region_type="WINDOW"
    bl_context="render"
   
    bt=bpy.types.Scene
           
    bt.prop_seconds = IntProperty(
        name="Seconds", description="Number of seconds the scene will be",
        min=0, max=59, default=0)
        
    global bt
    
    def draw(self,context):
        layout=self.layout
        
        obj=context.object
        scene=context.scene
      
        split=layout.split()
        col=split.column()
       
        col.prop(scene, "prop_seconds", slider=False)
        
        col.operator("op.calcFrames",text="Calculate")
        
        outLabel=str("Number of Frames: " + nf )
        row=layout.row()
        row.label(outLabel)
        
class SCENE_OT_calc(bpy.types.Operator):
    ''''''
    bl_idname = "op.calcFrames"
    bl_label = "Calculate"
 
    def execute(self, context):
        
        scene=context.scene
        
        fps=bpy.context.scene.render.fps
        frb=bpy.context.scene.render.fps_base
           
        propSeconds=scene.prop_seconds
        nfint=int(propSeconds*fps/frb)
        nf=str(nfint)
        scene.frame_end=nfint
        
        global nf
        global fps
        
        return {'FINISHED'}       

#################################################
#### REGISTER ###################################
#################################################
def register():
    pass

def unregister():
    bt = bpy.types.Scene
    del bt.prop_seconds

if __name__ == "__main__":
    register()