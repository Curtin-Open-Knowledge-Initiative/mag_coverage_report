
CREATE TEMP FUNCTION compute_percentiles(counts ARRAY<INT64>) AS (
  (SELECT as STRUCT
    ROUND(PERCENTILE_CONT(count, 0.50) OVER(), 2) as Median_PerRow,
    ROUND(PERCENTILE_CONT(count, 0.75) OVER(), 2) as Cent75_PerRow,
    ROUND(PERCENTILE_CONT(count, 0.90) OVER(), 2) as Cent90_PerRow,
    ROUND(PERCENTILE_CONT(count, 0.95) OVER(), 2) as Cent95_PerRow,
    ROUND(PERCENTILE_CONT(count, 0.99) OVER(), 2) as Cent99_PerRow
  FROM UNNEST(counts) as count LIMIT 1)
);

WITH
unnested_fields as (
    SELECT
        doi,
        crossref.published_year,
        crossref.published_month,
        crossref.ISSN[OFFSET(0)] as journal,
        crossref.type as cr_type,
        mag.CitationCount as mag_CitationCount,
        open_citations.citations_total as oc_CitationCount,
        open_citations.citations_two_years as oc2y_CitationCount,
        field
    FROM `academic-observatory.observatory.doi20210626`, UNNEST(mag.fields.level_0) as field
    WHERE crossref.published_year > 2010 AND crossref.published_year < 2022
    --and "Australia" in (SELECT name from UNNEST(affiliations.countries))
    -- and ("au_go8" in (SELECT identifier from UNNEST(affiliations.groupings)) OR "grid.1032.0" in (SELECT identifier from UNNEST(affiliations.institutions)))
    -- and ("au_atn" in (SELECT identifier from UNNEST(affiliations.groupings)) OR "grid.1032.0" in (SELECT identifier from UNNEST(affiliations.institutions)))

),

benchmarks_by_mag_field_year AS (
    SELECT
        field.DisplayName as fieldname,
        published_year,
        compute_percentiles(ARRAY_AGG(mag_CitationCount)).*,
        AVG(mag_CitationCount) AS mean
    FROM unnested_fields
    GROUP BY fieldname, published_year
),

benchmarks_by_mag_field_month AS (
    SELECT
        field.DisplayName as fieldname,
        published_year,
        published_month,
        compute_percentiles(ARRAY_AGG(mag_CitationCount)).*,
        AVG(mag_CitationCount) AS mean
    FROM unnested_fields
    GROUP BY fieldname, published_year, published_month
),

benchmarks_by_oc_field_year AS (
    SELECT
        field.DisplayName as fieldname,
        published_year,
        compute_percentiles(ARRAY_AGG(oc_CitationCount)).*,
        AVG(oc_CitationCount) AS mean,
    FROM unnested_fields
    GROUP BY fieldname, published_year
),

benchmarks_by_oc_field_month AS (
    SELECT
        field.DisplayName as fieldname,
        published_year,
        published_month,
        compute_percentiles(ARRAY_AGG(oc_CitationCount)).*,
        AVG(oc_CitationCount) AS mean,
    FROM unnested_fields
    GROUP BY fieldname, published_year, published_month
),

benchmarks_by_oc2y_field_year AS (
    SELECT
        field.DisplayName as fieldname,
        published_year,
        compute_percentiles(ARRAY_AGG(oc2y_CitationCount)).*,
        AVG(oc2y_CitationCount) AS mean,
    FROM unnested_fields
    GROUP BY fieldname, published_year
),

benchmarks_by_oc2y_field_month AS (
    SELECT
        field.DisplayName as fieldname,
        published_year,
        published_month,
        compute_percentiles(ARRAY_AGG(oc2y_CitationCount)).*,
        AVG(oc2y_CitationCount) AS mean,
    FROM unnested_fields
    GROUP BY fieldname, published_year, published_month
),

