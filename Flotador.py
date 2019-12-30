# This Python file uses the following encoding: utf-8
# Class Flotador
import math

# 81.3 metros cubicos


class Flotador:

    def __init__(self):

        self.d1 = 4.267  # diametro do flotador em metros
        self.d2 = 3.0  # diametro do flotador na regiao da camara de oleo em metros
        self.hOleo = 1.0  # altura da camera de oleo em metros
        self.h1 = 5.8  # altura da camera de agua produzida em metros
        self.po = 950.0  # kg/m3

        self.lvl1 = 0.0  # nivel da camara principal
        self.lvl2 = 0.0  # nivel da camara de oleo

        self.dT = 0.1  # delta t da simulaçao

        self.actualMass = 0.0  # massa atual acumulada no flotador
        self.actualMassOleo = 0.0  # massa atual acumulada na camara de óleo

        self.oleo = 0

        self.massAtH1 = math.pi * (self.d1/2) ** 2 * \
            self.h1 * self.po  # massa total em h1

        self.volume1 = math.pi * \
            ((self.d1/2) ** 2) * self.h1 + \
            math.pi * ((self.d2/2) ** 2) * self.hOleo

        self.volume2 = math.pi * \
            ((self.d1/2) ** 2 - (self.d2/2) ** 2) * self.hOleo

    def updateLevels(self, mP, mA, mO, dt):

        # Atualiza massa acumulada no vazo da agua produzdia
        self.actualMass += (mP - mA) * dt

        # Atualiza massa acumulada no vazo de oleo flotado
        mass = self.volume1 * self.po

        if self.actualMass > mass:
            self.actualMassOleo += self.actualMass - mass
            self.actualMass -= self.actualMass - mass

        # Calcula o nível atual do vaso de oleo flotado
        if self.actualMassOleo > 0:

            self.lvl2 = self.actualMassOleo / \
                (self.po * math.pi * ((self.d1/2)**2 - (self.d2/2) ** 2))

            self.actualMassOleo -= mO * dt

        # Calcula o nível atual do vaso da agua produzida
        if self.actualMass <= self.massAtH1:
            self.lvl1 = self.actualMass / \
                (self.po * math.pi * (self.d1 / 2) ** 2)
        else:
            self.lvl1 = self.h1 + (self.actualMass - self.massAtH1) / \
                (self.po * math.pi * (self.d2 / 2) ** 2)
