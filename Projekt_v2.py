import numpy as np
import pandas as pd
import pandasgui
import matplotlib.pyplot as plt
from IPython import get_ipython
import glob
from collections import Counter
import sqlite3
import math
from future.utils import iteritems
import os




#useful variables
years=[]
for i in range(1880,2020):
    years.append(str(i))
birth_f_amount_in_year = {}
birth_m_amount_in_year = {}
birth_years = {}
girl_boy_rate = []

# TODO 1 Wczytaj dane ze wszystkich plików do pojedynczej tablicy (używając Pandas).
path = r'names'
all_files = glob.glob(path + "/yob*.txt")
li = []
for filename in sorted(all_files):
    df = pd.read_csv(filename,sep=",", header=None,names=["Name","Gender","Amount"])
    df["year"] = filename[9:13]
    li.append(df)
frame = pd.concat(li, axis=0, ignore_index=True)
print("Zadanie 1: Wczytany data frame to: ")
print(frame)




# TODO 2 Określić ile różnych (unikalnych) imion zostało nadanych w tym czasie.
print("Zadanie nr 2:")
print("Ilość unikalnych imion to: " + str(frame['Name'].nunique()))

# TODO 3 Określić ile różnych (unikalnych) imion zostało nadanych w tym czasie rozróżniając imiona męskie i żeńskie.
male_names = frame.loc[frame['Gender']=='M',:]
female_names = frame.loc[frame['Gender']=='F',:]
print("Zadanie nr 3: ")
print("Ilość unikalnych imion męskich to: " +str(len(male_names['Name'].unique().tolist())))
print("Ilość unikalnych imion żeńskich to: " +str(len(female_names['Name'].unique().tolist())))

# TODO 4 Określ popularność każdego z imion w danym każdym roku dzieląc liczbę razy, kiedy imię zostało nadane przez całkowita liczbę urodzeń dla danej płci.
frame["frequency_male"]=0.0
frame["frequency_female"]=0.0

frame_sum_men = frame.loc[frame["Gender"] == 'M', :]
frame_sum_women = frame.loc[frame["Gender"] == 'F', :]
li2=[]
# start for task 6
df_men = frame_sum_men.pivot_table(index = 'year',columns='Name',values='Amount',fill_value = 0.0)
df_women = frame_sum_women.pivot_table(index = 'year',columns='Name',values='Amount',fill_value = 0.0)
# end task 6
for y in years:
    birth_years[y] = frame.loc[frame['year'] == y,'Amount'].sum()
    birth_f_amount_in_year[y] = frame_sum_women.loc[frame_sum_women['year'] == y,'Amount'].sum()
    birth_m_amount_in_year[y] = frame_sum_men.loc[frame_sum_men['year'] == y, 'Amount'].sum()
    frame_sum_women.loc[frame_sum_women['year'] == y, 'frequency_female'] = (frame_sum_women.loc[frame_sum_women['year'] == y,'Amount']) / birth_f_amount_in_year.get(y)
    frame_sum_men.loc[frame_sum_men['year'] == y, 'frequency_male'] = (frame_sum_men.loc[frame_sum_men['year'] == y,'Amount']) / birth_m_amount_in_year.get(y)
    girl_boy_rate.append(birth_f_amount_in_year.get(y) / birth_m_amount_in_year.get(y))
li2.append(frame_sum_women)
li2.append(frame_sum_men)
frame = pd.concat(li2, axis=0, ignore_index=False)
print("Zadanie nr 4: ")
print(frame)


df_women_freq = frame_sum_women.pivot_table(index = 'year',columns='Name',values='frequency_female',fill_value = 0.0)
#TODO 5
# Określ i wyświetl wykres złożony z dwóch podwykresów, gdzie osią x jest skala czasu, a oś y reprezentuje:
    #liczbę urodzin w danym roku (wykres na górze)
    # #stosunek liczby narodzin dziewczynek do liczby narodzin chłopców (wykres na dole) W którym roku zanotowano najmniejszą,
    # a w którym największą różnicę w liczbie urodzeń między chłopcami a dziewczynkami?

