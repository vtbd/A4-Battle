def main(api):
    r = {}
    r['__type__'] = "char"
    r['char_name'] = "wyl II"
    r['attack'] = 4
    r['health'] = 40
    r['group'] = 2

    s1 = {}
    s1['skill_name'] = '龙的传人'
    s1['skill_description'] = '失去 2 点生命，获得 2 个标记「权威」' 
    s1['skill_type'] = api.c.SkillType.ACTIVENONAGGRESSIVE
    s1['infinite'] = True
    def s1f(**kw):
        api.self.health -= 2
        api.self.marks['power'] = api.self.marks.get('power', 0) + 2
    s1['effect'] = {"func": s1f}

    s2 = {}
    s2['skill_name'] = '且听龙吟'
    s2['skill_description'] = '选择不超过当前自身「权威」个数的任意名角色，失去等量「权威」并使选择的角色都获得 1 枚「权威」。使敌方角色获得「权威」时，对其造成 5 点伤害，对自己造成 2 点伤害；使己方其他角色获得「权威」时，使其回复 5 点生命并失去一个随机负面 buff' 
    s2['skill_type'] = api.c.SkillType.ACTIVEAGGRESSIVE
    s2['infinite'] = True
    s2['choose'] = True
    s2['choosecount'] = api.math_expr(lambda **kw:list(range(1, 1+api.self.marks.get('power', 0))))
    s2['choosecount_dynamic'] = True
    def s2f(**kw):
        api.self.marks['power'] -= len(kw["chose"])
        for i in kw["chose"]:
            api.game.charlist[i].marks['power'] = api.game.charlist[i].marks.get('power', 0) + 1
            if i//3 == api.self.seq//3 and i != api.self.seq:
                heal = '''
                        {
                            "__effect__": true, 
                            "type": 2, 
                            "value": 7, 
                            "target": {"__target__": true, "type":10, "pos":"_pos"}
                        }'''
                heal_ = api.interpret(heal)
                print(heal_.target.targetdata)
                api.raw_exec(heal_, _pos=i, **kw)

                negative_buffs = [b for b in api.game.charlist[i].buffs if b.positivity == 1]
                if len(negative_buffs) > 0:
                    api.game.charlist[i].buffs.remove(api.random.choice(negative_buffs))
            else:
                api.damage(5, api.target(10, pos=i), **kw)
                api.damage(2, api.target(10, pos=api.self.seq), **kw)
    s2['effect'] = {"func": s2f}

    s3 = {}
    s3['skill_name'] = '动用权力'
    s3['skill_description'] = '清除场上所有「权威」，选择一名己方角色，使其回复 (4*清除标记数) 点生命且攻击力+3，然后使 1,2 技能失效' 
    s3['skill_type'] = api.c.SkillType.ACTIVEAGGRESSIVE
    s3['choose'] = True
    s3['choosearea'] = api.Target({"type": 4})
    def s3f(**kw):
        sum = 0
        for i in range(6):
            sum += api.game.charlist[i].marks.get('power', 0)
            api.game.charlist[i].marks['power'] = 0
        heal = '''
                {
                    "__effect__": true, 
                    "type": 2, 
                    "value": "heal", 
                    "target": {"__target__": true, "type":16}
                }'''
        api.raw_exec(api.interpret(heal), heal=sum*4, **kw)
        api.game.charlist[kw["chose"][0]].attack += 3
        api.self.skills[0].usetime = 0
        api.self.skills[1].usetime = 0

    s3['effect'] = {"func": s3f}

    r['skill'] = [s1, s2, s3]

    return r