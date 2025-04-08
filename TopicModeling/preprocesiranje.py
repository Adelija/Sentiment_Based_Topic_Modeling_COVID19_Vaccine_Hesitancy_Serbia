# -*- coding: utf-8 -*-
"""
Created on Sun Jan 08 00:23:23 2017

@author: Adela
"""
# many_stop_words paket ubacen kako bi se koristile srpske stop reci
# stopwords-sr.txt fajl sa stop recima 
from many_stop_words import get_stop_words
from nltk.tokenize import RegexpTokenizer
# from nltk.tokenize import TweetTokenizer
from nltk.tokenize import word_tokenize

import re
from csv import writer
from csv import reader

def preproces(recenica):
    stop_reci = get_stop_words('sr')
    recenica = recenica.lower()
    reg_tokenizer = RegexpTokenizer(r'\w+')
    
    # tweet_tokenizer = TweetTokenizer() # kao izlaz daje tip unicode pa pravi problem kao argument stemeru

    tokens = reg_tokenizer.tokenize(recenica)
    #tokens = tweet_tokenizer.tokenize(recenica)
    filtered_words = [w for w in tokens if not w in stop_reci]
    return " ".join(filtered_words)

def preprocesBezStopReci(recenica):
    recenica = recenica.lower()
    reg_tokenizer = RegexpTokenizer(r'\w+')
    
    # tweet_tokenizer = TweetTokenizer() # kao izlaz daje tip unicode pa pravi problem kao argument stemeru

    tokens = reg_tokenizer.tokenize(recenica)
    #tokens = tweet_tokenizer.tokenize(recenica)
    filtered_words = [w for w in tokens]
    return " ".join(filtered_words)




# #print type(normaliz)
# #stemov=stem_str(normaliz)
def srediBrojeve(tvit):
    tvit=re.sub("(\d+[,.]\d+) din", "", tvit) # brojevi sa tackom izmedju 20.000 i din na kraju
    tvit=re.sub(r"(\d+(?:\s+\d+)*) din", "",tvit) #brojevi i brojevi sa razmakom (npr. 20 000) i din na kraju
    tvit=re.sub("[£$€] \d+[,.]\d+", "", tvit)# brojevi sa tackom izmedju 20.000 i £, $ ili € na pocetku
    tvit=re.sub(r" [£$€] (\d+(?:\s+\d+)*)", "",tvit) # brojevi i brojevi sa razmakom (npr. 20 000) i i £, $ ili € na pocetku 
    tvit=re.sub("\d+[,.]\d+", "", tvit) #  brojevi sa tackom izmedju 20.000
    tvit=re.sub("(\d+[/|-]\d+[/|-]\d+)", "",tvit) # Datumi
    tvit=re.sub(r"(\d+(?:\s+\d+)*)", "",tvit) # brojevi sa razmakom (npr. 20 000)
    return tvit

def tokenizuj(tvitOrg):
   #tokenizacija brojeva, datuma, valuta
    tvit=re.sub("\\n"," ",tvitOrg,flags=re.MULTILINE)
    tvit=re.sub(r"[\\n][\\n]{2,}","", tvit,flags=re.MULTILINE)
    tvit=re.sub(r"\\n"," ",tvit)  # ovaj red je pravio problem ako se cita iy csv fajla zbog \n
    # tvit=' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",tvit).split()) #Uklanjanje hash simbola ali ostaje tekst
    tvit=tvit.replace("#", "")
    tvit=re.sub("https?://[^\s]+","",tvit) # Uklanjanje URLa
    tvit=re.sub("(?:@[\w_]+)"," ",tvit) # Uklanjanje @mention 
    # #tekst=re.sub("(?:\#+[\w_]+[\w\'_\-]*[\w_]+)","",tekst) # Uklanjanje #hashtag 
    tvit=re.sub("via","",tvit)
    tvit=re.sub("/\r?\n|\r/","",tvit) #uklanjanje nove linije
     
    tvit=re.sub("(\d+[,.]\d+) din", "", tvit) # brojevi sa tackom izmedju 20.000 i din na kraju
    tvit=re.sub(r"(\d+(?:\s+\d+)*) din", "",tvit) #brojevi i brojevi sa razmakom (npr. 20 000) i din na kraju
    tvit=re.sub("[£$€] \d+[,.]\d+", "", tvit)# brojevi sa tackom izmedju 20.000 i £, $ ili € na pocetku
    tvit=re.sub(r" [£$€] (\d+(?:\s+\d+)*)", "",tvit) # brojevi i brojevi sa razmakom (npr. 20 000) i i £, $ ili € na pocetku 
    #tvit = re.sub("([1-9]\d*(\.\d{2})?) din$", "CURRENCY",tvit)
    tvit=re.sub("\d+[,.]\d+", "", tvit) #  brojevi sa tackom izmedju 20.000
    #tvit=re.sub("\d+(?:\.\d+)?,\d+", "BN", tvit)
    tvit=re.sub("(\d+[/|-]\d+[/|-]\d+)", "  ",tvit) # Datumi
    tvit=re.sub(r"(\d+(?:\s+\d+)*)", "",tvit) # brojevi sa razmakom (npr. 20 000)
    tokenized=word_tokenize(tvit)
    tokenizeds= " ".join(tokenized)
    return tokenizeds  

