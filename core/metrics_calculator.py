from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, Any, Literal

from pydantic import BaseModel

from .git_processor import TreeData


class MetricsCalculatorConfigShape(BaseModel):
    verbose: bool = False


class MetricResult(BaseModel):
    metric_name: str
    subject_path: str
    value: float
    description: str | None = None
    result_scope: Literal['module'] | Literal['class'] | Literal['function']


class BlobMetrics(BaseModel):
    type: Literal['blob']
    name: str
    path: str
    metric_results: list[MetricResult]


class TreeMetrics(BaseModel):
    type: Literal['tree']
    name: str
    path: str
    metric_results: list[MetricResult]
    trees: list['TreeMetrics']
    blobs: list[BlobMetrics]


class MetricsCalculator[ConfigShapeT: MetricsCalculatorConfigShape](metaclass=ABCMeta):
    if TYPE_CHECKING:
        config_shape: type[ConfigShapeT]

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__()

        for el in {'config_shape'}:
            attr = kwargs.get(el, None)
            if attr is None:
                raise Exception(f'Invalid subclass {cls.__name__}: {el} is {attr}')

            setattr(cls, el, attr)

    def __init__(self, config_dict: dict[str, Any], tree_data: TreeData) -> None:
        self.config = self.validate_config(config_dict)
        self.tree_data = tree_data

    def validate_config(self, config_dict: dict[str, Any]) -> ConfigShapeT:
        return self.config_shape.model_validate(config_dict)

    @abstractmethod
    async def calculate(self) -> TreeMetrics: ...