# zmienic na punktowe
x_5 = np.arange(len(years))
fig, (ax5_1, ax5_2) = plt.subplots(2)
fig.suptitle('Zadanie 5')
ax5_1.plot(years,list(birth_years.values()), label='Total',color='red')
ax5_2.plot(years,girl_boy_rate,label='Female to male')
ax5_1.set_xlabel("year",fontsize=14)
ax5_1.set_ylabel("Total amount of births",color="red",fontsize=14)
ax5_2.set_ylabel("Girls to boys rate",color="blue",fontsize=14)
ax5_1.xaxis.set_major_locator(plt.MaxNLocator(6))
ax5_2.xaxis.set_major_locator(plt.MaxNLocator(6))
ax5_1.legend()
ax5_2.legend()


df_5 = pd.DataFrame({"year"   : years,
                     "male"   : list(birth_m_amount_in_year.values()),
                     "female" : list(birth_f_amount_in_year.values())},
                    index = None)
df_5["diff"]=abs(df_5["male"]-df_5["female"])

print("Zadanie nr 5: Najwieksza różnica w liczbie urodzeń między chłopcami a dziewczynkami"
      " wyniosła: " + str(df_5["diff"].max())
      + " i zanotowano ją w roku: "+str(df_5.loc[df_5[df_5['diff']==df_5["diff"].max()].index[0],"year"]))
print("Najmniejsza różnica w liczbie urodzeń między chłopcami a dziewczynkami"
      " wyniosła: " + str(df_5["diff"].min())
      + " i zanotowano ją w roku: "+str(abs(int(df_5.loc[df_5[df_5['diff']==df_5["diff"].min()].index[0],"year"]))))

#TODO 6 Wyznacz 1000 najpopularniejszych imion dla każdej płci w całym zakresie czasowym,
# metoda powinna polegać na wyznaczeniu 1000 najpopularniejszych imion dla każdego roku i dla każdej płci
# a następnie ich zsumowaniu w celu ustalenia rankingu top 1000 dla każdej płci.

df_men2 = df_men.iloc[:,0:1000]
df_women2 = df_women.iloc[:,0:1000]
top_1000_men_names = df_men.sum(axis=0)
top_1000_women_names = df_women.sum(axis=0)
top_1000_men_names.sort_values(axis=0,inplace=True,ascending=False)
top_1000_women_names.sort_values(axis=0,inplace=True,ascending=False)
print("Zadanie nr 6: 1000 najpopularniejszych imion męskich to: ")
print(top_1000_men_names[:1000])
print("oraz 1000 najpopularniejszych imion żeńskich to: ")
print(top_1000_women_names[:1000])

#TODO 7
#Wyświetl wykresy zmian dla imion Harry i Marilin oraz pierwszego imienia w żeńskiego i męskiego w rankingu:
    #na osi Y po lewej liczbę razy kiedy imę zostało nadane w każdym roku (zanotuj ile razy nadano to imię w 1940, 1980 i 2019r)?
    #na osi Y po prawej popularność tych imion w każdym z lat

# punkt pierwszy
Harry = df_men["Harry"]
Marilin = df_women["Marilin"]
top_man = df_men[top_1000_men_names.index[0]]
top_woman = df_women[top_1000_women_names.index[0]]

# punkt drugi
Harry_df = frame_sum_men.loc[frame_sum_men["Name"]=="Harry",:]
Harry_df.sort_values("year",axis=0,inplace=True,ascending=True)
top_man_df = frame_sum_men.loc[frame_sum_men["Name"]==str(top_1000_men_names.index[0]),:]
top_man_df.sort_values("year",axis=0,inplace=True,ascending=True)
top_woman_df = frame_sum_women.loc[frame_sum_women["Name"]==str(top_1000_women_names.index[0]),:]
top_woman_df.sort_values("year",axis=0,inplace=True,ascending=True)



fig_7_1, (ax_11) = plt.subplots()
ax_11.plot(years, list(Harry.values), color="red")
ax_11.set_xlabel("year",fontsize=14)
ax_11.set_ylabel("Harry total amount",color="red",fontsize=14)
ax_21 = ax_11.twinx()
ax_21.plot(years, list(Harry_df.loc[:,"frequency_male"].values), color="blue")
ax_21.set_ylabel("Harry popularity",color="blue",fontsize=14)
ax_11.xaxis.set_major_locator(plt.MaxNLocator(6))
ax_21.xaxis.set_major_locator(plt.MaxNLocator(6))
ax_11.set_title('Zadanie 7: Harry')

