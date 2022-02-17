#List all processes and the virutalmemory (VM) that each process is using
Get-Process | sort vm | select name, vm 

#List the last 5 processes and the virutalmemory (VM) that each process is using
Get-Process | sort vm | select name, vm -Last 5

#List the last 5 processes and the pagedmemory (PM) that each process is using
Get-Process | sort pm | select name, pm -Last 5

#list all processes based on name and id
Get-Process|Select-Object name,id

#get all processes based on name and id.  
#create a hash table named (n) virturalmemory that uses the expression (e) VM to pull the virtualmemory property
#create a hash table named (n) pagedmemory that uses the expression (e) PM to pull the pagedmemory property
Get-Process|Select-Object name,id,@{n='virtualmemory';e={$psitem.vm}},@{n='pagedmemory';e={$psitem.pm}}

#get all processes based on name and id.  
#create a hash table named (n) virturalmemory that uses the expression (e) VM to pull the virtualmemory property that is formatted in MB
#create a hash table named (n) pagedmemory that uses the expression (e) PM to pull the pagedmemory property that is formatted in MB
Get-Process|Select-Object name,id,@{n='virtualmemory(MB)';e={$psitem.vm/1MB}},@{n='pagedmemory(MB)';e={$psitem.pm/1MB}}

#Gets all processes. Processes will be listed by name and id.  Each process will have a column containing virtual memory and pagedmemory.
#virtualmemory and pagedmemory will be listedin MB format.  the format will be the numer of MB followed by two numbers after the decimal.
#For example 1MB will be listed as 1.00
Get-Process|Select-Object name,id,@{n='virtualmemory(MB)';e={'{0:n2}' -f ($psitem.vm/1MB)}},@{n='pagedmemory(MB)';e={'{0:n2}'-f ($psitem.pm/1MB)}}