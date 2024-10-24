import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Configurar a porta serial (ajuste a porta conforme o seu sistema)
ser = serial.Serial('COM5', 9600, timeout=1)

# Inicializar listas para armazenar os dados
temps, pressures, accXs, accYs, accZs = [], [], [], [], []

# Função para atualizar o gráfico
def update(frame):
    line = ser.readline().decode('utf-8').strip()
    if line:
        try:
            # Separar os valores recebidos
            temperature, pressure, accX, accY, accZ = map(float, line.split(','))

            # Adicionar os valores às listas
            temps.append(temperature)
            pressures.append(pressure)
            accXs.append(accX)
            accYs.append(accY)
            accZs.append(accZ)

            # Manter apenas os últimos 50 pontos para o gráfico
            temps[:] = temps[-50:]
            pressures[:] = pressures[-50:]
            accXs[:] = accXs[-50:]
            accYs[:] = accYs[-50:]
            accZs[:] = accZs[-50:]

            # Limpar os gráficos
            ax1.clear()
            ax2.clear()

            # Plotar temperatura e pressão
            ax1.plot(temps, label="Temperatura (C)")
            ax1.plot(pressures, label="Pressão (Pa)")
            ax1.legend(loc="upper left")

            # Plotar acelerações
            ax2.plot(accXs, label="Aceleração X")
            ax2.plot(accYs, label="Aceleração Y")
            ax2.plot(accZs, label="Aceleração Z")
            ax2.legend(loc="upper left")
        except ValueError:
            pass

# Configurar os subplots
fig, (ax1, ax2) = plt.subplots(2, 1)

# Função de animação para atualizar o gráfico
ani = FuncAnimation(fig, update, interval=500)

# Exibir o gráfico
plt.show()
