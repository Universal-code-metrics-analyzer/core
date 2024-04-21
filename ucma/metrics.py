from typing import Literal

from pydantic import BaseModel, Field


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


class PluginError(Exception):
    pass
