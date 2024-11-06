import tkinter

from marking_plan import MarkingPlan
from mp_reader import MPReader
from mp_writer import MPWriter

from data_layer import DataLayer
from dl_builder import DLBuilder

def build_data_layer(url):
	fname = 'xls/' + url.split('/')[2].replace('.', '_').replace('/', '_') + "_plan.xlsx"
	print(fname)
	
	writer = MPWriter()
	writer.build(fname, url)
	mp = writer.render()
	
	reader = MPReader()
	reader.build(fname)
	marking = reader.render()
	
	dl = DLBuilder()
	dl.build(marking)
	layers = dl.render_all()
	writer.write_dl(dl)
	
	print("Généré !")
	
	return layers
	
def get_file_name(url):
	return 'xls/' + url.split('/')[2].replace('.', '_').replace('/', '_') + "_plan.xlsx"