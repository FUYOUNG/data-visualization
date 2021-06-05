import pandas as pd
import requests
import pandas as pd
import time
import json

file_path=open(r'C:\Users\lenovo\Desktop\zufangdata.csv',encoding="GBK")
file_data=pd.read_csv(file_path)
file_data['位置']='武汉市'+file_data['区域'].values+'区'+file_data['小区名称'].values
file_data=file_data.loc[file_data['区域']=='江夏']
file_data=file_data.groupby(['位置'],as_index=False)['位置'].agg({'cnt':'count'})

class LngLat:
    # 获取一列的位置数据
    def get_data(self):
        house_names = file_data['位置']
        house_names = house_names.tolist()
        return house_names, file_data['cnt']

    def get_url(self):
        url_temp = "http://api.map.baidu.com/geocoding/v3/?address={}&output=json&ak=C8lrjvVvwLK18eyDu7S5BtB4jRYNWPaE&callback=showLocation"
        house_names, house_nums = self.get_data()
        return [url_temp.format(i) for i in house_names], [int(i) for i in house_nums]

    # 发送请求
    def parse_url(self, url):
        while 1:
            try:
                r = requests.get(url)
            except requests.exceptions.ConnectionError:
                time.sleep(2)
                print("等待中.....")
                continue
            return r.content.decode('UTF-8')

    def run(self):
        li = []
        urls, nums = self.get_url()
        for i in range(len(urls)):
            data = self.parse_url(urls[i])
            str = data.split("{")[-1].split("}")[0]
            try:
                lng = float(str.split(",")[0].split(":")[1])
                lat = float(str.split(",")[1].split(":")[1])
            except ValueError:
                continue

            dict_data = dict(lng=lng, lat=lat, count=nums[i])
            li.append(dict_data)
        f = open(r'C:\Users\lenovo\Desktop\经纬度信息.txt', 'w')
        f.write(json.dumps(li))
        f.close()
        print('正在写入...')
        print('写入成功')

if __name__ == '__main__':
    execute = LngLat()
    execute.run()