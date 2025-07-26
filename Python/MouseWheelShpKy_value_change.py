import bpy
import bge

cont = bge.logic.getCurrentController()
owner = cont.owner
body_mesh = bpy.data.objects["man_1"]
script_holder_object = bge.logic.getCurrentScene().objects["script_holder"]

mouse_over = cont.sensors["MouseOver"]
mouse_WheelUp = cont.sensors["MouseWheelUp"]
mouse_WheelDown = cont.sensors["MouseWheelDown"]


if mouse_WheelUp.positive & mouse_over.positive:
    CommandToExecute, ShapeKey = owner.name.split(":", 1)
    body_mesh.data.shape_keys.key_blocks[ShapeKey].value += 0.01
    script_holder_object["ShapeKeyToChange"] = ShapeKey
    
if mouse_WheelDown.positive & mouse_over.positive:
    CommandToExecute, ShapeKey = owner.name.split(":", 1)
    body_mesh.data.shape_keys.key_blocks[ShapeKey].value -= 0.01
    script_holder_object["ShapeKeyToChange"] = ShapeKey
    


   