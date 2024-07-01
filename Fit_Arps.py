from scipy.optimize import curve_fit
import Arps as arps
import datetime as dt
import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt

def arps_for_fit(time,initial_rate,decline_rate,decline_exponent):
    # if decline_exponent==0:
    #     decline_exponent=1e-8
    
    return initial_rate/((1.0+decline_exponent*decline_rate*time)**(1/decline_exponent))

dates, rates,_=arps.get_arps_dc(500,0.0005,start_date=dt.datetime(2020,1,1),end_date=dt.datetime(2050,1,1),forecast_frequency=arps.ForecastFrequency.QUARTER,decline_exponent=0.5)
times=[(dates[i]-dates[0]).days for i in range(len(dates))]
rates=np.random.normal(loc=np.array(rates),scale=np.array(rates)*(0.25*np.random.rand()))

popt, pcov=curve_fit(arps_for_fit,times,rates,bounds=([rates[0]*0.9,1e-8,1e-8],[rates[0]*1.1,1,1]))

fitted=[arps_for_fit(times[i],popt[0],popt[1],popt[2]) for i in range(len(times))]

outputs=[[times[i],rates[i],fitted[i]] for i in range(len(times))]
print(tabulate(outputs))


plt.plot(times,rates,'o')
plt.plot(times,fitted,'-')
plt.show()