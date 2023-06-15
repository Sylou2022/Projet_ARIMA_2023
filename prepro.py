import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.stattools import adfuller
import statsmodels.graphics.tsaplots as stg


# le travail porte sur la consommation de gaz en résidentiel de 2022 à l'horizon 2050 




#"Affichage de le donnée"
#print(df)

def preprocessing(file):
    df = pd.read_csv("C:/Users/sylva/OneDrive/Bureau/PROJET_ARIMA_devoir/gaz_perspectives_2022_2050.csv")
    
    
    # affichage de la donneé
    print(df)
    # # Affichage de la dimension
    # df.shape
    
    # Suppression des colonnes unitiles
    # df = df.drop('batiment', axis=1)
    df = df.drop('mobilite', axis=1)
    df = df.drop('industrie', axis=1) 
    df = df.drop('production_d_electricite_centralisee_et_cogeneration_industrielle', axis=1)
    
    # affichage de la donneé
    print("\n")
    
    print(df)
    print("\n")
  
    # Verification des elements manquants
    print("\n")
    
    df.isnull().sum()
    #Remplacer les données manquantes 
    df =df.interpolate()
    
    #vérification netoyage et verification 
    df.isnull().sum()
    print("\n")
    print(df)
    print("\n")
    # une copie de la dataframe .
    df1= df.copy()
    print("\n")
    print(df1)
    print("\n")
    ## Nous allons convertir l'index en date comprehenssible par pandas
    df.index = pd.to_datetime(df.dt)
    
    print("\n")
    print(df.describe())
    #Netoyage de la donnée
    df1 = df1.drop('tertiaire', axis=1)
    
    
    df1=df1.drop('agriculture',axis=1)
    df1.plot()
    
    plt.show()
    df1 = df1.drop('dt', axis=1)
    print("\n")
    print(df1)
    print("\n")
   
    #Histogramme Pour vérifier la temdance  
    sns.distplot(df1, hist=False);
    
    #forme de modele:
    print("Additif".center(50,"-"))
    #df1.index = pd.DatetimeIndex(df1.index, freq=None)
    MDA = seasonal_decompose(df1,period=12).plot()
    print("Multiplicatif".center(50,"-"))
    
    MDM = seasonal_decompose(df1, model='multiplicatif', period=12).plot()

    #On en deduit que c'est un model multiplicatif car la variance est trop grande au niveau de l'additif.
    # Rendons additif ce model
    #Première approche le technique de log
    df1 = np.log(df1)
    print(df1)
    #vérification
    plt.show()
    sns.distplot(df1, hist= False)
    #sns.kdeplot(df1)
    #deuxième approche la différentiation
    df1 = df1.diff().dropna()
    
    print(df1)
    #Vérification de la distribution 
    plt.show()
    sns.distplot(df1, hist = False)
    
    
   
    #ACF(Autocorrelation Function)
    resultat_adf1 = adfuller(df1)
    print(resultat_adf1)
    
    ACF = resultat_adf1[0]
    print(ACF)
    p_value = resultat_adf1[1]
    print(p_value)
    result = seasonal_decompose(df1, model='additive', period=4)
    result.plot()
    plt.show()

   
    result = seasonal_decompose(df1, model='additive', period=4)
    result.plot();
    plt.show()
    #P_value est inferieur à 5%  
    
    ## la courbe autocorrélation et autocorrélation partielle
    
    #Autocorrelation
    stg.plot_acf(df1)
    plt.show()
    
    #Partielle
    stg.plot_pacf(df1)
    plt.show()
    return df1
