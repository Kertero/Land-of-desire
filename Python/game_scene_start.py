import json
import os
import bpy
import bge
import math



from mathutils import Matrix
from bge import logic

def apply_hsv_to_materials(base_obj_name, keyword, channel, value):
    """
    Aplica un cambio HSV a todos los materiales cuyo nombre contenga `keyword`,
    dentro del objeto `base_obj_name` y sus hijos.

    :param base_obj_name: Nombre del objeto padre (ej. 'female_1')
    :param keyword: Palabra clave a buscar en el nombre del material (ej. 'skin')
    :param channel: 'hue', 'saturation', 'value'
    :param value: Valor a asignar
    """
    obj = bpy.data.objects.get(base_obj_name)
    if not obj:
        print(f"[ERROR] Objeto base '{base_obj_name}' no encontrado.")
        return

    channel_index = {"hue": 0, "saturation": 1, "value": 2}
    index = channel_index.get(channel)
    if index is None:
        print(f"[ERROR] Canal HSV inválido: {channel}")
        return

    def process_object(o):
        for slot in o.material_slots:
            mat = slot.material
            if mat and keyword.lower() in mat.name.lower():
                if mat.use_nodes:
                    hsv_node = next((n for n in mat.node_tree.nodes if n.type == 'HUE_SAT'), None)
                    if hsv_node:
                        hsv_node.inputs[index].default_value = value
                        print(f"[OK] {channel}={value} aplicado a '{mat.name}' en '{o.name}'")
                    else:
                        print(f"[WARN] Nodo HSV no encontrado en '{mat.name}'")
                else:
                    print(f"[WARN] Material '{mat.name}' no usa nodos")

    # Procesar el objeto principal
    process_object(obj)

    # Procesar hijos (si existen)
    for child in obj.children:
        process_object(child)





def load_blend_objects(full_path):
    if not os.path.exists(full_path):
        print(f"[ADVERTENCIA] No se encontró el archivo {full_path}")
        return []

    try:
        with bpy.data.libraries.load(full_path, link=False) as (data_from, data_to):
            data_to.objects = data_from.objects

        imported = []
        for obj in data_to.objects:
            if obj is None:
                continue
            if obj.name not in bpy.context.scene.objects:
                bpy.context.scene.collection.objects.link(obj)
                imported.append(obj)
        return imported

    except Exception as e:
        print(f"[ERROR] Falló al cargar {full_path}: {e}")
        return []

def rename_object(obj, prefix):
    new_name = f"{prefix}_{obj.name}"
    counter = 1
    while new_name in bpy.data.objects:
        new_name = f"{prefix}_{obj.name}_{counter:03d}"
        counter += 1
    obj.name = new_name
    return obj.name

def copy_shape_keys(source_body, target_obj):
    if target_obj.type != 'MESH':
        return
    if not (target_obj.data.shape_keys and source_body and source_body.data.shape_keys):
        return
    for sk_name, sk_block in target_obj.data.shape_keys.key_blocks.items():
        if sk_name in source_body.data.shape_keys.key_blocks:
            sk_block.value = source_body.data.shape_keys.key_blocks[sk_name].value

def register_armature(obj, script_holder):
    if obj.type != 'ARMATURE' or not script_holder:
        return
    current = script_holder.get("Armatures", "")
    script_holder["Armatures"] = current + "|" + obj.name if current else obj.name

def convert_and_parent(objs, scene, parent_name):
    parent = scene.objects.get(parent_name)
    if not parent:
        print(f"[ADVERTENCIA] '{parent_name}' no encontrado en la escena.")
        return
    for obj in objs:
        try:
            kx_obj = scene.convertBlenderObject(obj)
            kx_obj.setParent(parent)
            kx_obj.position = (0, 0, 0)
        except Exception as e:
            print(f"[ERROR] No se pudo convertir '{obj.name}': {e}")

