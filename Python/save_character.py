import bge
import json
import os

def save_character_data(cont):
    own = cont.owner

    if own.get("editing", False):
        return  # No guardar si se está editando

    scene = bge.logic.getCurrentScene()
    objects = scene.objects

    # Obtener nombre del personaje
    char_name_obj = objects.get("char_name")
    if not char_name_obj:
        print("No se encontró el objeto 'char_name'")
        return

    char_name = char_name_obj.get('Text', "").strip()
    if not char_name:
        print("El nombre del personaje está vacío")
        return

    # Definir género y rutas
    script_holder = objects.get("script_holder")
    gender = script_holder.get('gender', "")
    save_dirs  = {
        "male": os.path.join(bge.logic.expandPath("//"),  "Male", "Exported"),
        "female": os.path.join(bge.logic.expandPath("//"), "Female","Exported")
    }
    save_dir = save_dirs.get(gender)
    if not save_dir:
        print("Género no válido")
        return

    man_name = "man_1" if gender == "male" else "female_1"
    man = objects.get(man_name)
    if not man:
        print("No se encontró el objeto del personaje")
        return

    filename = f"{char_name}.json"
    full_path = os.path.join(save_dir, filename)

    # Obtener shape keys usando bpy
    shape_keys_data = {}
    try:
        import bpy
        man_bpy = bpy.data.objects.get(man_name)
        if man_bpy and man_bpy.data.shape_keys:
            for key_block in man_bpy.data.shape_keys.key_blocks:
                shape_keys_data[key_block.name] = key_block.value
    except Exception as e:
        print(f"[ADVERTENCIA] No se pudo acceder a shape keys vía bpy: {e}")

    # Custom properties
    props = {key: man[key] for key in man.getPropertyNames() if key != "_RNA_UI"}

    # Blend files desde objetos holders
    holders = ["eyebrows", "hair", "pants", "shoes", "torso_up"]
    blend_files = {}
    for holder in holders:
        obj = objects.get(f"{holder}_holder")
        blend_files[holder] = obj.get("blend_file", "") if obj else ""

    # Armar JSON
    character_data = {
        "name": char_name,
        "shape_keys": shape_keys_data,
        "properties": props,
        "blend_files": blend_files
    }

    try:
        with open(full_path, 'w') as f:
            json.dump(character_data, f, indent=4)
        print(f"[OK] Personaje guardado en: {full_path}")
    except Exception as e:
        print(f"[ERROR] No se pudo guardar el personaje: {e}")


# Ejecución principal
cont = bge.logic.getCurrentController()
mouse_over = cont.sensors["MouseOver"]
mouse_click = cont.sensors["MouseClick"]

if mouse_over.positive and mouse_click.positive:
    save_character_data(cont)