fig_7_2, (ax_12) = plt.subplots()
ax_12.plot(years, list(Marilin.values), color="red")
ax_12.set_xlabel("year",fontsize=14)
ax_12.set_ylabel("Marilin total amount",color="red",fontsize=14)
ax_22 = ax_12.twinx()
ax_22.plot(years, list(df_women_freq.loc[:,"Marilin"].values), color="blue")
ax_22.set_ylabel("Marilin popularity",color="blue",fontsize=14)
ax_12.xaxis.set_major_locator(plt.MaxNLocator(6))
ax_22.xaxis.set_major_locator(plt.MaxNLocator(6))
ax_12.set_title('Zadanie 7: Marilin')

fig_7_3, (ax_13) = plt.subplots()
ax_13.plot(years, list(top_man.values), color="red")
ax_13.set_xlabel("year",fontsize=14)
ax_13.set_ylabel(str(top_1000_men_names.index[0])+" total amount",color="red",fontsize=14)
ax_23 = ax_13.twinx()
ax_23.plot(years, list(top_man_df.loc[:,"frequency_male"].values), color="blue")
ax_23.set_ylabel(str(top_1000_men_names.index[0])+" popularity",color="blue",fontsize=14)
ax_13.xaxis.set_major_locator(plt.MaxNLocator(6))
ax_23.xaxis.set_major_locator(plt.MaxNLocator(6))
ax_13.set_title('Zadanie 7: '+ str(top_1000_men_names.index[0]))

fig_7_4, (ax_14) = plt.subplots()
ax_14.plot(years, list(top_woman.values), color="red")
ax_14.set_xlabel("year",fontsize=14)
ax_14.set_ylabel(str(top_1000_women_names.index[0])+" total amount",color="red",fontsize=14)
ax_24 = ax_14.twinx()
ax_24.plot(years, list(top_woman_df.loc[:,"frequency_female"].values), color="blue")
ax_24.set_ylabel(str(top_1000_women_names.index[0])+" popularity",color="blue",fontsize=14)
ax_14.xaxis.set_major_locator(plt.MaxNLocator(6))
ax_24.xaxis.set_major_locator(plt.MaxNLocator(6))
ax_14.set_title('Zadanie 7: '+ str(top_1000_women_names.index[0]))

#TODO 8 Wykreśl wykres z podziałem na lata i płeć zawierający informację jaki procent w danym roku stanowiły imiona należące do rankingu top1000.
# Wykres ten opisuje różnorodność imion, zanotuj rok w którym zaobserwowano największą różnicę w różnorodności między imionami męskimi a żeńskimi.


# tutaj mamy dwie opcje:
# 1) Wyznaczać lokalne top1000 dla każdego roku i na podstawie tych wartości dla każdego roku wyznaczać różnorodność
# 2) Wyznaczyc globabalne top 1000 i nie sprawdzać co rok top1000 imion, ale to podejscie ma mnijszy sens, bo nie odzwierciedla poprawnie danych dla kazdego roku
# Wybrałem opcję nr 1:

fig_8,ax1_8 = plt.subplots()
ax1_8.set_title('Zadanie 8')
y1=[]
y2=[]

dfx = df_men.sort_values(by=list(df_men.index.values),axis=1,ascending=False)
dfxy = df_women.sort_values(by=list(df_women.index.values),axis=1,ascending=False)

for k in range(0,len(list(df_men2.sum(axis=1)))):
    y1.append((list(dfx.iloc[:,:1000].sum(axis=1))[k]/list(birth_m_amount_in_year.values())[k])*100)
    y2.append((list(dfxy.iloc[:,:1000].sum(axis=1))[k]/list(birth_f_amount_in_year.values())[k])*100)

