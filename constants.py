import json

#display
##general
with open('settings.json', encoding='utf-8') as fl:
    f = json.load(fl)
    S = f['size']
with open('res.json', encoding='utf-8') as fl:
    f = json.load(fl)
    CHARFILE:dict[str, str] = f['charfile']
    CHARAVATARFILE:dict[str, str] = f['charavatarfile']
    EQUIPMENTFILE:dict[str, str] = f['equipmentfile']
    EQUIPMENTPICTUREFILE:dict[str, str] = f['equipmentpicturefile']

##specific
###screen
SCREENSIZE = (1600*S, 900*S)

###about chars
CHARPOSLIST = [(400*S, 100*S), (400*S, 225*S), (400*S, 350*S), (1200*S, 100*S), (1200*S, 225*S), (1200*S, 350*S)]
CHARHEALTHPOSLIST = [(470*S, 100*S), (470*S, 225*S), (470*S, 350*S), (1130*S, 100*S), (1130*S, 225*S), (1130*S, 350*S)]
CHARSHIELDPOSLIST = [(530*S, 100*S), (530*S, 225*S), (530*S, 350*S), (1070*S, 100*S), (1070*S, 225*S), (1070*S, 350*S)]
#CHARSUMMONEDPOSLIST = [()]
CHARNAMEPOSLIST = [(470*S, 100*S), (470*S, 225*S), (470*S, 350*S), (1130*S, 100*S), (1130*S, 225*S), (1130*S, 350*S)]

###about chars' attributes
SKILLBOARDPOS = (0, 0)
SKILLBOARDSIZE = (0, 0)
SKILLTITLEPOSLIST = [(200*S, 600*S), (200*S, 700*S), (200*S, 800*S)]
SKILLDESCRIPTIONPOSLIST = [(400*S, 600*S), (400*S, 700*S), (400*S, 800*S)]
SKILLDESCRIPTIONLENGTH = 800*S
ATTACKPOS = (100*S, 500*S)
ATTACKBUTTONPOS = (300*S, 500*S)
USESKILLBUTTONPUSLIST = [(1300*S, 600*S), (1300*S, 700*S), (1300*S, 800*S)]
SWICHCHARBUTTONPOS = (800*S, 500*S)

STATUSBOARDPOS = (0, 0)
STATUSBOARDSIZE = (0, 0)
STATUSTEXTPOS = (100*S, 500*S)
STATUSTEXTLENGTH = 1400*S

###about eqipments
INFOBOARDPOS = (0, 0)
INFOBOARDSIZE = (0, 0)
EQUIPMENTPOSLIST = [(150*S, 100*S), (275*S, 100*S), (150*S, 225*S), (275*S, 225*S), (150*S, 350*S), (275*S, 350*S), 
                    (1450*S, 100*S), (1325*S, 100*S), (1450*S, 225*S), (1325*S, 225*S), (1450*S, 350*S), (1325*S, 350*S)]
EQUIPMENTNAMEPOS = (200*S, 650*S)
EQUIPMENTDESCRIPTIONPOS = (400*S, 650*S)
EQUIPMENTDESCRIPTIONLENGTH = 800*S
USEEQUIPMENTBUTTONPOS = (1300*S, 650*S)

###game universal
ENDTURNBUTTONPOS = (800*S, 400*S)
ROUNDPOS = (800*S, 15*S)
TURNPOS = (800*S, 60*S)
INFORMATIONBUTTONPOS = (1400*S, 500*S)
INGAMERETRYBUTTONPOS = (800*S, 200*S)
WINBLOCKPOS = (800*S, 400*S)
WINTEXTPOS = (800*S, 300*S)
WINEXITBUTTONPOS = (575*S, 500*S)
WINRETRYBUTTONPOS = (1025*S, 500*S)
CHOOSEBLOCKPOS = (800*S, 425*S)
CHOOSETEXTPOS = (800*S, 150*S)
CHOOSEYESBUTTONPOS = (575*S, 650*S)
CHOOSENOBUTTONPOS = (1025*S, 650*S)
CHOOSECHARPOSLIST = [(600, 300), (800, 300), (1000, 300), (600, 500), (800, 500), (1000, 500)]

