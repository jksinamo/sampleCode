import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from webcrawl import *
import threading
import sys


class MainWindow:
    def __init__(self, master):

        # instantiating tkinter root
        self.master = master

        # instantiating all frames in the app
        self.frame1 = tk.Frame(self.master, width=350, height=90,
                               bg="ivory", relief = tk.GROOVE, borderwidth = 3)
        self.frame2 = tk.Frame(self.master, width=350, height=35,
                               bg="ivory", relief = tk.GROOVE, borderwidth = 3)
        self.frame3 = tk.Frame(self.master, width=350, height=35,
                               bg="ivory", relief = tk.GROOVE, borderwidth = 3)
        self.frame4a = tk.Frame(self.master, width=260, height=50,
                               bg="ivory", relief = tk.GROOVE, borderwidth = 3)
        self.frame4b = tk.Frame(self.master, width=90, height=50,
                               bg="ivory", relief = tk.GROOVE, borderwidth = 3)
        self.frame5 = tk.Frame(self.master, width=350, height=35,
                               bg="ivory", relief = tk.GROOVE, borderwidth = 3)
        self.frame6 = tk.Frame(self.master, width=350, height=35,
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

        self.frame4a.grid(column=0, row=3, columnspan=1)
        self.frame4a.pack_propagate(False)

        self.frame4b.grid(column=1, row=3, columnspan=1)
        self.frame4b.pack_propagate(False)

        self.frame5.grid(column=0, row=5, columnspan=2)
        self.frame5.pack_propagate(False)

        self.frame6.grid(column=0, row=6, columnspan=2)
        self.frame6.pack_propagate(False)

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
        tk.Label(self.frame6, text = " 5. Output Filename\t: ",
                 bg = "ivory", anchor = tk.W).pack(side = tk.LEFT)
        tk.Label(self.frame8, text = "I hereby acknowledge that I have read "
                                     "and understood the underlying laws and "
                                     "regulations in relation to web crawling, "
                                     "data mining, and intellectual property, "
                                     "and wish to proceed.",
                 bg="ivory", anchor=tk.N, wraplength = 340,
                 justify = tk.CENTER).pack(side=tk.TOP)
        tk.Label(self.frame6, text=".csv ", bg="ivory").pack(side =tk.RIGHT)

        # instantiating buttons
        self.seedAddress = ''
        self.filterAddress = None

        self.seedSelectButton = tk.Button(self.frame2,
                                          text =' select seed file',
                                          command = self.get_seed_address,
                                          anchor = tk.W)
        self.selectFilterButtonn = tk.Button(self.frame4b,
                                             text='select\nfilter file',
                                             command=self.get_filter_address)
        self.selectFilterButtonn.config(state=tk.DISABLED)
        self.executeCrawlingButton = tk.Button(self.frame9,
                                               text =" run the crawl!",
                                               command = self.new_window)

        self.seedSelectButton.pack(side = tk.LEFT)
        self.selectFilterButtonn.place(relx= 0.5, rely= 0.5, anchor=tk.CENTER)
        self.executeCrawlingButton.place(relx= 0.5, rely= 0.5, anchor=tk.CENTER)

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
        self.outputFilename = tk.Entry(self.frame6)
        self.outputFilename.pack()

        #self.crawlQuery = []

    def enable_filter_file(self):
        if self.contentFilterStatus.get():
            self.selectFilterButtonn.config(state=tk.NORMAL)
        else:
            self.selectFilterButtonn.config(state=tk.DISABLED)

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
        if self.outputFilename.get() == "":
            potentialError.append("- Output filename is missing")
        if self.disclaimerStatus.get() == 0:
            potentialError.append("- Please check 'I agree' checkbox or exit "
                                  "if you wish to expore more about the "
                                  "underlying regulations")

        if len(potentialError) != 0:
            messagebox.showwarning("Error", message="\n".join(potentialError))

        else:
            self.executeCrawlingButton.config(state=tk.DISABLED)
            self.newWindow = tk.Toplevel(self.master)
            self.app = RunTheCrawler(self.newWindow, self)

    def get_info(self):

        return([self.seedAddress,
                int(self.depthChoice.get()),
                bool(not self.noDomesticLinkStatus.get()),
                bool(self.contentFilterStatus.get()),
                self.filterAddress,
                int(self.parallelChoice.get()),
                str(self.outputFilename.get() + ".csv")])


class RunTheCrawler:
    def __init__(self, master, mainwindow):
        self.master = master
        self.frame = tk.Frame(self.master, height = 400, width = 400)
        self.frame.pack()

        self.executeSeedAddress    = mainwindow.get_info()[0]
        self.executeDepth          = mainwindow.get_info()[1]
        self.executeDomesticFilter = mainwindow.get_info()[2]
        self.executeContentFilter  = mainwindow.get_info()[3]
        self.executeFilterAddress  = mainwindow.get_info()[4]
        self.executeParallelChoice = mainwindow.get_info()[5]
        self.executeOutputFilename = mainwindow.get_info()[6]

        tk.Label(self.frame, text="Your crawl will have profile as "
                                  "follows...").grid(
            row=0, column=0, columnspan=3, sticky = tk.W)
        tk.Label(self.frame, text="Seed Address\t\t: " +
                                  self.executeSeedAddress).grid(
            row=1, column=0,columnspan=3, sticky = tk.W)
        tk.Label(self.frame, text="Depth\t\t\t: " +
                                  str(self.executeDepth)).grid(
            row=2, column=0, columnspan=3, sticky = tk.W)
        tk.Label(self.frame, text="Domestic Outlinks\t\t: " +
                                  str(self.executeDomesticFilter)).grid(
            row=3, column=0, columnspan=3, sticky = tk.W)
        tk.Label(self.frame, text="Content Filter\t\t: " +
                                  str(self.executeContentFilter)).grid(
            row=4, column=0, columnspan=3, sticky = tk.W)
        tk.Label(self.frame, text="Content Filter Address\t\t: " +
                                  str(self.executeFilterAddress)).grid(
            row=5, column=0, columnspan=3, sticky = tk.W)
        tk.Label(self.frame, text="Number of Parallel Process\t: " +
                                  str(self.executeParallelChoice)).grid(
            row=6, column=0, columnspan=3, sticky = tk.W)
        tk.Label(self.frame, text="Output Filename\t\t: " +
                                  self.executeOutputFilename).grid(
            row=7, column=0, columnspan=3, sticky = tk.W)
        tk.Label(self.frame, text="\nContinue?").grid(
            row=8, column=0, columnspan=3, sticky = tk.N)

        thr = threading.Thread(target=multiprocess_crawling,
                               args=(self.executeSeedAddress,
                                     self.executeDepth,
                                     self.executeDomesticFilter,
                                     self.executeParallelChoice,
                                     self.executeOutputFilename,
                                     self.executeFilterAddress))

        def run_the_crawl():
            cancel.config(state=tk.DISABLED)
            #thr.daemon = True
            thr.start()

        run = tk.Button(self.frame, text = "Yes", command = run_the_crawl)

        def back_to_master():
            mainwindow.executeCrawlingButton.config(state=tk.NORMAL)
            self.master.destroy()

        cancel = tk.Button(self.frame, text = "Back to Previous Window",
                           command = back_to_master)

        def exit_everything():

            for bot in botsList:
                bot.quit()
            sys.exit()

        exitApp = tk.Button(self.frame, text="Stop Everything",
                            command = exit_everything)

        run.grid(   row = 10, column = 0)
        cancel.grid(row = 10, column = 1)
        exitApp.grid(  row = 10, column = 2)


def main():
    root = tk.Tk()
    root.geometry("350x430")
    root.title("WebCrawler")
    root.resizable(False, False)
    app = MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()
