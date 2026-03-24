import pandas as pd

df = pd.read_csv('4_psychnouns_ratings.csv', sep = ";", encoding = 'utf-8')
nomi = df['noun'].to_list()

bases = {'andare_in_LVC' : ['estasi','panico','frenesia','ansia','paranoia','collera','furia'],
'avere_LVC' : ['passione','invidia','simpatia','agio','odio','amore','rabbia','ansia','affetto','antipatia','nausea','avversione','orrore','calma','pena','coraggio','rimorso','desiderio','terrore','diffidenza','interesse','disagio','letizia','disgusto','nostalgia','dolore','orgoglio','emozione','paranoia','empatia','paura','entusiasmo','pietà ','fastidio','rancore','fiducia','schifo','furia','soggezione','gioia','timore','impressione','vergogna'],
'dare_LVC' : ['letizia','timore','orgoglio','angoscia','gioia','ansia','nausea','calma','pena','coraggio','vergogna','disagio','impressione','dolore','malinconia','emozione','noia','entusiasmo','paura','euforia','soggezione','fastidio','tormento','fiducia','gaudio','inquietudine'],
'essere_in_LVC' : ['panico','dubbio','pena','angoscia','estasi','ansia','paranoia','apprensione','collera','frenesia'],
'fare_LVC' : ['rabbia','orrore','stupore','antipatia','pena','coraggio','schifo','dolore','timore','fastidio','paura','impressione','pietà ','invidia','ribrezzo','malinconia','simpatia','meraviglia','terrore','nausea','nostalgia','vergogna'],
'mettere_LVC' : ['malinconia','rabbia','orrore','angoscia','terrore','ansia','nostalgia','coraggio','paura','entusiasmo','soggezione','fiducia','vergogna','gioia','inquietudine'],
'prendere_LVC' : ['paura','interesse','pena','coraggio','fiducia'],
'provare_LVC' : ['passione','meraviglia','schifo','amore','odio','angoscia','rabbia','ansia','timore','antipatia','noia','astio','orrore','avversione','pena','desiderio','ribrezzo','diffidenza','stupore','disagio','malinconia','disgusto','nausea','dolore','nostalgia','eccitazione','orgoglio','emozione','panico','empatia','paura','fastidio','pietà ','fiducia','rancore','gioia','rimorso','indifferenza','simpatia','affetto','terrore','interesse','vergogna','invidia','inquietudine'],
'sentire_LVC' : ['passione','nausea','rabbia','amore','odio','avversione','pena','cordoglio','simpatia','desiderio','nostalgia','disagio','orrore','dolore','paura','emozione','pietà ','fastidio','rimorso','gioia','timore','affetto','vergogna'],
'conversion_caus' : ['strazio','schifo','nausea','angoscia','sollazzo','calma','meraviglia','disgusto','paranoia','emozione','shock','entusiasmo','stizza','impressione','tormento','interesse','agio'],
'parasynthesis_caus' : ['noia','timore','passione','collera','malinconia','coraggio','orgoglio','dolore','paura','fastidio','impazienza','ira'],
'conversion_si' : ['impazienza','meraviglia','stizza','amore','panico','angoscia','impressione','calma','vergogna','disgusto','nausea','emozione','entusiasmo','interesse'],
'parasynthesis_si' : ['orgoglio','rabbia','passione','amore','malinconia','collera','paranoia','dolore','paura','fastidio','timore','furia','ira'],
'conversion_stat' : ['odio','schifo','pena','gioia','invidia','letizia'],
'conversion_si_stat' :  ['vergogna','strazio','sollazzo','angoscia','interesse','tormento'],
'suffixation_stat' : ['empatia', 'simpatia', 'antipatia'],
'parasynthesis_si_stat' : ['noia'],
'suffixation_caus' : ['euforia', 'terrore'],
'farsi_LVC' : ['coraggio'],
'mettersi_LVC' : ['paura']}

nuovo_dic = dict()

for i in bases.keys():
    nuovo_dic[i] = ['other_cxns',]*len(nomi)

for j in range(len(nomi)):
    for i in bases.keys():
        if nomi[j] in bases[i]:
            nuovo_dic[i][j] = i

df2 = pd.DataFrame.from_dict(nuovo_dic)
df3 = pd.concat([df,df2], axis = 1)
df3.to_csv('6_dataset_pca.csv', sep = ";", encoding = 'utf-8', index=False)
