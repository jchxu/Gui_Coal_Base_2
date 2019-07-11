# coding=utf-8
import pandas as pd
import numpy as np
import sys,re
#pd.set_option('display.max_columns', None)
### 进度条相关
def report_progress(progress, total):
    ratio = progress / float(total)
    percentage = round(ratio * 100)
    length = 80
    percentnums = round(length*ratio)
    buf = '\r[%s%s] %d%%' % (('>'*percentnums),('-'*(length-percentnums)), percentage)
    sys.stdout.write(buf)
    sys.stdout.flush()
def report_progress_done():
    sys.stdout.write('\n')

### 逐个读取excel/csv数据文件
def read_data(self,datafiles):     #GUI程序用
#def read_data(datafiles):           #测试程序用
    dflist = []
    for i in range(len(datafiles)):
        datafile = datafiles[i]
        if (datafile.split('.')[-1] == 'xls') or (datafile.split('.')[-1] == 'xlsx'):
            print('读取Excel文件:', datafile)                         #测试程序用
            self.textEdit.append('读取Excel数据文件:%s' % datafile)   #GUI程序用
            df = pd.read_excel(datafile)
            dflist.append(df)
        elif (datafile.split('.')[-1] == 'csv'):
            print('读取CSV文件:', datafile)                       #测试程序用
            self.textEdit.append('读取CSV数据文件:%s' % datafile) #GUI程序用
            file = open(datafile)
            df = pd.read_csv(file)
            dflist.append(df)
            file.close()
    if len(dflist)>0:
        dfs = pd.concat(dflist, ignore_index=True, sort=False)
        #print(dfs)
        return dfs

### 判断字符是否为数字，若为数字，则保留一位小数返回
def numformat(itemvalue):
    pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
    result = pattern.match(itemvalue)
    pattern2 = re.compile(r'^[12]')
    result2 = pattern2.match(itemvalue)
    if result:
        if ('.' in itemvalue):
            if (int(itemvalue.split('.')[1])==0) and (len(itemvalue.split('.')[0])==4):
                floatvalue = str(int(itemvalue.split('.')[0]))      #年份.0
            else:
                floatvalue = ("%.1f" % float(itemvalue))    #有小数点，但.后0和.前4位数字不同符合
        elif (len(itemvalue) == 4) and (result2):
            floatvalue = ("%d" % float(itemvalue))      #没有小数点，总共4位,以1或2开头
        else:
            floatvalue = ("%.1f" % float(itemvalue))    #没有小数点，位数非4位
        return floatvalue
    else: return itemvalue

### 获取基础煤种的原始数据
#def get_Base_coal(self,dfs):
def get_Base_coal(dfs):
    namelist = dfs['煤名称'].tolist()
    yearlist = dfs['年份'].tolist()
    unique_name = list(set(namelist))
    # 获取每个煤名称对应的年份
    name_year = {}
    for item in unique_name:
        name_year[item] = []
    for i in range(len(namelist)):
        name_year[namelist[i]].append(int(yearlist[i]))
    # 获取次数并判断是否属于基础煤种
    base_name = []
    base_reason = {}
    for item in unique_name:
        years = name_year[item]
        years.sort()
        # 获取三个时间段内使用的年数
        list1996 = []
        list2009 = []
        list2015 = []
        for yy in years:
            if (yy >= 1996): list1996.append(yy)
            if (yy >= 2009): list2009.append(yy)
            if (yy >= 2015): list2015.append(yy)
        # 判断是否基础煤种，并记录使用年份
        if (len(set(list1996)) >= 16):
            base_name.append(item)
            base_reason[item] = '1996-2018年间用过不少于16年'
        elif (len(set(list2009)) >= 8):
            base_name.append(item)
            base_reason[item] = '2009-2018年间用过不少于8年'
        elif (len(set(list2015)) >= 4):
            base_name.append(item)
            base_reason[item] = '2015-2018年间用过不少于4年'
    # 根据基础煤种名称和使用年份，获取基础煤种原始数据
    dflist = []
    for item in base_name:
        df_name = dfs[(dfs['煤名称'] == item)]
        dflist.append(df_name)
    if len(dflist)>0:
        base_dfs = pd.concat(dflist, ignore_index=True, sort=False)
        new_indexs=['入选原因']
        base_dfs2 = pd.concat([base_dfs, pd.DataFrame(columns=new_indexs)], sort=False)
        for index, row in base_dfs2.iterrows():
            base_dfs2.loc[index, '入选原因'] = base_reason[row.煤名称]
    else:
        base_dfs2 = pd.DataFrame(columns=['A'])
    return base_dfs2

