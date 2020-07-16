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

    self.pattern.set_value("C:\\")

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

    self.set_size(700, 600)

    
  def mapa_type_match(self):
    return  {
    'INT': 'integer',
    'VARCHAR': 'string', 
    'DECIMAL': 'decimal', 
    'DATETIME': 'timestamp', 
    'BLOB': 'binary', 
    'BINARY': 'binary', 
    'LONGBLOB': 'binary', 
    'MEDIUMBLOB': 'binary', 
    'TINYBLOB': 'binary', 
    'VARBINARY': 'binary', 
    'DATETIME': 'timestamp', 
    'TIME': 'timestamp', 
    'TIMESTAMP': 'timestamp', 
    'YEAR': 'date', 
    'BIGINT': 'integer', 
    'DOUBLE': 'float', 
    'FLOAT': 'float', 
    'REAL': 'float', 
    'MEDIUMINT': 'integer', 
    'SMALLINT': 'integer', 
    'TINYINT': 'integer', 
    'CHAR': 'string', 
    'NVARCHAR': 'string', 
    'LONGTEXT': 'text', 
    'MEDIUMTEXT': 'text', 
    'TEXT': 'text', 
    'TINYTEXT': 'text', 
    'BIT': 'boolean', 
    'BOOLEAN': 'boolean', 
    'ENUM': 'text', 
    'SET':  'string'
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
        
        
  def export_porra_toda(self):
       schema = self.catalog.schemata[0]
       caminho = self.pattern.get_string_value() + "\\" 
       contador_tabela = 0
      # create the list of possible foreign keys from the list of tables
       print "--Tables - --------------------------------------"
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
          f.write("class Create" + rails_name + " < ActiveRecord::Migration[5.1]\n")
          f.write("   def change\n")
          f.write("      create_table :" +table.name + no_default_key  + " do |t|\n")

          
          instrucao_chaves = ""
          quantidade_colunas = len(table.columns) 
          contador = 1
          for column in table.columns:
             #print   column
             #print   column.name 
             #print   dict.get(column.name) 
             converted_field = self.convert_migration_type(column)

             instrucao_coluna = "" 
             if dict_pk.get(column.name) == None or  (dict_pk.get(column.name) != None and no_default_key != ""):

                if dict_pk.get(column.name) != None:
                   instrucao_coluna += "t.primary_key :" + column.name + ", :" + converted_field
                else:
                   instrucao_coluna += "t." + converted_field + " :" + column.name 

                rails_format = converted_field
                rails_field_name = column.name 
                
                if column.name != 'created_at' and  column.name != 'updated_at' and column.name != 'deleted_at':
                   scaffold += rails_field_name + ":"

                self.addRow(column,rails_name,rails_field_name,rails_format,file)

                if column.length != -1 :
                   instrucao_coluna += ", limit:  " + str(column.length)  

                if column.isNotNull != 0: 
                   instrucao_coluna += ", null: false "

                if column.defaultValue != '':
                   instrucao_coluna += ", default: " + column.defaultValue



                if dict_fk.get(column.name) != None: 
                   instrucao_coluna += "\n         t.index :" + column.name + ", name: :index_" + table.name + "_" +  str(contador)  

                contador += 1
                f.write("         "+instrucao_coluna+"\n")
             

             
             if dict_fk.get(column.name) != None: 
                   instrucao_chaves += "\n         t.foreign_key :" + dict_fk[column.name]['table'] + ", column: :"+ column.name +", primary_key: '"+ dict_fk[column.name]['primary_key'] +"' "              
                   scaffold +=  "combo[" + dict_fk[column.name]['table'] + ".nome] "    
             else:
                   if column.simpleType != None and column.simpleType.name == 'SET':
                      campos_check = column.datatypeExplicitParams 
                      campos_check = campos_check.replace("'", "").replace("(","").replace(")","")
                      scaffold +=  "check[" + campos_check  + "] "    
                   else: 
                      if column.name != 'created_at' and  column.name != 'updated_at' and column.name != 'deleted_at':
                         scaffold += rails_format + " "  

          
          contador = 0
          for indice in table.indices:
             if indice.indexType == 'UNIQUE':
                colunas_index =  self.agrupar_nome_virgula(indice.columns,'referencedColumn',1) 
                f.write("         t.index [" + colunas_index + "], unique: true, name: :" + table.name + "_index_u_" + str(contador) + "\n" )
                contador += 1 


          f.write("      end\n")
          f.write("   end\n")
          f.write("end\n")
          f.close()

          if  instrucao_chaves != "":
             f = open(caminho + self.formatar_data(contador_tabela+ len(schema.tables) + 1 ) + "_change_" + table.name + ".rb", "w")
             f.write("class Change" + self.camelize(table.name) + " < ActiveRecord::Migration[5.1]\n")
             f.write("   def change\n")
             f.write("      change_table :" +table.name + no_default_key  + " do |t|\n")
             f.write(instrucao_chaves + "\n")
             f.write("      end\n")
             f.write("   end\n")
             f.write("end\n")
             f.close()
          scaffold += "\n"
         

       f = open(caminho + "scaffolds.txt", "w")
       f.write("#scaffolds\n")
       f.write(scaffold)
       f.close()


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
           return column.userType.name
        elif mapa_type.get(column.simpleType.name) != None:    
           return mapa_type.get(column.simpleType.name)    
        else:
           return 'text'       

  def run(self):
    
    self.run_modal(self.okButton, self.cancelButton)


    
    

ModuleInfo = DefineModule(name= "MigrationsRails", author= "Luiz Loja", version="1.0")
@ModuleInfo.plugin("wb.catalog.util.migrationRails", caption= "Create Migration Files", input= [wbinputs.currentCatalog()], pluginMenu= "Utilities", type="standalone")
@ModuleInfo.export(grt.INT, grt.classes.db_Catalog)
def autoCreateRelationships(catalog):
  form = RelationshipCreator(catalog)
  form.run()
  return 0

