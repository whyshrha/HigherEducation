import pandas as pd
import numpy as np

data = pd.read_csv('./yansong/data/network_summary_机构新.csv',encoding='gb2312')
data_sch= pd.read_excel('./yansong/data/全国高等学校名单.xls')

sch = pd.DataFrame(data_sch['Unnamed: 1'])
sch = sch.dropna()
sch = sch.iloc[1:,:]
sch = sch.reset_index(drop=True)
sch = sch.rename(columns={'Unnamed: 1':'学校名称'})
sch_list = list(sch['学校名称'])
data = data[['Freq','Author']]
data['Author'] = data['Author'].str.replace('(','（')
data['Author'] = data['Author'].str.replace(')','）')

number = []
for name in sch_list:
    num = data[data['Author'].str.contains(name)]['Freq'].sum()
    number.append(num)


number = pd.DataFrame(number)
result_1 = sch.join(number)
result_1 = result_1.rename(columns={0:'出现频数'})

result_1.to_csv('./yansong/output_data/question1.csv',encoding='utf_8_sig')

##########################################################################################
# 问题一

data = pd.read_csv('./yansong/output/第一作者单位统计.csv')
data_sch= pd.read_csv('./yansong/output_data/终于搞定的最终版.csv')

data = data.drop('Unnamed: 0',axis=1)
data = data.rename(columns={'index':'Author','0':'Freq'})
data_sch = data_sch.drop('Unnamed: 0',axis=1)
data_sch = data_sch.rename(columns={'出现频数':'出现频数_原始'})
sch_list = list(data_sch['学校名称'])

data['Author'] = data['Author'].str.replace('(','（')
data['Author'] = data['Author'].str.replace(')','）')

number = []
for name in sch_list:
    num = data[data['Author'].str.contains(name)]['Freq'].sum()
    number.append(num)

number = pd.DataFrame(number)
result_1 = data_sch.join(number)
result_1 = result_1.rename(columns={0:'出现频数_New'})
result_1['出现频数_New'] = result_1['出现频数_New'].astype('int')

result_1.to_csv('./yansong/output_data/最最终版0917.csv',encoding='utf_8_sig')

##########################################################################################
# 问题二

for name in sch_list:
    data[name] = np.where(data['Author'].str.contains(name),1,0)


data_middle = data.loc[:,'北京大学':'新疆工业职业技术学院']
data['Col_sum'] = data_middle.apply(lambda x: x.sum(), axis=1)
data_include = data[['Freq','Author','Col_sum']]
result_2 = data_include[data_include['Col_sum'] == 0]
result_2 = result_2.iloc[:,:2]

result_2.to_csv('./yansong/output_data/except_university.csv',encoding='utf_8_sig')


##########################################################################################
# 问题三

data = pd.read_csv('./yansong/output_data/question1.csv')
data = data.drop('Unnamed: 0',axis=1)

data2 = pd.read_excel('./yansong/data/需要合并的数据（更新8所）.xlsx')
data2 = data2[['Author','Freq']]
data2 = data2.rename(columns={'Author':'学校名称','Freq':'出现频数'})

data_result = pd.concat([data,data2])
data_final = data_result['出现频数'].groupby(data_result['学校名称']).sum()
data_finals = pd.DataFrame(data_final).sort_values(by=['出现频数'],ascending=False)

data_finals.to_csv('./yansong/output_data/frequency_univ.csv',encoding='utf_8_sig')

data_test = data.set_index('学校名称')
data_finals.drop(data_test.index)
data_finals[data_finals.index=='淮北师范大学']
data[data['学校名称']=='淮北师范大学']
data2[data2['学校名称']=='淮北师范大学']

##########################################################################################
# 问题四

data_sch= pd.read_excel('./yansong/data/全国高等学校名单.xls',skiprows=2)