ax1_8.plot(years,y1,label = 'boys')
ax1_8.plot(years,y2,label = 'girls')
ax1_8.xaxis.set_major_locator(plt.MaxNLocator(6))
ax1_8.set_xlabel("year",fontsize=14)
ax1_8.set_ylabel("Top 1000 names in total",fontsize=14)
ax1_8.legend()

sub_f_m = [a_i - b_i for a_i,b_i in zip(list(dfx.iloc[:,:1000].sum(axis=1)),list(dfxy.iloc[:,:1000].sum(axis=1)))]
df_sub_f_m = pd.DataFrame(index = years,data=sub_f_m,columns=["Sub_F_M"])
print("Zadanie nr 8: największą różnicę w różnorodności między imionami męskimi a żeńskimi zanotowano w roku: " + str(df_sub_f_m['Sub_F_M'].idxmax()))

#TODO 9 Zweryfikuj hipotezę czy prawdą jest, że w obserwowanym okresie rozkład ostatnich liter imion męskich uległ istotnej zmianie?
years_9 = ['1910','1960','2015']
last_char_tab=[]

for i in ((frame.loc[:,["Name"]]).values.tolist()):
    last_char_tab.append(str(i)[-3])
frame["last_char"]=last_char_tab

sum_9 = 0.0
df_9 = frame.loc[(frame["year"]==years_9[0]) | (frame["year"]==years_9[1]) | (frame["year"]==years_9[2])]

for k in years_9:
    sum_9 = df_9.loc[df_9['year']==k,'Amount'].sum()
    df_9.loc[df_9['year'] == k, 'Amount'] = df_9.loc[df_9['year'] == k, 'Amount'] / sum_9


df_9_pivot = df_9.pivot_table(index = ['year','Gender'],values='Amount',columns='last_char',aggfunc=np.sum)
df_9_pivot.fillna(0.0,inplace=True)


fig_9,(ax1_9) = plt.subplots()
barWidth = 0.25
r1 = np.arange(len(df_9_pivot.columns))
r2 = [x + barWidth for x in r1]
r3 = [x + barWidth for x in r2]

ax1_9.bar(r1,list((df_9_pivot.loc[(years_9[0],'M'),:]).values),width=barWidth,label='1910')
ax1_9.bar(r2,list((df_9_pivot.loc[(years_9[1],'M'),:]).values),width=barWidth,label='1960')
ax1_9.bar(r3,list((df_9_pivot.loc[(years_9[2],'M'),:]).values),width=barWidth,label='2015')
ax1_9.set_xticks(r1)
ax1_9.set_xticklabels(df_9_pivot.columns)
ax1_9.legend()
ax1_9.set_title("Zadanie 9: Mężczyźni")


df_9_pivot_v1 = df_9_pivot
sub_f_m_2 = [abs(a_i - b_i) for a_i,b_i in zip(list(df_9_pivot.loc[('2015','M'),:]),list(df_9_pivot.loc[('1910','M'),:]))]
sub_f_m_2_v2 = [(a_i - b_i) for a_i,b_i in zip(list(df_9_pivot.loc[('2015','M'),:]),list(df_9_pivot.loc[('1910','M'),:]))]
df_9_pivot_v1.loc[('2020','M'),:] = (sub_f_m_2[0],sub_f_m_2[1],sub_f_m_2[2],sub_f_m_2[3],sub_f_m_2[4],sub_f_m_2[5],sub_f_m_2[6],sub_f_m_2[7],sub_f_m_2[8],sub_f_m_2[9],sub_f_m_2[10],sub_f_m_2[11],sub_f_m_2[12],sub_f_m_2[13],sub_f_m_2[14],sub_f_m_2[15],sub_f_m_2[16],sub_f_m_2[17],sub_f_m_2[18],sub_f_m_2[19],sub_f_m_2[20],sub_f_m_2[21],sub_f_m_2[22],sub_f_m_2[23],sub_f_m_2[24],sub_f_m_2[25])
df_9_pivot_v1.loc[('2020','F'),:] = (sub_f_m_2_v2[0],sub_f_m_2_v2[1],sub_f_m_2_v2[2],sub_f_m_2_v2[3],sub_f_m_2_v2[4],sub_f_m_2_v2[5],sub_f_m_2_v2[6],sub_f_m_2_v2[7],sub_f_m_2_v2[8],sub_f_m_2_v2[9],sub_f_m_2_v2[10],sub_f_m_2_v2[11],sub_f_m_2_v2[12],sub_f_m_2_v2[13],sub_f_m_2_v2[14],sub_f_m_2_v2[15],sub_f_m_2_v2[16],sub_f_m_2_v2[17],sub_f_m_2_v2[18],sub_f_m_2_v2[19],sub_f_m_2_v2[20],sub_f_m_2_v2[21],sub_f_m_2_v2[22],sub_f_m_2_v2[23],sub_f_m_2_v2[24],sub_f_m_2_v2[25])

