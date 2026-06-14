import pandas as pd
import numpy as np
import prestatu as pr
import ekuazioa as ek
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def datuak_prozesatu(bideagpt,bidea2d,bidea3d,bideaep,bidea_excel,izena):
    ds=pr.datuak_zabaldu(bideagpt,bidea2d,bidea3d,bideaep)
    latitudeak,longitudeak,denb=pr.ibilbidea_irakurri(bidea_excel)

    emaitzak=[]
    t_6=None

    for t, lat_zen, lon_zen in zip(denb, latitudeak, longitudeak):
        
        kutxa=pr.kutxa_lortu(ds,t,lat_zen,lon_zen)

        hizt={
                "denbora":t
        }
        if t_6 is not None: 
            kutxa_6=pr.kutxa_lortu(ds,t_6,lat_zen,lon_zen)  #lat eta lon berdinean baina 6 ordu lehenagoko balioak
            balantzea_hiztegia=ek.balantzea(kutxa,kutxa_6)  
            hizt.update(balantzea_hiztegia)
        else:  
            hutsik={"Dp":np.nan,"D\u03A6":np.nan,"ITT":np.nan,"EP":np.nan,"RESpte":np.nan,"TADV":np.nan,"VMT":np.nan,"DIABres":np.nan,"DIABptend":np.nan}
            hizt.update(hutsik)
            
        emaitzak.append(hizt) 
        t_6=t 

    df = pd.DataFrame(emaitzak)
    print(df)
    df.to_excel(f"emaitza_{izena}.xlsx")

    return df




def irudia1(df_osoa,izena,hasiera,bukaera,lim_inf,lim_sup):
    
    fig,ax=plt.subplots(figsize=(8,3),dpi=100)

    df_osoa["denbora"] = pd.to_datetime(df_osoa["denbora"])
    df_osoa=df_osoa.set_index("denbora")
    #aukeratu dugu irudikatzea nahi dugun egun eta ordu tartea soilik
    df=df_osoa.loc[hasiera:bukaera]



    terminoak=["D\u03A6","ITT","EP","RESpte"]
    df_irudikatzeko=df[terminoak]
    

    izenak_legend = {
        "D\u03A6": r"$D \Phi$",
        "ITT": "ITT",
        "EP": "EP",
        "RESpte": r"$RES_{PTE}$",
        "Dp": r"$D p$" 
    }
    
    df_positive=df_irudikatzeko.clip(lower=0)   #Banatu balio positibo eta negatiboak
    df_negative=df_irudikatzeko.clip(upper=0)

    df_positive.plot(kind='bar', stacked=True, ax=ax, color=["#00b427", "#ff0e0e","#00abee","#888383"],legend=False)
    df_negative.plot(kind='bar', stacked=True, ax=ax, color=["#00b427", "#ff0e0e","#00abee","#888383"],legend=False)


    ax.plot(range(len(df)),df["Dp"],label="Dp",color="black")

    ax.set_axisbelow(True)
    ax.grid(True,linestyle='--',color="gray",linewidth=0.5)

    ax.axhline(0,color="black",linewidth=0.8)

    etiketak = [d.strftime('%Y-%m-%d') for d in df.index]

    ax.set_xticks(range(0, len(df), 4))
    ax.set_xticklabels(etiketak[::4], rotation=0, ha="left")
    ax.set_xlabel("")

    plt.xticks(rotation=0,ha="left")
    ax.set_ylim(lim_inf,lim_sup)  
    ax.set_yticks(np.arange(lim_inf, lim_sup + 1, 10))
    ax.set_ylabel("[hPa/6h]")



    handles, labels = ax.get_legend_handles_labels()
    label_berriak = [izenak_legend.get(l, l) for l in labels]
    by_label = dict(zip(label_berriak, handles))
    
    ax.legend(by_label.values(), by_label.keys(), bbox_to_anchor=(1.05, 1), loc="upper left")


    plt.tight_layout()

    plt.savefig(f"irudia_PTE_{izena}.pdf",dpi=100)
    plt.show()
    plt.close()



def irudia2(df_osoa,izena,hasiera,bukaera,lim_inf2,lim_sup2):
    fig,ax=plt.subplots(figsize=(8,3),dpi=100)


    df_osoa["denbora"] = pd.to_datetime(df_osoa["denbora"])
    df_osoa=df_osoa.set_index("denbora")
    df=df_osoa.loc[hasiera:bukaera]
    


    terminoak=["TADV","VMT","DIABres"]
    df_irudikatzeko=df[terminoak]  


    izenak_legend = {
        "TADV": "TADV",
        "VMT": "VMT",
        "DIABres": r"$DIAB_{RES}$",
        "ITT": "ITT",
        "DIABptend": r"$DIAB_{ptend}$"
    }
    

    df_positive = df_irudikatzeko.clip(lower=0)
    df_negative = df_irudikatzeko.clip(upper=0)

    df_positive.plot(kind='bar', stacked=True, ax=ax, color=["#FF0000", "#016fb3","#ffe600"],legend=False)
    df_negative.plot(kind='bar', stacked=True, ax=ax, color=["#FF0000", "#016fb3","#ffe600"],legend=False)

    ax.plot(range(len(df)),df["ITT"],label="ITT",color="black")

    ax.set_axisbelow(True)
    ax.grid(True,linestyle='--',color="gray",linewidth=0.5)

    ax.axhline(0,color="black",linewidth=0.8)
   

    etiketak = [d.strftime('%Y-%m-%d') for d in df.index]
    
    
    ax.set_xticks(range(0, len(df), 4))
    ax.set_xticklabels(etiketak[::4], rotation=0, ha="left")
    ax.set_xlabel("")

    plt.xticks(rotation=0,ha="left")
    ax.set_ylim(lim_inf2,lim_sup2) 
    ax.set_yticks([-60,-40,-20,0,20,40,60])
    ax.set_ylabel("[hPa/6h]")


    ax2=ax.twinx()
    ax2.bar(range(len(df)),df["DIABptend"],label="DIABptend",color="gray",width=0.2)

    ax2.set_ylim(0,300)  
    ax2.set_yticks([0,30,60,90])
    ax2.set_ylabel("[%]",rotation=0)
    

    linea1, label1 = ax.get_legend_handles_labels()   
    linea2, label2 = ax2.get_legend_handles_labels()  


    handles = linea1 + linea2
    labels = label1 + label2


    label_berriak = [izenak_legend.get(l, l) for l in labels]
    by_label = dict(zip(label_berriak, handles))

    ax.legend(by_label.values(), by_label.keys(), bbox_to_anchor=(1.1, 1), loc="upper left", fontsize=9)



    plt.tight_layout()
    plt.savefig(f"irudia_ITT_{izena}.pdf",dpi=100)
    plt.show()
    plt.close()



    
