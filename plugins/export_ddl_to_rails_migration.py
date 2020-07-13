#Author: Luiz Fernando Batista Loja
#QueryExportPostgresPlugin:
#Generate ddl for postgresql 

#Workbench imports
from wb import *
import grt
import datetime

#Plugin definition
ModuleInfo = DefineModule(name='QueryExportPostgres', author='Luiz Fernando Batista Loja', version='1.0')
@ModuleInfo.plugin("sample.exportToPostgres",
  caption="Export the ddl to postgres",
  input=[wbinputs.objectOfClass("db.mysql.schema")],
  groups=["Overview/Utility"])
  
@ModuleInfo.export(grt.INT, grt.classes.db_mysql_Schema)



#Formatter
def export_porra_toda(schema):
 

  




  # create the list of possible foreign keys from the list of tables
   print "--Tables - --------------------------------------"
   for table in schema.tables:
      print "  "
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







      f = open("C:\Users\luizloja\AppData\Roaming\MySQL\Workbench\modules\migration\\" + formatar_data() + "_create_" + table.name + ".rb", "w")
      f.write("class Create" + camelize(table.name) + " < ActiveRecord::Migration[5.1]\n")
      f.write("   def change\n")
      f.write("      create_table :" +table.name + no_default_key  + " do |t|\n")
      
      
      quantidade_colunas = len(table.columns) 
      contador = 1
      for column in table.columns:
         #print   column
         #print   column.name 
         #print   dict.get(column.name) 
         converted_field = convert_migration_type(column)
         instrucao_coluna = "" 
         if dict_pk.get(column.name) == None or  (dict_pk.get(column.name) != None and no_default_key != ""):

            if dict_pk.get(column.name) != None:
               instrucao_coluna += "t.primary_key :" + column.name + ", :" + converted_field
            else:
               instrucao_coluna += "t." + converted_field + " :" + column.name 

            if column.length != -1 :
               instrucao_coluna += ", limit:  " + str(column.length)  

            if column.isNotNull != 0: 
               instrucao_coluna += ", null: false "

            if column.defaultValue != '':
               instrucao_coluna += ", default: " + column.defaultValue
         


            if dict_fk.get(column.name) != None: 
               instrucao_coluna = "t.foreign_key :" + dict_fk[column.name]['table'] + ", column: :"+ column.name +", primary_key: '"+ dict_fk[column.name]['primary_key'] +"' "
              

            contador += 1
            f.write("         "+instrucao_coluna+"\n")

      f.write("      end\n")
      f.write("   end\n")
      f.write("end\n")
      f.close()

   
##Chave estrangei
   print "--Foreign keys - --------------------------------------"


##Indices unicos
   print "--Unique INDEX - --------------------------------------"
   for table in schema.tables:
      for indice in table.indices:
         if indice.indexType == 'UNIQUE':
           # intrucao_tabela = "ALTER TABLE " + table.name + " ADD CONSTRAINT " + indice.name + " UNIQUE ("
            intrucao_tabela = "ALTER TABLE " + table.name + " ADD  UNIQUE ("
            colunas_index = agrupar_nome_virgula(indice.columns,'referencedColumn')
            intrucao_tabela += colunas_index + ");"
            print intrucao_tabela 

#Metodos 
def agrupar_nome_virgula (colunas, tipo='column'):
    contador_colunas = 1 
    quantidade_colunas =  len(colunas) 
    intrucao_campo_chave = ""
    for column in colunas:
        if tipo == 'column':     
           intrucao_campo_chave += column.name
        elif tipo == 'referencedColumn':     
           intrucao_campo_chave += column.referencedColumn.name

        if quantidade_colunas != contador_colunas: 
           intrucao_campo_chave += ","
        contador_colunas += 1 
    return  intrucao_campo_chave


def camelize (palavra):
	nome_completo = ""
	for palavra in palavra.split("_"):
		nome_completo += palavra.capitalize()
	return nome_completo 

def formatar_data():
    x = datetime.datetime.now()
    return x.strftime("%Y%m%d%H%M%S")

def convert_migration_type (column):
    if column.userType != None:
       return column.userType.name
    elif mapa_type.get(column.simpleType.name) != None:    
       return mapa_type.get(column.simpleType.name)    
    else:
       return 'text'




print "-------------------------"
mapa_type = {
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
#print grt.root.wb.doc.physicalModels[0].catalog.schemata[0]
export_porra_toda(grt.root.wb.doc.physicalModels[0].catalog.schemata[0])