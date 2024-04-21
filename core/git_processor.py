from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel


class GitProcessorConfigShape(BaseModel):
    pass


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

    def __init__(self, config: ConfigShapeT) -> None:
        self.config = self.validate_config(config)

    def validate_config(self, config: ConfigShapeT) -> ConfigShapeT:
        return self.config_shape.model_validate(dict(config))

    @abstractmethod
    async def get_root_tree(self, commit_sha: str) -> TreeT: ...

    @abstractmethod
    async def process_blob(self, blob: BlobT, depth: int) -> BlobData: ...

    @abstractmethod
    async def process_tree(self, tree: TreeT, depth: int = 0) -> TreeData: ...

    async def cleanup(self) -> None:
        pass

    async def process(self, commit_sha: str) -> str:
        result = await self.process_tree(await self.get_root_tree(commit_sha))
        await self.cleanup()
        return result.model_dump_json()
