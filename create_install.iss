; Script generated by the Inno Script Studio Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "EStarter"
#define MyAppVersion "V1.2.0"
#define MyAppPublisher "blindelectron"
#define MyAppURL "https://blind-electron.ml"
#define MyAppExeName "estarter.exe"


[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{812C84CF-39BB-426A-B185-AC2F12D6AB35}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={pf}\estarter
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile={#SourcePath}\LICENSE
OutputDir={#SourcePath}\estarter.dist
OutputBaseFilename=setup
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 0,6.1

[Files]
Source: "{#SourcePath}\estarter.dist\estarter.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SourcePath}\estarter.dist\accessible_output2\*"; DestDir: "{app}\accessible_output2"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#SourcePath}\estarter.dist\psutil\*"; DestDir: "{app}\accessible_output2"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#SourcePath}\estarter.dist\numpy\*"; DestDir: "{app}\accessible_output2"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#SourcePath}\estarter.dist\certifi\*"; DestDir: "{app}\certifi"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#SourcePath}\estarter.dist\s\*"; DestDir: "{app}\s"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#SourcePath}\estarter.dist\sound_lib\*"; DestDir: "{app}\sound_lib"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#SourcePath}\estarter.dist\config_default.ini"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SourcePath}\estarter.dist\np.cf"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SourcePath}\estarter.dist\*.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SourcePath}\estarter.dist\*.dll"; DestDir: "{app}"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:ProgramOnTheWeb,{#MyAppName}}"; Filename: "{#MyAppURL}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
