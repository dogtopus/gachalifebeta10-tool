from typing import (
    Callable,
    Final,
    Pattern,
    Match,
    Optional,
    cast,
)

import argparse
import json
import pprint
import re
import traceback

import miniamf.sol

from gachalifebeta10_tool.utils import load_and_validate_chara_files
from . import utils
from .save import *

SLOT_FILE_RE: Final[Pattern] = re.compile(r'^(\d+):(.+)$')

DoCallback = Callable[[miniamf.sol.SOL, CharaList, argparse.ArgumentParser, argparse.Namespace], None]


def slotfile(v: str) -> tuple[int, str]:
    m: Optional[Match] = SLOT_FILE_RE.match(v)
    if m is None:
        raise ValueError(f'Malformed string "{v}"')
    return int(m.group(1)), m.group(2)


def parse_args() -> tuple[argparse.ArgumentParser, argparse.Namespace]:
    p = argparse.ArgumentParser()
    p.add_argument('savefile', help='Save file.')
    p.add_argument('-B', '--no-save-backup', action='store_true', default=False,
                   help='Do not create backup for save file.')
    sps = p.add_subparsers(dest='action', metavar='action', help='Action.')

    sp = sps.add_parser('list-charas', help='List characters.')

    sp = sps.add_parser('import-charas', help='Import characters from JSON files.')
    sp.add_argument('chara_mapping', nargs='+', type=slotfile,
                    help='Slot mapped to character file (specified as <slot>:<file>).')

    sp = sps.add_parser('export-charas', help='Export characters as JSON files.')
    sp.add_argument('chara_mapping', nargs='+', type=slotfile,
                    help='Slot mapped to character file (specified as <slot>:<file>).')

    sp = sps.add_parser('dump-all', help='Pretty print all values in the save file. For testing only.')

    sp = sps.add_parser('update', help='Merge a JSON object into the save file, similar to Python\'s dict.update() '
                                       'method. For testing only and may break the save file if the JSON object '
                                       'contains bad values.')
    sp.add_argument('jsonobj', help='File containing the JSON object.')

    return p, p.parse_args()


def do_dump_all(sol: miniamf.sol.SOL,
                _charas: CharaList,
                _p: argparse.ArgumentParser,
                _args: argparse.Namespace) -> None:
    pprint.pprint(dict(sol))


def do_update(sol: miniamf.sol.SOL,
              _charas: CharaList,
              _p: argparse.ArgumentParser,
              args: argparse.Namespace) -> None:
    with open(args.jsonobj, 'r') as f:
        obj = json.load(f)

    sol.update(obj)

    utils.save_sol(sol, args.savefile, args.no_save_backup)


def do_list_charas(sol: miniamf.sol.SOL,
                   charas: CharaList,
                   p: argparse.ArgumentParser,
                   args: argparse.Namespace) -> None:
    for slot, chara in enumerate(charas):
        print(f'Slot #{slot+1}: {chara["namex"]}')


def do_export_charas(sol: miniamf.sol.SOL,
                     charas: CharaList,
                     p: argparse.ArgumentParser,
                     args: argparse.Namespace) -> None:
    save_format = detect_save_format(cast(Mapping, sol))
    max_slot_index = {'life': 20, 'club': 100, 'life2': 316}[save_format]
    chara_mapping: list[tuple[int, str]] = args.chara_mapping

    for slot, _ in chara_mapping:
        if not (1 <= slot <= max_slot_index):
            p.error(f'Invalid character slot #{slot}')
    for slot, filename in chara_mapping:
        with open(filename, 'w') as f:
            json.dump(charas[slot-1], f)


def do_import_charas(sol: miniamf.sol.SOL,
                     charas: CharaList,
                     p: argparse.ArgumentParser,
                     args: argparse.Namespace) -> None:
    save_obj = cast(MutableMapping, sol)
    save_format = detect_save_format(save_obj)
    chara_files: list[tuple[int, str]] = args.chara_mapping
    chara_mapping = load_and_validate_chara_files(chara_files, save_format)

    if save_format == 'life':
        import_charas_life(save_obj, chara_mapping)
    elif save_format == 'club':
        import_charas_club(save_obj, chara_mapping)
    elif save_format == 'life2':
        import_charas_life2(save_obj, chara_mapping)

    utils.save_sol(sol, args.savefile, args.no_save_backup)


ACTIONS: dict[str, DoCallback] = {
    'list-charas': do_list_charas,
    'export-charas': do_export_charas,
    'import-charas': do_import_charas,
    'dump-all': do_dump_all,
    'update': do_update,
}


def main():
    p, args = parse_args()

    with open(args.savefile, 'rb') as f:
        sol = miniamf.sol.load(f)

    charas: CharaList = []
    try:
        charas = extract_characters(sol)
    except CharacterExtractorError:
        if args.action in ('dump-all', 'update'):
            print(f'WARNING: {ERR_NO_CHARA_FIELD}')
            traceback.print_exc()
        else:
            print(f'ERROR: {ERR_NO_CHARA_FIELD}')
            traceback.print_exc()
            p.error(ERR_NO_CHARA_FIELD)
            raise

    action: DoCallback = ACTIONS[args.action]

    action(sol, charas, p, args)


if __name__ == '__main__':
    main()