data_sch = data_sch[pd.isnull(data_sch['学校名称'])==False]
data_sch['所在地'] = data_sch['所在地'].str.replace("\n", "")
data_sch['学校名称'] = data_sch['学校名称'].str.replace("\n", "")
data_sch['主管部门'] = data_sch['主管部门'].str.replace("\n", "")

data = pd.read_excel('./yansong/data/五类学校信息.xlsx')
data = data[['学校','院校层次1','院校层次2','院校层次3']]

data_result = pd.merge(data_sch,data,how='left',left_on='学校名称',right_on='学校')

data_result = data_result.drop('学校',axis=1)

# data_result['院校层次']
data_result['院校层次1'] = np.where(data_result['院校层次1']==985.0,1,0)
data_result['院校层次2'] = np.where(data_result['院校层次2']==211.0,1,0)

data_result['院校层次']=None
for i in range(len(data_result)):
    if data_result['院校层次1'][i]==1:
        data_result['院校层次'][i]=1
    elif data_result['院校层次1'][i]!=1 & data_result['院校层次2'][i]==1:
        data_result['院校层次'][i]=2
    else:
        data_result['院校层次'][i]=data_result['院校层次3'][i]

data_result['院校层次_1'] = np.where(pd.isnull(data_result['院校层次']),6,data_result['院校层次'])
data_result['公私属性'] = np.where(pd.isnull(data_result['备注']),1,2)
data_result1 = data_result[['学校名称','主管部门','所在地','办学层次','院校层次_1','公私属性']]
data_result1 = data_result1.rename(columns={'院校层次_1':'院校层次'})

data_freq = pd.read_csv('./yansong/output_data/frequency_univ.csv')
data_freq['学校名称'] = data_freq['学校名称'].str.replace("\n", "")

result = pd.merge(data_result1,data_freq,how='inner',left_on='学校名称',right_on='学校名称')

result['院校层次'] = result['院校层次'].astype(int)
result.to_csv('./yansong/output_data/终于搞定的最终版.csv',encoding='utf_8_sig')

##########################################################################################
# 问题五

data = pd.read_excel('./yansong/data/2016全国普通高校名单.xlsx')
data_2595 = data[pd.isnull(data['学校名称'])==False]

data_2631 = pd.read_csv('./yansong/output_data/终于搞定的最终版.csv')

data_left = pd.merge(data_2631,data_2595,how='left',left_on='学校名称',right_on='学校名称')
result1 = data_left[pd.isnull(data_left['主管部门_y'])]
result1 = result1[['学校名称','主管部门_x','所在地_x','办学层次_x','院校层次','公私属性','出现频数']]
result1.to_csv('./yansong/output_data/2631独特部分.csv',encoding='utf_8_sig')

data_right = pd.merge(data_2631,data_2595,how='right',left_on='学校名称',right_on='学校名称')
result2 = data_right[pd.isnull(data_right['公私属性'])]
result2 = result2[['学校名称','主管部门_y','所在地_y','办学层次_y']]
result2.to_csv('./yansong/output_data/2595独特部分.csv',encoding='utf_8_sig')


##########################################################################################
# 问题六
### 所有年份的关键词统计

import os
import codecs
import shutil

def extract_word(path,files,keywords):
    output_word = []
    for file in files:
        if file !='.DS_Store':  #如果不是文件夹的话
            file_path = path + "/" + file
            with codecs.open(file_path, 'r', 'utf-8') as f:
                for line in f.readlines():
                    obj = line.split(" ")
                    if obj[0] == keywords:
                        words = obj[1].replace(";",",").replace(";;",",").replace("\r\n","").split(",")
                        for w in words:
                            output_word.append(w)
    return output_word


def count_keyword(key_list):
    map1 = {}
    for w in key_list:
        if w not in map1:
            map1[w] = 1
        else:
            map1[w] = map1[w]+1

    # print(map1)
    aaa = pd.DataFrame(map1,index=[0]).T
    result = aaa.sort_values(by=0,ascending=False)
    return result


