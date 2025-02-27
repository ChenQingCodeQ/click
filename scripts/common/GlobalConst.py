# -*- coding: utf-8 -*-

"""
"""


# 定义背包最大容量
MAX_INV_SIZE = 12
MAX_EQUIP_SIZE = 6                              # 定义装备栏最大容量

DATA_FIX_UPDATE_TIME = 0.03                     # 固定更新时间
DATA_FOLLOW_UPDATE_TIME = 0.5                   # 跟随者数据更新时间
DATA_HATE_RANGE = 4                             # 仇恨范围

AI_MIN_WAIT_TIME = 10                           # AI最小等待时间
AI_WAIT_TIME_RANGE = 10                         # AI等待时间范围

DATA_MONSTER_DELAY_SPAWN_TIME = 1               # 怪物延迟生成时间
DATA_MONSTER_DELAY_DESTROY_TIME = 3             # 怪物延迟销毁时间

TIMER_TYPE_UPDATE = 1                           # 更新
TIMER_TYPE_DESTROY = 3                          # 销毁
TIMER_TYPE_SPAWN = 4                            # 生成
    
TRAP_TYPE_ATTACK = 1                            # 攻击范围陷阱
TRAP_TYPE_HATE = 2                              # 仇恨陷阱