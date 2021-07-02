# MAG Metadata Coverage Report
#
# Copyright 2020-21 ######
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Authors: Cameron Neylon, Bianca Kramer

# SQL Queries used for interacting with the BigQuery Datasets

# Document Types and Counts

doi_table_types = """
SELECT 
    mag.Doctype as mag_doctype,
    crossref.type as cr_type,
    count(doi) as total_count,
    countif(mag.PaperId IS NOT NULL) as mag,

FROM `academic-observatory.observatory.doi20210605`

GROUP BY mag_doctype, cr_type
ORDER BY total_count DESC
"""

mag_table_types = """
WITH table AS (
SELECT 
    *,
    CASE
        WHEN Doi is not null THEN TRUE
        ELSE FALSE
      END
        as has_doi 
FROM `academic-observatory.mag.Papers20210510` 
)

SELECT 
    Doctype,
    has_doi,
    count(PaperId) as count,
    countif(Doi IS NOT NULL) as count_doi
FROM table
GROUP BY Doctype, has_doi
ORDER BY count DESC
"""

mag_coverage_by_year = """
SELECT
    crossref.published_year,
    COUNTIF(mag.PaperId is Null) as no_mag_id,
    COUNTIF(crossref.type = "journal-article") as journal_article_count,
    COUNT(DOI) as total_count
FROM `academic-observatory.observatory.doi20210605`
WHERE crossref.published_year > 1980 and crossref.published_year < 2025
GROUP BY crossref.published_year
ORDER BY crossref.published_year DESC
"""

# Metadata Elements and MAG Added Value to Crossref

