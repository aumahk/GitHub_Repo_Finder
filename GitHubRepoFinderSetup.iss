[Setup]
AppName=GitHub Repo Finder
AppVersion=1.2.2
DefaultDirName={autopf}\GitHubRepoFinder
DefaultGroupName=GitHub Repo Finder
OutputBaseFilename=GitHubRepoFinderSetup
Compression=lzma
SolidCompression=yes
SetupIconFile=icon.ico

[Files]
Source: "dist\GitHubRepoFinder.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\GitHub Repo Finder"; Filename: "{app}\GitHubRepoFinder.exe"
Name: "{autodesktop}\GitHub Repo Finder"; Filename: "{app}\GitHubRepoFinder.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional icons:"
