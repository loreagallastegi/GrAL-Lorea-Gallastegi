import numpy as np
import metpy.calc as mpcalc
from metpy.units import units
import metpy.constants as mconst


#==============================================
#=========kalkuluetarako prestaketa============


def rho_surface(kutxa):
    
    p=kutxa["sp"]*units.Pa
    t=kutxa["t2m"]*units.K
    td=kutxa["d2m"]*units.K
    tv_sfc=mpcalc.virtual_temperature_from_dewpoint(p,t,td)

    rho=p/(mconst.Rd*tv_sfc) 
    return rho 

def tv(kutxa):

    q=kutxa["q"]*units("kg/kg")
    t=kutxa["t"]*units.K
    mixing_ratio=mpcalc.mixing_ratio_from_specific_humidity(q)

    tv=mpcalc.virtual_temperature(t,mixing_ratio)
    return tv


def dxdy(kutxa):

    dphi=np.deg2rad(0.75) 
    lat_rad_media=np.deg2rad(kutxa["latitude"].mean()) 
    R=mconst.earth_avg_radius

    dx=R*np.cos(lat_rad_media)*dphi 
    dy=R*dphi  
    return dx,dy


def adb_maila(kutxa,maila,dx,dy,tv):

    u=kutxa["u"].sel(pressure_level=maila).values
    v=kutxa["v"].sel(pressure_level=maila).values
    tv=tv.sel(pressure_level=maila).values
    adb=np.zeros((5,5)) 
    for i in range(1,4):
        for j in range(1,4):
            gradx=(tv[j,i+1]-tv[j,i-1])/(2*dx) 
            grady=(tv[j-1,i]-tv[j+1,i])/(2*dy) 
                                                
            adb[j,i]=-(u[j,i]*gradx+v[j,i]*grady)  
    
    return adb


#========================================================
#============termino bakoitzaren kalkulua================


def dp(kutxa,kutxa_6):

    p0=kutxa["sp"].mean()
    p6=kutxa_6["sp"].mean()

    emaitza=(p0-p6)/100
    return emaitza.item()

def gpt(kutxa,kutxa_6):

    gpt0=kutxa["z"].mean()
    gpt6=kutxa_6["z"].mean()
    dif=gpt0-gpt6
    rho_0=rho_surface(kutxa).mean()
    rho_6=rho_surface(kutxa_6).mean()
    rho_bb=(rho_0+rho_6)/2

    emaitza=(rho_bb*dif)/100
    return emaitza.item().magnitude

def ep(kutxa,kutxa_6):

    g=mconst.earth_gravity
    rho_ura=mconst.density_water
    e=kutxa["e"].mean()-kutxa_6["e"].mean()
    tp=kutxa["tp"].mean()-kutxa_6["tp"].mean()

    emaitza=g*(e-tp)*rho_ura/100 
    return emaitza.item().magnitude

def itt(kutxa,kutxa_6):

    tv_0=tv(kutxa).mean(dim=["latitude","longitude"])
    tv_6=tv(kutxa_6).mean(dim=["latitude","longitude"])
    
    p=kutxa.coords["pressure_level"].values[::-1] 
    #----------lehen batura: 1000hPa---------------------------------
    msl_media=kutxa["msl"].mean()
    dp_0=msl_media/100-((p[0]+p[1])/2)  
    dtv_0=tv_0.sel(pressure_level=p[0])-tv_6.sel(pressure_level=p[0])
    batura0=dtv_0*dp_0/p[0]
    #----------tarteko batura---------------------------------
    batura_tarte=0
    for i in range(1,len(p)-1):
        dp=(p[i-1]-p[i+1])/2
        dtv=tv_0.sel(pressure_level=p[i])-tv_6.sel(pressure_level=p[i])
        
        batura_tarte+=dtv*dp/p[i]
    #---------azken batura: 100 hPa---------------------------------------
    dtv_n=tv_0.sel(pressure_level=p[-1])-tv_6.sel(pressure_level=p[-1])
    dp_n=p[-2]-p[-1]
    batura_azkena=dtv_n*dp_n/p[-1]

    integrala=float(batura0+batura_tarte+batura_azkena)
   
    rho_sfc=rho_surface(kutxa).mean()
    emaitza=rho_sfc*mconst.Rd.magnitude*integrala/100
    return emaitza.item().magnitude                   


def tadv(kutxa):
    dx,dy=dxdy(kutxa)
    tv_tadv=tv(kutxa)   
    p=kutxa.coords["pressure_level"].values[::-1]
    
    #----------lehen batura: 1000hPa---------------------------------
    msl_media=kutxa["msl"].mean()
    dp_0=msl_media/100-((p[0]+p[1])/2)  
    adb_0=adb_maila(kutxa,p[0],dx,dy,tv_tadv)

    batura0=adb_0.mean()*dp_0/p[0]  
    
    #----------tarteko batura---------------------------------
    batura_tarte=0
    for i in range(1,len(p)-1):
        dp=(p[i-1]-p[i+1])/2
        adb_tarte=adb_maila(kutxa,p[i],dx,dy,tv_tadv)       
        batura_tarte+=adb_tarte.mean()*dp/p[i]


    #---------azken batura: 100 hPa---------------------------------------
    dp_n=p[-2]-p[-1]
    adb_n=adb_maila(kutxa,p[-1],dx,dy,tv_tadv)
    batura_azkena=adb_n.mean()*dp_n/p[-1]

    integrala=float(batura0+batura_tarte+batura_azkena)
    
    rho_sfc=rho_surface(kutxa).mean()
    emaitza=rho_sfc*mconst.Rd.magnitude*integrala*21600/100 
    return emaitza.item().magnitude
    

