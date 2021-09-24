import matplotlib.pyplot as plt
from numpy import linspace,round
from sympy import symbols,diff,lambdify

def parcijalni_izvod(funkcija,varijabla,tacka,n=1,red_varijabli=[]):
    '''
    Argumenti
    ----------
    funkcija : funkcija/izraz ciji izvod racunamo simbolicki i/ili numericki
    varijabla : varijabla po kojoj simbolicki racunamo izvod
    tacka : koordinate tacke u kojoj numericki racunamo izvod (float ili tuple)
    n : redni broj izvoda, ako ovaj parametar nije specificiran onda je n=1 (int)
    red_varijabli : redoslijed varijabli, vazno za racunanje izvoda u tacki
                    ako nije specificirano, varijable se sortiraju abecedno (lista stringova)
    Povratne vrijednosti
    -------
    izvod : simbolicki oblik n-tog izvoda funkcije 
    vrijednost : vrijednost izvoda funkcije u tacki (float)
                ako broj nezavisnih varijabli i koordinata tacke nije isti
                funkcija umjesto vrijednosti vraca None
    '''
    izvod = diff(funkcija,varijabla,n)
    
    point = [tacka]
    
    try:
        br_koordinata = len(point[0])
    except TypeError:
        br_koordinata = 1

    varijable = sortiraj_varijable(list(funkcija.free_symbols),red_varijabli)

    if len(funkcija.free_symbols)!=br_koordinata:
        print("greska u parcijalni_izvod: Broj nezavisnih varijabli i koordinata mora biti isti!")
        print("Funkcija ima sljedeci broj nezavisnih varijabli:",len(funkcija.free_symbols))
        print("Proslijedjena tacka ima sljedeci broj koordinata:",br_koordinata)
        return izvod, None
    
    lambda_fun = lambdify([tuple(varijable)],izvod,"math")
    try:
        vrijednost = lambda_fun(tacka)
    except TypeError:
        vrijednost = float(izvod.subs(varijable[0],tacka))
    return izvod,vrijednost

def sortiraj_varijable(varijable,var_string=[]):
    '''
    Argumenti
    ----------
    varijable : lista simbolickih varijabli iz funkcije
    var_string : lista stringova po kojima se sortiraju simbolicke varijable
                ako nije specificirano, varijable se sortiraju abecedno
                odnosno prema ASCII vrijednostima
    Ako su proslijedjena oba argumenta, oni moraju biti uskladjeni.
            
    Povratne vrijednosti
    -------
    sortirane : lista simbolickih varijabli sortirane prema ASCII vrijednostima
                ili kako je specificirano argumentom var_string
    '''

    if len(var_string):
        if len(var_string)!=len(varijable):
            raise ValueError("Lista simbolickih varijabli i lista stringova simbolickih varijabli nisu iste duzine.")
        
        var = []
        var_str = var_string.copy()
        for i in range(len(varijable)):
            var.append(str(varijable[i]))
        
        var.sort()
        var_str.sort()
        
        if var_str!=var:
            raise ValueError("Lista simbolickih varijabli i lista stringova simbolickih varijabli nemaju iste elemente.")
        
    else:
        var_string = varijable.copy()
        #pretvori u string radi poredjenja
        for i in range(len(var_string)):
            var_string[i] = str(varijable[i])
        var_string.sort() # sortiranje liste stringova        
    
    
    sortirane = []    
    #sortiranje simbolickih varijabli
    #na osnovu sortirane liste stringova
    for i in range(len(var_string)):
        for j in range(len(varijable)):
            if str(varijable[j])==var_string[i]:
                sortirane.append(varijable[j])
                break
            
    return sortirane