###animations
ANIMATIONPOSES = {
    'dsc2': (800*S, 450*S)
}

#about files
INITIALIZEFILE = 'initialize.json'

#CHARNAME = {1:'dsc', 2:'wyh', 3:'wm', 4:'zhh', 5:'Felix', 6:'zyf'}
#CHARFILE = {0:'chars/0.json', 1:'chars/1_dsc.json', 2:'chars/2_wyh.json', 3:'chars/3_wm.json', 4:'chars/4_zhh.json', 5:'chars/5_felix.json', 6:'chars/6_zyf.json'}
#CHARAVATARFILE = {0:'res/null.png',1:'res/char/dsc.png', 2:'res/char/wyh.png', 3:'res/char/wm.png', 4:'res/char/zhh.png', 5:'res/char/felix.png', 6:'res/char/zyf.png'}
CHARFRAMEFILE = 'res/avatar_frame.png'
CHARONFIGHTFRAMEFILE = 'res/avatar_frame_on_fight.png'
CHARDECORATORFILELIST = ['res/null.png', 'res/avatar_dead.png', 'res/choosing_block.png']

'''EQUIPMENTFILE = {
    1: 'equipment/1_ladybug_correction_tape.json',
    2: 'equipment/2_sonic_mop_rod.json',
    3: 'equipment/3_male_aesthetics.json',
    4: 'equipment/4_durian_thorn_extractor.json',
    5: 'equipment/5_camouflage_jacket.json',
    6: 'equipment/6_cigarette.json',
    7: 'equipment/7_spherical_drying_tube.json',
    8: 'equipment/8_orange.json',
    9: 'equipment/9_lemon_tree.json',
    10: 'equipment/10_masturbation_cup.json',
    11: 'equipment/11_jersey_no_24.json',
    12: 'equipment/12_xjp_talk.json', 
    15: 'equipment/测试用电脑.a4be'
}'''
'''EQUIPMENTPICTUREFILE = {1: 'res/equipment/1_ladybug_correction_tape.png', 
                 2: 'res/equipment/2_sonic_mop_rod.png', 
                 3: 'res/equipment/3_male_aesthetics.png', 
                 4: 'res/equipment/4_durian_thorn_extractor.png', 
                 5: 'res/equipment/5_camouflage_jacket.png', 
                 6: 'res/equipment/6_cigarette.png', 
                 7: 'res/equipment/7_spherical_drying_tube.png', 
                 8: 'res/equipment/8_orange.png',
                 9: 'res/equipment/9_lemon_tree.png',
                 10: 'res/equipment/10_masturbation_cup.png',
                 11: 'res/equipment/11_jersey_no_24.png',
                 12: 'res/equipment/12_xjp_talk.png', 
                 15: 'res/equipment/测试用电脑.png'}'''
EQUIPMENTFRAMEFILE = 'res/equipment_frame.png'
EQUIPMENTDECORATORFILELIST = ['res/null.png', 'res/equipment_used.png', 'res/choosing_block.png']


ATTACKBUTTONFILE = 'res/common_attack_button.png'
USEBUTTONFILE = 'res/use_button.png'
SWICHCHARBUTTONFILE = 'res/change_button.png'

ENDTURNBUTTONFILE = 'res/end_turn_button.png'
INFORMATIONBUTTONFILE = 'res/information_button.png'

ANIMATIONFILES = {
    'dsc2': [f'res/animations/chars/dsc/skill_2/{str(i).zfill(2)}.png' for i in range(1, 22)],
}

MASKFILE = 'res/mask.png'
WINBLOCKFILE = 'res/winblock.png'
WINRETRYBUTTONFILE = 'res/button_retry.png'
WINEXITBUTTONFILE = 'res/button_close.png'
SURESUREBUTTONFILE = 'res/sure_button.png'
SURECANCELBUTTONFILE = 'res/cancel_button_new.png'
CHOOSEBLOCKFILE = 'res/chooseblock.png'
INGAMERETRYBUTTONFILE = 'res/button_retry_in_game.png'

