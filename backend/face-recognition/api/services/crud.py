from base.crud import BaseCrud

app = 'ai'


class EmbeddingFaceCrud(BaseCrud):
    def __init__(self):
        super().__init__(f'{app}_embedding_face')

    async def add(self, data: dict, session=None):
        await self.set_unique([('username', 1)])
        return await super().add(data=data, session=session)
