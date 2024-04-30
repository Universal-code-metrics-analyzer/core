from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, Any, Literal

from pydantic import BaseModel, Field


class MetricsCalculatorConfigShape(BaseModel):
    verbose: bool = False


class MetricResult(BaseModel):
    metric_name: str = Field(alias='metricName')
    subject_path: str = Field(alias='subjectPath')
    value: float
    description: str | None = None


class BlobMetricResult(MetricResult):
    result_scope: Literal['module'] | Literal['class'] | Literal['function'] = Field(
        alias='resultScope'
    )


class BlobMetrics(BaseModel):
    type: Literal['blob']
    name: str
    path: str
    metric_results: list[BlobMetricResult] = Field(alias='metricResults')


class TreeMetricResult(MetricResult):
    result_scope: Literal['program'] | Literal['package'] = Field(alias='resultScope')


class TreeMetrics(BaseModel):
    type: Literal['tree']
    name: str
    path: str
    metric_results: list[TreeMetricResult] = Field(alias='metricResults')
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

    def __init__(self, config_dict: dict[str, Any]) -> None:
        self.config = self.validate_config(config_dict)

    def validate_config(self, config_dict: dict[str, Any]) -> ConfigShapeT:
        return self.config_shape.model_validate(config_dict)

    @abstractmethod
    async def calculate(self) -> TreeMetrics: ...
