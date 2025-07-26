import bpy
import bge

cont = bge.logic.getCurrentController()
owner = cont.owner
script_holder_object = bge.logic.getCurrentScene().objects["script_holder"]
mouse_clic = cont.sensors["MouseClick"]
mouse_over = cont.sensors["MouseOverIn"]


personaje = ""
torso = ""
pants = "" 
shoes = "" 
hair = ""
script_holder = bge.logic.getCurrentScene().objects["script_holder"]
gender = script_holder['gender']

if gender == "male":
    body_mesh = bpy.data.objects["man_1"]
if gender == "female":
    body_mesh = bpy.data.objects["female_1"]    



def adjust_mesh_clothes():
        try:
            torso_up_mesh =  bpy.data.objects["torso_up"]
            if torso_up_mesh:
                torso_up_mesh.data.shape_keys.key_blocks[ShapeKey].value = body_mesh.data.shape_keys.key_blocks[ShapeKey].value
        except Exception as e:
            print(f"{e} if it's somerthing about the clothes, it's fine actually")     
        try:
            pants_mesh =  bpy.data.objects["pants"]
            if pants_mesh:
                pants_mesh.data.shape_keys.key_blocks[ShapeKey].value = body_mesh.data.shape_keys.key_blocks[ShapeKey].value 
        except Exception as e:
            print(f"{e} if it's somerthing about the clothes, it's fine actually")     
        try:
            shoes_mesh =  bpy.data.objects["shoes"]
            if shoes_mesh:
                shoes_mesh.data.shape_keys.key_blocks[ShapeKey].value = body_mesh.data.shape_keys.key_blocks[ShapeKey].value 
        except Exception as e:
            print(f"{e} if it's somerthing about the clothes, it's fine actually")     

            

if mouse_clic.positive & mouse_over.positive:
    CommandToExecute, ShapeKey = owner.name.split(":", 1)
    if CommandToExecute=="minus":
        body_mesh.data.shape_keys.key_blocks[ShapeKey].value -= 0.1        
        script_holder_object["ShapeKeyToChange"] = ShapeKey
        adjust_mesh_clothes()
 
    if CommandToExecute=="plus":
        body_mesh.data.shape_keys.key_blocks[ShapeKey].value += 0.1
        script_holder_object["ShapeKeyToChange"] = ShapeKey
        adjust_mesh_clothes()         
            
            
                