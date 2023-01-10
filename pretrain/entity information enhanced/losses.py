from torch.nn import CrossEntropyLoss
from torch.nn import BCEWithLogitsLoss

__call__ = ['CrossEntropy', 'BCEWithLogitsLoss']


# Crossentropy loss function
class CrossEntropy(object):
    def __init__(self):
        self.loss_fn = CrossEntropyLoss()

    def __call__(self, output, target):
        loss = self.loss_fn(input=output, target=target)
        return loss

class NCEWithLogitsLoss(object):
    def __init__(self):
        self.loss_fn = NCEWithLogitsLoss()

    def __call__(self, output, target):
        output = output.float()
        target = target.float()
        loss = self.loss_fn(input=output, target=target)
        return loss