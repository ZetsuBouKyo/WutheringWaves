from enum import Enum


class TemplateResonatorTableColumnEnum(str, Enum):
    RESONATOR_NAME: str = "[角色]名稱"
    RESONATOR_CHAIN: str = "[角色]共鳴鏈"
    RESONATOR_WEAPON_NAME: str = "[武器]名稱"
    RESONATOR_WEAPON_RANK: str = "[武器]諧振"
    RESONATOR_INHERENT_SKILL_1: bool = "[角色]固有技能1"
    RESONATOR_INHERENT_SKILL_2: bool = "[角色]固有技能2"
    RESONATOR_ECHO_1: str = "[聲骸]名稱"
    RESONATOR_ECHO_SONATA_1: str = "[聲骸]合鳴1"
    RESONATOR_ECHO_SONATA_2: str = "[聲骸]合鳴2"
    RESONATOR_ECHO_SONATA_3: str = "[聲骸]合鳴3"
    RESONATOR_ECHO_SONATA_4: str = "[聲骸]合鳴4"
    RESONATOR_ECHO_SONATA_5: str = "[聲骸]合鳴5"