### 获取经典煤种数据
#def get_Classic_coal(self, dfs, yeardfs, alldfs):
def get_Classic_coal(yeardfs):
    #1999-2002年间使用的煤种
    classic_dfs1= yeardfs[(yeardfs.年份 >= 1999) & (yeardfs.年份 <= 2002)].reset_index(drop=True)
    classic_dfs1 = pd.concat([classic_dfs1, pd.DataFrame(columns=['入选原因'])], sort=False)
    for index, row in classic_dfs1.iterrows():
        classic_dfs1.loc[index, '入选原因'] = '1999-2002年间使用的煤种'
   #煤质分级为特等的煤种
    classic_dfs2 = yeardfs[(yeardfs.煤质分级 == '特等') & ((yeardfs.年份 < 1999) | (yeardfs.年份 > 2002))].reset_index(drop=True)
    classic_dfs2 = pd.concat([classic_dfs2, pd.DataFrame(columns=['入选原因'])], sort=False)
    for index, row in classic_dfs2.iterrows():
        classic_dfs2.loc[index, '入选原因'] = '年均煤质分级为特等'
    #分煤种、分时间段主要指标排名前3的煤种
    # 定义不同煤质指标的大小顺序(越大越好or越小越好)
    maincols = ['CRI', 'CSR', 'DI150_15','Y','G', 'TD', 'lgMF','Ad', 'Std', 'Vd', 'Pd', 'K2O_Na2O']
    colorder = {}
    for item in ['CSR','DI150_15','Y','G','TD','lgMF']:
        colorder[item] = False
    for item in ['CRI','Ad','Std','Vd','Pd','K2O_Na2O']:
        colorder[item] = True
    dflist = []
    kinds = list(set(yeardfs.煤种.tolist()))
    classic_dfs3 = pd.DataFrame(columns=['入选原因'])
    for kind in kinds:
        # 1985-2005期间，年均指标排名前3
        classic_dfs31 = yeardfs[(yeardfs.煤种 == kind) & (yeardfs.年份 >= 1985) & (yeardfs.年份 <= 2005)].reset_index(drop=True)
        for col in maincols:
            df = classic_dfs31.sort_values(ascending = colorder[col],by=col).reset_index(drop=True)
            indexs,tempname,coldflist = [],[],[]
            for i in range(len(df)):
                if len(tempname) < 3:
                    if (not (df.loc[i,'煤名称'] in tempname)):
                        tempname.append(df.loc[i,'煤名称'])
                        indexs.append(i)
                elif len(tempname) == 3:
                    break
            for ii in indexs:
                coldflist.append(df.loc[ii])
            coldf = pd.DataFrame(coldflist)
            coldf = pd.concat([coldf, pd.DataFrame(columns=['入选原因'])], sort=False).reset_index(drop=True)
            for index, row in coldf.iterrows():
                coldf.loc[index, '入选原因'] = '1985-2005'+kind+'年均'+col+'前%d' % len(indexs)
            classic_dfs3 = classic_dfs3.append(coldf,ignore_index=True,sort=False).reset_index(drop=True)
        #print(classic_dfs310)
        # 2006-2018期间，年均指标排名前3
        classic_dfs32 = yeardfs[(yeardfs.煤种 == kind) & (yeardfs.年份 >= 2006) & (yeardfs.年份 <= 2018)].reset_index(drop=True)
        for col in maincols:
            df = classic_dfs32.sort_values(ascending = colorder[col],by=col).reset_index(drop=True)
            indexs,tempname,coldflist = [],[],[]
            for i in range(len(df)):
                if len(tempname) < 3:
                    if (not (df.loc[i,'煤名称'] in tempname)):
                        tempname.append(df.loc[i,'煤名称'])
                        indexs.append(i)
                elif len(tempname) == 3:
                    break
            for ii in indexs:
                coldflist.append(df.loc[ii])
            coldf = pd.DataFrame(coldflist)
            coldf = pd.concat([coldf, pd.DataFrame(columns=['入选原因'])], sort=False).reset_index(drop=True)
            for index, row in coldf.iterrows():
                coldf.loc[index, '入选原因'] = '2006-2018'+kind+'年均'+col+'前%d' % len(indexs)
            classic_dfs3 = classic_dfs3.append(coldf,ignore_index=True,sort=False).reset_index(drop=True)
        # 获取2019年前各指标最差值
        min_df12 = classic_dfs3[(classic_dfs3.煤种 == kind)]
        colmin = {}
        for col in maincols:
            if colorder[col] == False:      #该指标数值越大越好
                colmin[col] = min_df12[col].min()
            elif colorder[col] == True:     #该指标数值越小越好
                colmin[col] = min_df12[col].max()
        # 2019以来，年均指标排名前3
        classic_dfs33 = yeardfs[(yeardfs.煤种 == kind) & (yeardfs.年份 >= 2019)].reset_index(drop=True)
        for col in maincols:
            df = classic_dfs33.sort_values(ascending = colorder[col],by=col).reset_index(drop=True)
            indexs,tempname,coldflist = [],[],[]
            for i in range(len(df)):
                if colorder[col] == False:  # 该指标数值越大越好
                    if df.loc[i,col] >= colmin[col]:
                        if len(tempname) < 3:
                            if not ('瘦煤' in tempname):
                                if (not (df.loc[i, '煤名称'] in tempname)):
                                    tempname.append(df.loc[i, '煤名称'])
                                    indexs.append(i)
                        elif len(tempname) == 3:
                            break
                    else:
                        break
                elif colorder[col] == True:  # 该指标数值越小越好
                    if df.loc[i,col] <= colmin[col]:
                        if len(tempname) < 3:
                            if not ('瘦煤' in tempname):
                                if (not (df.loc[i, '煤名称'] in tempname)):
                                    tempname.append(df.loc[i, '煤名称'])
                                    indexs.append(i)
                        elif len(tempname) == 3:
                            break
                    else:
                        break
            for ii in indexs:
                coldflist.append(df.loc[ii])
            coldf = pd.DataFrame(coldflist)
            coldf = pd.concat([coldf, pd.DataFrame(columns=['入选原因'])], sort=False).reset_index(drop=True)
            for index, row in coldf.iterrows():
                coldf.loc[index, '入选原因'] = '2019以来'+kind+'年均'+col+'前%d' % len(indexs)
            classic_dfs3 = classic_dfs3.append(coldf,ignore_index=True,sort=False).reset_index(drop=True)
    classic_dfs = pd.concat([classic_dfs1,classic_dfs2,classic_dfs3],ignore_index=True,sort=False).reset_index(drop=True)
    return classic_dfs

