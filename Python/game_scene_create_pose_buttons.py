import bpy
import bge
import re

def normalize_name(name):
    return re.sub(r'\.\d+$', '', name)

def build_pose_buttons():
    kxscene = bge.logic.getCurrentScene()
    objList = kxscene.objects
    y_offset = 0

    # Obtener armatures
    man = bpy.data.objects.get("man")
    woman = bpy.data.objects.get("woman")
    if not man or not woman:
        print("[ERROR] No se encontró 'man' o 'woman'")
        return
    if not man.animation_data or not woman.animation_data:
        print("[ERROR] Falta animation_data en los armatures")
        return

    def get_track_names(armature):
        return {normalize_name(track.name): track.name for track in armature.animation_data.nla_tracks}

    man_tracks = get_track_names(man)
    woman_tracks = get_track_names(woman)
    shared_pose_names = set(man_tracks.keys()).intersection(woman_tracks.keys())
    if not shared_pose_names:
        print("[INFO] No hay poses compartidas")
        return

    # Obtener template, holder y text_template
    template = bpy.data.objects.get("poses_buttons_template")
    holder = objList.get("pose_lists_holder")
#    text_template = None
    text_template = bpy.data.objects.get("poses_buttons_template_Text")
#    for child in template.children:
#        if child.type == 'FONT':
#            text_template = child
#            break
    if not template or not holder or not text_template:
        print("[ERROR] Falta template, holder o texto base")
        return

    # Colección destino
    collection = bpy.data.collections.get("game_scene_menues")
    if not collection:
        print("[ERROR] No existe la colección 'game_scene_menues'")
        return

    for pose_name in sorted(shared_pose_names):
        male_track = man_tracks[pose_name]
        female_track = woman_tracks[pose_name]

        # Duplicar botón
        obj_copy = template.copy()
        obj_copy.data = template.data.copy()
        collection.objects.link(obj_copy)
        obj_copy = kxscene.convertBlenderObject(obj_copy)
        obj_copy.setParent(holder)
        obj_copy.position = (0, y_offset, 0.1)

        print(obj_copy.position)
        obj_copy["pose_name_male"] = male_track
        obj_copy["pose_name_female"] = female_track

        # Duplicar texto
        text_copy = text_template.copy()
        text_copy.data = text_template.data.copy()
        collection.objects.link(text_copy)
        text_copy.name = "text:" + pose_name
        text_copy = kxscene.convertBlenderObject(text_copy)
        text_copy.setParent(obj_copy)
        text_copy.position = (0, 0, 0.01)



        #text_copy["Text"] = pose_name

        text_base = pose_name.split(":")[0] if ":" in pose_name else pose_name
        text_copy["Text"] = text_base


        y_offset -= 0.1

    print(f"[OK] Se crearon {len(shared_pose_names)} botones de poses.")





cont = bge.logic.getCurrentController()
own = cont.owner
    
if own["already_created_pose_buttons"] == False: 
    # Ejecutar
    build_pose_buttons()
    own["already_created_pose_buttons"] = True
    
    