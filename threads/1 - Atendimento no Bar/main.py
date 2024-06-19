import threading
import time
import random


class Cliente(threading.Thread):
    def __init__(self, nome, bar):
        super().__init__()
        self.nome = nome
        self.bar = bar

    def run(self):
        while True:
            if self.bar.fechou and not any(self.bar.pedidos):
                break
            self.bar.faz_pedido(self)
            self.bar.espera_pedido(self)
            self.bar.recebe_pedido(self)
            self.bar.consome_pedido(self)
            # Tempo aleatório para fazer um novo pedido
            time.sleep(random.uniform(1, 5))


class Garcom(threading.Thread):
    def __init__(self, nome, bar, capacidade_atendimento):
        super().__init__()
        self.nome = nome
        self.bar = bar
        self.capacidade_atendimento = capacidade_atendimento

    def run(self):
        while True:
            if self.bar.fechou and not any(self.bar.pedidos):
                break
            self.bar.recebe_maximo_pedidos(self)
            self.bar.registra_pedidos(self)
            self.bar.rodada += 1


class Bar:
    def __init__(self, num_clientes, num_garcons, capacidade_atendimento, num_rodadas):
        self.num_clientes = num_clientes
        self.num_garcons = num_garcons
        self.capacidade_atendimento = capacidade_atendimento
        self.num_rodadas = num_rodadas
        self.fechou = False
        self.clientes = []
        self.garcons = []
        self.pedidos = [[] for _ in range(num_garcons)]
        self.rodada = 0

        # Mutex para controlar o acesso à lista de pedidos
        self.mutex_pedidos = threading.Lock()

        for i in range(self.num_clientes):
            cliente = Cliente(f"Cliente {i+1}", self)
            self.clientes.append(cliente)

        for i in range(self.num_garcons):
            garcom = Garcom(f"Garçom {i+1}", self, self.capacidade_atendimento)
            self.garcons.append(garcom)

    def faz_pedido(self, cliente):
        garcom_index = random.randint(0, self.num_garcons - 1)
        with self.mutex_pedidos:
            self.pedidos[garcom_index].append(cliente)
        print(f"{cliente.nome} fez um pedido.")

    def espera_pedido(self, cliente):
        while not any(cliente in p for p in self.pedidos):
            if self.fechou:
                break

    def recebe_pedido(self, cliente):
        with self.mutex_pedidos:
            for i, pedidos_garcom in enumerate(self.pedidos):
                if cliente in pedidos_garcom:
                    garcom_index = i
                    print(f"{self.garcons[garcom_index].nome} recebeu o pedido de {cliente.nome}.")
                    break

    def consome_pedido(self, cliente):
        print(f"{cliente.nome} está consumindo seu pedido.")

    def recebe_maximo_pedidos(self, garcom):
        while len(self.pedidos[self.garcons.index(garcom)]) < self.capacidade_atendimento:
            if self.fechou:
                break

    def registra_pedidos(self, garcom):
        garcom_index = self.garcons.index(garcom)
        with self.mutex_pedidos:
            pedidos = self.pedidos[garcom_index]
            print(f"{garcom.nome} está registrando pedidos.")
            for cliente in pedidos:
                print(f"{garcom.nome} está atendendo o pedido de {cliente.nome}.")
                self.pedidos[garcom_index].remove(cliente)
            print(f"{garcom.nome} atendeu todos os pedidos.")

    def iniciar_simulacao(self):
        for garcom in self.garcons:
            garcom.start()
        for cliente in self.clientes:
            cliente.start()

        while self.rodada < self.num_rodadas:
            if(self.rodada<0):
                print(f'fim da rodada: {self.rodada}')
            print(f"Rodada {self.rodada + 1}:")
            time.sleep(1)  # Simula o tempo de uma rodada
            self.rodada += 1

        self.fechou = True
        print("O bar fechou.")

        # Espera todas as threads terminarem antes de encerrar
        for garcom in self.garcons:
            garcom.join()
        for cliente in self.clientes:
            cliente.join()

        print("Todas as threads foram concluídas.")


# Exemplo de utilização
bar = Bar(num_clientes=5, num_garcons=2,
          capacidade_atendimento=3, num_rodadas=3)
bar.iniciar_simulacao()