metrics as (
    SELECT
        doi,
        cr_type,
        CASE
            WHEN mag_CitationCount >= b_mag_field_year.Cent99_PerRow THEN "1"
            WHEN mag_CitationCount >= b_mag_field_year.Cent95_PerRow THEN "5"
            WHEN mag_CitationCount >= b_mag_field_year.Cent90_PerRow THEN "10"
            WHEN mag_CitationCount >= b_mag_field_year.Cent75_PerRow THEN "25"
            WHEN mag_CitationCount >= b_mag_field_year.Median_PerRow THEN "50"
            ELSE "Other"
        END as mag_field_year_percentile_group,
        CASE
            WHEN mag_CitationCount = 0 THEN "0"
            WHEN mag_CitationCount / b_mag_field_year.mean < 0.8 THEN "I"
            WHEN mag_CitationCount / b_mag_field_year.mean < 1.2 THEN "II"
            WHEN mag_CitationCount / b_mag_field_year.mean < 2 THEN "III"
            WHEN mag_CitationCount / b_mag_field_year.mean < 4 THEN "IV"
            WHEN mag_CitationCount / b_mag_field_year.mean < 8 THEN "V"
            ELSE "VI"
        END as mag_field_year_rci_group,
        CASE
            WHEN mag_CitationCount >= b_mag_field_month.Cent99_PerRow THEN "1"
            WHEN mag_CitationCount >= b_mag_field_month.Cent95_PerRow THEN "5"
            WHEN mag_CitationCount >= b_mag_field_month.Cent90_PerRow THEN "10"
            WHEN mag_CitationCount >= b_mag_field_month.Cent75_PerRow THEN "25"
            WHEN mag_CitationCount >= b_mag_field_month.Median_PerRow THEN "50"
            ELSE "Other"
        END as mag_field_month_percentile_group,
        CASE
            WHEN mag_CitationCount = 0 THEN "0"
            WHEN mag_CitationCount / b_mag_field_month.mean < 0.8 THEN "I"
            WHEN mag_CitationCount / b_mag_field_month.mean < 1.2 THEN "II"
            WHEN mag_CitationCount / b_mag_field_month.mean < 2 THEN "III"
            WHEN mag_CitationCount / b_mag_field_month.mean < 4 THEN "IV"
            WHEN mag_CitationCount / b_mag_field_month.mean < 8 THEN "V"
            ELSE "VI"
        END as mag_field_month_rci_group,

        CASE
            WHEN oc_CitationCount >= b_oc_field_year.Cent99_PerRow THEN "1"
            WHEN oc_CitationCount >= b_oc_field_year.Cent95_PerRow THEN "5"
            WHEN oc_CitationCount >= b_oc_field_year.Cent90_PerRow THEN "10"
            WHEN oc_CitationCount >= b_oc_field_year.Cent75_PerRow THEN "25"
            WHEN oc_CitationCount >= b_oc_field_year.Median_PerRow THEN "50"
            ELSE "Other"
        END as oc_field_year_percentile_group,
        CASE
            WHEN oc_CitationCount = 0 THEN "0"
            WHEN oc_CitationCount / b_oc_field_year.mean < 0.8 THEN "I"
            WHEN oc_CitationCount / b_oc_field_year.mean < 1.2 THEN "II"
            WHEN oc_CitationCount / b_oc_field_year.mean < 2 THEN "III"
            WHEN oc_CitationCount / b_oc_field_year.mean < 4 THEN "IV"
            WHEN oc_CitationCount / b_oc_field_year.mean < 8 THEN "V"
            ELSE "VI"
        END as oc_field_year_rci_group,
        CASE
            WHEN oc_CitationCount >= b_oc_field_month.Cent99_PerRow THEN "1"
            WHEN oc_CitationCount >= b_oc_field_month.Cent95_PerRow THEN "5"
            WHEN oc_CitationCount >= b_oc_field_month.Cent90_PerRow THEN "10"
            WHEN oc_CitationCount >= b_oc_field_month.Cent75_PerRow THEN "25"
            WHEN oc_CitationCount >= b_oc_field_month.Median_PerRow THEN "50"
            ELSE "Other"
        END as oc_field_month_percentile_group,
        CASE
            WHEN oc_CitationCount = 0 THEN "0"
            WHEN oc_CitationCount / b_oc_field_month.mean < 0.8 THEN "I"
            WHEN oc_CitationCount / b_oc_field_month.mean < 1.2 THEN "II"
            WHEN oc_CitationCount / b_oc_field_month.mean < 2 THEN "III"
            WHEN oc_CitationCount / b_oc_field_month.mean < 4 THEN "IV"
            WHEN oc_CitationCount / b_oc_field_month.mean < 8 THEN "V"
            ELSE "VI"
        END as oc_field_month_rci_group,

        CASE
            WHEN oc2y_CitationCount >= b_oc2y_field_year.Cent99_PerRow THEN "1"
            WHEN oc2y_CitationCount >= b_oc2y_field_year.Cent95_PerRow THEN "5"
            WHEN oc2y_CitationCount >= b_oc2y_field_year.Cent90_PerRow THEN "10"
            WHEN oc2y_CitationCount >= b_oc2y_field_year.Cent75_PerRow THEN "25"
            WHEN oc2y_CitationCount >= b_oc2y_field_year.Median_PerRow THEN "50"
            ELSE "Other"
        END as oc2y_field_year_percentile_group,
        CASE
            WHEN oc2y_CitationCount = 0 THEN "0"
            WHEN oc2y_CitationCount / b_oc2y_field_year.mean < 0.8 THEN "I"
            WHEN oc2y_CitationCount / b_oc2y_field_year.mean < 1.2 THEN "II"
            WHEN oc2y_CitationCount / b_oc2y_field_year.mean < 2 THEN "III"
            WHEN oc2y_CitationCount / b_oc2y_field_year.mean < 4 THEN "IV"
            WHEN oc2y_CitationCount / b_oc2y_field_year.mean < 8 THEN "V"
            ELSE "VI"
        END as oc2y_field_year_rci_group,
        CASE
            WHEN oc2y_CitationCount >= b_oc2y_field_month.Cent99_PerRow THEN "1"
            WHEN oc2y_CitationCount >= b_oc2y_field_month.Cent95_PerRow THEN "5"
            WHEN oc2y_CitationCount >= b_oc2y_field_month.Cent90_PerRow THEN "10"
            WHEN oc2y_CitationCount >= b_oc2y_field_month.Cent75_PerRow THEN "25"
            WHEN oc2y_CitationCount >= b_oc2y_field_month.Median_PerRow THEN "50"
            ELSE "Other"
        END as oc2y_field_month_percentile_group,
        CASE
            WHEN oc2y_CitationCount = 0 THEN "0"
            WHEN oc2y_CitationCount / b_oc2y_field_month.mean < 0.8 THEN "I"
            WHEN oc2y_CitationCount / b_oc2y_field_month.mean < 1.2 THEN "II"
            WHEN oc2y_CitationCount / b_oc2y_field_month.mean < 2 THEN "III"
            WHEN oc2y_CitationCount / b_oc2y_field_month.mean < 4 THEN "IV"
            WHEN oc2y_CitationCount / b_oc2y_field_month.mean < 8 THEN "V"
            ELSE "VI"
        END as oc2y_field_month_rci_group,

    FROM unnested_fields as u
        JOIN benchmarks_by_mag_field_year as b_mag_field_year on
            u.published_year=b_mag_field_year.published_year
            AND u.field.DisplayName= b_mag_field_year.fieldname
        JOIN benchmarks_by_mag_field_month as b_mag_field_month on
            u.published_year=b_mag_field_month.published_year
            AND u.published_month = b_mag_field_month.published_month
            AND u.field.DisplayName = b_mag_field_month.fieldname
        JOIN benchmarks_by_oc_field_year as b_oc_field_year on
            u.published_year=b_oc_field_year.published_year
            AND u.field.DisplayName= b_oc_field_year.fieldname
        JOIN benchmarks_by_oc_field_month as b_oc_field_month on
            u.published_year=b_oc_field_month.published_year
            AND u.published_month = b_oc_field_month.published_month
            AND u.field.DisplayName = b_oc_field_month.fieldname
        JOIN benchmarks_by_oc2y_field_year as b_oc2y_field_year on
            u.published_year=b_oc2y_field_year.published_year
            AND u.field.DisplayName= b_oc2y_field_year.fieldname
        JOIN benchmarks_by_oc2y_field_month as b_oc2y_field_month on
            u.published_year=b_oc2y_field_month.published_year
            AND u.published_month = b_oc2y_field_month.published_month
            AND u.field.DisplayName = b_oc2y_field_month.fieldname
)

