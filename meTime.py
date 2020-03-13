


class Time(object):
    def __init__(self,minutes=0,seconds=0):
        self.Minutes=minutes
        self.HourlyCost=0
        self.TimeParameters=None
        if seconds>0: self.Minutes=seconds/60.0
        self._update()


    def __add__(self,add):
        return Time(self.Minutes+add.Minutes)

    def __str__(self):
        return str(self.Minutes)

    def _update(self):
        self.compute()

    @property
    def Cost(self):
        return self.Minutes/60*self.HourlyCost

    def compute(self):
        if self.TimeParameters:
            self.Minutes=self.TimeParameters.compute()




class WorkTime(object):
    def __init__(self,
                 load=Time(),
                 tool=Time(),
                 move=Time(),
                 work=Time(),
                 look=Time(),
                 dwld=Time()):
        self.Load=load
        self.Tool=tool
        self.Move=move
        self.Work=work
        self.Look=look
        self.Dwld=dwld

    def __add__(self,add_time):
        return(WorkTime(self.Load+add_time.Load,
                        self.Tool+add_time.Tool,
                        self.Move+add_time.Move,
                        self.Work+add_time.Work,
                        self.Look+add_time.Look,
                        self.Dwld+add_time.Dwld))

    def __str__(self):
        return str(self.Load)+','+str(self.Tool)

    @property
    def Cost(self):
        cost=self.Load.Cost
        cost+=self.Tool.Cost
        cost+=self.Move.Cost
        cost+=self.Work.Cost
        cost+=self.Look.Cost
        cost+=self.Dwld.Cost
        return cost


    @property
    def TotalTime(self):
        minutes=self.Load.Minutes
        minutes+=self.Tool.Minutes
        minutes+=self.Move.Minutes
        minutes+=self.Work.Minutes
        minutes+=self.Look.Minutes
        minutes+=self.Dwld.Minutes
        return minutes

    @property
    def HourlyCost(self):
        return self.Cost/self.TotalTime*60

    def compute(self):
        self.Load.compute()
        self.Tool.compute()
        self.Move.compute()
        self.Work.compute()
        self.Look.compute()
        self.Dwld.compute()

class TimeParameters(object):
    def __init__(self,
                 BlockTime=0,
                 NumBlock=0,
                 Length=0,
                 Speed=1):
        self.BlockTime=BlockTime          #minutes
        self.NumBlock=NumBlock    #times
        self.Length=Length         #mm
        self.Speed=Speed    #minutes/mm
        self.Time=self.compute()

    def __str__(self):
        return 'Time computed: '+str(self.Time)+' minutes'

    def compute (self):
        self.Time=self.BlockTime*self.NumBlock+self.Length/self.Speed
        return self.Time
