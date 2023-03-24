from base.crud import BaseCrud

app = 'ai'


class EmbeddingFaceCrud(BaseCrud):
    def __init__(self):
        super().__init__(f'{app}_embedding_face')


class AviFaceCrud(BaseCrud):
    def __init__(self):
        super().__init__(f'{app}_avi_face')
