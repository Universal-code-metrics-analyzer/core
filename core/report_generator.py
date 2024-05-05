from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel

from .metrics_calculator import TreeMetrics


class ReportGenratorConfigShape(BaseModel):
    verbose: bool = False


class ReportGenerator[ConfigShapeT: ReportGenratorConfigShape](ABC):
    if TYPE_CHECKING:
        config_shape: type[ConfigShapeT]

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__()

        for el in {'config_shape'}:
            attr = getattr(kwargs, el)
            if attr is None:
                raise Exception(f'Invalid subclass {cls.__name__}: {el} is None')

            setattr(cls, el, attr)

    def __init__(self, config: ConfigShapeT, tree_metrics: TreeMetrics) -> None:
        self.config = self.validate_config(config)
        self.tree_metrics = tree_metrics

    def validate_config(self, config: ConfigShapeT) -> ConfigShapeT:
        return self.config_shape.model_validate(dict(config))

    @abstractmethod
    async def generate(self, tree_metrics: TreeMetrics) -> None: ...
