def main(api):
    r = {}
    r['__type__'] = "char"
    r['char_name'] = "yc"
    r['attack'] = 7
    r['health'] = 41
    r['group'] = 2

    s1 = {}
    s1['skill_name'] = '先上历史'
    s1['skill_description'] = '全场进入“历史课”3 回合，期间所有己方角色攻击力 +2，双方皆无法使用技能、道具' 
    s1['skill_type'] = api.c.SkillType.ACTIVENONAGGRESSIVE
    s1es = api.interpret('''[{
                "__effect__": true, 
                "type": 7, 
                "target": {"__target__": true, "type": 8}, 
                "buff": {
                    "identification": -1, 
                    "name": "__lsk__", 
                    "lasttime": 6, 
                    "usetime": -1, 
                    "type": 4, 
                    "positivity": 3,
                    "buffdata":{
                        "eventtime": 9, 
                        "effects": [{
                            "__effect__": true, 
                            "type": 5, 
                            "variableid": {"__variableid__":true, "type":"4"},
                            "value": 0
                        }, {
                            "__effect__": true, 
                            "type": 5, 
                            "variableid": {"__variableid__":true, "type":"10"},
                            "value": 0
                        }]
                    }
                }
            }, {
                "__effect__": true, 
                "type": 7, 
                "target": {"__target__": true, "type": 4}, 
                "buff": {
                    "identification": -1, 
                    "name": "__lsk_self__", 
                    "lasttime": 6, 
                    "usetime": -1, 
                    "type": 3, 
                    "positivity": 3,
                    "buffdata": {
                        "attrid": "2",
                        "value": {"__mathexpression__": true, "operator": "1", "data": ["original", 2]}
                    }
                }
            }]''')
    def s1f(**kw):
        api.raw_exec(s1es, **kw)
    s1['effect'] = {"func": s1f}

    s2 = {}
    s2['skill_name'] = '船毁人亡'
    s2['skill_description'] = '己方全部“上船”，生命 +9，攻击力 +1，指定一人为“船长”，若船长死亡，则己方其余角色皆受到 5 点无来源伤害，且攻击力 -1' 
    s2['skill_type'] = api.c.SkillType.ACTIVENONAGGRESSIVE
    s2['choose'] = True
    s2['choosearea'] = api.Target({"type": 4})
    s2es = api.interpret('''[{
                "__effect__": true, 
                "type": 4, 
                "variableid": {
                    "__variableid__": true,
                    "type": "1", 
                    "target": {"__target__": true, "type": 4}
                }, 
                "increment": 9
            }, {
                "__effect__": true, 
                "type": 4, 
                "variableid": {
                    "__variableid__": true,
                    "type": "2", 
                    "target": {"__target__": true, "type": 4}
                }, 
                "increment": 1
            }, {
                "__effect__": true, 
                "type": 7, 
                "target": {"__target__": true, "type": 16}, 
                "buff": {
                    "identification": -1, 
                    "name": "__captain__", 
                    "lasttime": -1, 
                    "usetime": 1, 
                    "type": 4, 
                    "positivity": 3, 
                    "buffdata": {
                        "effects":[{
                            "__effect__": true, 
                            "type": 4, 
                            "variableid": {
                                "__variableid__": true,
                                "type": "2", 
                                "target": {"__target__": true, "type": 4}
                            }, 
                            "increment": -1
                        },{
                            "__effect__": true, 
                            "type": 1, 
                            "target": {"__target__": true, "type": 4}, 
                            "damage": 5
                        }],
                        "eventtime":15
                    }
                }
            }]''')
    
    def s2f(**kw):
        api.raw_exec(s2es, **kw)
    s2['effect'] = {"func": s2f}

    s3 = {}
    s3['skill_name'] = '断腿求生'
    s3['skill_description'] = '发动后，每回合攻击力 -1，获得 5 护盾，若攻击力不大于零则失去该效果' 
    s3['skill_type'] = api.c.SkillType.ACTIVENONAGGRESSIVE
    s3es = api.interpret('''[{
                "__effect__": true, 
                "type": 7, 
                "target": {"__target__": true, "type": 7}, 
                "buff": {
                    "identification": "_dtqs"
                }
            }]''')
    
    def s3f(**kw):
        api.raw_exec(s3es, **kw)
    s3['effect'] = {"func": s3f}

    r['skill'] = [s1, s2, s3]

    return r