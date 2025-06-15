import constants
import pygame
import gui
import json
import math
import random
import os

def custom_decoder(obj):
    if "__tuple__" in obj:
        return tuple(obj["data"])
    if "__effect__" in obj:
        return Effect(**obj)
    if "__skill__" in obj:
        return Skill(obj)
    if "__target__" in obj:
        return Target(obj)
    if "__variableid__" in obj:
        return Variableid(obj)
    if "__mathexpression__" in obj:
        return MathExpression(obj)
    if "__boolexpression__" in obj:
        return BoolExpression(obj)
    if "__summoned__" in obj:
        return Summoned(**obj)
    return obj


def loadanimation(animlist, screen, root, pos, mode, size, alpha=False):
    an = gui.MtpApprObj(screen, root, 0, pos, mode, size, alpha)
    an.setimagelist(animlist, 2, [(an.rect.center, (0, 0), size, True)]*len(animlist))
    return an
        

class Target:
    def __init__(self, targetdata: dict):
        self.targetdata = targetdata

    def concretize(self, game, **kw) -> list[int]:
        # 这只是暂时的解决方案，早晚会出问题
        ignore_alive = self.concretize_ignore_alive(game, **kw)
        if self.targetdata.get("restrict_alive", False) == False:
            return ignore_alive
        else:
            alive = []
            for seq in ignore_alive:
                if game.charlist[seq].alive:
                    alive.append(seq)
            return alive

    def concretize_ignore_alive(self, game, **kw) -> list[int]:
        game:Game
        t = self.targetdata['type']
        td = self.targetdata
        hardmode = td.get('hardmode', False)
        # hardmode: 根据当前角色`charself`计算敌方/己方。关闭时，会根据当前轮次计算敌方/己方。
        if hardmode:
            gt = kw['charself'] // 3
        else:
            gt = game.turns %2
        if t == constants.Target.ENEMYONFIGHT:
            if game.specialvars.get('____target_enemy_on_fight____', -1) == -1:
                if gt == 0:
                    return [game.onfightr]
                if gt == 1:
                    return [game.onfightl]
                raise
            return [game.specialvars.get('____target_enemy_on_fight____')]
        elif t == constants.Target.ENEMYALL:
            if gt == 0:
                return [3, 4, 5]
            if gt == 1:
                return [0, 1, 2]
        elif t == constants.Target.ENEMYNOTONFIGHT:
            if gt == 0:
                a = [3, 4, 5]
                a.remove(game.onfightr)
                return a
            if gt == 1:
                a = [0, 1, 2]
                a.remove(game.onfightl)
                return a
        elif t == constants.Target.SELF:
            if kw.get('charself') == None:
                raise ValueError(f'Charself expected')
            else:
                return [kw['charself']]
        elif t == constants.Target.ALL:
            return list(range(6))
        elif t == constants.Target.SELFONFIGHT:
            if gt == 0:
                return [game.onfightl]
            if gt == 1:
                return [game.onfightr]
        elif t == constants.Target.SELFALL:
            if gt == 0:
                return [0, 1, 2]
            if gt == 1:
                return [3, 4, 5]
        elif t == constants.Target.SELFNOTONFIGHT:
            if gt == 0:
                a = [0, 1, 2]
                a.remove(game.onfightl)
                return a
            if gt == 1:
                a = [3, 4, 5]
                a.remove(game.onfightr)
                return a
        elif t == constants.Target.DAMAGESOURCE:
            return [kw.get('source')] if kw.get('source') is not None else []
        elif t == constants.Target.DAMAGERECEIVER:
            return [kw.get('receiver')]
        elif t == constants.Target.SPECIFICCHAR:
            rl = []
            for i, x in enumerate(game.charidlist):
                if x == td['char']:
                    rl.append(i)
            return rl
        elif t == constants.Target.SPECIFICPOSITION:
            m = td['pos']
            if type(m) == list:
                return m
            if type(m) == int:
                return [m]
            if type(m) == MathExpression or type(m) == Variableid:
                return [game.calcnum(m, **kw)]
        elif t == constants.Target.GROUP:
            rl = []
            for i, x in enumerate(game.charlist):
                if x.group in td['groups']:
                    rl.append(i)
            return rl
        elif t == constants.Target.UNIONSET:
            return list(set(td['sets'][0].concretize(game, **kw)).union(*map(lambda x:x.concretize(game, **kw), td['sets'][1:])))
        elif t == constants.Target.INTERSECTIONSET:
            return list(set(td['sets'][0].concretize(game, **kw)).intersection(*map(lambda x:x.concretize(game, **kw), td['sets'][1:])))
        elif t == constants.Target.CHOOSE:
            return kw['chose']
        elif t == constants.Target.MAXIMIZE:
            rangef = self.targetdata['range'].concretize(game, **kw)
            if rangef == []:
                return []
            for i, ci in enumerate(rangef):
                if i == 0:
                    largestnum = game.calcnum(self.targetdata['expression'], iterchar=i)
                    largestchar = ci
                else:
                    n = game.calcnum(self.targetdata['expression'], iterchar=i)
                    if largestnum < n:
                        largestnum = n
                        largestchar = ci
            return [largestchar]   
        elif t == constants.Target.ITERCHAR:
            return [kw['iterchar']]
        elif t == constants.Target.INTEAMNEXT:
            return (kw['base']+1)%3 + kw['base']//3
        elif t == constants.Target.RANDOM:
            return [random.choice(self.targetdata['target'].concretize(game, **kw))]
        else:
            raise ValueError(f'Invalid target id:{t}')


class Buff:
    def __init__(self, dat:dict):
        self.dat = dat.copy()
        self.load(dat)
    
    def load(self, dat):
        self.identification = dat.get('identification', -1)
        if self.identification != -1:
            tempdat = bufflist[self.identification] | dat   # 合并两字典，当前数据覆盖原有
            self.dat = tempdat
        self.name = self.dat['name']
        self.lasttime = self.dat['lasttime']
        self.usetime = self.dat['usetime']
        self.age = 0
        self.type = self.dat['type']
        self.environmental = self.dat.get("environmental", False)
        self.isbuff = False if self.type == constants.BuffPositivity.NOTBUFF else True
        if not self.environmental:
            self.positivity = self.dat['positivity']
        if self.type == constants.Bufftype.EFFECT:
            self.effects = EffectSet(self.dat['buffdata']['effects'])
            if self.environmental:
                pass
            else:
                self.eventtime = self.dat['buffdata']['eventtime']
        elif self.type == constants.Bufftype.INCREASEDAMAGEMADE:
            self.increment = self.dat['buffdata']['increment']
        elif self.type == constants.Bufftype.DECREASEDAMAGERECEIVED:
            self.decrement = self.dat['buffdata']['decrement']
        elif self.type == constants.Bufftype.ATTRIBUTE:
            self.attrid = self.dat['buffdata']['attrid']
            self.value = self.dat['buffdata']['value']
        if self.dat.get('condition') != None:
            self.condition = self.dat['condition']
        else:
            self.condition = True

    def copy(self):
        return Buff(self.dat)


class Effect:
    def __init__(self, **kw):
        self.kw = kw
        self.load(**kw)

    def load(self, **kw):
        self.effecttype:int = kw['type']
        self.condition:bool = kw.get('condition', True)
        t = self.effecttype
        if t == constants.EffectType.DEBUG_PRINT:
            self.message = kw['message']
        elif t == constants.EffectType.DAMAGE:
            self.damage:int = kw['damage']
            self.target:Target = kw['target']
            self.source:dict = kw.get('source')
            self.flags:list[int] = kw.get('flags', [])
        elif t == constants.EffectType.HEAL:
            self.value:int = kw['value']
            self.target:Target = kw['target']
        elif t == constants.EffectType.SET:
            self.variableid:Variableid = kw['variableid']
            self.value = kw['value']
        elif t == constants.EffectType.INCREASE:
            self.variableid:Variableid = kw['variableid']
            self.increment = kw['increment']
        elif t == constants.EffectType.BUFF:
            self.buff:Buff = Buff(kw['buff'])
            self.target:Target = kw['target']
        elif t == constants.EffectType.BUFFCLEAR:
            self.target:Target = kw['target']
            self.clear_type = kw.get("clear_type", constants.BuffClearType.POSITIVITY)
            if self.clear_type == constants.BuffClearType.POSITIVITY:
                self.positivities:list[int] = kw['positivities']
            elif self.clear_type == constants.BuffClearType.IDENTIFICATION:
                self.identification = kw['identification']
            else:
                raise ValueError(f'Invalid buffclear type:{self.clear_type}')
        elif t == constants.EffectType.SPECIFIC:
            self.specific = kw['specific']
        elif t == constants.EffectType.ENVIRONMENTALBUFF:
            self.buff = Buff(kw['buff'])
        elif t == constants.EffectType.KILL:
            self.target = kw['target']
        elif t == constants.EffectType.RANDOM:
            self.probabilities = kw['probabilities']
            self.effects = kw['effects']
        elif t == constants.EffectType.SUMMON:
            self.summoned:Summoned = kw['summoned']
            self.target:Target = kw['target']
        elif t == constants.EffectType.REVIVE:
            self.target:Target = kw['target']
            self.revivehealth = kw['revivehealth']
        elif t == constants.EffectType.SWITCHSCENE:
            self.scene = kw['scene']
        elif t == constants.EffectType.DESPOIL:
            self.despoil_from:Variableid = kw['from']
            self.despoil_to:Variableid = kw['to']
            self.value = kw['value']
        else:
            raise ValueError(f'Invalid effect type:{t}')
    
            