path = "/Users/haoyuwu/Documents/个人文档/教学学院项目/yansong/withAD"  # 文件夹目录
files = os.listdir(path)
output = extract_word(path,files,'K1')
result = count_keyword(output)
result = result.iloc[1:,:]
result.to_csv('./yansong/output/所有年份关键词统计6000.csv',encoding='utf_8_sig')


### 所有年份作者统计
path = "/Users/haoyuwu/Documents/个人文档/教学学院项目/yansong/rawdata/data"  # 文件夹目录
files = os.listdir(path)
output = extract_word(path,files,'A1')
result = count_keyword(output)
result = result.iloc[1:,:]
result.to_csv('./yansong/output/所有年份作者所在行统计.csv',encoding='utf_8_sig')

# withAD
path = "/Users/haoyuwu/Documents/个人文档/教学学院项目/yansong/withAD"  # 文件夹目录
files = os.listdir(path)
output = extract_word(path,files,'A1')
result = count_keyword(output)
result = result.iloc[1:,:]
result.to_csv('./yansong/output/所有年份作者所在行统计.csv',encoding='utf_8_sig')


### 所有机构统计
path = "/Users/haoyuwu/Documents/个人文档/教学学院项目/yansong/rawdata/data"  # 文件夹目录
files = os.listdir(path)
output = extract_word(path,files,'AD')
result = count_keyword(output)
result = result.iloc[1:,:]
result.to_csv('./yansong/output/所有年份所有单位统计.csv',encoding='utf_8_sig')

# withAD
path = "/Users/haoyuwu/Documents/个人文档/教学学院项目/yansong/withAD"  # 文件夹目录
files = os.listdir(path)
output = extract_word(path,files,'AD')
result = count_keyword(output)
result = result.iloc[1:,:]
result.to_csv('./yansong/output/所有年份所有单位统计6000.csv',encoding='utf_8_sig')


### 第一作者机构统计

def extract_word_first(path,files,keywords):
    data_jigou=[]
    for file in files:
        if file!='.DS_Store':  #如果不是文件夹的话
            file_path = path + "/" + file
            with codecs.open(file_path, 'r', 'utf-8') as f:
                for line in f.readlines():
                    obj = line.split(" ")
                    if obj[0] == keywords:
                        words = obj[1].replace(";",",").replace(";;",",").replace("\r\n","").split(",")
                        data_jigou.append(words[0])
    return data_jigou


path = "/Users/haoyuwu/Documents/个人文档/教学学院项目/yansong/rawdata/data"  # 文件夹目录
files = os.listdir(path)
data_jigou = extract_word_first(path,files,'AD')
data_jigou = pd.DataFrame(data_jigou)
data_jigou = pd.DataFrame(data_jigou[0].value_counts())
aaa = data_jigou.reset_index()
aaa.to_csv('./yansong/output/第一作者单位统计.csv',encoding='utf_8_sig')

path = "/Users/haoyuwu/Documents/个人文档/教学学院项目/yansong/withAD"  # 文件夹目录
files = os.listdir(path)
data_jigou = extract_word_first(path,files,'AD')
data_jigou = pd.DataFrame(data_jigou)
data_jigou = pd.DataFrame(data_jigou[0].value_counts())
aaa = data_jigou.reset_index()
aaa.to_csv('./yansong/output/第一作者单位统计.csv',encoding='utf_8_sig')

### 统计有无AD字段
path = "/Users/haoyuwu/Documents/个人文档/教学学院项目/yansong/rawdata/data"  # 文件夹目录
pathwithAD = '/Users/haoyuwu/Documents/个人文档/教学学院项目/yansong/withAD/'
pathwithoutAD = '/Users/haoyuwu/Documents/个人文档/教学学院项目/yansong/withoutAD/'
files = os.listdir(path)
for file in files:
    file_path = path + "/" + file
    with codecs.open(file_path, 'r', 'utf-8') as f:
        file_str = f.read()
        if 'AD' in file_str:
            shutil.copyfile(file_path,pathwithAD + '/' + file) 
        else:
            shutil.copyfile(file_path,pathwithoutAD + '/' + file) 


