USE pubminer;

CREATE INDEX pmid
ON pubmed_extracted_dis (pmid);

CREATE INDEX pmid
ON pubmed_extracted_gene (pmid);

CREATE INDEX pmid
ON pubmed_extracted_chem (pmid);
