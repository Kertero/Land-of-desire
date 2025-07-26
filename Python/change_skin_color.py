import bpy
import bge

cont = bge.logic.getCurrentController()
owner = cont.owner
mouse_clic = cont.sensors["MouseClick"]
mouse_over = cont.sensors["MouseOverIn"]

script_holder = bge.logic.getCurrentScene().objects["script_holder"]
gender = script_holder['gender']

if gender == "male":
    personaje = bge.logic.getCurrentScene().objects['man_1']
    personaje_name = "man_1"
if gender == "female":
    personaje = bge.logic.getCurrentScene().objects['female_1']
    personaje_name = "female_1"


def change_color(obj_name, material_name, channel, value):
    """
    Cambia el valor de 'hue', 'saturation' o 'value' en un nodo Hue/Saturation/Value de un material de un objeto.

    :param obj_name: Nombre del objeto que contiene el material.
    :param material_name: Nombre del material que se quiere modificar.
    :param channel: 'hue', 'saturation' o 'value'.
    :param value: Valor a asignar (entre 0 y 1, o más si querés efectos raros).
    """
    obj = bpy.data.objects.get(obj_name)
    if not obj:
#        print(f"[ERROR] Objeto '{obj_name}' no encontrado.")
        return

    if channel not in ["hue", "saturation", "value"]:
       # print(f"[ERROR] Canal '{channel}' no válido. Usar: hue, saturation o value.")
        return

    for mat_slot in obj.material_slots:
        mat = mat_slot.material
        if mat and mat.name == material_name:
            if not mat.use_nodes:
#                print(f"[WARNING] Material '{material_name}' no usa nodos.")
                return

            hsv_node = next((n for n in mat.node_tree.nodes if n.type == 'HUE_SAT'), None)
            if not hsv_node:
#                print(f"[WARNING] Nodo HUE_SAT no encontrado en '{material_name}'.")
                return

            channel_index = {
                "hue": 0,
                "saturation": 1,
                "value": 2
            }

            hsv_node.inputs[channel_index[channel]].default_value = value
#            print(f"[OK] Canal '{channel}' de '{material_name}' en '{obj_name}' actualizado a {value}")
            return

#    print(f"[ERROR] Material '{material_name}' no encontrado en objeto '{obj_name}'.")


        
def update_slider_bar(slider_name, property_value, scale=100):
    """
    Actualiza el valor de un slider en base a la propiedad dada y un factor de escala.

    :param slider_name: Nombre del objeto slider en la escena.
    :param property_value: Valor numérico de la propiedad que se quiere mostrar.
    :param scale: Factor de escala para transformar el valor (por defecto es 100).
    """
    # Obtiene la escena actual
    scene = bge.logic.getCurrentScene()
    
    # Obtiene el objeto slider usando su nombre
    slider_bar = scene.objects.get(slider_name)
    if slider_bar is None:
        print(f"No se encontró el slider con el nombre: {slider_name}")
        return
    
    # Actualiza la propiedad "slider_value" del objeto
    slider_bar["slider_value"] = property_value * scale
       


#-------------------------------------------------------------------------------


if mouse_clic.positive & mouse_over.positive:
    CommandToExecute, SliderName, geometry = owner.name.split(":", 2)
    
# Piel --------------------------------    

    if CommandToExecute=="minus" and SliderName=="hue" and geometry=="skin":
        personaje["skin_hue"] -= 0.05        
        change_color("genitals", "Human.caucasian.skin", "hue", personaje["skin_hue"])     
        change_color(personaje_name, "Human.caucasian.skin", "hue", personaje["skin_hue"]) 
        update_slider_bar("slider:hue:skin", personaje["skin_hue"])            
 
    if CommandToExecute=="plus" and SliderName=="hue"and geometry=="skin":
        personaje["skin_hue"] += 0.05    
        change_color("genitals", "Human.caucasian.skin", "hue", personaje["skin_hue"])     
        change_color(personaje_name, "Human.caucasian.skin", "hue", personaje["skin_hue"])                       
        update_slider_bar("slider:hue:skin", personaje["skin_hue"])    

    if CommandToExecute=="minus" and SliderName=="sat" and geometry=="skin":
        personaje["skin_sat"] -= 0.05        
        change_color("genitals", "Human.caucasian.skin", "saturation", personaje["skin_sat"])     
        change_color(personaje_name, "Human.caucasian.skin", "saturation", personaje["skin_sat"]) 
        update_slider_bar("slider:sat:skin", personaje["skin_sat"])            
 
    if CommandToExecute=="plus" and SliderName=="sat"and geometry=="skin":
        personaje["skin_sat"] += 0.05    
        change_color("genitals", "Human.caucasian.skin", "saturation", personaje["skin_sat"])     
        change_color(personaje_name, "Human.caucasian.skin", "saturation", personaje["skin_sat"])                       
        update_slider_bar("slider:sat:skin", personaje["skin_sat"])    
                        
    if CommandToExecute=="minus" and SliderName=="val" and geometry=="skin":
        personaje["skin_val"] -= 0.05        
        change_color("genitals", "Human.caucasian.skin", "value", personaje["skin_val"])     
        change_color(personaje_name, "Human.caucasian.skin", "value", personaje["skin_val"]) 
        update_slider_bar("slider:val:skin", personaje["skin_val"])            
 
    if CommandToExecute=="plus" and SliderName=="val"and geometry=="skin":
        personaje["skin_val"] += 0.05    
        change_color("genitals", "Human.caucasian.skin", "value", personaje["skin_val"])     
        change_color(personaje_name, "Human.caucasian.skin", "value", personaje["skin_val"])                       
        update_slider_bar("slider:val:skin", personaje["skin_val"])    
        
