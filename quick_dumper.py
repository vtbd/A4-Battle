import json

with open("res.json", encoding='utf-8') as fo:
    fn = json.load(fo)
    chars = fn['charfile'].values()
    char_dex = {}
    for dir in chars:
        try:
            with open(dir, encoding='utf-8') as d:
                fc = json.loads(d.read())
                key = fc['name']
                if key != 'none':
                    value = f'{fc['name']}\n攻击：{fc['attack']}\n生命：{fc['health']}\n分组：{['无', '学生', '教师'][fc['group']]}\n技能：\n{'\n'.join(map(lambda x:f'{x['name']}：\n{x['description']}', fc['skill']))}'
                    char_dex[key] = value
        except FileNotFoundError:
            pass

    equipment = fn['equipmentfile'].values()
    equipment_dex = {}
    for dir in equipment:
        try:
            with open(dir, encoding='utf-8') as d:
                fc = json.loads(d.read())
                key = fc['name']
                if key != 'none':
                    value = f'{fc['name']}\n{fc['description']}'
                    equipment_dex[key] = value
        except FileNotFoundError:
            pass
        
with open('dex.json', 'r', encoding='utf-8') as fr:
    original_dict = json.load(fr)

with open("dex.json", 'w', encoding='utf-8') as fw:
    original_dict['角色'] = char_dex
    original_dict['装备'] = equipment_dex
    fw.write(str(json.dumps(original_dict, ensure_ascii=False, indent=4)))