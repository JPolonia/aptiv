from PyPDF2 import PdfFileWriter, PdfFileReader

with open("in.pdf", "rb") as in_f:
    input1 = PdfFileReader(in_f)
    output = PdfFileWriter()

    numPages = input1.getNumPages()
    print ("document has %s pages." % numPages)

    for i in range(numPages):
        page = input1.getPage(i)
        print (page.mediaBox.getUpperRight_x(), page.mediaBox.getUpperRight_y())
        page.trimBox.lowerLeft = (25, 25)
        page.trimBox.upperRight = (225, 225)
        page.cropBox.lowerLeft = (50, 50)
        page.cropBox.upperRight = (200, 200)
        output.addPage(page)

    with open("out.pdf", "wb") as out_f:
        output.write(out_f)






path1 = "files/24090330_H.pdf"
path2 = "out.pdf"

import copy
import math
import PyPDF2

def split_pages(src, dst):
    with open(src, "rb") as in_f:
        input = PyPDF2.PdfFileReader(in_f)
        output = PyPDF2.PdfFileWriter()
        numPages = input.getNumPages()


        for i in range(numPages):
            p = input.getPage(i)
            q = copy.copy(p)
            q.mediaBox = copy.copy(p.mediaBox)

            x1, x2 = p.mediaBox.lowerLeft
            x3, x4 = p.mediaBox.upperRight

            x1, x2 = math.floor(x1), math.floor(x2)
            x3, x4 = math.floor(x3), math.floor(x4)
            x5, x6 = math.floor(x3/2), math.floor(x4/2)

            if x3 > x4:
                # horizontal
                p.mediaBox.upperRight = (x5, x4)
                p.mediaBox.lowerLeft = (x1, x2)

                q.mediaBox.upperRight = (x3, x4)
                q.mediaBox.lowerLeft = (x5, x2)
            else:
                # vertical
                p.mediaBox.upperRight = (x3, x4)
                p.mediaBox.lowerLeft = (x1, x6)

                q.mediaBox.upperRight = (x3, x6)
                q.mediaBox.lowerLeft = (x1, x2)

            output.addPage(p)
            output.addPage(q)

        with open(dst, "wb") as out_f:
            output.write(out_f)

split_pages(path1, path2)


from non_used.trim_page import trim
trim(path2)



class assembley:
    def __init(self,nome,componentes,local1): #mete-se 0 no inicio porque ainda nao tem componentes
        self.componentes = {}
        self.name = nome
        self.local = local1
        def adionarquantidadejaexiste(self,partnumber,quantidade):
            x = self.componente[partnumber]
            del self.componente[partnumber]
            self.componete[partnumber]=quantidade+x
        def adicionarcomponentes(self,partnumber,descricao):
            if partnumber in self.componentes == False:
                self.componentes[partnumber]={"qty" : 1, "description" : descricao}
            else:

                self.componentes[partnumber]["qty"] += 1

class componente:
    def _init_  (self,nameentrou,quantidadeinicial):
        self.name= nameentrou
        self.quantidade = quantidadeinicial
    def adicionar(self):
        self.quantidade +=1

x = {"ola":1}
x["tu"] = 10
x["ele"] = {'qty':10, 'boneco':9}

#ordenar keys
x=sorted(x)


print(list(x))

for i in range(0, list(x).count):
    list(x)[i]






scores = {"class1": [], "class2": [], "class3": []}

def main():
    name= input ('What is your name?')
    for i in range(0,3)
        score = input("Enter your score: ")
        clss =input('which class?')
        if clss==1:
            scores["class1"].append({"name": name, "score": score})
        elif clss==2:
            scores["class2"].append({"name": name, "score": score})
        elif clss==3:
            scores["class3"].append({"name": name, "score": score})
    print scores





for x in test_list:
    if x.value == value:
        print
        "i found it!"
        break
else:
    x = None