# coding: utf-8
from matplotlib import pyplot as plt
import math


import Flotador
import Pid
import Lv

mP = 50.0  # kg/s
mO = 0.0  # kg/s
mA = 0.0  # kg/s

dt = 0.1  # s passo da simulação
total = 3600
t = total  # s tempo total da simulação

limite_inferior = 6.4
limite_superior = (6.8 * 87) / 85


flotador = Flotador.Flotador()
pid533306 = Pid.Pid(1.2, 0.0166667, 0)
pid533605 = Pid.Pid(0.01, 0.00333334, 0, 6.9, 6.7)
pid533601 = Pid.Pid(2.5, 0.0333334, 0.5)
lv533602 = Lv.Lv()
lv533601 = Lv.Lv()


pid533605.setPoint(15)
pid533601.setPoint(0.6)

time = []
level = []
level2 = []
valve = []
oleo = []
mpa = []
oleoMass = []

while t > 0.0:

    flotador.updateLevels(mP, 100 - mA, 100 - mO, dt)

    mA = pid533306.update(flotador.lvl1, dt)

    mO = pid533601.update(flotador.lvl2, dt)

    nivelAjustado = pid533605.update(100 - mO, dt)

    pid533306.setPoint(nivelAjustado)  # nível desejado no vaso

    # print(flotador.lvl1, total - t, flotador.actualMass, mA)

    # salva valores
    mpa.append(nivelAjustado)
    time.append(total - t)
    level.append(flotador.lvl1)
    level2.append(flotador.lvl2)
    valve.append((100 - mA)/100)
    oleo.append((100 - mO)/100)
    oleoMass.append(flotador.actualMassOleo)

    t -= dt


# Gráficos de saídas


fig = plt.figure()
st = fig.suptitle("Controle Avançado Flotador", fontsize="x-large")

ax1 = fig.add_subplot(411)
ax1.plot(time, level, color='blue')
ax1.plot(time, valve, color='orange')
ax1.set_title("Nivel de Agua Produzida")
ax1.grid(True)

ax2 = fig.add_subplot(412)
ax2.plot(time, oleo, color='red')
ax2.plot(time, level2, color='yellow')
ax2.set_title("Nivel da Câmara de Óleo")
ax2.grid(True)


ax3 = fig.add_subplot(413)
ax3.plot(time, oleo, color='green')
ax3.plot(time, mpa, color='blue')
ax3.set_title("Saída do MPA")
ax3.grid(True)

ax4 = fig.add_subplot(414)
ax4.plot(time, oleoMass, color='green')
ax4.set_title("Volume de Óleo")
ax4.grid(True)


fig.tight_layout()

st.set_y(0.95)
fig.subplots_adjust(top=0.85)

plt.show()
