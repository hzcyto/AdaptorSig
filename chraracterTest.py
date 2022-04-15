class Status:
    def __init__(self, Str:int=5, Con:int=5, Dex:int=5, ):
        self.sttsD = dict(
            STR = Str,
            CON = Con,
            
        )

class Job:
    def __init__(self, subf:bool=False):
        self.subF = subf
        self.sttsB

    def lvUpSeq(self):
        pass

class Character:
    def __init__(self, job:Job, lv:int=1):
        self.job = job
        self.subJob:Job = None
        self.lv = lv

    def lvUp(self):
        self.lv += 1
        self.Job.lvUpSeq()
        if not self.subJob is None:
            self.subJob.lvUpSeq()