doi_table_categories_query = """
WITH truth_table_update AS (
    SELECT
        doi,
        crossref.type,
        crossref.published_year,    
        CASE
            WHEN (SELECT COUNT(1) FROM UNNEST(crossref.author) AS authors, UNNEST(authors.affiliation) AS affiliation WHERE affiliation.name is not null) > 0 THEN TRUE
            ELSE FALSE
        END
        as has_cr_affiliation_string,
        CASE
            WHEN 
                (SELECT COUNT(1) from UNNEST(mag.authors) AS mauthors where mauthors.OriginalAffiliation is not null) > 0  THEN TRUE
            ELSE FALSE
        END
        as has_mag_aff_string,
        CASE
            WHEN 
                (SELECT COUNT(1) FROM UNNEST(crossref.author) AS authors, UNNEST(authors.affiliation) AS affiliation WHERE affiliation.name is not null) = 0
                and
                (SELECT COUNT(1) from UNNEST(mag.authors) AS mauthors where mauthors.OriginalAffiliation is not null) > 0  THEN TRUE
            ELSE FALSE
        END
        as has_mag_aff_string_not_cr_affiliation,
        CASE
            WHEN (SELECT COUNT(1) FROM UNNEST(crossref.author) AS authors WHERE authors.authenticated_orcid is not null) > 0 THEN TRUE
            ELSE FALSE
        END
        as has_cr_authenticated_orcid,
        CASE
            WHEN (SELECT COUNT(1) FROM UNNEST(crossref.author) AS authors WHERE authors.ORCID is not null) > 0 THEN TRUE
            ELSE FALSE
        END
        as has_cr_orcid,
        CASE
            WHEN 
                ((SELECT COUNT(1) FROM UNNEST(mag.authors) AS mauthors WHERE mauthors.AuthorId is not null) > 0) THEN TRUE
            ELSE FALSE
        END
        as has_mag_authorid,
        CASE
            WHEN 
                ((SELECT COUNT(1) FROM UNNEST(crossref.author) AS authors WHERE authors.ORCID is not null) = 0) AND
                ((SELECT COUNT(1) FROM UNNEST(mag.authors) AS mauthors WHERE mauthors.AuthorId is not null) > 0) THEN TRUE
            ELSE FALSE
        END
        as has_mag_authorid_not_cr_orcid,
        CASE
            WHEN (SELECT COUNT(1) FROM UNNEST(crossref.author) AS authors WHERE authors.family is not null) > 0 THEN TRUE
            ELSE FALSE
        END
        as has_cr_author_name,
        CASE
            WHEN 
                (SELECT COUNT(1) FROM UNNEST(mag.authors) AS mauthors WHERE mauthors.OriginalAuthor is not null) > 0 THEN TRUE
            ELSE FALSE
        END
        as has_mag_author_name,
        CASE
            WHEN 
                (SELECT COUNT(1) FROM UNNEST(crossref.author) AS authors WHERE authors.family is not null) = 0 
                AND
                (SELECT COUNT(1) FROM UNNEST(mag.authors) AS mauthors WHERE mauthors.OriginalAuthor is not null) > 0 THEN TRUE
            ELSE FALSE
        END
        as has_mag_not_cr_author_name,
        CASE
            WHEN (crossref.abstract is not null) THEN TRUE
            ELSE FALSE
        END
        as has_cr_abstract,
        CASE
            WHEN (mag.abstract is not null) THEN TRUE
            ELSE FALSE
        END
        as has_mag_abstract,
        CASE
            WHEN 
                (crossref.abstract is null) AND
                (mag.abstract is not null) THEN TRUE
            ELSE FALSE
        END
        as has_mag_not_cr_abstract,    
        CASE
            WHEN crossref.is_referenced_by_count > 0 THEN TRUE
            ELSE FALSE
        END
        as has_cr_citations,
        CASE
            WHEN (mag.CitationCount > 0) THEN TRUE
            ELSE FALSE
        END
        as has_mag_citations,
        CASE
            WHEN (crossref.is_referenced_by_count = 0) and (mag.CitationCount > 0) THEN TRUE
            ELSE FALSE
        END
        as has_mag_no_cr_citations,
        CASE
            WHEN (crossref.is_referenced_by_count = mag.CitationCount) THEN "EQUAL"
            WHEN (crossref.is_referenced_by_count > mag.CitationCount) THEN "MORE_CR"
            WHEN (crossref.is_referenced_by_count < mag.CitationCount) THEN "MORE_MAG"
            ELSE "FALSE"
        END
        as mag_vs_cr_cites,
        CASE
            WHEN crossref.references_count > 0 THEN TRUE
            ELSE FALSE
        END
        as has_cr_references,
        CASE
            WHEN (mag.ReferenceCount > 0) THEN TRUE
            ELSE FALSE
        END
        as has_mag_references,
        CASE
            WHEN (crossref.references_count = 0) and (mag.ReferenceCount > 0) THEN TRUE
            ELSE FALSE
        END
        as has_mag_no_cr_references,
        CASE
            WHEN (crossref.references_count = mag.ReferenceCount) THEN "EQUAL"
            WHEN (crossref.references_count > mag.ReferenceCount) THEN "MORE_CR"
            WHEN (crossref.references_count < mag.ReferenceCount) THEN "MORE_MAG"
            ELSE "FALSE"
        END
        as mag_vs_cr_references,    

        CASE
            WHEN ARRAY_LENGTH(crossref.subject) > 0 THEN crossref.subject[OFFSET(0)]
            ELSE null
        END as 
        cr_top_subject,
        CASE
            WHEN ARRAY_LENGTH(crossref.subject) > 0 THEN ARRAY_TO_STRING(crossref.subject, ";")
            ELSE null
        END as 
        cr_concat_subjects,

        CASE
            WHEN ARRAY_LENGTH(crossref.subject) > 0 THEN ARRAY_LENGTH(crossref.subject) 
            ELSE null
        END as num_cr_subjects,

        CASE
            WHEN (ARRAY_LENGTH(mag.fields.level_0) > 0) THEN ARRAY_LENGTH(mag.fields.level_0)
            ELSE null
        END as 
        num_mag_field0,
        CASE
            WHEN (ARRAY_LENGTH(crossref.subject) = 0) AND (ARRAY_LENGTH(mag.fields.level_0) > 0) THEN TRUE
            ELSE FALSE
        END as 
        has_mag_field0_not_cr_subject,

    FROM `academic-observatory.observatory.doi20210619`
)

SELECT
    published_year,
    type,
    COUNT(doi) as num_dois,
    
    COUNTIF(has_cr_affiliation_string) as dois_with_cr_affiliation_strings,
    COUNTIF(has_mag_aff_string) as dois_with_mag_affiliation_strings,
    COUNTIF(has_mag_aff_string_not_cr_affiliation) as dois_mag_aff_string_but_not_cr,
    
    COUNTIF(has_cr_orcid) as dois_with_cr_orcid,
    COUNTIF(has_cr_authenticated_orcid) as doi_with_cr_authenticated_orcid,
    COUNTIF(has_mag_authorid) as dois_with_mag_author_id,
    COUNTIF(has_mag_authorid_not_cr_orcid) as dois_with_mag_author_id_but_not_cr_orcid,
    
    COUNTIF(has_cr_author_name) as dois_with_cr_author_name,
    COUNTIF(has_mag_author_name) as dois_with_mag_author_name,
    COUNTIF(has_mag_not_cr_author_name) as dois_with_mag_not_cr_author_name,
    
    COUNTIF(has_cr_abstract) as dois_with_cr_abstract,
    COUNTIF(has_mag_abstract) as dois_with_mag_abstract,
    COUNTIF(has_mag_not_cr_abstract) as dois_with_mag_not_cr_abstract,
      
    COUNTIF(has_cr_citations) as dois_with_cr_citations,
    COUNTIF(has_mag_citations) as dois_with_mag_citations,
    COUNTIF(has_mag_no_cr_citations) as dois_with_mag_not_cr_citations,
    COUNTIF(mag_vs_cr_cites = "EQUAL") as dois_same_mag_cr_citations,
    COUNTIF(mag_vs_cr_cites = "MORE_CR") as dois_more_cr_citations,
    COUNTIF(mag_vs_cr_cites = "MORE_MAG") as dois_more_mag_citations,

    COUNTIF(has_cr_references) as dois_with_cr_references,
    COUNTIF(has_mag_references) as dois_with_mag_references,
    COUNTIF(has_mag_no_cr_references) as dois_with_mag_not_cr_references,
    COUNTIF(mag_vs_cr_references = "EQUAL") as dois_same_mag_cr_references,
    COUNTIF(mag_vs_cr_references = "MORE_CR") as dois_more_cr_references,
    COUNTIF(mag_vs_cr_references = "MORE_MAG") as dois_more_mag_references,
    
    COUNTIF(num_cr_subjects is not null) as dois_with_cr_subjects,
    COUNTIF(num_mag_field0 is not null) as dois_with_mag_field0,
    COUNTIF(has_mag_field0_not_cr_subject) as dois_with_mag_field_not_cr_subject
    
FROM truth_table_update

GROUP BY published_year, type
ORDER BY published_year DESC, type ASC
"""