class EffectSet:
    def __init__(self, fl:list[Effect]):
        self.effects = fl
    

class Equipment:
    def __init__(self, datafilestr, game, seq:int):
        try:
            with open(os.path.join(constants.BASEPATH, datafilestr), encoding='utf-8') as datafile:
                data:dict = json.load(datafile, object_hook=custom_decoder)
        except FileNotFoundError:
            print(f'Warning: File not found: {datafilestr}')
            with open(os.path.join(constants.BASEPATH, constants.EQUIPMENTNULLFILE), encoding='utf-8') as datafile:
                data:dict = json.load(datafile, object_hook=custom_decoder)

        self.seq:int = seq
        self.owner:int = seq // 2
        self.name:str = data['name']
        self.description:str = data['description']
        #self.equiptype:int = data['type']
        self.effects:EffectSet = EffectSet(data['effect'])
        self.usetime = data.get('usetime', 1)
        self.choose:bool = data.get('choose', False)
        self.choosearea:Target = data.get('choosearea', Target({"type":constants.Target.ALL}))
        self.choosecondition:bool|BoolExpression = data.get('choosecondition', True)
        self.choosecount:int = data.get('choosecount', 1)
        
        self.infoboard = gui.LayoutObj(game.root, constants.INFOBOARDPOS, size=constants.INFOBOARDSIZE)
        self.infoboard.movability = True
        self.skilltexts:list[gui.TextImagifier] = []
        self.skilltexts += [gui.TextImagifier(game.screen, self.infoboard, game.font_big, self.name, (0, 0, 0), constants.EQUIPMENTNAMEPOS, (0, 0))]
        self.skilltexts += [gui.TextImagifier(game.screen, self.infoboard, game.font_small, self.description, (0, 0, 0), constants.EQUIPMENTDESCRIPTIONPOS, (1, 0), constants.EQUIPMENTDESCRIPTIONLENGTH)]
        self.infodisplayer:list[gui.ImageObj] = [m.imagify() for i, m in enumerate(self.skilltexts)]

        self.useequipbutton:gui.ButtonObj = gui.ButtonObj(game.screen, self.infoboard, constants.USEBUTTONFILE, constants.USEEQUIPMENTBUTTONPOS, (1, 0), constants.S, True)

        self.allrelatingobjs = self.infodisplayer.copy()
        self.allrelatingobjs.append(self.useequipbutton)

    def update(self, game):
        game:Game
        self.changingdisplayer = []
        if game.chosetype == 2 and game.chose == self.seq and self.usetime > 0:
            if self.owner == Target({"type": constants.Target.SELFONFIGHT}).concretize(game)[0]:
                if game.useequiptime > 0:
                    self.changingdisplayer.append(self.useequipbutton)
                    
        self.infodisplayer:list[gui.ImageObj] = [m.imagify() for i, m in enumerate(self.skilltexts)]


class Scene:
    def __init__(self, datafilestr, game):
        try:
            with open(os.path.join(constants.BASEPATH, datafilestr), encoding='utf-8') as datafile:
                data:dict = json.load(datafile, object_hook=custom_decoder)
        except FileNotFoundError:
            print(f'Warning: File not found: {datafilestr}')
            with open(os.path.join(constants.BASEPATH, constants.SCENENULLFILE), encoding='utf-8') as datafile:
                data:dict = json.load(datafile, object_hook=custom_decoder)

        self.datafilestr = datafilestr
        self.game:Game = game
        self.name:str = data['name']
        self.description:str = data['description']
        self.sceneid = data['id']
        if constants.SHOWSCENEBACKGROUND:
            self.bgfile:str = constants.SCENEPICTUREFILE[self.sceneid]
            self.bgimage:gui.ImageObj = gui.ImageObj(game.screen, game.root, self.bgfile, (0, 0), (1, 1), constants.SCREENSIZE, notfound=constants.NULLPICTUREFILE)
        self.effects_instant = EffectSet(data['effect'])
        self.effect_time_sets:list[EffectSet] = [EffectSet(fl) for fl in data['effect_time']]
        self.timelist:list[int] = data['timelist']
        self.age = 0
    
    def copy(self):
        return Scene(self.datafilestr, self.game)


class Summoned:
    def __init__(self, **kw):
        self.dic = kw
        self.name:str = kw['name']
        self.additionalbuff:list[Buff] = list(map(lambda x:Buff(x), kw.get('buff', [])))
        self.health:int = kw['health']
        self.on_death:list[Effect] = EffectSet(kw.get('on_death', []))
        self.follow_attack:bool = kw.get('follow_attack', False)
        self.attack = kw.get('attack', 0)

    def copy(self):
        return Summoned(**self.dic)
    

class Skill:
    def __init__(self, skilldict:dict, game=None):
        self.name:str = skilldict['name']
        self.description:str = skilldict['description'] if 'long_description_alternate' not in skilldict else skilldict.get('long_description_alternate', '')
        self.skilltype:int = skilldict['type']
        self.effects:EffectSet = EffectSet(skilldict['effect'])
        self.usetime = skilldict.get("usetime", 1)
        self.infinite = skilldict.get('infinite', False)
        self.choose:bool = skilldict.get('choose', False)
        self.choosecondition:bool|BoolExpression = skilldict.get('choosecondition', True)
        self.choosearea:Target = skilldict.get('choosearea', Target({"type":constants.Target.ALL}))
        self.choosecount:int = skilldict.get('choosecount', 1)
        #if skilldict.get('animation') != None:
        #    #need to be changed
        #    self.animation = loadanimation(constants.ANIMATIONFILES[skilldict['animation']], game.screen, game.root, constants.ANIMATIONPOSES[skilldict['animation']], (0, 0), constants.S*2, True)
        #else:
        #    self.animation = None


