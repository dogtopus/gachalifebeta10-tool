import json
from typing import Optional

from .save import CharaDict
import pathlib
import miniamf.sol


GAME_NAMES = {
    'life': 'Gacha Life',
    'club': 'Gacha Club',
    'life2': 'Gacha Life 2',
}


def load_sol(savefile: str | pathlib.Path) -> miniamf.sol.SOL:
    sol_path = pathlib.Path(savefile)
    with sol_path.open('rb') as f:
        return miniamf.sol.load(f)


def save_sol(sol: miniamf.sol.SOL, savefile: str | pathlib.Path, skip_backup: bool) -> None:
    output = pathlib.Path(savefile)
    if not skip_backup:
        output.rename(output.with_suffix('.bak'))

    with output.open('wb') as solfile:
        sol.save(solfile, miniamf.AMF3)


def load_and_validate_chara_files(chara_mapping: list[tuple[int, str]],
                                  expected_type: Optional[str] = None) -> list[tuple[int, CharaDict]]:
    result = []
    for slot, chara_file in chara_mapping:
        with open(chara_file, 'r') as f:
            chara = json.load(f)
            if expected_type != chara['_type']:
                raise ValueError(f'{repr(chara_file)} is not a {GAME_NAMES.get(expected_type, expected_type)}'
                                 f'chara file.')
            result.append((slot, chara))
    return result
