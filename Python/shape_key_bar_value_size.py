import bpy
import bge

cont = bge.logic.getCurrentController()
ThisObject = cont.owner
property_changed = cont.sensors["Property"]


personaje = ""
torso = "" 
pants = "" 
shoes = "" 
hair = ""
kxscene = bge.logic.getCurrentScene()
objList = kxscene.objects
script_holder = objList["script_holder"]
gender = script_holder['gender']
script_holder = objList["script_holder"]
gender = script_holder['gender']


if gender == "male":
    body_mesh = bpy.data.objects["man_1"]
if gender == "female":
    body_mesh = bpy.data.objects["female_1"]    



if  property_changed.positive and ThisObject["ShapeKeyToChange"] != "":
    slider_bar_to_modify_name = "slider:"+ ThisObject["ShapeKeyToChange"]
    slider_bar_to_modify = bge.logic.getCurrentScene().objects[slider_bar_to_modify_name]
    slider_bar_to_modify["slider_value"] = body_mesh.data.shape_keys.key_blocks[ThisObject["ShapeKeyToChange"]].value * 100
    ThisObject["ShapeKeyToChange"] = ""    
