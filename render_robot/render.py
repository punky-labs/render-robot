import csv
import os, subprocess
import requests
import codecs
from contextlib import closing

from PyQt6.QtCore import QObject, pyqtSignal



class Render(QObject):
    # Define custom signals
    progressed = pyqtSignal(int)
    rendered_file = pyqtSignal(str)
    status_update = pyqtSignal(str)
    finished = pyqtSignal()
    TEST = True

    def __init__(self, ae_path, proj_path, out_path, 
                 comp_prefix, var_path, set_file, 
                 comp_name, csv_name=False,
                 output_module = False, file_ext = '.mp4',
                 num_pad = '0'
                 ):
        super().__init__()
        self._ae_path = ae_path
        self._proj_path = proj_path
        self._out_path = out_path
        if self._out_path == '':
            self._out_path = os.path.dirname(os.path.abspath(self._proj_path))
        self._comp_prefix = comp_prefix
        self._var_path = var_path
        self._set_file = set_file
        self._comp_name = comp_name
        self._csv_name = csv_name
        self._output_module = output_module
        self._file_ext = file_ext
        self._num_pad = num_pad
             

    def renderAE(self, out_name, comp_name, om):
        final_path = '"'+self._ae_path + '\\aerender.exe"'
        final_path += ' -project "' + self._proj_path + '"'
        final_path += ' -comp "' + comp_name + '"' 
        if self._output_module:
            final_path += ' -OMtemplate "' + om + '"'
        final_path += ' -output "' + self._out_path +'\\'+ out_name + self._file_ext + '"'
        if self.TEST:
            print(final_path)
        else:
            render_proc = subprocess.Popen(final_path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for line in render_proc.stdout:
                self.status_update.emit(line.decode("utf-8").rstrip())
                #print(line.decode("utf-8").rstrip())


    def streamCSV(self):
        """Reads CSV data from online URL"""
        count = -1
        with closing(requests.get(self._var_path, stream=False)) as r:
            temp_reader = csv.reader(codecs.iterdecode(r.iter_lines(), 'utf-8'))
            for _ in temp_reader:
                count += 1
        with closing(requests.get(self._var_path, stream=False)) as r:
            csv_reader = csv.reader(codecs.iterdecode(r.iter_lines(), 'utf-8'))
            self.process(csv_reader, count)

    def localCSV(self):
        """Reads CSV data from local file"""
        with open(self._var_path, mode='r') as csv_file:
            reader = csv.reader(csv_file)
            count = sum(1 for _ in reader)
            csv_file.seek(0)
        with open(self._var_path, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            self.process(csv_reader, count-1)

    def process(self, csv_reader, count):
        """"""
        print("Processing {}".format(count))
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                header = row
            else:
                with open(self._set_file, mode='w', newline='') as settings_file:
                    settings_writer = csv.writer(settings_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    settings_writer.writerow(header)
                    settings_writer.writerow(row)
                if self._csv_name:
                    out_name = row[self._comp_prefix]
                else:
                    out_name = self._comp_prefix + str(line_count).rjust(len(self._num_pad), '0')
                full_comp = self._out_path +"\\"+ out_name + ".mp4"
                if self._output_module:
                    om = row[self._output_module]
                else:
                    om = self._output_module
                comp_name = row[self._comp_name]
                self.status_update.emit("Rendering...")
                self.renderAE(out_name, comp_name, om)
                self.rendered_file.emit(full_comp)
                self.status_update.emit("Rendered")
            self.progressed.emit(int(line_count/count*100))
            line_count += 1
        self.status_update.emit(f'Processed {line_count-1} variations.')
        self.finished.emit()


"""
https://docs.google.com/spreadsheets/d/e/2PACX-1vT1g1DxlMTdSBmiaugiCEwsWK8FsFRUNWB4yyUaEZFSWouyGd2EBrHmq2rIC1dxknUIYCNEun31XnYs/pub?gid=0&single=true&output=csv
"""