def ispis_kraj(tacka,vrijednost,br_iter,tacke_pretrazivanja,nadjeno_rjesenje,preciznost):
    '''
    Argumenti
    ----------
    tacka : float ili tuple - tacka trenutnog/krajnjeg rjesenja
    vrijednost : float - vrijednost kriterija u trenutnom rjesenju
    br_iter : int - trenutno dostignuti broj iteracija
    tacke_pretrazivanja : float ili tuple lista tacaka u kojima se vrsilo pretrazivanje
    nadjeno_rjesenje : string koji moze imati vrijednosti DA ili NE
                    u zavisnosti od toga da li je algoritam dostigao rješenje
    preciznost : proslijedjuje se kao argument radi prilagodjenog ispisa rezultata

    Funkcija ne vraća ništa
    ---------
    '''

    br_dec = 0
    if preciznost<1:
        while True:
            if int(preciznost)>0:
                break
            else:
                preciznost = preciznost*10
                br_dec = br_dec + 1
                
    br_dec = br_dec+2
    print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
    print("Rjesenje pronadjeno:",nadjeno_rjesenje)
    print("Broj iteracija:",br_iter)
    print("Tacke u kojima se vrsilo pretrazivanje:",round(tacke_pretrazivanja,br_dec))
    print("Tacka (trenutnog) rjesenja:",round(tacka,br_dec))
    print("Vrijednost funkcije u tacki:",round(vrijednost,br_dec))

def Southwell_search(funkcija,pocetna_tacka,max_iter=1e3,preciznost=1e-6,crtanje=0,red_varijabli=[],ispis=0):
    '''
    Southwell_search trazi optimum proslijedjene funkcije.
    Argumenti
    ----------
    funkcija : simbolicka funkcija ciji ekstrem trazimo
    pocetna_tacka : pocetna tacka za pretrazivanje ekstrema (float ili tuple)
    max_iter : maksimalni broj iteracija (int)
                ako nije specificirano, maksimalni broj je 1000
    preciznost : algoritam se zaustavlja kada je maksimalna vrijednost izvoda
                po svim varijablama manja od ove vrijednosti
                ako nije specificirano, preciznost iznosi 1 mikron (float)
    red_varijabli : lista stringova naziva varijabli
                    redoslijed bitan zbog izracunavanja vrijednosti u tacki
    ispis : ako je ovaj parametar razlicit od nule, ispisuju se koraci algoritma
            ako je ovaj parametar jednak nuli ili nije specificiran, koraci se ne ispisuju (bool)

    Povratne vrijednosti
    -------
    x_ex : tacka ekstremuma (float)
    fx_ex : vrijednost funkcije u tacki ekstremuma (float)
    k : broj iteracija koji je bio potreban za dostizanje rjesenja (int)
    '''
    if ispis:
        print("Southwell pretrazivanje:")
        
    x_ex = pocetna_tacka
    varijable = sortiraj_varijable(list(funkcija.free_symbols),red_varijabli)
    
    if ispis:
        print("Funkcija:",funkcija)
        print("Varijable",varijable)
    
    tacke_pretrazivanja = []
    
    for k in range(1,int(max_iter)):
        tacke_pretrazivanja.append(x_ex)
        
        if ispis:
            print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
            print("Iteracija br:",k)
            
        izvodi_x = []
        
        for i in range(len(varijable)):
            der,vrijednost = parcijalni_izvod(funkcija, varijable[i], x_ex,1,red_varijabli)
            
            if ispis:
                print("Parcijalni izvod funkcije po varijabli",varijable[i],"iznosi",der)
                print("U tacki",x_ex,"iznosi",vrijednost)
            try:
                izvodi_x.append(abs(vrijednost))
            except TypeError:
                print("greska u Southwell_search: Pocetna tacka nema odgovarajuci broj koordinata.")
                return None,None,None,None
        
        if ispis:
            print("Vrijednosti izvoda funkcije po svim varijablama",varijable,"u tacki iznosi",izvodi_x)
        
        if max(izvodi_x)<preciznost:
            lambda_fun = lambdify([tuple(varijable)],funkcija,"math")
            try:
                fx_ex = lambda_fun(x_ex)
            except TypeError:
                fx_ex = float(funkcija.subs(varijable[0],x_ex))
            
            ispis_kraj(x_ex, fx_ex, k, tacke_pretrazivanja, 'DA', preciznost)
            
            if crtanje:
                crtanje_funkcije(funkcija, varijable, x_ex, fx_ex, tacke_pretrazivanja)
            
            return x_ex,fx_ex,tacke_pretrazivanja,k
        
        imax_izvod = izvodi_x.index(max(izvodi_x))
        
        if ispis:
            print("Za varijablu po kojoj se vrsi jednodimenzionalno pretrazivanje bira se:",varijable[imax_izvod])
        
        der1,g1 = parcijalni_izvod(funkcija, varijable[imax_izvod], x_ex, 1, red_varijabli)
        der2,g2 = parcijalni_izvod(funkcija, varijable[imax_izvod], x_ex, 2, red_varijabli)
        
        if ispis:
            print("Izvod funkcije po varijabli",varijable[imax_izvod],"iznosi",der1)
            print("Vrijednost izvoda iznosi:",g1)
            print("Drugi izvod funkcije po varijabli",varijable[imax_izvod],"iznosi",der2)
            print("Vrijednost drugog izvoda iznosi:",g2)
        
        alfa = 1
        
        try:
            g = g1/g2
        except ZeroDivisionError:
            g2 = 1e-3
        
        
        if ispis:
            print("Stara vrijednost rjesenja:",varijable,"=",x_ex)
        
        try:
            ex_list = list(x_ex)
            ex_list[imax_izvod] = ex_list[imax_izvod] - alfa * g1/g2
            x_ex = tuple(ex_list)
        except TypeError:
            x_ex = x_ex - alfa * g1/g2
        
        if ispis:
            print("Nova vrijednost rjesenja:",varijable,"=",x_ex)
        
    lambda_fun = lambdify([tuple(varijable)],funkcija,"math")
    
    try:
        fx_ex = lambda_fun(x_ex)
    except TypeError:
        fx_ex = float(funkcija.subs(varijable[0],x_ex))
                      
    ispis_kraj(x_ex, fx_ex, k, tacke_pretrazivanja, 'NE', preciznost)
    return None,None,None,None


