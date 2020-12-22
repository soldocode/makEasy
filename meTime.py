


class Time(object):
    ''' This class define time entity ''' 
    
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
    ''' It defines the entire spectrum of times that affect the work cycles:
        - load - time spent in the upload activity
        - tool - time taken to prepare the machine for work
        - move - time taken to position the pieces or work tools
        - work - time of actual work on the material
        - look - time spent checking the quality of work
        - dwld - time taken to unload the pieces at the end of the job '''
        
    def __init__(self):
        self.Load=Time()
        self.Tool=Time()
        self.Move=Time()
        self.Work=Time()
        self.Look=Time()
        self.Dwld=Time()

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


    @property
    def DictTimes(self):
        t={'Load':round(self.Load.Minutes,2)}
        t['Tool']=round(self.Tool.Minutes,2)
        t['Move']=round(self.Move.Minutes,2)
        t['Work']=round(self.Work.Minutes,2)
        t['Look']=round(self.Look.Minutes,2)
        t['Dwld']=round(self.Dwld.Minutes,2)
        return t

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
        self.BlockTime=BlockTime  #minutes
        self.NumBlock=NumBlock    #times
        self.Length=Length        #mm
        self.Speed=Speed          #minutes/mm
        self.Time=self.compute()

    def __str__(self):
        return 'BlockTime:'+str(self.BlockTime)+' - Speed:'+str(self.Speed)

    def compute (self):
        self.Time=self.BlockTime*self.NumBlock+self.Length/self.Speed
        return self.Time
