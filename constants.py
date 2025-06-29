import sys
import os
import json

if getattr(sys, 'frozen', False):
    BASEPATH = sys._MEIPASS
else:
    BASEPATH = os.path.dirname(__file__)

# path
_res_path = os.path.join(BASEPATH, 'res.json')
BUFFPATH = os.path.join(BASEPATH, 'bufflist.json')

#display
##general
with open('settings.json', encoding='utf-8') as fl:
    f = json.load(fl)
    S = f['size']
    SHOWSCENEBACKGROUND = f['show_scene_background']

with open(_res_path, encoding='utf-8') as fl:
    f = json.load(fl)
    CHARFILE:dict[str, str] = f['charfile']
    CHARAVATARFILE:dict[str, str] = f['charavatarfile']
    EQUIPMENTFILE:dict[str, str] = f['equipmentfile']
    EQUIPMENTPICTUREFILE:dict[str, str] = f['equipmentpicturefile']
    SCENEFILE:dict[str, str] = f['scenefile']
    SCENEPICTUREFILE:dict[str, str] = f['scenepicturefile']
    CHARNULLFILE = CHARFILE['default']
    EQUIPMENTNULLFILE = EQUIPMENTFILE['default']
    SCENENULLFILE = SCENEFILE['default']


THEME = \
{
    "defaults":
    {
        "colours":
        {
            "normal_bg":"#25292e",
            "hovered_bg":"#45494e",
            "disabled_bg":"#25292e",
            "selected_bg":"#193754",
            "dark_bg":"#15191e",
            "normal_text":"#c5cbd8",
            "hovered_text":"#FFFFFF",
            "selected_text":"#FFFFFF",
            "disabled_text":"#6d736f",
            "link_text": "#0000EE",
            "link_hover": "#2020FF",
            "link_selected": "#551A8B",
            "text_shadow": "#777777",
            "normal_border": "#DDDDDD",
            "hovered_border": "#B0B0B0",
            "disabled_border": "#808080",
            "selected_border": "#8080B0",
            "active_border": "#8080B0",
            "filled_bar":"#f4251b",
            "unfilled_bar":"#CCCCCC"
        }
    },
    "#regular": {
        "font": {
            "name": "zcool",
            "size": 32*S, 
            "regular_path": "res/zcool.ttf"
        }, 
        "misc": {
            "shape": "rounded_rectangle", 
            "shape_corner_radius": f"{round(20*S)}", 
            "border_width": f"{round(4*S)}", 
            "tool_tip_delay": "1.0",
            "text_shadow_size": "1",
            "text_shadow_offset": "0,0",
            "state_transitions":
            {
                "normal_hovered": "0.2",
                "hovered_normal": "0.2"
            }
        }
    }, 
    "button": {
        "prototype": "#regular"
    }
}

##specific

###screen
SCREENSIZE = (1600*S, 900*S)

### main interface
START_BUTTON_SIZE = (300*S, 80*S)
START_BUTTON_POS = (800*S, 400*S)

SETTINGS_BUTTON_SIZE = (300*S, 80*S)
SETTINGS_BUTTON_POS = (800*S, 520*S)

CHOOSE_BUTTON_SIZE = (300*S, 80*S)
CHOOSE_BUTTON_POS = (800*S, 640*S)

### in game
BACK_BUTTON_SIZE = (80*S, 80*S)
BACK_BUTTON_POS = (0, 0)

###about chars
CHARPOSLIST = [(400*S, 100*S), (400*S, 225*S), (400*S, 350*S), (1200*S, 100*S), (1200*S, 225*S), (1200*S, 350*S)]
CHARHEALTHPOSLIST = [(470*S, 100*S), (470*S, 225*S), (470*S, 350*S), (1130*S, 100*S), (1130*S, 225*S), (1130*S, 350*S)]
CHARSHIELDPOSLIST = [(530*S, 100*S), (530*S, 225*S), (530*S, 350*S), (1070*S, 100*S), (1070*S, 225*S), (1070*S, 350*S)]
CHARSUMMONEDPOSLIST = [(590*S, 100*S), (590*S, 225*S), (590*S, 350*S), (1010*S, 100*S), (1010*S, 225*S), (1010*S, 350*S)]
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
CHOOSECHARPOSLIST = [(600*S, 300*S), (800*S, 300*S), (1000*S, 300*S), (600*S, 500*S), (800*S, 500*S), (1000*S, 500*S)]

