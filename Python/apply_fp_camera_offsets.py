import bge
from mathutils import Vector

def apply_fp_camera_offsets(cont):
    scene = bge.logic.getCurrentScene()
    objects = scene.objects

    cam = objects.get("Man_FPV_Camera")
    head = objects.get("man_head_z")
    proxy = objects.get("Male_head_bone_proxy")

    if not (cam and head and proxy):
        print("[ERROR] Objeto(s) no encontrado(s):")
        if not cam: print(" - Man_FPV_Camera")
        if not head: print(" - man_head_z")
        if not proxy: print(" - Male_head_bone_proxy")
        return

    # Offset deseado respecto al proxy
    cam_offset = Vector((0.0, 0.02, 0.02))      # Ajustá según necesites
    head_offset = Vector((0.0, -0.131586, 0.05081))

    # Aplicar posición con offset en el espacio local del proxy
 #   cam.worldPosition = proxy.worldTransform @ cam_offset
#    head.worldPosition = proxy.worldTransform @ head_offset
    rotated_offset = proxy.worldOrientation @ cam_offset
    cam.worldPosition = proxy.worldPosition + rotated_offset
    head.worldPosition = proxy.worldPosition + rotated_offset

    print(head.worldPosition)

# Ejecutar la función
apply_fp_camera_offsets(bge.logic.getCurrentController())
