# Protoc program
$protoc = "G:/YastAI/protoc.exe"

# Push Location then pop
Push-Location ./protobuf

foreach ($proto_file in Get-ChildItem -Filter *.proto) {
    Write-Output "Compiling $proto_file"
    $proto_filaname = $proto_file.Name
    Write-Output $proto_filaname
    Invoke-Expression "$protoc --python_out='../py' $proto_filaname"
    Write-Output "python ../jsonify.py -f $proto_filaname -t protobuf -o ../json/$proto_filaname.json"
    python ../jsonify.py -f $proto_filaname -t protobuf -o ../json/$proto_filaname.json
}
Pop-Location