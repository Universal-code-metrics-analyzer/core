from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel


class GitProcessorConfigShape(BaseModel):
    verbose: bool = False


class BlobData(BaseModel):
    name: str
    path: str
    content: str
    type: str = 'blob'


class TreeData(BaseModel):
    name: str
    path: str
    trees: list['TreeData']
    blobs: list[BlobData]
    type: str = 'tree'


class GitProcessor[ConfigShapeT: GitProcessorConfigShape, TreeT, BlobT](metaclass=ABCMeta):
    if TYPE_CHECKING:
        config_shape: type[ConfigShapeT]

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__()

        for el in {'config_shape'}:
            attr = kwargs.get(el, None)
            if attr is None:
                raise Exception(f'Invalid subclass {cls.__name__}: {el} is {attr}')

            setattr(cls, el, attr)

    def __init__(self, config_dict: dict[str, Any], commit_sha: str) -> None:
        self.config = self.validate_config(config_dict)
        self.commit_sha = commit_sha

    def validate_config(self, config_dict: dict[str, Any]) -> ConfigShapeT:
        return self.config_shape.model_validate(config_dict)

    @abstractmethod
    async def get_root_tree(self) -> TreeT: ...

    @abstractmethod
    async def process_blob(self, blob: BlobT, depth: int) -> BlobData: ...

    @abstractmethod
    async def process_tree(self, tree: TreeT, depth: int) -> TreeData: ...

    async def cleanup(self) -> None:
        pass

    async def process(self) -> str:
        result = await self.process_tree(await self.get_root_tree(), 0)
        await self.cleanup()
        return result.model_dump_json()
