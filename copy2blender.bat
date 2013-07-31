::
:: Utility for copying MH scripts to Blenders addon folder
:: Usage:
:: 
::     copy2blender path\to\addons\folder

echo Copy files to %1

copy .\tools\blender26x\mhx_importer\*.py %1

mkdir %1\makeclothes
copy .\tools\blender26x\makeclothes\*.py %1\makeclothes
mkdir %1\makeclothes\targets
copy .\tools\blender26x\makeclothes\targets\*.target %1\makeclothes\targets

mkdir %1\maketarget
copy .\tools\blender26x\maketarget\*.py %1\maketarget
mkdir %1\makeclothes\data
copy .\tools\blender26x\maketarget\data\*.obj %1\maketarget\data
copy .\tools\blender26x\maketarget\data\*.mhclo %1\maketarget\data

mkdir %1\mh_mocap_tool
copy .\tools\blender26x\mh_mocap_tool\*.py %1\mh_mocap_tool
copy .\tools\blender26x\mh_mocap_tool\*.json %1\mh_mocap_tool
mkdir %1\mh_mocap_tool\target_rigs
copy .\tools\blender26x\mh_mocap_tool\target_rigs\*.trg %1\mh_mocap_tool\target_rigs
mkdir %1\mh_mocap_tool\source_rigs
copy .\tools\blender26x\mh_mocap_tool\source_rigs\*.src %1\mh_mocap_tool\source_rigs

echo All files copied




