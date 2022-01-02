#!/usr/bin/env python3

from __future__ import annotations

from typing import (
    Tuple,
    List,
    Dict,
    Callable,
    TypedDict,
    Final,
    Union,
    Pattern,
    Match,
    Optional,
    Literal,
    Iterator,
    cast,
)

import argparse
import functools
import json
import pprint
import os
import pprint
import re

import miniamf.sol

SLOT_FILE_RE: Final[Pattern] = re.compile(r'^(\d+):(.+)$')

CHARA_FIELDS: Final[Tuple[str, ...]] = (
    'accessory', 'accessorycolor', 'accessorycoloralt',
    'ahoge',
    'answer1x', 'answer2x', 'answer3x', 'answer4x', 'answer5x', 'answer6x',
    'answer7x', 'answer8x',
    'backhair',
    'backweapon', 'backweaponcolor', 'backweaponcoloralt',
    'belt', 'beltcolor', 'beltcoloralt',
    'bg',
    'blush',
    'cape', 'capecolor', 'capecoloralt',
    'chin',
    'elementx',
    'eye1color', 'eye2color',
    'eyebrows',
    'eyecam',
    'eyehigh',
    'eyes',
    'eyewink',
    'fronthair',
    'gender',
    'glasses', 'glassescolor', 'glassescoloralt',
    'gloves', 'glovescolor', 'glovescoloralt',
    'haircolor', 'haircoloracc', 'haircoloralt', 'haircolorfade',
    'hat', 'hatcolor', 'hatcoloralt',
    'head',
    'heightx',
    'job',
    'mouth',
    'namex',
    'other', 'othercolor', 'othercoloralt',
    'pants', 'pantscolor', 'pantscoloralt',
    'ponytail',
    'pupil', 'pupil1color', 'pupil2color',
    'rarityx',
    'rearhair',
    'relationship',
    'scarf', 'scarfcolor', 'scarfcoloralt',
    'shadow',
    'shield', 'shieldcolor', 'shieldcoloralt',
    'shirt', 'shirtcolor', 'shirtcoloralt',
    'shoes', 'shoescolor', 'shoescoloralt',
    'skincolor',
    'sleeves', 'sleevescolor', 'sleevescoloralt',
    'stance',
    'tail', 'tailcolor', 'tailcoloralt',
    'trait',
    'weapon', 'weaponcolor', 'weaponcoloralt',
    'wings', 'wingscolor', 'wingscoloralt',
)

