------Command selection lock
local	gs_lockselectioncommand = command.create ("Guerilleros|Permission|Selection Lock ", nil, "")
function gs_lockselectioncommand:isenabled ()
	return tonumber(os.getenv("GUERILLA_POWER_USER"))==1
end

function gs_lockselectioncommand:action ()
	gs_setselectionpermission(false)
end

------Command selection Unlock
local	gs_unlockselectioncommand = command.create ("Guerilleros|Permission|Selection Unlock ", nil, "")
function gs_unlockselectioncommand:isenabled ()
	return tonumber(os.getenv("GUERILLA_POWER_USER"))==1
end

function gs_unlockselectioncommand:action ()
	gs_setselectionpermission(true)
end

------Command Lock Materials
local	gs_lockmaterialcommand = command.create ("Guerilleros|Permission|Materials Lock", nil, "")
function gs_lockmaterialcommand:isenabled ()
	return tonumber(os.getenv("GUERILLA_POWER_USER"))==1
end

function gs_lockmaterialcommand:action ()
	gs_setmaterialpermission(false)
end

------Command Unlock Materials
local	gs_unlockmaterialcommand = command.create ("Guerilleros|Permission|Materials Unlock ", nil, "")
function gs_unlockmaterialcommand:isenabled ()
	return tonumber(os.getenv("GUERILLA_POWER_USER"))==1
end

function gs_unlockmaterialcommand:action ()
	gs_setmaterialpermission(true)
end

------Command incremental save
local	gs_incrementalsavecommand = command.create ("Guerilleros|File|Incremental Save", "icon_file_save.png", "")

function gs_incrementalsavecommand:isenabled ()
	return true
end

function gs_incrementalsavecommand:action ()
	gs_incrementalsave()
end

------Command incremental save flush
local	gs_incrementalsaveflushcommand = command.create ("Guerilleros|File|Incremental Flush", "button_bin.png", "")

function gs_incrementalsaveflushcommand:isenabled ()
	return true
end

function gs_incrementalsaveflushcommand:action ()
	gs_incrementalsaveflush()
end

------UI
if MainMenu then
	--Lock menu
	MainMenu:addcommand (gs_lockselectioncommand, "Guerilleros", "Permission")
	MainMenu:addcommand (gs_unlockselectioncommand, "Guerilleros", "Permission")
	MainMenu:addseparator ("Guerilleros", "Permission")
	MainMenu:addcommand (gs_lockmaterialcommand, "Guerilleros", "Permission")
	MainMenu:addcommand (gs_unlockmaterialcommand, "Guerilleros", "Permission")
	--File
	MainMenu:addcommand (gs_incrementalsavecommand, "Guerilleros", "File")
	MainMenu:addcommand (gs_incrementalsaveflushcommand, "Guerilleros", "File")
end
