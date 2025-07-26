import bpy
import bge

cont = bge.logic.getCurrentController()
owner = cont.owner
mouse_clic = cont.sensors["MouseClick"]
mouse_over = cont.sensors["MouseOver"]
script_holder = bge.logic.getCurrentScene().objects["game_scene_script_holder"]

if mouse_clic.positive and mouse_over.positive:
    # Valores de pose seleccionados
    male_pose = owner.get("pose_name_male", "")
    female_pose = owner.get("pose_name_female", "")

    script_holder["male_pose"] = male_pose
    script_holder["female_pose"] = female_pose

    # Determinar qué action usar para man/woman, incluso si están vacíos
    def get_action_end(arm_obj_name, pose_prop):
        arm_obj = bpy.data.objects.get(arm_obj_name)
        if arm_obj is None or arm_obj.type != 'ARMATURE':
            return 0
        action_name = script_holder.get(pose_prop) or arm_obj.animation_data and arm_obj.animation_data.action and arm_obj.animation_data.action.name
        if not action_name:
            return 0
        action = bpy.data.actions.get(action_name)
        if not action:
            return 0
        return action.frame_range[1]  # frame_range es un Vector [start,end] :contentReference[oaicite:1]{index=1}

    end_man = get_action_end("man", "male_pose")
    end_woman = get_action_end("woman", "female_pose")
    last_frame = max(end_man, end_woman)
    script_holder["pose_last_frame"] = last_frame
    print("pose_last_frame establecido a", last_frame)