###animations
ANIMATIONPOSES = {
    'dsc2': (800*S, 450*S)
}

#about files
INITIALIZEFILE = 'initialize.json'

#CHARNAME = {1:'dsc', 2:'wyh', 3:'wm', 4:'zhh', 5:'Felix', 6:'zyf'}
#CHARFILE = {0:'chars/0.json', 1:'chars/1_dsc.json', 2:'chars/2_wyh.json', 3:'chars/3_wm.json', 4:'chars/4_zhh.json', 5:'chars/5_felix.json', 6:'chars/6_zyf.json'}
#CHARAVATARFILE = {0:'res/null.png',1:'res/char/dsc.png', 2:'res/char/wyh.png', 3:'res/char/wm.png', 4:'res/char/zhh.png', 5:'res/char/felix.png', 6:'res/char/zyf.png'}
SCENEIDLIST = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

CHARFRAMEFILE = 'res/avatar_frame.png'
CHARONFIGHTFRAMEFILE = 'res/avatar_frame_on_fight.png'
CHARDECORATORFILELIST = ['res/null.png', 'res/avatar_dead.png', 'res/choosing_block.png']

EQUIPMENTFRAMEFILE = 'res/equipment_frame.png'
EQUIPMENTDECORATORFILELIST = ['res/null.png', 'res/equipment_used.png', 'res/choosing_block.png']

NULLPICTUREFILE = 'res/null.png'

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

SOUND_CLICK = 'res/sound/click.wav'

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
          15:'DAMAGERECEIVER', 16: 'CHOOSE', 17: 'MAXIMIZE', 18:'ITERCHAR', 19:'INTEAMNEXT', 20:'RANDOM'}
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
    MAXIMIZE = 17
    ITERCHAR = 18
    INTEAMNEXT = 19
    RANDOM = 20

EFFECTTYPE = {-1: 'DEBUG_PRINT', 0:'EXTERNAL', 1: 'DAMAGE', 2: 'HEAL', 3:'KILL', 4: 'INCREASE', 5: 'SET', 6: 'RANDOM', 7:'BUFF', 8:'BUFFCLEAR', 9:'SPECIFIC',
              10:'ENVIRONMENTALBUFF', 11:'SUMMON', 12:'REVIVE', 13:'SWITCHSCENE', 14:'DESPOIL'}
class EffectType:
    DEBUG_PRINT = -1
    EXTERNAL = 0
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
    REVIVE = 12
    SWITCHSCENE = 13
    DESPOIL = 14
    class Specific:
        ZHH = 1
        LB_2 = 2
        LB_3 = 3
        CAT = 4

VARIABLEID = {'0':'SPECIALVARIABLE', '1': 'HEALTH', '2': 'ATTACK', '3': 'ATTACKTIME', '4': 'SKILLTIME', 
              '5': 'SWITCHCHARTIME', '6': 'ROUND', '7': 'SHIELD', '8': 'MARKS', '9': 'SKILLUSETIME', 
              '10': 'EQUIPTIME'}
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
    SKILLUSETIME = '9'
    EQUIPTIME = '10'

MARKNAMES = {'suppress': '憋', 'dam': '坝', 'lazy': '惰', 'shuang': '爽', 'alcohol': '酒', 'ji': "唧", 'power': '权威'}

SKILLTYPE = {1:'ACTIVEAGGRESSIVE', 2: 'ACTIVENONAGRESSIVE', 3: 'PASSIVE'}
class SkillType:
    ACTIVEAGGRESSIVE = 1
    ACTIVENONAGGRESSIVE = 2
    PASSIVE = 3

ATTACKFLAGS = {0: 'COMMONATTACK', 1:'NOEVENT', 2:'DSC', 3:'NORETURN', 4:'SKIPSHIELD'}
class AttackFlags:
    COMMONATTACK = 0
    NOEVENT = 1
    DSC = 2
    NORETURN = 3
    SKIPSHIELD = 4

