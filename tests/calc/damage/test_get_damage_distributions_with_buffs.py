from ww.calc.damage import Damage
from ww.calc.simulated_resonators import SimulatedResonators
from ww.crud.template import get_template
from ww.locale import ZhTwEnum, _


def test_get_damage_distributions_with_buffs():
    prefix = _(ZhTwEnum.ECHOES_AFFIXES_15_1)
    monster_id = _(ZhTwEnum.MONSTER_LV_90_RES_20)
    template_id = (
        "[腦測]+3漂泊者·湮滅(男)+1裁春,+6散華+1赫奕流明,+0維里奈+1奇幻變奏-2套A"
    )
    resonator_template = get_template(template_id)

    simulated_resonators = SimulatedResonators(resonator_template)
    resonators_table = simulated_resonators.get_3_resonators_with_prefix(prefix)
    calculated_resonators = simulated_resonators.get_calculated_resonators(
        resonators_table
    )
    calculated_resonators_table = calculated_resonators.get_table()

    resonator_ids = calculated_resonators.get_3_ids()

    damage = Damage(
        monster_id=monster_id,
        resonators_table=resonators_table,
        calculated_resonators_table=calculated_resonators_table,
    )

    damage_distributions = damage.get_damage_distributions_with_buffs(
        template_id,
        resonator_ids[0],
        resonator_ids[1],
        resonator_ids[2],
        monster_id=monster_id,
    )

    for buff_name, damage_distribution in damage_distributions:
        damage = damage_distribution.damage
        print(f"{buff_name}: {damage}")
