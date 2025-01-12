# SPDX-License-Identifier: GPL-3.0
# Copyright (c) 2014-2025 William Edwards <shadowapex@gmail.com>, Benjamin Bean <superman2k5@gmail.com>
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Union

from tuxemon.combat import set_var
from tuxemon.db import StatType
from tuxemon.item.itemeffect import ItemEffect, ItemEffectResult

if TYPE_CHECKING:
    from tuxemon.item.item import Item
    from tuxemon.monster import Monster


@dataclass
class ChangeStatEffect(ItemEffect):
    """
    Increases or decreases target's stats by percentage permanently.

    Parameters:
        statistic: type of statistic (hp, armour, etc.)
        percentage: percentage of the statistic (increase / decrease)

    """

    name = "change_stat"
    statistic: str
    percentage: float

    def apply(
        self, item: Item, target: Union[Monster, None]
    ) -> ItemEffectResult:
        assert target

        if self.statistic not in list(StatType):
            raise ValueError(f"{self.statistic} isn't among {list(StatType)}")

        set_var(self.session, self.name, str(target.instance_id.hex))
        client = self.session.client.event_engine
        params = [self.name, self.statistic, self.percentage]
        client.execute_action("modify_monster_stats", params, True)
        return ItemEffectResult(
            name=item.name, success=True, num_shakes=0, extras=[]
        )