#displayed constants
ATTACKHINT = '攻击：'
ROUNDHINT = ('第', '回合')
TURNHINT = ('左边行动', '右边行动')
WINTEXT = ('左边胜利', '右边胜利')
SURETEXT = '当前尚未攻击，是否结束回合？'
CHOOSETEXT = '选择角色'
BUFFHINT = 'buff：'
MARKHINT = '标记：'
SUMMONHINT = '召唤物：'

#group constants
CHARGROUP = {0:'NONE', 1: 'STUDENT', 2: 'TEACHER'}
class CharGroup:
    NONE = 0
    STUDENT = 1
    TEACHER = 2

TARGET = {1: 'ENEMYONFIGHT', 2: 'SELFONFIGHT', 3: 'ENEMYALL', 4: 'SELFALL', 5: 'ENEMYNOTONFIGHT', 6: 'SELFNOTONFIGHT', 7:'SELF', 8:'ALL', 
          9: 'Specific char', 10: 'Specific position', 11:'DAMAGESOURCE', 12:'GROUP', 13:'UNIONSET', 14:'INTERSECTIONSET', 
          15:'DAMAGERECEIVER', 16: 'CHOOSE'}
class Target:
    ENEMYONFIGHT = 1
    SELFONFIGHT = 2
    ENEMYALL = 3
    SELFALL = 4
    ENEMYNOTONFIGHT = 5
    SELFNOTONFIGHT = 6
    SELF = 7
    ALL = 8
    SPECIFICCHAR = 9
    SPECIFICPOSITION = 10
    DAMAGESOURCE = 11
    GROUP = 12
    UNIONSET = 13
    INTERSECTIONSET = 14
    DAMAGERECEIVER = 15
    CHOOSE = 16

EFFECTTYPE = {1: 'DAMAGE', 2: 'HEAL', 3:'KILL', 4: 'INCREASE', 5: 'SET', 6: 'RANDOM', 7:'BUFF', 8:'BUFFCLEAR', 9:'SPECIFIC',
              10:'ENVIRONMENTALBUFF', 11:'SUMMON'}
class EffectType:
    DAMAGE = 1
    HEAL = 2
    KILL = 3
    INCREASE = 4
    SET = 5
    RANDOM = 6
    BUFF = 7
    BUFFCLEAR = 8
    SPECIFIC = 9
    ENVIRONMENTALBUFF = 10
    SUMMON = 11
    class Specific:
        ZHH = 1

VARIABLEID = {'0':'SPECIALVARIABLE', '1': 'HEALTH(targeted)', '2': 'ATTACK(targeted)', '3': 'ATTACKTIME', '4': 'SKILLTIME', '5': 'SWITCHCHARTIME', '6': 'ROUND', '7': 'SHIELD(targeted)', '8': 'MARKS(targeted)'}
class VariableId:
    SPECIALVARIABLE = '0'
    HEALTH = '1'
    ATTACK = '2'
    ATTACKTIME = '3'
    SKILLTIME = '4'
    SWITCHCHARTIME = '5'
    ROUND = '6'
    SHIELD = '7'
    MARKS = '8'

MARKNAMES = {'suppress': '憋', 'dam': '坝', 'lazy': '惰', 'shuang': '爽'}

SKILLTYPE = {1:'ACTIVEAGGRESSIVE', 2: 'ACTIVENONAGRESSIVE', 3: 'PASSIVE'}
class SkillType:
    ACTIVEAGGRESSIVE = 1
    ACTIVENONAGGRESSIVE = 2
    PASSIVE = 3

ATTACKFLAGS = {0: 'COMMONATTACK', 1:'NOEVENT', 2:'DSC', 3:'NORETURN'}
class AttackFlags:
    COMMONATTACK = 0
    NOEVENT = 1
    DSC = 2
    NORETURN = 3

CALCULATOR = {'-1': 'CALLSPECIALVARIABLE', '0': 'CALLVARIABLE', '1': 'ADD', '2': 'SUB', '3': 'TIMES', '4': 'DIV', '5': 'EXP', '6': 'LOG',
               '7': 'ROUND', '8': 'FLOOR', '9': 'CEIL', '10': 'MODE', '11': 'MAX', '12': 'MIN'}