CHARA_FIELDS_CLUB: Final[Tuple[str, ...]] = (
    'namex', 'birthday', 'age', 'profile', 'creator', 'favcolor', 'favfood',
    'location','personality', 'occupation', 'avatar', 'club', 'title', 'icon',
    'heightx','heighty', 'pose', 'rotation', 'flip', 'shadow', 'headlayer',
    'objectshadow','fronthair', 'rearhair', 'backhair', 'ponytail', 'ahoge',
    'eyes1x','eyes2x', 'eyebrows1x', 'eyebrows2x', 'pupil1x', 'pupil2x',
    'mouth','glasses', 'accessory1x', 'accessory2x', 'accessory3x', 'hat',
    'other1x','other2x', 'other3x', 'other4x', 'shirt', 'shirtex',
    'sleeves1x','sleeves2x', 'pants1x', 'pants2x', 'socks1x', 'socks2x',
    'shoes1x','shoes2x', 'belt1x', 'belt2x', 'gloves1x', 'gloves2x',
    'wrist1x','wrist2x', 'cape', 'scarf1x', 'scarf2x', 'wings1x', 'wings2x',
    'tail','shoulder1x', 'shoulder2x', 'weapon1x', 'weapon2x', 'weaponsize1x',
    'weaponsize2x','shield', 'eyecam', 'eyehigh', 'headshape', 'nose',
    'blush','headsize', 'headsizey', 'headflip', 'blushpos', 'nosepos',
    'hand1x','hand2x', 'propsize1x', 'propsize2x', 'proprot1x', 'proprot2x',
    'shieldsize','shieldrot', 'knee1x', 'knee2x', 'logo', 'logopos',
    'faceshadow','tint', 'displayoutline', 'special', 'specialsizex',
    'specialsizey','specialtint', 'objectpose', 'petequip', 'blinkani',
    'wingsani','capeani', 'tailani', 'leyexpos', 'leyeypos', 'leyesize',
    'leyesizey','leyerot', 'reyexpos', 'reyeypos', 'reyesize', 'reyesizey',
    'reyerot','lpupilxpos', 'lpupilypos', 'lpupilsize', 'lpupilsizey',
    'lpupilrot','rpupilxpos', 'rpupilypos', 'rpupilsize', 'rpupilsizey',
    'rpupilrot','leyebrowxpos', 'leyebrowypos', 'leyebrowsize',
    'leyebrowsizey','leyebrowrot', 'reyebrowxpos', 'reyebrowypos',
    'reyebrowsize','reyebrowsizey', 'reyebrowrot', 'mouthxpos', 'mouthypos',
    'mouthsize','mouthsizey', 'mouthrot', 'nosexpos', 'noseypos', 'nosesize',
    'nosesizey','noserot', 'hatxpos', 'hatypos', 'hatsize', 'hatsizey',
    'hatrot','glassesxpos', 'glassesypos', 'glassessize', 'glassessizey',
    'glassesrot','other1xpos', 'other1ypos', 'other1size', 'other1sizey',
    'other1rot','other2xpos', 'other2ypos', 'other2size', 'other2sizey',
    'other2rot','other3xpos', 'other3ypos', 'other3size', 'other3sizey',
    'other3rot','other4xpos', 'other4ypos', 'other4size', 'other4sizey',
    'other4rot','acc1xpos', 'acc1ypos', 'acc1size', 'acc1sizey', 'acc1rot',
    'acc2xpos','acc2ypos', 'acc2size', 'acc2sizey', 'acc2rot', 'acc3xpos',
    'acc3ypos','acc3size', 'acc3sizey', 'acc3rot', 'capesize', 'capesizey',
    'caperot','tailsize', 'tailsizey', 'tailrot', 'wingxpos', 'wingypos',
    'wingsize','wingsizey', 'wingrot', 'facepreset', 'highlights',
    'fronthairxpos','fronthairypos', 'fronthairxscale', 'fronthairyscale',
    'ahogexpos','ahogeypos', 'ahogexscale', 'ahogeyscale', 'fronthairrot',
    'backhairrot','ahogerot', 'mypetshadowx', 'mypetposx', 'mypetxposx',
    'mypetyposx','mypetxscalex', 'mypetyscalex', 'mypetrotx', 'displayhead',
    'displayface','displayhair', 'displaybody', 'displayshoulder',
    'displayhand','displaybackshoulder', 'displaybackhand', 'displaythigh',
    'displayfoot','displaybackthigh', 'displaybackfoot', 'namefontx',
    'chatfontx','bubblex', 'emotex', 'chatstylex', 'bgx', 'bgxposx',
    'bgyposx','bgxscalex', 'bgyscalex', 'bgtintx', 'fgx', 'fgtintx',
    'backhairxpos','backhairypos', 'backhairxscale', 'backhairyscale',
    'ponytailxpos','ponytailypos', 'ponytailxscale', 'ponytailyscale',
    'ponytailrot','capexpos', 'capeypos', 'tailxpos', 'tailypos',
    'specialxpos','specialypos', 'special2x', 'specialxpos2x',
    'specialypos2x','specialsizex2x', 'specialsizey2x', 'specialtint2x',
    'specialrot','specialrot2x', 'propxpos1x', 'propypos1x', 'propxpos2x',
    'propypos2x','shieldxpos', 'shieldypos', 'fhairani', 'bhairani',
    'skincolor1x','skincolor2x', 'rearhaircolor1x', 'rearhaircolor2x',
    'rearhaircolor3x','fronthaircolor1x', 'fronthaircolor2x',
    'fronthaircolor3x','backhaircolor1x', 'backhaircolor2x',
    'backhaircolor3x','ponytailcolor1x', 'ponytailcolor2x', 'ponytailcolor3x',
    'ahogecolor1x','ahogecolor2x', 'ahogecolor3x', 'hairacccolorx',
    'hairtipscolorx','eye1color1x', 'eye1color2x', 'eye1color3x',
    'eye2color1x','eye2color2x', 'eye2color3x', 'pupil1color1x',
    'pupil1color2x','pupil2color1x', 'pupil2color2x', 'eyebrows1color1x',
    'eyebrows1color2x','eyebrows2color1x', 'eyebrows2color2x',
    'glassescolor1x','glassescolor2x', 'glassescolor3x', 'accessory1color1x',
    'accessory1color2x','accessory1color3x', 'accessory2color1x',
    'accessory2color2x','accessory2color3x', 'accessory3color1x',
    'accessory3color2x','accessory3color3x', 'blushcolorx', 'logocolorx',
    'nosecolor1x','nosecolor2x', 'mouthcolor1x', 'mouthcolor2x',
    'mouthcolor3x','hatcolor1x', 'hatcolor2x', 'hatcolor3x', 'other1color1x',
    'other1color2x','other1color3x', 'other2color1x', 'other2color2x',
    'other2color3x','other3color1x', 'other3color2x', 'other3color3x',
    'other4color1x','other4color2x', 'other4color3x', 'shirtcolor1x',
    'shirtcolor2x','shirtcolor3x', 'shirtexcolor1x', 'shirtexcolor2x',
    'shirtexcolor3x','shoulder1color1x', 'shoulder1color2x',
    'shoulder1color3x','shoulder2color1x', 'shoulder2color2x',
    'shoulder2color3x','sleeves1color1x', 'sleeves1color2x',
    'sleeves1color3x','sleeves2color1x', 'sleeves2color2x', 'sleeves2color3x',
    'pants1color1x','pants1color2x', 'pants1color3x', 'pants2color1x',
    'pants2color2x','pants2color3x', 'belt1color1x', 'belt1color2x',
    'belt1color3x','belt2color1x', 'belt2color2x', 'belt2color3x',
    'gloves1color1x','gloves1color2x', 'gloves1color3x', 'gloves2color1x',
    'gloves2color2x','gloves2color3x', 'shoes1color1x', 'shoes1color2x',
    'shoes1color3x','shoes2color1x', 'shoes2color2x', 'shoes2color3x',
    'socks1color1x','socks1color2x', 'socks1color3x', 'socks2color1x',
    'socks2color2x','socks2color3x', 'capecolor1x', 'capecolor2x',
    'capecolor3x','scarf1color1x', 'scarf1color2x', 'scarf1color3x',
    'scarf2color1x','scarf2color2x', 'scarf2color3x', 'wings1color1x',
    'wings1color2x','wings1color3x', 'wings2color1x', 'wings2color2x',
    'wings2color3x','tailcolor1x', 'tailcolor2x', 'tailcolor3x',
    'weapon1color1x','weapon1color2x', 'weapon1color3x', 'weapon2color1x',
    'weapon2color2x','weapon2color3x', 'shieldcolor1x', 'shieldcolor2x',
    'shieldcolor3x','wrist1color1x', 'wrist1color2x', 'wrist1color3x',
    'wrist2color1x','wrist2color2x', 'wrist2color3x', 'knee1color1x',
    'knee1color2x','knee1color3x', 'knee2color1x', 'knee2color2x',
    'knee2color3x','faceshadowcolorx', 'tintcolorx', 'tintspecialcolorx',
    'namecolorx','chatcolorx', 'bubblecolorx', 'bubblecolor2x',
    'bgtintcolorx','bgcolor1x', 'bgcolor2x', 'fgtintcolorx',
    'tintspecialcolor2x',
)