# 统计文件夹下文件的个数
def countnum(path):
    count = 0
    for file in os.listdir(path):
        count = count+1
    return count

pathnum = countnum(path)
print(pathnum)
pathAD = countnum(pathwithAD)
print(pathAD)
pathoutAD = countnum(pathwithoutAD)
print(pathoutAD)
# 每个下面有个隐藏文件
# 7445
# 6710
# 735

### 对年份进行分类
pathwithAD = '/Users/haoyuwu/Documents/个人文档/教学学院项目/yansong/withAD/'
files = os.listdir(pathwithAD)
for file in files:
    file_path = path + "/" + file
    year_array = file.split("_")
    year_str=year_array[1][0:4]
    if not os.path.exists('/Users/haoyuwu/Documents/个人文档/教学学院项目/yansong/year/'+year_str):
        os.mkdir('/Users/haoyuwu/Documents/个人文档/教学学院项目/yansong/year/'+year_str)
    else:
        shutil.copyfile(file_path,'/Users/haoyuwu/Documents/个人文档/教学学院项目/yansong/year/'+year_str + '/' + file)



## 对每年的进行统计
### 每年的K1
fileyear = '/Users/haoyuwu/Documents/个人文档/教学学院项目/yansong/year'
files = os.listdir(fileyear)
print(files)
for name in files:
    if name!='.DS_Store':
        file = os.listdir(fileyear + '/'+ name)
        output = extract_word(fileyear + '/'+ name,file,'K1')
        result = count_keyword(output)
        result = result.iloc[1:,:]
        result.to_csv('./yansong/year_output_K1/'+name+'.csv',encoding='utf_8_sig')



### 每年的AD
fileyear = '/Users/haoyuwu/Documents/个人文档/教学学院项目/yansong/year/'
files = os.listdir(fileyear)
print(files)
for name in files:
    if name!='.DS_Store':
        file = os.listdir(fileyear + '/'+ name)
        output = extract_word(fileyear + '/'+ name,file,'AD')
        result = count_keyword(output)
        result = result.iloc[1:,:]
        result.to_csv('./yansong/year_output_AD/'+name+'.csv',encoding='utf_8_sig')




### 每年的A1
fileyear = '/Users/haoyuwu/Documents/个人文档/教学学院项目/yansong/year/'
files = os.listdir(fileyear)
print(files)
for name in files:
    if name!='.DS_Store':
        file = os.listdir(fileyear + '/'+ name)
        output = extract_word(fileyear + '/'+ name,file,'A1')
        result = count_keyword(output)
        result = result.iloc[1:,:]
        result.to_csv('./yansong/year_output_A1/'+name+'.csv',encoding='utf_8_sig')





### 每年的第一机构
fileyear = '/Users/haoyuwu/Documents/个人文档/教学学院项目/yansong/year/'
files = os.listdir(fileyear)
print(files)
if name!='.DS_Store':
    file = os.listdir(fileyear + '/'+ name)
    output = extract_word_first(fileyear + '/'+ name,file,'AD')
    result = count_keyword(output)
    result.to_csv('./yansong/year_output_ADfirst/'+name+'.csv',encoding='utf_8_sig')


### 统计年份的篇数
import os
import codecs
import pandas as pd

path = "/Users/haoyuwu/Documents/个人文档/教学学院项目/yansong/withAD"  # 文件夹目录
files = os.listdir(path)
year_map = {}

for file in files:
    if not os.path.isdir(file):  #如果不是文件夹的话
        year_array = file.split("_")
        if len(year_array) != 2:
            continue
        year_str=year_array[1][0:4] # 按下划线分割字符串，取数组第二个元素的钱四个字符作为年份 e.g. download_200712006.txt
        if year_str not in year_map:
            year_map[year_str] = 1
        else:
             year_map[year_str] += 1
                
print(year_map)

