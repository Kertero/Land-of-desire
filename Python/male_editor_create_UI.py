import bpy
import bge
import os

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

def create_button_with_text(template_button_name, text_template_name, parent, name_prefix, y_offset, text_value, collection, kxscene):
    obj = bpy.context.scene.objects.get(template_button_name)
    if not obj:
        print(f"El objeto '{template_button_name}' no se encontró.")
        return

    # Crear el botón duplicado con un nombre único y prefijo
    button = duplicate_and_prepare_object(obj, collection, kxscene, f"{name_prefix}_{template_button_name}")
    button.setParent(parent)
    button.position = (0, y_offset, 0)

    # Crear el texto para el botón
    text_obj = bpy.data.objects.get(text_template_name)
    text_copy = duplicate_and_prepare_object(text_obj, collection, kxscene, f"text:{name_prefix}_{name_prefix}")
    text_copy.setParent(button)
    text_copy.position = text_obj.location
    text_copy["Text"] = text_value

def create_shape_key_sliders(character_obj, slider_template, kxscene, parent_field, collection):
    y_offset = 0
    shape_keys = character_obj.data.shape_keys.key_blocks
    for shape_key in shape_keys:
        slider = duplicate_and_prepare_object(slider_template, collection, kxscene, f"control_box:{shape_key.name}")
        slider.setParent(parent_field)
        slider.position = (0, y_offset, 0)
        y_offset -= 0.2

        # Hijos del slider
        for child_name, prefix in [("button_minus", "minus"), ("button_plus", "plus"), ("slider", "slider"), ("Text", "text")]:
            base_obj = bpy.data.objects.get(child_name)
            if not base_obj:
                print(f"El objeto '{child_name}' no se encontró.")
                continue
            child_copy = duplicate_and_prepare_object(base_obj, collection, kxscene, f"{prefix}:{shape_key.name}")
            child_copy.setParent(slider)
            child_copy.position = base_obj.location

            if prefix == "slider":
                child_copy["slider_value"] = shape_key.value * 100
            elif prefix == "text":
                child_copy["Text"] = shape_key.name

        slider["shape_key_name"] = shape_key.name

def create_clothing_buttons(directory, template_button_name, text_template_name, field_obj, collection, kxscene, name_prefix=""):
    y_offset = 0
    for filename in os.listdir(directory):
        if filename.endswith(".blend"):
            # Llamamos a la función para crear los botones con un prefijo en el nombre
            create_button_with_text(template_button_name, text_template_name, field_obj, name_prefix, y_offset, filename, collection, kxscene)
            y_offset -= 0.1

# ------------------------------------------
# INICIO DEL SCRIPT
# ------------------------------------------
print('-' * 150)

# Obtener la propiedad para el género del personaje

    
kxscene = bge.logic.getCurrentScene()
objList = kxscene.objects
collection = bpy.data.collections.get("HUD")
cont = bge.logic.getCurrentController()

script_holder = objList["script_holder"]
gender = script_holder['gender']

shape_key_sliders_field_objet = objList["shape_key_sliders_field"]
object_button_cloth_field = objList['torso_clothes_field']
object_button_pants_field = objList['pants_field']
object_button_shoes_field = objList['shoes_field']
object_button_hairs_field = objList['hair_field']

slider_template = bpy.data.objects.get('shape_keys_slider_holder')
    

# Definir el objeto y los directorios según el género

character_template = ''
character_object_name = ''
directory_torso_clothes = ''
directory_pants = ''
directory_shoes = ''
directory_eyebrowns = ''
directory_hairs = ''

if gender == "male":
    base_path = bge.logic.expandPath("//")
    character_template = os.path.join(base_path,  "Male_char_template.blend")
    character_object_name = 'man_1'
    directory_torso_clothes = os.path.join(base_path,  "Male", "Clothes", "Torso")
    directory_pants = os.path.join(base_path,  "Male", "Clothes", "Pants")
    directory_shoes = os.path.join(base_path,  "Male", "Clothes", "Shoes")
    directory_eyebrowns = os.path.join(base_path,  "Male", "Eyebrowns")
    directory_hairs = os.path.join(base_path,  "Male", "Hairs")
elif gender == "female":
    base_path = bge.logic.expandPath("//")
    character_template = os.path.join(base_path, "Characters", "Female_char_template.blend")
    character_object_name = 'female_1'
    directory_torso_clothes = os.path.join(base_path,  "Female", "Clothes", "Torso")
    directory_pants = os.path.join(base_path, "Female", "Clothes", "Pants")
    directory_shoes = os.path.join(base_path,  "Female", "Clothes", "Shoes")
    directory_eyebrowns = os.path.join(base_path,  "Female", "Eyebrowns")
    directory_hairs = os.path.join(base_path,  "Female", "Hairs")

blend_file_path = os.path.join(os.path.join(bge.logic.expandPath("//")), f"{'Male' if gender == 'male' else 'Female'}_char_template.blend")
print(gender)

# Comprobar si el archivo .blend existe
if os.path.exists(blend_file_path):
    print(f"Cargando el archivo {blend_file_path}")
    
    # Usar bpy.data.libraries.load para cargar todos los objetos de la carpeta 'Object'
    with bpy.data.libraries.load(blend_file_path) as (data_from, data_to):
        data_to.objects = data_from.objects  # Cargar todos los objetos

    # Enlazar los objetos cargados a la escena actual
    for obj in data_to.objects:
        if obj is not None:
            bpy.context.scene.collection.objects.link(obj)
            kxscene.convertBlenderObject(obj) 
else:
    print(f"Error: El archivo {blend_file_path} no existe.")


# Inicializar el resto de objetos y botones

if gender == 'male':
    character_obj = bpy.data.objects.get('man_1')
if gender == 'female':
    character_obj = bpy.data.objects.get('female_1')
    
if character_obj and slider_template:
    create_shape_key_sliders(character_obj, slider_template, kxscene, shape_key_sliders_field_objet, collection)
else:
    print("No se encontraron los objetos de malla o slider.")
    
    

# Crear botones de ropa con el prefijo correspondiente al género
create_clothing_buttons(directory_torso_clothes, "button_template", "button_text_template", object_button_cloth_field, collection, kxscene, "torso")
create_clothing_buttons(directory_pants, "button_template", "button_text_template", object_button_pants_field, collection, kxscene, "pants")
create_clothing_buttons(directory_shoes, "button_template", "button_text_template", object_button_shoes_field, collection, kxscene, "shoes")
#create_clothing_buttons(directory_eyebrowns, "button_template", "button_text_template", object_button_eyebrowns_field, collection, kxscene, "eyebrowns")
create_clothing_buttons(directory_hairs, "button_template", "button_text_template", object_button_hairs_field, collection, kxscene, "hair")



