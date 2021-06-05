import jieba
topn=1000
text = open(r'C:\Users\lenovo\Desktop\斗破苍穹.txt', "r", encoding='gbk').read()#读取文件
stopwords = [line.rstrip() for  line in open(r'停用词.txt',encoding = 'utf-8')]
words=jieba.lcut(text.strip())
counts={}
for word in words:
    if len(word)==1:
        continue
    elif word not in stopwords:
        counts[word]=counts.get(word,0)+1
items=list(counts.items())
items.sort(key=lambda x:x[1],reverse=True)
f=open('词频.txt','w')
for i in range (topn):
    word,count=items[i]
    f.writelines("{}\t{}\n".format(word,count))
f.close()
import wordcloud
import matplotlib.pyplot as plt
from imageio import imread

f=open('词频.txt','r')
txt=f.read()
pic=imread('背景.jpg')
wcloud = wordcloud.WordCloud(background_color='white',
                    font_path=r'C:\Windows\Fonts\simhei.ttf',
                    height=1200,
                    width=1600,
                    max_words=500,
                    mask=pic,
        random_state=100,).generate(txt)
wcloud.to_file('斗破苍穹.jpg')
plt.imshow(wcloud)
plt.axis('off')
plt.show()
import re
from pyecharts import options as opts
lst_chapter=[]
chapter=re.findall("第[0-9]+章",text)
for x in chapter:
    if x not in lst_chapter:
        lst_chapter.append(x)
        
lst_start_chapterindex=[]
for x in lst_chapter:
    lst_start_chapterindex.append(text.index(x))


lst_end_chapterindex=lst_start_chapterindex[1:]+[len(text)]
lst_chapterindex=list(zip(lst_start_chapterindex,lst_end_chapterindex))

xiaoyan=[]
for ii in range(150):
    start=lst_chapterindex[ii][0]
    end=lst_chapterindex[ii][1]
    xiaoyan.append(text[start:end].count("萧炎"))
xiaoyan.insert(0,0)
from pyecharts.charts import Line
columns=[]
for iii in range(151):
    columns.append(iii)

line = Line()
line.add_xaxis(columns)
line.add_yaxis("萧炎出场",xiaoyan)
line.set_global_opts(
        title_opts=opts.TitleOpts(title="前150章萧炎出场数"),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
        xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
    )
line.render("前150萧炎出场数.html")
import matplotlib.pyplot as plt
cnt_chap=[]
cnt_word=[]
for ii in range(30):
    start=lst_chapterindex[ii][0]
    end=lst_chapterindex[ii][1]
    cnt_chap.append(text[start:end].count('\n'))
    cnt_word.append(len(text[start:end]))

plt.figure(figsize=(14,12))
plt.scatter(cnt_chap,cnt_word)
for ii in range(30):
    plt.text(cnt_chap[ii]-2,cnt_word[ii]+100,lst_chapter[ii],Fontproperties='SimHei',size=15)
plt.xlabel("章节段数",Fontproperties='SimHei',fontsize=15)
plt.ylabel("章节字数",Fontproperties='SimHei',fontsize=15)
plt.title("斗破苍穹前30",Fontproperties='SimHei')
plt.savefig('斗破前30.png')
text = open(r'C:\Users\lenovo\Desktop\斗破苍穹.txt', "r", encoding='gbk').read()#读取文件
Names=['萧炎','小医仙','美杜莎','云韵','紫研','海波','纳兰','韩枫','药老','苏千','萧厉','雅妃']
relations={}
lst_para=text.split('\n')
for t in lst_para:
    for name1 in Names:
        if name1 in t:
            for name2 in Names:
                if name2 in t and name1!=name2 and (name2,name1) not in relations:
                    relations[(name1,name2)]=relations.get((name1,name2),0)+1
maxRela=max([v for k,v in relations.items()])
relations={k:v/maxRela for k,v in relations.items()}
print(relations.items())
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif']=['SimHei']

plt.figure(figsize=(15,15))
G=nx.Graph()

for k,v in relations.items():
    G.add_edge(k[0],k[1],weight=v)

elarge=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight']>0.6]
emidle=[(u,v) for (u,v,d) in G.edges(data=True) if (d['weight']>0.3) & (d['weight']<=0.6)]
esmall=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight']<=0.3]

pos=nx.circular_layout(G)
nx.draw_networkx_nodes(G,pos,alpha=0.6,node_size=4000)
nx.draw_networkx_edges(G,pos,edgelist=elarge,width=2.5,alpha=0.9,edge_color='g')
nx.draw_networkx_edges(G,pos,edgelist=emidle,width=1.5,alpha=0.6,edge_color='y')
nx.draw_networkx_edges(G,pos,edgelist=esmall,width=1,alpha=0.2,edge_color='b',style='dashed')
nx.draw_networkx_labels(G,pos,font_size=18)
plt.axis('off')
plt.title('斗破苍穹主要人物社交关系网络图')
plt.savefig('斗破苍穹主要人物社交关系网络图.png')