COLOR_FIELDS_CLUB = set(CHARA_FIELDS_CLUB[CHARA_FIELDS_CLUB.index('skincolor1x'):])

CHARSTRING_JOINER_1D = '|'
CHARSTRING_JOINER_2D = '¦'

ERR_NO_CHARA_FIELD = 'Unable to find character fields. Is this a Gacha Life save?'

class CharacterExtractorError(ValueError):
    pass

CharaDict = Dict[str, Union[int, str]]
FlatternedCharaDict = Dict[str, Union[int, str]]
CharaList = List[CharaDict]
DoCallback = Callable[[miniamf.sol.SOL, CharaList, argparse.ArgumentParser, argparse.Namespace], None]

def slotfile(v: str) -> Tuple[int, str]:
    m: Optional[Match] = SLOT_FILE_RE.match(v)
    if m is None:
        raise ValueError(f'Malformed string "{v}"')
    return int(m.group(1)), m.group(2)

def parse_args() -> Tuple[argparse.ArgumentParser, argparse.Namespace]:
    p = argparse.ArgumentParser()
    p.add_argument('savefile', help='Save file.')
    p.add_argument('-B', '--no-save-backup', action='store_true', default=False, help='Do not create backup for save file.')
    sps = p.add_subparsers(dest='action', metavar='action', help='Action.')

    sp = sps.add_parser('list-charas', help='List characters.')

    sp = sps.add_parser('import-charas', help='Import characters from JSON files.')
    sp.add_argument('chara_mapping', nargs='+', type=slotfile, help='Slot mapped to character file (specified as <slot>:<file>).')

    sp = sps.add_parser('export-charas', help='Export characters as JSON files.')
    sp.add_argument('chara_mapping', nargs='+', type=slotfile, help='Slot mapped to character file (specified as <slot>:<file>).')

    sp = sps.add_parser('dump-all', help='Pretty print all values in the save file. For testing only.')

    sp = sps.add_parser('update', help='Merge a JSON object into the save file, similar to Python\'s dict.update() method. For testing only and may break the save file if the JSON object contains bad values.')
    sp.add_argument('jsonobj', help='File containing the JSON object.')

    return p, p.parse_args()