paper_num = pd.DataFrame(year_map,index=[0]).T
paper_num.to_csv('./yansong/output/每年发文量的统计.csv',encoding='utf_8_sig')


##########################################################################################
# 问题七


year = []
ke = []
rencai = []
jiaoxue = []
path = '/Users/haoyuwu/Documents/个人文档/教学学院项目/yansong/year_output_K1/'
files = os.listdir(path)
for file in files:
    if file !='.DS_Store':
        data = pd.read_csv(path + file)
        data_ke = data[data['Unnamed: 0'].str.contains('课')]
        data_rencai = data[data['Unnamed: 0'].str.contains('人才培养')]
        data_jiaoxue = data[data['Unnamed: 0'].str.contains('教学')]
        year.append(file[0:4])
        ke.append(data_ke['0'].sum())
        rencai.append(data_rencai['0'].sum())
        jiaoxue.append(data_jiaoxue['0'].sum())


year = pd.DataFrame(year)
ke = pd.DataFrame(ke)
ke = ke.rename(columns={0:'含课个数'})
rencai = pd.DataFrame(rencai)
rencai = rencai.rename(columns={0:'人才培养个数'})
jiaoxue = pd.DataFrame(jiaoxue)
jiaoxue = jiaoxue.rename(columns={0:'教学个数'})
result = year.join(ke,rencai,jiaoxue)
result = year.join([ke,rencai,jiaoxue])
result = result.rename(columns={0:'年份'})
result = result.sort_values(by='年份') 
result = result.reset_index(drop=True)

result.to_csv('./yansong/output_data/特别关键词.csv',encoding='utf_8_sig')

##########################################################################################
# 问题八
data = pd.read_excel('./yansong/data/清洗后的高校名单.xlsx',header=None)
data = data.rename(columns={0:'出现频数',1:'学校名称'})

data_all = pd.read_csv('./yansong/output_data/最最终版0917.csv')
data_all = data_all.drop(['Unnamed: 0','出现频数_原始'],axis=1)
data_all = data_all.rename(columns={'出现频数_New':'出现频数'})

data1 = data_all[['学校名称','出现频数']]
data_m = pd.concat([data1,data])
data_final = data_m['出现频数'].groupby(data_m['学校名称']).sum()
data_finals = pd.DataFrame(data_final).sort_values(by=['出现频数'],ascending=False)
data_finals = data_finals.reset_index()

data_result = pd.merge(data_all,data_finals,how='left',left_on='学校名称',right_on='学校名称')
data_result = data_result.drop(['出现频数_x'],axis=1)
data_result = data_result.rename(columns={'出现频数_y':'出现频数'})

data_right = pd.merge(data_all,data,how='right',left_on='学校名称',right_on='学校名称')
data_ri = data_right[pd.isnull(data_right['出现频数_x'])]
data_ri = data_ri[['学校名称','出现频数_y']]
data_ri.to_csv('./yansong/output_data/最终未分配0919.csv',encoding='utf_8_sig')

data_result.to_csv('./yansong/output_data/这个真的是最终的0919.csv',encoding='utf_8_sig')

##########################################################################################
# 问题九
result = []
years = []
fileyear = '/Users/haoyuwu/Documents/个人文档/教学学院项目/yansong/year_output_K1/'
files = os.listdir(fileyear)
print(files)
for name in files:
    if name!='.DS_Store':
        file = pd.read_csv(fileyear + '/'+ name)
        year = name[0:4]
        res = file['0'].sum()
        years.append(year)
        result.append(res)


years = pd.DataFrame(years)
result = pd.DataFrame(result)
years = years.reset_index()
result = result.reset_index()

final = pd.merge(years,result,how='inner',left_on='index',right_on='index')
final = final.drop(['index'],axis=1)
final = final.rename(columns={'0_x':'year','0_y':'sum'})
final = final.sort_values(by='year')
final = final.reset_index(drop=True)

final.to_csv('./yansong/output_data/nine.csv',encoding='utf_8_sig')







