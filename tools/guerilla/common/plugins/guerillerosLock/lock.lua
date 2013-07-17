--Function to lock unlock shader in the scene
function gs_setmaterialpermission(iseditable)
	for node in children (Document, "Material", nil, true) do
		node:seteditable(iseditable)
	end
end

function gs_setselectionpermission(iseditable)
	for k,node in pairs(Document:getselection()) do
		node:seteditable(iseditable)
	end
end

