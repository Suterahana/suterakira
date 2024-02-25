from ..base_slashes import BaseSlashes


class MainSlashes(BaseSlashes):

    def __init__(self, interaction):
        super().__init__(interaction=interaction)

    async def preprocess_and_validate(self, **kwargs):
        if not await super().preprocess_and_validate(**kwargs):
            return False
        return True
