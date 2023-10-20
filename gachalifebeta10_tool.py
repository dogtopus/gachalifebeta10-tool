#!/usr/bin/env python3

from __future__ import annotations

from typing import (
    Callable,
    TypedDict,
    Final,
    Pattern,
    Match,
    Optional,
    Literal,
    Iterator,
    Sequence,
    cast,
)

import argparse
import json
import pprint
import os
import pprint
import re
import traceback

import miniamf.sol

SLOT_FILE_RE: Final[Pattern] = re.compile(r'^(\d+):(.+)$')

CHARA_FIELDS: Final[tuple[str, ...]] = (
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

CHARA_FIELDS_CLUB: Final[tuple[str, ...]] = (
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

CHARA_FIELDS_LIFE2 = (
    'namex', 'creatorx', 'birthdayx', 'agex', 'pronounsx', 'profilex', 'iconx',
    'fontx', 'heightxx', 'heightyx', 'headshapex', 'ear1x', 'ear1xpos',
    'ear1ypos', 'ear1rot', 'ear1xscale', 'ear1yscale', 'tintcharx', 'shadowx',
    'shadowxpos', 'shadowypos', 'shadowrot', 'shadowxscale', 'shadowyscale',
    'shadowalpha', 'blinkanix', 'fhairanix', 'bhairanix', 'capetailanix',
    'wingsanix', 'skindisplayx', 'facelayerx', 'handlayerx', 'feetlayerx',
    'coloralphax', 'linealphax', 'allalphax', 'poselayerx', 'posex', 'hand1x',
    'hand2x', 'hand1xpos', 'hand1ypos', 'hand1rot', 'hand1xscale',
    'hand1yscale', 'hand2xpos', 'hand2ypos', 'hand2rot', 'hand2xscale',
    'hand2yscale', 'arm1xpos', 'arm1ypos', 'arm1rot', 'arm1xscale',
    'arm1yscale', 'arm2xpos', 'arm2ypos', 'arm2rot', 'arm2xscale', 'arm2yscale',
    'shoulder1xpos', 'shoulder1ypos', 'shoulder1rot', 'shoulder1xscale',
    'shoulder1yscale', 'shoulder2xpos', 'shoulder2ypos', 'shoulder2rot',
    'shoulder2xscale', 'shoulder2yscale', 'thigh1xpos', 'thigh1ypos',
    'thigh1rot', 'thigh1xscale', 'thigh1yscale', 'thigh2xpos', 'thigh2ypos',
    'thigh2rot', 'thigh2xscale', 'thigh2yscale', 'foot1xpos', 'foot1ypos',
    'foot1rot', 'foot1xscale', 'foot1yscale', 'foot2xpos', 'foot2ypos',
    'foot2rot', 'foot2xscale', 'foot2yscale', 'headxpos', 'headypos', 'headrot',
    'headxscale', 'headyscale', 'bodyxpos', 'bodyypos', 'bodyrot', 'bodyxscale',
    'bodyyscale', 'rearhairx', 'fronthairx', 'sidehair1x', 'sidehair2x',
    'ahogex', 'backhairx', 'ponytail1x', 'ponytail2x', 'hairlight1x',
    'hairlight2x', 'rearhairxpos', 'rearhairypos', 'rearhairrot',
    'rearhairxscale', 'rearhairyscale', 'rearhairalpha', 'fronthairxpos',
    'fronthairypos', 'fronthairrot', 'fronthairxscale', 'fronthairyscale',
    'fronthairalpha', 'sidehair1xpos', 'sidehair1ypos', 'sidehair1rot',
    'sidehair1xscale', 'sidehair1yscale', 'sidehair1alpha', 'sidehair2xpos',
    'sidehair2ypos', 'sidehair2rot', 'sidehair2xscale', 'sidehair2yscale',
    'sidehair2alpha', 'ahogexpos', 'ahogeypos', 'ahogerot', 'ahogexscale',
    'ahogeyscale', 'ahogealpha', 'backhairxpos', 'backhairypos', 'backhairrot',
    'backhairxscale', 'backhairyscale', 'backhairalpha', 'ponytail1xpos',
    'ponytail1ypos', 'ponytail1rot', 'ponytail1xscale', 'ponytail1yscale',
    'ponytail1alpha', 'ponytail2xpos', 'ponytail2ypos', 'ponytail2rot',
    'ponytail2xscale', 'ponytail2yscale', 'ponytail2alpha', 'hairlight1xpos',
    'hairlight1ypos', 'hairlight1rot', 'hairlight1xscale', 'hairlight1yscale',
    'hairlight2xpos', 'hairlight2ypos', 'hairlight2rot', 'hairlight2xscale',
    'hairlight2yscale', 'eyeshape1x', 'eyeshape2x', 'eyeball1x', 'eyeball2x',
    'pupil1x', 'pupil2x', 'eyelight1x', 'eyelight2x', 'eyebrow1x', 'eyebrow2x',
    'mouthx', 'nosex', 'eyeshape1xpos', 'eyeshape1ypos', 'eyeshape1rot',
    'eyeshape1xscale', 'eyeshape1yscale', 'eyeshape1alpha', 'eyeshape2xpos',
    'eyeshape2ypos', 'eyeshape2rot', 'eyeshape2xscale', 'eyeshape2yscale',
    'eyeshape2alpha', 'eyeball1xpos', 'eyeball1ypos', 'eyeball1rot',
    'eyeball1xscale', 'eyeball1yscale', 'eyeball1alpha', 'eyeball2xpos',
    'eyeball2ypos', 'eyeball2rot', 'eyeball2xscale', 'eyeball2yscale',
    'eyeball2alpha', 'pupil1xpos', 'pupil1ypos', 'pupil1rot', 'pupil1xscale',
    'pupil1yscale', 'pupil2xpos', 'pupil2ypos', 'pupil2rot', 'pupil2xscale',
    'pupil2yscale', 'eyelight1xpos', 'eyelight1ypos', 'eyelight1rot',
    'eyelight1xscale', 'eyelight1yscale', 'eyelight2xpos', 'eyelight2ypos',
    'eyelight2rot', 'eyelight2xscale', 'eyelight2yscale', 'eyebrow1xpos',
    'eyebrow1ypos', 'eyebrow1rot', 'eyebrow1xscale', 'eyebrow1yscale',
    'eyebrow2xpos', 'eyebrow2ypos', 'eyebrow2rot', 'eyebrow2xscale',
    'eyebrow2yscale', 'mouthxpos', 'mouthypos', 'mouthrot', 'mouthxscale',
    'mouthyscale', 'mouthalpha', 'nosexpos', 'noseypos', 'noserot',
    'nosexscale', 'noseyscale', 'hat1x', 'hat2x', 'other1x', 'other2x',
    'other3x', 'other4x', 'glasses1x', 'glasses2x', 'faceacc1x', 'faceacc2x',
    'scarf1x', 'scarf2x', 'hat1xpos', 'hat1ypos', 'hat1rot', 'hat1xscale',
    'hat1yscale', 'hat1alpha', 'hat2xpos', 'hat2ypos', 'hat2rot', 'hat2xscale',
    'hat2yscale', 'hat2alpha', 'other1xpos', 'other1ypos', 'other1rot',
    'other1xscale', 'other1yscale', 'other1alpha', 'other2xpos', 'other2ypos',
    'other2rot', 'other2xscale', 'other2yscale', 'other2alpha', 'other3xpos',
    'other3ypos', 'other3rot', 'other3xscale', 'other3yscale', 'other3alpha',
    'other4xpos', 'other4ypos', 'other4rot', 'other4xscale', 'other4yscale',
    'other4alpha', 'glasses1xpos', 'glasses1ypos', 'glasses1rot',
    'glasses1xscale', 'glasses1yscale', 'glasses1alpha', 'glasses2xpos',
    'glasses2ypos', 'glasses2rot', 'glasses2xscale', 'glasses2yscale',
    'glasses2alpha', 'faceacc1xpos', 'faceacc1ypos', 'faceacc1rot',
    'faceacc1xscale', 'faceacc1yscale', 'faceacc1alpha', 'faceacc2xpos',
    'faceacc2ypos', 'faceacc2rot', 'faceacc2xscale', 'faceacc2yscale',
    'faceacc2alpha', 'scarf1xpos', 'scarf1ypos', 'scarf1rot', 'scarf1xscale',
    'scarf1yscale', 'scarf1alpha', 'scarf2xpos', 'scarf2ypos', 'scarf2rot',
    'scarf2xscale', 'scarf2yscale', 'scarf2alpha', 'shirtx', 'shirtlengthx',
    'jacketx', 'jacketlengthx', 'sleeve1x', 'sleeve2x', 'glove1x', 'glove2x',
    'wrist1x', 'wrist2x', 'shoulderacc1x', 'shoulderacc2x', 'shirtalpha',
    'jacketalpha', 'shirtlengthxpos', 'shirtlengthypos', 'shirtlengthrot',
    'shirtlengthxscale', 'shirtlengthyscale', 'shirtlengthalpha',
    'jacketlengthxpos', 'jacketlengthypos', 'jacketlengthrot',
    'jacketlengthxscale', 'jacketlengthyscale', 'jacketlengthalpha',
    'sleeve1alpha', 'sleeve2alpha', 'glove1alpha', 'glove2alpha', 'wrist1xpos',
    'wrist1ypos', 'wrist1rot', 'wrist1xscale', 'wrist1yscale', 'wrist1alpha',
    'wrist2xpos', 'wrist2ypos', 'wrist2rot', 'wrist2xscale', 'wrist2yscale',
    'wrist2alpha', 'shoulderacc1xpos', 'shoulderacc1ypos', 'shoulderacc1rot',
    'shoulderacc1xscale', 'shoulderacc1yscale', 'shoulderacc1alpha',
    'shoulderacc2xpos', 'shoulderacc2ypos', 'shoulderacc2rot',
    'shoulderacc2xscale', 'shoulderacc2yscale', 'shoulderacc2alpha', 'pants1x',
    'pants2x', 'sock1x', 'sock2x', 'shoe1x', 'shoe2x', 'belt1x', 'belt2x',
    'thighacc1x', 'thighacc2x', 'footacc1x', 'footacc2x', 'pants1alpha',
    'pants2alpha', 'sock1alpha', 'sock2alpha', 'shoe1xpos', 'shoe1ypos',
    'shoe1rot', 'shoe1xscale', 'shoe1yscale', 'shoe1alpha', 'shoe2xpos',
    'shoe2ypos', 'shoe2rot', 'shoe2xscale', 'shoe2yscale', 'shoe2alpha',
    'belt1xpos', 'belt1ypos', 'belt1rot', 'belt1xscale', 'belt1yscale',
    'belt1alpha', 'belt2xpos', 'belt2ypos', 'belt2rot', 'belt2xscale',
    'belt2yscale', 'belt2alpha', 'thighacc1xpos', 'thighacc1ypos',
    'thighacc1rot', 'thighacc1xscale', 'thighacc1yscale', 'thighacc1alpha',
    'thighacc2xpos', 'thighacc2ypos', 'thighacc2rot', 'thighacc2xscale',
    'thighacc2yscale', 'thighacc2alpha', 'footacc1xpos', 'footacc1ypos',
    'footacc1rot', 'footacc1xscale', 'footacc1yscale', 'footacc1alpha',
    'footacc2xpos', 'footacc2ypos', 'footacc2rot', 'footacc2xscale',
    'footacc2yscale', 'footacc2alpha', 'prop1x', 'prop2x', 'cape1x', 'cape2x',
    'tail1x', 'tail2x', 'wing1x', 'wing2x', 'wing3x', 'wing4x', 'shirtlogox',
    'hatlogox', 'prop1xpos', 'prop1ypos', 'prop1rot', 'prop1xscale',
    'prop1yscale', 'prop1alpha', 'prop2xpos', 'prop2ypos', 'prop2rot',
    'prop2xscale', 'prop2yscale', 'prop2alpha', 'cape1xpos', 'cape1ypos',
    'cape1rot', 'cape1xscale', 'cape1yscale', 'cape1alpha', 'cape2xpos',
    'cape2ypos', 'cape2rot', 'cape2xscale', 'cape2yscale', 'cape2alpha',
    'tail1xpos', 'tail1ypos', 'tail1rot', 'tail1xscale', 'tail1yscale',
    'tail1alpha', 'tail2xpos', 'tail2ypos', 'tail2rot', 'tail2xscale',
    'tail2yscale', 'tail2alpha', 'wing1xpos', 'wing1ypos', 'wing1rot',
    'wing1xscale', 'wing1yscale', 'wing1alpha', 'wing2xpos', 'wing2ypos',
    'wing2rot', 'wing2xscale', 'wing2yscale', 'wing2alpha', 'wing3xpos',
    'wing3ypos', 'wing3rot', 'wing3xscale', 'wing3yscale', 'wing3alpha',
    'wing4xpos', 'wing4ypos', 'wing4rot', 'wing4xscale', 'wing4yscale',
    'wing4alpha', 'shirtlogoxpos', 'shirtlogoypos', 'shirtlogorot',
    'shirtlogoxscale', 'shirtlogoyscale', 'shirtlogoalpha', 'hatlogoxpos',
    'hatlogoypos', 'hatlogorot', 'hatlogoxscale', 'hatlogoyscale',
    'hatlogoalpha', 'faceacc3x', 'faceacc4x', 'fx1x', 'fx2x', 'fx3x', 'fx4x',
    'faceacc3xpos', 'faceacc3ypos', 'faceacc3rot', 'faceacc3xscale',
    'faceacc3yscale', 'faceacc3alpha', 'faceacc4xpos', 'faceacc4ypos',
    'faceacc4rot', 'faceacc4xscale', 'faceacc4yscale', 'faceacc4alpha',
    'fx1xpos', 'fx1ypos', 'fx1rot', 'fx1xscale', 'fx1yscale', 'fx1alpha',
    'fx2xpos', 'fx2ypos', 'fx2rot', 'fx2xscale', 'fx2yscale', 'fx2alpha',
    'fx3xpos', 'fx3ypos', 'fx3rot', 'fx3xscale', 'fx3yscale', 'fx3alpha',
    'fx4xpos', 'fx4ypos', 'fx4rot', 'fx4xscale', 'fx4yscale', 'fx4alpha',
    'shadowskewx', 'shadowskewy', 'ear1skewx', 'ear1skewy', 'shoulderacc1skewx',
    'shoulderacc1skewy', 'shoulderacc2skewx', 'shoulderacc2skewy', 'arm1skewx',
    'arm1skewy', 'arm2skewx', 'arm2skewy', 'shoulder1skewx', 'shoulder1skewy',
    'shoulder2skewx', 'shoulder2skewy', 'thigh1skewx', 'thigh1skewy',
    'thigh2skewx', 'thigh2skewy', 'foot1skewx', 'foot1skewy', 'foot2skewx',
    'foot2skewy', 'headskewx', 'headskewy', 'bodyskewx', 'bodyskewy',
    'rearhairskewx', 'rearhairskewy', 'fronthairskewx', 'fronthairskewy',
    'sidehair1skewx', 'sidehair1skewy', 'sidehair2skewx', 'sidehair2skewy',
    'ahogeskewx', 'ahogeskewy', 'backhairskewx', 'backhairskewy',
    'ponytail1skewx', 'ponytail1skewy', 'ponytail2skewx', 'ponytail2skewy',
    'hairlight1skewx', 'hairlight1skewy', 'hairlight2skewx', 'hairlight2skewy',
    'eyeshape1skewx', 'eyeshape1skewy', 'eyeshape2skewx', 'eyeshape2skewy',
    'eyeball1skewx', 'eyeball1skewy', 'eyeball2skewx', 'eyeball2skewy',
    'pupil1skewx', 'pupil1skewy', 'pupil2skewx', 'pupil2skewy',
    'eyelight1skewx', 'eyelight1skewy', 'eyelight2skewx', 'eyelight2skewy',
    'eyebrow1skewx', 'eyebrow1skewy', 'eyebrow2skewx', 'eyebrow2skewy',
    'mouthskewx', 'mouthskewy', 'noseskewx', 'noseskewy', 'hat1skewx',
    'hat1skewy', 'hat2skewx', 'hat2skewy', 'other1skewx', 'other1skewy',
    'other2skewx', 'other2skewy', 'other3skewx', 'other3skewy', 'other4skewx',
    'other4skewy', 'glasses1skewx', 'glasses1skewy', 'glasses2skewx',
    'glasses2skewy', 'faceacc1skewx', 'faceacc1skewy', 'faceacc2skewx',
    'faceacc2skewy', 'scarf1skewx', 'scarf1skewy', 'scarf2skewx', 'scarf2skewy',
    'shirtlengthskewx', 'shirtlengthskewy', 'jacketlengthskewx',
    'jacketlengthskewy', 'wrist1skewx', 'wrist1skewy', 'wrist2skewx',
    'wrist2skewy', 'shoe1skewx', 'shoe1skewy', 'shoe2skewx', 'shoe2skewy',
    'belt1skewx', 'belt1skewy', 'belt2skewx', 'belt2skewy', 'thighacc1skewx',
    'thighacc1skewy', 'thighacc2skewx', 'thighacc2skewy', 'footacc1skewx',
    'footacc1skewy', 'footacc2skewx', 'footacc2skewy', 'prop1skewx',
    'prop1skewy', 'prop2skewx', 'prop2skewy', 'cape1skewx', 'cape1skewy',
    'cape2skewx', 'cape2skewy', 'tail1skewx', 'tail1skewy', 'tail2skewx',
    'tail2skewy', 'wing1skewx', 'wing1skewy', 'wing2skewx', 'wing2skewy',
    'wing3skewx', 'wing3skewy', 'wing4skewx', 'wing4skewy', 'shirtlogoskewx',
    'shirtlogoskewy', 'hatlogoskewx', 'hatlogoskewy', 'faceacc3skewx',
    'faceacc3skewy', 'faceacc4skewx', 'faceacc4skewy', 'fx1skewx', 'fx1skewy',
    'fx2skewx', 'fx2skewy', 'fx3skewx', 'fx3skewy', 'fx4skewx', 'fx4skewy',
    'skincolx1', 'skincolx2', 'skincolx3', 'shadowcolx', 'tintcolx',
    'rearhaircolx1', 'rearhaircolx2', 'rearhaircolx3', 'rearhaircolx4',
    'fronthaircolx1', 'fronthaircolx2', 'fronthaircolx3', 'fronthaircolx4',
    'sidehair1colx1', 'sidehair1colx2', 'sidehair1colx3', 'sidehair1colx4',
    'sidehair2colx1', 'sidehair2colx2', 'sidehair2colx3', 'sidehair2colx4',
    'ahogecolx1', 'ahogecolx2', 'ahogecolx3', 'ahogecolx4', 'backhaircolx1',
    'backhaircolx2', 'backhaircolx3', 'backhaircolx4', 'ponytail1colx1',
    'ponytail1colx2', 'ponytail1colx3', 'ponytail1colx4', 'ponytail2colx1',
    'ponytail2colx2', 'ponytail2colx3', 'ponytail2colx4', 'hairlightcolx1',
    'hairlightcolx2', 'hairacccolx1', 'hairacccolx2', 'hairacccolx3',
    'hairacccolx4', 'hairacccolx5', 'eyeshape1colx1', 'eyeshape1colx2',
    'eyeshape1colx3', 'eyeshape1colx4', 'eyeshape2colx1', 'eyeshape2colx2',
    'eyeshape2colx3', 'eyeshape2colx4', 'eyeball1colx1', 'eyeball1colx2',
    'eyeball1colx3', 'eyeball1colx4', 'eyeball2colx1', 'eyeball2colx2',
    'eyeball2colx3', 'eyeball2colx4', 'pupil1colx1', 'pupil1colx2',
    'pupil2colx1', 'pupil2colx2', 'eyelightcolx1', 'eyelightcolx2',
    'eyebrow1colx1', 'eyebrow1colx2', 'eyebrow2colx1', 'eyebrow2colx2',
    'nosecolx1', 'nosecolx2', 'mouthcolx1', 'mouthcolx2', 'mouthcolx3',
    'mouthcolx4', 'hat1colx1', 'hat1colx2', 'hat1colx3', 'hat1colx4',
    'hat2colx1', 'hat2colx2', 'hat2colx3', 'hat2colx4', 'other1colx1',
    'other1colx2', 'other1colx3', 'other1colx4', 'other2colx1', 'other2colx2',
    'other2colx3', 'other2colx4', 'other3colx1', 'other3colx2', 'other3colx3',
    'other3colx4', 'other4colx1', 'other4colx2', 'other4colx3', 'other4colx4',
    'glasses1colx1', 'glasses1colx2', 'glasses1colx3', 'glasses1colx4',
    'glasses2colx1', 'glasses2colx2', 'glasses2colx3', 'glasses2colx4',
    'faceacc1colx1', 'faceacc1colx2', 'faceacc1colx3', 'faceacc1colx4',
    'faceacc2colx1', 'faceacc2colx2', 'faceacc2colx3', 'faceacc2colx4',
    'scarf1colx1', 'scarf1colx2', 'scarf1colx3', 'scarf1colx4', 'scarf2colx1',
    'scarf2colx2', 'scarf2colx3', 'scarf2colx4', 'shirtcolx1', 'shirtcolx2',
    'shirtcolx3', 'shirtcolx4', 'shirtlengthcolx1', 'shirtlengthcolx2',
    'shirtlengthcolx3', 'shirtlengthcolx4', 'jacketcolx1', 'jacketcolx2',
    'jacketcolx3', 'jacketcolx4', 'jacketlengthcolx1', 'jacketlengthcolx2',
    'jacketlengthcolx3', 'jacketlengthcolx4', 'sleeve1colx1', 'sleeve1colx2',
    'sleeve1colx3', 'sleeve1colx4', 'sleeve2colx1', 'sleeve2colx2',
    'sleeve2colx3', 'sleeve2colx4', 'glove1colx1', 'glove1colx2', 'glove1colx3',
    'glove1colx4', 'glove2colx1', 'glove2colx2', 'glove2colx3', 'glove2colx4',
    'wrist1colx1', 'wrist1colx2', 'wrist1colx3', 'wrist1colx4', 'wrist2colx1',
    'wrist2colx2', 'wrist2colx3', 'wrist2colx4', 'shoulderacc1colx1',
    'shoulderacc1colx2', 'shoulderacc1colx3', 'shoulderacc1colx4',
    'shoulderacc2colx1', 'shoulderacc2colx2', 'shoulderacc2colx3',
    'shoulderacc2colx4', 'pants1colx1', 'pants1colx2', 'pants1colx3',
    'pants1colx4', 'pants2colx1', 'pants2colx2', 'pants2colx3', 'pants2colx4',
    'sock1colx1', 'sock1colx2', 'sock1colx3', 'sock1colx4', 'sock2colx1',
    'sock2colx2', 'sock2colx3', 'sock2colx4', 'shoe1colx1', 'shoe1colx2',
    'shoe1colx3', 'shoe1colx4', 'shoe2colx1', 'shoe2colx2', 'shoe2colx3',
    'shoe2colx4', 'belt1colx1', 'belt1colx2', 'belt1colx3', 'belt1colx4',
    'belt2colx1', 'belt2colx2', 'belt2colx3', 'belt2colx4', 'thighacc1colx1',
    'thighacc1colx2', 'thighacc1colx3', 'thighacc1colx4', 'thighacc2colx1',
    'thighacc2colx2', 'thighacc2colx3', 'thighacc2colx4', 'footacc1colx1',
    'footacc1colx2', 'footacc1colx3', 'footacc1colx4', 'footacc2colx1',
    'footacc2colx2', 'footacc2colx3', 'footacc2colx4', 'prop1colx1',
    'prop1colx2', 'prop1colx3', 'prop1colx4', 'prop2colx1', 'prop2colx2',
    'prop2colx3', 'prop2colx4', 'cape1colx1', 'cape1colx2', 'cape1colx3',
    'cape1colx4', 'cape2colx1', 'cape2colx2', 'cape2colx3', 'cape2colx4',
    'tail1colx1', 'tail1colx2', 'tail1colx3', 'tail1colx4', 'tail2colx1',
    'tail2colx2', 'tail2colx3', 'tail2colx4', 'wing1colx1', 'wing1colx2',
    'wing1colx3', 'wing1colx4', 'wing2colx1', 'wing2colx2', 'wing2colx3',
    'wing2colx4', 'wing3colx1', 'wing3colx2', 'wing3colx3', 'wing3colx4',
    'wing4colx1', 'wing4colx2', 'wing4colx3', 'wing4colx4', 'shirtlogocolx1',
    'hatlogocolx1', 'faceacc3colx1', 'faceacc3colx2', 'faceacc3colx3',
    'faceacc3colx4', 'faceacc4colx1', 'faceacc4colx2', 'faceacc4colx3',
    'faceacc4colx4', 'fx1colx1', 'fx1colx2', 'fx1colx3', 'fx1colx4', 'fx2colx1',
    'fx2colx2', 'fx2colx3', 'fx2colx4', 'fx3colx1', 'fx3colx2', 'fx3colx3',
    'fx3colx4', 'fx4colx1', 'fx4colx2', 'fx4colx3', 'fx4colx4', 'hairacccolx6',
    'hairacccolx7', 'hairacccolx8', 'ear2x', 'ear2xpos', 'ear2ypos', 'ear2rot',
    'ear2xscale', 'ear2yscale', 'ear2skewx', 'ear2skewy', 'ear1alpha',
    'ear2alpha', 'ear1colx1', 'ear1colx2', 'ear1colx3', 'ear1colx4',
    'ear2colx1', 'ear2colx2', 'ear2colx3', 'ear2colx4',
)

COLOR_FIELDS_CLUB = set(CHARA_FIELDS_CLUB[CHARA_FIELDS_CLUB.index('skincolor1x'):])
COLOR_FIELDS_LIFE2 = set(field for field in CHARA_FIELDS_LIFE2 if field.find('colx') > 0)

CHARSTRING_JOINER_1D = '|'
CHARSTRING_JOINER_2D = '¦'

ERR_NO_CHARA_FIELD = 'Unable to find character fields. Is this a Gacha Life save?'

class CharacterExtractorError(ValueError):
    pass

CharaDict = dict[str, int | str]
FlatternedCharaDict = dict[str, int | str]
CharaList = list[CharaDict]
DoCallback = Callable[[miniamf.sol.SOL, CharaList, argparse.ArgumentParser, argparse.Namespace], None]

def slotfile(v: str) -> tuple[int, str]:
    m: Optional[Match] = SLOT_FILE_RE.match(v)
    if m is None:
        raise ValueError(f'Malformed string "{v}"')
    return int(m.group(1)), m.group(2)

def parse_args() -> tuple[argparse.ArgumentParser, argparse.Namespace]:
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

def charstring_to_dict(all_fields: Sequence[str], color_fields: set[str], charstring: str, expand_color: bool = False) -> CharaDict:
    charstring_splitted = charstring.split(CHARSTRING_JOINER_1D)
    assert len(charstring_splitted) == len(all_fields), 'Malformed charstring.'
    obj: CharaDict = {}
    for key, val in zip(all_fields, charstring_splitted):
        if expand_color and key in color_fields:
            obj[key] = f'0x{val}'
        else:
            obj[key] = val
    return obj

def iterate_club_extraslot(sol: miniamf.sol.SOL) -> Iterator[CharaDict]:
    slots = sol['extraslotstring'].split(CHARSTRING_JOINER_2D)
    if len(slots) != 90:
        raise ValueError('Uncompacted extraslotstring must contain exactly 90 items.')
    for charstring in slots:
        obj = charstring_to_dict(CHARA_FIELDS_CLUB, COLOR_FIELDS_CLUB, charstring, True)
        yield obj

def iterate_life2_slot_single(slot_data: str, size: int) -> Iterator[CharaDict]:
    slots = slot_data.split(CHARSTRING_JOINER_2D)
    if len(slots) != size:
        raise ValueError(f'Uncompacted datachar must contain exactly {len(slots)} items.')
    for charstring in slots:
        obj = charstring_to_dict(CHARA_FIELDS_LIFE2, COLOR_FIELDS_LIFE2, charstring, True)
        yield obj

def iterate_life2_slot(sol: miniamf.sol.SOL) -> Iterator[CharaDict]:
    for index in range(1, 3):
        yield from iterate_life2_slot_single(sol[f'datachar{index}'], 8)
    for index in range(1, 31):
        yield from iterate_life2_slot_single(sol[f'dataslot{index}'], 10)

def clubplus_chara_list_to_extraslotstring(all_fields: Sequence[str],
                                           color_fields: set[str],
                                           chara_list: CharaList) -> str:
    return CHARSTRING_JOINER_2D.join(
        clubplus_chara_dict_to_charstring(all_fields, color_fields, chara, compact_color=True)
        for chara in chara_list
    )

def clubplus_chara_dict_to_charstring(all_fields: Sequence[str],
                                      color_fields: set[str],
                                      obj: CharaDict,
                                      compact_color: bool = False) -> str:
    def _compact_color_fields(obj: CharaDict, compact_color: bool):
        for key in all_fields:
            if compact_color and key in color_fields and isinstance(obj[key], str) and cast(str, obj[key]).startswith('0x'):
                yield cast(str, obj[key])[2:]
            else:
                yield str(obj[key])
    charstring = CHARSTRING_JOINER_1D.join(_compact_color_fields(obj, compact_color))
    return charstring

def detect_save_format(sol: miniamf.sol.SOL) -> Literal['club', 'life', 'life2', 'unknown']:
    if 'accessory1' in sol:
        return 'life'
    elif 'charstring1' in sol:
        return 'club'
    elif 'datachar1' in sol:
        return 'life2'
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
            obj = charstring_to_dict(CHARA_FIELDS_CLUB, COLOR_FIELDS_CLUB, sol[f'charstring{active_chara_index}'])
            obj['_type'] = 'club'
            yield obj
        for obj in iterate_club_extraslot(sol):
            obj['_type'] = 'club'
            yield obj

    def _iterator_life2(sol: miniamf.sol.SOL) -> Iterator[CharaDict]:
        for obj in iterate_life2_slot(sol):
            obj['_type'] = 'life2'
            yield obj

    save_format = detect_save_format(sol)

    try:
        if save_format == 'life':
            print('Detected Gacha Life save data.')
            return list(_iterator_life(sol))
        elif save_format == 'club':
            print('Detected Gacha Club save data.')
            return list(_iterator_club(sol))
        elif save_format == 'life2':
            print('Detected Gacha Life 2 save data.')
            return list(_iterator_life2(sol))
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
    max_slot_index = {'life': 20, 'club': 100, 'life2': 316}[save_format]
    chara_mapping: list[tuple[int, str]] = args.chara_mapping

    for slot, _ in chara_mapping:
        if not (1 <= slot <= max_slot_index):
            p.error(f'Invalid character slot #{slot}')
    for slot, filename in chara_mapping:
        with open(filename, 'w') as f:
            json.dump(charas[slot-1], f)

def do_import_charas(sol: miniamf.sol.SOL, charas: CharaList, p: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    save_format = detect_save_format(sol)
    chara_mapping: list[tuple[int, str]] = args.chara_mapping

    if save_format == 'life':
        import_charas_life(sol, charas, p, chara_mapping)
    elif save_format == 'club':
        import_charas_club(sol, charas, p, chara_mapping)
    elif save_format == 'life2':
        import_charas_life2(sol, charas, p, chara_mapping)

    _save_sol(sol, args.savefile, args.no_save_backup)

def import_charas_life(sol: miniamf.sol.SOL, charas: CharaList, p: argparse.ArgumentParser, chara_mapping: list[tuple[int, str]]) -> None:
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

def import_charas_club(sol: miniamf.sol.SOL, charas: CharaList, p: argparse.ArgumentParser, chara_mapping: list[tuple[int, str]]) -> None:
    extra_updated = False
    extra_slots: CharaList = list(iterate_club_extraslot(sol))
    extra_names: list[str] = sol['extranamestring'].split(CHARSTRING_JOINER_1D)

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
            charstring = clubplus_chara_dict_to_charstring(CHARA_FIELDS_CLUB, COLOR_FIELDS_CLUB, chara)
            sol[f'charstring{slot}'] = charstring
        else:
            extra_updated = True
            # slot #11 is array index 0
            slot -= 11
            extra_slots[slot] = chara
            extra_names[slot] = chara['namex']
    if extra_updated:
        sol['extranamestring'] = CHARSTRING_JOINER_1D.join(extra_names)
        sol['extraslotstring'] = clubplus_chara_list_to_extraslotstring(CHARA_FIELDS_CLUB, COLOR_FIELDS_CLUB, extra_slots)

def import_charas_life2(sol: miniamf.sol.SOL, charas: CharaList, p: argparse.ArgumentParser, chara_mapping: list[tuple[int, str]]) -> None:
    updated = {}

    for slot, _ in chara_mapping:
        if not (1 <= slot <= 316):
            p.error(f'Invalid character slot #{slot}')
    for slot_global, filename in chara_mapping:
        with open(filename, 'r') as f:
            chara = json.load(f)
        if chara.get('_type', 'life') != 'life2':
            p.error(f"'{filename}' is not a Gacha Life 2 chara file.")
        for key, val in chara.items():
            if isinstance(val, str) and (CHARSTRING_JOINER_1D in val or CHARSTRING_JOINER_2D in val):
                print("WARNING: Replacing array delimiter in file '{filename}', field '{key}' with '_'.")
                chara[key] = val.replace(CHARSTRING_JOINER_1D, '_').replace(CHARSTRING_JOINER_2D, '_')
        if '_type' in chara:
            del chara['_type']
        if slot_global <= 16:
            datachar_index, slot_index = divmod(slot_global - 1, 8)
            key = f'datachar{datachar_index+1}'
            expected_size = 8
        else:
            dataslot_index, slot_index = divmod(slot_global - 17, 10)
            key = f'dataslot{dataslot_index+1}'
            expected_size = 10

        if key not in updated:
            updated[key] = list(iterate_life2_slot_single(sol[key], expected_size))
        updated[key][slot_index] = chara

    for key, slots in updated.items():
        sol[key] = clubplus_chara_list_to_extraslotstring(CHARA_FIELDS_LIFE2, COLOR_FIELDS_LIFE2, slots)

def do_dump_all(sol: miniamf.sol.SOL, _charas: CharaList, _p: argparse.ArgumentParser, _args: argparse.Namespace) -> None:
    pprint.pprint(dict(sol))

def do_update(sol: miniamf.sol.SOL, _charas: CharaList, _p: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    with open(args.jsonobj, 'r') as f:
        obj = json.load(f)

    sol.update(obj)

    _save_sol(sol, args.savefile, args.no_save_backup)

ACTIONS: dict[str, DoCallback] = {
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
            traceback.print_exc()
        else:
            print(f'ERROR: {ERR_NO_CHARA_FIELD}')
            traceback.print_exc()
            p.error(ERR_NO_CHARA_FIELD)
            raise

    action: DoCallback = ACTIONS[args.action]

    action(sol, charas, p, args)
