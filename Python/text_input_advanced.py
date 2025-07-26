import bge
from bge import logic, events



def main(cont):

    own = cont.owner

    # Si no está en modo edición, salimos
    if not own.get('editing', False):
        return

    keyboard = logic.keyboard
    status = logic.KX_INPUT_JUST_ACTIVATED
    is_shift = keyboard.events[events.LEFTSHIFTKEY] == logic.KX_INPUT_ACTIVE or \
               keyboard.events[events.RIGHTSHIFTKEY] == logic.KX_INPUT_ACTIVE

    # Accedemos al objeto de texto
    if "char_name" not in own.children:
        print("char_name no encontrado en hijos de textbox.")
        return

    text_obj = own.children["char_name"]
    current_text = text_obj.get("Text", "")

    # Diccionario de teclas básicas
    normal_keys = {
        events.AKEY: 'a', events.BKEY: 'b', events.CKEY: 'c', events.DKEY: 'd',
        events.EKEY: 'e', events.FKEY: 'f', events.GKEY: 'g', events.HKEY: 'h',
        events.IKEY: 'i', events.JKEY: 'j', events.KKEY: 'k', events.LKEY: 'l',
        events.MKEY: 'm', events.NKEY: 'n', events.OKEY: 'o', events.PKEY: 'p',
        events.QKEY: 'q', events.RKEY: 'r', events.SKEY: 's', events.TKEY: 't',
        events.UKEY: 'u', events.VKEY: 'v', events.WKEY: 'w', events.XKEY: 'x',
        events.YKEY: 'y', events.ZKEY: 'z',
        events.SPACEKEY: ' ',
        events.ZEROKEY: '0', events.ONEKEY: '1', events.TWOKEY: '2',
        events.THREEKEY: '3', events.FOURKEY: '4', events.FIVEKEY: '5',
        events.SIXKEY: '6', events.SEVENKEY: '7', events.EIGHTKEY: '8', events.NINEKEY: '9',
    }

    shift_keys = {
        '1': '!', '2': '"', '3': '#', '4': '$', '5': '%',
        '6': '&', '7': '/', '8': '(', '9': ')', '0': '=',
    }

    for key_code, char in normal_keys.items():
        if keyboard.events[key_code] == status:
            if is_shift:
                char = shift_keys.get(char, char.upper())
            current_text += char
            text_obj["Text"] = current_text
            return

    # Borrar con backspace
    if keyboard.events[events.BACKSPACEKEY] == status:
        text_obj["Text"] = current_text[:-1]


main(bge.logic.getCurrentController())

