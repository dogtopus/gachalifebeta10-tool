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
)

import argparse
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

ERR_NO_CHARA_FIELD = 'Unable to find character fields. Is this a Gacha Life save?'

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

def extract_characters(sol: miniamf.sol.SOL) -> CharaList:
    return list({ field_name: sol[f'{field_name}{chara_index}'] for field_name in CHARA_FIELDS } for chara_index in range(1, 21))

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
    chara_mapping: List[Tuple[int, str]] = args.chara_mapping
    for slot, _ in chara_mapping:
        if not (1 <= slot <= 20):
            p.error(f'Invalid character slot #{slot}')
    for slot, filename in chara_mapping:
        with open(filename, 'w') as f:
            json.dump(charas[slot-1], f)

def do_import_charas(sol: miniamf.sol.SOL, charas: CharaList, p: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    chara_mapping: List[Tuple[int, str]] = args.chara_mapping
    for slot, _ in chara_mapping:
        if not (1 <= slot <= 20):
            p.error(f'Invalid character slot #{slot}')
    for slot, filename in chara_mapping:
        with open(filename, 'r') as f:
            chara = json.load(f)
        flatterned_chara = flattern_character(slot, chara)
        sol.update(flatterned_chara)

    _save_sol(sol, args.savefile, args.no_save_backup)

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
    except KeyError:
        if args.action in ('dump-all', 'update'):
            print(f'WARNING: {ERR_NO_CHARA_FIELD}')
        else:
            p.error(ERR_NO_CHARA_FIELD)
            raise

    action: DoCallback = ACTIONS[args.action]

    action(sol, charas, p, args)
