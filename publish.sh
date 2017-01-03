tar -vzcf src.tar.gz ./src
scp ./src.tar.gz textMining:~/PubmedExtractor
echo "start decompress"
ssh textMining "tar  -C ~/PubmedExtractor -vzxf ~/PubmedExtractor/src.tar.gz"
