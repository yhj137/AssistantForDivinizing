from copy import deepcopy
import itertools
import random

class DivinizingEnv():
    '''
        origin_xianxing: 初始仙性
        linggen: 金，木，水，火，土 五种灵根值列表
        is_xianti: 是否吃下混元仙体丹
        is_cuiti: 是否吃下天命淬体丹
        is_suhun: 是否吃下澄心塑魂丹

        state设计: 
            (0.当前行动状态(0:出牌,1:消散灵气,2.消耗灵气),
            1.当前仙凡状态(0:凡体,1:仙胎),
            2.当前灵根分布(5元组),
            3.五行化神(0.金 1.木 2.水 3.火 4.土),
            4.是否吃下混元仙体丹,
            5.是否吃下天命淬体丹,
            6.是否吃下澄心塑魂丹,
            7.当前回合数,
            8.当前灵气数(5元组),
            9.当前凡性,
            10.当前仙性,
            11.当前淬体,
            12.当前塑魂,
            13.当前定元咒层数,
            14.当前涌泉法层数,
            15.是否使用过忘凡咒,
            16.当前回合是否使用过化神,
            17.当前回合是否使用过化凡,
            18.当前回合是否使用过涌泉法,
            19.当前回合是否使用过意守法,
            20.当前回合是否使用过定元咒,
            21.当前回合是否使用过忘凡咒,
            22.当前释放技能,
            23.当前所需灵气(5元组),
            24.当前选中灵气(5元组))

        行为列表:
            0.结束回合
            1.选择1点金灵气
            2.选择1点木灵气
            3.选择1点水灵气
            4.选择1点火灵气
            5.选择1点土灵气
            6.使用灵气
            7.消散灵气
            8.使用化神:(3)【后继无力】【凡体】状态下方可使用.【仙性】+1并进入仙胎状态;每有【塑魂】*10,则【仙性】额外+1
            9.使用化凡:(2)【后继无力】【仙胎】状态下方可使用。进入凡体状态，每有【淬体】*10,则吸收一点灵气
            10.使用淬体法:(5)【淬体】+5。若处于【凡体】状态,则【淬体】额外+1
            11.使用塑魂法:(5)【塑魂】+5。若处于【仙胎】状态,则【塑魂】额外+2
            12.使用感应法:(3+1)【仙性】+3,若在【仙胎】状态下释放,则【仙性】额外+2
            13.使用涌泉法:(2+2)【后继无力】下回合开始时,吸收4点灵气。若在【仙胎】状态下释放,则【凡性】-3
            14.使用意守法:(3+2)【后继无力】下回合开始时若处于【仙胎】状态，则每有【仙性】*10,吸收一点灵气
            15.使用定元咒:(3+1)【后继无力】【凡体】状态下方可使用.下一次进入【仙胎】状态时,吸收4点灵气
            16.使用忘凡咒:(1+1)【后继无力】【仙胎】状态下方可使用.本回合结束时，若仍处于【仙胎】状态,则【凡性】-4.首次释放此技能时,效果翻倍.
            17.使用九龙天雷火:(2+1)使用相生的灵气释放时,【淬体】+3; 使用相克的灵气释放时,【塑魂】+3.

        游戏机制: 
            1.胜利条件: 当凡性达到100时,游戏失败;当仙性达到100时,游戏成功,淬体和塑魂越高越好。凡性先于仙性结算。
            2.【凡体】回合结束时，如果你处于【凡体】状态，【凡性】+4;回合开始时,如果你处于【凡体】状态,获得随机8点灵气
            3.【仙胎】回合开始时，如果你处于【仙胎】状态，【仙性】+4;跳过吸收灵气阶段.
            4.第n回合结束时,【凡性】增加n
            5.混元仙体丹:初始仙性+4
            6.天命淬体丹:每次淬体效果+1
            7.澄心塑魂丹:每次塑魂效果+1
            8.相生灵气:金-水, 水-木, 木-火, 火-土, 土-金
            9.相克灵气:金-木, 水-火, 木-土, 火-金, 土-水
            10.游戏从第1回合开始计算,处于【凡体】,初始拥有8点灵气
            11.灵气上限为6点,回合结束时若有多余的灵气需要消散到灵气上限
            12.灵气获取按照灵根分布概率抽取
            13.默认五行化神,每回合额外吸收一点相应灵气
    '''
    def __init__(self):#, origin_xianxing, linggen, is_xianti, is_cuiti, is_suhun):
        #self.origin_xianxing = origin_xianxing
        #self.linggen = linggen # list of the value of [jin, mu, shui, huo, tu]
        #self.is_xianti = is_xianti
        #self.is_cuiti = is_cuiti
        #self.is_suhun = is_suhun
        pass

    def _check_lingqi(self, lingqi, to_check, used_lingqi = (0,0,0,0,0)):            
        res = [False for i in range(5)]
        for i in itertools.permutations((0,1,2,3,4), len(to_check)):
            flag = True
            for j in range(len(to_check)):
                if used_lingqi[i[j]] != to_check[j]:
                    flag = False
                    break
            if flag:
                return res
        for i in itertools.permutations((0,1,2,3,4), len(to_check)):
            skip_flag = False
            for j in range(5):
                if used_lingqi[j] > 0 and j not in i:
                    skip_flag = True
                    break
            if skip_flag:
                continue
            flag = True
            for j in range(len(to_check)):
                #print(i,lingqi[i[j]] + used_lingqi[i[j]],to_check[j])
                if lingqi[i[j]] + used_lingqi[i[j]] < to_check[j] or used_lingqi[i[j]] > to_check[j]:
                    flag = False
            if flag == True:
                #print(i)
                for j in range(len(to_check)):
                    if lingqi[i[j]] > 0 and used_lingqi[i[j]] < to_check[j]:
                        res[i[j]] = True
                #return True
        return res


    def get_action_list(self, state):
        self.action_list = []
        if state[0] == 0:# 出牌
            if state[1] == 0:# 凡体
                if state[16] == 0 and sum(self._check_lingqi(state[8], (3,))):# 无化神
                    self.action_list.append(8)
                if state[20] == 0 and sum(self._check_lingqi(state[8], (3,1))):# 无定元
                    self.action_list.append(15)
            if state[1] == 1:#仙胎
                if state[17] == 0 and sum(self._check_lingqi(state[8], (2,))):# 无化凡
                    self.action_list.append(9)
                if state[21] == 0 and sum(self._check_lingqi(state[8], (1,1))):# 无忘凡
                    self.action_list.append(16)
            if sum(self._check_lingqi(state[8], (5,))):# 淬体, 塑魂
                self.action_list.append(10)
                self.action_list.append(11)
            if sum(self._check_lingqi(state[8], (3,1))):# 感应
                self.action_list.append(12)
            if state[18] == 0 and sum(self._check_lingqi(state[8], (2,2))):# 无涌泉
                self.action_list.append(13)
            if state[19] == 0 and sum(self._check_lingqi(state[8], (3,2))):# 无意守
                self.action_list.append(14)
            if sum(self._check_lingqi(state[8], (2,1))):# 九龙天雷火
                self.action_list.append(17)
            self.action_list.append(0)
        elif state[0] == 1: #消散灵气
            if sum(state[8]) <= 6:
                self.action_list.append(7)
            else:
                for i in range(5):
                    if state[8][i] > 0:
                        self.action_list.append(i+1)
        elif state[0] == 2: #消耗灵气
            #skill_list = {8:(3,),9:(2,),10:(5,),11:(5,),12:(3,1),13:(2,2),14:(3,2),15:(3,1),16:(1,1),17:(2,1)}
            to_check = []
            for i in range(5):
                if state[23][i] > 0:
                    to_check.append(state[23][i]) 
            avaluable_lingqi = self._check_lingqi(state[8], tuple(to_check), state[24])
            for i in range(len(avaluable_lingqi)):
                if avaluable_lingqi[i]:
                    self.action_list.append(i+1)
            if sum(avaluable_lingqi) == 0:
                self.action_list.append(6)
            pass
        self.action_list.sort()
        return self.action_list

    def _get_lingqi(self, state, num):
        p = [state[2][i]/sum(state[2]) for i in range(5)]
        now_lingqi = list(state[8])
        added_lingqi = random.choices(list(range(5)),weights=p,k=num)
        for i in added_lingqi:
            now_lingqi[i] += 1
        return tuple(now_lingqi)

    def get_next_state(self, state, action):
        temp_state = list(state)
        if action == 0:
            temp_state[0] = 1
        elif 1 <= action <= 5:
            now_lingqi = list(state[8])
            used_lingqi = list(state[24])
            now_lingqi[action-1] -= 1
            used_lingqi[action-1] += 1
            temp_state[8] = tuple(now_lingqi)
            temp_state[24] = tuple(used_lingqi)
        elif action == 6:
            if state[22] == 8: #化神
                temp_state[1] = 1
                temp_state[10] += (1 + state[12] // 10)
                temp_state[8] = self._get_lingqi(state, temp_state[13])
                temp_state[16] = 1
                temp_state[13] = 0
            elif state[22] == 9:#化凡
                temp_state[1] = 0
                temp_state[8] = self._get_lingqi(state, state[11]//10)
                temp_state[17] = 1
            elif state[22] == 10:#淬体法
                temp_state[11] += 5
                if state[1] == 0:
                    temp_state[11] += 1
                if state[5] == 1:
                    temp_state[11] += 1
            elif state[22] == 11:#塑魂法
                temp_state[12] += 5
                if state[1] == 1:
                    temp_state[12] += 2
                if state[6] == 1:
                    temp_state[12] += 1
            elif state[22] == 12:#感应法
                temp_state[10] += 3
                if state[1] == 1:
                    temp_state[10] += 2
            elif state[22] == 13:#涌泉法
                temp_state[14] += 4
                if state[1] == 1:
                    temp_state[9] -= 3
                temp_state[18] = 1
            elif state[22] == 14:#意守法
                temp_state[19] = 1
            elif state[22] == 15:#定元咒
                temp_state[13] += 4
                temp_state[20] = 1
            elif state[22] == 16:#忘凡咒
                temp_state[21] = 1
            elif state[22] == 17:#九龙天雷火
                if (state[24][0]>0 and state[24][2]> 0) or\
                    (state[24][2]>0 and state[24][1]> 0) or\
                    (state[24][1]>0 and state[24][3]> 0) or\
                    (state[24][3]>0 and state[24][4]> 0) or\
                    (state[24][4]>0 and state[24][0]> 0):
                    temp_state[11] += 3
                    if state[5] == 1:
                        temp_state[11] += 1
                else:
                    temp_state[12] += 3
                    if state[6] == 1:
                        temp_state[12] += 1
            temp_state[22] = 0
            temp_state[23] = (0,0,0,0,0)
            temp_state[24] = (0,0,0,0,0)
            temp_state[0] = 0
        elif action == 7:
            temp_state[9] += temp_state[7]
            if temp_state[1] == 0: #凡体
                temp_state[9] += 4
                temp_state[8] = self._get_lingqi(state, 8+state[14])
                now_lingqi = list(temp_state[8])
                now_lingqi[state[3]] += 1
                temp_state[8] = tuple(now_lingqi)
            else:
                temp_state[10] += 4
                if state[19] == 1:
                    temp_state[8] = self._get_lingqi(state, state[14]+state[10] // 10)
                else:
                    temp_state[8] = self._get_lingqi(state, state[14])
                if state[21] == 1:
                    if state[15] == 0:
                        temp_state[9] -= 8
                        temp_state[15] = 1
                    else:
                        temp_state[9] -= 4

            temp_state[7] += 1
            temp_state[14] = 0
            temp_state[16] = 0
            temp_state[17] = 0
            temp_state[18] = 0
            temp_state[19] = 0
            temp_state[20] = 0
            temp_state[21] = 0
            temp_state[23] = (0,0,0,0,0)
            temp_state[24] = (0,0,0,0,0)
            temp_state[0] = 0
        elif 8 <= action <= 17:
            skill_list = {8:(3,0,0,0,0),9:(2,0,0,0,0),
                          10:(5,0,0,0,0),11:(5,0,0,0,0),
                          12:(3,1,0,0,0),13:(2,2,0,0,0),
                          14:(3,2,0,0,0),15:(3,1,0,0,0),
                          16:(1,1,0,0,0),17:(2,1,0,0,0)}
            temp_state[0] = 2
            temp_state[22] = action
            temp_state[23] = skill_list[action]
            temp_state[24] = (0,0,0,0,0)
        
        temp_state[9] = max(0,temp_state[9])

        return tuple(temp_state)
    
    def is_finished(self, state):
        if state[9] >= 100:
            return -1
        if state[10] >= 100:
            return 1
        return 0

'''
state = (0,
         0,
        (400,400,5,5,5),
        0,
        1,
        1,
        1,
        1,
        (0,1,1,0,1),
        10,
        15,
        20,
        40,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        (0,0,0,0,0),
        (0,0,0,0,0))


test_env = DivinizingEnv(10, [50,10,10,10,10], 1, 1, 1)
print(test_env.get_action_list(state))
state = test_env.get_next_state(state, 0)
print(state)
print(test_env.get_action_list(state))
state = test_env.get_next_state(state, 7)
print(state)
print(test_env.get_action_list(state))
'''