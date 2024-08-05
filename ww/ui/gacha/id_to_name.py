from typing import Optional

from pydantic import BaseModel


class GachaResonatorModel(BaseModel):
    id: str = ""
    rank: Optional[int] = None
    name: str = ""
    permanent: Optional[bool] = None


GachaWeaponModel = GachaResonatorModel

resonators = {
    "1102": GachaResonatorModel(id="1102", rank=4, name="散華", permanent=True),
    "1103": GachaResonatorModel(id="1103", rank=4, name="白芷", permanent=True),
    "1104": GachaResonatorModel(id="1104", rank=5, name="凌陽", permanent=True),
    "1105": GachaResonatorModel(id="1105", rank=5, name="折枝", permanent=False),
    "1202": GachaResonatorModel(id="1202", rank=4, name="熾霞", permanent=True),
    "1203": GachaResonatorModel(id="1203", rank=5, name="安可", permanent=True),
    "1204": GachaResonatorModel(id="1204", rank=4, name="莫特斐", permanent=True),
    "1205": GachaResonatorModel(id="1205", rank=5, name="長離", permanent=False),
    "1301": GachaResonatorModel(id="1301", rank=5, name="卡卡羅", permanent=True),
    "1302": GachaResonatorModel(id="1302", rank=5, name="吟霖", permanent=False),
    "1303": GachaResonatorModel(id="1303", rank=4, name="淵武", permanent=True),
    "1304": GachaResonatorModel(id="1304", rank=5, name="今汐", permanent=False),
    "1305": GachaResonatorModel(id="1305", rank=5, name="相里要", permanent=False),
    "1402": GachaResonatorModel(id="1402", rank=4, name="秧秧", permanent=True),
    "1403": GachaResonatorModel(id="1403", rank=4, name="秋水", permanent=True),
    "1404": GachaResonatorModel(id="1404", rank=5, name="忌炎", permanent=False),
    "1405": GachaResonatorModel(id="1405", rank=5, name="鑒心", permanent=True),
    "1501": GachaResonatorModel(
        id="1501", rank=None, name="漂泊者·衍射", permanent=None
    ),
    "1502": GachaResonatorModel(
        id="1502", rank=None, name="漂泊者·衍射", permanent=None
    ),
    "1503": GachaResonatorModel(id="1503", rank=5, name="維里奈", permanent=True),
    "1601": GachaResonatorModel(id="1601", rank=4, name="桃祈", permanent=True),
    "1602": GachaResonatorModel(id="1602", rank=4, name="丹瑾", permanent=True),
    "1604": GachaResonatorModel(
        id="1604", rank=None, name="漂泊者·湮滅", permanent=None
    ),
    "1605": GachaResonatorModel(
        id="1605", rank=None, name="漂泊者·湮滅", permanent=None
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
    "21010024": "異響空靈",
    "21010034": "重破刃-41型",
    "21010044": "永夜長明",
    "21010064": "東落",
    "21010074": "紋秋",
    "21010015": GachaWeaponModel(
        id="21010015", rank=5, name="浩境粼光", permanent=True
    ),
    "21010016": GachaWeaponModel(
        id="21010016", rank=5, name="蒼鱗千嶂", permanent=False
    ),
    "21010026": GachaWeaponModel(
        id="21010026", rank=5, name="時和歲稔", permanent=False
    ),
    "21020011": "教學迅刀",
    "21020012": "原初迅刀·鳴雨",
    "21020013": "暗夜迅刀·黑閃",
    "21020023": "源能迅刀·測貳",
    "21020043": "遠行者迅刀·旅跡",
    "21020053": "戍關迅刀·鎮海",
    "21020024": GachaWeaponModel(
        id="21020024", rank=4, name="行進序曲", permanent=True
    ),
    "21020034": "瞬斬刀-18型",
    "21020044": "不歸孤軍",
    "21020064": "西升",
    "21020074": "飛景",
    "21020015": GachaWeaponModel(
        id="21020015", rank=5, name="千古洑流", permanent=True
    ),
    "21020016": GachaWeaponModel(
        id="21020016", rank=5, name="赫奕流明", permanent=False
    ),
    "21030011": "教學佩槍",
    "21030012": "原初佩槍·穿林",
    "21030013": "暗夜佩槍·暗星",
    "21030053": "戍關佩槍·平雲",
    "21030023": "源能佩槍·測叁",
    "21030043": "遠行者佩槍·洞察",
    "21030024": GachaWeaponModel(
        id="21030024", rank=4, name="華彩樂段", permanent=True
    ),
    "21030044": "無眠烈火",
    "21030064": "飛逝",
    "21030034": "穿擊槍-26型",
    "21030074": "奔雷",
    "21030015": GachaWeaponModel(
        id="21030015", rank=5, name="停駐之煙", permanent=True
    ),
    "21040011": "教學臂鎧",
    "21040012": "原初臂鎧·磐巖",
    "21040013": "暗夜臂鎧·夜芒",
    "21040053": "戍關臂鎧·拔山",
    "21040023": GachaWeaponModel(
        id="21040023", rank=3, name="源能臂鎧·測肆", permanent=True
    ),
    "21040043": "遠行者臂鎧·破障",
    "21040024": "呼嘯重音",
    "21040044": "袍澤之固",
    "21040034": "鋼影拳-21丁型",
    "21040074": "金掌",
    "21040064": "駭行",
    "21040015": GachaWeaponModel(
        id="21040015", rank=5, name="擎淵怒濤", permanent=True
    ),
    "21040016": GachaWeaponModel(
        id="21040016", rank=5, name="諸方玄樞", permanent=False
    ),
    "21050011": "教學音感儀",
    "21050012": "原初音感儀·聽浪",
    "21050013": "暗夜矩陣·暝光",
    "21050023": "源能音感儀·測五",
    "21050043": "遠行者矩陣·探幽",
    "21050053": "戍關音感儀·留光",
    "21050024": GachaWeaponModel(
        id="21050024", rank=4, name="奇幻變奏", permanent=True
    ),
    "21050034": "鳴動儀-25型",
    "21050044": "今州守望",
    "21050064": "異度",
    "21050074": "清音",
    "21050015": GachaWeaponModel(
        id="21050015", rank=5, name="漪瀾浮錄", permanent=True
    ),
    "21050016": GachaWeaponModel(
        id="21050016", rank=5, name="掣傀之手", permanent=False
    ),
    "21050026": GachaWeaponModel(
        id="21050026", rank=5, name="瓊枝冰綃", permanent=False
    ),
}
