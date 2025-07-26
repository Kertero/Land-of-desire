import bpy
import bge
import os

def import_all_objects_and_parent(owner, blend_path):
    if not os.path.exists(blend_path):
        return

    with bpy.data.libraries.load(blend_path, link=False) as (data_from, data_to):
        data_to.objects = data_from.objects

    kxscene = bge.logic.getCurrentScene()

    # Buscar el objeto que tiene la propiedad 'Armatures'
    game_scene_script_holder = kxscene.objects.get("game_scene_script_holder")
    if game_scene_script_holder is None:
        print("[import_all_objects] No se encontró el objeto 'game_scene_script_holder'")
        return

    # Inicializar la propiedad 'Armatures' si no existe
    if "Armatures" not in game_scene_script_holder:
        game_scene_script_holder["Armatures"] = ""

    # Contador para nombres únicos
    armature_counter = 1
    armature_names = []

    for obj in data_to.objects:
        if obj is None:
            continue

        if obj.name not in [o.name for o in bpy.context.scene.objects]:
            bpy.context.scene.collection.objects.link(obj)

        # Si es un armature, renombrarlo y guardar el nuevo nombre
        if obj.type == 'ARMATURE':
            new_name = "Base_Mesh_"
            obj.name =  new_name +obj.name 
            armature_names.append(obj.name)

        kx_obj = kxscene.convertBlenderObject(obj)
        kx_obj.worldPosition = owner.worldPosition.copy()
        kx_obj.worldOrientation = owner.worldOrientation.copy()
        kx_obj.setParent(owner)
        

    # Concatenar los nombres con '|'
    if armature_names:
        current_value = game_scene_script_holder.get("Armatures", "")
        if current_value:
            game_scene_script_holder["Armatures"] = current_value + "|" + "|".join(armature_names) + "|" 
        else:
            game_scene_script_holder["Armatures"] = "|".join(armature_names)

def main():
    cont = bge.logic.getCurrentController()
    owner = cont.owner
    base_path = os.path.join(bge.logic.expandPath("//"), "Characters") + "/"
    if owner["already_loaded"] == False:
        gender = owner.get("gender")
        if not gender:
            print("[main] No se encontró la propiedad 'gender' en el objeto owner")
            return
    
        if gender == "male":
            blend_path = os.path.join(base_path, "Male_char_template.blend")
        elif gender == "female":
            blend_path = os.path.join(base_path, "Female_char_template.blend")
        else:
            print(f"[main] Género desconocido: {gender}")
            return

        import_all_objects_and_parent(owner, blend_path)
        owner["already_loaded"] = True

main()
