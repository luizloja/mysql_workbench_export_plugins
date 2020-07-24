import datetime
# import the wb module
from wb import *
# import the grt module
import grt

from grt.modules import Workbench
from wb import wbinputs
from wb_utils_grt import ModuleInfo
# import the mforms module for GUI stuff
import mforms



# define this Python module as a GRT module
ModuleInfo = DefineModule(name= "Migration Rails", author= "Luiz Loja", version="1.0")


class RelationshipCreator(mforms.Form):
  def __init__(self, catalog):
    mforms.Form.__init__(self, None, mforms.FormNormal)

    self.catalog = catalog

    self.set_title("Mockup Copy Successful")

    box = mforms.newBox(False)
    self.set_content(box)
    box.set_padding(12)
    box.set_spacing(12)

    label = mforms.newLabel("Click on Copy to Copy!")
    box.add(label, False, True)


    hbox = mforms.newBox(True)
    hbox.set_spacing(12)
    self.matchCount = mforms.newLabel("")
    hbox.add(self.matchCount, False, True)
    self.cancelButton = mforms.newButton()
    self.cancelButton.set_text("Cancel")
    hbox.add_end(self.cancelButton, False, True)

    self.okButton = mforms.newButton()
    self.okButton.set_text("Copy, buddy!")
    hbox.add_end(self.okButton, False, True)
    self.okButton.add_clicked_callback(self.export_table_clipboard)
    box.add(hbox, False, True)
    self.component_id = 0
    self.set_size(233,144 )




  def export_table_clipboard(self):	
	  #print table.inserts.methods
	  #print table.foreignKeys.columns
	  #print table.name
	  #Primary key 
	  table = self.catalog
	  dict_pk = {}
	  for column in table.primaryKey.columns:
		  dict_pk[column.referencedColumn.name] = 1

	  no_default_key = ""
	  if dict_pk.get('id') == None or len(table.primaryKey.columns) > 1:
		  no_default_key = ",{id: false} "


	  #foreign key 
	  dict_fk = {}
	  for keys in table.foreignKeys:
		 quantidade_colunas =  len(keys.columns) 
		 maiu_column = ""
		# if it dos have more than one column the code is broken
		 for column in keys.columns:
			dict_fk[column.name] = {}
			maiu_column = column.name

		 for column in keys.referencedColumns:
			dict_fk[maiu_column]['primary_key'] = column.name
			dict_fk[maiu_column]['table'] =  column.owner.name   
	  


	  rails_name= self.camelize(table.name)
	  rails_field_name= ""
	  rails_format= ""

	  instrucao_coluna =  '{"mockup":\n'
	  instrucao_coluna += '    {"controls":\n'
	  instrucao_coluna += '       {"control":[ \n'

	  instrucao_chaves = ""
	  quantidade_colunas = len(table.columns) 
	  contador = 1
	  posicao_x = 108 
	  posicao_y = 124
	  tamanho_label_x = 56
	  posicao_x_inputs = 251
	  colunas_grid = "" 
	  dados_dump = ""
	  dados_dump_2 = ""
	  comments = ""
	  for column in table.columns:
		 #print   column
		 #print   column.name 
		 #print   dict.get(column.name) 
		 converted_field = self.convert_migration_type(column)
		 if column.name != 'created_at' and  column.name != 'updated_at' and column.name != 'deleted_at' and column.name != 'id':
			instrucao_coluna += '{"ID":"'+ str(self.generate_id()) +'","measuredH":"21","measuredW":"' + str(tamanho_label_x) + '","properties":{"text":"' + self.humanize(column.name) + ': "},"typeID":"Label","x":"' + str(posicao_x) + '","y":"' + str(posicao_y) + '","zOrder":"1"}, \n' 
			colunas_grid += self.humanize(column.name) + " ^v,"

			if column.comment != None and column.comment != '' : 
			   comments += column.name + ": " + column.comment + "\\n"

			if dict_fk.get(column.name) == None:
			   if converted_field == "TextInput":
				   instrucao_coluna += '{"ID":"'+ str(self.generate_id()) +'","measuredH":"27","measuredW":"200","properties":{"text":""},"typeID":"TextInput","w":"283", "x":"'+ str(posicao_x_inputs) +'","y":"'+ str(posicao_y - 3 ) +'","zOrder":"1"},\n'
				   dados_dump += "Dado qualquer ," 
				   dados_dump_2 += "Dado 2 ," 
			   elif converted_field == "ComboBox":
				   instrucao_coluna += '{"ID":"'+ str(self.generate_id()) +'","measuredH":"27","measuredW":"200","properties":{"text":""},"typeID":"ComboBox","w":"283", "x":"'+ str(posicao_x_inputs) +'","y":"'+ str(posicao_y - 3 ) +'","zOrder":"1"},\n'
				   dados_dump += "Dado ," 
				   dados_dump_2 += "Dado Combo ," 
			   elif converted_field == "DateChooser":
				   instrucao_coluna += '{"ID":"'+ str(self.generate_id()) +'","measuredH":"27","measuredW":"200","properties":{"text":"  /  /    "},"typeID":"DateChooser","w":"148", "x":"'+ str(posicao_x_inputs) +'","y":"'+ str(posicao_y - 3 ) +'","zOrder":"1"},\n'
				   dados_dump += "25/08/2020 ," 
				   dados_dump_2 += "11/04/2010 ," 
			   elif converted_field == "NumericStepper":
				   instrucao_coluna += '{"ID":"'+ str(self.generate_id()) +'","measuredH":"27","measuredW":"200","properties":{"text":""},"typeID":"NumericStepper","w":"148", "x":"'+ str(posicao_x_inputs) +'","y":"'+ str(posicao_y - 3 ) +'","zOrder":"1"},\n'
				   dados_dump += "42 ," 
				   dados_dump_2 += "3.1418 ," 
			   elif converted_field == "CheckBox":
				   instrucao_coluna += '{"ID":"'+ str(self.generate_id()) +'","measuredH":"27","measuredW":"200","properties":{"text":""},"typeID":"CheckBox", "x":"'+ str(posicao_x_inputs) +'","y":"'+ str(posicao_y - 3 ) +'","zOrder":"1"},\n'
				   dados_dump += "Sim ," 
				   dados_dump_2 += "Nao ," 
			   elif converted_field == "TextArea":
				   instrucao_coluna += '{"ID":"'+ str(self.generate_id()) +'","measuredH":"10","measuredW":"100","typeID":"HRule","w":"283","x":"251","y":"'+ str(posicao_y + 4 ) +'","zOrder":"1"},'
				   instrucao_coluna += '{"ID":"'+ str(self.generate_id()) +'","measuredH":"27","measuredW":"200","properties":{"text":""},"typeID":"TextArea", "w":"416","h":"100" ,"x":"117","y":"'+ str(posicao_y + 21 ) +'","zOrder":"1"},\n'
				   posicao_y += 100
				   dados_dump += "Texto Longo ," 
				   dados_dump_2 += "Texto Curto ," 
			else:
			   instrucao_coluna += '{"ID":"'+ str(self.generate_id()) +'","measuredH":"27","measuredW":"200","properties":{"text":""},"typeID":"ComboBox","w":"283", "x":"'+ str(posicao_x_inputs) +'","y":"'+ str(posicao_y - 3 ) +'","zOrder":"1"},\n' 
			   dados_dump += "Dado ," 
			   dados_dump_2 += "Dado ," 

			posicao_y += 30

	  instrucao_coluna +=  '{"ID":"' + str(self.generate_id()) + '","h":"'+str(posicao_y-88)+'","measuredH":"123","measuredW":"109","properties":{"align":"left","size":"10","text":"'+comments+'"},"typeID":"StickyNote","w":"450","x":"567","y":"188","zOrder":"0"},\n'
	  instrucao_coluna +=  '{"ID":"' + str(self.generate_id()) + '","measuredH":"21","measuredW":"328","properties":{"text":"'+colunas_grid+"\\n" + dados_dump + "\\n" + dados_dump_2 +'"},"typeID":"DataGrid","x":"583","y":"90","zOrder":"0"},\n'
	  instrucao_coluna += '{"ID":"' + str(self.generate_id()) + '","measuredH":"27","measuredW":"62","properties":{"text":"Salvar"},"typeID":"Button","x":"416","y":"'+str(posicao_y+42)+'","zOrder":"1"},\n'
	  instrucao_coluna += '{"ID":"' + str(self.generate_id()) + '","measuredH":"27","measuredW":"59","properties":{"text":"Voltar"},"typeID":"Button","x":"147","y":"'+str(posicao_y+42)+'","zOrder":"1"},\n'
	  instrucao_coluna += '{"ID":"' + str(self.generate_id()) + '","measuredH":"214","measuredW":"450","properties":{"text":"' + self.humanize(table.name)  + '"},"typeID":"TitleWindow","h":"'+str(posicao_y+10)+'","x":"100","y":"90","zOrder":"0"}\n'
	  instrucao_coluna += ']},"measuredH":"453","measuredW":"1199","mockupH":"400","mockupW":"914","version":"1.0"}}\n'
	  Workbench.copyToClipboard(instrucao_coluna)



    
  def mapa_type_match(self):
    return  {
    'INT': 'NumericStepper',
    'VARCHAR': 'TextInput', 
    'DECIMAL': 'NumericStepper', 
    'DATE': 'DateChooser', 
    'DATETIME': 'DateChooser', 
    'BLOB': 'TextInput', 
    'BINARY': 'TextInput', 
    'LONGBLOB': 'TextInput', 
    'MEDIUMBLOB': 'TextInput', 
    'TINYBLOB': 'TextInput', 
    'VARBINARY': 'TextInput', 
    'DATETIME': 'DateChooser', 
    'TIME': 'Time', 
    'TIMESTAMP': 'Time', 
    'YEAR': 'DateChooser', 
    'BIGINT': 'NumericStepper', 
    'DOUBLE': 'NumericStepper', 
    'FLOAT': 'NumericStepper', 
    'REAL': 'NumericStepper', 
    'MEDIUMINT': 'NumericStepper', 
    'SMALLINT': 'NumericStepper', 
    'TINYINT': 'NumericStepper', 
    'CHAR': 'TextInput', 
    'NVARCHAR': 'TextArea', 
    'LONGTEXT': 'TextArea', 
    'MEDIUMTEXT': 'TextArea', 
    'TEXT': 'TextArea', 
    'TINYTEXT': 'TextArea', 
    'BIT': 'CheckBox', 
    'BOOLEAN': 'CheckBox', 
    'boolean': 'CheckBox', 
    'ENUM': 'ComboBox', 
    'SET':  'ComboBox'
    }
    
    
 
  def choose_directory(self):
      file_chooser = mforms.newFileChooser(self,3,1)
      file_chooser.set_title("Choose a directory!")
      file_chooser.run_modal()
      self.pattern.set_value(file_chooser.get_path())



  def addRow(self,column,rails_name,rails_field_name,rails_format,file):
      row = self.candidateTree.add_node()
      row.set_string(0, column.owner.name)
      row.set_string(1, column.name)
      row.set_string(2, column.formattedType)
      row.set_string(3, rails_name)
      row.set_string(4, rails_field_name)
      row.set_string(5, rails_format)
      row.set_string(6, file)        

  def generate_id(self):
       self.component_id += 1
       return self.component_id 

  def humanize(self,palavra):
        nome_completo = ""
        for palavra in palavra.split("_"):
            if palavra != 'id': 
               nome_completo += " " +  palavra.capitalize() 

        return nome_completo 
        
  def agrupar_nome_virgula (self,colunas, tipo='column', simbolo=0):
        contador_colunas = 1 
        quantidade_colunas =  len(colunas) 
        intrucao_campo_chave = ""
        dois_pontos = ":"
        if simbolo == 0:
            dois_pontos = "" 
        for column in colunas:
            if tipo == 'column':     
               intrucao_campo_chave += dois_pontos + column.name
            elif tipo == 'referencedColumn':     
               intrucao_campo_chave += dois_pontos + column.referencedColumn.name

            if quantidade_colunas != contador_colunas: 
               intrucao_campo_chave += ","
            contador_colunas += 1 
        return  intrucao_campo_chave      

  def camelize (self,palavra):
        nome_completo = ""
        for palavra in palavra.split("_"):
            nome_completo += palavra.capitalize()
        return nome_completo 

  def formatar_data(self, count=0):
        tempo = datetime.datetime.now()
        return str(int(tempo.strftime("%Y%m%d%H%M%S")) + count)    
    
    
  def convert_migration_type (self, column):

        mapa_type = self.mapa_type_match()    

        if column.userType != None:
           return mapa_type.get(column.userType.name)
        elif mapa_type.get(column.simpleType.name) != None:    
           return mapa_type.get(column.simpleType.name)    
        else:
           return 'TextInput'       

  def run(self):
    self.run_modal(self.okButton, self.cancelButton)


    
    

ModuleInfo = DefineModule(name= "MigrationsRails", author= "Luiz Loja", version="1.0")
@ModuleInfo.plugin('wb.util.copySQLToClipboard', caption='Balsamiq Mockup JSON', input= [wbinputs.objectOfClass('db.DatabaseObject')], groups= ['Catalog/Utilities', 'Menu/Objects'], accessibilityName="Balsamiq Mockup JSON")
@ModuleInfo.export(grt.INT, grt.classes.GrtNamedObject)
def autoCreateRelationships(catalog):
  form = RelationshipCreator(catalog)
  form.run()
  return 0

