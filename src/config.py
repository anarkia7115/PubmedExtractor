mongodb = dict(
    host = "192.168.2.10"
    , port = 27017
)

runtime_data_dir = "/home/shawn/git/PubmedExtractor/data"

dir_path = dict(
    article = "{data_dir}/article".format(data_dir=runtime_data_dir)
    , chem_rst = "{data_dir}/chemOut".format(data_dir=runtime_data_dir)
    , gene_rst = "{data_dir}/geneOut".format(data_dir=runtime_data_dir)
    , pubmed = "/home/shawn/workspace/PubMed"
)

exec_dir = dict(
    dis = "{0}/DNorm-0.0.7".format(dir_path['pubmed'])
    , chem = "{0}/tmChem".format(dir_path['pubmed'])
    , gene = "{0}/GNormPlusJava".format(dir_path['pubmed']) 
)

exec_cmd = dict(
    dis = "/bin/bash {dis_dir}/ApplyDNorm.sh {dis_dir}/config/banner_NCBIDisease_UMLS2013AA_TEST.xml {dis_dir}/data/CTD_diseases.tsv {dis_dir}/output/simmatrix_NCBIDisease_e4.bin    {pubmed_dir}/Ab3P-v1.5/ ./tmpdata {in_path} {out_path}".format(
        dis_dir=exec_dir['dis'],
        pubmed_dir=dir_path['pubmed'],
        in_path="{in_path}",
        out_path="{out_path}")

    , chem = "perl {chem_dir}/tmChem.pl -i {in_path} -o {out_path}".format(
        chem_dir=exec_dir['chem'],
        in_path="{in_path}",
        out_path="{out_path}")
    , gene = "java -Xmx10G -Xms10G -jar {gene_dir}/GNormPlus.jar {in_path} {out_path} setup.txt".format(
        gene_dir=exec_dir['gene'],
        in_path="{in_path}",
        out_path="{out_path}")
)

file_path = dict(
    article = "{article_dir}/articleOut".format(article_dir=dir_path['article'])
    , chem = "{chem_dir}/articleOut.tmChem".format(chem_dir=dir_path['chem'])
    , gene = "{gene_dir}/articleOut".format(gene_dir=dir_path['gene_dir'])
    , dis  = "{data_dir}/disOut".format(data_dir=runtime_data_dir)

    , chem_word = "{data_dir}/chemWord".format(data_dir=runtime_data_dir)
    , gene_word = "{data_dir}/geneWord".format(data_dir=runtime_data_dir)
    , dis_word  = "{data_dir}/disWord".format(data_dir=runtime_data_dir)
)
