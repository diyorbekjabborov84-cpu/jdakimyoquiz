"""25 C thermodynamic models; potentials referenced to SHE. Not experimental data."""
import math,csv
from pathlib import Path
R=8.31446261815324;T=298.15;F=96485.33212
S=math.log(10)*R*T/F
E0={'H':0.,'Zn':-.7618,'Cu':.337,'Fe':.771,'Mn':1.507,'NO':.957,'per_water':1.776,'oxy_per':.695}
def nernst(e,n,logq):return e-S/n*logq
def ph_potential(e,m,n,ph):return e-S*m/n*ph
def thermo(e,n):return -n*F*e,n*e/S

def worked():
    mn=.02*.02;fe=.05*.05;xi=min(mn,fe/5);vol=.07
    fe2=(fe-5*xi)/vol;fe3=5*xi/vol;mn2=xi/vol
    e=E0['Fe']+S*math.log10(fe3/fe2)
    log_mn4_mn2=5/S*(e-E0['Mn'])+8 # aH=0.1, E=E0+S/5 log(MnO4/Mn2)-8S/5 pH
    return dict(xi=xi,Fe2=fe2,Fe3=fe3,Mn2=mn2,H_consumed=8*xi,E=e,log_Mn4_Mn2=log_mn4_mn2,Mn4=mn2*10**log_mn4_mn2)

def save():
    a=Path(__file__).resolve().parents[1]/'rasmlar/redoks';a.mkdir(parents=True,exist_ok=True)
    def csvout(name,fields,rows):
        with (a/(name+'.csv')).open('w',newline='') as f:
            w=csv.writer(f);w.writerow(fields);w.writerows(rows)
    csvout('energiya',['E_cell_V','dG_n1_kJ','dG_n2_kJ','dG_n5_kJ'],[[e,*[thermo(e,n)[0]/1000 for n in [1,2,5]]] for e in [-.2+i*.005 for i in range(281)]])
    csvout('ph',['pH','H_V','Mn_V','NO_V'],[[p,ph_potential(0,2,2,p),ph_potential(1.507,8,5,p),ph_potential(.957,4,3,p)] for p in [i*.02 for i in range(201)]])
    csvout('sigim',['route','electrons_per_center'],[['N+5_to_NO2',1],['N+5_to_NO',3],['N+5_to_NH4',8],['S+6_to_SO2',2],['S+6_to_S',6],['S+6_to_H2S',8]])
    csvout('peroksid',['pH','water_V','oxygen_V','difference_V'],[[p,ph_potential(1.776,2,2,p),ph_potential(.695,2,2,p),1.081] for p in [i*.02 for i in range(201)]])
if __name__=='__main__':
    save();print('S=',S,'Mn/Fe dG/logK',thermo(.736,5),'peroxide',thermo(1.081,2));print(worked())
