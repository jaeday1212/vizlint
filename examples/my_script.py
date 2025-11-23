import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.bar(["A", "B"], [101, 103])
ax.set_ylim(100, 104)
