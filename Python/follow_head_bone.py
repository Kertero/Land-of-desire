import bge

def follow_head_bone(cont):
    own = cont.owner
    scene = bge.logic.getCurrentScene()
    armature = scene.objects.get("Base_Mesh_Man_Armature")  # o el nombre real del armature

    if not armature:
        return

    bone_name = "head"
    bone_matrix = armature.channels[bone_name].pose_matrix

    # Solo actualizar la posición, no la rotación
    bone_world_pos = (armature.worldTransform @ bone_matrix).to_translation()
    own.worldPosition = bone_world_pos

    
    
    
follow_head_bone(bge.logic.getCurrentController())    