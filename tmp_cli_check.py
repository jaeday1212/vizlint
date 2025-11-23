import matplotlib.pyplot as plt

fig1, ax1 = plt.subplots()
ax1.bar(['A', 'B'], [101, 103])
ax1.set_ylim(100, 104)

fig2, ax2 = plt.subplots()
ax2.plot([0, 1, 2], [1, 4, 9])
ax2.set_xlabel('x')
ax2.set_ylabel('y')

fig3, ax3 = plt.subplots()
ax3.scatter([1, 2, 3], [3, 2, 5])
ax3.set_title('Scatter Example')

