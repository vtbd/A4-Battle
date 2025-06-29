def main(api):
    r = {}
    r['__type__'] = "char"
    r['char_name'] = "wyl II"
    r['attack'] = 6
    r['health'] = 40
    r['group'] = 2

    s1 = {}
    s1['skill_name'] = 'Skill 1'
    s1['skill_description'] = 'print hello' 
    s1['skill_type'] = api.c.SkillType.ACTIVEAGGRESSIVE
    def s1f(**kw):
        print('hello')
    s1['effect'] = {"func": s1f}

    s2 = {}
    s2['skill_name'] = '盖饭'
    s2['skill_description'] = '同盖饭' 
    s2['skill_type'] = api.c.SkillType.ACTIVEAGGRESSIVE
    s2es = api.interpret('''[{
                "__effect__": true, 
                "type": 1, 
                "target": {"__target__": true, "type": 1}, 
                "damage": 8,
                "flags": []
            }, {
                "__effect__": true, 
                "type": 7, 
                "target": {"__target__": true, "type": 1}, 
                "buff": {
                    "identification": -1, 
                    "name": "饭中淹", 
                    "lasttime": 7, 
                    "usetime": -1, 
                    "type": 5, 
                    "positivity": 1
                }
            }]''')
    def s2f(**kw):
        api.raw_exec(api.EffectSet(s2es))
    s2['effect'] = {"func": s2f}

    r['skill'] = [s1, s2, {}]

    return r