### 获取新煤种数据
def get_New_coal(dfs):
    new_dfs1 = dfs[(dfs.备注.notna())] # & ((dfs.备注 == '新') | (dfs.备注 == 'new'))]
    if (new_dfs1.empty):
        new_dfs = pd.DataFrame(columns=['A'])
    else:
        new_dfs = new_dfs1[(new_dfs1.备注 == '新') | (new_dfs1.备注 == 'new')]
        if (new_dfs.empty):
            new_dfs = pd.DataFrame(columns=['A'])
    return new_dfs

### 获取煤种趋势数据
def get_Trend_coal(base_dfs):
    trend_df = pd.DataFrame
    # （1）2016年以来按年均
    df_3years = base_dfs[(base_dfs.年份 >= 2016)]
    if (df_3years.empty):
        df_3years = pd.DataFrame(columns=['A'])
    else:
        df_3years = mean_by_year(df_3years)
    # （2）2016年前按时间段
    df_yearregion = base_dfs[base_dfs.年份 < 2016]
    if (df_yearregion.empty):
        df_yearregion = pd.DataFrame(columns=['A'])
    else:
        df_yearregion = mean_by_yearregion(df_yearregion)
    # （1）（2）合并
    if (df_3years.empty) and (df_yearregion.empty):
        trend_df = pd.DataFrame(columns=['A'])
    elif (df_3years.empty):
        trend_df = df_yearregion
    elif (df_yearregion.empty):
        trend_df = df_3years
    else:
        trend_df = pd.concat([df_yearregion,df_3years], ignore_index=True, sort=False)
    return trend_df

### 根据煤种和硫分数据，判断硫分分级
def get_S_level(coal_kind,coal_Std):
    if coal_kind == '焦煤':
        if (coal_Std < 0.4):  return ('特低')
        elif (0.4 <= coal_Std < 0.6):  return ('低')
        elif (0.6 <= coal_Std < 1):  return ('中')
        elif (1 <= coal_Std <= 1.5):  return ('高')
        elif (coal_Std > 1.5):  return ('特高')
    elif (coal_kind == '肥煤') or (coal_kind == '1/3焦煤'):
        if (coal_Std < 0.4):  return ('特低')
        elif (0.4 <= coal_Std < 0.7):  return ('低')
        elif (0.7 <= coal_Std < 1.0):  return ('中')
        elif (1.0 <= coal_Std <= 2.0):  return ('高')
        elif (coal_Std > 2.0):  return ('特高')
    elif (coal_kind == '气煤'):
        if (coal_Std < 0.4):  return ('特低')
        elif (0.4 <= coal_Std < 0.6):  return ('低')
        elif (0.6 <= coal_Std < 0.8):  return ('中')
        elif (0.8 <= coal_Std <= 1.0):  return ('高')
        elif (coal_Std > 1.0):  return ('特高')
    elif (coal_kind == '瘦煤'):
        if (coal_Std < 0.4):  return ('特低')
        elif (0.4 <= coal_Std < 0.6):  return ('低')
        elif (0.6 <= coal_Std < 0.8):  return ('中')
        elif (0.8 <= coal_Std <= 1.2):  return ('高')
        elif (coal_Std > 1.2):  return ('特高')
    else:
        return ('煤种未知')