class Calculator:
    CALLSPECIALVARIABLE = '-1'
    CALLVARIABLE = '0'
    ADD = '1'
    SUB = '2'
    TIMES = '3'
    DIV = '4'
    EXP = '5'
    LOG = '6'
    ROUND = '7'
    FLOOR = '8'
    CEIL = '9'
    MOD = '10'
    MAX = '11'
    MIN = '12'

EVENTTIME = {0: 'COMMONATTACK', 1: 'USESKILL', 2: 'WESWITCH', 3: 'SWITCHTO', 4: 'SWITCHFROM', 5: 'GETHURTED', 6: 'ENEMYCOMMONATTACK', 7: 'ENEMYUSESKILL', 8: 'ENEMYSWITCH', 9:'TURNSTART', 10:'TURNEND', 11:'MAKEDAMAGE'}
class EventTime:
    COMMONATTACK = 0
    USESKILL = 1
    WESWITCH = 2
    SWITCHTO = 3
    SWITCHFROM = 4
    GETHURTED = 5
    ENEMYCOMMONATTACK = 6
    ENEMYUSESKILL = 7
    ENEMYSWITCH = 8
    TURNSTART = 9
    TURNEND = 10
    MAKEDAMAGE = 11
    
    
EVENTTYPE = {0: 'ATTACK', 1: 'SKILL', 2: 'SWITCH', 3: 'HURTED', 4: 'TURNSWITCH', 5:'DAMAGEMADE'}
class EventType:
    ATTACK = 0
    SKILL = 1
    SWITCH = 2
    HURTED = 3
    TURNSWITCH = 4
    DAMAGEMADE = 5

BUFFTYPE = {0: 'NONE', 1: 'INCREASEDAMAGEMADE', 2: 'DECREASEDAMAGERECEIVED', 3: 'ATTRIBUTE', 4: 'EFFECT', 5: 'NOSKILL', 6: 'NOATTACK'}
class Bufftype:
    NONE = 0
    INCREASEDAMAGEMADE = 1 
    DECREASEDAMAGERECEIVED = 2 
    ATTRIBUTE = 3
    EFFECT = 4
    NOSKILL = 5
    NOATTACK = 6

BUFFIDENTIFICATION = {-1: 'OTHER', 0: 'ORANGE', 1: 'FLOODEDINFOOD', 2:'BEAUTY', 3:'ILLUSION', 4:'SHY'}
class BuffIdentification:
    OTHER = -1
    ORANGE = 0
    FLOODEDINFOOD = 1
    BEAUTY = 2
    ILLUSION = 3
    SHY = 4

BUFFPOSITIVITY = {0: 'POSITIVE', 1: 'NEGATIVE', 2: 'NEUTRAL', 3: 'INDESTRUCTIBLE'}
class BuffPositivity:
    POSITIVE = 0
    NEGATIVE = 1
    NEUTRAL = 2
    INDESTRUCTIBLE = 3

BOOLJUDGEMENT = {'0': 'GREATER', '1': 'LESS', '2': 'EQUAL', '3': 'GREATEROREQUAL', '4': 'LESSOREQUAL', '5': 'NOTEQUAL', 
                 '6': 'AND', '7': 'OR', '8': 'NOT', '9': 'XOR', '10': 'IN', '11': 'NOTIN'}
class BoolJudgement:
    GREATER = '0'
    LESS = '1'
    EQUAL = '2'
    GREATEROREQUAL = '3'
    LESSOREQUAL = '4'
    NOTEQUAL = '5'
    AND = '6'
    OR = '7'
    NOT = '8'
    XOR = '9'
    IN = '10'
    NOTIN = '11'



#editor
ED_TYPE_READER = {
    '角色': 'char',
    '装备': 'equipment',
    '技能': 'skill',
    '效果': 'effect',
    'Buff': 'buff',
    '数字表达式': 'expression',
    '布尔表达式': 'boolean'
}

ED_TYPE_READER_INVERT = {
    'char': '角色',
    'equipment': '装备',
    'skill': '技能',
    'effect': '效果',
    'buff': 'Buff',
    'expression': '数字表达式',
    'boolean': '布尔表达式'
}

