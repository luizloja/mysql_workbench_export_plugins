#Author: Luiz Fernando Batista Loja
#QueryExportPostgresPlugin:
#Generate ddl for postgresql 

#Workbench imports
from wb import *
import grt

#Plugin definition
ModuleInfo = DefineModule(name='QueryExportPostgres', author='Luiz Fernando Batista Loja', version='1.0')
@ModuleInfo.plugin("sample.exportToPostgres",
  caption="Export the ddl to postgres",
  input=[wbinputs.objectOfClass("db.mysql.schema")],
  groups=["Overview/Utility"])
  
@ModuleInfo.export(grt.INT, grt.classes.db_mysql_Schema)

#Formatter
def export_porra_toda(schema):
 


#   f = open("C:\Users\luizloja\AppData\Roaming\MySQL\Workbench\modules\demofile3.txt", "w")
#   f.write("Woops! I have deleted the content!")
#   f.close()

  #-- Drop Tables
 #  for table in schema.tables:
 #     print "drop table " + table.name + " cascade;"

  # create the list of possible foreign keys from the list of tables
   print "--Tables - --------------------------------------"
   for table in schema.tables:
      print "  "
      #print table.inserts.methods
      #print table.foreignKeys.columns
      #print table.name


      instrucao_coluna = "CREATE TABLE " + table.name + " (\n"
      quantidade_colunas = len(table.columns) 
      contador = 1
      for column in table.columns:
         #print column.name
         #print column
         #print column.userType
         if column.autoIncrement == 1:
            instrucao_coluna +=  column.name + " serial " 
         elif column.userType != None:
            instrucao_coluna +=  column.name + " " + column.userType.name + " "   
         elif column.simpleType.name == 'VARCHAR':
            instrucao_coluna += column.name + " " + column.simpleType.name + "(" + str(column.length)  + ")"    
         elif column.simpleType.name == 'SET':
            instrucao_coluna += column.name + " TEXT "    
         else:
            instrucao_coluna += column.name + " " + column.simpleType.name + " "   

         if column.isNotNull != 0: 
            instrucao_coluna += " not null "

         if column.defaultValue != '':
            instrucao_coluna += " DEFAULT " + column.defaultValue

         if column.simpleType != None and column.simpleType.name == 'SET':
            campos_check = column.datatypeExplicitParams 
            instrucao_coluna += " CHECK " + column.name + " in  " + campos_check   

 
         if quantidade_colunas != contador:
             instrucao_coluna += ",\n"
              

         contador += 1

      print (instrucao_coluna + "); ") 
      
#Chaves primarias
   print "--Primary keys - --------------------------------------"
   for table in schema.tables:
     contador_colunas = len(table.primaryKey.columns) 
     contador = 1
     chaves_virgula = ""
     for column in table.primaryKey.columns:
         chaves_virgula += column.referencedColumn.name 
         if contador_colunas != contador:
             chaves_virgula += ","

     instrucao_chave = "ALTER TABLE " + table.name + " ADD  PRIMARY KEY (" + chaves_virgula + "); "
     print instrucao_chave 
   
##Chave estrangei
   print "--Foreign keys - --------------------------------------"
   for table in schema.tables:
     for keys in table.foreignKeys:
         instrucao_completa = "ALTER TABLE " +  table.name + " ADD  FOREIGN KEY ("
         contador_colunas = 1 
         quantidade_colunas =  len(keys.columns) 
         intrucao_campo_chave = ""
         intrucao_tabela = ""
        # print keys 
         for column in keys.columns:
            intrucao_campo_chave += column.name
            if quantidade_colunas != contador_colunas: 
                intrucao_campo_chave += ","
            contador_colunas += 1

         instrucao_completa += intrucao_campo_chave + ") REFERENCES "
         intrucao_campo_chave = ""
         contador_colunas = 1 
         for column in keys.referencedColumns:
            intrucao_campo_chave += column.name
            if quantidade_colunas != contador_colunas: 
                intrucao_campo_chave += ","
            intrucao_tabela = column.owner.name   
         instrucao_completa += intrucao_tabela + "(" + intrucao_campo_chave + ");"

         print instrucao_completa   

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

print "-------------------------"
#print grt.root.wb.doc.physicalModels[0].catalog.schemata[0]
export_porra_toda(grt.root.wb.doc.physicalModels[0].catalog.schemata[0])