### 根据煤种和灰分数据，判断灰分分级
def get_Ash_level(coal_kind,coal_Ad):
    if (coal_kind == '焦煤') or (coal_kind == '瘦煤'):
        if (coal_Ad < 8):  return ('特低')
        elif (8 <= coal_Ad < 9):  return ('低')
        elif (9 <= coal_Ad < 10.5):  return ('中')
        elif (10.5 <= coal_Ad <= 11.5):  return ('高')
        elif (coal_Ad > 11.5):  return ('特高')
    elif (coal_kind == '肥煤'):
        if (coal_Ad < 8):  return ('特低')
        elif (8 <= coal_Ad < 9):  return ('低')
        elif (9 <= coal_Ad < 10.5):  return ('中')
        elif (10.5 <= coal_Ad <= 11.5):  return ('高')
        elif (coal_Ad > 11.5):  return ('特高')
    elif (coal_kind == '1/3焦煤'):
        if (coal_Ad < 7.5):  return ('特低')
        elif (7.5 <= coal_Ad < 8.5):  return ('低')
        elif (8.5 <= coal_Ad < 9.5):  return ('中')
        elif (9.5 <= coal_Ad <= 10.5):  return ('高')
        elif (coal_Ad > 10.5):  return ('特高')
    elif (coal_kind == '气煤'):
        if (coal_Ad < 7):  return ('特低')
        elif (7 <= coal_Ad < 7.5):  return ('低')
        elif (7.5 <= coal_Ad < 8.5):  return ('中')
        elif (8.5 <= coal_Ad <= 9.5):  return ('高')
        elif (coal_Ad > 9.5):  return ('特高')
    else:
        return ('煤种未知')

### 根据煤种和CSR数据，判断热强度分级
def get_HotStrength_level(coal_kind,coal_CSR):
    if (coal_kind == '焦煤') or (coal_kind == '肥煤'):
        if (coal_CSR < 60):  return ('C级')
        elif (60 <= coal_CSR < 70):  return ('B级')
        elif (coal_CSR >= 70):  return ('A级')
    elif (coal_kind == '1/3焦煤'):
        if (coal_CSR < 52):  return ('C级')
        elif (52 <= coal_CSR < 60):  return ('B级')
        elif (coal_CSR >= 60):  return ('A级')
    elif (coal_kind == '气煤') or (coal_kind == '瘦煤'):
        if (coal_CSR < 40):  return ('C级')
        elif (40 <= coal_CSR < 50):  return ('B级')
        elif (coal_CSR >= 50):  return ('A级')
    else:
        return ('煤种未知')