ED_SAVE_HINT = {
    '角色': 'A4 Battle 角色',
    '装备': 'A4 Battle 装备',
    '技能': 'A4 Battle 技能',
    '效果': 'A4 Battle 效果',
    'Buff': 'A4 Battle Buff',
    '数字表达式': 'A4 Battle 数字表达式',
    '布尔表达式': 'A4 Battle 布尔表达式'
}

ED_SAVE_TYPE = {
    '角色': '.a4bc',
    '装备': '.a4be',
    '技能': '.a4bs',
    '效果': '.a4be',
    'Buff': '.a4bb',
    '数字表达式': '.a4bx',
    '布尔表达式': '.a4bo'
}

ED_CHAR_INPUTER_VALUES = {
    0: 'name', 
    1: 'health', 
    2: 'attack'
}

ED_CHAR_CHOICE_VALUES = {
    0: 'group'
}

ED_CHAR_CHOICE_READER = {
    '学生': 1,
    '教师': 2
}

ED_CHAR_CHOICE_READER_INVERT = {
    1: '学生',
    2: '教师'
}

ED_EFFECT_TYPE_READER = {
    '伤害': 1,
    '治疗': 2,
    #'击杀': 3,
    '增加': 4,
    '设定': 5,
    '随机': 6,
    'Buff': 7,
    'Buff 清除': 8,
    #'特殊': 9
}

ED_EFFECT_TYPE_READER_INVERT = {
    1: '伤害',
    2: '治疗',
    #3: '击杀',
    4: '增加',
    5: '设定',
    6: '随机',
    7: 'Buff',
    8: 'Buff 清除',
    #9: '特殊'
}

ED_TARGET_READER = {
    '敌方出战': 1,
    '我方出战': 2,
    '敌方全体': 3,
    '我方全体': 4,
    '敌方非场上角色': 5,
    '我方非场上角色': 6,
    '自身': 7,
    '所有角色': 8,
    #'指定角色': 9,
    #'指定位置': 10,
    #'伤害来源': 11,
    #'组': 12,
    #'并集': 13,
    #'交集': 14
}

ED_TARGET_READER_INVERT = {
    1: '敌方出战',
    2: '我方出战',
    3: '敌方全体',
    4: '我方全体',
    5: '敌方非场上角色',
    6: '我方非场上角色',
    7: '自身',
    8: '所有角色',
    #9: '指定角色',
    #10: '指定位置',
    #11: '伤害来源',
    #12: '组',
    #13: '并集',
    #14: '交集'
}

ED_VARIABLEID_READER = {
    '生命值': '1',
    '攻击力': '2',
    '攻击次数': '3',
    '技能次数': '4',
    '换人次数': '5',
    '回合数': '6',
    '护盾值': '7',
    '标记数': '8'
}

ED_VARIABLEID_READER_INVERT = {
    '1': '生命值',
    '2': '攻击力',
    '3': '攻击次数',
    '4': '技能次数',
    '5': '换人次数',
    '6': '回合数',
    '7': '护盾值',
    '8': '标记数'
}

ED_SKILL_TYPE_READER = {
    '主动攻击': 1,
    '主动非攻击': 2,
    '被动': 3
}

ED_SKILL_TYPE_READER_INVERT = {
    1: '主动攻击',
    2: '主动非攻击',
    3: '被动'
}

ED_BUFF_TYPE_READER = {
    '无': 0, 
    '改变打出伤害': 1, 
    '改变受到伤害': 2,  
    '改变属性': 3, 
    '定时执行效果': 4, 
    '禁止使用技能': 5, 
    '禁止攻击': 6
}

ED_BUFF_TYPE_READER_INVERT = {
    0: '无',
    1: '改变打出伤害',
    2: '改变受到伤害',
    3: '改变属性',
    4: '定时执行效果',
    5: '禁止使用技能',
    6: '禁止攻击'
}

ED_BUFF_POSITIVITY_READER = {
    '正面': 0,
    '负面': 1,
    '中性': 2,
    '不被清除标识': 3
}

ED_BUFF_POSITIVITY_READER_INVERT = {
    0: '正面', 
    1: '负面', 
    2: '中性', 
    3: '不被清除标识'
}

