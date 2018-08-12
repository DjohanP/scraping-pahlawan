import urllib.request
from lxml import html
import requests
import re
from operator import itemgetter

class ob_pahlawan:
    def __init__(self,nomor,name="",lhr="",mng="",ket="",pen="",lnk=""):
        self.id=nomor
        self.nama=name
        self.lahir=lhr
        self.meninggal=mng
        self.keterangan=ket
        self.penetapan=pen
        self.link=lnk
        self.keturunan=[]
cek=0
cektdkinfo=0
cektdk=0
def keturunan(urlweb="",nama="",keturunany=1):
    global cek
    global cektdkinfo
    global cektdk
    ada=0
    webpahlawan=requests.get("https://id.wikipedia.org"+urlweb)
    isiweb=webpahlawan.text
    if ("Tidak ada teks di halaman ini" in isiweb) or webpahlawan.status_code!=200:
        #print(nama+" Tidak Ditemukan")
        return
    else:
        if '<table class="infobox' not in isiweb:
            a=19
            #cektdkinfo=cektdkinfo+1
            #print(nama+" tidak ada info box")
        else:
            #infobox=re.split('<table class="infobox |</table>',isiweb)
            #print(nama+" Info Box")
            infobox=isiweb.split('<table class="infobox')
            infobox=infobox[1].split('</table>')
            infobox=infobox[0]
            if  "ANAK</th>" in infobox:
                #print(nama+" Punya Anak")
                anak=infobox.split('ANAK</th>')
                ada=1
                #cek=cek+1
            elif "anak</th>" in infobox:
                #print(nama+" Punya Anak")
                anak=infobox.split('anak</th>')
                ada=1
                #cek=cek+1
            elif "Anak</th>" in infobox:
                #print(nama+" Punya Anak")
                anak=infobox.split('Anak</th>')
                ada=1
                #cek=cek+1
            if ada==1:
                anak=anak[1].split('</td>')
                anak=anak[0]
                anak=anak.replace("</th><td>\n","")
                anak=anak.replace("<td>","")
                anak=anak.replace("\n","")
                anak=anak.replace("1.","")
                anak=anak.replace('2. ',"")
                anak=anak.replace('3. ',"")
                anak=anak.replace('4. ',"")
                anak=anak.replace('5. ',"")
                anak=anak.replace('6. ',"")
                anak=anak.replace('♂ ',"")
                anak=anak.replace('♀ ',"")
                anak=anak.replace("<b>","")
                anak=anak.replace("</b>","")
                anak=anak.replace("<p>","")
                anak=anak.replace("</p>","")
                anak=anak.replace("<small>","")
                anak=anak.replace("</small>","")

                if "<div" not in anak:
                    #print(nama)
                    anak=anak.split("<br />")
                    arrayanak=[]
                    for m in anak:
                        if "<a" in m:#ada web tambahan
                            lnk=m
                            lnk=lnk.split('href="')
                            lnk=lnk[1].split('"')
                            lnk=lnk[0]
                            #print(lnk)
                            ketx=keturunany+1
                            mx=bersih_tag(m)
                            if "<sup" in mx:
                                mx=mx.split("<sup")
                                mx=mx[0]

                            xy=keturunan(lnk,mx,ketx)


                            arr={}
                            arr['nama']=mx
                            arr['keturunan']=keturunany
                            arrayanak.append(arr)
                            if xy is not None:
                                arrayanak.append(xy)
                        else:
                            arr={}
                            arr['nama']=m
                            arr['keturunan']=keturunany
                            arrayanak.append(arr)
                    #print(arrayanak)
                    return arrayanak
                    
                else:
                    return anak
                


def bersih_tag(nama):
    clean=""
    nama=nama.replace("<b>","")
    nama=nama.replace("</b>","")
    nama=nama.replace("<p>","")
    nama=nama.replace("</p>","")
    nama=nama.replace("\n","")
    ket2=re.split('<a |</a>',nama)
    for kete in ket2:
        if "href" not in kete:
            clean=clean+kete
        else:
            hapus=kete.split('">')
            clean=clean+hapus[1]
    return clean
    

def bershih_html(ket):
    kali=ket.count('<a')
    if kali > 0:
        clean=""
        ket2=re.split('<a |</a>',ket)
        for kete in ket2:
            if "href" not in kete:
                clean=clean+kete
            else:
                hapus=kete.split('">')
                clean=clean+hapus[1]
        return clean
    else:
        return ket
    


pahlawan=[]



isiawal=requests.get("https://id.wikipedia.org/wiki/Daftar_pahlawan_nasional_Indonesia")
isiawal=isiawal.text
#hapus atas
isiawal=isiawal.split("<caption>Pahlawan Nasional Indonesia")
isiawal=isiawal[1].split("</caption>")
isiawal=isiawal[1]

#hapus bawah
isiawal=isiawal.split('<h2><span class="mw-headline" id="Lihat_pula">Lihat pula')

isiawal=isiawal[0]

#ambil data nama pahlawan
isiawal=isiawal.split('<tr>')

i=0
for isi in isiawal:
    if(i>1):
        #ambil nama
        nama=isi.split("</th>")
        tablelain=nama[1]
        link=nama[0]
        nama=nama[0].split("</a>")
        nama=nama[0].split("title=")
        nama=nama[1].split('">')
        nama=nama[1]
        tablelain=tablelain.split("<td>")

        #thnlahir
        thnlhr=tablelain[1].split("\n</td>")
        thnlhr=thnlhr[0]
        
        #thnwafat
        thnwft=tablelain[2].split("\n</td>")
        thnwft=thnwft[0]

        #keterangan
        ket=tablelain[2].split('\n<td align="left">')
        ket=ket[1].split('\n</td>')
        ket=ket[0]
        ket=bershih_html(ket)

        #penetapan
        pen=tablelain[3].split("\n</td>")
        pen=pen[0]
        #link
        link=link.split('" title=')
        link=link[0].split('<a href="')
        link=link[1].split('" class')
        link=link[0]
        #print(tablelain)
        
        x=ob_pahlawan(i-1,nama,thnlhr,thnwft,ket,pen,link)
        pahlawan.append(x)
    i=i+1
i=1

for x in pahlawan:
    anakcucu=keturunan(x.link,x.nama,1)
    if anakcucu is not None:
        x.keturunan=anakcucu

for x in pahlawan:
    print(x.nama)
    print(x.keturunan)