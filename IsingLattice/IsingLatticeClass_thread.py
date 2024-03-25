import numpy as np
import matplotlib.pyplot as plt
import threading

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


class IsingLattice:
    def __init__(self, num_rows, num_cols):
        self.J = 1.0
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.maxrep_state = 2 ** (num_rows * num_cols) - 1
        self.spin = np.array([[IsingSpin() for _ in range(num_cols)] for _ in range(num_rows)])

    def JO(self):
        # 返回当前 J 值
        return self.J
    
    def change_J(self, new_J):
        # 修改 J 值
        self.J = new_J

    def num_spins(self):
        # 返回晶格中自旋的总数
        return self.num_rows * self.num_cols

    def maxrep_stateQ(self):
        # 返回晶格中自旋的最大表示状态 2^(num_rows * num_cols) - 1
        return self.maxrep_state

    def _sz(self, row_idx, col_idx):
        # 返回晶格中指定位置的自旋值
        return self.spin[row_idx][col_idx].get_sz()

    def set_up_spin(self, row_idx, col_idx):
        # 将晶格中指定位置的自旋设置为+1
        self.spin[row_idx][col_idx].set_up()

    def set_dw_spin(self, row_idx, col_idx):
        # 将晶格中指定位置的自旋设置为-1
        self.spin[row_idx][col_idx].set_dw()

    def set_spin(self, row_idx, col_idx, s_spec):
        # 将晶格中指定位置的自旋设置为给定的值
        self.spin[row_idx][col_idx].set_sz(s_spec)

    def flip_spin(self, row_idx, col_idx):
        # 翻转晶格中指定位置的自旋
        self.spin[row_idx][col_idx].flip()

    def set_spin_configuration(self, configuration_code):
        # 通过给定的配置码设置晶格中的自旋 5 -> 00000101 -> [[1, -1, 1], [-1, -1, -1], [-1, -1, -1]]
        binary_string = bin(configuration_code)[2:].zfill(self.num_rows * self.num_cols)
        spin_array = np.array([int(bit) * 2 - 1 for bit in binary_string])
        spin_array = np.flipud(spin_array)
        spin_array = spin_array.reshape(self.num_rows, self.num_cols)

        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self.spin[i][j].set_sz(spin_array[i][j])
    
    def get_index(self, row_idx, col_idx):
        # 返回晶格中指定位置的索引
        return row_idx * self.num_cols + col_idx

    def get_spin_state_all(self):
        # 返回晶格中所有自旋的状态 
        return np.array([[self.spin[i][j].get_sz() for j in range(self.num_cols)] for i in range(self.num_rows)])
    
    def calculate_total_energy(self):
        # 计算晶格的总能量
        energy = 0
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                energy += -self.J * self.spin[i][j].get_sz() * (self.spin[(i + 1) % self.num_rows][j].get_sz() +
                                                                self.spin[i][(j + 1) % self.num_cols].get_sz() +
                                                                self.spin[(i - 1) % self.num_rows][j].get_sz() +
                                                                self.spin[i][(j - 1) % self.num_cols].get_sz()) 
        return energy / 2

    def calculate_total_magnetization(self):
        # 计算晶格的总磁矩
        return np.sum([[self.spin[i][j].get_sz() for j in range(self.num_cols)] for i in range(self.num_rows)])

    def get_neighbours(self, row_idx, col_idx):
        # 返回晶格中指定位置的自旋的所有邻居的自旋值
        # 以二维晶格为例，对于晶格中的一个自旋，其邻居有四个，分别是上、右、下、左四个方向的自旋
        # return a dictionary of neighbours' spin and their index
        neighbours = {}
        neighbours['up:index'+str(self.get_index((row_idx - 1) % self.num_rows, col_idx))] = self.spin[(row_idx - 1) % self.num_rows][col_idx].get_sz()
        neighbours['right'] = self.spin[row_idx][(col_idx + 1) % self.num_cols].get_sz()
        neighbours['down'] = self.spin[(row_idx + 1) % self.num_rows][col_idx].get_sz()
        neighbours['left'] = self.spin[row_idx][(col_idx - 1) % self.num_cols].get_sz()
        neighbours['current'] = self.spin[row_idx][col_idx].get_sz()

        return neighbours

    def get_picture_of_spin(self, save_name):
        # 返回晶格中所有自旋的图片

        spin_state_now = np.array([[self.spin[i][j].get_sz() for j in range(self.num_cols)] for i in range(self.num_rows)])
        color = np.where(spin_state_now == 1, 'bo', 'ro')


        x_array = np.linspace(0, self.num_cols-1, self.num_cols)
        y_array = np.linspace(0, self.num_rows-1, self.num_rows)
        coordinates = []
        for x in x_array:
            for y in y_array:
                coordinates.append([x, y])

        fig, ax = plt.subplots(figsize=(self.num_rows,self.num_cols))
        plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95)
        plt.axis('off')
        for i1 in range(len(coordinates)):
            for i2 in range(len(coordinates)):
                if np.sqrt((coordinates[i1][0] - coordinates[i2][0])**2+(coordinates[i1][1] - coordinates[i2][1])**2) < 1.1:
                    ax.plot([coordinates[i1][0], coordinates[i2][0]], [coordinates[i1][1], coordinates[i2][1]], '-k', linewidth=1)
        for i in range(len(coordinates)):
            ax.plot(coordinates[i][0], coordinates[i][1], 
                    color[ int(coordinates[i][1]) ][ int(coordinates[i][0]) ], markersize=10)
        ax.set_ylim(ax.get_ylim()[::-1])

        # plt.savefig('/home/sjtu/Workplace_ygj/CP2024_code/picture/data/{}.jpg'.format(save_name), dpi=300, bbox_inches='tight')
        plt.show()



    def calculate_total_energy_T(self):
        # 计算晶格的总能量
        energy = 0
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                energy += -self.J * self.spin[i][j].get_sz() * (self.spin[(i + 1) % self.num_rows][j].get_sz() +
                                                                self.spin[i][(j + 1) % self.num_cols].get_sz() +
                                                                self.spin[(i - 1) % self.num_rows][j].get_sz() +
                                                                self.spin[i][(j - 1) % self.num_cols].get_sz()) 
        return energy / 2

    def calculate_total_magnetization_T(self):
        # 计算晶格的总磁矩
        return np.sum([[self.spin[i][j].get_sz() for j in range(self.num_cols)] for i in range(self.num_rows)])

    def calculate_energy_and_magnetization(self, start, end, energy_results, magnetization_results):
        for i in range(start, end):
            self.set_spin_configuration(i)
            energy_results[i] = self.calculate_total_energy_T()
            magnetization_results[i] = self.calculate_total_magnetization_T()

    def all_state_H_M(self):
        # 返回晶格中所有可能状态的能量和磁矩

        num_states = 2 ** (self.num_rows * self.num_cols)
        num_threads = 10  # 设置线程数
        energy_results = [0] * num_states
        magnetization_results = [0] * num_states
        threads = []

        for i in range(num_threads):
            start = i * (num_states // num_threads)
            end = (i + 1) * (num_states // num_threads) if i < num_threads - 1 else num_states
            thread = threading.Thread(target=self.calculate_energy_and_magnetization, args=(start, end, energy_results, magnetization_results))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return [energy_results, magnetization_results]



    def all_state_energy(self):
        # 返回晶格中所有可能状态的能量
        self.all_energy = []
        for i in range(2 ** (self.num_rows * self.num_cols)):
            self.set_spin_configuration(i)
            self.all_energy.append(self.calculate_total_energy())
        return self.all_energy
    
    def all_state_magnetization(self):
        # 返回晶格中所有可能状态的磁矩
        self.all_magnetization = []
        for i in range(2 ** (self.num_rows * self.num_cols)):
            self.set_spin_configuration(i)
            self.all_magnetization.append(self.calculate_total_magnetization())
        return self.all_magnetization

    def all_property_compute(self, T, 
                             compute_H=False,
                             compute_H2=False, 
                             compute_M=False,
                             compute_M2=False,
                             compute_C=False,):
        # 返回晶格中所有可能状态的能量和磁矩

        kb = 1
        beta = 1 / (kb * T)
        if compute_C:
            compute_H = True
        if compute_M2:
            compute_M = True
            compute_H = True
        if compute_H2:
            compute_H = True
        if compute_C:
            compute_H = True
            compute_H2 = True

        self.all_energy = []
        self.all_magnetization = []

        if compute_H:
            for i in range(2 ** (self.num_rows * self.num_cols)):
                self.set_spin_configuration(i)
                self.all_energy.append(self.calculate_total_energy())

        if compute_M:
            for i in range(2 ** (self.num_rows * self.num_cols)):
                self.set_spin_configuration(i)
                self.all_magnetization.append(self.calculate_total_magnetization())

        self.all_energy = np.array(self.all_energy)
        self.all_magnetization = np.array(self.all_magnetization)

        property_dict = {}

        if compute_H:
            property_dict['Z'] = np.sum(np.exp(-np.array(self.all_energy)*beta))
            property_dict['average_H'] = np.sum(self.all_energy*np.exp(-np.array(self.all_energy)*beta) / property_dict['Z'])
        if compute_H2:
            property_dict['average_H2'] = np.sum(self.all_energy**2*np.exp(-np.array(self.all_energy)*beta) / property_dict['Z'])
        if compute_M:
            property_dict['average_M'] = np.sum(self.all_magnetization*np.exp(-np.array(self.all_energy)*beta) / property_dict['Z'])
        if compute_M2:
            property_dict['average_M2'] = np.sum(self.all_magnetization**2*np.exp(-np.array(self.all_energy)*beta) \
                                                 / property_dict['Z']) / self.num_spins()**2
        if compute_C:
            property_dict['average_C'] = (property_dict['average_H2'] - property_dict['average_H']**2) / (T**2) / self.num_spins()

        return property_dict
    
    def all_property_compute_T(self, T, 
                             compute_H=False,
                             compute_H2=False, 
                             compute_M=False,
                             compute_M2=False,
                             compute_C=False,):
        # 返回晶格中所有可能状态的能量和磁矩

        kb = 1
        beta = 1 / (kb * T)
        if compute_C:
            compute_H = True
        if compute_M2:
            compute_M = True
            compute_H = True
        if compute_H2:
            compute_H = True
        if compute_C:
            compute_H = True
            compute_H2 = True

        self.all_H_B = []
    
        if compute_H:
            for i in range(2 ** (self.num_rows * self.num_cols)):
                self.set_spin_configuration(i)
                self.all_H_B.append(self.all_state_H_M())
         

        self.all_energy = np.array(self.all_H_B[0])
        self.all_magnetization = np.array(self.all_H_B[0])

        property_dict = {}

        if compute_H:
            property_dict['Z'] = np.sum(np.exp(-np.array(self.all_energy)*beta))
            property_dict['average_H'] = np.sum(self.all_energy*np.exp(-np.array(self.all_energy)*beta) / property_dict['Z'])
        if compute_H2:
            property_dict['average_H2'] = np.sum(self.all_energy**2*np.exp(-np.array(self.all_energy)*beta) / property_dict['Z'])
        if compute_M:
            property_dict['average_M'] = np.sum(self.all_magnetization*np.exp(-np.array(self.all_energy)*beta) / property_dict['Z'])
        if compute_M2:
            property_dict['average_M2'] = np.sum(self.all_magnetization**2*np.exp(-np.array(self.all_energy)*beta) \
                                                 / property_dict['Z']) / self.num_spins()**2
        if compute_C:
            property_dict['average_C'] = (property_dict['average_H2'] - property_dict['average_H']**2) / (T**2) / self.num_spins()

        return property_dict
    

# # Example usage:
# rows = 4
# cols = 4
# system = IsingSystem(rows, cols)

# configurations = [7, 77, 777]

# for config in configurations:
#     system.set_spin_configuration(config)
#     M = system.calculate_total_magnetization()
#     E = system.calculate_total_energy()
#     print(f"For configuration {config}:")
#     print(system.get_spin_state())
#     print(f"Total Magnetization: {M}")
#     print(f"Total Energy: {E}")
#     print()


