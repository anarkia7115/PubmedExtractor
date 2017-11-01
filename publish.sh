tar -vzcf src.tar.gz ./src
#scp ./src.tar.gz textMining:~/PubmedExtractor
scp ./src.tar.gz app08:~/PubmedExtractor
echo "start decompress"
#ssh textMining "tar  -C ~/PubmedExtractor -vzxf ~/PubmedExtractor/src.tar.gz"
ssh app08 "tar  -C ~/PubmedExtractor -vzxf ~/PubmedExtractor/src.tar.gz"
ssh app08 "cp ~/PubmedExtractor/src/config_product.py ~/PubmedExtractor/src/config.py"
