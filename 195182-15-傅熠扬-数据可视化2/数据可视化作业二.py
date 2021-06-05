import plotly_express as px
import plotly
import pandas as pd
import numpy as np

file_path=open(r'C:\Users\lenovo\Desktop\data.csv')
file_data=pd.read_csv(file_path)
file_path=open(r'C:\Users\lenovo\Desktop\data.csv')
file_data=pd.read_csv(file_path)
file_data=file_data.fillna(value=0)
file_data=pd.concat([file_data.iloc[:,0:2],file_data.iloc[:,44:64]],axis=1)
data=file_data
data=data.set_index(['Country Name','Country Code'])
data=data.stack()
data.index=data.index.rename('year',level=2)
data.name='gdp'
data=data.reset_index()

fig=px.choropleth(
  data,  # 数据集
  locations="Country Code",  # 配合颜色color显示
  color="gdp", # 颜色的字段选择
  hover_name="Country Name",  # 悬停字段名字
  animation_frame="year",  # 注释
  color_continuous_scale=px.colors.sequential.Plasma,  # 颜色变化
  projection="natural earth"  # 全球地图
             )
plotly.offline.plot(fig, filename='global_gdf.html')

election=px.data.election()
fig=px.scatter_3d(
    election,  # 传入数据集
    x="Joly",  # 指定XYZ坐标轴的数据
    y="Coderre",  
    z="Bergeron",  
    color="winner",  # 颜色取值
    size="total",   # 大小取值
    hover_name="district_id",  # 指定颜色种类、大小和显示名称
    symbol="result",  # 右边的圆形和菱形
    color_discrete_map={"Joly":"red",
                        "Bergeron":"blue",
                        "Coderre":"green"}   # 改变默认颜色
)
plotly.offline.plot(fig, filename='election_3d.html')

tips=px.data.tips()
total_bill_bysex=tips.groupby(by='sex')["total_bill"].sum().reset_index()
total_bill_bysex
fig=px.pie(total_bill_bysex, # 绘图数据
       names="sex",  # 每个组的名字
       values="total_bill"  # 组的取值
      )
plotly.offline.plot(fig, filename='sex_bill.html')

gapminder = px.data.gapminder()
gapminder_1977= gapminder[gapminder["year"] == 1977]
fig=px.scatter(gapminder_1977,   # 传入的数据集
           x="gdpPercap",
           y="pop",
           color="continent"
          )
plotly.offline.plot(fig, filename='gapminder_1977.html')