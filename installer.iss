[Setup]
AppName=Python Fences
AppVersion=1.0.0
AppVerName=Python Fences 1.0.0
VersionInfoVersion=1.0.0
VersionInfoCompany=Your Company
VersionInfoCopyright=© 2024 Your Name
VersionInfoProductName=Python Fences
VersionInfoProductVersion=1.0.0
WizardStyle=modern
DefaultDirName={autopf}\Python Fences
DefaultGroupName=Python Fences
UninstallDisplayIcon={app}\fence_icon.ico
OutputDir=installer
OutputBaseFilename=PythonFences_Setup
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\PythonFences.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Python Fences"; Filename: "{app}\PythonFences.exe"
Name: "{commondesktop}\Python Fences"; Filename: "{app}\PythonFences.exe"

[Run]
Filename: "{app}\PythonFences.exe"; Description: "Launch Python Fences"; Flags: nowait postinstall skipifsilent 