def vmt(kutxa):
    tv_tadv=tv(kutxa).mean(dim=["latitude","longitude"])
    p=kutxa.coords["pressure_level"].values[::-1] 
    w=kutxa["w"].mean(dim=["latitude","longitude"])
    Rd=mconst.Rd.magnitude
    Cp=mconst.Cp_d.magnitude
    dist=-2500 
    #----------lehen batura: 1000hPa--------aurreranzko diferentziarekin-------------------------
    msl_media=kutxa["msl"].mean()
    dp_0=msl_media/100-((p[0]+p[1])/2)  
    tv_0=tv_tadv.sel(pressure_level=p[0])
    w_0=w.sel(pressure_level=p[0])
    dtv_0=(tv_tadv.sel(pressure_level=p[1])-tv_tadv.sel(pressure_level=p[0]))
    kalkulua0=(((Rd*tv_0)/(Cp*p[0]*100))-(dtv_0/dist))*w_0 
    
    batura0=kalkulua0*dp_0/p[0]  
    #----------tarteko batura---------diferentzia zentratuekin------------------------
    batura_tarte=0
    for i in range(1,len(p)-1):

        dp=(p[i-1]-p[i+1])/2

        tv_i=tv_tadv.sel(pressure_level=p[i])
        dtv_i=(tv_tadv.sel(pressure_level=p[i+1])-tv_tadv.sel(pressure_level=p[i-1]))
        w_i=w.sel(pressure_level=p[i])
        kalkulua_tarte=(((Rd*tv_i)/(Cp*p[i]*100))-(dtv_i/(2*dist)))*w_i
               
        batura_tarte+=kalkulua_tarte*dp/p[i]
        

    #---------azken batura: 100 hPa---------------------------------------
    
    dp_n=p[-2]-p[-1]
    tv_n=(tv_tadv.sel(pressure_level=p[-1]))
    dtv_azk=(tv_tadv.sel(pressure_level=p[-1])-tv_tadv.sel(pressure_level=p[-2]))
    w_n=w.sel(pressure_level=p[-1])
    kalkulua_n=(((Rd*tv_n)/(Cp*p[-1]*100))-(dtv_azk/dist))*w_n
    batura_azkena=kalkulua_n*dp_n/p[-1]

    integrala=float(batura0+batura_tarte+batura_azkena)
    
    rho_sfc=rho_surface(kutxa).mean()
    emaitza=rho_sfc*Rd*integrala*21600/100 
    return emaitza.item().magnitude
    

#=================portzentaia==========================

def portzentaia(balioa_tadv,balioa_vmt,balioa_diabres): 
    portzentaia=0
    diabres=abs(balioa_diabres)
    tadv=abs(balioa_tadv)
    vmt=abs(balioa_vmt)
    

    if (balioa_diabres*balioa_tadv>0 and balioa_diabres*balioa_vmt>0):
        portzentaia=(diabres/(tadv+vmt+diabres))*100
    elif (balioa_diabres*balioa_tadv>0 and balioa_diabres*balioa_vmt<0):
        portzentaia=(diabres/(tadv+diabres))*100
    elif (balioa_diabres*balioa_vmt>0 and balioa_diabres*balioa_tadv<0):
        portzentaia=(diabres/(vmt+diabres))*100
    return portzentaia



#======================================================
#==================BALANTZEA===========================


def balantzea(kutxa,kutxa_6):
    balioa_dp=dp(kutxa,kutxa_6)
    balioa_gpt=gpt(kutxa,kutxa_6)
    balioa_itt=-itt(kutxa,kutxa_6) 
    balioa_ep=ep(kutxa,kutxa_6)
    balioa_respte=balioa_dp-(balioa_gpt+balioa_itt+balioa_ep)

    balioa_tadv=-(tadv(kutxa)+tadv(kutxa_6))/2
    balioa_vmt=(vmt(kutxa)+vmt(kutxa_6))/2
    balioa_diabres=balioa_itt-balioa_tadv-balioa_vmt

    balioa_ptend=portzentaia(balioa_tadv,balioa_vmt,balioa_diabres)


   

    return {
            "Dp":balioa_dp,
            "D\u03A6":balioa_gpt,
            "ITT":balioa_itt,
            "EP":balioa_ep,
            "RESpte":balioa_respte,
            "TADV":balioa_tadv,
            "VMT":balioa_vmt,
            "DIABres":balioa_diabres,
            "DIABptend":balioa_ptend
        }


