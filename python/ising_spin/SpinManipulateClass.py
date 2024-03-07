import numpy as np

class IsingSpin:
    def __init__(self):
        self.sz = 1  # 默认构造函数，将自旋初始化为+1

    def get_sz(self):
        return self.sz  # 返回当前自旋的值

    def set_up(self):
        self.sz = 1  # 将自旋设置为+1，表示向上

    def set_dw(self):
        self.sz = -1  # 将自旋设置为-1，表示向下

    def set_sz(self, sz_spec):
        # 设置自旋为给定的值，参数必须是+1或-1，否则会触发断言错误
        assert sz_spec == 1 or sz_spec == -1
        self.sz = sz_spec

    def flip(self):
        self.sz *= -1  # 翻转自旋的方向，由+1变为-1，或由-1变为+1


# # 测试 IsingSpin 类的功能
# ising_spin = IsingSpin()
# print("Initial sz:", ising_spin.get_sz())

# ising_spin.set_dw()
# print("After setting down:", ising_spin.get_sz())

# ising_spin.flip()
# print("After flipping:", ising_spin.get_sz())

