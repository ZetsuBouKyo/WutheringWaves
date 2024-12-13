from typing import Optional

from pydantic import BaseModel


class GachaResonatorModel(BaseModel):
    id: str = ""
    star: Optional[int] = None
    name: str = ""
    permanent: Optional[bool] = None
    number: int = 0


GachaWeaponModel = GachaResonatorModel

resonators = {
    "1102": GachaResonatorModel(id="1102", star=4, name="散華", permanent=True),
    "1103": GachaResonatorModel(id="1103", star=4, name="白芷", permanent=True),
    "1104": GachaResonatorModel(id="1104", star=5, name="凌陽", permanent=True),
    "1105": GachaResonatorModel(id="1105", star=5, name="折枝", permanent=False),
    "1106": GachaResonatorModel(id="1106", star=4, name="釉瑚", permanent=True),
    "1202": GachaResonatorModel(id="1202", star=4, name="熾霞", permanent=True),
    "1203": GachaResonatorModel(id="1203", star=5, name="安可", permanent=True),
    "1204": GachaResonatorModel(id="1204", star=4, name="莫特斐", permanent=True),
    "1205": GachaResonatorModel(id="1205", star=5, name="長離", permanent=False),
    "1301": GachaResonatorModel(id="1301", star=5, name="卡卡羅", permanent=True),
    "1302": GachaResonatorModel(id="1302", star=5, name="吟霖", permanent=False),
    "1303": GachaResonatorModel(id="1303", star=4, name="淵武", permanent=True),
    "1304": GachaResonatorModel(id="1304", star=5, name="今汐", permanent=False),
    "1305": GachaResonatorModel(id="1305", star=5, name="相里要", permanent=False),
    "1402": GachaResonatorModel(id="1402", star=4, name="秧秧", permanent=True),
    "1403": GachaResonatorModel(id="1403", star=4, name="秋水", permanent=True),
    "1404": GachaResonatorModel(id="1404", star=5, name="忌炎", permanent=False),
    "1405": GachaResonatorModel(id="1405", star=5, name="鑒心", permanent=True),
    "1501": GachaResonatorModel(
        id="1501", star=None, name="漂泊者·衍射", permanent=None
    ),
    "1502": GachaResonatorModel(
        id="1502", star=None, name="漂泊者·衍射", permanent=None
    ),
    "1503": GachaResonatorModel(id="1503", star=5, name="維里奈", permanent=True),
    "1504": GachaResonatorModel(id="1504", star=4, name="燈燈", permanent=True),
    "1505": GachaResonatorModel(id="1505", star=5, name="守岸人", permanent=True),
    "1601": GachaResonatorModel(id="1601", star=4, name="桃祈", permanent=True),
    "1602": GachaResonatorModel(id="1602", star=4, name="丹瑾", permanent=True),
    "1603": GachaResonatorModel(id="1603", star=5, name="椿", permanent=False),
    "1604": GachaResonatorModel(
        id="1604", star=None, name="漂泊者·湮滅", permanent=None
    ),
    "1605": GachaResonatorModel(
        id="1605", star=None, name="漂泊者·湮滅", permanent=None
    ),
}

