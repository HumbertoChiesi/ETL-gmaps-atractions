from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Optional

class Manipulador(ABC):
    @abstractmethod
    def definir_proximo(self, manipulador: Manipulador) -> Manipulador:
        pass

    @abstractmethod
    def manipular(self, request) -> Optional[str]:
        pass


class ManipuladorAbstrato(Manipulador):
    _proximo_manipulador: Manipulador = None

    def definir_proximo(self, manipulador: Manipulador) -> Manipulador:
        self._proximo_manipulador = manipulador
        return manipulador

    @abstractmethod
    def manipular(self, request: Any) -> Any:
        if self._proximo_manipulador:
            return self._proximo_manipulador.manipular(request)

        return request