### 根据挥发分、基质流动度、全膨胀数据，判断硬煤分类
def get_Hard_level(coal_Vd,coal_lgMF,coal_TD):
    coal_MF = 10**coal_lgMF
    if 30 <= coal_Vd < 33:  #高档硬A
        if (coal_MF >= 15000) and (coal_TD >= 200): return ('硬煤')
        elif (coal_MF >= 15000) or (coal_TD >= 200): return ('半硬优')
        elif (coal_MF < 1000) and (coal_TD < 50): return ('软煤')
        elif (coal_MF < 1000) or (coal_TD < 50): return ('半软')
        else: return ('半硬')
    elif 33 <= coal_Vd < 36:  #高档硬B
        if (10000 <= coal_MF < 15000) and (175 <= coal_TD < 200): return ('硬煤')
        elif (10000 <= coal_MF < 15000) or (175 <= coal_TD < 200): return ('半硬优')
        elif (coal_MF < 1000) and (coal_TD < 50): return ('软煤')
        elif (coal_MF < 1000) or (coal_TD < 50): return ('半软')
        else: return ('半硬')
    elif 36 <= coal_Vd:  #高档硬C
        if (2500 <= coal_MF < 10000) and (50 <= coal_TD < 175): return ('硬煤')
        elif (2500 <= coal_MF < 10000) or (50 <= coal_TD < 175): return ('半硬优')
        elif (coal_MF < 1000) and (coal_TD < 50): return ('软煤')
        elif (coal_MF < 1000) or (coal_TD < 50): return ('半软')
        else: return ('半硬')
    elif 27 <= coal_Vd < 30:  #中档硬A
        if (7500 <= coal_MF) and (175 <= coal_TD): return ('硬煤')
        elif (7500 <= coal_MF) or (175 <= coal_TD): return ('半硬优')
        elif (coal_MF < 90) and (coal_TD < 50): return ('软煤')
        elif (coal_MF < 90) or (coal_TD < 50): return ('半软')
        else: return ('半硬')
    elif 24 <= coal_Vd < 27:  #中档硬B
        if (2500 <= coal_MF < 7500) and (150 <= coal_TD < 175): return ('硬煤')
        elif (2500 <= coal_MF < 7500) or (150 <= coal_TD < 175): return ('半硬优')
        elif (coal_MF < 90) and (coal_TD < 50): return ('软煤')
        elif (coal_MF < 90) or (coal_TD < 50): return ('半软')
        else: return ('半硬')
    elif 22 <= coal_Vd < 24:  #中档硬C
        if (300 <= coal_MF < 2500) and (50 <= coal_TD < 150): return ('硬煤')
        elif (300 <= coal_MF < 2500) or (50 <= coal_TD < 150): return ('半硬优')
        elif (coal_MF < 90) and (coal_TD < 50): return ('软煤')
        elif (coal_MF < 90) or (coal_TD < 50): return ('半软')
        else: return ('半硬')
    elif 18 <= coal_Vd < 22:  #低档硬A
        if (300 <= coal_MF) and (75 <= coal_TD): return ('硬煤')
        elif (300 <= coal_MF) or (75 <= coal_TD): return ('半硬优')
        elif (coal_MF < 10) and (coal_TD < 25): return ('软煤')
        elif (coal_MF < 10) or (coal_TD < 25): return ('半软')
        else: return ('半硬')
    elif 15 <= coal_Vd < 18:  #低档硬B
        if (100 <= coal_MF < 300) and (50 <= coal_TD < 100): return ('硬煤')
        elif (100 <= coal_MF < 300) or (50 <= coal_TD < 100): return ('半硬优')
        elif (coal_MF < 10) and (coal_TD < 25): return ('软煤')
        elif (coal_MF < 10) or (coal_TD < 25): return ('半软')
        else: return ('半硬')
    elif coal_Vd < 15:  #低档硬C
        if (coal_MF < 100) and (coal_TD < 50): return ('硬煤')
        elif (coal_MF < 100) or (coal_TD < 50): return ('半硬优')
        elif (coal_MF < 10) and (coal_TD < 25): return ('软煤')
        elif (coal_MF < 10) or (coal_TD < 25): return ('半软')
        else: return ('半硬')

### 根据大小关系、分数范围给指标打分
def get_score(flag,lowvalue,highvalue,value):
    low_cutoff = lowvalue + (highvalue-lowvalue)/4
    high_cutoff = highvalue - (highvalue-lowvalue)/4
    if (flag == 'small'):
        if (value <= low_cutoff): return 100
        elif (value <= high_cutoff): return 70
        elif (value > high_cutoff): return 40
    elif (flag == 'big'):
        if (value >= high_cutoff): return 100
        elif (value >= low_cutoff): return 70
        elif (value < low_cutoff): return 40
### 根据灰分、硫分指标等级打分
def get_score_level(level):
    if (level == '特低'): return 110
    elif (level == '低'): return 100
    elif (level == '中'): return 70
    elif (level == '高'): return 40
    elif (level == '特高'): return 10

