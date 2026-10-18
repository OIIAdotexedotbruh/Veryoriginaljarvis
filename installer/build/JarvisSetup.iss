; Inno Setup 6 – J.A.R.V.I.S. Setup
; Auf Windows: iscc installer/build/JarvisSetup.iss
; Erzeugt: installer/dist/JARVIS-Setup-v1.0.49.exe
#define MyAppName "J.A.R.V.I.S."
#define MyAppVersion "1.0.49"
#define MyAppPublisher "Stark Industries"
#define MyAppURL "https://github.com/OIIAdotexedotbruh/Veryoriginaljarvis"

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-1234567890AB}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
DefaultDirName={localappdata}\Programs\JARVIS
DisableDirPage=no
DefaultGroupName=JARVIS
AllowNoIcons=yes
LicenseFile=..\..\README.md
OutputDir=..\dist
OutputBaseFilename=JARVIS-Setup-v1.0.49
Compression=lzma
SolidCompression=yes
WizardStyle=modern
SetupIconFile=arc.ico
UninstallDisplayIcon={app}\JARVIS.exe
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

[Languages]
Name: "german"; MessagesFile: "compiler:Languages\German.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "autostart"; Description: "Beim Windows-Start starten (wie in YouTube Videos)"; GroupDescription: "Autostart:"; Flags: unchecked

[Files]
Source: "..\dist\JARVIS-Setup.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\..\web-preview\*"; DestDir: "{app}\web-preview"; Flags: ignoreversion recursesubdirs
Source: "..\..\docs\QUALITATIVER_FRAGEBOGEN.md"; DestDir: "{app}\docs"; Flags: ignoreversion

[Icons]
Name: "{group}\J.A.R.V.I.S."; Filename: "{app}\JARVIS-Setup.exe"; IconFilename: "{app}\JARVIS-Setup.exe"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\J.A.R.V.I.S."; Filename: "{app}\JARVIS-Setup.exe"; Tasks: desktopicon; IconFilename: "{app}\JARVIS-Setup.exe"

[Registry]
Root: HKCU; Subkey: "SOFTWARE\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "JARVIS"; ValueData: """{app}\JARVIS-Setup.exe"""; Tasks: autostart; Flags: uninsdeletevalue

[Run]
Filename: "{app}\JARVIS-Setup.exe"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}\web-preview"
