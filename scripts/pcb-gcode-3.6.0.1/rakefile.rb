# _*_ Mode: Ruby -*-
#
# Rakefile for pcb-gcode.
#
require 'pp'

# this will be improved later
PCB_GCODE_VERSION = "3.6.0.1"

RELEASE_FILE = "~/Documents/pcb-gcode-#{PCB_GCODE_VERSION}.zip"

ignore_files = ['pcb_gcode_is_setup', '*.old', 'storage.nv',
  'make/*', 'make', '*.b#*', '*.s#*', '*.l#*',
  '*.DS_Store', 'optomize_me.txt']

desc "Build the docs/readme.html file."
file 'docs/readme.html' => 'docs/readme.textile' do |t|
  system "redcloth #{t.prerequisites[0]} >#{t.name}"
end

desc "Create the .zip file to be released."
task :release_file do
  zip_cmd = "zip -r ~/Documents/pcb-gcode-#{PCB_GCODE_VERSION}.zip *"
  zip_cmd += ' -x '
  zip_cmd += ignore_files.join(' -x ')
  system(zip_cmd)
end

desc "Copy current settings/* files to the safe_options folder."
task :safe_options do
  SAFE_OPTIONS = ['pcb-defaults', 'pcb-machine', 'pcb-gcode-options', 'user-gcode']
  SAFE_OPTIONS.each do |name|
    cp 'settings/' + name + '.h', 'safe_options/' + name + '.release.h'
  end
end

desc "Recreate data folders for viewers. Usually after re-exporting from Processing."
task :fix_viewers do
  system("cp -R viewer/data viewer/applet")
  system("cp -R viewer/data viewer/application.linux/")
  system("cp -R viewer/data viewer/application.macosx/")
  system("cp -R viewer/data viewer/application.windows/")
end

desc "Write the convert units function in pcb-gcode-setup.ulp."
task :write_convert_units do
  system("make/write_convert_units.rb")
end

task :default => ['docs/readme.html', :fix_viewers, :safe_options, :release_file] do
end
