import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from webcrawl import *


class MainWindow:
    def __init__(self, master):

        # instantiating root
        self.master = master

        # instantiating all frames in the app
        self.frame1 = tk.Frame(self.master, width=350, height=90,
                               bg="ivory", relief = tk.GROOVE, borderwidth = 3)
        self.frame2 = tk.Frame(self.master, width=350, height=35,
                               bg="ivory", relief = tk.GROOVE, borderwidth = 3)
        self.frame3 = tk.Frame(self.master, width=350, height=35,
                               bg="ivory", relief = tk.GROOVE, borderwidth = 3)
        self.frame4a = tk.Frame(self.master, width=260, height=100,
                               bg="ivory", relief = tk.GROOVE, borderwidth = 3)
        self.frame4b = tk.Frame(self.master, width=90, height=50,
                               bg="ivory", relief = tk.GROOVE, borderwidth = 3)
        self.frame4c = tk.Frame(self.master, width=90, height=50,
                                bg="ivory", relief=tk.GROOVE, borderwidth=3)
        self.frame5 = tk.Frame(self.master, width=350, height=35,
                               bg="ivory", relief = tk.GROOVE, borderwidth = 3)
        self.frame6 = tk.Frame(self.master, width=350, height=35,
                               bg="ivory", relief = tk.GROOVE, borderwidth = 3)
        self.frame7 = tk.Frame(self.master, width=350, height=35,
                               bg="ivory", relief = tk.GROOVE, borderwidth = 3)
        self.frame8 = tk.Frame(self.master, width=350, height=100,
                               bg="ivory", relief = tk.GROOVE, borderwidth=3)
        self.frame9 = tk.Frame(self.master, width=350, height=50,
                               bg="ivory", relief = tk.GROOVE, borderwidth=3)

        self.frame1.grid(column=0, row=0, columnspan=2)
        self.frame1.pack_propagate(False)

        self.frame2.grid(column=0, row=1, columnspan=2)
        self.frame2.pack_propagate(False)

        self.frame3.grid(column=0, row=2, columnspan=2)
        self.frame3.pack_propagate(False)

        self.frame4a.grid(column=0, row=3, columnspan=1, rowspan = 2)
        self.frame4a.pack_propagate(False)

        self.frame4b.grid(column=1, row=3, columnspan=1, rowspan = 1)
        self.frame4b.pack_propagate(False)

        self.frame4c.grid(column=1, row=4, columnspan=1, rowspan = 1)
        self.frame4c.pack_propagate(False)


        self.frame5.grid(column=0, row=5, columnspan=2)
        self.frame5.pack_propagate(False)

        self.frame6.grid(column=0, row=6, columnspan=2)
        self.frame6.pack_propagate(False)

        self.frame7.grid(column=0, row=7, columnspan=2)
        self.frame7.pack_propagate(False)

        self.frame8.grid(column=0, row=8, columnspan=2)
        self.frame8.pack_propagate(False)

        self.frame9.grid(column=0, row=9, columnspan=2)
        self.frame9.pack_propagate(False)

        # ---------------------------------------------------------------------

        # instantiating all label for each frame in the app
        tk.Label(self.frame1, text="Hello, Welcome to WebCrawler! \n"
                                   "The purpose of this program is to mine "
                                   "links and their contents. Intended users "
                                   "are researchers and for non-profit "
                                   "purposes only.",
                 bg = "ivory", anchor = tk.N, justify = tk.CENTER,
                 wraplength = 340).pack(side =tk.TOP)

        tk.Label(self.frame2, text = " 1. Load your seed file\t\t: ",
                 bg = "ivory", anchor = tk.W).pack(side = tk.LEFT)
        tk.Label(self.frame3, text = " 2. Crawling depth\t\t: ",
                 bg = "ivory", anchor = tk.W).pack(side = tk.LEFT)
        tk.Label(self.frame4a, text = " 3. Filter type : ",
                 bg = "ivory", anchor = tk.W).pack(side = tk.LEFT)
        tk.Label(self.frame5, text = " 4. Number of concurrent crawling\t: ",
                 bg = "ivory", anchor = tk.W).pack(side = tk.LEFT)
        tk.Label(self.frame6, text = " 5. Edges List Filename\t: ",
                 bg = "ivory", anchor = tk.W).pack(side = tk.LEFT)
        tk.Label(self.frame7, text = " 6. Nodes List Filename\t: ",
                 bg = "ivory", anchor = tk.W).pack(side = tk.LEFT)
        tk.Label(self.frame8, text = "I hereby acknowledge that I have read "
                                     "and understood the underlying laws and "
                                     "regulations in relation to web crawling, "
                                     "data mining, and intellectual property, "
                                     "and wish to proceed.",
                 bg="ivory", anchor=tk.N, wraplength = 340,
                 justify = tk.CENTER).pack(side=tk.TOP)
        tk.Label(self.frame6, text = ".csv ").pack(side = tk.RIGHT)
        tk.Label(self.frame7, text = ".csv ").pack(side = tk.RIGHT)

        # instantiating buttons
        self.button1 = tk.Button(self.frame2, text = ' select seed file',
                                 command = self.get_seed_address, anchor = tk.W)
        self.button2 = tk.Button(self.frame4b, text='select\nfilter file',
                                 command=self.get_filter_address)
        self.button2.config(state=tk.DISABLED)
        self.button3 = tk.Button(self.frame9, text = " run the crawl!",
                                 command = self.new_window)

        self.button1.pack(side = tk.LEFT)
        self.button2.place(relx = 0.5, rely = 0.5, anchor = tk.CENTER)
        self.button3.place(relx = 0.5, rely = 0.5, anchor = tk.CENTER)

        # instantiating drop-down menus
        crawl_depth_options       = list(range(1, 11))
        parallel_instance_options = list(range(1, 5))

        self.depthChoice    = tk.StringVar(self.frame3)
        self.depthChoice.set(crawl_depth_options[0])
        self.crawl_depth = tk.OptionMenu(self.frame3, self.depthChoice,
                                         *crawl_depth_options)
        self.crawl_depth.place(relx = 0.75, rely = 0.5, anchor = tk.CENTER)

        self.parallelChoice = tk.StringVar(self.frame5)
        self.parallelChoice.set(parallel_instance_options[0])
        self.parallel_instance = tk.OptionMenu(self.frame5, self.parallelChoice,
                                               *parallel_instance_options)
        self.parallel_instance.place(relx = 0.75, rely = 0.5,
                                     anchor = tk.CENTER)

        # instantiate checkbuttons
        self.noDomesticLinkStatus = tk.IntVar()
        self.contentFilterStatus  = tk.IntVar()
        self.disclaimerStatus     = tk.IntVar()

        no_domestic_link = tk.Checkbutton(self.frame4a, text = "Non-domestic",
                                          variable = self.noDomesticLinkStatus,
                                          bg = "ivory", fg = "black")
        content_filter    = tk.Checkbutton(self.frame4a, text = "Keywords\t",
                                          variable = self.contentFilterStatus,
                                          bg = "ivory", fg = "black",
                                          command = self.enable_filter_file)
        i_agree          = tk.Checkbutton(self.frame8, text = "I agree",
                                          variable = self.disclaimerStatus,
                                          bg = "ivory", fg = "black")

        no_domestic_link.pack(side = tk.TOP, anchor = tk.W)
        content_filter.pack(side = tk.BOTTOM, anchor = tk.W)
        i_agree.pack(side = tk.TOP)

        # instantiate textboxes
        self.edgesListFilename = tk.Entry(self.frame6)
        self.nodesListFilename = tk.Entry(self.frame7)

        self.edgesListFilename.pack()
        self.nodesListFilename.pack()

        self.seedAddress = ''
        self.filterAddress = ''

    def enable_filter_file(self):
        if self.contentFilterStatus.get():
            self.button2.config(state=tk.NORMAL)
        else:
            self.button2.config(state=tk.DISABLED)

    def get_seed_address(self):
        self.seedAddress = filedialog.askopenfilename()

    def get_filter_address(self):
        self.filterAddress = filedialog.askopenfilename()

    def new_window(self):

        potentialError = []

        if self.seedAddress == "":
            potentialError.append("- Seed file is missing")
        if self.contentFilterStatus.get() == 1 and self.filterAddress == "":
            potentialError.append("- Filter file is missing")
        if self.edgesListFilename.get() == "":
            potentialError.append("- Edges list filename is missing")
        if self.nodesListFilename.get() == "":
            potentialError.append("- Nodes list filename is missing")
        if self.disclaimerStatus.get() == 0:
            potentialError.append("- Please check 'I agree' checkbox or exit "
                                  "if you wish to expore more about the "
                                  "underlying regulations")

        crawlQuery = [self.seedAddress, self.depthChoice.get(),
                      self.noDomesticLinkStatus.get(),
                      self.contentFilterStatus.get(), self.filterAddress,
                      self.parallelChoice.get(), self.edgesListFilename.get(),
                      self.nodesListFilename.get()]

        if len(potentialError) != 0:
            messagebox.showwarning("Error", message="\n".join(potentialError))

        else:
            msgBox = messagebox.askquestion("Proceed?",
                                   message = "Do you wish to proceed with "
                                             "entires as follows:" + \
                                             "\n".join(crawlQuery))
            if msgBox == "yes":
                #multiprocess_crawling(crawlQuery[0], crawlQuery[1],
                #                      crawlQuery[2], crawlQuery[])
                self.newWindow = tk.Toplevel(self.master)
                self.app = RunTheCrawler(self.newWindow, self)

    def get_info(self):

        return([self.seedAddress, "\n",
              self.depthChoice.get(), "\n",
              self.noDomesticLinkStatus.get(), " ",
              self.contentFilterStatus.get(),
              "\n",
              self.filterAddress, "\n",
              self.parallelChoice.get(), "\n",
              self.edgesListFilename.get(), "\n",
              self.nodesListFilename.get(), "\n"])

        
# TODO
class RunTheCrawler:
    def __init__(self, master, mainwindow):
        self.master = master
        self.frame = tk.Frame(self.master, height = 400, width = 400)
        self.frame.pack()
        self.label1 = tk.Label(self.frame, text = mainwindow.get_info())
        self.label1.pack()

    def close_windows(self):
        self.master.destroy()


def main():
    root = tk.Tk()
    root.geometry("350x515")
    root.title("WebCrawler")
    root.resizable(False, False)
    app = MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()