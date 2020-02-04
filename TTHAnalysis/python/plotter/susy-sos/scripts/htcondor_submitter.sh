executable      = [SCRIPT]
arguments       = [NAME]
output          = [DIR]/job.[NAME].0.out
error           = [DIR]/job.[NAME].0.err
log             = [DIR]/job.[NAME].log
+JobFlavour	= "[QUEUE]"
+AccountingGroup = "group_u_CMST3.all"
queue
