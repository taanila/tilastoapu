#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def kuvioasetukset(leveys=6.4, korkeus=4.8):
    
    """
    Säätää kuvioiden ulkoasua ja palauttaa figure ja axes olion.
    
    Parametrit:
    
        leveys: Kuvion leveys tuumina.
        korkeus: Kuvion korkeus tuumina.
    """
    
    from matplotlib import rcParams
    
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['Arial', 'Tahoma', 'Verdana']
    
    plt.rc('font', size=10)          
    plt.rc('axes', titlesize=10)     
    plt.rc('axes', labelsize=12)    
    plt.rc('xtick', labelsize=10)    
    plt.rc('ytick', labelsize=10)    
    plt.rc('legend', fontsize=10)    
    plt.rc('figure', titlesize=14)
    
    sns.set_palette(None)
    
    fig, ax = plt.subplots(figsize = (leveys, korkeus))
    return fig, ax

def frekve(data, muuttuja, lista=0, dropna=1, leveys=6.4, korkeus=4.8):

    """
    Laskee muuttujan frekvenssitaulukon ja tekee prosenteista vaakapylväskaavion.
    
    Parametrit:
    
        data: dataframe, jota käytetään.
        muuttuja: muuttuja, jolle frekvenssitaulukko lasketaan.
        lista: ei pakollinen, muuttujan numeerisia arvoja vastaavat tekstimuotoiset 
            arvot listana.
        dropna: ei pakollinen, dropna=0: puuttuvat arvot näytetään frekvenssitaulukossa, 
            dropna=1 (oletus): puuttuvat arvot poistetaan ennen frekvenssitaulukon 
            laskemista.
        leveys: ei pakollinen, kuvan leveys tuumina.
        korkeus: ei pakollinen, kuvan korkeus tuumina.
    """

    frekve = data[muuttuja].value_counts(dropna = dropna).sort_index().to_frame()
    frekve['%'] = data[muuttuja].value_counts(normalize = True, dropna = dropna) * 100
    frekve.columns = ['Lkm', '%']
    if (lista != 0) & (dropna == 1):
        try:
            frekve.index = lista
        except ValueError:
            print('Hupsista! Lista ei taida sopia tilanteeseen?')
    elif (lista != 0) & (data[muuttuja].isnull().sum() > 0):
        try:
            frekve.index = lista + ['Tieto puuttuu']
        except ValueError:
            print('Hupsista! Lista ei taida sopia tilanteeseen?')
    elif (lista != 0) & (data[muuttuja].isnull().sum() == 0):
        try:
            frekve.index = lista
        except ValueError:
            print('Hupsista! Lista ei taida sopia tilanteeseen?')
    
    fig, ax = kuvioasetukset(leveys, korkeus)
    
    frekve['%'].plot.barh(ax = ax, width = 0.8)
    n = frekve['Lkm'].sum()
    ax.set_xlabel('% vastanneista, n=' + str(n))
    ax.set_xticklabels(['{:.0f} %'.format(x) for x in ax.get_xticks()])
    ax.grid(axis='x')
    ax.set_axisbelow(True)
    ax.tick_params(axis='both', length=0)
    if lista != 0:
        ax.set_yticklabels(lista)
    
    frekve.loc['Yhteensä'] = frekve.sum()
    frekve['Lkm'] = frekve['Lkm'].apply('{:.0f}'.format)
    frekve['%'] = frekve['%'].apply('{:.2f} %'.format)
    
    return frekve, fig, ax

def ristiin(data, rivimuuttuja, sarakemuuttuja, rivilista=0, sarakelista=0, kuvio='%', leveys=6.4, korkeus=4.8):
    
    """
    Laskee kahden muuttujan välisen ristiintaulukoinnin ja esittää sen vierekkäisinä 
        pylväinä tai 100 % pinottuina pylväinä.
    
    Parametrit:
    
        data: dataframe, jota käytetään.
        rivimuuttuja: muuttuja, jonka arvo tulevat taulukon riviotsikoiksi.
        sarakemuuttuja: ei pakollinen, muuttuja, jonka arvo tulevat taulukon sarakeotsikoiksi.
        rivilista: ei pakollinen, rivimuuttujan numeerisia arvoja vastaavat tekstimuotoiset arvot listana.
        sarakelista: ei pakollinen, sarakemuuttujan numeerisia arvoja vastaavat tekstimuotoiset arvot listana.
        kuvio: ei pakollinen, oletuksena kuvio='%', jolloin kuviona 100 % pinotut pylväät; 
        jos kuvio='n', niin kuviona vierekkäiset lukumääräpylväät.
        leveys: ei pakollinen, kuvion leveys tuumina.
        korkeus: ei pakollinen, kuvion korkeus tuumina.
    """
    
    print('Ristiintaulukointi: riveillä', rivimuuttuja, ', sarakkeissa', sarakemuuttuja)
    
    risti_lkm = pd.crosstab(index = data[rivimuuttuja], columns = data[sarakemuuttuja], margins = True)
    risti = pd.crosstab(index = data[rivimuuttuja], columns = data[sarakemuuttuja], normalize = 'columns', margins = True) * 100
    if rivilista != 0:
        try:
            risti.index = rivilista
        except ValueError:
            print('Hupsista! Rivilista ei taida sopia tilanteeseen?')
    risti.loc['n'] = risti_lkm.iloc[-1]
    if sarakelista != 0:
        try:
            risti_lkm.columns = sarakelista + ['All']
            risti.columns = sarakelista + ['Kaikki']
        except ValueError:
            print('Hupsista! Sarakelista ei taida sopia tilanteeseen?')
    else:
        risti = risti.rename(columns = {'All': 'Kaikki'})
    
    fig, ax = kuvioasetukset(leveys, korkeus)
    if kuvio != '%':
        risti_lkm.drop('All', axis = 1).iloc[0:risti_lkm.shape[0]-1,:].plot.bar(ax = ax, width = 0.8)
        ax.set_ylabel('Lukumäärä')
        ax.grid(axis = 'y')
        ax.set_axisbelow(True)
        ax.tick_params(axis = 'both', length = 0)
        if rivilista != 0:
            ax.set_xticklabels(rivilista) 
    else:
        from matplotlib.colors import ListedColormap
        ax.set_xlim(0, 100)
        risti.drop('Kaikki', axis = 1).iloc[0:risti.shape[0]-1,:].T.plot.barh(ax = ax, width = 0.8, stacked = True,
                colormap = ListedColormap(sns.color_palette("RdBu", 10)))
        ax.set_xlabel('%')
        ax.grid(axis = 'x')
        ax.set_axisbelow(True)
        ax.tick_params(axis = 'both', length = 0)
        ax.set_xticklabels(['{:.0f} %'.format(x) for x in ax.get_xticks()])
        ax.legend(ncol = risti.shape[0]-1, bbox_to_anchor = (0, 1), loc = 'lower left')
    
    risti.loc['n'] = risti.loc['n'].apply('{:.0f}'.format)
    for rivi in range(0, risti.shape[0]-1):
        risti.iloc[rivi] = risti.iloc[rivi].apply('{:.2f} %'.format)
    return risti, fig, ax
 