def load_character(json_path, gender, root_name):
    scene = logic.getCurrentScene()
    objects = scene.objects

    if not os.path.exists(json_path):
        print(f"[ERROR] El archivo {json_path} no existe.")
        return

    with open(json_path, 'r') as f:
        data = json.load(f)

    body = bpy.data.objects.get(root_name)
    if not body:
        print(f"[ERROR] No se encontró el objeto {root_name}")
        return
    
    


    # Aplicar shape keys al cuerpo base
    if body.data.shape_keys:
        for key_name, value in data.get("shape_keys", {}).items():
            if key_name in body.data.shape_keys.key_blocks:
                body.data.shape_keys.key_blocks[key_name].value = value

    # Propiedades del personaje
    kx_body = objects.get(root_name)
    for prop_name, value in data.get("properties", {}).items():
        if kx_body:
            kx_body[prop_name] = value



    base_dirs = {
        "male": os.path.join(bge.logic.expandPath("//"), "Characters", "Male"),
        "female": os.path.join(bge.logic.expandPath("//"), "Characters", "Female")
    }

    folder_map = {
        "hair": "Hairs",
        "pants": "Clothes/Pants",
        "shoes": "Clothes/Shoes",
        "torso_up": "Clothes/Torso"
    }

    game_script_holder = objects.get("game_scene_script_holder")

    for part, blend_file in data.get("blend_files", {}).items():
        if not blend_file:
            continue
        subdir = folder_map.get(part)
        if not subdir:
            print(f"[ADVERTENCIA] Parte desconocida: {part}")
            continue
        full_path = os.path.join(base_dirs[gender], subdir, blend_file)
        imported_objs = load_blend_objects(full_path)

        for obj in imported_objs:
            rename_object(obj, f"{gender}_{part}")
            copy_shape_keys(body, obj)
            register_armature(obj, game_script_holder)
            
            
        convert_and_parent(imported_objs, scene, "characters_holder")


            # -------------------- APLICAR COLORES HSV A PARTIR DEL JSON --------------------############################
    props = data.get("properties", {})

    if kx_body:  # El objeto ya convertido en la escena
        # Guardar los valores HSV como propiedades para que funcionen con tu slider
        for prop in ["skin_hue", "skin_sat", "skin_val",
                     "iris_hue", "iris_sat", "iris_val",
                     "brow_hue", "brow_sat", "brow_val"]:
            if prop in props:
                kx_body[prop] = props[prop]

        apply_hsv_to_materials(root_name, "skin", "hue", props.get("skin_hue", 0))
        apply_hsv_to_materials(root_name, "skin", "saturation", props.get("skin_sat", 0))
        apply_hsv_to_materials(root_name, "skin", "value", props.get("skin_val", 0))

        apply_hsv_to_materials(root_name, "iris", "hue", props.get("iris_hue", 0))
        apply_hsv_to_materials(root_name, "iris", "saturation", props.get("iris_sat", 0))
        apply_hsv_to_materials(root_name, "iris", "value", props.get("iris_val", 0))

        apply_hsv_to_materials(root_name, "brow", "hue", props.get("brow_hue", 0))
        apply_hsv_to_materials(root_name, "brow", "saturation", props.get("brow_sat", 0))
        apply_hsv_to_materials(root_name, "brow", "value", props.get("brow_val", 0))

            
    #################################3       


    




# -------------------- LOAD SCENE --------------------

cont = logic.getCurrentController()
own = cont.owner

if own.get("already_loaded") == False:

    scene_file = own.get("scene_to_load")
    if not scene_file:
        print("scene_to_load no definida")

    blend_path = os.path.join(bge.logic.expandPath("//"),"Scenes", scene_file)
    if not os.path.isfile(blend_path):
        print("No existe:", blend_path)

    with bpy.data.libraries.load(blend_path, link=False) as (data_src, data_dst):
        data_dst.objects = data_src.objects

    loaded = []
    for obj in data_dst.objects:
        if obj is not None:
            bpy.context.scene.collection.objects.link(obj)
            loaded.append(obj)

    if not loaded:
        print("No se importó ningún objeto")

    scene = logic.getCurrentScene()
    for obj in loaded:
        if obj.name not in scene.objects:
            try:
                scene.convertBlenderObject(obj)
            except Exception as e:
                print(f"[ERROR] No se pudo convertir '{obj.name}' a KX_GameObject: {e}")
        else:
            print(f"[INFO] '{obj.name}' ya estaba en escena. Saltado.")

    print("game_scene_start.py")

    load_character(os.path.join(bge.logic.expandPath("//"), "Characters", "Female", "Exported") + "/" + own["female_char"], "female", "female_1")
    load_character(os.path.join(bge.logic.expandPath("//"), "Characters", "Male", "Exported") + "/" + own["male_char"], "male", "man_1")
    
    
        # -------------------- POST-INICIALIZACIÓN DE CÁMARA --------------------
    scene = logic.getCurrentScene()
    objects = scene.objects

    cam = objects.get("Man_FPV_Camera")
    head = objects.get("man_head_z")
    Male_head_proxy = objects.get("Male_head_bone_proxy") 

    if cam and head:
        head.worldPosition = (-0.002637, -0.167261, 1.62521)
        head.setParent(Male_head_proxy)
        cam.setParent(head)

        cam.worldOrientation = Matrix.Rotation(math.radians(90), 3, 'X')
        head.worldOrientation = Matrix.Rotation(math.radians(180), 3, 'Z')

        print("[INFO] Cámara parentada correctamente y cabeza posicionada.")
    else:
        if not cam:
            print("[ERROR] No se encontró 'Man_FPV_Camera' en la escena.")
        if not head:
            print("[ERROR] No se encontró 'man_head_z' en la escena.")




    own["already_loaded"] = True
