import pipeline.utils as utils
'''
|-
|''composite''
|rcmp
|-
'''

assetlist = utils.getAssetTasks()

for i in assetlist :
    print """|''%s''
|%s
|-""" % ( i, assetlist[i] )