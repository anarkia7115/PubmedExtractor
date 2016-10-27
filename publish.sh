tar -vzcf src.tar.gz ./src
scp ./src.tar.gz textMining:~/pubmedTextMining
ssh textMining "tar  -C ~/pubmedTextMining -vzxf pubmedTextMining/src.tar.gz"