x_dict = df_9_pivot_v1.loc[('2020','M'),:].to_dict()
x_dict_v2 = df_9_pivot_v1.loc[('2020','F'),:].to_dict()
sorted_x_dict = {k: v for k, v in sorted(x_dict .items(), key=lambda item: item[1],reverse=True)}
sorted_x_dict_v2 = {k: v for k, v in sorted(x_dict_v2 .items(), key=lambda item: item[1])[:1]}
key_list = []
key_list2 = []
for i in sorted_x_dict_v2.keys():
    key_list2.append(i)
for i in sorted_x_dict.keys():
    key_list.append(i)

last_char_tab2=[]

frame_sum_men2 = frame.loc[frame["Gender"] == 'M', :]
print("Zadanie nr 9:")
print("Największy wzrost między rokiem 1910 a 2015 zanotowano dla litery: "+str(key_list[0]))
print("Największy spadek między rokiem 1910 a 2015 zanotowano dla litery: "+str(key_list2[0]))
sum_99 =0
for key,value in birth_years.items():

    frame_sum_men2.loc[frame_sum_men2['year'] == key, 'Amount'] = frame_sum_men2.loc[frame_sum_men2['year'] == key, 'Amount'] / value

frame_sum_men3 = frame_sum_men2.loc[(frame_sum_men2["last_char"]==key_list[0]) | (frame_sum_men2["last_char"]==key_list[1]) | (frame_sum_men2["last_char"]==key_list[2])]

df_n = frame_sum_men3.loc[frame_sum_men2['last_char'] == key_list[0],:]
df_r = frame_sum_men3.loc[frame_sum_men2['last_char'] == key_list[1],:]
df_d = frame_sum_men3.loc[frame_sum_men2['last_char'] == key_list[2],:]

df_n2 = frame_sum_men3.loc[frame_sum_men2['last_char'] == key_list[0],:].groupby("year").sum()
df_r2 = frame_sum_men3.loc[frame_sum_men2['last_char'] == key_list[1],:].groupby("year").sum()
df_d2 = frame_sum_men3.loc[frame_sum_men2['last_char'] == key_list[2],:].groupby("year").sum()

fig_9_2,ax1_9_22 = plt.subplots()
ax1_9_22.set_title('Zadanie 9_v2')
ax1_9_22.plot(years,list(df_n2['Amount'].values),label = key_list[0])
ax1_9_22.plot(years,list(df_r2['Amount'].values),label = key_list[1])
ax1_9_22.plot(years,list(df_d2['Amount'].values),label = key_list[2])
ax1_9_22.xaxis.set_major_locator(plt.MaxNLocator(6))
ax1_9_22.set_xlabel("year",fontsize=14)
ax1_9_22.set_ylabel("Popularity",fontsize=14)
ax1_9_22.legend()

print("W obserwowanym okresie rozkład ostatnich liter imion męskich nie uległ istotnej zmianie - po wykonaniu wszsytkich koniecznych obliczeń można to zaobserwować na wykresie o tytule Zadanie nr 9")

#TODO 10 Znajdź imiona, które nadawane były zarówno dziewczynkom jak i chłopcom (zanotuj najpopularniejsze imię męskie i żeńskie)

frame_10_2 = frame.pivot_table(index = ['Name','year'],values='Amount',columns='Gender',aggfunc=np.sum)

frame_10_2_indx = frame_10_2.index.values.tolist()
df10_2 = frame_10_2.dropna(how='any', axis=0)
df10_2_v2 = df10_2.groupby('Name').sum()


