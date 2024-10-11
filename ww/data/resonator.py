from ww.locale import ZhTwEnum, _
from ww.model.resonator import BaseResonatorModel

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
SHOREKEEPER: str = "守岸人"
TAOQI: str = "桃祈"
DANJIN: str = "丹瑾"
ROVER_HAVOC_FEMALE: str = "漂泊者·湮滅(女)"
ROVER_HAVOC_MALE: str = "漂泊者·湮滅(男)"

resonators = {
    _(ZhTwEnum.SANHUA): BaseResonatorModel(
        name=_(ZhTwEnum.SANHUA), element=_(ZhTwEnum.GLACIO)
    ),
    _(ZhTwEnum.BAIZHI): BaseResonatorModel(
        name=_(ZhTwEnum.BAIZHI), element=_(ZhTwEnum.GLACIO)
    ),
    _(ZhTwEnum.LINGYANG): BaseResonatorModel(
        name=_(ZhTwEnum.LINGYANG), element=_(ZhTwEnum.GLACIO)
    ),
    _(ZhTwEnum.ZHEZHI): BaseResonatorModel(
        name=_(ZhTwEnum.ZHEZHI), element=_(ZhTwEnum.GLACIO)
    ),
    _(ZhTwEnum.YOUHU): BaseResonatorModel(
        name=_(ZhTwEnum.YOUHU), element=_(ZhTwEnum.GLACIO)
    ),
    _(ZhTwEnum.CHIXIA): BaseResonatorModel(
        name=_(ZhTwEnum.CHIXIA), element=_(ZhTwEnum.FUSION)
    ),
    _(ZhTwEnum.ENCORE): BaseResonatorModel(
        name=_(ZhTwEnum.ENCORE), element=_(ZhTwEnum.FUSION)
    ),
    _(ZhTwEnum.MORTEFI): BaseResonatorModel(
        name=_(ZhTwEnum.MORTEFI), element=_(ZhTwEnum.FUSION)
    ),
    _(ZhTwEnum.CHANGLI): BaseResonatorModel(
        name=_(ZhTwEnum.CHANGLI), element=_(ZhTwEnum.FUSION)
    ),
    _(ZhTwEnum.CALCHARO): BaseResonatorModel(
        name=_(ZhTwEnum.CALCHARO), element=_(ZhTwEnum.ELECTRO)
    ),
    _(ZhTwEnum.YINLIN): BaseResonatorModel(
        name=_(ZhTwEnum.YINLIN), element=_(ZhTwEnum.ELECTRO)
    ),
    _(ZhTwEnum.YUANWU): BaseResonatorModel(
        name=_(ZhTwEnum.YUANWU), element=_(ZhTwEnum.ELECTRO)
    ),
    _(ZhTwEnum.JINHSI): BaseResonatorModel(
        name=_(ZhTwEnum.JINHSI), element=_(ZhTwEnum.SPECTRO)
    ),
    _(ZhTwEnum.XIANGLIYAO): BaseResonatorModel(
        name=_(ZhTwEnum.XIANGLIYAO), element=_(ZhTwEnum.ELECTRO)
    ),
    _(ZhTwEnum.YANGYANG): BaseResonatorModel(
        name=_(ZhTwEnum.YANGYANG), element=_(ZhTwEnum.AERO)
    ),
    _(ZhTwEnum.AALTO): BaseResonatorModel(
        name=_(ZhTwEnum.AALTO), element=_(ZhTwEnum.AERO)
    ),
    _(ZhTwEnum.JIYAN): BaseResonatorModel(
        name=_(ZhTwEnum.JIYAN), element=_(ZhTwEnum.AERO)
    ),
    _(ZhTwEnum.JIANXIN): BaseResonatorModel(
        name=_(ZhTwEnum.JIANXIN), element=_(ZhTwEnum.AERO)
    ),
    _(ZhTwEnum.ROVER_SPECTRO_MALE): BaseResonatorModel(
        name=_(ZhTwEnum.ROVER_SPECTRO_MALE), element=_(ZhTwEnum.SPECTRO)
    ),
    _(ZhTwEnum.ROVER_SPECTRO_FEMALE): BaseResonatorModel(
        name=_(ZhTwEnum.ROVER_SPECTRO_FEMALE), element=_(ZhTwEnum.SPECTRO)
    ),
    _(ZhTwEnum.VERINA): BaseResonatorModel(
        name=_(ZhTwEnum.VERINA), element=_(ZhTwEnum.SPECTRO)
    ),
    _(ZhTwEnum.SHOREKEEPER): BaseResonatorModel(
        name=_(ZhTwEnum.SHOREKEEPER), element=_(ZhTwEnum.SPECTRO)
    ),
    _(ZhTwEnum.TAOQI): BaseResonatorModel(
        name=_(ZhTwEnum.TAOQI), element=_(ZhTwEnum.HAVOC)
    ),
    _(ZhTwEnum.DANJIN): BaseResonatorModel(
        name=_(ZhTwEnum.DANJIN), element=_(ZhTwEnum.HAVOC)
    ),
    _(ZhTwEnum.CAMELLYA): BaseResonatorModel(
        name=_(ZhTwEnum.CAMELLYA), element=_(ZhTwEnum.HAVOC)
    ),
    _(ZhTwEnum.ROVER_HAVOC_FEMALE): BaseResonatorModel(
        name=_(ZhTwEnum.ROVER_HAVOC_FEMALE), element=_(ZhTwEnum.HAVOC)
    ),
    _(ZhTwEnum.ROVER_HAVOC_MALE): BaseResonatorModel(
        name=_(ZhTwEnum.ROVER_HAVOC_MALE), element=_(ZhTwEnum.HAVOC)
    ),
}
