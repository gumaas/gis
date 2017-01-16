# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 11:28:22 2017

@author: gumas
"""

import numpy
import matplotlib.pyplot as plt
import copy 
import sys
import itertools

import os
import fnmatch

obszar=(1,1)
zakresjakosci=(1,1)
losuj_wierzcholek_startowy = False
losuj_nowy_graf = True
wspolczynnik_drogi_jednokierunkowej = 9999

glob_liczba_wierzcholkow = 500
glob_liczba_jednokierunkowych = 5000
glob_sciezka_obrazkow = "../images/"



if glob_liczba_jednokierunkowych >= (glob_liczba_wierzcholkow-1)* glob_liczba_wierzcholkow/2 :
    print "Zbyt duzo ulic jednokierunkowych"
    sys.exit()
  
def wprowadz_jednokierunkowe( odleglosci, jednokierunkowe ):

    for i in xrange( len(jednokierunkowe) ):
        odleglosci[jednokierunkowe[i][0],jednokierunkowe[i][1]] = odleglosci[jednokierunkowe[i][0],jednokierunkowe[i][1]]*wspolczynnik_drogi_jednokierunkowej
        
    return odleglosci        


def losuj_drogi_jednokierunkowe( liczba ):
    jednokierunkowe = list(itertools.combinations(range(0,glob_liczba_wierzcholkow),2))

    kierunek = numpy.random.random_integers(0,1,len(jednokierunkowe) )
    
    for i in xrange( len(jednokierunkowe) ) :
        if jednokierunkowe[i][0] == jednokierunkowe[i][1]-1:
            jednokierunkowe[i] = ( jednokierunkowe[i][1], jednokierunkowe[i][0] ) 

        elif ( jednokierunkowe[i][0] == 0) and ( jednokierunkowe[i][1] == glob_liczba_wierzcholkow-1) :
            jednokierunkowe[i] = ( glob_liczba_wierzcholkow-1, 0 )
        else:
            if kierunek[i] == 1 :
                jednokierunkowe[i] = ( jednokierunkowe[i][1], jednokierunkowe[i][0] ) 
                
    numpy.random.shuffle(jednokierunkowe)
    return jednokierunkowe[:liczba]


def generuj_drogi( liczba_wierzcholkow, liczba_drog_jednokierunkowych ) :
    tablica_wiercholkow = obszar*numpy.random.rand(liczba_wierzcholkow,2)
    drogi_jednokierunkowe = losuj_drogi_jednokierunkowe(glob_liczba_jednokierunkowych)
    
    return [ tablica_wiercholkow, drogi_jednokierunkowe ]
    

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


def szukaj_pod_prad( jednokierunkowe, cykl ):
    pod_prad = []    
    cnt = 0
    for i in xrange( 1, len(cykl) ) :
        for j in xrange( len(jednokierunkowe ) ):
            if numpy.array_equal( numpy.array( cykl[i-1:i+1] ), numpy.array( jednokierunkowe[j] ) ):
                pod_prad.append( cykl[i-1:i+1 ] )
                cnt += 1
                
    return [ cnt, pod_prad ]


def generuj_dane_wejsciowe( liczba, zbior_liczb_wiercholkow, zbior_liczb_jednokier, katalog ):

    global glob_liczba_wierzcholkow
    global glob_liczba_jednokierunkowych
    idxw=-1
    for lw in zbior_liczb_wiercholkow:
        idxw += 1
        idxj =-1
        for lj in zbior_liczb_jednokier:
            idxj += 1
            for n in xrange( liczba ):
#                if ( n % 10 ) == 0 :
                print "Liczba wiercholkow: %d/%d, jednokierunkowe: %d/%d, zbior: %d/%d" % ( idxw, len( zbior_liczb_wiercholkow ), idxj, len(zbior_liczb_jednokier), n, liczba ) 
                glob_liczba_wierzcholkow = lw
                glob_liczba_jednokierunkowych = int(lw*(lw-1)*lj/2)
                [ v, j ] = generuj_drogi( glob_liczba_wierzcholkow, glob_liczba_jednokierunkowych )
                filename="w%04.d_j%04.d_n%04.d" % ( glob_liczba_wierzcholkow, glob_liczba_jednokierunkowych, n )
                if len(j) != glob_liczba_jednokierunkowych:
                    print "dlugosc wektora: %d, nazwapliku: %d" % ( len(j), glob_liczba_jednokierunkowych  )
                    sys.exit("Niezgodna liczba drog jednokierunkowych")
                numpy.save( katalog+filename, [v,j] )


def polacz_dane_wyjsciowe_wsp( d1, d2 ):
    new = {}
    for k in d1.keys():
        new[k] = dict( d1[k].items()+d2[k].items() )
    
    return new            

def parsename( name ):
    v = int( name.split('_')[0][1:] )
    j = int( name.split('_')[1][1:] )
    n = int( name.split('_')[2][1:] )
    return [v,j,n]
    
def testuj(dirname,wyjscie, pattern, wspolczynniki ):
    global glob_liczba_jednokierunkowych
    global glob_liczba_wierzcholkow
    global wspolczynnik_drogi_jednokierunkowej
    
    result = {}
    if not os.path.isdir(wyjscie):
        os.mkdir(wyjscie)
        
    for f in os.listdir(dirname):
        if fnmatch.fnmatch( f, pattern):
            print f
            [v,j] = numpy.load( dirname+'/'+f )
            [cw,cj,cn] = parsename(f.split('.')[0])
            if cw != len(v) :
                exit( "Niezgodnosc liczby wierzcholkow")

            if cj != len(j) :
                print "dlugosc wektora: %d, nazwapliku: %d" % ( cj, len(j) )
                sys.exit( "Niezgodnosc liczby drog jednokierunkowych")            
            
            glob_liczba_jednokierunkowych = cj
            glob_liczba_wierzcholkow= cw
            
            
            for w in wspolczynniki:
                print "%s wspolczynnik: %d" % (f, w)
                wspolczynnik_drogi_jednokierunkowej = w
                
                odleglosci = oblicz_wszystkie_odleglosci(v)
                odleglosci = wprowadz_jednokierunkowe( odleglosci, j )
                
                cykl_sasiad = najblizszy_sasiad( v, odleglosci )
                dlugosc_sasiad = zmierz_cykl( cykl_sasiad, odleglosci )
                
                [cykl_2opt, dlugosc_2opt] = opt2( cykl_sasiad, odleglosci )
    
                [ liczba_pod_prad_sasiad, pod_prad ]  = szukaj_pod_prad( j, cykl_sasiad )
                [ liczba_pod_prad_2opt, pod_prad2 ]  = szukaj_pod_prad( j, cykl_2opt )

                dlugosc_znany = zmierz_cykl( range(0,glob_liczba_wierzcholkow)+ [0], odleglosci )
                
                tmp = [ dlugosc_sasiad, liczba_pod_prad_sasiad, dlugosc_2opt, liczba_pod_prad_2opt, dlugosc_znany ]
                
                
                try:
                    result[cj][w].append( tmp )
                except:
                    try:
                        result[cj][w] = [ tmp ]
                    except:
                        result[cj] = {}
                        result[cj][w] = [ tmp ]
#                print "Długość cyklu: %.16f" % dlugosc_sasiad            
#                print "Długość cyklu: %.16f" % dlugosc_2opt
        
    filename="w%04.d_result" % ( glob_liczba_wierzcholkow )
    numpy.save( wyjscie + '/0' + filename, result )        
    return result



def test_generuj_dane( ):
    generuj_dane_wejsciowe( 50, [5], numpy.arange(0, 1.0 ,0.1 ), "../wejsciowe3/" )
    generuj_dane_wejsciowe( 50, [10], numpy.arange(0, 1.0 ,0.1 ), "../wejsciowe3/" )
    generuj_dane_wejsciowe( 50, [20], numpy.arange(0, 1.0 ,0.1 ), "../wejsciowe3/" )
    generuj_dane_wejsciowe( 50, [50], numpy.arange(0, 1.0 ,0.1 ), "../wejsciowe3/" )
    generuj_dane_wejsciowe( 50, [100], numpy.arange(0, 1.0 ,0.1 ), "../wejsciowe3/" )

def test_testuj():
    wsp = [ 1.5, 2, 5, 10, 100 ]
    testuj( "../wejsciowe3/", "../wyjsciowe3/", "w0005*", wsp )
    testuj( "../wejsciowe3/", "../wyjsciowe3/", "w0010*", wsp )
    testuj( "../wejsciowe3/", "../wyjsciowe3/", "w0020*", wsp )
    testuj( "../wejsciowe3/", "../wyjsciowe3/", "w0050*", wsp )
    testuj( "../wejsciowe3/", "../wyjsciowe3/", "w0100*", wsp )

def test_testuj_wiecej():
    wsp = [ 1000, 10000 ]
    testuj( "../wejsciowe3/", "../wyjsciowe4/", "w0005*", wsp )
    testuj( "../wejsciowe3/", "../wyjsciowe4/", "w0010*", wsp )
    testuj( "../wejsciowe3/", "../wyjsciowe4/", "w0020*", wsp )
    testuj( "../wejsciowe3/", "../wyjsciowe4/", "w0050*", wsp )
    testuj( "../wejsciowe3/", "../wyjsciowe4/", "w0100*", wsp )

def plot_zle_od_ljednokierunkowych( dane, wsp, kolor, dlugosc_cyklu, label ):
    res =[]
    for k in sorted( dane.keys() ):
        res.append( numpy.array( dane[k][wsp] ).mean(0)[3]/dlugosc_cyklu )
        
    plt.plot(numpy.arange(0, 1.0 ,0.1 )*100, numpy.multiply( res,100), kolor, label=label)

def plot_zlecykle_od_ljednokierunkowych( dane, wsp, kolor, dlugosc_cyklu, label ):
    res =[]
    for k in sorted( dane.keys() ):
        res.append( len(numpy.array( dane[k][wsp] )[:,3].nonzero()[0]) )
        
    plt.plot(numpy.arange(0, 1.0 ,0.1 )*100, numpy.divide( res,0.50), kolor, label=label)


def zaleznosc_od_liczby_drog():
    
    dat5 = polacz_dane_wyjsciowe_wsp(
            numpy.load('../wyjsciowe3/0w0005_result.npy').item(),
            numpy.load('../wyjsciowe4/0w0005_result.npy').item() )    
    dat10 = polacz_dane_wyjsciowe_wsp(
            numpy.load('../wyjsciowe3/0w0010_result.npy').item(),
            numpy.load('../wyjsciowe4/0w0010_result.npy').item() )    
    dat20 = polacz_dane_wyjsciowe_wsp(
            numpy.load('../wyjsciowe3/0w0020_result.npy').item(),
            numpy.load('../wyjsciowe4/0w0020_result.npy').item() )    
    dat50 = polacz_dane_wyjsciowe_wsp(
            numpy.load('../wyjsciowe3/0w0050_result.npy').item(),
            numpy.load('../wyjsciowe4/0w0050_result.npy').item() )    
    dat100 = polacz_dane_wyjsciowe_wsp(
            numpy.load('../wyjsciowe3/0w0100_result.npy').item(),
            numpy.load('../wyjsciowe4/0w0100_result.npy').item() )    
    
    for wsp in [ 2, 10, 100, 10000 ]:
        plot_zle_od_ljednokierunkowych( dat5, wsp, 'r-', 6, "n=5" )
        plot_zle_od_ljednokierunkowych( dat10, wsp, 'g-', 11, "n=10" )    
        plot_zle_od_ljednokierunkowych( dat20, wsp, 'b-', 21, "n=20" )
        plot_zle_od_ljednokierunkowych( dat50, wsp, 'm-', 51, "n=50" )
        plot_zle_od_ljednokierunkowych( dat100, wsp, 'y-', 101, "n=100"  )
        plt.legend( loc=2)
        plt.title("Wspolczynnik drogi jednokierunkowej = %.1f" % wsp)
        plt.xlabel( "Odsetek liczby drog jednokierunkowych w grafie [%]")
        plt.ylabel( "Odsetek liczby odcinkow pokonanych pod prad [%]")
        plt.savefig(glob_sciezka_obrazkow+"zleodc_njedn_w%d.pdf" % wsp )    
        plt.show()
        
    for wsp in [ 2, 10, 100, 10000 ]:
        plot_zlecykle_od_ljednokierunkowych( dat5, wsp, 'r-', 6, "n=5" )
        plot_zlecykle_od_ljednokierunkowych( dat10, wsp, 'g-', 11, "n=10" )    
        plot_zlecykle_od_ljednokierunkowych( dat20, wsp, 'b-', 21, "n=20" )
        plot_zlecykle_od_ljednokierunkowych( dat50, wsp, 'm-', 51, "n=50" )
        plot_zlecykle_od_ljednokierunkowych( dat100, wsp, 'y-', 101, "n=100"  )
        plt.legend( loc=2)
        plt.title("Wspolczynnik drogi jednokierunkowej = %.1f" % wsp)
        plt.xlabel( "Odsetek liczby drog jednokierunkowych w grafie [%]")
        plt.ylabel( "Odsetek liczby cykli zawierajacych odcinek pod prad [%]")
        plt.savefig(glob_sciezka_obrazkow+"zlecykl_njedn_w%d.pdf" % wsp )    
        plt.show()


def plot_zle_od_wspolczynnika( dane, jednokierprop, kolor, dlugosc_cyklu, label ):
    res =[]
    x = []
    ljednokier=numpy.sort( dane.keys() )[ jednokierprop ]
    for k in sorted( dane[ljednokier].keys() ):
        res.append( numpy.array( dane[ljednokier][k] ).mean(0)[3]/dlugosc_cyklu )
        x.append(k)
        
    plt.semilogx(x, numpy.multiply(res,100), kolor, label=label)


def plot_zlecykle_od_wsp( dane, jednokierprop, kolor, dlugosc_cyklu, label ):
    res =[]
    x=[]
    ljednokier=numpy.sort( dane.keys() )[ jednokierprop ]

    for k in sorted( dane[ljednokier].keys() ):
       res.append( len(numpy.array( dane[ljednokier][k] )[:,3].nonzero()[0] ) )
       x.append(k)

    plt.semilogx(x, numpy.multiply(res,2), kolor, label=label)


def zaleznosc_od_wspolczynnika():
    
    dat5 = polacz_dane_wyjsciowe_wsp(
            numpy.load('../wyjsciowe3/0w0005_result.npy').item(),
            numpy.load('../wyjsciowe4/0w0005_result.npy').item() )    
    dat10 = polacz_dane_wyjsciowe_wsp(
            numpy.load('../wyjsciowe3/0w0010_result.npy').item(),
            numpy.load('../wyjsciowe4/0w0010_result.npy').item() )    
    dat20 = polacz_dane_wyjsciowe_wsp(
            numpy.load('../wyjsciowe3/0w0020_result.npy').item(),
            numpy.load('../wyjsciowe4/0w0020_result.npy').item() )    
    dat50 = polacz_dane_wyjsciowe_wsp(
            numpy.load('../wyjsciowe3/0w0050_result.npy').item(),
            numpy.load('../wyjsciowe4/0w0050_result.npy').item() )    
    dat100 = polacz_dane_wyjsciowe_wsp(
            numpy.load('../wyjsciowe3/0w0100_result.npy').item(),
            numpy.load('../wyjsciowe4/0w0100_result.npy').item() )    
#    dat100=numpy.load('../wyjsciowe3/0w0100_result.npy').item()
    
    for jednokier_idx in [ 2, 5, 8 ]:
        plot_zle_od_wspolczynnika( dat5, jednokier_idx, 'rx-', 6, "n=5" )
        plot_zle_od_wspolczynnika( dat10, jednokier_idx, 'gx-', 11, "n=10" )    
        plot_zle_od_wspolczynnika( dat20, jednokier_idx, 'bx-', 21, "n=20" )
        plot_zle_od_wspolczynnika( dat50, jednokier_idx, 'mx-', 51, "n=50" )
        plot_zle_od_wspolczynnika( dat100, jednokier_idx, 'yx-', 101, "n=100" )
        plt.legend( loc=1)
        plt.xlabel( "Wspolczynnik kosztu drogi jednokierunkowej")
        plt.ylabel( "Odsetek liczby odcinkow pokonanych pod prad [%]")
        plt.title( "Odsetek drog jednokierunkowych = %d%%" % numpy.multiply(jednokier_idx,10) )
        plt.savefig(glob_sciezka_obrazkow+"zleodc_wsp_j%d.pdf"% jednokier_idx)    
        plt.show()
    
    for jednokier_idx in [ 2, 5 ]:
        plot_zlecykle_od_wsp( dat5, jednokier_idx, 'rx-', 6, "n=5" )
        plot_zlecykle_od_wsp( dat10, jednokier_idx, 'gx-', 11, "n=10" )    
        plot_zlecykle_od_wsp( dat20, jednokier_idx, 'bx-', 21, "n=20" )
        plot_zlecykle_od_wsp( dat50, jednokier_idx, 'mx-', 51, "n=50" )
        plot_zlecykle_od_wsp( dat100, jednokier_idx, 'yx-', 101, "n=100" )
        plt.legend( loc=1)
        plt.xlabel( "Wspolczynnik kosztu drogi jednokierunkowej")
        plt.ylabel( "Odsetek cykli zawierajacych niedozwolone drogi [%]")
        plt.title( "Odsetek drog jednokierunkowych = %d%%" % numpy.multiply(jednokier_idx,10) )
        plt.savefig(glob_sciezka_obrazkow+"zlecykle_wsp_j%d.pdf"% jednokier_idx)    
        plt.show()

def plot_rozrzut_od_ljednokierunkowych( dane, wsp, kolor, dlugosc_cyklu, label ):
    res =[]
    for k in sorted( dane.keys() ):
        res.append( numpy.array( dane[k][wsp] ).std(0)[3] )
        
    plt.plot(numpy.arange(0, 1.0 ,0.1 )*100, res, kolor, label=label)

def rozrzut_od_liczby_drog():
    
    dat5 = polacz_dane_wyjsciowe_wsp(
            numpy.load('../wyjsciowe3/0w0005_result.npy').item(),
            numpy.load('../wyjsciowe4/0w0005_result.npy').item() )    
    dat10 = polacz_dane_wyjsciowe_wsp(
            numpy.load('../wyjsciowe3/0w0010_result.npy').item(),
            numpy.load('../wyjsciowe4/0w0010_result.npy').item() )    
    dat20 = polacz_dane_wyjsciowe_wsp(
            numpy.load('../wyjsciowe3/0w0020_result.npy').item(),
            numpy.load('../wyjsciowe4/0w0020_result.npy').item() )    
    dat50 = polacz_dane_wyjsciowe_wsp(
            numpy.load('../wyjsciowe3/0w0050_result.npy').item(),
            numpy.load('../wyjsciowe4/0w0050_result.npy').item() )    
    dat100 = polacz_dane_wyjsciowe_wsp(
            numpy.load('../wyjsciowe3/0w0100_result.npy').item(),
            numpy.load('../wyjsciowe4/0w0100_result.npy').item() )    
#    dat100=numpy.load('../wyjsciowe3/0w0100_result.npy').item()
    
    wsp = 100
    plot_rozrzut_od_ljednokierunkowych( dat5, wsp, 'r-', 6, "n=5" )
    plot_rozrzut_od_ljednokierunkowych( dat10, wsp, 'g-', 11, "n=10" )    
    plot_rozrzut_od_ljednokierunkowych( dat20, wsp, 'b-', 21, "n=20" )
    plot_rozrzut_od_ljednokierunkowych( dat50, wsp, 'm-', 51, "n=50" )
    plot_rozrzut_od_ljednokierunkowych( dat100, wsp, 'y-', 101, "n=100"  )
    plt.legend( loc=2)
    plt.xlabel( "Odsetek liczby drog jednokierunkowych w grafie [%]")
    plt.ylabel( "Odchylenie standardowe odsetka cykli niedozwolonych [%]")
    
    plt.savefig(glob_sciezka_obrazkow+"rozrzut_njedn.pdf")    
    plt.show()


def plot_rozrzut_od_wspolczynnika( dane, jednokierprop, kolor, dlugosc_cyklu, label ):
    res =[]
    x = []
    ljednokier=numpy.sort( dane.keys() )[ jednokierprop ]
    for k in sorted( dane[ljednokier].keys() ):
        res.append( numpy.array( dane[ljednokier][k] ).std(0)[3] )
        x.append(k)
        
    plt.semilogx(x, res, kolor, label=label)

def rozrzut_od_wspolczynnika():
    
    dat5 = polacz_dane_wyjsciowe_wsp(
            numpy.load('../wyjsciowe3/0w0005_result.npy').item(),
            numpy.load('../wyjsciowe4/0w0005_result.npy').item() )    
    dat10 = polacz_dane_wyjsciowe_wsp(
            numpy.load('../wyjsciowe3/0w0010_result.npy').item(),
            numpy.load('../wyjsciowe4/0w0010_result.npy').item() )    
    dat20 = polacz_dane_wyjsciowe_wsp(
            numpy.load('../wyjsciowe3/0w0020_result.npy').item(),
            numpy.load('../wyjsciowe4/0w0020_result.npy').item() )    
    dat50 = polacz_dane_wyjsciowe_wsp(
            numpy.load('../wyjsciowe3/0w0050_result.npy').item(),
            numpy.load('../wyjsciowe4/0w0050_result.npy').item() )    
    dat100 = polacz_dane_wyjsciowe_wsp(
            numpy.load('../wyjsciowe3/0w0100_result.npy').item(),
            numpy.load('../wyjsciowe4/0w0100_result.npy').item() )    
#    dat100=numpy.load('../wyjsciowe3/0w0100_result.npy').item()
    
    jednokier_idx = 5 
    plot_rozrzut_od_wspolczynnika( dat5, jednokier_idx, 'rx-', 6, "n=5" )
    plot_rozrzut_od_wspolczynnika( dat10, jednokier_idx, 'gx-', 11, "n=10" )    
    plot_rozrzut_od_wspolczynnika( dat20, jednokier_idx, 'bx-', 21, "n=20" )
    plot_rozrzut_od_wspolczynnika( dat50, jednokier_idx, 'mx-', 51, "n=50" )
    plot_rozrzut_od_wspolczynnika( dat100, jednokier_idx, 'yx-', 101, "n=100" )    
    plt.legend( loc=1)
    plt.title( "Odsetek drog jednokierunkowych d = %d%%" % numpy.multiply(jednokier_idx,10) )
    plt.xlabel( "Wspolczynnik kosztu drogi jednokierunkowej")
    plt.ylabel( "Odchylenie standardowe odsetka cykli niedozwolonych [%]")
    
    plt.savefig(glob_sciezka_obrazkow+"zleodc_wsp.pdf")    
    plt.show()


def liczba_krotszych_pod_prad( dane ):
    
#    4 - dlugosc znanej legalnej drogi 
#    2 - dlugosc drogi znalezionej przez 2opt
#    jak roznica dodatnia, to znaleziona droga krotsza niz referencyjna
#    jak roznica ujemna to znaleziona jest dluzsza niz referencyjna
    danearr=numpy.asarray( dane )    
    roznice = danearr[:,4] - danearr[:,2]
    krotsza_pod_prad = 0
    wszystkie = 0.
    for i in xrange( len(roznice ) ):
#        jezeli bylo pod prad
        if dane[i][3 ] >0 :
            wszystkie += 1
            if roznice[i] > 0 :
                krotsza_pod_prad += 1
    if wszystkie == 0:
        return 1
    else:
        return numpy.divide( krotsza_pod_prad,wszystkie)
    
def plot_krotsze_pod_prad_wsp( dane, jednokierprop, kolor, dlugosc_cyklu, label ):
    res =[]
    x = []
    ljednokier=numpy.sort( dane.keys() )[ jednokierprop ]
    for k in sorted( dane[ljednokier].keys() ):
        res.append( liczba_krotszych_pod_prad( dane[ljednokier][k] ) )
        x.append(k)
        
    plt.semilogx(x, numpy.multiply( res, 100), kolor, label=label)

def krotsze_pod_prad_od_wsp():
    
      
    dat5 = polacz_dane_wyjsciowe_wsp(
            numpy.load('../wyjsciowe3/0w0005_result.npy').item(),
            numpy.load('../wyjsciowe4/0w0005_result.npy').item() )    
    dat10 = polacz_dane_wyjsciowe_wsp(
            numpy.load('../wyjsciowe3/0w0010_result.npy').item(),
            numpy.load('../wyjsciowe4/0w0010_result.npy').item() )    
    dat20 = polacz_dane_wyjsciowe_wsp(
            numpy.load('../wyjsciowe3/0w0020_result.npy').item(),
            numpy.load('../wyjsciowe4/0w0020_result.npy').item() )    
    dat50 = polacz_dane_wyjsciowe_wsp(
            numpy.load('../wyjsciowe3/0w0050_result.npy').item(),
            numpy.load('../wyjsciowe4/0w0050_result.npy').item() )    
    dat100 = polacz_dane_wyjsciowe_wsp(
            numpy.load('../wyjsciowe3/0w0100_result.npy').item(),
            numpy.load('../wyjsciowe4/0w0100_result.npy').item() )    
#    dat100=numpy.load('../wyjsciowe3/0w0100_result.npy').item()
    
    jednokier_idx =  3
    plot_krotsze_pod_prad_wsp( dat5, jednokier_idx, 'rx-', 6, "n=5" )
    plot_krotsze_pod_prad_wsp( dat10, jednokier_idx, 'gx-', 11, "n=10" )    
    plot_krotsze_pod_prad_wsp( dat20, jednokier_idx, 'bx-', 21, "n=20" )
    plot_krotsze_pod_prad_wsp( dat50, jednokier_idx, 'mx-', 51, "n=50" )
    plot_krotsze_pod_prad_wsp( dat100, jednokier_idx, 'yx-', 101, "n=100" )    
    plt.legend( loc=2)
    plt.title( "Odsetek drog jednokierunkowych d = %d%%" % numpy.multiply(jednokier_idx,10) )

    plt.xlabel( "Wspolczynnik kosztu drogi jednokierunkowej")
    plt.ylabel( "Odsetek niedozwolonych cykli krotszych niz referencyjny [%]")
    plt.ylim((-10,110))    
    
    plt.savefig(glob_sciezka_obrazkow+"krotsze_wsp.pdf")    
    plt.show()


def plot_krotsze_pod_prad_od_ljednokierunkowych( dane, wsp, kolor, dlugosc_cyklu, label ):
    res =[]
    for k in sorted( dane.keys() ):
        res.append( liczba_krotszych_pod_prad( dane[k][wsp] ) )
        
    plt.plot(numpy.arange(0, 1.0 ,0.1 )*100, numpy.multiply( res,100), kolor, label=label)

def krotsze_pod_prad_od_liczby_drog():
    
    dat5 = polacz_dane_wyjsciowe_wsp(
            numpy.load('../wyjsciowe3/0w0005_result.npy').item(),
            numpy.load('../wyjsciowe4/0w0005_result.npy').item() )    
    dat10 = polacz_dane_wyjsciowe_wsp(
            numpy.load('../wyjsciowe3/0w0010_result.npy').item(),
            numpy.load('../wyjsciowe4/0w0010_result.npy').item() )    
    dat20 = polacz_dane_wyjsciowe_wsp(
            numpy.load('../wyjsciowe3/0w0020_result.npy').item(),
            numpy.load('../wyjsciowe4/0w0020_result.npy').item() )    
    dat50 = polacz_dane_wyjsciowe_wsp(
            numpy.load('../wyjsciowe3/0w0050_result.npy').item(),
            numpy.load('../wyjsciowe4/0w0050_result.npy').item() )    
    dat100 = polacz_dane_wyjsciowe_wsp(
            numpy.load('../wyjsciowe3/0w0100_result.npy').item(),
            numpy.load('../wyjsciowe4/0w0100_result.npy').item() )    
#    dat100=numpy.load('../wyjsciowe3/0w0100_result.npy').item()
    
    wsp = 10000
    plot_krotsze_pod_prad_od_ljednokierunkowych( dat5, wsp, 'r-', 6, "n=5" )
    plot_krotsze_pod_prad_od_ljednokierunkowych( dat10, wsp, 'g-', 11, "n=10" )    
    plot_krotsze_pod_prad_od_ljednokierunkowych( dat20, wsp, 'b-', 21, "n=20" )
    plot_krotsze_pod_prad_od_ljednokierunkowych( dat50, wsp, 'm-', 51, "n=50" )
#    plot_krotsze_pod_prad_od_ljednokierunkowych( dat100, wsp, 'y-', 101, "n=100"  )
    plt.legend( loc=2)
    plt.title( "Wspolczynnik drogi jednokierunkowej %d" % wsp )

    plt.xlabel( "Odsetek liczby drog jednokierunkowych w grafie [%]")
    plt.ylabel( "Odsetek niedozwolonych cykli krotszych niz referencyjny [%]")
    plt.ylim((-10,110))    
    
    plt.savefig(glob_sciezka_obrazkow+"krotsze_jednokier.pdf")    
    plt.show()

def rysuj_wykresy():

    global glob_sciezka_obrazkow
    glob_sciezka_obrazkow="../images/"
    
    if not os.path.isdir( glob_sciezka_obrazkow ):
        os.mkdir(glob_sciezka_obrazkow)
            
    zaleznosc_od_liczby_drog()
    zaleznosc_od_wspolczynnika()
    rozrzut_od_liczby_drog()
    rozrzut_od_wspolczynnika()
    
    krotsze_pod_prad_od_wsp( )
    krotsze_pod_prad_od_liczby_drog()
    

dat5 = polacz_dane_wyjsciowe_wsp(
            numpy.load('../wyjsciowe3/0w0005_result.npy').item(),
            numpy.load('../wyjsciowe4/0w0005_result.npy').item() )

    
if __name__ == "__main__":
    rysuj_wykresy()
    
#glob_liczba_wierzcholkow = 1000
#losuj_drogi_jednokierunkowe( 5000 )


#
#if losuj_nowy_graf:
#    [v, k ] = generuj_drogi(glob_liczba_wierzcholkow, glob_liczba_jednokierunkowych)
#    numpy.save( 'tmp',v)
#else:
#    v=numpy.load('tmp.npy')
#
#
#odleglosci = oblicz_wszystkie_odleglosci(v)
#odleglosci = wprowadz_jednokierunkowe( odleglosci, k )
#
#
#cykl = najblizszy_sasiad( v, odleglosci )
#print "Długość cyklu: %.16f" % zmierz_cykl( cykl, odleglosci )
#rysuj_cykl( v, cykl )
#print cykl
#
#[cykl2opt, dlugosc2opt] = opt2( cykl, odleglosci )
#print "Długość cyklu: %.16f" % dlugosc2opt
#rysuj_cykl( v, cykl2opt )
#print cykl2opt
#
##print k
# 
#[ cnt, pod_prad ]  = szukaj_pod_prad( k, cykl )
#[ cnt2, pod_prad2 ]  = szukaj_pod_prad( k, cykl2opt )
#print "Liczba iść pod prąd:"
#print "Zachlanny:%d" % cnt
#print pod_prad
#print "2opt:%d" % cnt2
#print pod_prad2
#
#print "\n\n\n"
##print k
##print odleglosci
##print cykl
##print zmierz_cykl( cykl, odleglosci )
##
##print cykl2opt
##print zmierz_cykl( cykl2opt, odleglosci )