CALCULATOR = {'-2': 'FUNCTION', '-1': 'CALLSPECIALVARIABLE', '0': 'CALLVARIABLE', '1': 'ADD', '2': 'SUB', '3': 'TIMES', '4': 'DIV', '5': 'EXP', '6': 'LOG',
               '7': 'ROUND', '8': 'FLOOR', '9': 'CEIL', '10': 'MODE', '11': 'MAX', '12': 'MIN', '13': 'COUNT', '14': 'LEN', '15': 'RANDINT'}
class Calculator:
    FUNCTION = '-2'
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
    COUNT = '13'
    LEN = '14'
    RANDINT = '15'

EVENTTIME = {0: 'COMMONATTACK', 1: 'USESKILL', 2: 'WESWITCH', 3: 'SWITCHTO', 4: 'SWITCHFROM', 5: 'GETHURTED', 6: 'ENEMYCOMMONATTACK',
              7: 'ENEMYUSESKILL', 8: 'ENEMYSWITCH', 9:'TURNSTART', 10:'TURNEND', 11:'MAKEDAMAGE', 12: 'WEEQUIP', 13:'ENEMYEQUIP', 14:'USEEQUIP', 
              15: 'SELFDIE', 16: 'OWNSIDEDIE', 17: 'ENEMYDIE'}
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
    WEEQUIP = 12
    ENEMYEQUIP = 13
    USEEQUIP = 14
    SELFDIE = 15
    OWNSIDEDIE = 16
    ENEMYDIE = 17
    GETDAMAGED = 18    # 与 GETHURTED 不等价，此事件参数在触发自身效果之前触发
    TURNSWITCH = 19
    
EVENTTYPE = {0: 'ATTACK', 1: 'SKILL', 2: 'SWITCH', 3: 'HURTED', 4: 'TURNSWITCH', 5:'DAMAGEMADE', 6:'EQUIP', 7: 'DIE'}
class EventType:
    ATTACK = 0
    SKILL = 1
    SWITCH = 2
    HURTED = 3
    TURNSWITCH = 4
    DAMAGEMADE = 5
    EQUIP = 6
    DIE = 7

BUFFTYPE = {0: 'NONE', 1: 'INCREASEDAMAGEMADE', 2: 'DECREASEDAMAGERECEIVED', 3: 'ATTRIBUTE', 4: 'EFFECT', 5: 'NOSKILL', 6: 'NOATTACK', 7:'IMMORTAL'}
class Bufftype:
    NONE = 0
    INCREASEDAMAGEMADE = 1 
    DECREASEDAMAGERECEIVED = 2 
    ATTRIBUTE = 3
    EFFECT = 4
    NOSKILL = 5
    NOATTACK = 6
    IMMORTAL = 7

BUFFCLEARTYPE = {"1": "POSITIVITY", "2": "IDENTIFICATION"}
class BuffClearType:
    POSITIVITY = "1"
    IDENTIFICATION = "2"

BUFFPOSITIVITY = {0: 'POSITIVE', 1: 'NEGATIVE', 2: 'NEUTRAL', 3: 'NOTBUFF', 4: 'INDESTRUCTIBLE'}
class BuffPositivity:
    POSITIVE = 0
    NEGATIVE = 1
    NEUTRAL = 2
    NOTBUFF = 3
    INDESTRUCTIBLE = 4

BOOLJUDGEMENT = {'-1': 'SPECIAL', '0': 'GREATER', '1': 'LESS', '2': 'EQUAL', '3': 'GREATEROREQUAL', '4': 'LESSOREQUAL', '5': 'NOTEQUAL', 
                 '6': 'AND', '7': 'OR', '8': 'NOT', '9': 'XOR', '10': 'IN', '11': 'NOTIN', '12': 'ALIVE', '13': 'GROUP'}
class BoolJudgement:
    SPECIAL = '-1'
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
    ALIVE = '12'
    GROUP = '13'

    class Special:
        HAVEBUFF = "1"
        EQUIPMENTUSED = "2"
