import bge

cont = bge.logic.getCurrentController()
own = cont.owner  # El botón que fue clickeado

mouse_clic = cont.sensors["MouseClick"]
mouse_over = cont.sensors["MouseOver"]

if mouse_clic.positive and mouse_over.positive:
    scene = bge.logic.getCurrentScene()
    target = scene.objects.get("character_selector_script_holder")
    if not target:
        print("ERROR: No se encontró 'character_selector_script_holder'")
       

    # Validar que el botón tenga propiedades válidas
    if "file" not in own or "gender" not in own:
        print("ERROR: El botón no tiene 'file' o 'gender'")
        

    filename = own["file"]
    gender = own["gender"]

    if gender == "male":
        target["male_char"] = filename
      #  print(f"Asignado male_char = {filename}")
    elif gender == "female":
        target["female_char"] = filename
     #   print(f"Asignado female_char = {filename}")
    else:
        print(f"ERROR: género desconocido '{gender}'")
