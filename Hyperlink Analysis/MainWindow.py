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
        self.welcome_FRAME            = tk.Frame(self.master,
                                                 width=350, height=90,
                                                 bg="ivory", relief=tk.GROOVE,
                                                 borderwidth=3)
        self.load_seed_FRAME          = tk.Frame(self.master,
                                                 width=350, height=35,
                                                 bg="ivory", relief=tk.GROOVE,
                                                 borderwidth=3)
        self.crawling_depth_FRAME     = tk.Frame(self.master,
                                                 width=350, height=35,
                                                 bg="ivory", relief=tk.GROOVE,
                                                 borderwidth=3)
        self.filter_type_FRAME         = tk.Frame(self.master,
                                                 width=260, height=50,
                                                 bg="ivory", relief=tk.GROOVE,
                                                 borderwidth=3)
        self.select_filter_FRAME       = tk.Frame(self.master,
                                                 width=90, height=50,
                                                 bg="ivory", relief=tk.GROOVE,
                                                 borderwidth=3)
        self.parallel_process_FRAME   = tk.Frame(self.master,
                                                 width=350, height=35,
                                                 bg="ivory", relief=tk.GROOVE,
                                                 borderwidth = 3)
        self.edges_filename_FRAME      = tk.Frame(self.master,
                                                 width=350, height=35,
                                                 bg="ivory", relief=tk.GROOVE,
                                                 borderwidth = 3)
        self.nodes_filename_FRAME      = tk.Frame(self.master,
                                                 width=350, height=35,
                                                 bg="ivory", relief=tk.GROOVE,
                                                 borderwidth=3)
        self.disclaimer_FRAME         = tk.Frame(self.master,
                                                 width=350, height=100,
                                                 bg="ivory", relief=tk.GROOVE,
                                                 borderwidth=3)
        self.run_crawl_FRAME          = tk.Frame(self.master,
                                                 width=350, height=50,
                                                 bg="ivory", relief=tk.GROOVE,
                                                 borderwidth=3)

        self.welcome_FRAME.grid(column=0, row=0, columnspan=2)
        self.welcome_FRAME.pack_propagate(False)

        self.load_seed_FRAME.grid(column=0, row=1, columnspan=2)
        self.load_seed_FRAME.pack_propagate(False)

        self.crawling_depth_FRAME.grid(column=0, row=2, columnspan=2)
        self.crawling_depth_FRAME.pack_propagate(False)

        self.filter_type_FRAME.grid(column=0, row=3, columnspan=1)
        self.filter_type_FRAME.pack_propagate(False)

        self.select_filter_FRAME.grid(column=1, row=3, columnspan=1)
        self.select_filter_FRAME.pack_propagate(False)

        self.parallel_process_FRAME.grid(column=0, row=5, columnspan=2)
        self.parallel_process_FRAME.pack_propagate(False)

        self.edges_filename_FRAME.grid(column=0, row=6, columnspan=2)
        self.edges_filename_FRAME.pack_propagate(False)

        self.nodes_filename_FRAME.grid(column=0, row=7, columnspan=2)
        self.nodes_filename_FRAME.pack_propagate(False)

        self.disclaimer_FRAME.grid(column=0, row=8, columnspan=2)
        self.disclaimer_FRAME.pack_propagate(False)

        self.run_crawl_FRAME.grid(column=0, row=9, columnspan=2)
        self.run_crawl_FRAME.pack_propagate(False)

        # ---------------------------------------------------------------------

        # instantiating all label for each frame in the app
        tk.Label(self.welcome_FRAME, text="Hello, Welcome to WebCrawler! \n"
                                   "The purpose of this program is to mine "
                                   "links and their contents. Intended users "
                                   "are researchers and for non-profit "
                                   "purposes only.",
                 bg = "ivory", anchor = tk.N, justify = tk.CENTER,
                 wraplength = 340).pack(side =tk.TOP)

        tk.Label(self.load_seed_FRAME,
                 text =" 1. Load your seed file\t\t: ",
                 bg = "ivory", anchor = tk.W).pack(side = tk.LEFT)
        tk.Label(self.crawling_depth_FRAME,
                 text =" 2. Crawling depth\t\t: ",
                 bg = "ivory", anchor = tk.W).pack(side = tk.LEFT)
        tk.Label(self.filter_type_FRAME,
                 text =" 3. Filter type : ",
                 bg = "ivory", anchor = tk.W).pack(side = tk.LEFT)
        tk.Label(self.parallel_process_FRAME,
                 text =" 4. Number of concurrent crawling\t: ",
                 bg = "ivory", anchor = tk.W).pack(side = tk.LEFT)
        tk.Label(self.edges_filename_FRAME,
                 text =" 5. Edges Filename\t: ",
                 bg = "ivory", anchor = tk.W).pack(side = tk.LEFT)
        tk.Label(self.nodes_filename_FRAME,
                 text=" 6. Nodes Filename\t: ",
                 bg="ivory", anchor=tk.W).pack(side=tk.LEFT)
        tk.Label(self.disclaimer_FRAME,
                 text = "I hereby acknowledge that I have read "
                        "and understood the underlying laws and "
                        "regulations in relation to web crawling, "
                        "data mining, and intellectual property, "
                        "and wish to proceed.",
                 bg="ivory", anchor=tk.N, wraplength = 340,
                 justify = tk.CENTER).pack(side=tk.TOP)

        tk.Label(self.edges_filename_FRAME, text=".csv ", bg="ivory").pack(
            side =tk.RIGHT)
        tk.Label(self.nodes_filename_FRAME, text=".csv ", bg="ivory").pack(
            side=tk.RIGHT)

        # instantiating buttons
        self.seedAddress = ''
        self.filterAddress = None

        self.seedSelectButton = tk.Button(self.load_seed_FRAME,
                                          text =' select seed file',
                                          command = self.get_seed_address,
                                          anchor = tk.W)
        self.selectFilterButtonn = tk.Button(self.select_filter_FRAME,
                                             text='select\nfilter file',
                                             command=self.get_filter_address)
        self.selectFilterButtonn.config(state=tk.DISABLED)
        self.executeCrawlingButton = tk.Button(self.run_crawl_FRAME,
                                               text =" run the crawl!",
                                               command = self.new_window)

        self.seedSelectButton.pack(side = tk.LEFT)
        self.selectFilterButtonn.place(relx= 0.5, rely= 0.5, anchor=tk.CENTER)
        self.executeCrawlingButton.place(relx= 0.5, rely= 0.5, anchor=tk.CENTER)

        # instantiating drop-down menus
        crawl_depth_options       = list(range(1, 11))
        parallel_instance_options = list(range(1, 5))

        self.depthChoice    = tk.StringVar(self.crawling_depth_FRAME)
        self.depthChoice.set(crawl_depth_options[0])
        self.crawl_depth = tk.OptionMenu(self.crawling_depth_FRAME, self.depthChoice,
                                         *crawl_depth_options)
        self.crawl_depth.place(relx = 0.75, rely = 0.5, anchor = tk.CENTER)

        self.parallelChoice = tk.StringVar(self.parallel_process_FRAME)
        self.parallelChoice.set(parallel_instance_options[0])
        self.parallel_instance = tk.OptionMenu(self.parallel_process_FRAME, self.parallelChoice,
                                               *parallel_instance_options)
        self.parallel_instance.place(relx = 0.75, rely = 0.5,
                                     anchor = tk.CENTER)

        # instantiate checkbuttons
        self.noDomesticLinkStatus = tk.IntVar()
        self.contentFilterStatus  = tk.IntVar()
        self.disclaimerStatus     = tk.IntVar()

        no_domestic_link = tk.Checkbutton(self.filter_type_FRAME,
                                          text ="Non-domestic",
                                          variable = self.noDomesticLinkStatus,
                                          bg = "ivory", fg = "black")
        content_filter    = tk.Checkbutton(self.filter_type_FRAME,
                                           text ="Keywords\t",
                                           variable = self.contentFilterStatus,
                                           bg = "ivory", fg = "black",
                                           command = self.enable_filter_file)
        i_agree          = tk.Checkbutton(self.disclaimer_FRAME,
                                          text ="I agree",
                                          variable = self.disclaimerStatus,
                                          bg = "ivory", fg = "black")

        no_domestic_link.pack(side = tk.TOP, anchor = tk.W)
        content_filter.pack(side = tk.BOTTOM, anchor = tk.W)
        i_agree.pack(side = tk.TOP)

        # instantiate textboxes
        self.edgesFilename = tk.Entry(self.edges_filename_FRAME)
        self.edgesFilename.pack()
        self.nodesFilename = tk.Entry(self.nodes_filename_FRAME)
        self.nodesFilename.pack()

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
        if self.edgesFilename.get() == "":
            potentialError.append("- Edges filename is missing")
        if self.nodesFilename.get() == "":
            potentialError.append("- Nodes filename is missing")
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
                str(self.edgesFilename.get() + ".csv"),
                str(self.nodesFilename.get() + ".csv")])


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
        self.executeEdgesFilename  = mainwindow.get_info()[6]
        self.executeNodesFilename  = mainwindow.get_info()[7]

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
        tk.Label(self.frame, text="Edges Filename\t\t: " +
                                  self.executeEdgesFilename).grid(
            row=7, column=0, columnspan=3, sticky = tk.W)
        tk.Label(self.frame, text="Nodes Filename\t\t: " +
                                  self.executeNodesFilename).grid(
            row=8, column=0, columnspan=3, sticky = tk.W)
        tk.Label(self.frame, text="\nContinue?").grid(
            row=9, column=0, columnspan=3, sticky = tk.N)

        thr = threading.Thread(target=multiprocess_crawling,
                               args=(self.executeSeedAddress,
                                     self.executeDepth,
                                     self.executeDomesticFilter,
                                     self.executeParallelChoice,
                                     self.executeEdgesFilename,
                                     self.executeNodesFilename,
                                     self.executeFilterAddress))

        def run_the_crawl():
            back.config(state=tk.DISABLED)
            exitApp.config(state=tk.NORMAL)
            thr.daemon = True

            thr.start()

            messagebox.showinfo(message="Your crawl has finished!\n"
                                        f"Elapsed time = "
                                        f"{config.endTime - config.startTime}")

        run = tk.Button(self.frame, text = "Yes", command = run_the_crawl)

        def back_to_master():
            mainwindow.executeCrawlingButton.config(state=tk.NORMAL)
            self.master.destroy()

        back = tk.Button(self.frame, text = "Back to Previous Window",
                         command = back_to_master)

        def exit_everything():

            config.stopThis = True
            for job in config.jobs:
                job.terminate()
            for bot in config.botsList:
                bot.quit()

            self.master.destroy()
            sys.exit(0)

        exitApp = tk.Button(self.frame, text="Stop Everything",
                            command = exit_everything)
        exitApp.config(state = tk.DISABLED)

        run.grid(     row = 10, column = 0)
        back.grid(  row = 10, column = 1)
        exitApp.grid( row = 10, column = 2)


def main():
    root = tk.Tk()
    root.geometry("350x465")
    root.title("WebCrawler")
    root.resizable(False, False)
    app = MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()
