#script to make rigify compatible with unity humanoid
#HOWTO: right after generating rig using rigify
#	press armature -> Rigify To Unity Converter -> (Prepare rig for unity) button
bl_info = {
    "name": "Rigify to Unity",
    "category": "Rigging",
    "description": "Change Rigify rig into Mecanim-ready rig for Unity",
    "location": "At the bottom of Rigify rig data/armature tab",
    "blender":(2,80,0)
}

import bpy
import re


class UnityMecanim_Panel(bpy.types.Panel):
    bl_label = "Rigify to Unity converter"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"

    @classmethod
    def poll(self, context):
        return context.object.type == 'ARMATURE' and "DEF-spine.006" in bpy.context.object.data.bones
    
    def draw(self, context):
        self.layout.operator("rig4mec.convert2unity")
        
        
class UnityMecanim_Convert2Unity(bpy.types.Operator):
    bl_idname = "rig4mec.convert2unity"
    bl_label = "Prepare rig for unity"
    
    def execute(self, context):
        ob = bpy.context.object

        parents = [ \
            ('DEF-pelvis.L', 'DEF-spine'), \
            ('DEF-pelvis.R', 'DEF-spine'), \
            ('DEF-breast.L', 'DEF-spine.003'), \
            ('DEF-breast.R', 'DEF-spine.003'), \
            ('DEF-shoulder.L', 'DEF-spine.003'), \
            ('DEF-shoulder.R', 'DEF-spine.003'), \
            ('DEF-upper_arm.L', 'DEF-shoulder.L'), \
            ('DEF-upper_arm.R', 'DEF-shoulder.R'), \
            ('DEF-thigh.L', 'DEF-spine'), \
            ('DEF-thigh.R', 'DEF-spine'), \
            ('DEF-f_index.01.R', 'DEF-hand.R'), \
            ('DEF-thumb.01.R', 'DEF-hand.R'), \
            ('DEF-f_middle.01.R', 'DEF-hand.R'), \
            ('DEF-f_ring.01.R', 'DEF-hand.R'), \
            ('DEF-f_pinky.01.R', 'DEF-hand.R'), \
            ('DEF-f_index.01.L', 'DEF-hand.L'), \
            ('DEF-thumb.01.L', 'DEF-hand.L'), \
            ('DEF-f_middle.01.L', 'DEF-hand.L'), \
            ('DEF-f_ring.01.L', 'DEF-hand.L'), \
            ('DEF-f_pinky.01.L', 'DEF-hand.L'), \
            ('DEF-palm.01.L', 'DEF-hand.L') ,\
            ('DEF-palm.02.L', 'DEF-hand.L') ,\
            ('DEF-palm.03.L', 'DEF-hand.L') ,\
            ('DEF-palm.04.L', 'DEF-hand.L') ,\
            ('DEF-palm.01.R', 'DEF-hand.R') ,\
            ('DEF-palm.02.R', 'DEF-hand.R') ,\
            ('DEF-palm.03.R', 'DEF-hand.R') ,\
            ('DEF-palm.04.R', 'DEF-hand.R') ,\
        ]

        #commented out to prevent deletion of this bones
        
        disableDeforms = [ \
            # 'DEF-breast.L', \
            # 'DEF-breast.R', \
            # 'DEF-pelvis.L', \
            # 'DEF-pelvis.R', \
        ]

        tailsToCopy = [ \
            # ('DEF-upper_arm.L', 'DEF-upper_arm.L.001'), \
            # ('DEF-forearm.L', 'DEF-forearm.L.001'), \
            # ('DEF-upper_arm.R', 'DEF-upper_arm.R.001'), \
            # ('DEF-forearm.R', 'DEF-forearm.R.001'), \
            # ('DEF-thigh.L', 'DEF-thigh.L.001'), \
            # ('DEF-shin.L', 'DEF-shin.L.001'), \
            # ('DEF-thigh.R', 'DEF-thigh.R.001'), \
            # ('DEF-shin.R', 'DEF-shin.R.001') \
        ]
        
        parentsToCopy = [ \
            # ('DEF-forearm.L', 'DEF-upper_arm.L.001'), \
            # ('DEF-hand.L', 'DEF-forearm.L.001'), \
            # ('DEF-forearm.R', 'DEF-upper_arm.R.001'), \
            # ('DEF-hand.R', 'DEF-forearm.R.001'), \
            # ('DEF-shin.L', 'DEF-thigh.L.001'), \
            # ('DEF-foot.L', 'DEF-shin.L.001'), \
            # ('DEF-shin.R', 'DEF-thigh.R.001'), \
            # ('DEF-foot.R', 'DEF-shin.R.001') \
        ]

        bonesToDelete = [ \
            # 'DEF-upper_arm.L.001', \
            # 'DEF-forearm.L.001', \
            # 'DEF-upper_arm.R.001', \
            # 'DEF-forearm.R.001', \
            # 'DEF-thigh.L.001', \
            # 'DEF-shin.L.001', \
            # 'DEF-thigh.R.001', \
            # 'DEF-shin.R.001', \
            # 'DEF-pelvis.L', \
            # 'DEF-pelvis.R', \
            # 'DEF-breast.L', \
            # 'DEF-breast.R' \
        ]
        renames = [ \
            ("DEF-spine.006", "DEF-head"), \
            ("DEF-spine.005","DEF-neck") \
        ]

        bpy.ops.object.mode_set(mode='OBJECT')
        
        for bone in disableDeforms:
            if bone in ob.data.bones :
                ob.data.bones[bone].use_deform = False

        bpy.ops.object.mode_set(mode='EDIT')

        for child, parent in parents:
            if child in ob.data.bones and parent in ob.data.bones:
                ob.data.edit_bones[child].parent = ob.data.edit_bones[parent]
        
        for child, parent in tailsToCopy:
            if child in ob.data.bones and parent in ob.data.bones:
                ob.data.edit_bones[child].tail = ob.data.edit_bones[parent].tail

        for child, parent in parentsToCopy:
            if child in ob.data.bones and parent in ob.data.bones:
                ob.data.edit_bones[child].parent = ob.data.edit_bones[parent].parent

        for bone in bonesToDelete:
            if bone in ob.data.bones :
                ob.data.edit_bones.remove(ob.data.edit_bones[bone])

        bpy.ops.object.mode_set(mode='OBJECT')


        for name, newname in renames:
            pb = ob.pose.bones.get(name)
            if pb is None:
                continue
            pb.name = newname

        self.report({'INFO'}, 'Unity ready rig!')                

        return{'FINISHED'}

def register():
    bpy.utils.register_class(UnityMecanim_Panel)
    bpy.utils.register_class(UnityMecanim_Convert2Unity)
    
    
def unregister():
    bpy.utils.unregister_class(UnityMecanim_Panel)
    bpy.utils.unregister_class(UnityMecanim_Convert2Unity)
