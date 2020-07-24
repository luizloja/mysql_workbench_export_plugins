import datetime
# import the wb module
from wb import *
# import the grt module
import grt
# import the mforms module for GUI stuff
import mforms



# define this Python module as a GRT module
ModuleInfo = DefineModule(name= "Migration Rails", author= "Luiz Loja", version="1.0")


class RelationshipCreator(mforms.Form):
  def __init__(self, catalog):
    mforms.Form.__init__(self, None, mforms.FormNormal)

    self.catalog = catalog

    self.set_title("Create Migration for Rails")

    box = mforms.newBox(False)
    self.set_content(box)
    box.set_padding(12)
    box.set_spacing(12)

    label = mforms.newLabel(
"""This is going to create all migration files necessary in Rails application. 
   It also creates a scaffold.txt with scaffold commands to be customized, as you wish my Lord.  
   To use it, you must inform the path where the files will be created and click on Create Files button.""")
    box.add(label, False, True)

    hbox = mforms.newBox(True)
    hbox.set_spacing(12)
    box.add(hbox, False, True)

    label = mforms.newLabel("Path to create:")
    hbox.add(label, False, True)
    self.pattern = mforms.newTextEntry()
    hbox.add(self.pattern, True, True)
    self.browser_file_button = mforms.newButton()
    self.browser_file_button.set_text("...")
    hbox.add(self.browser_file_button, False, True)
    self.browser_file_button.add_clicked_callback(self.choose_directory)
    #self.matchType.set_active(True)
    search = mforms.newButton()
    search.set_text("Create Files")
    search.add_clicked_callback(self.export_porra_toda)
    hbox.add(search, False, True)

    self.pattern.set_value("E:\\18")

    self.candidateTree = mforms.newTreeView(mforms.TreeShowHeader)
    self.candidateTree.add_column(mforms.StringColumnType, "Table", 100, False)
    self.candidateTree.add_column(mforms.StringColumnType, "Column", 100, False)
    self.candidateTree.add_column(mforms.StringColumnType, "Type", 100, False)
    self.candidateTree.add_column(mforms.StringColumnType, "Migration", 100, False)
    self.candidateTree.add_column(mforms.StringColumnType, "Column", 100, False)
    self.candidateTree.add_column(mforms.StringColumnType, "Type", 100, False)
    self.candidateTree.add_column(mforms.StringColumnType, "File", 100, False)    
    self.candidateTree.end_columns()
    box.add(self.candidateTree, True, True)

    hbox = mforms.newBox(True)
    hbox.set_spacing(12)
    self.matchCount = mforms.newLabel("")
    hbox.add(self.matchCount, False, True)
    self.cancelButton = mforms.newButton()
    self.cancelButton.set_text("Cancel")
    hbox.add_end(self.cancelButton, False, True)

    self.okButton = mforms.newButton()
    self.okButton.set_text("Thanks!")
    hbox.add_end(self.okButton, False, True)
    #self.okButton.add_clicked_callback(self.createFKs)
    box.add(hbox, False, True)
    self.component_id = 0
    self.set_size(700, 600)


    
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
    
    
  def findMatches(self):
    candidates = []
    for schema in self.catalog.schemata:
      candidates += get_fk_candidate_list(schema, self.pattern.get_string_value(), self.matchType.get_active())
    self.candidateTree.clear_rows()
    for table, column, ref_table, ref_column in candidates:
      row = self.candidateTree.add_row()
      self.candidateTree.set_string(row, 0, table.name)
      self.candidateTree.set_string(row, 1, column.name)
      self.candidateTree.set_string(row, 2, column.formattedType)
      self.candidateTree.set_string(row, 3, ref_table.name)
      self.candidateTree.set_string(row, 4, ref_column.name)
      self.candidateTree.set_string(row, 5, ref_column.formattedType)
    self.matchCount.set_text("%i matches found" % len(candidates))
 
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
        
  def export_porra_toda(self):
       schema = self.catalog.schemata[0]
       caminho = self.pattern.get_string_value() + "\\" 
       contador_tabela = 0

       
       scaffold = "" 
       for table in schema.tables:
          #print table.inserts.methods
          #print table.foreignKeys.columns
          #print table.name
          #Primary key 
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
          

          data_formatada = self.formatar_data(contador_tabela)

          rails_name= self.camelize(table.name)
          rails_field_name= ""
          rails_format= ""
          file = data_formatada + "_create_" + table.name + ".rb"
          scaffold += "rails generate ext_scaffold " +  table.name + " "
          contador_tabela +=1 
 
          f = open(caminho + file , "w")
          f.write('{"mockup":\n')
          f.write('    {"controls":\n')
          f.write('       {"control":[ \n')

          instrucao_chaves = ""
          quantidade_colunas = len(table.columns) 
          contador = 1
          instrucao_coluna = ""
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

              # rails_format = converted_field
              #  rails_field_name = column.name 
                
              #  if column.name != 'created_at' and  column.name != 'updated_at' and column.name != 'deleted_at':
              #     scaffold += rails_field_name + ":"

              #  self.addRow(column,rails_name,rails_field_name,rails_format,file)

             #   if column.length != -1 :
              #     instrucao_coluna += ", limit:  " + str(column.length)  

             #   if column.isNotNull != 0: 
               #    instrucao_coluna += ", null: false "

           #     if column.defaultValue != '':
               #    instrucao_coluna += ", default: " + column.defaultValue



             #   if dict_fk.get(column.name) != None: 
                #   instrucao_coluna += "\n         t.index :" + column.name + ", name: :index_" + table.name + "_" +  str(contador)  

              #  contador += 1
             

          
          #   if dict_fk.get(column.name) != None: 
               #    instrucao_chaves += "\n         t.foreign_key :" + dict_fk[column.name]['table'] + ", column: :"+ column.name +", primary_key: '"+ dict_fk[column.name]['primary_key'] +"' "              
               #    scaffold +=  "combo[" + dict_fk[column.name]['table'] + ".nome] "    
         #    else:
           #        if column.simpleType != None and column.simpleType.name == 'SET':
             #         campos_check = column.datatypeExplicitParams 
             #         campos_check = campos_check.replace("'", "").replace("(","").replace(")","")
             #         scaffold +=  "check[" + campos_check  + "] "    
           #        else: 
             #         if column.name != 'created_at' and  column.name != 'updated_at' and column.name != 'deleted_at':
             #            scaffold += rails_format + " "  

          
         # contador = 0
          instrucao_coluna +=  '{"ID":"' + str(self.generate_id()) + '","h":"'+str(posicao_y-88)+'","measuredH":"123","measuredW":"109","properties":{"align":"left","size":"10","text":"'+comments+'"},"typeID":"StickyNote","w":"450","x":"567","y":"188","zOrder":"0"},\n'
          instrucao_coluna +=  '{"ID":"' + str(self.generate_id()) + '","measuredH":"21","measuredW":"328","properties":{"text":"'+colunas_grid+"\\n" + dados_dump + "\\n" + dados_dump_2 +'"},"typeID":"DataGrid","x":"583","y":"90","zOrder":"0"},\n'
          instrucao_coluna += '{"ID":"' + str(self.generate_id()) + '","measuredH":"27","measuredW":"62","properties":{"text":"Salvar"},"typeID":"Button","x":"416","y":"'+str(posicao_y+42)+'","zOrder":"1"},\n'
          instrucao_coluna += '{"ID":"' + str(self.generate_id()) + '","measuredH":"27","measuredW":"59","properties":{"text":"Voltar"},"typeID":"Button","x":"147","y":"'+str(posicao_y+42)+'","zOrder":"1"},\n'
          instrucao_coluna += '{"ID":"' + str(self.generate_id()) + '","measuredH":"214","measuredW":"450","properties":{"text":"' + self.humanize(table.name)  + '"},"typeID":"TitleWindow","h":"'+str(posicao_y+10)+'","x":"100","y":"90","zOrder":"0"}'
          f.write("         "+instrucao_coluna+"\n")    
          f.write(']},"measuredH":"453","measuredW":"1199","mockupH":"400","mockupW":"914","version":"1.0"}}\n')
          f.close()
          print("Fim")
        



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
@ModuleInfo.plugin("wb.catalog.util.migrationRails", caption= "Create Migration Files", input= [wbinputs.currentCatalog()], pluginMenu= "Utilities", type="standalone")
@ModuleInfo.export(grt.INT, grt.classes.db_Catalog)
def autoCreateRelationships(catalog):
  form = RelationshipCreator(catalog)
  form.run()
  return 0

autoCreateRelationships(grt.root.wb.doc.physicalModels[0].catalog)