from tkinter import *
import requests 
import json
import urllib
from PIL import Image,ImageTk
import cred

root = Tk()
root.title('WeaQ')
root.geometry('280x280')


def search(lat,long):
    global iconTk
    
    root.columnconfigure(0,weight=1)
    root.columnconfigure(2,weight=1)
    lat_label.grid_remove()
    long_label.grid_remove()
    latitude.grid_remove()
    longitude.grid_remove()
    searchBut.grid_remove()
    
    
    try:
        try:
            
            cityLab.destroy()
            temperatureFrame.destroy()
            weatherFrame.destroy()
            aqiFrame.destroy()
        except:
            pass
        finally: 
            #Getting the API request from openweathermap based on the latitude and longitude provided
            weather_req = requests.get('http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}'.format(lat,long,cred.weather_api_key))
            weather = json.loads(weather_req.content)

            #Getting the weather description and icon from the request result
            weath = weather['weather'][0]['description']
            icon_id = weather['weather'][0]['icon']
            
            urllib.request.urlretrieve('http://openweathermap.org/img/wn/{}@2x.png'.format(icon_id),'icon')
            icon = Image.open('icon')
            iconTk = ImageTk.PhotoImage(icon)
            
            
            day_night = icon_id[2]
            temp = weather['main']['temp'] - 273.15
            
            #Checking if it is day or night
            if day_night == 'd':
                color_day = 'white'
                txt_color = 'black'
            if day_night == 'n':
                color_day = 'gray'
                txt_color = 'white'

            
            
            #Getting the AQI index from airowapi
            
            api_req = requests.get('https://www.airnowapi.org/aq/observation/latLong/current/?format=application/json&latitude={}&longitude={}&distance=100&API_KEY={}'.format(lat,long,cred.aqi_api_key))
            api = json.loads(api_req.content)
            
            city = api[0]['ReportingArea']
            quality = api[0]['AQI']
            category = api[0]['Category']['Name']
            if category == 'Good':
                color_weather = 'green'
            elif category == 'Moderate':
                color_weather = 'yellow'
            elif category=='Unhealthy for Sensitive Groups':
                color_weather = 'orange'
            elif category == 'Unhealthy':
                color_weather = 'red'
            elif category == 'Very Unhealthy':
                color_weather = 'purple'
            elif category == 'Hazardous':
                color_weather = 'maroon'

            #Heading
            cityLab = Label(root,text=city,font = ('Bahnschrift Light',20))
            cityLab.grid(row=0,column=1,pady=(0,10))

            #Temperature
            temperatureFrame = LabelFrame(root,background=color_day)
            temperatureFrame.grid(column=1,row=1)
            tempLabel = Label(temperatureFrame,text='Temperature ' + str(int(temp))+'°C',font = ('Bahnschrift Light',15),
                              background=color_day,fg = txt_color,padx=35)
            tempLabel.grid(row=0,column=1)



            #Weather
            weatherFrame = LabelFrame(root)
            weatherFrame.grid(column=1,row=2)
            iconLabel = Label(weatherFrame,image = iconTk)
            iconLabel.grid(row =0,column=0)
            weatherLabel = Label(weatherFrame,text=weath,font = ('Bahnschrift Light',15))
            weatherLabel.grid(row=0,column=1)


            #AQI
            aqiFrame = LabelFrame(root)
            aqiFrame.grid(column=1,row=3)
            myLabel = Label(aqiFrame,text='Air Quality ' + str(quality) + '  ' + category,font = ('Bahnschrift Light',15),background=color_weather)
            myLabel.pack()


            

    except Exception as e:
            Label(root,text='Location data not available').grid(row=1,column=1)
            api = 'Error'


root.columnconfigure(0,weight=1)
root.columnconfigure(3,weight=1)



lat_label = Label(root,text='Latitude',font = ('Bahnschrift Light',15))
lat_label.grid(row=0,column=1)
latitude = Entry(root,width=10,borderwidth=2)
latitude.grid(row=0,column=2)

long_label = Label(root,text='Longitude',font = ('Bahnschrift Light',15))
long_label.grid(row=1,column=1)
longitude = Entry(root,width=10,borderwidth=2)
longitude.grid(row=1,column=2)


searchBut = Button(root,text='Search',font = ('Bahnschrift Light',15),command = lambda : search(latitude.get(),longitude.get()))
searchBut.grid(row = 3,column=1, columnspan = 2)


root.mainloop()