### 根据若干指标计算煤质分级
def get_CoalQuality_level(coal_kind,Std_level,Ash_level,coal_CRI,coal_CSR,coal_DI,coal_Y,coal_G,coal_TD,coal_lgMF,coal_Ad,coal_Std,coal_Vd,coal_Pd,coal_K2O):
    if (coal_kind == '焦煤'):
        score_CRI = get_score('small',15.7,30.3,coal_CRI)
        score_CSR = get_score('big',56.6,74.0,coal_CSR)
        score_DI = get_score('big',79.6,87.7,coal_DI)
        score_Y = get_score('big',11.8,17.7,coal_Y)
        score_G = get_score('big',72.3,86.0,coal_G)
        score_TD = get_score('big',27.4,104.0,coal_TD)
        score_lgMF = get_score('big',1.37,3.25,coal_lgMF)
        score_Ad = get_score_level(Ash_level)
        score_Std = get_score_level(Std_level)
        score_Vd = get_score('small',17.4,25.2,coal_Vd)
        score_Pd = get_score('small',0.008,0.076,coal_Pd)
        score_K2O = get_score('small',0.73,2.52,coal_K2O)
    elif (coal_kind == '肥煤'):
        score_CRI = get_score('small',13.8,27.5,coal_CRI)
        score_CSR = get_score('big',53.0,75.0,coal_CSR)
        score_DI = get_score('big',81.4,86.0,coal_DI)
        score_Y = get_score('big',23.0,27.0,coal_Y)
        score_G = get_score('big',86.0,94.0,coal_G)
        score_TD = get_score('big',142.0,266.0,coal_TD)
        score_lgMF = get_score('big',3.3,4.4,coal_lgMF)
        score_Ad = get_score_level(Ash_level)
        score_Std = get_score_level(Std_level)
        score_Vd = get_score('small',23.0,30.0,coal_Vd)
        score_Pd = get_score('small',0.009,0.063,coal_Pd)
        score_K2O = get_score('small',0.53,2.85,coal_K2O)
    elif (coal_kind == '1/3焦煤'):
        score_CRI = get_score('small',17.5,28.6,coal_CRI)
        score_CSR = get_score('big',52.0,71.2,coal_CSR)
        score_DI = get_score('big',70.0,84.8,coal_DI)
        score_Y = get_score('big',16.0,24.0,coal_Y)
        score_G = get_score('big',80.0,92.5,coal_G)
        score_TD = get_score('big',92.0,237.0,coal_TD)
        score_lgMF = get_score('big',2.05,4.68,coal_lgMF)
        score_Ad = get_score_level(Ash_level)
        score_Std = get_score_level(Std_level)
        score_Vd = get_score('small',26.0,39.0,coal_Vd)
        score_Pd = get_score('small',0.003,0.045,coal_Pd)
        score_K2O = get_score('small',0.72,3.54,coal_K2O)
    elif (coal_kind == '气煤'):
        score_CRI = get_score('small',32.0,56.5,coal_CRI)
        score_CSR = get_score('big',21.0,52.0,coal_CSR)
        score_DI = get_score('big',57.0,83.0,coal_DI)
        score_Y = get_score('big',10.7,16.0,coal_Y)
        score_G = get_score('big',61.0,87.0,coal_G)
        score_TD = get_score('big',4.0,115.0,coal_TD)
        score_lgMF = get_score('big',1.13,3.76,coal_lgMF)
        score_Ad = get_score_level(Ash_level)
        score_Std = get_score_level(Std_level)
        score_Vd = get_score('small',32.0,36.5,coal_Vd)
        score_Pd = get_score('small',0.005,0.042,coal_Pd)
        score_K2O = get_score('small',0.95,3.57,coal_K2O)
    elif (coal_kind == '瘦煤'):
        score_CRI = get_score('small',17.0,43.0,coal_CRI)
        score_CSR = get_score('big',30.0,62.0,coal_CSR)
        score_DI = get_score('big',34.0,84.0,coal_DI)
        score_Y = get_score('big',5.0,12.0,coal_Y)
        score_G = get_score('big',29.0,79.0,coal_G)
        score_TD = get_score('big',40.0,40.0,coal_TD)
        score_lgMF = get_score('big',0,1.76,coal_lgMF)
        score_Ad = get_score_level(Ash_level)
        score_Std = get_score_level(Std_level)
        score_Vd = get_score('small',14.2,18.6,coal_Vd)
        score_Pd = get_score('small',0.002,0.043,coal_Pd)
        score_K2O = get_score('small',0.61,1.74,coal_K2O)
    mean_score = np.mean([score_CRI,score_CSR,score_DI,score_Y,score_G,score_TD,score_lgMF,score_Ad,score_Std,score_Vd,score_Pd,score_K2O])
    if (mean_score > 80): return ('优质', mean_score)
    elif (60 <= mean_score <= 80): return ('中等', mean_score)
    elif (mean_score < 60): return ('一般', mean_score)

### 更新煤质分级指标（5个指标中有4个是最好的，煤质分级更新为特等）
def update_CoalQuality_level(S_level,Ash_level,HotStrength_level,Hard_level,CoalQuality_level):
    count = 0
    if (S_level == '特低') or (S_level == '低'): count += 1
    if (Ash_level == '特低') or (Ash_level == '低'): count += 1
    if (HotStrength_level == 'A级') : count += 1
    if (Hard_level == '硬煤') or (Hard_level == '半硬优'): count += 1
    if (CoalQuality_level == '优质') : count += 1
    if (count >= 4): return '特等'
    else: return CoalQuality_level