weapons = {
    "21010011": "教學長刃",
    "21010012": "原初長刃·樸石",
    "21010013": "暗夜長刃·玄明",
    "21010023": "源能長刃·測壹",
    "21010043": "遠行者長刃·辟路",
    "21010053": "戍關長刃·定軍",
    "21010063": "鈞天正音",
    "21010024": GachaWeaponModel(
        id="21010024", star=4, name="異響空靈", permanent=True
    ),
    "21010034": "重破刃-41型",
    "21010044": GachaWeaponModel(
        id="21010044", star=4, name="永夜長明", permanent=True
    ),
    "21010064": GachaWeaponModel(id="21010064", star=4, name="東落", permanent=True),
    "21010074": "紋秋",
    "21010015": GachaWeaponModel(
        id="21010015", star=5, name="浩境粼光", permanent=True
    ),
    "21010016": GachaWeaponModel(
        id="21010016", star=5, name="蒼鱗千嶂", permanent=False
    ),
    "21010026": GachaWeaponModel(
        id="21010026", star=5, name="時和歲稔", permanent=False
    ),
    "21020011": "教學迅刀",
    "21020012": "原初迅刀·鳴雨",
    "21020013": "暗夜迅刀·黑閃",
    "21020023": "源能迅刀·測貳",
    "21020026": GachaWeaponModel(id="21020026", star=5, name="裁春", permanent=False),
    "21020043": "遠行者迅刀·旅跡",
    "21020053": "戍關迅刀·鎮海",
    "21020024": GachaWeaponModel(
        id="21020024", star=4, name="行進序曲", permanent=True
    ),
    "21020034": "瞬斬刀-18型",
    "21020044": GachaWeaponModel(
        id="21020044", star=4, name="不歸孤軍", permanent=True
    ),
    "21020064": GachaWeaponModel(id="21020064", star=4, name="西升", permanent=True),
    "21020074": "飛景",
    "21020015": GachaWeaponModel(
        id="21020015", star=5, name="千古洑流", permanent=True
    ),
    "21020016": GachaWeaponModel(
        id="21020016", star=5, name="赫奕流明", permanent=False
    ),
    "21030011": "教學佩槍",
    "21030012": "原初佩槍·穿林",
    "21030013": "暗夜佩槍·暗星",
    "21030053": "戍關佩槍·平雲",
    "21030023": "源能佩槍·測叁",
    "21030043": "遠行者佩槍·洞察",
    "21030024": GachaWeaponModel(
        id="21030024", star=4, name="華彩樂段", permanent=True
    ),
    "21030044": GachaWeaponModel(
        id="21030044", star=4, name="無眠烈火", permanent=True
    ),
    "21030064": GachaWeaponModel(id="21030064", star=4, name="飛逝", permanent=True),
    "21030034": "穿擊槍-26型",
    "21030074": "奔雷",
    "21030015": GachaWeaponModel(
        id="21030015", star=5, name="停駐之煙", permanent=True
    ),
    "21040011": "教學臂鎧",
    "21040012": "原初臂鎧·磐巖",
    "21040013": "暗夜臂鎧·夜芒",
    "21040053": "戍關臂鎧·拔山",
    "21040023": GachaWeaponModel(
        id="21040023", star=3, name="源能臂鎧·測肆", permanent=True
    ),
    "21040043": "遠行者臂鎧·破障",
    "21040024": GachaWeaponModel(
        id="21040024", star=4, name="呼嘯重音", permanent=True
    ),
    "21040044": GachaWeaponModel(
        id="21040044", star=4, name="袍澤之固", permanent=True
    ),
    "21040034": "鋼影拳-21丁型",
    "21040074": "金掌",
    "21040064": GachaWeaponModel(id="21040064", star=4, name="駭行", permanent=True),
    "21040015": GachaWeaponModel(
        id="21040015", star=5, name="擎淵怒濤", permanent=True
    ),
    "21040016": GachaWeaponModel(
        id="21040016", star=5, name="諸方玄樞", permanent=False
    ),
    "21050011": "教學音感儀",
    "21050012": "原初音感儀·聽浪",
    "21050013": "暗夜矩陣·暝光",
    "21050023": "源能音感儀·測五",
    "21050043": "遠行者矩陣·探幽",
    "21050053": "戍關音感儀·留光",
    "21050024": GachaWeaponModel(
        id="21050024", star=4, name="奇幻變奏", permanent=True
    ),
    "21050034": "鳴動儀-25型",
    "21050044": GachaWeaponModel(
        id="21050044", star=4, name="今州守望", permanent=True
    ),
    "21050064": GachaWeaponModel(id="21050064", star=4, name="異度", permanent=True),
    "21050074": "清音",
    "21050015": GachaWeaponModel(
        id="21050015", star=5, name="漪瀾浮錄", permanent=True
    ),
    "21050016": GachaWeaponModel(
        id="21050016", star=5, name="掣傀之手", permanent=False
    ),
    "21050026": GachaWeaponModel(
        id="21050026", star=5, name="瓊枝冰綃", permanent=False
    ),
    "21010084": GachaWeaponModel(
        id="21010084", star=4, name="凋亡頻移", permanent=False
    ),
    "21020084": GachaWeaponModel(
        id="21020084", star=4, name="永續坍縮", permanent=False
    ),
    "21030084": GachaWeaponModel(
        id="21030084", star=4, name="悖論噴流", permanent=False
    ),
    "21040084": GachaWeaponModel(
        id="21040084", star=4, name="塵雲旋臂", permanent=False
    ),
    "21050084": GachaWeaponModel(
        id="21050084", star=4, name="核熔星盤", permanent=False
    ),
    "21050036": GachaWeaponModel(
        id="21050036", star=5, name="星序協響", permanent=False
    ),
}