def skaliranje_opsega(potencijalnaRjesenja,lijeva,desna):
    '''
    Argumenti
    ----------
    potencijalnaRjesenja : float lista - potencijalnih rjesenja po odgovarajucoj varijabli
    lijeva : lijeva granica opsega u kojem se crta funkcija (float)
    desna : desna granica opsega u kojem se crta funkcija (float)

    Ukoliko se neko od potencijalnih rjesenja nalazi izvan opsega u kojem se crta funkcija
        opseg se prosiruje tako da se prikazu sve tacke pretrazivanja

    Povratne vrijednosti
    -------
    lijeva : (modifikovana) lijeva granica za crtanje funkcije
    desna : (modifikovana) desna granica za crtanje funkcije
    '''

    if len(potencijalnaRjesenja):
        
        if max(potencijalnaRjesenja)>desna:
            desna=max(potencijalnaRjesenja)
            
        if min(potencijalnaRjesenja)<lijeva:
            lijeva=min(potencijalnaRjesenja)    

    return lijeva,desna

def crtanje_funkcije(funkcija,varijable,tacka,ekstrem,potencijalnaRjesenja=[],granica=5,brojTacaka=500):
    '''
    Argumenti
    ----------
    funkcija : simbolicka funkcija jedne ili dvije promjenljive koju zelimo iscrtati
    varijable : sortirana lista varijabli koje se nalaze u proslijedjenoj funkciji
    tacka : tacka(float) ili uredjeni par u kojoj se nalazi ekstrem 
    ekstrem : vrijednost funkcije u tacki ekstrema (float)
    potencijalnaRjesenja : lista tacaka/uredjenih parova potencijalnih rjesenja
    granica : odredjuje opseg za koji se crtaju funkcije (float)
                ako nije specificirano, vrijednost ovog argumenta iznosi 5
    brojTacaka : broj tacaka u opsegu u kojem se crta funkcija
                ako nije specificirano, vrijednost ovog argumenta iznosi 500

    Povratne vrijednosti
    ------
    0 - crtanje neuspjesno
    1 - crtanje uspjesno

        '''
    
    if len(varijable)<0 or len(varijable)>2:
        print("upozorenje u crtanje_funkcije: Moguce je crtati samo funkcije jedne ili dvije promjenljive.")
        return 0
    
    fun = []

    if len(varijable)==1:
        try:
            lijeva = tacka-granica
            desna = tacka+granica
        except TypeError:
            print("greska u crtanje_funkcije: Proslijedjena tacka nema odgovarajuci broj koordinata.")
            return 0
        
        if len(potencijalnaRjesenja):
            lijeva,desna = skaliranje_opsega(potencijalnaRjesenja, lijeva, desna)
        
        ap = linspace(lijeva,desna,brojTacaka) 
        
        for i in range(len(ap)):
            fun.append(float(funkcija.subs(varijable[0],ap[i])))
              
        plt.figure(1)
        plt.plot(ap,fun,'c')
        plt.plot(tacka,ekstrem,'ro')
        plt.grid(True)
  
        if len(potencijalnaRjesenja):
            for i in range(len(potencijalnaRjesenja)-1):
                plt.plot(potencijalnaRjesenja[i],float(funkcija.subs(varijable[0],potencijalnaRjesenja[i])),'kx')
        return 1
        
    if len(varijable)==2:
        lamb_fun = lambdify([tuple(varijable)],funkcija,"math")

        try:
            lijeva = tacka[0]-granica
            desna = tacka[0]+granica
        except TypeError:
            print("greska u crtanje_funkcije: Proslijedjena tacka nema odgovarajuci broj koordinata.")
            return 0   
        
        if len(potencijalnaRjesenja):
            pretr_aps = []
            pretr_ord = []
            for i in range(len(potencijalnaRjesenja)):
                pretr_aps.append(potencijalnaRjesenja[i][0])
                pretr_ord.append(potencijalnaRjesenja[i][1])
                
        
        if len(pretr_aps):
            lijeva,desna = skaliranje_opsega(pretr_aps, lijeva, desna)      
        
        
        ap = linspace(lijeva,desna,brojTacaka)

        lijeva = tacka[1]-granica
        desna = tacka[1]+granica
        
        if len(pretr_ord):
            lijeva,desna = skaliranje_opsega(pretr_ord, lijeva, desna)
        
        ordi = linspace(lijeva,desna,brojTacaka)
        
        for i in range(len(ap)):
            lista = []
            for j in range(len(ordi)):
                lista.append(lamb_fun((ap[j],ordi[i])))
            fun.append(lista)
            
        plt.figure(1)
        plt.contour(ap, ordi, fun, 100, cmap='RdGy')
        plt.colorbar()
        plt.xlabel(str(varijable[0]))
        plt.ylabel(str(varijable[1]))
        plt.title('Nivo linije')
        plt.grid(True)
        plt.plot(pretr_aps,pretr_ord,'c-')
        for i in range(len(pretr_aps)-1):
            plt.plot(pretr_aps[i],pretr_ord[i],'kx')
        plt.plot(tacka[0],tacka[1],'ro')
        
        
        plt.figure(2)
        ose = plt.axes(projection = '3d')
        ose.contour3D(ap, ordi, fun, 100, cmap='RdGy')
        ose.grid(True)
        ose.set_xlabel(str(varijable[0]))
        ose.set_ylabel(str(varijable[1]))
        ose.set_title('3D Prikaz')
        ose.scatter(tacka[0],tacka[1],ekstrem,c='b', marker='o')
        plt.show()
        
        return 1


print("Biblioteka SouthwellSearchLibVH ucitana.")
print("Biblioteka >>matplotlib.pyplot<< ucitana kao >>plt<<.")
print("Ucitana je funkcija 'linspace' iz >>numpy<< biblioteke.")
print("Ucitane su funkcije 'symbols','diff' i 'lambdify' iz >>sympy<< biblioteke.")
