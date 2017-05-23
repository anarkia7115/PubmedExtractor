USE pubminer; 

CREATE TABLE if not exists pubmed_extracted_dis(
	pmid int(20),
	mention_start int(5), 
	mention_end int(5), 
	mention varchar(200),
	tag varchar(100),
	term_id varchar(100)
);
CREATE TABLE if not exists pubmed_extracted_gene(
	pmid int(20),
	mention_start int(5), 
	mention_end int(5), 
	mention varchar(200),
	tag varchar(100),
	term_id varchar(100)
);
CREATE TABLE if not exists pubmed_extracted_chem(
	pmid int(20),
	mention_start int(5), 
	mention_end int(5), 
	mention varchar(200),
	tag varchar(100),
	term_id varchar(100)
);
