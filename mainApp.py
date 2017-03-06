# This file contain code for GUI of application and function calling
# TODO list
# 1. Create GUI for this that take input and classify that as one of mention category.
# 2. Output should be shown at GUI itself.
import tkinter as tk
import pygubu
from processing import SVM
import os


class Application:
    def __init__(self, master):
        #os.chdir('')
        self.master = master
        # 1: Create a builder
        self.builder = builder = pygubu.Builder()

        # 2: Load an ui file
        builder.add_from_file('gui.ui')

        # 3: Create the widget using a master as parent
        self.mainwindow = builder.get_object('main_window', master)

        builder.connect_callbacks(self)

    def on_classify_click(self):
        selected_classifier = self.builder.get_variable('selected_classifier').get()
        selected_size = self.builder.get_variable('selected_size').get()
        isStopCheck  = self.builder.get_variable('selected_stop_word').get()
        # print(selected_classifier, selected_size,isStopCheck)

        if selected_classifier!='' and selected_size!='' and isStopCheck!='':

            error_label = self.builder.get_variable('error_message')
            error_label.set('')

            if selected_classifier == 'Support_Vector_Machine(SVM)':
                accuracy =  SVM.perform(isStopCheck,selected_size)

            out_classifier_label = self.builder.get_variable('classifier_ans')
            out_classifier_label.set(selected_classifier)

            out_stop_label = self.builder.get_variable('stop_word_ans')
            out_stop_label.set(isStopCheck)

            out_accuracy_label = self.builder.get_variable('accuracy_ans')
            out_accuracy_label.set(accuracy)

        elif selected_classifier =='':
            error_label = self.builder.get_variable('error_message')
            error_label.set('Please select Classifier !!')
        elif selected_size=='':
            error_label = self.builder.get_variable('error_message')
            error_label.set('Please select training Size !!')
        elif isStopCheck=='':
            error_label = self.builder.get_variable('error_message')
            error_label.set("Please Select stop word condition !!")
        else:
            error_label = self.builder.get_variable('error_message')
            error_label.set("Please Select valid Input !!")

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Document Classifier')
    app = Application(root)
    root.mainloop()