def ukloniStopReci(recenica):
    stop_reci = get_stop_words('sr')
    recenica = recenica.lower()
    #reg_tokenizer = RegexpTokenizer(r'\w+')
    #reg_tokenizer = RegexpTokenizer(r'\w+|\S+')
    reg_tokenizer = RegexpTokenizer(r'\w+|[.,?!:;]+')
    tokens = reg_tokenizer.tokenize(recenica)
    filtered_words = [w for w in tokens if not w in stop_reci]
    return " ".join(filtered_words)   

with open('../podaci/negativni_filtered_ispravljenID_lematizovan.csv', 'r', encoding="utf8") as read_obj, \
        open('../podaci/negativni_filtered_ispravljenID_lematizovanBezStop.csv', 'w', newline='', encoding="utf8") as write_obj:
    # Create a csv.reader object from the input file object
    csv_reader = reader(read_obj)
    # Create a csv.writer object from the output file object
    csv_writer = writer(write_obj)
    # Read each row of the input csv file as list
    for row in csv_reader:
        # Append the default text in the row / list
        # a="Šta nam zapravo govori glavni čovek u #USA 🇺🇸 po pitanju #Covid19, “doktor Fauči”? \nDa #Pfizer &amp; co. vakcine ne mogu zaustaviti pandemiju. https://t.co/0PvxFT4hrB"
        # a='USA\nSmrtni slučajevi #KORONA od "KOVID-19" 2020. u odnosu na 2021. godinu:\n\n- 2020 Kada nije bilo vakcina: 351.754\n\n- 2021 Sa velikim procentom vakcinisanih:\n 412,609\n\nPovećanje od 17% https://t.co/jVbyBEV9rF'
        a=row[3]
        print("original: "+a)
        # b=tokenizuj(a)
        # print("bez n n : "+b)
        # c=srediBrojeve(b)
        # # print("tokenizovano", b)
        s=ukloniStopReci(a) #ovde se uklanjaju i stop reci
        print("bez stop reci", s)
        # st=stem_str(s)  //necemo stemovati jer cemo koristiti RELDI tokenizer
        # print("Stemovano",st)
        row.append(s)
        print("")
        # Add the updated row / list to the output file
        csv_writer.writerow(row)

    



# # # # # s=" 25-15-2016 , 100 000 000 din, 100 din , $ 5000.00 , $ 500, 2.608 din, 69.90, 9000 "  
# s='USA\nSmrtni slučajevi od "KOVID-19" 2020. u odnosu na 2021. godinu:\n\n- 2020 Kada nije bilo vakcina: 351.754\n\n- 2021 Sa velikim procentom vakcinisanih:\n 412,609\n\nPovećanje od 17% https://t.co/jVbyBEV9rF'
# # # # s="Krije se sastav #mRNA💉💉, jer je u pitanju, tobož, poslovna tajna. \nAli danas znamo koje štetne materije su sadržavale 💉💉protiv svinjskog gripa, koje je pre desetak godina, jednako siledžijski, uz pretnje i zastrašivanje, kao danas, promovisao #PredragKon! \nhttps://t.co/hNvyLEXHDA https://t.co/wd2JeD3PTe"
# print("original: ",s)
# t=tokenizuj(s)
# print ("Tokenizovano: ", t,"\n")
# b=srediBrojeve(t)
# k=preproces(b)
# print ("Preprocesirano: ",k)


 