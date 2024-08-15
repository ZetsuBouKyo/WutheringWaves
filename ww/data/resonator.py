from ww.locale import ZhTwEnum, _
from ww.model.resonator import ResonatorModel

SANHUA: str = "散華"
BAIZHI: str = "白芷"
LINGYANG: str = "凌陽"
ZHEZHI: str = "折枝"
CHIXIA: str = "熾霞"
ENCORE: str = "安可"
MORTEFI: str = "莫特斐"
CHANGLI: str = "長離"
CALCHARO: str = "卡卡羅"
YINLIN: str = "吟霖"
YUANWU: str = "淵武"
JINHSI: str = "今汐"
XIANGLIYAO: str = "相里要"
YANGYANG: str = "秧秧"
AALTO: str = "秋水"
JIYAN: str = "忌炎"
JIANXIN: str = "鑒心"
ROVER_SPECTRO_MALE: str = "漂泊者·衍射(男)"
ROVER_SPECTRO_FEMALE: str = "漂泊者·衍射(女)"
VERINA: str = "維里奈"
TAOQI: str = "桃祈"
DANJIN: str = "丹瑾"
ROVER_HAVOC_FEMALE: str = "漂泊者·湮滅(女)"
ROVER_HAVOC_MALE: str = "漂泊者·湮滅(男)"

resonators = {
    _(ZhTwEnum.SANHUA): ResonatorModel(
        name=_(ZhTwEnum.SANHUA), element=_(ZhTwEnum.GLACIO)
    ),
    _(ZhTwEnum.BAIZHI): ResonatorModel(
        name=_(ZhTwEnum.BAIZHI), element=_(ZhTwEnum.GLACIO)
    ),
    _(ZhTwEnum.LINGYANG): ResonatorModel(
        name=_(ZhTwEnum.LINGYANG), element=_(ZhTwEnum.GLACIO)
    ),
    _(ZhTwEnum.ZHEZHI): ResonatorModel(
        name=_(ZhTwEnum.ZHEZHI), element=_(ZhTwEnum.GLACIO)
    ),
    _(ZhTwEnum.CHIXIA): ResonatorModel(
        name=_(ZhTwEnum.CHIXIA), element=_(ZhTwEnum.FUSION)
    ),
    _(ZhTwEnum.ENCORE): ResonatorModel(
        name=_(ZhTwEnum.ENCORE), element=_(ZhTwEnum.FUSION)
    ),
    _(ZhTwEnum.MORTEFI): ResonatorModel(
        name=_(ZhTwEnum.MORTEFI), element=_(ZhTwEnum.FUSION)
    ),
    _(ZhTwEnum.CHANGLI): ResonatorModel(
        name=_(ZhTwEnum.CHANGLI), element=_(ZhTwEnum.FUSION)
    ),
    _(ZhTwEnum.CALCHARO): ResonatorModel(
        name=_(ZhTwEnum.CALCHARO), element=_(ZhTwEnum.ELECTRO)
    ),
    _(ZhTwEnum.YINLIN): ResonatorModel(
        name=_(ZhTwEnum.YINLIN), element=_(ZhTwEnum.ELECTRO)
    ),
    _(ZhTwEnum.YUANWU): ResonatorModel(
        name=_(ZhTwEnum.YUANWU), element=_(ZhTwEnum.ELECTRO)
    ),
    _(ZhTwEnum.JINHSI): ResonatorModel(
        name=_(ZhTwEnum.JINHSI), element=_(ZhTwEnum.SPECTRO)
    ),
    _(ZhTwEnum.XIANGLIYAO): ResonatorModel(
        name=_(ZhTwEnum.XIANGLIYAO), element=_(ZhTwEnum.ELECTRO)
    ),
    _(ZhTwEnum.YANGYANG): ResonatorModel(
        name=_(ZhTwEnum.YANGYANG), element=_(ZhTwEnum.AERO)
    ),
    _(ZhTwEnum.AALTO): ResonatorModel(name=_(ZhTwEnum.AALTO), element=_(ZhTwEnum.AERO)),
    _(ZhTwEnum.JIYAN): ResonatorModel(name=_(ZhTwEnum.JIYAN), element=_(ZhTwEnum.AERO)),
    _(ZhTwEnum.JIANXIN): ResonatorModel(
        name=_(ZhTwEnum.JIANXIN), element=_(ZhTwEnum.AERO)
    ),
    _(ZhTwEnum.ROVER_SPECTRO_MALE): ResonatorModel(
        name=_(ZhTwEnum.ROVER_SPECTRO_MALE), element=_(ZhTwEnum.SPECTRO)
    ),
    _(ZhTwEnum.ROVER_SPECTRO_FEMALE): ResonatorModel(
        name=_(ZhTwEnum.ROVER_SPECTRO_FEMALE), element=_(ZhTwEnum.SPECTRO)
    ),
    _(ZhTwEnum.VERINA): ResonatorModel(
        name=_(ZhTwEnum.VERINA), element=_(ZhTwEnum.SPECTRO)
    ),
    _(ZhTwEnum.TAOQI): ResonatorModel(
        name=_(ZhTwEnum.TAOQI), element=_(ZhTwEnum.HAVOC)
    ),
    _(ZhTwEnum.DANJIN): ResonatorModel(
        name=_(ZhTwEnum.DANJIN), element=_(ZhTwEnum.HAVOC)
    ),
    _(ZhTwEnum.ROVER_HAVOC_FEMALE): ResonatorModel(
        name=_(ZhTwEnum.ROVER_HAVOC_FEMALE), element=_(ZhTwEnum.HAVOC)
    ),
    _(ZhTwEnum.ROVER_HAVOC_MALE): ResonatorModel(
        name=_(ZhTwEnum.ROVER_HAVOC_MALE), element=_(ZhTwEnum.HAVOC)
    ),
}
