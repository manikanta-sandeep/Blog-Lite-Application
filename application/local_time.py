from datetime import datetime,timedelta
import pytz



class time_calc:
    def time(self):
        UTC = pytz.utc
        IST = pytz.timezone('Asia/Kolkata')
        datetime_ist = datetime.now(IST)
        return datetime_ist.strftime('%Y:%m:%d %H:%M:%S %Z')
    def time_with(self,start,end):
        start_time=datetime.strptime(start, '%Y:%m:%d %H:%M:%S %Z')
        end_time=datetime.strptime(end, '%Y:%m:%d %H:%M:%S %Z')
        difference=end_time-start_time 
        minutes=(difference.seconds)//60
        hours=(difference.seconds)//3600
        days=difference.days
        weeks=days//7
        months=days//30
        years=months//12
        seconds=difference.seconds
        return minutes,hours,days,weeks,months,years,seconds

    def convert(self,s):
        #print(time_calc().time())
        e=time_calc().time()
        (a,b,c,d,f,g,h)=time_calc().time_with(s,e)
        #print("seconds",h,"minutes",a,"hours",b,"days",c,"weeks",d,"months",f,"years",g)
        if g>=1:
            temp=str(g)
            if g==1:
                temp=temp+" year"
            else:
                temp=temp+" years"
        elif f>=1:
            temp=str(f)
            if f==1:
                temp=temp+" month"
            else:
                temp=temp+" months"
        elif d>=1:
            temp=str(d)
            if d==1:
                temp=temp+" week"
            else:
                temp=temp+" weeks"
        elif c>=1:
            temp=str(c)
            if c==1:
                temp=temp+" day"
            else:
                temp=temp+" days"
        elif b>=1:
            temp=str(b)
            if b==1:
                temp=temp+" hour"
            else:
                temp=temp+" hours"
        elif a>=1:
            temp=str(a)
            if a==1:
                temp=temp+" minute"
            else:
                temp=temp+" minutes"
        else:
            temp=str(h)
            if h==1:
                temp=temp+" second"
            else:
                temp=temp+" seconds"
        return temp+" ago"