def club_charstring_to_dict(charstring: str, expand_color: bool = False) -> CharaDict:
    charstring_splitted = charstring.split(CHARSTRING_JOINER_1D)
    assert len(charstring_splitted) == len(CHARA_FIELDS_CLUB), 'Malformed charstring.'
    obj: CharaDict = {}
    for key, val in zip(CHARA_FIELDS_CLUB, charstring_splitted):
        if expand_color and key in COLOR_FIELDS_CLUB:
            obj[key] = f'0x{val}'
        else:
            obj[key] = val
    return obj

def iterate_club_extraslot(sol: miniamf.sol.SOL) -> Iterator[CharaDict]:
    slots = sol['extraslotstring'].split(CHARSTRING_JOINER_2D)
    if len(slots) != 90:
        raise ValueError('Splitted extraslotstring must contain exactly 90 items.')
    for charstring in slots:
        obj = club_charstring_to_dict(charstring, True)
        yield obj

def club_chara_list_to_extraslotstring(chara_list: CharaList) -> str:
    return CHARSTRING_JOINER_2D.join(map(functools.partial(club_chara_dict_to_charstring, compact_color=True), chara_list))

def club_chara_dict_to_charstring(obj: CharaDict, compact_color: bool = False) -> str:
    def _compact_color_fields(obj: CharaDict, compact_color: bool):
        for key in CHARA_FIELDS_CLUB:
            if compact_color and key in COLOR_FIELDS_CLUB and isinstance(obj[key], str) and cast(str, obj[key]).startswith('0x'):
                yield cast(str, obj[key])[2:]
            else:
                yield str(obj[key])
    charstring = CHARSTRING_JOINER_1D.join(_compact_color_fields(obj, compact_color))
    return charstring

def detect_save_format(sol: miniamf.sol.SOL) -> Literal['club', 'life', 'unknown']:
    if 'accessory1' in sol:
        return 'life'
    elif 'charstring1' in sol:
        return 'club'
    else:
        return 'unknown'

def extract_characters(sol: miniamf.sol.SOL) -> CharaList:
    def _iterator_life(sol: miniamf.sol.SOL) -> Iterator[CharaDict]:
        for chara_index in range(1, 21):
            obj = {field_name: sol[f'{field_name}{chara_index}'] for field_name in CHARA_FIELDS}
            obj['_type'] = 'life'
            yield obj

    def _iterator_club(sol: miniamf.sol.SOL) -> Iterator[CharaDict]:
        for active_chara_index in range(1, 11):
            obj = club_charstring_to_dict(sol[f'charstring{active_chara_index}'])
            obj['_type'] = 'club'
            yield obj
        for obj in iterate_club_extraslot(sol):
            obj['_type'] = 'club'
            yield obj

    save_format = detect_save_format(sol)

    try:
        if save_format == 'life':
            print('Detected Gacha Life save data.')
            return list(_iterator_life(sol))
        elif save_format == 'club':
            print('Detected Gacha Club save data.')
            return list(_iterator_club(sol))
        else:
            raise CharacterExtractorError('AMF file is missing required fields. Is this a Gacha save file?')
    except Exception as e:
        raise CharacterExtractorError('Error when parsing save file. Corrupted save?') from e


def flattern_character(slot: int, chara: CharaDict) -> FlatternedCharaDict:
    return {f'{field}{slot}': value for field, value in chara.items()}

def _save_sol(sol: miniamf.sol.SOL, savefile: str, skip_backup: bool):
    output: str = savefile
    if not skip_backup:
        os.rename(output, f'{output}.bak')

    with open(output, 'wb') as solfile:
        sol.save(solfile, miniamf.AMF3)

