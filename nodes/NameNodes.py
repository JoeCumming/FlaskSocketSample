import time

from bonobo.config import use


class NameTransformer:
    def __call__(self, name: str):
        yield name.upper()


@use('status')
class NameConsumer:
    def __call__(self, name: str, status):
        print(name)
        status.emit("status", {"message": name})


class NameProducer:

    def __init__(self, number):
        self.number = number

    def __call__(self):
        for i in range(0, self.number):
            time.sleep(1)
            yield f"Test_{i}"