def moniv(data, monivalinta, leveys = 6.4, korkeus = 4.8):
    
    """
    Laskee monivalinnan vaihtoehtojen valintojen lukumäärät ja prosentit sekä tekee vaakapylväskaavion.
    
    Parametrit:
    
        data: dataframe, jota käytetään.
        monivalinta: lista muuttujista, jotka kuuluvat monivalintaan.
        leveys: ei pakollinen, kuvion leveys tuumina.
        korkeus:ei pakollinen, kuvion korkeus tuumina.    
    """
    
    moniv = data[monivalinta].count().to_frame('lkm').sort_values(by = 'lkm', ascending = False)
    n = data.shape[0]
    moniv['% vastaajista'] = moniv['lkm'] / n * 100
    moniv.index = monivalinta
        
    fig, ax = kuvioasetukset()
    moniv['% vastaajista'].plot.barh(ax = ax, width = 0.8)
    ax.set_xlabel('% vastaajista, n=' + str(n))
    ax.grid(axis='x')
    ax.set_axisbelow(True)
    ax.tick_params(axis='both', length=0)
    ax.set_xticklabels(['{:.0f} %'.format(x) for x in ax.get_xticks()])
    
    moniv['% vastaajista'] = moniv['% vastaajista'].apply('{:.2f} %'.format)
    
    return moniv, fig, ax


def moniv_ristiin(data, monivalinta, muuttuja, lista=0, leveys = 6.4, korkeus = 4.8):
    
    """
    Laskee monivalinnan vaihtoehtojen valintojen lukumäärät ja prosentit sekä tekee vaakapylväskaavion.
    
    Parametrit:
    
        data: dataframe, jota käytetään.
        monivalinta: lista muuttujista, jotka kuuluvat monivalintaan.
        muuttuja: ryhmittelevä muuttuja.
        lista: ei pakollinen, ryhmittelevän muuttujan tekstimuotoiset arvot listana.
        leveys: ei pakollinen, kuvion leveys tuumina.
        korkeus:ei pakollinen, kuvion korkeus tuumina.    
    """
    
    moniv_ristiin = data.groupby(muuttuja)[monivalinta].count()
    n_arvot = []
    i = 0
    for arvo in moniv_ristiin.index:
        n_arvot.append(data[muuttuja][data[muuttuja] == arvo].count())
        moniv_ristiin.iloc[i] = moniv_ristiin.iloc[i] / n_arvot[i] * 100
        i+=1
    moniv_ristiin['n'] = n_arvot
    if lista != 0:
        try:
            moniv_ristiin.index = lista
        except ValueError:
            print('Hupsista! Lista ei taida sopia tilanteeseen?')
       
    fig, ax = kuvioasetukset(leveys, korkeus)
    moniv_ristiin.drop('n', axis = 1).plot.barh(ax = ax, legend = 'reverse')
    ax.set_xlabel('%')
    ax.grid(axis = 'x')
    ax.set_axisbelow(True)
    ax.tick_params(axis = 'both', length = 0)
    ax.set_xticklabels(['{:.0f} %'.format(x) for x in ax.get_xticks()])
        
    moniv_ristiin.loc[:,'n'] = moniv_ristiin.loc[:,'n'].apply('{:.0f}'.format)
    for i in range(0, moniv_ristiin.shape[1]-1):
        moniv_ristiin.iloc[:,i] = moniv_ristiin.iloc[:,i].apply('{:.2f} %'.format)
    
    return moniv_ristiin, fig, ax