def do_list_charas(sol: miniamf.sol.SOL, charas: CharaList, p: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    for slot, chara in enumerate(charas):
        print(f'Slot #{slot+1}: {chara["namex"]}')

def do_export_charas(sol: miniamf.sol.SOL, charas: CharaList, p: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    save_format = detect_save_format(sol)
    max_slot_index = {'life': 20, 'club': 100}[save_format]
    chara_mapping: List[Tuple[int, str]] = args.chara_mapping

    for slot, _ in chara_mapping:
        if not (1 <= slot <= max_slot_index):
            p.error(f'Invalid character slot #{slot}')
    for slot, filename in chara_mapping:
        with open(filename, 'w') as f:
            json.dump(charas[slot-1], f)

def do_import_charas(sol: miniamf.sol.SOL, charas: CharaList, p: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    save_format = detect_save_format(sol)
    chara_mapping: List[Tuple[int, str]] = args.chara_mapping

    if save_format == 'life':
        import_charas_life(sol, charas, p, chara_mapping)
    elif save_format == 'club':
        import_charas_club(sol, charas, p, chara_mapping)

    _save_sol(sol, args.savefile, args.no_save_backup)

def import_charas_life(sol: miniamf.sol.SOL, charas: CharaList, p: argparse.ArgumentParser, chara_mapping: List[Tuple[int, str]]) -> None:
    for slot, _ in chara_mapping:
        if not (1 <= slot <= 20):
            p.error(f'Invalid character slot #{slot}')
    for slot, filename in chara_mapping:
        with open(filename, 'r') as f:
            chara = json.load(f)
        if chara.get('_type', 'life') != 'life':
            p.error(f"'{filename}' is not a Gacha Life chara file.")
        if '_type' in chara:
            del chara['_type']
        flatterned_chara = flattern_character(slot, chara)
        sol.update(flatterned_chara)

def import_charas_club(sol: miniamf.sol.SOL, charas: CharaList, p: argparse.ArgumentParser, chara_mapping: List[Tuple[int, str]]) -> None:
    extra_updated = False
    extra_slots: CharaList = list(iterate_club_extraslot(sol))
    extra_names: List[str] = sol['extranamestring'].split(CHARSTRING_JOINER_1D)

    for slot, _ in chara_mapping:
        if not (1 <= slot <= 100):
            p.error(f'Invalid character slot #{slot}')
    for slot, filename in chara_mapping:
        with open(filename, 'r') as f:
            chara = json.load(f)
        if chara.get('_type', 'life') != 'club':
            p.error(f"'{filename}' is not a Gacha Club chara file.")
        for key, val in chara.items():
            if isinstance(val, str) and (CHARSTRING_JOINER_1D in val or CHARSTRING_JOINER_2D in val):
                print("WARNING: Replacing array delimiter in file '{filename}', field '{key}' with '_'.")
                chara[key] = val.replace(CHARSTRING_JOINER_1D, '_').replace(CHARSTRING_JOINER_2D, '_')
        if '_type' in chara:
            del chara['_type']
        if slot <= 10:
            charstring = club_chara_dict_to_charstring(chara)
            sol[f'charstring{slot}'] = charstring
        else:
            extra_updated = True
            # slot #11 is array index 0
            slot -= 11
            extra_slots[slot] = chara
            extra_names[slot] = chara['namex']
    if extra_updated:
        sol['extranamestring'] = CHARSTRING_JOINER_1D.join(extra_names)
        sol['extraslotstring'] = club_chara_list_to_extraslotstring(extra_slots)

def do_dump_all(sol: miniamf.sol.SOL, _charas: CharaList, _p: argparse.ArgumentParser, _args: argparse.Namespace) -> None:
    pprint.pprint(dict(sol))

def do_update(sol: miniamf.sol.SOL, _charas: CharaList, _p: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    with open(args.jsonobj, 'r') as f:
        obj = json.load(f)

    sol.update(obj)

    _save_sol(sol, args.savefile, args.no_save_backup)

ACTIONS: Dict[str, DoCallback] = {
    'list-charas': do_list_charas,
    'export-charas': do_export_charas,
    'import-charas': do_import_charas,
    'dump-all': do_dump_all,
    'update': do_update,
}

if __name__ == '__main__':
    p, args = parse_args()

    with open(args.savefile, 'rb') as f:
        sol = miniamf.sol.load(f)

    charas: CharaList = []
    try:
        charas = extract_characters(sol)
    except CharacterExtractorError:
        if args.action in ('dump-all', 'update'):
            print(f'WARNING: {ERR_NO_CHARA_FIELD}')
        else:
            p.error(ERR_NO_CHARA_FIELD)
            raise

    action: DoCallback = ACTIONS[args.action]

    action(sol, charas, p, args)
