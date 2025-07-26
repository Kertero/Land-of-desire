import bpy
import bge
import os


kxscene = bge.logic.getCurrentScene()
objList = kxscene.objects
collection = bpy.data.collections.get("character_selector_UI")
cont = bge.logic.getCurrentController()

def duplicate_and_prepare_object(obj, collection, kxscene, name=None):
    obj_copy = obj.copy()
    obj_copy.data = obj.data.copy()
    collection.objects.link(obj_copy)
    
    if name:
        # Verificar si ya existe un objeto con ese nombre en la escena
        existing_name = name
        counter = 1
        while bpy.context.scene.objects.get(existing_name):
            existing_name = f"{name}_{counter}"
            counter += 1
        obj_copy.name = existing_name  # Asignamos el nombre único
        
    return kxscene.convertBlenderObject(obj_copy)


def create_scene_selector_buttons(scene_dir, button_template_name, text_template_name, parent_obj, collection, kxscene):
    y_offset = 0.0

    for filename in os.listdir(scene_dir):
        if not filename.endswith(".blend"):
            continue

        # Obtener nombre sin extensión
        scene_name = os.path.splitext(filename)[0]

        # Duplicar botón
        button_template = bpy.data.objects.get(button_template_name)
        if not button_template:
            print(f"Error: No se encontró el objeto '{button_template_name}'")
            continue

        button = duplicate_and_prepare_object(button_template, collection, kxscene, f"scene_btn:{scene_name}")
        button.setParent(parent_obj)
        button.position = (0,  y_offset , 0)
        y_offset -= 0.1

        # Asignar la propiedad 'scene_target'
        button["scene_target"] = filename  # incluye .blend

        # Duplicar texto hijo
        text_template = bpy.data.objects.get(text_template_name)
        if not text_template:
            print(f"Error: No se encontró el texto '{text_template_name}'")
            continue

        text_copy = duplicate_and_prepare_object(text_template, collection, kxscene, f"text:{scene_name}")
        text_copy.setParent(button)
        text_copy.position = (0, 0, 0.01)
        text_copy["Text"] = scene_name  # sin extensión


# Parámetros de entrada

scene_dir = os.path.join(bge.logic.expandPath("//"), "Scenes")
scene_selector_field = objList["scene_selector_list"]  # el objeto padre donde se agrupan los botones

# Ejecutar
create_scene_selector_buttons(
    scene_dir,
    "scene_selector_button_template",
    "scene_selector_button_template_Text",
    scene_selector_field,
    collection,
    kxscene
)
