
import bge
import os

cont = bge.logic.getCurrentController()
owner = cont.owner

mouse_clic = cont.sensors["MouseClic"]
mouse_over = cont.sensors["MouseOver"]

# Propiedad del objeto con el nombre del archivo .blend
this_blend = owner.get("destiny")  # por ejemplo: "character_editor.blend"
# Propiedad del objeto con el nombre de la escena dentro de ese .blend
scene_name_destiny = owner.get("scene_name")  # por ejemplo: "editor_scene"


# volver_al_menu.py
if mouse_clic.positive and mouse_over.positive:
    LibFree(this_blend)
    replaceScene(scene_name_destiny)
