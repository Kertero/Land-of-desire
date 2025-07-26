import bpy
import bge
import os


def duplicate_and_prepare_object(obj, collection, kxscene, name=None):
    obj_copy = obj.copy()
    obj_copy.data = obj.data.copy()
    collection.objects.link(obj_copy)
    
    if name:
        existing_name = name
        counter = 1
        while bpy.context.scene.objects.get(existing_name):
            existing_name = f"{name}_{counter}"
            counter += 1
        obj_copy.name = existing_name
        
    return kxscene.convertBlenderObject(obj_copy)




def create_buttons_from_json_files(directory, button_template_name, text_template_name, parent_obj, collection, kxscene, name_prefix=""):
    import os

    y_offset = 0
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            # Duplicar el botón base con nombre único
            button = duplicate_and_prepare_object(
                bpy.context.scene.objects.get(button_template_name),
                collection, kxscene,
                f"{name_prefix}_{filename}"
            )
            if not button:
                print(f"No se pudo duplicar el botón base '{button_template_name}'.")
                continue

            button.setParent(parent_obj)
            button.position = (0, y_offset, 0)

            
            # Duplicar el texto base, ponerle de texto el nombre del json
            text_obj = bpy.data.objects.get(text_template_name)
            if not text_obj:
                print(f"No se encontró el objeto texto '{text_template_name}'.")
                continue

            text_copy = duplicate_and_prepare_object(text_obj, collection, kxscene, f"text:{name_prefix}_{filename}")
            text_copy.setParent(button)
            #text_copy.position = text_obj.location
            text_copy.position = (0, 0, 0.01)
            print(button.position)
            button["file"] = filename
            button["gender"] = gender
                       
            # Asignar el nombre del json como texto
            text_copy["Text"] = os.path.splitext(filename)[0]


            y_offset -= 0.1



kxscene = bge.logic.getCurrentScene()
collection = bpy.data.collections.get("character_selector_UI")
parent_obj = kxscene.objects.get("character_selector_male_chars_list")
gender = "male"
ruta = os.path.join(bge.logic.expandPath("//"), "Characters", "Male", "Exported")
create_buttons_from_json_files(
    ruta,
    "character_selector_button_template",
    "character_selector_button_template_Text",
    parent_obj,
    collection,
    kxscene,
    "torso"
)


parent_obj = kxscene.objects.get("character_selector_female_chars_list")
gender = "female"
ruta =  os.path.join(bge.logic.expandPath("//"), "Characters", "Female", "Exported")
create_buttons_from_json_files(
    ruta,
    "character_selector_button_template",
    "character_selector_button_template_Text",
    parent_obj,
    collection,
    kxscene,
    "torso"
)


if parent_obj is None:
    print("Error: no se encontró el objeto padre.")
if collection is None:
    print("Error: no se encontró la colección.")
if kxscene is None:
    print("Error: no se encontró la escena de BGE.")