### 根据时间段对数据进行分段平均
#def mean_by_yearregion(self,dfs):    #GUI程序用
def mean_by_yearregion(dfs):          #测试程序用
    year_range = ['1985-1990','1991-1995','1996-1998','1999-2002','2003-2005','2006-2010','2011-2015','2016至今']
    cols = dfs.columns.tolist()
    dfs_mean_yearrange = pd.DataFrame(columns=cols)
    for item in ['煤种', '煤名称', '年份', '国家', '产地']:
        if item in cols:
            cols.remove(item)
    for i in range(len(year_range)):
        if (i != len(year_range)-1):
            year_start = int(year_range[i].split('-')[0])
            year_end = int(year_range[i].split('-')[1])
            dfs_yearrange = dfs[(dfs.年份 >= year_start) & (dfs.年份 <= year_end)]
        else:
            year_start = int(year_range[i][:4])
            dfs_yearrange = dfs[(dfs.年份 >= year_start)]
        if len(dfs_yearrange.index) > 0:
            names = list(set(dfs_yearrange['煤名称'].tolist()))
            coal_kind,coal_country,coal_place = {},{},{}
            size, elem, duidensity, ashcomposition, therm, water, reason = {}, {}, {}, {}, {}, {}, {}
            for name in names:
                size[name] = []
                elem[name] = []
                duidensity[name] = []
                ashcomposition[name] = []
                therm[name] = []
                water[name] = []
                reason[name] = []
            already_names = []
            for index,row in dfs_yearrange.iterrows():
                size[row.煤名称].append(row.粒级分布)
                elem[row.煤名称].append(row.元素分析)
                duidensity[row.煤名称].append(row.堆密度)
                ashcomposition[row.煤名称].append(row.灰成分)
                therm[row.煤名称].append(row.发热量)
                water[row.煤名称].append(row.全水分)
                if ('入选原因' in cols):
                    reason[row.煤名称].append(row.入选原因)
                if (row.煤名称 in names) and (row.煤名称 not in already_names):
                    coal_kind[row.煤名称] = row.煤种
                    coal_country[row.煤名称] = row.国家
                    coal_place[row.煤名称] = row.产地
                    already_names.append(row.煤名称)
            for name in names:
                size[name] = list(set(size[name]))
                elem[name] = list(set(elem[name]))
                duidensity[name] = list(set(duidensity[name]))
                ashcomposition[name] = list(set(ashcomposition[name]))
                therm[name] = list(set(therm[name]))
                water[name] = list(set(water[name]))
                reason[name] = list(set(reason[name]))
            dfs_yearrangeGM = dfs_yearrange.loc[:,cols].groupby(dfs_yearrange['煤名称']).mean()
            initnum = len(dfs_mean_yearrange.index)
            for nameindex in range(len(names)):
                for col in cols:
                    #dfs_mean_yearrange.loc[initnum+nameindex, '序号'] = initnum+nameindex+1
                    dfs_mean_yearrange.loc[initnum+nameindex, '煤种'] = coal_kind[names[nameindex]]
                    dfs_mean_yearrange.loc[initnum+nameindex, '煤名称'] = names[nameindex]
                    dfs_mean_yearrange.loc[initnum+nameindex, '年份'] = year_range[i]
                    dfs_mean_yearrange.loc[initnum+nameindex, '国家'] = coal_country[names[nameindex]]
                    dfs_mean_yearrange.loc[initnum+nameindex, '产地'] = coal_place[names[nameindex]]
                    if (names[nameindex] in dfs_yearrangeGM.index) and (col in dfs_yearrangeGM.columns):
                        dfs_mean_yearrange.loc[initnum+nameindex,col] = dfs_yearrangeGM.loc[names[nameindex],col]
                    dfs_mean_yearrange.loc[initnum + nameindex, '粒级分布'] = size[names[nameindex]]
                    dfs_mean_yearrange.loc[initnum + nameindex, '元素分析'] = elem[names[nameindex]]
                    dfs_mean_yearrange.loc[initnum + nameindex, '堆密度'] = duidensity[names[nameindex]]
                    dfs_mean_yearrange.loc[initnum + nameindex, '灰成分'] = ashcomposition[names[nameindex]]
                    dfs_mean_yearrange.loc[initnum + nameindex, '发热量'] = therm[names[nameindex]]
                    dfs_mean_yearrange.loc[initnum + nameindex, '全水分'] = water[names[nameindex]]
                    if ('入选原因' in cols):
                        dfs_mean_yearrange.loc[initnum + nameindex, '入选原因'] = reason[names[nameindex]]
    #print('已根据时间段对各煤种进行指标数据平均')                   #测试程序用
    #self.textEdit.append('已根据时间段对各煤种进行指标数据平均')   #GUI程序用
    return dfs_mean_yearrange

