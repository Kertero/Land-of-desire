import json
import os
import bpy
import bge

def load_character(json_path, gender, root_name):
    scene = bge.logic.getCurrentScene()
    objects = scene.objects

    if not os.path.exists(json_path):
        print(f"[ERROR] El archivo {json_path} no existe.")
        return

    with open(json_path, 'r') as f:
        data = json.load(f)

    # 1. Obtener objeto del cuerpo
    body = bpy.data.objects.get(root_name)
    if not body:
        print(f"[ERROR] No se encontró el objeto {root_name}")
        return

    # 2. Aplicar shape keys
    if body.data.shape_keys:
        for key_name, value in data.get("shape_keys", {}).items():
            if key_name in body.data.shape_keys.key_blocks:
                body.data.shape_keys.key_blocks[key_name].value = value

    # 3. Aplicar propiedades personalizadas
    kx_body = objects.get(root_name)
    if kx_body:
        for prop_name, value in data.get("properties", {}).items():
            kx_body[prop_name] = value

    # 4. Restaurar HSV de cejas
    eyebrows = objects.get("eyebrows_holder")
    for key in ["hue", "saturation", "value"]:
        if key in data.get("eyebrows_hsv", {}):
            if eyebrows:
                eyebrows[key] = data["eyebrows_hsv"][key]

    # 5. Cargar prendas y pelo
    base_dirs = {
    	"male": os.path.join(bge.logic.expandPath("//"), "Characters", "Male"),
    	"female": os.path.join(bge.logic.expandPath("//"), "Characters", "Female")
    }

    for part, blend_file in data.get("blend_files", {}).items():
        if not blend_file:
            continue
        folder_map = {
            "hair": "Hairs",
            "pants": "Clothes/Pants",
            "shoes": "Clothes/Shoes",
            "torso_up": "Clothes/Torso"
        }
        subdir = folder_map.get(part)
        if not subdir:
            continue
        full_path = os.path.join(base_dirs[gender], subdir, blend_file)
        if not os.path.exists(full_path):
            print(f"[ADVERTENCIA] No se encontró el archivo {full_path}")
            continue
        try:
            bpy.ops.wm.append(
                filepath=os.path.join(full_path, "Object", part),
                directory=os.path.join(full_path, "Object"),
                filename=part
            )
            obj = scene.convertBlenderObject(bpy.data.objects[part])
            holder = objects.get(f"{part}_holder")
            if holder:
                obj.setParent(holder)
                obj.position = (0, 0, 0)
        except Exception as e:
            print(f"[ERROR] Falló la carga de {part} desde {blend_file}: {e}")
