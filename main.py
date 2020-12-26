try:
    import config
except:
    print('No config fond!')
    exit()
try:
    import yandex_weather_api
    import matplotlib.pyplot as plt
    import pymysql
    import requests
    import datetime
    import time
except:
    print('some required libraries not found!')
    exit()


class weahter:
    """просто __init__ =)"""
    def __init__(self):
        self.temp = None
        self.wind_dir = None
        self.wind_speed = None
        self.condition = None

        
    """Актуаьлная погода"""
    def now(self):
        try:
            weahter1 = yandex_weather_api.get(requests, config.apikey, lat = config.lat , lon=config.lon)
            now = (weahter1['fact'])
            self.temp = str(now['temp'])
            self.wind_dir = str(now['wind_dir'])
            self.wind_speed= str(now['wind_speed'])
            self.condition= str(now['condition'])
        except:
            print('No enternet connection')
            self.temp = '0'
            self.wind_dir = '0'
            self.wind_speed= '0'
            self.condition= '0'            
        
        return(self)


    """Возвращает все значения в форме
    Температура(str), Направление ветра (стр) скорость ветра (str), облочность (стр)"""
    def reportall(self):
        return(self.temp, self.wind_dir, self.wind_speed, self.condition)

def sql_init():
    sesion = pymysql.Connection(host = config.mysql_server_addres , user = config.mysql_server_user, password = config.mysql_server_pass, database = config.db)
    sesion.connect()
    cursor = sesion.cursor()
    return(sesion, cursor)


def sqladd(w1, cursor, sesion):
    corteg = w1.reportall()
    date = datetime.datetime(2000, 1,1, 1, 1, 1 )
    date = date.now()
    datel = date.strftime('%Y-%m-%d-%H-%M')
    cursor.execute('insert into weather values(\''+corteg[0]+'\' , \''+corteg[1]+'\' , \''+corteg[2]+'\' , \''+datel+'\', \''+corteg[3]+'\' );')
    sesion.commit()

def getat(cursor):
    temp = []
    windd = []
    winds = []
    con = []
    date = []
    cursor.execute('select * from weather')
    resp = cursor.fetchall()
    for data in resp:
        temp.append(data[0])
        windd.append(data[1])
        winds.append(data[2])
        con.append(data[4])
        date.append(data[3])
    res = {'temp' : temp, 'windd' : windd, 'winds' : winds, 'date' : date, 'con' : con}
    return(res)
    
def tempg(res):
    temlist = res['temp']
    datelist = res['date']
    
    plt.plot(datelist, temlist)
    print(type(plt.show()))



    
if __name__ == '__main__':
    while True:
        a = weahter()
        a = a.now()
        s, c = sql_init()
        sqladd(a, c, s)
    #    res = getat(c)
    #    tempg(res)
        time.sleep(3600)