SELECT
    crossref.published_year,
    school,
    COUNT(DISTINCT d.doi) as total_outputs,
    COUNTIF(cr_type = "journal-article") as journal_articles,
    SUM(mag.CitationCount) as total_citations,
    COUNTIF(mag_field_year_rci_group = "0") as magy_rci_group_0,
    COUNTIF(mag_field_year_rci_group = "I") as magy_rci_group_I,
    COUNTIF(mag_field_year_rci_group = "II") as magy_rci_group_II,
    COUNTIF(mag_field_year_rci_group = "III") as magy_rci_group_III,
    COUNTIF(mag_field_year_rci_group = "IV") as magy_rci_group_IV,
    COUNTIF(mag_field_year_rci_group = "V") as magy_rci_group_V,
    COUNTIF(mag_field_year_rci_group = "VI") as magy_rci_group_VI,
    COUNTIF(mag_field_year_percentile_group = "1") as magy_centile_1,
    COUNTIF(mag_field_year_percentile_group = "5") as magy_centile_5,
    COUNTIF(mag_field_year_percentile_group = "10") as magy_centile_10,
    COUNTIF(mag_field_year_percentile_group = "25") as magy_centile_25,
    COUNTIF(mag_field_year_percentile_group = "50") as magy_centile_50,
    COUNTIF(mag_field_year_percentile_group = "Other") as magy_centile_other,

    COUNTIF(mag_field_month_rci_group = "0") as magm_rci_group_0,
    COUNTIF(mag_field_month_rci_group = "I") as magm_rci_group_I,
    COUNTIF(mag_field_month_rci_group = "II") as magm_rci_group_II,
    COUNTIF(mag_field_month_rci_group = "III") as magm_rci_group_III,
    COUNTIF(mag_field_month_rci_group = "IV") as magm_rci_group_IV,
    COUNTIF(mag_field_month_rci_group = "V") as magm_rci_group_V,
    COUNTIF(mag_field_month_rci_group = "VI") as magm_rci_group_VI,
    COUNTIF(mag_field_month_percentile_group = "1") as magm_centile_1,
    COUNTIF(mag_field_month_percentile_group = "5") as magm_centile_5,
    COUNTIF(mag_field_month_percentile_group = "10") as magm_centile_10,
    COUNTIF(mag_field_month_percentile_group = "25") as magm_centile_25,
    COUNTIF(mag_field_month_percentile_group = "50") as magm_centile_50,
    COUNTIF(mag_field_month_percentile_group = "Other") as magm_centile_other,

    COUNTIF(oc_field_year_rci_group = "0") as ocy_rci_group_0,
    COUNTIF(oc_field_year_rci_group = "I") as ocy_rci_group_I,
    COUNTIF(oc_field_year_rci_group = "II") as ocy_rci_group_II,
    COUNTIF(oc_field_year_rci_group = "III") as ocy_rci_group_III,
    COUNTIF(oc_field_year_rci_group = "IV") as ocy_rci_group_IV,
    COUNTIF(oc_field_year_rci_group = "V") as ocy_rci_group_V,
    COUNTIF(oc_field_year_rci_group = "VI") as ocy_rci_group_VI,
    COUNTIF(oc_field_year_percentile_group = "1") as ocy_centile_1,
    COUNTIF(oc_field_year_percentile_group = "5") as ocy_centile_5,
    COUNTIF(oc_field_year_percentile_group = "10") as ocy_centile_10,
    COUNTIF(oc_field_year_percentile_group = "25") as ocy_centile_25,
    COUNTIF(oc_field_year_percentile_group = "50") as ocy_centile_50,
    COUNTIF(oc_field_year_percentile_group = "Other") as ocy_centile_other,

    COUNTIF(oc_field_month_rci_group = "0") as ocm_rci_group_0,
    COUNTIF(oc_field_month_rci_group = "I") as ocm_rci_group_I,
    COUNTIF(oc_field_month_rci_group = "II") as ocm_rci_group_II,
    COUNTIF(oc_field_month_rci_group = "III") as ocm_rci_group_III,
    COUNTIF(oc_field_month_rci_group = "IV") as ocm_rci_group_IV,
    COUNTIF(oc_field_month_rci_group = "V") as ocm_rci_group_V,
    COUNTIF(oc_field_month_rci_group = "VI") as ocm_rci_group_VI,
    COUNTIF(oc_field_month_percentile_group = "1") as ocm_centile_1,
    COUNTIF(oc_field_month_percentile_group = "5") as ocm_centile_5,
    COUNTIF(oc_field_month_percentile_group = "10") as ocm_centile_10,
    COUNTIF(oc_field_month_percentile_group = "25") as ocm_centile_25,
    COUNTIF(oc_field_month_percentile_group = "50") as ocm_centile_50,
    COUNTIF(oc_field_month_percentile_group = "Other") as ocm_centile_other,

    COUNTIF(oc2y_field_year_rci_group = "0") as oc2yy_rci_group_0,
    COUNTIF(oc2y_field_year_rci_group = "I") as oc2yy_rci_group_I,
    COUNTIF(oc2y_field_year_rci_group = "II") as oc2yy_rci_group_II,
    COUNTIF(oc2y_field_year_rci_group = "III") as oc2yy_rci_group_III,
    COUNTIF(oc2y_field_year_rci_group = "IV") as oc2yy_rci_group_IV,
    COUNTIF(oc2y_field_year_rci_group = "V") as oc2yy_rci_group_V,
    COUNTIF(oc2y_field_year_rci_group = "VI") as oc2yy_rci_group_VI,
    COUNTIF(oc2y_field_year_percentile_group = "1") as oc2yy_centile_1,
    COUNTIF(oc2y_field_year_percentile_group = "5") as oc2yy_centile_5,
    COUNTIF(oc2y_field_year_percentile_group = "10") as oc2yy_centile_10,
    COUNTIF(oc2y_field_year_percentile_group = "25") as oc2yy_centile_25,
    COUNTIF(oc2y_field_year_percentile_group = "50") as oc2yy_centile_50,
    COUNTIF(oc2y_field_year_percentile_group = "Other") as oc2yy_centile_other,

    COUNTIF(oc2y_field_month_rci_group = "0") as oc2ym_rci_group_0,
    COUNTIF(oc2y_field_month_rci_group = "I") as oc2ym_rci_group_I,
    COUNTIF(oc2y_field_month_rci_group = "II") as oc2ym_rci_group_II,
    COUNTIF(oc2y_field_month_rci_group = "III") as oc2ym_rci_group_III,
    COUNTIF(oc2y_field_month_rci_group = "IV") as oc2ym_rci_group_IV,
    COUNTIF(oc2y_field_month_rci_group = "V") as oc2ym_rci_group_V,
    COUNTIF(oc2y_field_month_rci_group = "VI") as oc2ym_rci_group_VI,
    COUNTIF(oc2y_field_month_percentile_group = "1") as oc2ym_centile_1,
    COUNTIF(oc2y_field_month_percentile_group = "5") as oc2ym_centile_5,
    COUNTIF(oc2y_field_month_percentile_group = "10") as oc2ym_centile_10,
    COUNTIF(oc2y_field_month_percentile_group = "25") as oc2ym_centile_25,
    COUNTIF(oc2y_field_month_percentile_group = "50") as oc2ym_centile_50,
    COUNTIF(oc2y_field_month_percentile_group = "Other") as oc2ym_centile_other,

    COUNTIF(oc2y_field_month_rci_group = "0") as oc2ym_rci_group_0,
    COUNTIF(oc2y_field_month_rci_group = "I") as oc2ym_rci_group_I,
    COUNTIF(oc2y_field_month_rci_group = "II") as oc2ym_rci_group_II,
    COUNTIF(oc2y_field_month_rci_group = "III") as oc2ym_rci_group_III,
    COUNTIF(oc2y_field_month_rci_group = "IV") as oc2ym_rci_group_IV,
    COUNTIF(oc2y_field_month_rci_group = "V") as oc2ym_rci_group_V,
    COUNTIF(oc2y_field_month_rci_group = "VI") as oc2ym_rci_group_VI,
    COUNTIF(oc2y_field_month_percentile_group = "1") as oc2ym_centile_1,
    COUNTIF(oc2y_field_month_percentile_group = "5") as oc2ym_centile_5,
    COUNTIF(oc2y_field_month_percentile_group = "10") as oc2ym_centile_10,
    COUNTIF(oc2y_field_month_percentile_group = "25") as oc2ym_centile_25,
    COUNTIF(oc2y_field_month_percentile_group = "50") as oc2ym_centile_50,
    COUNTIF(oc2y_field_month_percentile_group = "Other") as oc2ym_centile_other,

FROM `coki-scratch-space.curtin.schools_outputs_deduped` as schools
    INNER JOIN `academic-observatory.observatory.doi20210626` as d on schools.doi = d.doi
    JOIN metrics as m on d.doi=m.doi

GROUP BY crossref.published_year, school
ORDER BY crossref.published_year DESC, school ASC

