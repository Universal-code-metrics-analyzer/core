from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel

from core.git_processor import CommitMeta

from .metrics_calculator import TreeMetrics


class ReportGenratorConfigShape(BaseModel):
    verbose: bool = False


class ReportGenerator[ConfigShapeT: ReportGenratorConfigShape](ABC):
    if TYPE_CHECKING:
        config_shape: type[ConfigShapeT]

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__()

        for el in {'config_shape'}:
            attr = kwargs.get(el, None)
            if attr is None:
                raise Exception(f'Invalid subclass {cls.__name__}: {el} is None')

            setattr(cls, el, attr)

    def __init__(
        self,
        config_dict: dict[str, Any],
        sha: str,
        commit_meta: CommitMeta,
        tree_metrics: TreeMetrics,
    ) -> None:
        self.config = self.validate_config(config_dict)
        self.sha = sha
        self.commit_meta = commit_meta
        self.tree_metrics = tree_metrics

    def validate_config(self, config_dict: dict[str, Any]) -> ConfigShapeT:
        return self.config_shape.model_validate(config_dict)

    @abstractmethod
    async def generate(self) -> None: ...
