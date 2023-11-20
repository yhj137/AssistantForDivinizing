import env
import random
import matplotlib.pyplot as plt
from tqdm import tqdm

class DivinizingGame():
    def __init__(self, origin_xianxing, linggen, wuxing, is_xianti, is_cuiti, is_suhun):
        self.env = env.DivinizingEnv()
        self.origin_xianxing = origin_xianxing
        self.linggen = linggen
        self.wuxing = wuxing
        self.is_xianti = is_xianti
        self.is_cuiti = is_cuiti
        self.is_suhun = is_suhun
        self.state = [      0,
                            0,
                            linggen,
                            wuxing,
                            is_xianti,
                            is_cuiti,
                            is_suhun,
                            1,
                            tuple([(0 if wuxing != i else 1) for i in range(5)]),
                            0,
                            origin_xianxing,
                            0,
                            0,
                            0,
                            0,
                            0,
                            0,
                            0,
                            0,
                            0,
                            0,
                            0,
                            0,
                            (0,0,0,0,0),
                            (0,0,0,0,0)]
        self.state[8] = self.env._get_lingqi(self.state, 16)
        self.state = tuple(self.state)

    def get_action_list(self):
        return self.env.get_action_list(self.state)

    def step(self, action):
        self.state = self.env.get_next_state(self.state, action)

    def is_finished(self):
        return self.env.is_finished(self.state)

    def run(self):
        while self.env.is_finished(self.state) == 0:
            actions = self.env.get_action_list(self.state)
            action = actions[random.randint(0, len(actions)-1)]
            self.state = self.env.get_next_state(self.state, action)
        return self.env.is_finished(self.state), self.state[9], self.state[10], self.state[11], self.state[12]
    
    def reset(self):
        self.state = [      0,
                            0,
                            self.linggen,
                            self.wuxing,
                            self.is_xianti,
                            self.is_cuiti,
                            self.is_suhun,
                            1,
                            tuple([(0 if self.wuxing != i else 1) for i in range(5)]),
                            0,
                            self.origin_xianxing,
                            0,
                            0,
                            0,
                            0,
                            0,
                            0,
                            0,
                            0,
                            0,
                            0,
                            0,
                            0,
                            (0,0,0,0,0),
                            (0,0,0,0,0)]
        self.state[8] = self.env._get_lingqi(self.state, 16)
        self.state = tuple(self.state)

if __name__ == "__main__":

    success_rate_list = []
    ave_cuiti_list = []
    ave_suhun_list = []
    ave_fanxing_list = []
    ave_xianxing_list = []

    round_num = 100

    for i in tqdm(range(100)):
        game = DivinizingGame(i, (610,610,10,10,10), 0, 1, 1, 1)
        success_rate = 0
        ave_cuiti = 0
        ave_suhun = 0
        ave_fanxing = 0
        ave_xianxing = 0
        for j in range(round_num):
            res = game.run()
            ave_fanxing += res[1]
            ave_xianxing += res[2]
            if res[0] > 0:
                success_rate += 1
                ave_cuiti += res[3]
                ave_suhun += res[4]
            game.reset()
        success_rate_list.append(success_rate/round_num)
        ave_fanxing_list.append(ave_fanxing/round_num)
        ave_xianxing_list.append(ave_xianxing/round_num)
        ave_cuiti_list.append(ave_cuiti/success_rate if success_rate>0 else 0)
        ave_suhun_list.append(ave_suhun/success_rate if success_rate>0 else 0)

    plt.figure()
    plt.xlabel('Origin Xianxing')
    plt.ylabel('Success Rate')
    plt.plot(list(range(100)), success_rate_list, c='black')
    plt.show()

    plt.xlabel('Origin Xianxing')
    plt.ylabel('Average Fanxing')
    plt.plot(list(range(100)), ave_fanxing_list, c='red')
    plt.show()

    plt.xlabel('Origin Xianxing')
    plt.ylabel('Average Xianxing')
    plt.plot(list(range(100)), ave_xianxing_list, c='blue')
    plt.show()

    plt.xlabel('Origin Xianxing')
    plt.ylabel('Average Cuiti')
    plt.plot(list(range(100)), ave_cuiti_list, c='orange')
    plt.show()

    plt.xlabel('Origin Xianxing')
    plt.ylabel('Average Suhun')
    plt.plot(list(range(100)), ave_suhun_list, c='purple')
    plt.show()
