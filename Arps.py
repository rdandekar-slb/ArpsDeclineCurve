from datetime import datetime as dt
# from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule,MONTHLY,YEARLY
from enum import Enum
import math
from tabulate import tabulate
import matplotlib.pyplot as plt
import numpy as np



class ForecastFrequency(Enum):
    DAY=1
    WEEK=2
    MONTH=3
    QUARTER=4
    HALFYEAR=5
    YEAR=6

    
def get_dates_and_times(start_date,end_date,forecast_frequency):
    times=[]
    dates=[]
    if forecast_frequency==ForecastFrequency.MONTH:
        dates=list(rrule(freq=MONTHLY,bymonthday=1,dtstart=start_date,until=end_date))
    elif forecast_frequency==ForecastFrequency.QUARTER:
        dates=list(rrule(freq=MONTHLY,bymonthday=1,bymonth=[1,4,7,10],dtstart=start_date,until=end_date))
    elif forecast_frequency==ForecastFrequency.HALFYEAR:
        dates=list(rrule(freq=MONTHLY,bymonthday=1,bymonth=[1,7],dtstart=start_date,until=end_date))
    elif forecast_frequency==ForecastFrequency.YEAR:
        dates=list(rrule(freq=YEARLY,bymonthday=1,bymonth=[1],dtstart=start_date,until=end_date))
    if dates[0]!=start_date:
        dates=[start_date]+dates
    if dates[-1]!=end_date:
        dates=dates+[end_date]
    times=[(dates[i]-start_date).total_seconds()/(3600*24) for i in range(len(dates))]
    return dates,times


def get_arps_dc(initial_rate:float,initial_decline_rate:float,
                start_date,end_date,decline_exponent:float=0,forecast_frequency=ForecastFrequency.MONTH):
    dates,times=get_dates_and_times(start_date,end_date,forecast_frequency)

    if decline_exponent==0.0:
        rates=[initial_rate*math.exp(-initial_decline_rate*times[i]) for i in range(len(times))]
    else:
        rates=[initial_rate/((1.0+decline_exponent*initial_decline_rate*times[i])**(1/decline_exponent)) for i in range(len(times))]
    cums=[]
    cums.append(0)
    for i in range(1,len(times)):
        cums.append(cums[i-1]+rates[i]*(times[i]-times[i-1]))
    return dates,rates,cums



if __name__=="__main__":
    dates, rates,cums=get_arps_dc(500,0.0005,start_date=dt(2020,1,1),end_date=dt(2050,1,1),forecast_frequency=ForecastFrequency.QUARTER,decline_exponent=0.5)
    _, rates1,cums1=get_arps_dc(500,0.0005,start_date=dt(2020,1,1),end_date=dt(2050,1,1),forecast_frequency=ForecastFrequency.QUARTER,decline_exponent=0.0)
    _, rates2,cums2=get_arps_dc(500,0.0005,start_date=dt(2020,1,1),end_date=dt(2050,1,1),forecast_frequency=ForecastFrequency.QUARTER,decline_exponent=1.0)


    fig,ax=plt.subplots(figsize=(5,2.7))
    ax.plot(dates,rates)
    ax.plot(dates,rates1)
    ax.plot(dates,rates2)
    plt.show()
 
    output=[[dates[i].date(),rates[i],cums[i]] for i in range(len(dates))]
    print(tabulate(output))

 