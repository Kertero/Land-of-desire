import bge


def update_armatures_animation():
    scene = bge.logic.getCurrentScene()
    holder = scene.objects.get("game_scene_script_holder")
    if not holder:
        print("[ERROR] No se encontró game_scene_script_holder")
        return

    armature_names = [n.strip() for n in holder.get("Armatures", "").split("|") if n.strip()]
    anim_speed  = holder["animation_speed"]
    anim_frame  = holder["anim_frame"]
    last_frame  = holder["pose_last_frame"]

    male_pose   = holder.get("male_pose", "")
    female_pose = holder.get("female_pose", "")

    for name in armature_names:
        kx_arm = scene.objects.get(name)
        if not kx_arm or not hasattr(kx_arm, 'playAction'):
#            print(f"[ADVERTENCIA] No se encontró armature: {name}")
            continue

        lname = name.lower()
        if "female" in lname or "woman" in lname:
            action_name = female_pose
        elif "male" in lname or "man" in lname:
            action_name = male_pose
        else:
#            print(f"[ADVERTENCIA] Género no detectado en: {name}")
            continue

        if not action_name:
#            print(f"[ERROR] Pose no definida para {name}")
            continue

        kx_arm.playAction(action_name, anim_frame, anim_frame, bge.logic.KX_ACTION_MODE_PLAY, 1)

    # Asignar correctamente el nuevo frame
    anim_frame = anim_frame + anim_speed
    
    if anim_frame > last_frame:
        anim_frame = 0
        
    holder["anim_frame"] = anim_frame  # <--- CORRECTO

 #   print("Frame actual:", anim_frame, " frame final:",last_frame)




update_armatures_animation()