class Char:
    def __init__(self, datafilestr, game, seq:int):
        try:
            with open(os.path.join(constants.BASEPATH, datafilestr), encoding='utf-8') as datafile:
                data:dict = json.load(datafile, object_hook=custom_decoder)
        except FileNotFoundError:
            print(f'Warning: File not found: {datafilestr}')
            with open(os.path.join(constants.BASEPATH, constants.CHARNULLFILE), encoding='utf-8') as datafile:
                data:dict = json.load(datafile, object_hook=custom_decoder)

        self.game:Game = game
        self.seq:int = seq
        self.name:str = data['name']
        self.attack:int = data['attack']
        self.absattack:int = self.attack
        self.originalattack:int = self.attack
        self.shield:int = 0
        self.skills:tuple[Skill, Skill, Skill] = tuple(k for k in data['skill'])
        self.buffs:list[Buff] = []
        self.group:int = data['group']
        self.alive:bool = True
        self._health:int = data['health']
        self.maxhealth:int = self._health
        self.marks:dict = {}
        self.summons:list[Summoned] = []

        self.skillboard = gui.LayoutObj(game.root, constants.SKILLBOARDPOS, size=constants.SKILLBOARDSIZE)
        self.skillboard.movability = True
        self.skilltexts_black:list[gui.TextImagifier] = []
        self.skilltexts_black += [gui.TextImagifier(game.screen, self.skillboard, game.font_big, ("*" if skill.skilltype == constants.SkillType.ACTIVEAGGRESSIVE else "") + skill.name, (0, 0, 0), constants.SKILLTITLEPOSLIST[i], (0, 0)) for i, skill in enumerate(self.skills)]
        self.skilltexts_black += [gui.TextImagifier(game.screen, self.skillboard, game.font_small, skill.description, (0, 0, 0), constants.SKILLDESCRIPTIONPOSLIST[i], (1, 0), constants.SKILLDESCRIPTIONLENGTH) for i, skill in enumerate(self.skills)]
        self.skilltexts_grey:list[gui.TextImagifier] = []
        self.skilltexts_grey += [gui.TextImagifier(game.screen, self.skillboard, game.font_big, ("*" if skill.skilltype == constants.SkillType.ACTIVEAGGRESSIVE else "") + skill.name, (128, 128, 128), constants.SKILLTITLEPOSLIST[i], (0, 0)) for i, skill in enumerate(self.skills)]
        self.skilltexts_grey += [gui.TextImagifier(game.screen, self.skillboard, game.font_small, skill.description, (128, 128, 128), constants.SKILLDESCRIPTIONPOSLIST[i], (1, 0), constants.SKILLDESCRIPTIONLENGTH) for i, skill in enumerate(self.skills)]

        self.skillimage_black:list[gui.ImageObj] = [m.imagify() for i, m in enumerate(self.skilltexts_black)]
        self.skillimage_grey:list[gui.ImageObj] = [m.imagify() for i, m in enumerate(self.skilltexts_grey)]
        self.skilldisplayer:list[gui.ImageObj] = self.skillimage_black.copy()

        self.attacktext = gui.TextImagifier(game.screen, self.skillboard, game.font_big, constants.ATTACKHINT+str(self.attack), (0, 0, 0), constants.ATTACKPOS, (1, 0))
        self.attackdisplayer = self.attacktext.imagify()

        self.attackbutton = gui.ButtonObj(game.screen, self.skillboard, constants.ATTACKBUTTONFILE, constants.ATTACKBUTTONPOS, (1, 0), constants.S, True)
        self.useskillbuttons: list[gui.ButtonObj] = [gui.ButtonObj(game.screen, self.skillboard, constants.USEBUTTONFILE, constants.USESKILLBUTTONPUSLIST[i], (1, 0), constants.S, True) for i, skill in enumerate(self.skills)]
        self.switchcharbutton = gui.ButtonObj(game.screen, self.skillboard, constants.SWICHCHARBUTTONFILE, constants.SWICHCHARBUTTONPOS, (0, 0), constants.S, True)

        self.buttons = self.useskillbuttons.copy()
        self.buttons.append(self.attackbutton)
        self.buttons.append(self.switchcharbutton)

        self.statusboard = gui.LayoutObj(game.root, constants.STATUSBOARDPOS, size=constants.STATUSBOARDSIZE)
        self.statusboard.movability = True
        self.updatestatus()
        
    def updatestatus(self):
        bufftext = constants.BUFFHINT + '\n    ' + ', '.join([buff.name for buff in self.buffs if buff.name[0] != '_' or debug_showallbuff])
        markstext = constants.MARKHINT + '\n    ' + ', '.join([f'{constants.MARKNAMES.get(k, k)}:{v}' for k, v in self.marks.items() if (v != 0 and k in constants.MARKNAMES) or debug_showallmark])
        summontext = constants.SUMMONHINT + '\n    ' + ', '.join([f'{s.name}(生命:{s.health})' for s in self.summons if s.name[0] != '_'])
        self.statusdisplayer = gui.TextImagifier(self.game.screen, self.statusboard, self.game.font_big, bufftext + '\n' + markstext+ '\n'+ summontext, (0, 0, 0), constants.STATUSTEXTPOS, (1, 1), constants.STATUSTEXTLENGTH).imagify()

    def update(self):
        self.changingdisplayer = []
        if self.game.chosetype == 1 and self.game.chose == self.seq and self.alive:
            if self.game.chose == Target({"type": constants.Target.SELFONFIGHT}).concretize(self.game)[0]:
                if self.game.attacktime > 0:
                    if constants.Bufftype.NOATTACK not in map(lambda x: x.type, self.buffs):
                        self.changingdisplayer.append(self.attackbutton)
                if constants.Bufftype.NOSKILL not in map(lambda x: x.type, self.buffs):
                    for i, s in enumerate(self.skills):
                        if (s.skilltype == constants.SkillType.ACTIVEAGGRESSIVE and self.game.attacktime >= 1 and self.game.skilltime >= 1 or s.skilltype == constants.SkillType.ACTIVENONAGGRESSIVE and self.game.skilltime >= 1) and (s.usetime >= 1):
                            self.changingdisplayer.append(self.useskillbuttons[i])
            if self.game.chose in Target({"type": constants.Target.SELFNOTONFIGHT}).concretize(self.game):
                if self.game.switchchartime > 0:
                    self.changingdisplayer.append(self.switchcharbutton)
        self.absattack = self.attack
        for b in self.buffs:
            if b.type == constants.Bufftype.ATTRIBUTE:
                if b.attrid == constants.VariableId.ATTACK:
                    if self.game.calbool(b.condition, charself=self.seq, age=b.age):
                        self.absattack = self.game.calcnum(b.value, original=self.absattack, age=b.age)
        for skillindex, sk in enumerate(self.skills):
            if sk.usetime <= 0:
                self.skilldisplayer[skillindex] = self.skillimage_grey[skillindex]
                self.skilldisplayer[skillindex+3] = self.skillimage_grey[skillindex+3]
            else:
                self.skilldisplayer[skillindex] = self.skillimage_black[skillindex]
                self.skilldisplayer[skillindex+3] = self.skillimage_black[skillindex+3]
        self.attacktext = gui.TextImagifier(self.game.screen, self.skillboard, self.game.font_big, constants.ATTACKHINT+str(self.absattack), (0, 0, 0), constants.ATTACKPOS, (1, 0))
        self.attackdisplayer = self.attacktext.imagify()
        #self.skilldisplayer:list[gui.ImageObj] = [m.imagify() for i, m in enumerate(self.skilltexts)]
        #???  ↓
        #self.skilltexts[6] = [gui.TextImagifier(game.screen, self.skillboard, game.font_big, constants.ATTACKHINT+str(self.attack), (0, 0, 0), constants.ATTACKPOS, (1, 0))]

    def receivedamage(self, damage: int, source: int, flags: list[int]):
        damage_t = damage
        sourcegroup = None if source == None else self.game.charlist[source].group
        if source != None:
            for b in self.game.charlist[source].buffs:
                if b.type == constants.Bufftype.INCREASEDAMAGEMADE:
                    if self.game.calbool(b.condition, source=source, damage=damage_t, flags=flags):
                        damage_t = self.game.calcnum(b.increment, damage=damage_t, charself=source)
                        b.usetime -= 1
            self.game.charlist[source].updatebuff()
        self.game.handleevent((constants.EventType.DAMAGEMADE, self.seq, source), source=source, damage=damage_t, receiver=self.seq)
        for b in self.buffs:
            if b.type == constants.Bufftype.DECREASEDAMAGERECEIVED:
                if self.game.calbool(b.condition, source=source, damage=damage_t, flags=flags, group=sourcegroup, charself=self.seq):
                    damage_t = self.game.calcnum(b.decrement, damage=damage_t)
                    b.usetime -= 1
        if constants.AttackFlags.SKIPSHIELD in flags:
            damage_aftershield = damage_t
        else:
            if self.shield >= damage_t:
                damage_aftershield = 0
                self.shield -= damage_t
            else:
                damage_aftershield = damage_t-self.shield
                self.shield = 0
        if self.summons == []:
            self._health -= damage_aftershield
        else:
            remaining_damage = damage_aftershield
            while remaining_damage > 0 and len(self.summons) > 0:
                health_temp = self.summons[-1].health
                self.summons[-1].health -= remaining_damage
                remaining_damage -= health_temp
                if self.summons[-1].health <= 0:
                    s = self.summons.pop()
                    for b in s.additionalbuff:
                        self.buffs.remove(b)
                    self.game.executeeffects(s.on_death, charself=self.seq)
        self.updatebuff()
        if not constants.AttackFlags.NOEVENT in flags:
            self.game.handleevent((constants.EventType.HURTED, self.seq), source=source, damage=damage_t)
        self.health = self._health

    def updatebuff(self):
        k = []
        for buff in self.buffs:
            if buff.age != buff.lasttime and buff.usetime != 0:
                k.append(buff)
        self.buffs = k
        self.updatestatus()

    @property
    def health(self):
        return self._health
    
    @health.setter
    def health(self, h):
        self._health = h
        if self._health <= 0:
            self._health = 0
            if self.alive:
                self.alive = False
                self.game.handleevent((constants.EventType.DIE, self.seq))

    @property
    def attack(self):
        return self._attack
    
    @attack.setter
    def attack(self, value):
        self._attack = value

class Variableid:
    def __init__(self, varid:dict):
        self.vardata = varid
        t = varid['type']
        targetedtypes = [constants.VariableId.ATTACK, constants.VariableId.HEALTH, constants.VariableId.MARKS, constants.VariableId.SHIELD]
        doubletargetedtypes = [constants.VariableId.SKILLUSETIME]
        if t in targetedtypes:
            self.targeted = True
            self.doubletargeted = False
            self.target:Target = self.vardata['target']
        elif t in doubletargetedtypes:
            self.targeted = True
            self.doubletargeted = True
            self.target:Target = self.vardata['target']
        else:
            self.targeted = False
        self.concretized = False
        self.targetabs = None
        self.absolute = self.vardata.get("absolute", False)
    
    def copy(self):
        return Variableid(self.vardata)
        

class MathExpression:
    def __init__(self, exp:dict):
        self.operator = exp['operator']
        self.data = exp['data']


