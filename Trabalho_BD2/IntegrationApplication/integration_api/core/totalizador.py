from threading import Lock
from datetime import date, datetime


class TotalizadorDiario:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._totais = {}  # Dicionário {data: total}
                cls._instance._lock = Lock()
        return cls._instance

    def adicionar_pedido(self, valor: float, data_pedido: date) -> None:
        with self._lock:
            data_str = data_pedido.isoformat()
            if data_str not in self._totais:
                self._totais[data_str] = 0.0
            self._totais[data_str] += valor

    def obter_total_hoje(self) -> float:
        with self._lock:
            hoje = date.today().isoformat()
            return self._totais.get(hoje, 0.0)

    def obter_total_por_data(self, data: date) -> float:
        with self._lock:
            data_str = data.isoformat()
            return self._totais.get(data_str, 0.0)


# Instância global
totalizador_diario = TotalizadorDiario()