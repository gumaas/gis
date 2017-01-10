# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 11:28:22 2017

@author: gumas
"""

import numpy
import matplotlib.pyplot as plt

obszar=(1,1)
zakresjakosci=(1,1)
losuj_wierzcholek_startowy = False

def generuj_drogi( liczba_wierzcholkow, liczba_drog_jednokierunkowych ) :
    tablica_wiercholkow = obszar*numpy.random.rand(liczba_wierzcholkow,2)
    jakosc_drogi = ( zakresjakosci[1]-zakresjakosci[0])*numpy.random.rand(liczba_wierzcholkow,2)+zakresjakosci[0]
    drogi_jednokierunkowe = (liczba_wierzcholkow*numpy.random.rand(liczba_drog_jednokierunkowych)).astype(int)
    
    return [ tablica_wiercholkow, jakosc_drogi, drogi_jednokierunkowe ]
    

def oblicz_odleglosc( v1, v2 ):
    dx = v2[0] - v1[0]
    dy = v2[1] - v1[1]
    return numpy.sqrt( dx**2 +dy**2 )
    
def znajdz_najblizszy( idx, tablica_wierzcholkow, odwiedzone ):
    q=len( tablica_wierzcholkow )
    najblizszy_koszt = 9999999
    najblizszy_idx  = -1
    for i in xrange( q ):
        if ( i != idx ) and ( odwiedzone[i] == 0 ) :
            koszt = oblicz_odleglosc(tablica_wierzcholkow[idx], tablica_wierzcholkow[i] )
            if koszt < najblizszy_koszt :
                najblizszy_idx = i
                najblizszy_koszt = koszt
    
    return [ najblizszy_idx, najblizszy_koszt ]

def najblizszy_sasiad( tablica_wierzcholkow ):
    q=len( tablica_wierzcholkow )
    odwiedzone = [0] * q
    cykl = []
    if losuj_wierzcholek_startowy:
        aktualny_wiercholek = int( q*numpy.random.rand() )
    else:
        aktualny_wiercholek = 0
    odwiedzone [aktualny_wiercholek ] = 1
    cykl.append(aktualny_wiercholek)
    print aktualny_wiercholek
    
    for i in xrange( q -1):
        [idx, koszt ] = znajdz_najblizszy( aktualny_wiercholek, tablica_wierzcholkow, odwiedzone )
        odwiedzone[idx] = 1
        cykl.append(idx)
        aktualny_wiercholek = idx
        print aktualny_wiercholek
        
    return cykl

def rysuj_cykl( tablica_wiercholkow, cykl ):
    q=len( tablica_wiercholkow )
    x=[]
    y=[]    
    
    for i in xrange( q ):
        x.append(tablica_wiercholkow[cykl[i],0] )
        y.append(tablica_wiercholkow[cykl[i],1] )
        
    x.append(tablica_wiercholkow[cykl[0],0] )
    y.append(tablica_wiercholkow[cykl[0],1] )
    
    plt.plot(x,y,'ro-')
    plt.show()
    print x
    print y
    
new = True
new = False    
if new:
    [v, j, k ] = generuj_drogi(5, 2)
    numpy.save( 'tmp',v)
else:
    v=numpy.load('tmp.npy')
print v

cykl = najblizszy_sasiad( v )
rysuj_cykl( v, cykl )

#print oblicz_odleglosc( (2,2), (5,2) )
        
