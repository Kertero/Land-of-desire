import bge
import bpy


cont = bge.logic.getCurrentController()
own = cont.owner

def extract_area_from_pose():


    poses = [own.get("male_pose", ""), own.get("female_pose", "")]
    
    for pose in poses:
        if not pose:
            continue
        if ":" in pose:
            area_part = pose.split(":", 1)[1]  # Tomar lo que viene después del :
            area = area_part.split(".", 1)[0]  # Quitar el .001 si existe
            own["area"] = area
            print(f"[INFO] Área extraída de pose '{pose}': '{area}'")
            return  # Usamos la primera pose válida que encontremos

    print("[INFO] No se encontró ninguna pose válida para extraer área.")

# Ejecutar
extract_area_from_pose()



def set_last_pose_frames():

    
    # Obtener nombres de las animaciones desde las propiedades
    male_pose_name = own.get("male_pose")
    female_pose_name = own.get("female_pose")
    
    # Inicializar valores por defecto
    own["male_pose_last_frame"] = 0.0
    own["female_pose_last_frame"] = 0.0

    # Buscar el objeto Armature "man"
    man_armature = bpy.data.objects.get("man")
    if man_armature and man_armature.animation_data:
        action = bpy.data.actions.get(male_pose_name)
        if action:
            own["male_pose_last_frame"] = action.frame_range[1]

    # Buscar el objeto Armature "woman"
    woman_armature = bpy.data.objects.get("woman")
    if woman_armature and woman_armature.animation_data:
        action = bpy.data.actions.get(female_pose_name)
        if action:
            own["female_pose_last_frame"] = action.frame_range[1]


set_last_pose_frames()
