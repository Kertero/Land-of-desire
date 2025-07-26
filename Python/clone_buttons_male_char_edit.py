import bpy
import bge
import os

# Obtener el objeto que quieres duplicar
obj = bpy.context.scene.objects.get("button_cloth_template")  # Asegúrate de que el objeto se llama 'button'
kxscene = bge.logic.getCurrentScene()

directory = os.path.join(bge.logic.expandPath("//"), "Characters", "Male","Clothes", "Torso")
objList = kxscene.objects
object_button_cloth_field = objList['button_cloth_field']
y_offset = 0
collection_name = "HUD"
collection = bpy.data.collections.get(collection_name)


for nombre_archivo in os.listdir(directory):
    # Comprueba si el archivo tiene la extensión .blend
    if nombre_archivo.endswith('.blend'):
        if obj:
            print(nombre_archivo)
    # Duplicar el objeto (esto es como hacerlo manualmente)
            obj_copy = obj.copy()  # Crear una copia del objeto
            obj_copy.data = obj.data.copy()  # Crear una copia de los datos (como malla, materiales, etc.)
            
            # Añadir la copia a la escena
            bpy.context.collection.objects.link(obj_copy)
            obj_copy = kxscene.convertBlenderObject(obj_copy)
            # Establecer las coordenadas de la copia en (0, 0, 0)
            obj_copy.setParent(object_button_cloth_field)
            obj_copy.position = (0, y_offset, 0)
            y_offset -= 0.1
                
            text_obj =  bpy.data.objects.get("button_cloth_text")
            text_copy = text_obj.copy()
            text_copy.data = text_obj.data.copy() 
            collection.objects.link(text_copy)
            text_copy.name = "text:" + nombre_archivo
            text_copy = kxscene.convertBlenderObject(text_copy)
            text_copy.setParent(obj_copy)
            text_copy.position = text_obj.location  # Mantener posición relativa
            text_copy["Text"] = nombre_archivo  # Asignar el nombre de la shape key
        
        else:
            print("El objeto 'button' no se encontró.")
