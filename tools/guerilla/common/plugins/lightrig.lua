print ("hk-guerilla")
class ( "LightRig", "SceneGraphNode" )

function createlightrig ()
	local mod = Document:modify ()
	-- Create a child in the Document
	local node = mod.createnode (Document, "LightRig", "LightRig")
	mod.finish ()
end