print("Zadanie nr 10: Imiona, które były nadawane zarówno dziewczynkom jak i chłopcom to: ")
print(list(df10_2_v2.index.values))
p = df10_2_v2["F"].idxmax()
o = df10_2_v2["M"].idxmax()
df10_2_v3 = df10_2_v2.groupby(level='Name').sum()
print("Najpopularniejsze imię męskie to: "+str(df10_2_v2["F"].idxmax())+" z ilością urodzeń: "+str(df10_2_v3.loc[o,"F"]))
print("Najpopularniejsze imię żeńskie to: "+str(df10_2_v2["M"].idxmax())+" z ilością urodzeń: "+str(df10_2_v3.loc[p,"M"]))

print("Wykonuję zadanie 11 - proszę chwilę poczekać :)")

#TODO 11 Spróbuj znaleźć najpopularniejsze imiona, które przez pewien czas były imionami żeńskimi/męskimi a następnie stały się imionami męskimi/żeńskimi.

frame1880 = frame.query(("year >= '1800' & year <= '1920'"))
frame2000 = frame.query(("year >= '2000' & year <= '2020'"))

frame1880_v2 = frame1880.groupby(["Name",'Gender']).sum()
frame2000_v2 = frame2000.groupby(["Name",'Gender']).sum()



x_list = list(frame1880_v2.index.get_level_values(level = 0))
xx_list = list(frame1880_v2.index.values)
x2_list = list(frame2000_v2.index.get_level_values(level = 0))
xx2_list = list(frame2000_v2.index.values)



dict1880 = {}
dict2000 = {}
for i in (list(frame1880_v2.index.get_level_values(level = 0))):
    if (str(i),'M') in xx_list:
        if (str(i), 'F') in xx_list:
            if (frame1880_v2.loc[(str(i), "M"), 'frequency_male'] != 0.0) and (frame1880_v2.loc[(str(i), "F"), 'frequency_female'] != 0.0):
                dict1880[str(i)] = frame1880_v2.loc[(str(i), "M"), 'frequency_male'] / (frame1880_v2.loc[(str(i), "M"), 'frequency_male'] + frame1880_v2.loc[(str(i), "F"), 'frequency_female'])
    if (str(i),'M') in xx2_list:
        if (str(i), 'F') in xx2_list:
            if (frame2000_v2.loc[(str(i), "M"), 'frequency_male'] != 0.0) and (frame2000_v2.loc[(str(i), "F"), 'frequency_female'] != 0.0):
                dict2000[str(i)] = frame2000_v2.loc[(str(i), "M"), 'frequency_male'] / (frame2000_v2.loc[(str(i), "M"), 'frequency_male'] + frame2000_v2.loc[(str(i), "F"), 'frequency_female'])


sub_1880_2000 = {}
for a_key,a_value in dict1880.items():
    if a_key in dict2000.keys():
        if a_key not in sub_1880_2000.keys():
            sub_1880_2000[str(a_key)] = abs((dict2000.get(str(a_key))-dict1880.get(str(a_key))))

sorted_x11_dict = {k: v for k, v in sorted(sub_1880_2000 .items(), key=lambda item: item[1],reverse=True)[:2]}
key_list3 = []
for i in sorted_x11_dict.keys():
    key_list3.append(i)


frame11_plot = frame.pivot_table(index = 'year',values='Amount',columns='Name',aggfunc=np.sum)
y11_1=list(frame11_plot.loc[:,str(key_list3[0])].values)
y11_2=list(frame11_plot.loc[:,str(key_list3[1])].values)

fig_11,ax1_11 = plt.subplots()
ax1_11.set_title('Zadanie 11')

ax1_11.plot(years,y11_1,label = str(key_list3[0]))
ax1_11.plot(years,y11_2,label = str(key_list3[1]))
ax1_11.xaxis.set_major_locator(plt.MaxNLocator(6))
ax1_11.set_xlabel("year",fontsize=14)
ax1_11.set_ylabel("Amount",fontsize=14)
ax1_11.legend()

