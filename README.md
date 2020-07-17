# mysql_workbench_export_plugins
I loved the Mysql Workbench tool, nevertheless I was never a big mysql fan. So I decided to create a project to develop some plugins to export from Mysql Workbench to other plataforms as postgres, rails migration and laravel migration

## What does it?
This plugin generates all migration files for Rails based on the relational model. 
It also creates a scaffold file with all scaffolds commands.
It makes sure that no body will ever forget that foreign key ;).

### Installation
1. Download export_ddl_to_rails_migration.py
2. In MySQL Workbench, click the Scripting menu > Install Plugin/Module...
3. Find and choose export_ddl_to_rails_migration.py and click Open
4. Restart MySQL Workbench

### Usage
1. Open a schem 
2. Click on Tools -> Utilities -> Create Migration Files
3. A Window will open
4. Select the place where your files will be created at ...
5. Click on Create Files button
6. Cheers, that's it dude :)

### Known Issues
1. It only exports the first schem 
2. It exports tables, primary and foreign keys, index and some constraints as unique
3. The plugin for generate postgres ddls is ready, however I didn't have time to adapt it to a form.
