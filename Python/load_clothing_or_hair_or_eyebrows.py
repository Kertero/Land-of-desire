import bpy
import os
import bge
import GameLogic

cont = bge.logic.getCurrentController()
owner = cont.owner
mouse_clic = cont.sensors["MouseClick"]
mouse_over = cont.sensors["MouseOver"]

script_holder = bge.logic.getCurrentScene().objects["script_holder"]
gender = script_holder['gender']

if gender == "male":
    base_path = bge.logic.expandPath("//")
    pants_directory = os.path.join(base_path,"Male", "Clothes", "Pants") + "/"
    torsosc_directory = os.path.join(base_path, "Male", "Clothes", "Torso") + "/"
    shoes_directory = os.path.join(base_path,  "Male", "Clothes", "Shoes") + "/"
    hair_directory = os.path.join(base_path,  "Male", "Hairs") + "/"
    gender_objet = "man_1"
    
if gender == "female":
    base_path = bge.logic.expandPath("//")
    pants_directory = os.path.join(base_path, "Female", "Clothes", "Pants") + "/"
    torsosc_directory = os.path.join(base_path, "Female", "Clothes", "Torso") + "/"
    shoes_directory = os.path.join(base_path,  "Female", "Clothes", "Shoes") + "/"
    hair_directory = os.path.join(base_path,  "Female", "Hairs") + "/"
    gender_objet = "female_1"

def load_clothing_or_hair_or_eyebrows(object_type, folder_path, object_name, holder_name, shape_key_object_name=gender_objet):
    """
    Función generalizada para cargar cualquier objeto de ropa, pelo, o cejas.
    
    :param object_type: El tipo de objeto (ej. 'Torso', 'Pants', 'Shoes', 'Hair', 'Eyebrows').
    :param folder_path: Ruta del directorio donde están los archivos .blend.
    :param object_name: Nombre del objeto en el archivo .blend a cargar (puede ser diferente según el tipo de prenda).
    :param holder_name: Nombre del objeto que actúa como contenedor en la escena.
    :param shape_key_object_name: Nombre del objeto que contiene las shape keys (por defecto es 'man_1').
    """
    cont = bge.logic.getCurrentController()
    owner = cont.owner  # El objeto que está ejecutando el controlador (el botón que fue clicado)
    mouse_clic = cont.sensors["MouseClick"]
    mouse_over = cont.sensors["MouseOver"]
    kxscene = bge.logic.getCurrentScene()
    objList = kxscene.objects
    mesh_holder = objList[holder_name]  # Contenedor de la prenda o elemento
    body_mesh = bpy.data.objects.get(shape_key_object_name)  # El cuerpo del personaje
    mesh = kxscene.objects.get(object_name)  # El objeto que se va a cargar
    blend_name = None
    if mouse_clic.positive and mouse_over.positive:
        if mesh:
            # Si ya existe un objeto cargado, lo eliminamos
            for child in mesh_holder.children:
                child.endObject()
                break
        else:
            # Obtener el nombre del archivo de la prenda desde el texto en el botón (propiedad 'Text' del botón)
            for child in owner.children:
                if 'Text' in child:
                    file_name = child['Text']
                    blend_name = child['Text']
                    break

            # Ruta completa al archivo .blend
            file_path = folder_path + file_name
            bpy.ops.wm.append(
                filepath=os.path.join(file_path, "Object", object_name),
                directory=os.path.join(file_path, "Object"),
                filename=object_name
            )

            # Convertir el objeto y asignarle su posición
            clothing = kxscene.convertBlenderObject(bpy.data.objects[object_name])
            clothing.setParent(mesh_holder)
            clothing.position = 0, 0, 0

            # Asignar shape keys (si el objeto tiene shape keys)
            for shape_key in body_mesh.data.shape_keys.key_blocks:
                if shape_key.name in bpy.data.objects[object_name].data.shape_keys.key_blocks:
                    bpy.data.objects[object_name].data.shape_keys.key_blocks[shape_key.name].value = shape_key.value

        return blend_name  # Al final de la función
    return None  # Si no se cargó nada

# ------------------------------------------
# Llamada que determina qué objeto cargar según el prefijo
# ------------------------------------------

def load_by_prefix():
    cont = bge.logic.getCurrentController()
    owner = cont.owner  # El objeto que está ejecutando el controlador (el botón que fue clicado)
    kxscene = bge.logic.getCurrentScene()   
    
    # Obtener el prefijo del nombre del objeto
    object_name = owner.name
    prefijo = object_name.split('_')[0]  # Obtener el prefijo, que es la primera parte antes del "_"  
    # Según el prefijo, cargar el objeto adecuado
    if prefijo == 'torso':
        #load_clothing_or_hair_or_eyebrows("Torso", '/home/dude/Proyectos/PrnGame/PrnGameProject/Characters/Male/Clothes/Torso/', "torso_up", "torso_up_holder")
        blend_name = load_clothing_or_hair_or_eyebrows("Torso", torsosc_directory , "torso_up", "torso_up_holder")
        if blend_name:
            object_holder = kxscene.objects.get("torso_up_holder")
            object_holder['blend_file'] = blend_name
    
    elif prefijo == 'pants':
        blend_name = load_clothing_or_hair_or_eyebrows("Pants", pants_directory, "pants", "pants_holder")
        if gender == "male":
            genitals_mesh = kxscene.objects.get("genitals")
        pants = bpy.data.objects.get('pants')  # Devuelve None si no existe el objeto 'pants'
        if pants:
            if gender == "male":
                genitals_mesh.visible = False
        else:
            if gender == "male":
                genitals_mesh.visible = True
        if blend_name:
            object_holder = kxscene.objects.get("pants_holder")
            object_holder['blend_file'] = blend_name    
    elif prefijo == 'shoes':
        blend_name =load_clothing_or_hair_or_eyebrows("Shoes", shoes_directory, "shoes", "shoes_holder")
        if blend_name:
            object_holder = kxscene.objects.get("shoes_holder")
            object_holder['blend_file'] = blend_name
    elif prefijo == 'hair':
        blend_name = load_clothing_or_hair_or_eyebrows("Hair", hair_directory, "hair", "hair_holder")
    
        object_holder = kxscene.objects.get("hair_holder")
        if blend_name:
            object_holder['blend_file'] = blend_name
        else:
        # El pelo ya estaba en escena y no se reasignó blend_file — obtenelo manualmente desde el botón
            for child in owner.children:
                if 'Text' in child:
                    object_holder['blend_file'] = child['Text']
                    break
   
# Llamar a la función que determina qué objeto cargar según el prefijo
load_by_prefix()


