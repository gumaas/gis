# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 11:28:22 2017

@author: gumas
"""

import numpy
import matplotlib.pyplot as plt
import copy 
import sys

obszar=(1,1)
zakresjakosci=(1,1)
losuj_wierzcholek_startowy = False
losuj_nowy_graf = True
wspolczynnik_drogi_jednokierunkowej = 9999

glob_liczba_wierzcholkow = 100
glob_liczba_jednokierunkowych = 1000



if glob_liczba_jednokierunkowych >= (glob_liczba_wierzcholkow-1)* glob_liczba_wierzcholkow/2 :
    print "Zbyt duzo ulic jednokierunkowych"
    sys.exit()
  
def wprowadz_jednokierunkowe( odleglosci, jednokierunkowe ):

    for i in xrange( len(jednokierunkowe) ):
        odleglosci[jednokierunkowe[i][0],jednokierunkowe[i][1]] = odleglosci[jednokierunkowe[i][0],jednokierunkowe[i][1]]*wspolczynnik_drogi_jednokierunkowej
        
    return odleglosci        

def losuj_drogi_jednokierunkowe( liczba ):
    jednokierunkowe = [ numpy.random.random_integers(0,glob_liczba_wierzcholkow-1,2) ]
    while( len( jednokierunkowe ) < liczba ):
        new = numpy.random.random_integers(0,glob_liczba_wierzcholkow-1,2)
        if new[0] != new[1]:
            err = False
            for i in xrange(len(jednokierunkowe) ):
                if numpy.array_equal( numpy.sort(jednokierunkowe[i]), numpy.sort(new) ):
                    err = True                    
                    break
            if not err : 
                jednokierunkowe.append(new)

    return jednokierunkowe
    


def generuj_drogi( liczba_wierzcholkow, liczba_drog_jednokierunkowych ) :
    tablica_wiercholkow = obszar*numpy.random.rand(liczba_wierzcholkow,2)
    jakosc_drogi = ( zakresjakosci[1]-zakresjakosci[0])*numpy.random.rand(liczba_wierzcholkow,2)+zakresjakosci[0]
    drogi_jednokierunkowe = losuj_drogi_jednokierunkowe(glob_liczba_jednokierunkowych)
    
    return [ tablica_wiercholkow, jakosc_drogi, drogi_jednokierunkowe ]
    

def oblicz_odleglosc( v1, v2 ):
    dx = v2[0] - v1[0]
    dy = v2[1] - v1[1]
    return numpy.sqrt( dx**2 +dy**2 )

def oblicz_odleglosc2( v1, v2, odleglosci ):
    return odleglosci[v2,v1]

def oblicz_wszystkie_odleglosci( tablica_wierzcholkow ):
    odleglosci= numpy.zeros( (glob_liczba_wierzcholkow, glob_liczba_wierzcholkow ) ) 
    
    for i in xrange( len( tablica_wierzcholkow ) ):
        for j in xrange( len( tablica_wierzcholkow ) ) :
            odleglosci[ i, j ] = oblicz_odleglosc( tablica_wierzcholkow[i], tablica_wierzcholkow[j] )
    
    return odleglosci

def zmierz_cykl( cykl, odleglosci ):
    droga=0
    for i in xrange( 1, len(cykl) ):
        tmp = oblicz_odleglosc2(cykl[i],cykl[i-1], odleglosci )    
        droga += tmp
#        print tmp
        
    return droga
    

def znajdz_najblizszy( idx, tablica_wierzcholkow, odwiedzone, odleglosci ):
    q=len( tablica_wierzcholkow )
    najblizszy_koszt = 9999999
    najblizszy_idx  = -1
    for i in xrange( q ):
        if ( i != idx ) and ( odwiedzone[i] == 0 ) :
            koszt = oblicz_odleglosc2(idx, i, odleglosci )
            if koszt < najblizszy_koszt :
                najblizszy_idx = i
                najblizszy_koszt = koszt
    
    return [ najblizszy_idx, najblizszy_koszt ]

def najblizszy_sasiad( tablica_wierzcholkow, odleglosci ):
    q=len( tablica_wierzcholkow )
    odwiedzone = [0] * q
    cykl = []
    if losuj_wierzcholek_startowy:
        aktualny_wiercholek = int( q*numpy.random.rand() )
    else:
        aktualny_wiercholek = 0
    odwiedzone [aktualny_wiercholek ] = 1
    cykl.append(aktualny_wiercholek)
   
    for i in xrange( q -1):
        [idx, koszt ] = znajdz_najblizszy( aktualny_wiercholek, tablica_wierzcholkow, odwiedzone, odleglosci )
        odwiedzone[idx] = 1
        cykl.append(idx)
        aktualny_wiercholek = idx
        
    cykl.append(cykl[0])
    return cykl


def opt2_zamien( cykl, a, b ):
    poczatek = cykl[ :a]
    srodek = cykl[a:b]
    koniec = cykl[b:]
    srodek= srodek[::-1]
    return poczatek+srodek+koniec


def opt2( cykl_wejsciowy, odleglosci ):
    q=len( cykl_wejsciowy )

    cykl =  copy.copy( cykl_wejsciowy )
    dlugosc = 99999998
    poprzednia_dlugosc = 99999999
    cnt =0
    while( poprzednia_dlugosc > dlugosc ) :
        poprzednia_dlugosc = dlugosc        
        print "Próba %d, dlugosc %f" % ( cnt, dlugosc )
        cnt += 1

        for i in xrange( 1, q ):
            for j in xrange( i+1, q ):
                nowycykl = opt2_zamien( cykl, i, j )
                nowadlugosc = zmierz_cykl( nowycykl, odleglosci )
                if nowadlugosc < dlugosc :
                    dlugosc = nowadlugosc
                    cykl = nowycykl
        
    return [ cykl, dlugosc ]


def rysuj_cykl( tablica_wiercholkow, cykl ):
    q=len( tablica_wiercholkow )
    x=[]
    y=[]    
    
    for i in xrange( q ):
        x.append(tablica_wiercholkow[cykl[i],0] )
        y.append(tablica_wiercholkow[cykl[i],1] )
        
    
    plt.plot(x,y,'ro-')
    plt.show()

if losuj_nowy_graf:
    [v, j, k ] = generuj_drogi(glob_liczba_wierzcholkow, glob_liczba_jednokierunkowych)
    numpy.save( 'tmp',v)
else:
    v=numpy.load('tmp.npy')


def szukaj_pod_prad( jednokierunkowe, cykl ):
    pod_prad = []    
    cnt = 0
    for i in xrange( 1, len(cykl) ) :
        for j in xrange( len(jednokierunkowe ) ):
            if numpy.array_equal( numpy.array( cykl[i-1:i+1] ), numpy.array( jednokierunkowe[j] ) ):
                pod_prad.append( cykl[i-1:i+1 ] )
                cnt += 1
                
    return [ cnt, pod_prad ]




odleglosci = oblicz_wszystkie_odleglosci(v)
odleglosci = wprowadz_jednokierunkowe( odleglosci, k )


cykl = najblizszy_sasiad( v, odleglosci )
print "Długość cyklu: %.16f" % zmierz_cykl( cykl, odleglosci )
rysuj_cykl( v, cykl )
print cykl

[cykl2opt, dlugosc2opt] = opt2( cykl, odleglosci )
print "Długość cyklu: %.16f" % dlugosc2opt
rysuj_cykl( v, cykl2opt )
print cykl2opt

#print k
 
[ cnt, pod_prad ]  = szukaj_pod_prad( k, cykl )
[ cnt2, pod_prad2 ]  = szukaj_pod_prad( k, cykl2opt )
print "Liczba iść pod prąd:"
print "Zachlanny:%d" % cnt
print pod_prad
print "2opt:%d" % cnt2
print pod_prad2

print "\n\n\n"
#print k
#print odleglosci
#print cykl
#print zmierz_cykl( cykl, odleglosci )
#
#print cykl2opt
#print zmierz_cykl( cykl2opt, odleglosci )