doi_table_categories_aggregation = """
SELECT 
    type,

    sum( num_dois ) as dois,
    
    sum( dois_with_cr_affiliation_strings ) as dois_cr_aff_strings,
    sum( dois_with_mag_affiliation_strings ) as dois_mag_aff_strings,
    sum( dois_mag_aff_string_but_not_cr ) as dois_mag_not_cr_aff_strings,
    
    sum ( dois_with_cr_abstract ) as dois_cr_abstract,
    sum ( dois_with_mag_abstract ) as dois_mag_abstract,
    sum ( dois_with_mag_not_cr_abstract ) as dois_mag_not_cr_abstracts,
    
    sum( dois_with_cr_subjects ) as dois_cr_subjects,
    sum( dois_with_mag_field0 ) as dois_mag_subjects,
    sum( dois_with_mag_field_not_cr_subject ) as dois_mag_not_cr_subjects,
    
    sum( dois_with_cr_citations ) as dois_cr_citations,
    sum( dois_with_mag_citations ) as dois_mag_citations,
    sum( dois_with_Mag_not_cr_citations ) as dois_mag_not_cr_citations,
    sum( dois_more_mag_citations ) as dois_mag_more_citations,
    
    sum( dois_with_cr_references ) as dois_cr_references,
    sum( dois_with_mag_references ) as dois_mag_references,
    sum( dois_with_mag_not_cr_references ) as dois_mag_not_cr_references,
    sum( dois_more_mag_references ) as dois_mag_more_references

FROM `utrecht-university.MAG.doi_table_category_queries_update_results`
WHERE
    published_year IN (2019, 2020, 2021)

GROUP BY type
ORDER BY dois DESC
"""

