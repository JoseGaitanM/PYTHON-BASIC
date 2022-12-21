import os
from datetime import datetime
import json
from lxml import etree

def generate(date: datetime.date):
    data=[]
    date = date.strftime("%Y_%m_%d")
    dic_header={}

    mean_temp_global = 0
    mean_wind_speed_global = 0
    coldest_place = float('inf')
    warmest_place = float('-inf')
    windiest_place = float('-inf')


    for city in sorted(os.listdir('source_data')):
        file = open("source_data/" + str(city) + '/' + str(date) + ".json")
        
        json_data = json.load(file)
        hours = json_data['hourly']

        min_temp = hours[0]['temp']
        max_temp = hours[0]['temp']
    

        min_wind_speed=hours[0]['wind_speed']
        max_wind_speed=hours[0]['wind_speed']


        sum_temp=0
        sum_wind_speed=0

        for hour in hours:
            temp=hour['temp']
            wind_speed=hour['wind_speed']

            sum_temp=sum_temp+temp
            sum_wind_speed=sum_wind_speed+wind_speed

            if (temp < min_temp):
                min_temp = temp
            elif (temp > max_temp):
                max_temp = temp
            
            if (wind_speed < min_wind_speed):
                min_wind_speed = wind_speed
            elif (wind_speed > max_wind_speed):
                max_wind_speed = wind_speed
        
        mean_temp=round(sum_temp/len(hours),2)
        mean_wind_speed=round(sum_wind_speed/len(hours),2)

        mean_temp_global=mean_temp_global+mean_temp
        mean_wind_speed_global=mean_wind_speed_global+mean_wind_speed


        if(mean_temp < coldest_place):
            dic_header['coldest_place']=city
            coldest_place = mean_temp
        if(mean_temp > warmest_place):
            dic_header['warmest_place']=city
            warmest_place = mean_temp
        if(mean_wind_speed > windiest_place):
            dic_header['windiest_place']=city
            windiest_place = mean_wind_speed
        
        
        dic={'city':str(city).replace(" ", "_"),'mean_temp':mean_temp,"mean_wind_speed":mean_wind_speed,"min_temp":min_temp,"min_wind_speed":min_wind_speed,"max_temp":max_temp,"max_wind_speed":max_wind_speed}
        data.append(dic)

    number_cities=len(os.listdir('source_data'))
    mean_temp_global = round(mean_temp_global/number_cities,2)
    mean_wind_speed_global = round(mean_wind_speed_global/number_cities,2)
    dic_header['mean_temp']=mean_temp_global
    dic_header['mean_wind_speed']=mean_wind_speed_global

    weather = etree.Element("weather", country="Spain", date=date.replace("_", "-"))

    summary = etree.SubElement(weather, "summary",
                               attrib={"mean_temp": str(dic_header['mean_temp']),
                                       "mean_wind_speed": str(dic_header['mean_wind_speed']),
                                       "coldest_place": dic_header['coldest_place'],
                                       "warmest_place": dic_header['warmest_place'],
                                       "windiest_place": dic_header['windiest_place']}
                               )

    cities = etree.SubElement(weather, "cities")

    for x in data:
        city=etree.SubElement(cities, x['city'],
                               attrib={"mean_temp": str(x['mean_temp']),
                                       "mean_wind_speed": str(x['mean_wind_speed']),
                                       "min_temp": str(x['min_temp']),
                                       "min_wind_speed": str(x['min_wind_speed']),
                                       "max_temp": str(x['max_temp']),
                                       "max_wind_speed": str(x['max_wind_speed'])}
                               )

    file = open("Spain_weather_" + date + ".xml", 'w')
    file.write(etree.tostring(weather, pretty_print=True).decode())



    

    



        

if __name__ == '__main__':
    date_str='2021/09/25'
    format = '%Y/%m/%d'
    date=datetime.strptime(date_str, format).date()
    
    generate(date)