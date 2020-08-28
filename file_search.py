import os,pickle

import PySimpleGUI as sg
sg.ChangeLookAndFeel('Dark2')
class Gui:
    def __init__(self):
        self.layout=[[sg.Text('Find',size=(10,1)),sg.Input(size=(40,1),focus=True,key='TERM'),sg.Radio('Contains',group_id='choice',key='CONTAINS',default=True),sg.Radio('Startswith',group_id='choice',key='STARTSWITH'),sg.Radio('Endswith',group_id='choice',key='ENDSWITH')],
                     [sg.Text('Root path',size=(10,1)),sg.Input(size=(40,1),key='PATH'),sg.FolderBrowse('browse'),sg.Button('re_index',size=(10,1),key='REINDEX'),sg.Button('Search',size=(10,1),key='SEARCH',bind_return_key=True)],
                     [sg.Output(size=(100,30),key='OUTPUT')]]
        self.window=sg.Window('search Engine',self.layout)
        

class SearchEngine:
    def __init__(self):
        self.file_index=[]
        self.results=[]
        self.matches=0
        self.records=0
    
    def create_index(self,values): 
        root_path=values['PATH']      
        self.file_index= [(root,files) for root,dirs,files in os.walk(root_path) if files]
        with open('file_index.pkl','wb') as f:
            pickle.dump(self.file_index,f)
            

    def load_index(self):
        try:
            with open('file_index.pkl','rb') as f:
                self.file_index=pickle.load(f)
        except:
            self.file_index=[]
            
        pass
    def search(self,values):
        self.results.clear()
        self.matches=0
        term=values['TERM']
        self.records=0
        for path,files in self.file_index:
            for file in files:
                self.records+=1
                if (values['CONTAINS'] and term.lower() in file.lower() 
                    or values['STARTSWITH'] and file.lower().startswith(term.lower())
                    or values['ENDSWITH'] and file.lower().endswith(term.lower())
                ):
                    fullpath=os.path.join(path,file)
                    self.results.append(fullpath)
                    self.matches+=1
                    
        with open('search_results.txt','w') as f:
            for row in self.results:
                f.write(row+'\n')
def test1():
    s=SearchEngine()
    s.create_index('/home/helios')
    s.load_index()
    s.search('biblioteca')
    print()
    print(f'>>there were {s.matches} matches out of {s.records} records')
# test()
def testgui():
    gui=Gui()
    while True:
        event,values=gui.window.read()
        print(event,values)
        
def eventLoop():
    s=SearchEngine()
    gui=Gui()
    s.load_index()
    while True:
        event,values=gui.window.read()
        if event is None:
            break
        if event=='REINDEX':
            print('creating index')
            s.create_index(values)
            print('\n>>index created')
        if event=='SEARCH':
            gui.window.FindElement('OUTPUT').Update('')
            os.system('clear')
            print('searching')
            s.search(values)
            print(f'>> {s.matches} matches found out of {s.records} records')
            if s.matches>0:
                print('\nresults saved to search_results.txt file\n')
            for res in s.results:
                print(res)
                

if __name__ == '__main__': 
    eventLoop()
                

                
                