# MAG non-DOI Metadata Quality
mag_table_categories_query = """
WITH truth_table AS (
    SELECT
        Doi,
        PaperId,
        DocType,
        Year,
        CASE
            WHEN (SELECT COUNT(1) FROM UNNEST(authors) AS authors WHERE authors.AffiliationId is not null) > 0 THEN TRUE
            ELSE FALSE
        END
        as has_affiliation_id,
        CASE
            WHEN (SELECT COUNT(1) FROM UNNEST(authors) AS authors WHERE authors.GridId is not null) > 0 THEN TRUE
            ELSE FALSE
        END
        as has_gridid,
        CASE
            WHEN (SELECT COUNT(1) FROM UNNEST(authors) AS authors WHERE authors.OriginalAffiliation is not null) > 0 THEN TRUE
            ELSE FALSE
        END
        as has_affiliation_string,
         CASE
            WHEN CitationCount > 0 THEN TRUE
            ELSE FALSE
        END
        as has_citations,  
        CASE
            WHEN ReferenceCount > 0 THEN TRUE
            ELSE FALSE
        END
        as has_references,     

        fields.level_0[OFFSET(0)].DisplayName as field,
        ARRAY_LENGTH(fields.level_0) as num_fields,

        CASE
            WHEN ((Doi is not null) AND (PaperId != FamilyId) AND (FamilyId is not null)) THEN TRUE 
            ELSE FALSE
        END
        as doi_not_canonical_family

    FROM `utrecht-university.MAG.mag_all_papers`
)

SELECT
    Year,
    DocType,
    field,
    COUNTIF(Doi is not null) as num_dois,
    COUNTIF(has_affiliation_id and Doi is not null) as dois_with_affiliation_ids,
    COUNTIF(has_gridid and Doi is not null) as dois_with_grids,
    COUNTIF(has_affiliation_string and Doi is not null) as dois_with_affiliation_strings,
    COUNTIF(has_citations and Doi is not null) as dois_with_citations,
    COUNTIF(has_references and Doi is not null) as dois_with_references,
    COUNTIF(num_fields > 1 and Doi is not null) as dois_with_more_than_one_field,
    
    COUNT(PaperId) as num_objects,
    COUNTIF(has_affiliation_id) as objects_with_affiliation_ids,
    COUNTIF(has_gridid) as objects_with_grids,
    COUNTIF(has_affiliation_string) as objects_with_affiliation_strings,
    COUNTIF(has_citations) as objects_with_citations,
    COUNTIF(has_references) as objects_with_references,
    COUNTIF(num_fields > 1) as objects_with_more_than_one_field,

    COUNTIF(doi_not_canonical_family) as doi_not_canonical_family
    
FROM truth_table
GROUP BY Year, DocType, field
ORDER BY Year DESC, DocType ASC, field ASC
"""

mag_table_categories_aggregation = """
SELECT

---DocType,
---field,

sum(num_dois) as dois,
sum(dois_with_affiliation_ids) as dois_aff_id,
sum(dois_with_grids) as dois_grids,
sum(dois_with_affiliation_strings) as dois_aff_strings,
sum(CASE WHEN field IS NOT NULL THEN num_dois END) as dois_subject,
sum(dois_with_citations) as dois_citations,
sum(dois_with_references) as dois_references,

sum(num_objects) - sum(num_dois) as non_dois,
sum(objects_with_affiliation_ids) - sum(dois_with_affiliation_ids) as non_dois_aff_id,
sum(objects_with_grids)  - sum(dois_with_grids) as non_dois_grids,
sum(objects_with_affiliation_strings) - sum(dois_with_affiliation_strings) as non_dois_aff_strings,
sum(CASE WHEN field IS NOT NULL THEN num_objects END) - sum(CASE WHEN field IS NOT NULL THEN num_dois END) as non_dois_subject,
sum(objects_with_citations) - sum(dois_with_citations) as non_dois_citations,
sum(objects_with_references) - sum(dois_with_references) as non_dois_references,


FROM `utrecht-university.MAG.mag_category_queries_result`
---WHERE
---Year IN (2019, 2020, 2021)

---GROUP BY
---DocType,
---field

---ORDER BY dois DESC
"""