### 根据年份对数据进行平均
#def mean_by_year(self,dfs):    #GUI程序用
def mean_by_year(dfs):          #测试程序用
    cols = dfs.columns.tolist()
    dfs_mean_year = pd.DataFrame(columns=cols)
    for item in ['煤种', '煤名称', '年份', '国家', '产地']:
        if item in cols:
            cols.remove(item)
    years = list(set(dfs['年份'].tolist()))
    years.sort()
    for i in range(len(years)):
        dfs_year = dfs[(dfs.年份 == years[i])]
        names = list(set(dfs_year['煤名称'].tolist()))
        coal_kind, coal_country, coal_place = {}, {}, {}
        already_names = []
        for index, row in dfs_year.iterrows():
            if (row.煤名称 in names) and (row.煤名称 not in already_names):
                coal_kind[row.煤名称] = row.煤种
                coal_country[row.煤名称] = row.国家
                coal_place[row.煤名称] = row.产地
                already_names.append(row.煤名称)
        dfs_yearGM = dfs_year.loc[:,cols].groupby(dfs_year['煤名称']).mean()
        initnum = len(dfs_mean_year.index)
        for nameindex in range(len(names)):
            for col in cols:
                #dfs_mean_year.loc[initnum+nameindex, '序号'] = initnum+nameindex+1
                dfs_mean_year.loc[initnum+nameindex, '煤种'] = coal_kind[names[nameindex]]
                dfs_mean_year.loc[initnum+nameindex, '煤名称'] = names[nameindex]
                dfs_mean_year.loc[initnum+nameindex, '年份'] = years[i]
                dfs_mean_year.loc[initnum+nameindex, '国家'] = coal_country[names[nameindex]]
                dfs_mean_year.loc[initnum+nameindex, '产地'] = coal_place[names[nameindex]]
                if (names[nameindex] in dfs_yearGM.index) and (col in dfs_yearGM.columns):
                    dfs_mean_year.loc[initnum+nameindex,col] = dfs_yearGM.loc[names[nameindex],col]
    #print('已根据年份对各煤种进行指标数据平均')  # 测试程序用
    #self.textEdit.append('已根据年份对各煤种进行指标数据平均')   #GUI程序用
    return dfs_mean_year

### 根据煤种对数据做平均
def mean_by_kind(trend_df,maincols):
    #maincols = ['CRI', 'CSR', 'DI150_15', 'Y', 'G', 'TD', 'lgMF', 'Ad', 'Std', 'Vd', 'Pd', 'K2O_Na2O']
    trend_kind = pd.DataFrame(columns=['煤种','年份'])
    trend_kind = pd.concat([trend_kind,pd.DataFrame(columns=maincols)],ignore_index=True,sort=False)
    kinds = list(set(trend_df.煤种.tolist()))
    for item in kinds:
        tempdf = trend_df[trend_df.煤种 == item].reset_index(drop=True)
        del tempdf['煤名称']
        del tempdf['国家']
        del tempdf['产地']
        yearlist = list(set(tempdf.年份.tolist()))
        for year in yearlist:
            test = {}
            test['年份'] = numformat(str(year))
            test['煤种'] = item
            tempdf1 = tempdf[tempdf.年份 == year]
            for col in maincols:
                test[col] = tempdf1[col].mean()
            new = pd.DataFrame([test])
            trend_kind = trend_kind.append(new, ignore_index=True, sort=True)
            #trend_kind = pd.concat([trend_kind,new],ignore_index=True,sort=False)
    trend_kind = trend_kind.sort_values(by=['煤种','年份'], ascending=[True, True])
    return trend_kind

### 根据数据对煤质、热强度、硬煤分类、灰分、硫分进行分级，并插入各自数据中
#def init_level(self,dfs):  #GUI程序用
def init_level(dfs):        #测试程序用
    colnum = len(dfs.index)
    new_indexs = ['煤质分级','煤质分级评分','热强度分级','硬煤分类','灰分分级','硫分分级']
    dfs = pd.concat([dfs, pd.DataFrame(columns=new_indexs)],sort=False)
    #print('根据各指标进行煤质、热强度、硬煤分类、灰分、硫分分级')                  #测试程序用
    #self.textEdit.append('根据各指标进行煤质、热强度、硬煤分类、灰分、硫分分级')  #GUI程序用
    for index,row in dfs.iterrows():
        dfs.loc[index,'硫分分级'] = get_S_level(row.煤种,row.Std)
        dfs.loc[index,'灰分分级'] = get_Ash_level(row.煤种,row.Ad)
        dfs.loc[index,'热强度分级'] = get_HotStrength_level(row.煤种,row.CSR)
        dfs.loc[index,'硬煤分类'] = get_Hard_level(row.Vd,row.lgMF,row.TD)
    for index, row in dfs.iterrows():
        (level,score) = get_CoalQuality_level(row.煤种,row.硫分分级,row.灰分分级,row.CRI,row.CSR,row.DI150_15,row.Y,row.G,row.TD,row.lgMF,row.Ad,row.Std,row.Vd,row.Pd,row.K2O_Na2O)
        dfs.loc[index, '煤质分级'] = level
        dfs.loc[index, '煤质分级评分'] = score
    for index, row in dfs.iterrows():
        dfs.loc[index,'煤质分级'] = update_CoalQuality_level(row.硫分分级,row.灰分分级,row.热强度分级,row.硬煤分类,row.煤质分级)
        #report_progress(index, len(dfs.index))
    #report_progress_done()
    return dfs