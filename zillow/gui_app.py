from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
from scrapy import spiderloader
from scrapy.utils import project
from scrapy.utils.log import configure_logging
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
import threading


def get_spiders():
    settings = project.get_project_settings()
    spider_loader = spiderloader.SpiderLoader.from_settings(settings)
    return spider_loader.list()

def get_chosen_spider(spider):
    global chosen_spider
    chosen_spider = spider
    return chosen_spider

def get_chosen_feed(feed):
    global chosen_feed
    chosen_feed = feed
    return chosen_feed

def browse_btn():
    global folder_path
    folder_path = filedialog.askdirectory()
    folder_path_entry.delete(0,END)
    folder_path_entry.insert(0,folder_path)
    return folder_path

#Spawing a new thread
def start_execute_thread(event):
    global execute_thread
    execute_thread = threading.Thread(target=execute_spider, daemon=True)
    execute_thread.start()
    app.after(10, check_execute_thread)


def check_execute_thread(event):
    if execute_thread.is_alive():
        app.after(10, check_execute_thread)


def execute_spider():
    if dataset_entry.get() == '' or chosen_feed not in ['csv','json']:
        messagebox.showerror("Error IF",'All entries are required')
        return
    try:
        feed_url = f"file:///{folder_path}/{dataset_entry.get()}.{chosen_feed}"
    except:
        messagebox.showerror("Error TRY",'All entries are required')

    settings = project.get_project_settings()
    settings.set('FEED_URI',feed_url)
    settings.set('FEED_TYPE',chosen_feed)

    configure_logging()
    runner = CrawlerRunner(settings)
    runner.crawl(chosen_spider)

    reactor.run(installSignalHandlers=False)



def drop_menu_items(sp_label='Choose a spider',sp_text='choose a spider',spiders_list=['Spider_1', 'spider_2'],scom='' ,srow=0, scolumn=0, drow=0, dcolumn=1, clspan=2, spx=10, spy=10):
    spider_label = Label(app, text=sp_label)
    spider_label.grid(row=srow , column=scolumn, sticky=W, pady=spx, padx=spy)
    spider_text = StringVar(app)
    spider_text.set(sp_text)
    spiders_dropdown = OptionMenu(app, spider_text, *spiders_list, command= scom)
    spiders_dropdown.grid(row=drow, column=dcolumn, columnspan=clspan)

app = Tk()
spiders_loader_list= [spider for spider in get_spiders()]

#Spiders List
drop_menu_items(spiders_list=spiders_loader_list,scom=get_chosen_spider)

#Feed Type
drop_menu_items(sp_label='Choose a feed',sp_text='choose a feed',scom=get_chosen_feed,spiders_list=['json', 'csv'], srow=1, scolumn=0, drow=1, dcolumn=1)

#Path Entry
folder_path_text= StringVar(app)
folder_path_entry= Entry(app, textvariable=folder_path_text)
folder_path_entry.grid(row=2, column=0, pady=10 ,padx=10)

#Dataset Entry
dataset_text= StringVar(app)
dataset_entry= Entry(app, textvariable=dataset_text ,width=10)
dataset_entry.grid(row=2, column=1, pady=10 ,padx=10)

browse_btn = Button(app, text="Browse", command=browse_btn)
browse_btn.grid(row=2, column=2)


exe_btn = Button(app, text="Execute", command=lambda:start_execute_thread(None))
exe_btn.grid(row=3, column=0, columnspan=3)


app.title('Spider Executor')
app.geometry('300x200')
app.resizable(False, False)
app.mainloop()


