import program_nagusi as nag

def xynthia_kalkulua():
    bideagpt='XYNTHIA/GPT-2010-2-25_3-4.nc'
    bidea2d='XYNTHIA/2D-2010-2-25_3-4.nc'
    bidea3d='XYNTHIA/3D-2010-2-25_3-4.nc'
    bideaep='XYNTHIA/EP-2010-2-25_3-4.nc'
    bidea_excel="XYNTHIA/xynthia_ibil_datua_ald.xlsx"
    emaitza_totala=nag.datuak_prozesatu(bideagpt,bidea2d,bidea3d,bideaep,bidea_excel,"Xynthia ekaitza")
    return emaitza_totala



def zikloi_klaus_2():
    bideagpt='klaus/GPT-2009-1-21_26.nc'
    bidea2d='klaus/2D-2009-1-21_26.nc'
    bidea3d='klaus/3D-2009-1-21_26.nc'
    bideaep='klaus/EP-2009-1-21_26.nc'
    bidea_excel="klaus/klaus.xlsx"
    emaitza_totala=nag.datuak_prozesatu(bideagpt,bidea2d,bidea3d,bideaep,bidea_excel,"Klaus")
    return emaitza_totala




def zikloi8_kalkulua():  #Fastnet 1979
    bideagpt='ZIKLOI 8/GPT-1979-8-12_17.nc'
    bidea2d='ZIKLOI 8/2D-1979-8-12_17.nc'
    bidea3d='ZIKLOI 8/3D-1979-8-12_17.nc'
    bideaep='ZIKLOI 8/EP-1979-8-12_17.nc'
    bidea_excel="ZIKLOI 8/zikloi8.xlsx"
    emaitza_totala=nag.datuak_prozesatu(bideagpt,bidea2d,bidea3d,bideaep,bidea_excel,"zikloi8 1979")
    return emaitza_totala



def zikloi_braer():
    bideagpt='braer/GPT-1993-1-8_14.nc'
    bidea2d='braer/2D-1993-1-8_14.nc'
    bidea3d='braer/3D-1993-1-8_14.nc'
    bideaep='braer/EP-1993-1-8_14.nc'
    bidea_excel="braer/braer.xlsx"
    emaitza_totala=nag.datuak_prozesatu(bideagpt,bidea2d,bidea3d,bideaep,bidea_excel,"Braer")
    return emaitza_totala






df_xynthia=xynthia_kalkulua()

hasiera="2010-02-26 06:00:00"
bukaera="2010-03-02 00:00:00"
lim_sup=10
lim_inf=-30
lim_sup2=60
lim_inf2=-100
izena="Xynthia"
grafikoa1=nag.irudia1(df_xynthia,izena,hasiera,bukaera,lim_inf,lim_sup)
grafikoa2=nag.irudia2(df_xynthia,izena,hasiera,bukaera,lim_inf2,lim_sup2)



df_klaus=zikloi_klaus()
hasiera="2009-01-22 06:00:00"
bukaera="2009-01-26 00:00:00"
lim_sup=10
lim_inf=-30
lim_sup2=60
lim_inf2=-100
izena="Klaus S"
grafikoa1=nag.irudia1(df_klaus,izena,hasiera,bukaera,lim_inf,lim_sup)
grafikoa2=nag.irudia2(df_klaus,izena,hasiera,bukaera,lim_inf2,lim_sup2)


df_klaus=zikloi_klaus_2()
hasiera="2009-01-22 06:00:00"
bukaera="2009-01-26 00:00:00"
lim_sup=10
lim_inf=-30
lim_sup2=60
lim_inf2=-100
izena="Klaus"
grafikoa1=nag.irudia1(df_klaus,izena,hasiera,bukaera,lim_inf,lim_sup)
grafikoa2=nag.irudia2(df_klaus,izena,hasiera,bukaera,lim_inf2,lim_sup2)


df_zikloi8=zikloi8_kalkulua() #Fastnet 1979
hasiera="1979-08-12 06:00:00"
bukaera="1979-08-16 00:00:00"
lim_sup=10
lim_inf=-30
lim_sup2=60
lim_inf2=-100
izena="Fastnet"
grafikoa1=nag.irudia1(df_zikloi8,izena,hasiera,bukaera,lim_inf,lim_sup)
grafikoa2=nag.irudia2(df_zikloi8,izena,hasiera,bukaera,lim_inf2,lim_sup2)



df_braer=zikloi_braer()
hasiera="1993-01-08 06:00:00"
bukaera="1993-01-12 00:00:00"
lim_sup=20
lim_inf=-30
lim_sup2=60
lim_inf2=-100
izena="Braer"
grafikoa1=nag.irudia1(df_braer,izena,hasiera,bukaera,lim_inf,lim_sup)
grafikoa2=nag.irudia2(df_braer,izena,hasiera,bukaera,lim_inf2,lim_sup2)