# Iris --------------------------    
        
    if CommandToExecute=="minus" and SliderName=="hue" and geometry=="iris":
        personaje["iris_hue"] -= 0.05            
        change_color(personaje_name, "Human.eyes.iris", "hue", personaje["iris_hue"]) 
        update_slider_bar("slider:hue:iris", personaje["iris_hue"])            
 
    if CommandToExecute=="plus" and SliderName=="hue"and geometry=="iris":
        personaje["iris_hue"] += 0.05       
        change_color(personaje_name, "Human.eyes.iris", "hue", personaje["iris_hue"])                       
        update_slider_bar("slider:hue:iris", personaje["iris_hue"])    
                        
    if CommandToExecute=="minus" and SliderName=="sat" and geometry=="iris":
        personaje["iris_sat"] -= 0.05            
        change_color(personaje_name, "Human.eyes.iris", "saturation", personaje["iris_sat"]) 
        update_slider_bar("slider:sat:iris", personaje["iris_sat"])            
 
    if CommandToExecute=="plus" and SliderName=="sat"and geometry=="iris":
        personaje["iris_sat"] += 0.05       
        change_color(personaje_name, "Human.eyes.iris", "saturation", personaje["iris_sat"])                       
        update_slider_bar("slider:sat:iris", personaje["iris_sat"])    

    if CommandToExecute=="minus" and SliderName=="val" and geometry=="iris":
        personaje["iris_val"] -= 0.05            
        change_color(personaje_name, "Human.eyes.iris", "value", personaje["iris_val"]) 
        update_slider_bar("slider:val:iris", personaje["iris_val"])            
 
    if CommandToExecute=="plus" and SliderName=="val"and geometry=="iris":
        personaje["iris_val"] += 0.05       
        change_color(personaje_name, "Human.eyes.iris", "value", personaje["iris_val"])                       
        update_slider_bar("slider:val:iris", personaje["iris_val"])    
        
        
#Cejas --------------------------        
  
    if CommandToExecute=="minus" and SliderName=="hue" and geometry=="brow":
        personaje["brow_hue"] -= 0.05            
        change_color(personaje_name, "Human.brows", "hue", personaje["brow_hue"]) 
        update_slider_bar("slider:hue:brow", personaje["brow_hue"])            
 
    if CommandToExecute=="plus" and SliderName=="hue" and geometry=="brow":
        personaje["brow_hue"] += 0.05       
        change_color(personaje_name, "Human.brows", "hue", personaje["brow_hue"])                       
        update_slider_bar("slider:hue:brow", personaje["brow_hue"])    
                        
    if CommandToExecute=="minus" and SliderName=="sat" and geometry=="brow":
        personaje["brow_sat"] -= 0.05            
        change_color(personaje_name, "Human.brows", "saturation", personaje["brow_sat"]) 
        update_slider_bar("slider:sat:brow", personaje["brow_sat"])            
 
    if CommandToExecute=="plus" and SliderName=="sat" and geometry=="brow":
        personaje["brow_sat"] += 0.05       
        change_color(personaje_name, "Human.brows", "saturation", personaje["brow_sat"])                       
        update_slider_bar("slider:sat:brow", personaje["brow_sat"])    

    if CommandToExecute=="minus" and SliderName=="val" and geometry=="brow":
        personaje["brow_val"] -= 0.05            
        change_color(personaje_name, "Human.brows", "value", personaje["brow_val"]) 
        update_slider_bar("slider:val:brow", personaje["brow_val"])            
 
    if CommandToExecute=="plus" and SliderName=="val" and geometry=="brow":
        personaje["brow_val"] += 0.05       
        change_color(personaje_name, "Human.brows", "value", personaje["brow_val"])                       
        update_slider_bar("slider:val:brow", personaje["brow_val"])    
                                                                           