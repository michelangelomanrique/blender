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
    "name": "Render Estimated Time",
    "author": "Michelangelo Manrique aka Magicland",
    "version": (0,1),
    "blender": (2, 5, 4),
    "api": 31847,
    "location": "Render Properties Panel",
    "description": "This script calculates the render estimated time",
    "warning": "",
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.5/Py/"\
        "Scripts/Render/Render_Estimated_Time",
    "tracker_url": "https://projects.blender.org/tracker/index.php?"\
        "func=detail&aid=22327&group_id=153&atid=468",
    "category": "Render"}

"""
Rev 0. Initial release
"""

import bpy
from bpy.props import *

et=""

class OBJECT_PT_Render(bpy.types.Panel):
    bl_label="Estimated Time"
    bl_space_type="PROPERTIES"
    bl_region_type="WINDOW"
    bl_context="render"
    
    bt=bpy.types.Scene
           
    bt.prop_frames = IntProperty(
        name="Frames", description="Number of frames the animation is suposed",
        min=0, max=10000, default=250)        
    
    bt.prop_days = IntProperty(
        name="Days", description="Number of days of the single render",
        min=0, max=30, default=0)
    
    bt.prop_hours = IntProperty(
        name="Hours", description="Number of hours of the single render",
        min=0, max=24, default=0)
    
    bt.prop_minutes = IntProperty(
        name="Minutes", description="Number of minutes of the single render",
        min=0, max=59, default=0)
    
    bt.prop_seconds = IntProperty(
        name="Seconds", description="Number of seconds of the single render",
        min=0, max=59, default=0)  

    global bt
    
    def draw(self,context):
        layout=self.layout
        
        obj=context.object
        scene=context.scene
        
      
        split=layout.split()
        col=split.column()
       
        # col.prop(scene, "prop_frames", slider=True)
        col.prop(scene, "prop_days", slider=False)
        col.prop(scene, "prop_hours", slider=False)
        col.prop(scene, "prop_minutes", slider=False)
        col.prop(scene, "prop_seconds", slider=False)
        
        
        col.operator("op.calcRenderTime",text="Calculate",icon="RENDER_RESULT");
        
      
        row=layout.row()
        row.label(text="Estimated Render Time:")
        row=layout.row()
        row.label(et)
        
class RENDER_OT_calc(bpy.types.Operator):
    ''''''
    bl_idname = "op.calcRenderTime"
    bl_label = "Calculate"
 
    def execute(self, context):
        
        scene=context.scene
        
        propDays=scene.prop_days
        propHours=scene.prop_hours
        propMinutes=scene.prop_minutes
        propSeconds=scene.prop_seconds
        

        startFrame=scene.frame_start
        endFrame=scene.frame_end
        nF=int(endFrame-startFrame+1)
        
        rt=[propDays,propHours,propMinutes,propSeconds]
        
        rtd=rt[0]
        rth=rt[1]
        rtm=rt[2]
        rts=rt[3]
        
        rtd=rtd*86400
        rth=rth*3600
        rtm=rtm*60
        
        rtime=rtd+rth+rtm+rts
        rtime=rtime*nF
        
        if rtime<60 :
            rtSec=rtime
        
        if rtime>=60 & rtime<3600 :
            rtMin=int(rtime/60)
            rtMinrest=rtime-(rtMin*60)
            rtSec=rtMinrest
            rtDay="0"
        
        if rtime>=3600 & rtime<=86400 :
            rtHrs=int(rtime/3600)
            rtHrsrest=rtime-(rtHrs*3600)
            rtMin=int(rtHrsrest/60)
            rtMinrest=rtHrsrest-(rtMin*60)
            rtSec=rtMinrest
            rtDay="0"
        
        if rtime>=86400 :
            rtDay=int(rtime/86400)
            rtDayrest=rtime-(rtDay*86400)
            rtHrs=int(rtDayrest/3600)
            rtHrsrest=rtDayrest-(rtHrs*3600)
            rtMin=int(rtHrsrest/60)
            rtMinrest=rtHrsrest-(rtMin*60)
            rtSec=rtMinrest
            
        et=str(rtDay) + "days " + str(rtHrs) + "hrs " + str(rtMin) + "min " + str(rtSec) + "sec "
        global et
        
        return {'FINISHED'}       

#################################################
#### REGISTER ###################################
#################################################
def register():
    pass

def unregister():
    bt = bpy.types.Scene
    del bt.prop_days
    del bt.prop_hours
    del bt.prop_minutes
    del bt.prop_seconds

if __name__ == "__main__":
    register()