#TODO 12 Wczytaj dane z bazy opisującej śmiertelność w okresie od 1959-2018r w poszczególnych grupach wiekowych: USA_ltper_1x1.sqlite,
# opis: https://www.mortality.org/Public/ExplanatoryNotes.php. Spróbuj zagregować dane już na etapie zapytania SQL.

conn = sqlite3.connect("USA_ltper_1x1.sqlite")
#df_usa_deaths = pd.read_sql_query('SELECT * FROM USA_fltper_1x1 INNER JOIN USA_mltper_1x1 ON USA_mltper_1x1.Year = USA_fltper_1x1.Year AND USA_mltper_1x1.Age = USA_fltper_1x1.Age GROUP BY USA_mltper_1x1.PoPName', conn)
df_usa_deaths = pd.read_sql_query('SELECT * FROM USA_fltper_1x1 UNION ALL SELECT * FROM USA_mltper_1x1', conn)
print("Zadanie nr 12: Wczytane dane to:")
print(df_usa_deaths)

#TODO 13 Wyznacz przyrost naturalny w analizowanym okresie
year_sql = np.arange(df_usa_deaths.iloc[0,2],df_usa_deaths.iloc[-1,2]+1,1)
survival_age = 1

frame13 = frame.query(("year >= '1959' & year <= '2017'"))
frame13_v1 = frame13.groupby("year").sum()

frame13_v2 = list(frame13_v1['Amount'])
frame13_v3 = frame13_v1['Amount'].to_dict()

df_13 = pd.DataFrame()
natural_rate = 0.0

df_13 = df_usa_deaths.groupby('Year').sum()
for i in range(0,len(year_sql)):
    natural_rate += frame13_v2[i] - df_13.loc[year_sql[i],'dx']

print("Zadanie nr 13: Średni przyrost naturalny w analizowanym okresie to: " +str(natural_rate/len(year_sql)))

#TODO 14 Wyznacz i wyświetl współczynnik przeżywalności dzieci w pierwszym roku życia

df_14 = df_usa_deaths.pivot_table(index='Age',columns='Year',values='lx',fill_value=0.0)
df_14_deaths_age = df_usa_deaths.pivot_table(index='Age',columns='Year',values='dx',fill_value=0.0)
df_14_deaths_age_sum = df_14_deaths_age.sum(axis=1)

y14 = []
df_14_v2 = df_usa_deaths.groupby(['Year','Age']).sum()

# wersja druga jesli ktoś używa kolumny LLx jako liczby urodzeń
#y14 = df_14.loc[survival_age,:].values/(df_14.loc[survival_age,:].values + df_14_deaths_age_sum.values[0])

for i in range(0,len(year_sql)):
    y14.append((frame13_v2[i] - df_14_v2.loc[(year_sql[i],0),'dx'])/frame13_v2[i])

fig_14,ax1_14 = plt.subplots()
ax1_14.set_title('Zadanie 14')
ax1_14.plot(year_sql,y14,label='1 year')
ax1_14.xaxis.set_major_locator(plt.MaxNLocator(6))
ax1_14.set_xlabel("year",fontsize=11)
ax1_14.set_ylabel("Survival rate",fontsize=11)



#TODO 15 Na wykresie z pkt 14 wyznacz współczynnik przeżywalności dzieci w pierwszych 5 latach życia (pamiętaj,
# że dla roku urodzenia x należy uwzględnić śmiertelność w grupie wiekowej 0 lat w roku x, 1rok w roku x+1 itd).

death_5_years = 0
dict_deaths = {}
survival_rate = []
df_15 = df_usa_deaths.groupby(['Year','Age','Sex']).sum()


for year in year_sql:
    for k in range(0,5):
        if (year + k >= df_usa_deaths.iloc[0,2]) and (year + k <= df_usa_deaths.iloc[-1,2]):
            death_5_years += df_15.loc[(year+k,k,'f'),'dx'] + df_15.loc[(year+k,k,'m'),'dx']
    survival_rate.append((frame13_v3.get(str(year)) - death_5_years)/frame13_v3.get(str(year)))
    death_5_years = 0


ax1_14.plot(year_sql,survival_rate,label='5 year',color = 'red')
ax1_14.legend(loc='left')

plt.show()
