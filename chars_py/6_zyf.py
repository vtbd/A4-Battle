__version__ = "0"
def main(api):
    r = {}
    r['__type__'] = "char"
    r['char_name'] = "zyf"
    r['attack'] = 5
    r['health'] = 35
    r['group'] = 1

    s1 = {}
    s1['skill_name'] = '大坝工程师'
    s1['skill_description'] = '普通攻击使对方出战获得 1 个「坝」标记，场上每多 1 个「坝」就获得 3 护盾，场上每少 1 个「坝」就失去 3 生命' 
    s1['skill_type'] = api.c.SkillType.PASSIVE
    def catk(**kw):
        api.self.shield += 3
        mk = api.game.charlist[api.get_target(1, **kw)[0]].marks
        mk['dam'] = mk.get('dam', 0) + 1
    def s1f(**kw):
        buff = api.Buff({
            "name": "__zyf_1__", 
            "lasttime": -1, 
            "usetime": -1, 
            "type": api.c.BuffType.EFFECT, 
            "positivity": 3,
            "buffdata": {
                "eventtime": api.c.EventTime.COMMONATTACK, 
                "effects":[api.Effect({"type":0, "func":catk})]
            }
        })
        api.self.append_buff(buff)
    s1['effect'] = {"func": s1f}

    s2 = {}
    s2['skill_name'] = '取你大坝'
    s2['skill_description'] = '移除对方出战角色的所有「坝」标记，对其造成 5 倍相当于移除标记数的伤害' 
    s2['skill_type'] = api.c.SkillType.ACTIVEAGGRESSIVE
    def s2f(**kw):
        target = api.target(1, **kw)
        target_char = api.game.charlist[api.conc_target(target, **kw)[0]]
        dam_count = target_char.marks.get('dam', 0)
        target_char.marks['dam'] = 0
        api.damage(5*dam_count, target, **kw)
        api.self.health -= dam_count*3
    s2['effect'] = {"func": s2f}

    s3 = {}
    s3['skill_name'] = '祈雨'
    s3['skill_description'] = '使所有敌方存活角色获得一个「坝」标记，然后对每个敌方存活角色造成 (其「坝」标记数 *3) 点伤害' 
    s3['skill_type'] = api.c.SkillType.ACTIVEAGGRESSIVE
    def s3f(**kw):
        targets = api.get_target(3, restrict_alive=True, **kw)
        for seq in targets:
            target = api.target(10, pos=seq)
            target_char = api.game.charlist[seq]
            target_char.marks['dam'] = target_char.marks.get("dam", 0)+1
            dam_count = target_char.marks.get('dam', 0)
            api.damage(3*dam_count, target, **kw)
            api.self.shield += 3

    s3['effect'] = {"func": s3f}

    r['skill'] = [s1, s2, s3]

    return r