class BoolExpression:
    def __init__(self, exp:dict):
        self.operator = exp['operator']
        self.data = exp['data']
        if self.operator == constants.BoolJudgement.SPECIAL:
            self.specialid = exp['type']


class Game:
    def __init__(self, screen, root, font_big, font_small):
        self.screen = screen
        self.root = root
        self.font_big = font_big
        self.font_small = font_small
        with open(constants.INITIALIZEFILE) as itf:
            it = json.load(itf, object_hook=custom_decoder)
            self.charidlist:list[str] = it['chars']
            self.equipidlist:list[int] = it['equipment']
            self.initial_sceneid:str = it['scene']

        self.charlist:list[Char] = [Char(constants.CHARFILE[char], self, i) for i, char in enumerate(self.charidlist)]

        self.charavatarlist:list[gui.ImageObj] = [gui.ImageObj(screen, root, constants.CHARAVATARFILE.get(char, 'a'), constants.CHARPOSLIST[i], (0, 0), constants.S, True) for i, char in enumerate(self.charidlist)]
        self.charframelist:list[gui.ButtonObj] = [gui.ButtonObj(screen, root, constants.CHARFRAMEFILE, constants.CHARPOSLIST[i], (0, 0), constants.S, True) for i, char in enumerate(self.charidlist)]
        self.charframeonfightlist:list[gui.ButtonObj] = [gui.ButtonObj(screen, root, constants.CHARONFIGHTFRAMEFILE, constants.CHARPOSLIST[(0, 3)[i]], (0, 0), constants.S, True) for i in range(2)]
        self.chardecoratorlist:list[gui.MtpApprObj] = [gui.MtpApprObj(screen, root, 0, constants.CHARPOSLIST[i], (0, 0)) for i, char in enumerate(self.charidlist)]
        for i, deco in enumerate(self.chardecoratorlist):
            deco.setimagelist(constants.CHARDECORATORFILELIST, 2, [(deco.rect.center, (0, 0), constants.S, True)]*len(constants.CHARDECORATORFILELIST))
            deco.start()
        self.generate_char_states()
        self.charnamelist:list[gui.ImageObj] = [gui.TextImagifier(screen, root, font_big, char.name, (0, 0, 0), constants.CHARNAMEPOSLIST[i], (1 if i <= 2 else -1, -1)).imagify() for i, char in enumerate(self.charlist)]

        self.equiplist:list[Equipment] = [Equipment(constants.EQUIPMENTFILE[equip], self, i) for i, equip in enumerate(self.equipidlist)]
        self.equipframelist:list[gui.ButtonObj] = [gui.ButtonObj(screen, root, constants.EQUIPMENTFRAMEFILE, constants.EQUIPMENTPOSLIST[i], (0, 0), constants.S, True) for i, equip in enumerate(self.equipidlist)]
        self.equippicturelist:list[gui.ImageObj] = [gui.ImageObj(screen, root, constants.EQUIPMENTPICTUREFILE[equip], constants.EQUIPMENTPOSLIST[i], (0, 0), constants.S, True) for i, equip in enumerate(self.equipidlist)]
        self.equipdecoratorlist:list[gui.MtpApprObj] = [gui.MtpApprObj(screen, root, 0, constants.EQUIPMENTPOSLIST[i], (0, 0)) for i, equip in enumerate(self.equipidlist)]
        for i, deco in enumerate(self.equipdecoratorlist):
            deco.setimagelist(constants.EQUIPMENTDECORATORFILELIST, 2, [(deco.rect.center, (0, 0), constants.S, True)]*len(constants.EQUIPMENTDECORATORFILELIST))
            deco.start()

        self.scenes:dict[str, Scene] = {scene:Scene(constants.SCENEFILE[scene], self) for i, scene in enumerate(constants.SCENEIDLIST)}
        self.currentscene:Scene = self.scenes[self.initial_sceneid]

        self.endturnbutton = gui.ButtonObj(screen, root, constants.ENDTURNBUTTONFILE, constants.ENDTURNBUTTONPOS, (0, 0), constants.S, True)
        self.informationbutton = gui.ButtonObj(screen, root, constants.INFORMATIONBUTTONFILE, constants.INFORMATIONBUTTONPOS, (0, 0), constants.S, True)

        self.roundimagifier = gui.TextImagifier(screen, root, font_big, constants.ROUNDHINT[0] + str(1) + constants.ROUNDHINT[1], (0, 0, 0), constants.ROUNDPOS, (0, 1))
        self.roundshow = self.roundimagifier.imagify()
        self.turnshowlist:list[gui.ImageObj] = [gui.TextImagifier(screen, root, font_small, constants.TURNHINT[i], (0, 0, 0), constants.TURNPOS, (0, 1)).imagify() for i in range(2)]
        self.turnshowing = self.turnshowlist[0]

        self.ingameretrybutton = gui.ButtonObj(screen, root, constants.INGAMERETRYBUTTONFILE, constants.INGAMERETRYBUTTONPOS, (0, 1), constants.S, True)

        self.onfightl = 0
        self.onfightr = 3
        self.rounds = 1
        self.turns = 0
        #If turns is even, the left acts; if turns is odd, the right acts
        self.chose = -1
        self.chosetype = -1
        self.displaymode = 0
        '''
         - 0: attack and skills
         - 1: status
        '''

        self.attacktime = 1
        self.skilltime = 0
        # 第一回合先手不能使用技能
        self.switchchartime = 1
        self.useequiptime = 1
        self.specialvars = {}
        self.environmentalbuff:list[Buff] = []

        self.animations:list[gui.MtpApprObj] = []


        self.mask = gui.ImageObj(screen, root, constants.MASKFILE, (0, 0), size=constants.SCREENSIZE, alpha=True)
        self.winblock = gui.ImageObj(screen, root, constants.WINBLOCKFILE, constants.WINBLOCKPOS, (0, 0), constants.S, True)
        self.wintext = [gui.TextImagifier(screen, root, font_big, constants.WINTEXT[i], (0, 0, 0), constants.WINTEXTPOS, (0, 1)).imagify() for i in range(2)]
        self.winretrybutton = gui.ButtonObj(screen, root, constants.WINRETRYBUTTONFILE, constants.WINRETRYBUTTONPOS, (0, 0), constants.S, True)
        self.winexitbutton = gui.ButtonObj(screen, root, constants.WINEXITBUTTONFILE, constants.WINEXITBUTTONPOS, (0, 0), constants.S, True)

        self.sureblock = gui.ImageObj(screen, root, constants.WINBLOCKFILE, constants.WINBLOCKPOS, (0, 0), constants.S, True)
        self.suretext = gui.TextImagifier(screen, root, font_big, constants.SURETEXT, (0, 0, 0), constants.WINTEXTPOS, (0, 1)).imagify()
        self.suresurebutton = gui.ButtonObj(screen, root, constants.SURESUREBUTTONFILE, constants.WINRETRYBUTTONPOS, (0, 0), constants.S, True)
        self.surecancelbutton = gui.ButtonObj(screen, root, constants.SURECANCELBUTTONFILE, constants.WINEXITBUTTONPOS, (0, 0), constants.S, True)

        self.chooseblock = gui.ImageObj(screen, root, constants.CHOOSEBLOCKFILE, constants.CHOOSEBLOCKPOS, (0, 0), constants.S, True)
        self.choosetext = gui.TextImagifier(screen, root, font_big, constants.CHOOSETEXT, (0, 0, 0), constants.CHOOSETEXTPOS, (0, 1)).imagify()
        self.choosesurebutton = gui.ButtonObj(screen, root, constants.SURESUREBUTTONFILE, constants.CHOOSEYESBUTTONPOS, (0, 0), constants.S, True)
        self.choosecancelbutton = gui.ButtonObj(screen, root, constants.SURECANCELBUTTONFILE, constants.CHOOSENOBUTTONPOS, (0, 0), constants.S, True)

        self.gameend = False
        self.winner = -1
        self.new = False

        self.choosecharavatarlist:list[gui.ImageObj] = [gui.ImageObj(screen, root, constants.CHARAVATARFILE.get(char, 'a'), constants.CHOOSECHARPOSLIST[i], (0, 0), constants.S, True) for i, char in enumerate(self.charidlist)]
        self.choosecharframelist:list[gui.ButtonObj] = [gui.ButtonObj(screen, root, constants.CHARFRAMEFILE, constants.CHOOSECHARPOSLIST[i], (0, 0), constants.S, True) for i, char in enumerate(self.charidlist)]
        self.choosechardecoratorlist:list[gui.MtpApprObj] = [gui.MtpApprObj(screen, root, 0, constants.CHOOSECHARPOSLIST[i], (0, 0)) for i, char in enumerate(self.charidlist)]
        for i, deco in enumerate(self.choosechardecoratorlist):
            deco.setimagelist(constants.CHARDECORATORFILELIST, 2, [(deco.rect.center, (0, 0), constants.S, True)]*len(constants.CHARDECORATORFILELIST))
            deco.start()

        self.choosecondition: bool|BoolExpression = True
        self.choosecount:int = 1
        self.availablechoice:list[int] = [0, 1, 2, 3, 4, 5]
        self.choselist:list[int] = []
        self.stack:list = [0]
        '''
         - 0: common game
         - 1: win
         - 2: sure ending round
         - 3: choose
         - 4: info
        '''

        for i, char in enumerate(self.charlist):
            for m in char.skills:
                if m.skilltype == constants.SkillType.PASSIVE:
                    self.executeeffects(m.effects, i)
        for i, char in enumerate(self.charlist):
            char.update()
        for i, equip in enumerate(self.equiplist):
            equip.update(self)
        self.updatedecorator()

    def inturncharseqs(self) -> list[int]:
        return [[0, 1, 2], [3, 4, 5]][self.turns%2]

    def displaysingle(self, obj: gui.ImageObj):
        obj.draw()
        obj.drawn = True

    def displaylist(self, objlist):
        for obj in objlist:
            self.displaysingle(obj)

    def displayall(self):
        for layoutid in self.stack:
            if layoutid == 0:
                if constants.SHOWSCENEBACKGROUND:
                    self.displaysingle(self.currentscene.bgimage)
                self.displaylist(self.charframelist)
                self.displaylist(self.charframeonfightlist)
                self.displaylist(self.charavatarlist)
                self.displaylist(self.chardecoratorlist)
                self.displaylist(self.charhealthlist)
                self.displaylist(self.charshieldlist)
                self.displaylist(self.charnamelist)
                self.displaylist(self.charsummonedhealthlist)
                self.displaylist(self.equipframelist)
                self.displaylist(self.equippicturelist)
                self.displaylist(self.equipdecoratorlist)

                if self.chosetype == 1:
                    if self.displaymode == 0:
                        self.displaylist(self.charlist[self.chose].skilldisplayer)
                        self.displaysingle(self.charlist[self.chose].attackdisplayer)
                        self.displaylist(self.charlist[self.chose].changingdisplayer)
                    elif self.displaymode == 1:
                        self.displaysingle(self.charlist[self.chose].statusdisplayer)
                    self.displaysingle(self.informationbutton)
                elif self.chosetype == 2:
                    self.displaylist(self.equiplist[self.chose].infodisplayer)
                    self.displaylist(self.equiplist[self.chose].changingdisplayer)

                self.displaysingle(self.endturnbutton)
                self.displaysingle(self.roundshow)
                self.displaysingle(self.turnshowing)
                self.displaylist(self.animations)

                if self.gameend:
                    self.displaysingle(self.ingameretrybutton)

            if layoutid == 1:
                self.mask.draw()
                self.winblock.draw()
                self.wintext[self.winner].draw()
                self.winretrybutton.draw()
                self.winexitbutton.draw()

            if layoutid == 2:
                self.mask.draw()
                self.sureblock.draw()
                self.surecancelbutton.draw()
                self.suresurebutton.draw()
                self.suretext.draw()

            if layoutid == 3:
                self.mask.draw()
                self.chooseblock.draw()
                self.choosecancelbutton.draw()
                self.choosesurebutton.draw()
                self.choosetext.draw()
                for i in self.availablechoice:
                    self.choosecharframelist[i].draw()
                    self.choosecharavatarlist[i].draw()
                    self.choosechardecoratorlist[i].draw()

    def detectclick(self, pos):
        layoutid = self.stack[-1]
        if layoutid == 0:
            for i, frame in enumerate(self.charframelist):
                if frame.surveil(pos):
                    if (self.chose, self.chosetype) == (i, 1):
                        self.chose = -1
                        self.chosetype = -1
                        self.updatedecorator()
                    elif self.charlist[i].alive:
                        self.chose = i
                        self.chosetype = 1
                        self.updatedecorator()
                        self.charlist[i].updatestatus()
            for i, frame in enumerate(self.equipframelist):
                if frame.surveil(pos):
                    if (self.chose, self.chosetype) == (i, 2):
                        self.chose = -1
                        self.chosetype = -1
                        self.updatedecorator()
                    elif self.equiplist[i].usetime > 0:
                        self.chose = i
                        self.chosetype = 2
                        self.updatedecorator()
            if self.chosetype == 1:
                chosechar = self.charlist[self.chose]
                if chosechar.attackbutton.drawn:
                    if chosechar.attackbutton.surveil(pos):
                        self.common_attack(chosechar)
                for i, m in enumerate(chosechar.useskillbuttons):
                    if m.drawn:
                        if m.surveil(pos):
                            sk = chosechar.skills[i]
                            if sk.choose:
                                self.initialize_choose_skill(i, chosechar, sk)
                                return
                            self.use_skill(chosechar, sk)
                if chosechar.switchcharbutton.drawn:
                    if chosechar.switchcharbutton.surveil(pos):
                        if self.turns%2 == 0:
                            originalchose = self.onfightl
                            self.onfightl = self.chose
                            self.charframeonfightlist[0].rect.center = constants.CHARPOSLIST[self.chose]
                        elif self.turns%2 == 1:
                            originalchose = self.onfightr
                            self.onfightr = self.chose
                            self.charframeonfightlist[1].rect.center = constants.CHARPOSLIST[self.chose]
                        self.switchchartime -= 1
                        self.handleevent((constants.EventType.SWITCH, (originalchose, self.chose)))
            if self.chosetype == 2:
                choseequip = self.equiplist[self.chose]
                if choseequip.useequipbutton.drawn:
                    if choseequip.useequipbutton.surveil(pos):
                        if choseequip.choose:
                            self.initialize_choose_equip(choseequip)
                            return
                        self.use_equipment(choseequip)
            if self.endturnbutton.surveil(pos):
                if self.attacktime > 0:
                    self.stack.append(2)
                else:
                    self.endturn()     
            if self.informationbutton.surveil(pos):
                self.displaymode = [1, 0][self.displaymode]
            if self.ingameretrybutton.drawn:
                if self.ingameretrybutton.surveil(pos):
                    self.retry()
            for a in self.charlist:
                a.update()
            for a in self.equiplist:
                a.update(self)
        elif layoutid == 1:
            if self.winretrybutton.surveil(pos):
                self.retry()
            elif self.winexitbutton.surveil(pos):
                self.stack.pop()
        elif layoutid == 2:
            if self.suresurebutton.surveil(pos):
                self.endturn()
                self.stack.pop()
            elif self.surecancelbutton.surveil(pos):
                self.stack.pop()
        elif layoutid == 3:
            if self.choosesurebutton.surveil(pos):
                if len(self.choselist) == self.choosecount:
                    if self.choosetype == 1:
                        self.use_skill(self.chooseskillcharseri, self.chooseskill, chose=self.choselist)
                    elif self.choosetype == 2:
                        self.use_equipment(self.chooseequip, chose=self.choselist)
                    self.stack.pop()
            elif self.choosecancelbutton.surveil(pos):
                self.stack.pop()
            else:
                for i, ava in enumerate(self.choosecharframelist):
                    if i in self.availablechoice:
                        if ava.surveil(pos):
                            if self.choosecount == 1:
                                for j, deco in enumerate(self.choosechardecoratorlist):
                                    deco.setappr(0)
                                self.choselist = [i]
                                self.choosechardecoratorlist[i].setappr(2)
                            else:
                                if i in self.choselist:
                                    self.choselist.remove(i)
                                    self.choosechardecoratorlist[i].setappr(0)
                                else:
                                    self.choselist.append(i)
                                    self.choosechardecoratorlist[i].setappr(2)

    def common_attack(self, chosechar:Char):
        commonattackdict = {"type": 1, "target": Target({"type": constants.Target.ENEMYONFIGHT}), "damage": chosechar.absattack, "flags": [constants.AttackFlags.COMMONATTACK]}
        self.executeeffects(EffectSet([Effect(**commonattackdict)]), self.chose)
        follow_attack_dict = {"type": 1, "target": Target({"type": constants.Target.ENEMYONFIGHT}), "damage": 0, "source": {"None": True}}
        for summoned in chosechar.summons:
            if summoned.follow_attack:
                follow_attack_dict['damage'] = summoned.attack
                self.executeeffects(EffectSet([Effect(**follow_attack_dict)]), self.chose)
        self.attacktime -= 1
        self.handleevent((constants.EventType.ATTACK, self.chose))
        self.updatedecorator()

    def use_equipment(self, choseequip:Equipment, **kw):
        self.executeeffects(choseequip.effects, [self.onfightl, self.onfightr][self.turns%2], **kw)
        self.handleevent((constants.EventType.EQUIP, self.chose))
        choseequip.usetime -= 1
        self.useequiptime -= 1
        self.chosetype = -1
        self.chose = -1
        self.updatedecorator()

    def initialize_choose_skill(self, seq:int, chosechar:Char, sk:Skill):
        for j, deco in enumerate(self.choosechardecoratorlist):
            deco.setappr(0)
        self.stack.append(3)
        self.choosetype = 1
        self.choselist = []
        self.chooseskill = sk
        self.chooseskillseri = seq
        self.chooseskillcharseri = chosechar
        self.choosecondition = sk.choosecondition
        self.choosearea = sk.choosearea.concretize(self, charself=chosechar.seq)
        self.choosecount = sk.choosecount
        self.availablechoice = []
        for j in self.choosearea:
            if self.calbool(self.choosecondition, iterchar=j):
                self.availablechoice.append(j)                    

    def initialize_choose_equip(self, equip:Equipment):
        for j, deco in enumerate(self.choosechardecoratorlist):
            deco.setappr(0)
        self.stack.append(3)
        self.choosetype = 2
        self.choselist = []
        self.chooseequip = equip
        self.choosecondition = equip.choosecondition
        self.choosearea = equip.choosearea.concretize(self, charself=equip.seq//2)
        self.choosecount = equip.choosecount
        self.availablechoice = []
        for j in self.choosearea:
            if self.calbool(self.choosecondition, iterchar=j):
                self.availablechoice.append(j)                    

    def use_skill(self, char:Char, sk:Skill, **kw):
        self.executeeffects(sk.effects, self.chose, **kw)
        if sk.skilltype == constants.SkillType.ACTIVEAGGRESSIVE:
            self.attacktime -= 1
            self.skilltime -= 1
        elif sk.skilltype == constants.SkillType.ACTIVENONAGGRESSIVE:
            self.skilltime -= 1
        if not sk.infinite:
            sk.usetime -= 1
        char.update()
        self.handleevent((constants.EventType.SKILL, self.chose))
        '''if sk.animation != None:
                                self.animations.append(sk.animation)
                                sk.animation.start()'''
        self.updatedecorator()

    def endturn(self):
        self.newturn()
        self.handleevent((constants.EventType.TURNSWITCH, self.turns%2))
        self.chose = -1
        self.chosetype = -1

    def retry(self):
        self.new = True

    def updatedecorator(self):
        for i, char in enumerate(self.charlist):
            if char.alive == False:
                self.chardecoratorlist[i].setappr(1)
            elif (self.chose, self.chosetype) == (i, 1):
                self.chardecoratorlist[i].setappr(2)
            else:
                self.chardecoratorlist[i].setappr(0)
        for i, equip in enumerate(self.equiplist):
            if equip.usetime <= 0:
                self.equipdecoratorlist[i].setappr(1)
            elif (self.chose, self.chosetype) == (i, 2):
                self.equipdecoratorlist[i].setappr(2)
            else:
                self.equipdecoratorlist[i].setappr(0)

    def updateanimations(self):
        na = []
        for i, anim in enumerate(self.animations):
            if anim.next() != 0:
                na.append(anim)
        self.animations = na

    def update(self):
        self.generate_char_states()
        for a in self.charlist:
            for b in a.buttons:
                b.drawn = False
        for a in self.equiplist:
            for b in a.allrelatingobjs:
                b.drawn = False
        self.informationbutton.drawn = False
        self.ingameretrybutton.drawn = False
        self.winblock.drawn = False
        self.wintext[0].drawn = False
        self.wintext[1].drawn = False
        self.winretrybutton.drawn = False
        self.winexitbutton.drawn = False
        self.displayall()

    def generate_char_states(self):
        self.charhealthlist:list[gui.ImageObj] = [gui.TextImagifier(self.screen, self.root, self.font_big, str(char.health), (0, 0, 0), constants.CHARHEALTHPOSLIST[i], (1 if i <= 2 else -1, 1)).imagify() for i, char in enumerate(self.charlist)]
        self.charshieldlist:list[gui.ImageObj] = [gui.TextImagifier(self.screen, self.root, self.font_big, str(char.shield) if char.shield > 0 else '', (128, 128, 128), constants.CHARSHIELDPOSLIST[i], (1 if i <= 2 else -1, 1)).imagify() for i, char in enumerate(self.charlist)]
        self.charsummonedhealthlist:list[gui.ImageObj] = [gui.TextImagifier(self.screen, self.root, self.font_big, str(k) if (k:=len(char.summons)) > 0 else '', (96, 86, 47), constants.CHARSUMMONEDPOSLIST[i], (1 if i <= 2 else -1, 1)).imagify() for i, char in enumerate(self.charlist)]

    def executeeffect(self, effect:Effect, charself = None, **kw):
        if effect.effecttype == constants.EffectType.DEBUG_PRINT:
            print(effect.message)
        elif effect.effecttype == constants.EffectType.DAMAGE:
            target = effect.target.concretize(self, charself=charself, **kw)
            if effect.source == None:
                so = charself
            elif effect.source.get('None') == True:
                so = None
            else:
                so = effect.source['data'].concretize(self, charself=charself, **kw)
            for a in target:
                self.charlist[a].receivedamage(self.calcnum(effect.damage, charself=charself, **kw), so, effect.flags)
                #self.charlist[a].receivedamage(self.calcnum(effect.damage, charself=charself, receiver=a, **kw), so, effect.flags)
        elif effect.effecttype == constants.EffectType.HEAL:
            target = effect.target.concretize(self, charself=charself, **kw)
            for a in target:
                char = self.charlist[a]
                if char.health < char.maxhealth:
                    char.health += self.calcnum(effect.value, charself=charself, **kw)
                    char.health = min(char.health, char.maxhealth)
        elif effect.effecttype == constants.EffectType.SET:
            if not effect.variableid.targeted:
                original = self.getvariable(effect.variableid)
                self.setvariable(effect.variableid, self.calcnum(effect.value, charself=charself, **kw, original=original))
            else:
                var_x = effect.variableid.copy()
                for tar in effect.variableid.target.concretize(self, charself=charself, **kw):
                    var_x.concretized = True
                    var_x.targetabs = tar
                    original = self.getvariable(var_x)
                    self.setvariable(var_x, self.calcnum(effect.value, charself=charself, **kw, original=original))
        elif effect.effecttype == constants.EffectType.INCREASE:
            if not effect.variableid.targeted:
                self.setvariable(effect.variableid, self.getvariable(effect.variableid) + self.calcnum(effect.increment, charself=charself, **kw))
            else:
                var_x = effect.variableid.copy()
                var_x.absolute = True
                for tar in effect.variableid.target.concretize(self, charself=charself, **kw):
                    var_x.concretized = True
                    var_x.targetabs = tar
                    self.setvariable(var_x, self.getvariable(var_x) + self.calcnum(effect.increment, charself=charself, **kw))
        elif effect.effecttype == constants.EffectType.BUFF:
            target = effect.target.concretize(self, charself=charself, **kw)
            for a in target:
                self.charlist[a].buffs.append(effect.buff.copy())
        elif effect.effecttype == constants.EffectType.BUFFCLEAR:
            target = effect.target.concretize(self, charself=charself, **kw)
            for a in target:
                k = []
                if effect.clear_type == constants.BuffClearType.POSITIVITY:
                    for b in self.charlist[a].buffs:
                        if b.positivity not in effect.positivities:
                            k.append(b)
                elif effect.clear_type == constants.BuffClearType.IDENTIFICATION:
                    for b in self.charlist[a].buffs:
                        if b.identification != effect.identification:
                            k.append(b)
                self.charlist[a].buffs = k
        elif effect.effecttype == constants.EffectType.ENVIRONMENTALBUFF:
            self.environmentalbuff.append(effect.buff.copy())
        elif effect.effecttype == constants.EffectType.KILL:
            for i in effect.target.concretize(self, charself=charself, **kw):
                self.charlist[i].health = 0
                self.charlist[i].alive = False
        elif effect.effecttype == constants.EffectType.RANDOM:
            r = random.random()
            for p, e in zip(effect.probabilities, effect.effects):
                if r <= p:
                    self.executeeffects(EffectSet(e), charself=charself, **kw)
                    break
        elif effect.effecttype == constants.EffectType.SUMMON:
            target = effect.target.concretize(self, charself=charself, **kw)
            for a in target:
                if self.charlist[a].alive:
                    s = effect.summoned.copy()
                    self.charlist[a].summons.append(s)
                    for b in s.additionalbuff:
                        self.charlist[a].buffs.append(b)
        elif effect.effecttype == constants.EffectType.REVIVE:
            target = effect.target.concretize(self, charself=charself, **kw)
            for a in target:
                self.charlist[a].health = effect.revivehealth
                self.charlist[a].alive = True
        elif effect.effecttype == constants.EffectType.SWITCHSCENE:
            self.currentscene = self.scenes[effect.scene].copy()
            self.executeeffects(self.currentscene.effects_instant, charself=charself, **kw)
        elif effect.effecttype == constants.EffectType.DESPOIL:
            var_s = effect.despoil_from.copy()
            var_s.absolute = True
            var_s.concretized = True
            var_s.targetabs = var_s.target.concretize(self, charself=charself, **kw)[0]
            var_r = effect.despoil_to.copy()
            var_r.absolute = True
            var_r.concretized = True
            var_r.targetabs = var_r.target.concretize(self, charself=charself, **kw)[0]
            source_value = self.calcnum(var_s, charself=charself, **kw)
            transfer_value = min(self.calcnum(effect.value, charself=charself, **kw), source_value)
            self.setvariable(var_s, source_value - transfer_value)
            self.setvariable(var_r, self.getvariable(var_r) + transfer_value)
        elif effect.effecttype == constants.EffectType.SPECIFIC:
            self.handle_special_effects(effect, charself, kw)
        else:
            raise ValueError(f'Invalid effecttype:{effect.effecttype}')

    def handle_special_effects(self, effect:Effect, charself, kw):
        if effect.specific == constants.EffectType.Specific.ZHH:
            equipseqs = [range(6, 12), range(0, 6)][self.turns%2]
            validequipseq = []
            for i in equipseqs:
                if self.equiplist[i].usetime > 0:
                    validequipseq.append(i)
            if len(validequipseq) > 0:
                self.equiplist[random.choice(validequipseq)].usetime = 0
        elif effect.specific == constants.EffectType.Specific.LB_2:
            enemy_alive = Target({"type": constants.Target.ENEMYALL, "restrict_alive": True}).concretize(self).copy()
            if len(enemy_alive) >= 2:
                on_fight = self.on_fight[(self.turns+1)%2]
                enemy_alive.remove(on_fight)
                m = self.on_fight.copy()
                m[(self.turns+1)%2] = random.choice(enemy_alive)
                self.on_fight = m
            else:
                pass
        elif effect.specific == constants.EffectType.Specific.LB_3:
            chose = kw['chose'][0]
            m = self.on_fight.copy()
            m[(self.turns+1)%2] = chose
            self.on_fight = m
        elif effect.specific == constants.EffectType.Specific.CAT:
            eqs = []
            for i in range(2):
                if self.equiplist[charself*2+i].usetime == 0:
                    eqs.append(charself*2+i)
            if len(eqs) == 0:
                return
            eq = random.choice(eqs)
            self.equiplist[eq].usetime += 1
        else:
            raise ValueError(f'Invalid specific:{effect.specific}')

    def executeeffects(self, effects:EffectSet, charself = None, **kw):
        for effect in effects.effects:
            if self.calbool(effect.condition, charself=charself, **kw):
                self.executeeffect(effect, charself, **kw)
        self.checkdeath()

    def processevent(self, event:tuple, charseq:int) -> list[int]:
        '''
        Calculates the EventTime for one specific character based on the event and the character's sequence number.
        Parameters:
        - event (tuple): A tuple containing the event type and its associated data.
        - charseq (int): The sequence number of the character.
        Returns:
        - list[int]: A list of EventTime values that are relevant for the character.
        '''
        if event[0] == constants.EventType.ATTACK:
            return [constants.EventTime.COMMONATTACK] if event[1] == charseq else []
        if event[0] == constants.EventType.HURTED:
            return [constants.EventTime.GETHURTED] if event[1] == charseq else []
        if event[0] == constants.EventType.SKILL:
            if event[1] == charseq:
                return [constants.EventTime.USESKILL]
            return []
        if event[0] == constants.EventType.SWITCH:
            if event[1][0] in self.inturncharseqs():
                if event[1][0] == charseq:
                    return [constants.EventTime.SWITCHFROM, constants.EventTime.WESWITCH]
                if event[1][1] == charseq:
                    return [constants.EventTime.SWITCHTO, constants.EventTime.WESWITCH]
                return [constants.EventTime.WESWITCH]
            return [constants.EventTime.ENEMYSWITCH]
        if event[0] == constants.EventType.TURNSWITCH:
            if event[1] == (0 if charseq in [0, 1, 2] else 1):
                return [constants.EventTime.TURNSTART]
            return [constants.EventTime.TURNEND]
        if event[0] == constants.EventType.DAMAGEMADE:
            resl = []
            if event[2] == charseq:
                resl.append(constants.EventTime.MAKEDAMAGE)
            if event[1] == charseq:
                resl.append(constants.EventTime.GETDAMAGED)
            return resl
        if event[0] == constants.EventType.EQUIP:
            if event[1] // 2 == charseq:
                return [constants.EventTime.USEEQUIP, constants.EventTime.WEEQUIP]
            elif event[1] // 2 in [[0, 1, 2], [3, 4, 5]][charseq//3]:
                return [constants.EventTime.WEEQUIP]
            else:
                return [constants.EventTime.ENEMYEQUIP]
        if event[0] == constants.EventType.DIE:
            if event[1] == charseq:
                return [constants.EventTime.SELFDIE, constants.EventTime.OWNSIDEDIE]
            elif event[1] // 2 in [[0, 1, 2], [3, 4, 5]][charseq//3]:
                return [constants.EventTime.OWNSIDEDIE]
            else:
                return [constants.EventTime.ENEMYDIE]
        raise ValueError(f'Invalid event type:{event[0]}')
            
    def handleevent(self, event:tuple, **kw):
        for i, char in enumerate(self.charlist):
            et =  self.processevent(event, i)
            for buff in char.buffs:
                if buff.type == constants.Bufftype.EFFECT:
                    if buff.eventtime in et:
                        if self.calbool(buff.condition, charself=i, age=buff.age, **kw):
                            buff.usetime -= 1
                            self.executeeffects(buff.effects, charself=i, age=buff.age, **kw)
            char.updatebuff()

    def newturn(self):
        self.turns += 1
        if self.turns%2 == 0:
            self.rounds += 1
        self.chose = -1
        self.chosetype = -1
        self.updatedecorator()
        self.attacktime = 1
        self.skilltime = 1
        self.switchchartime = 1
        self.useequiptime = 1
        self.roundimagifier.text = (constants.ROUNDHINT[0] + str(self.rounds) + constants.ROUNDHINT[1])
        self.roundshow = self.roundimagifier.imagify()
        self.turnshowing = self.turnshowlist[self.turns%2]
        for i, char in enumerate(self.charlist):
            k = []
            for buff in char.buffs:
                buff.age += 1
                if buff.age != buff.lasttime:
                    k.append(buff)
            char.buffs = k
        k = []
        for buff in self.environmentalbuff:
            buff.age += 1
            if buff.age != buff.lasttime and buff.usetime != 0:
                k.append(buff)
        self.environmentalbuff = k
        for buff in self.environmentalbuff:
            if buff.type == constants.Bufftype.EFFECT:
                if self.calbool(buff.condition, age=buff.age):
                    buff.usetime -= 1
                    self.executeeffects(buff.effects, age=buff.age)
        self.checkdeath()

    def getvariable(self, varid:Variableid):
        d = varid.vardata
        dt = d['type']
        if dt == constants.VariableId.SPECIALVARIABLE:
            return self.specialvars.get(d['varname'], 0)
        if dt == constants.VariableId.SKILLTIME:
            return self.skilltime
        if dt == constants.VariableId.SWITCHCHARTIME:
            return self.switchchartime
        if dt == constants.VariableId.ATTACKTIME:
            return self.attacktime
        if dt == constants.VariableId.ROUND:
            return self.rounds
        if dt == constants.VariableId.ATTACK:
            return getattr(self.charlist[varid.targetabs], "attack" if varid.absolute else "absattack")
        if dt == constants.VariableId.HEALTH:
            return self.charlist[varid.targetabs].health
        if dt == constants.VariableId.SHIELD:
            return self.charlist[varid.targetabs].shield
        if dt == constants.VariableId.MARKS:
            return self.charlist[varid.targetabs].marks.get(d['mark'], 0)
        if dt == constants.VariableId.SKILLUSETIME:
            return self.charlist[varid.targetabs].skills[varid.vardata['serial']].usetime
        raise ValueError(f'Invalid id:{dt}')
            
    def setvariable(self, varid:Variableid, value):
        d = varid.vardata
        dt = d['type']
        if dt == constants.VariableId.SPECIALVARIABLE:
            self.specialvars[d['varname']] = value
        elif dt == constants.VariableId.SKILLTIME:
            self.skilltime = value
        elif dt == constants.VariableId.SWITCHCHARTIME:
            self.switchchartime = value
        elif dt == constants.VariableId.ATTACKTIME:
            self.attacktime = value
        elif dt == constants.VariableId.ROUND:
            self.rounds = value
        elif dt == constants.VariableId.ATTACK:
            self.charlist[varid.targetabs].attack = value
        elif dt == constants.VariableId.HEALTH:
            self.charlist[varid.targetabs].health = value
        elif dt == constants.VariableId.SHIELD:
            self.charlist[varid.targetabs].shield = value
        elif dt == constants.VariableId.MARKS:
            self.charlist[varid.targetabs].marks[d['mark']] = value
        elif dt == constants.VariableId.SKILLUSETIME:
            char = self.charlist[varid.targetabs]
            skillindex = varid.vardata['serial']
            sk = char.skills[skillindex]
            sk.usetime = value
            char.update()
        else:
            raise ValueError(f'Invalid id:{dt}')
    
    def calcnum(self, cal:int|float|str|Target|MathExpression|Variableid, **vars) -> int|float:
        if type(cal) == int or type(cal) == float:
            return cal
        if type(cal) == str:
            if cal in vars.keys():
                return vars[cal]
            else:
                raise ValueError(f'Invalid key:{cal}')
        if type(cal) == MathExpression:
            dat = cal.data
            if cal.operator == constants.Calculator.CALLVARIABLE:
                return self.calcnum(dat, **vars)
            if cal.operator == constants.Calculator.ADD:
                return sum(map(lambda x: self.calcnum(x, **vars), dat))
            if cal.operator == constants.Calculator.SUB:
                return self.calcnum(dat[0], **vars) - self.calcnum(dat[1], **vars)
            if cal.operator == constants.Calculator.TIMES:
                return self.calcnum(dat[0], **vars) * self.calcnum(dat[1], **vars)
            if cal.operator == constants.Calculator.DIV:
                return self.calcnum(dat[0], **vars) / self.calcnum(dat[1], **vars)
            if cal.operator == constants.Calculator.MOD:
                return self.calcnum(dat[0], **vars) % self.calcnum(dat[1], **vars)
            if cal.operator == constants.Calculator.MAX:
                return max(map(lambda x: self.calcnum(x, **vars), dat))
            if cal.operator == constants.Calculator.MIN:
                return min(map(lambda x: self.calcnum(x, **vars), dat))
            if cal.operator == constants.Calculator.EXP:
                if len(dat) == 1:
                    return math.exp(self.calcnum(dat[0], **vars))
                return self.calcnum(dat[0], **vars) ** self.calcnum(dat[1], **vars)
            if cal.operator == constants.Calculator.LOG:
                if len(dat) == 1:
                    return math.log(self.calcnum(dat[0], **vars))
                return math.log(self.calcnum(dat[1], **vars), self.calcnum(dat[0], **vars))
            if cal.operator == constants.Calculator.ROUND:
                return round(self.calcnum(dat[0], **vars))
            if cal.operator == constants.Calculator.FLOOR:
                return math.floor(self.calcnum(dat[0], **vars))
            if cal.operator == constants.Calculator.CEIL:
                return math.ceil(self.calcnum(dat[0], **vars))
            if cal.operator == constants.Calculator.CALLSPECIALVARIABLE:
                if dat == 'living_count':
                    return len([1 for c in self.charlist if c.alive])
            if cal.operator == constants.Calculator.COUNT:
                count = 0
                for b in dat:
                    if self.calbool(b, **vars):
                        count += 1
                return count
            if cal.operator == constants.Calculator.LEN:
                return len(self.callist(dat[0], **vars))
            raise ValueError(f'Invalid operator:{cal.operator}')
        if type(cal) == Variableid:
            dat = cal
            m:Variableid = dat.copy()
            if not m.targeted:
                return self.getvariable(m)
            else:
                m.targetabs = m.target.concretize(self, **vars)[0]
                m.concretized = True
                return self.getvariable(m)
        if type(cal) == Target:
            return cal.concretize(self, **vars)[0]
        raise TypeError(f'Invalid type:{type(cal)}')
    
    def calbool(self, cal:bool|BoolExpression|str, **vars) -> bool:
        if type(cal) == bool:
            return cal
        if type(cal) == BoolExpression:
            dat = cal.data
            if cal.operator == constants.BoolJudgement.GREATER:
                return self.calcnum(dat[0], **vars) > self.calcnum(dat[1], **vars)
            if cal.operator == constants.BoolJudgement.GREATEROREQUAL:
                return self.calcnum(dat[0], **vars) >= self.calcnum(dat[1], **vars)
            if cal.operator == constants.BoolJudgement.LESS:
                return self.calcnum(dat[0], **vars) < self.calcnum(dat[1], **vars)
            if cal.operator == constants.BoolJudgement.LESSOREQUAL:
                return self.calcnum(dat[0], **vars) <= self.calcnum(dat[1], **vars)
            if cal.operator == constants.BoolJudgement.EQUAL:
                return self.calcnum(dat[0], **vars) == self.calcnum(dat[1], **vars)
            if cal.operator == constants.BoolJudgement.NOTEQUAL:
                return self.calcnum(dat[0], **vars) != self.calcnum(dat[1], **vars)
            if cal.operator == constants.BoolJudgement.AND:
                return self.calbool(dat[0], **vars) and self.calbool(dat[1], **vars)
            if cal.operator == constants.BoolJudgement.OR:
                return self.calbool(dat[0], **vars) or self.calbool(dat[1], **vars)
            if cal.operator == constants.BoolJudgement.XOR:
                return self.calbool(dat[0], **vars) != self.calbool(dat[1], **vars)
            if cal.operator == constants.BoolJudgement.NOT:
                print(dat[0], vars, self.calbool(dat[0], **vars))
                return not self.calbool(dat[0], **vars)
            if cal.operator == constants.BoolJudgement.IN:
                return self.calcnum(dat[0], **vars) in self.callist(dat[1], **vars)
            if cal.operator == constants.BoolJudgement.NOTIN:
                return self.calcnum(dat[0], **vars) not in self.callist(dat[1], **vars)
            if cal.operator == constants.BoolJudgement.ALIVE:
                return self.charlist[dat[0].concretize(self, **vars)[0]].alive
            if cal.operator == constants.BoolJudgement.GROUP:
                return self.charlist[dat[0].concretize(self, **vars)[0]].group == dat[1]
            if cal.operator == constants.BoolJudgement.SPECIAL:
                if cal.specialid == constants.BoolJudgement.Special.HAVEBUFF:
                    char = self.charlist[dat[0].concretize(self, **vars)[0]]
                    for b in char.buffs:
                        b:Buff
                        if b.positivity in dat[1]:
                            return True
                    return False
                if cal.specialid == constants.BoolJudgement.Special.EQUIPMENTUSED:
                    eqseri = dat[0].concretize(self, **vars)[0]*2
                    if tuple(map(lambda x:self.equiplist[x].usetime, [eqseri, eqseri+1])) == (0, 0):
                        return True
                    return False
                raise ValueError(f'Invalid special type:{cal.specialid}')
            raise ValueError(f'Invalid operator:{cal.operator}')
        if type(cal) == str:
            if vars.get(cal) != None:
                return vars[cal]
            else:
                raise ValueError(f'Invalid key:{cal}')
        raise TypeError(f'Invalid type:{type(cal)}')
        
    def callist(self, cal:list|str|Target, **vars) -> list:
        if type(cal) == str:
            if vars.get(cal) != None:
                return vars[cal]
            else:
                raise ValueError(f'Invalid key:{cal}')
        if type(cal) == Target:
            return cal.concretize(self, **vars)
        if type(cal) != list:
            raise TypeError(f'Invalid type:{type(cal)}')
        return [self.calcnum(i, **vars) for i in cal]
    
    def checkdeath(self):
        for char in self.charlist:
            char.health = char.health
        if self.charlist[self.onfightl].alive == False:
            for i in range(1, 3):
                if self.charlist[(self.onfightl+i)%3].alive == True:
                    self.onfightl = (self.onfightl+i)%3
                    self.charframeonfightlist[0].rect.center = constants.CHARPOSLIST[self.onfightl]
                    break
            else:
                self.gameend = True
                self.stack.append(1)
                self.winner = 1
                return
        if self.charlist[self.onfightr].alive == False:
            for i in range(1, 3):
                if self.charlist[3 + (self.onfightr+i)%3].alive == True:
                    self.onfightr = 3 + (self.onfightr+i)%3
                    self.charframeonfightlist[1].rect.center = constants.CHARPOSLIST[self.onfightr]
                    break
            else:
                self.gameend = True
                self.stack.append(1)
                self.winner = 0
                return

    @property
    def on_fight(self):
        return [self.onfightl, self.onfightr]
    
    @on_fight.setter
    def on_fight(self, value:list|tuple):
        self.onfightl = value[0]
        self.onfightr = value[1]
        self.charframeonfightlist[0].rect.center = constants.CHARPOSLIST[self.onfightl]
        self.charframeonfightlist[1].rect.center = constants.CHARPOSLIST[self.onfightr]

with open(constants.BUFFPATH, encoding='utf-8') as bpf:
    bp = json.load(bpf, object_hook=custom_decoder)
    bufflist = bp

debug_showallbuff = False
debug_showallmark = False
debug_print = True