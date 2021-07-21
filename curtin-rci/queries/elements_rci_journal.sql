CREATE TEMP FUNCTION compute_percentiles(counts ARRAY<INT64>) AS (
  (SELECT as STRUCT
    ROUND(PERCENTILE_CONT(count, 0.50) OVER(), 2) as MAG_Citations_Median_PerRow,
    ROUND(PERCENTILE_CONT(count, 0.75) OVER(), 2) as MAG_Citations_Cent75_PerRow,
    ROUND(PERCENTILE_CONT(count, 0.90) OVER(), 2) as MAG_Citations_Cent90_PerRow,
    ROUND(PERCENTILE_CONT(count, 0.95) OVER(), 2) as MAG_Citations_Cent95_PerRow,
    ROUND(PERCENTILE_CONT(count, 0.99) OVER(), 2) as MAG_Citations_Cent99_PerRow
  FROM UNNEST(counts) as count LIMIT 1)
);

WITH

doi_table_with_imputed_journal AS (
    SELECT
        doi,
        crossref.published_year as published_year,
        mag.CitationCount as CitationCount,
        CASE
            WHEN mag.journal.JournalId is not null then CONCAT('j-', mag.journal.JournalId)
            WHEN mag.conferenceSeries.ConferenceSeriesId is not null then CONCAT('cs-', mag.conferenceSeries.ConferenceSeriesId)
            WHEN mag.conferenceInstance.ConferenceInstanceId is not null then CONCAT('ci-', mag.conferenceInstance.ConferenceInstanceId)
            ELSE null
        END as container_id,
        FROM `academic-observatory.observatory.doi20210626`
        -- WHERE "Australia" in (SELECT name from UNNEST(affiliations.countries))

),
benchmarks_by_container_year AS (
    SELECT
        container_id,
        published_year,
        compute_percentiles(ARRAY_AGG(CitationCount)).*,
        AVG(CitationCount) as mean
    FROM doi_table_with_imputed_journal
    GROUP BY container_id, published_year
),

metrics_by_doi as (
    SELECT
        doi,
        d.published_year,
        d.container_id,
        CitationCount,
        CASE
            WHEN CitationCount >= MAG_Citations_Cent99_PerRow THEN "1"
            WHEN CitationCount >= MAG_Citations_Cent95_PerRow THEN "5"
            WHEN CitationCount >= MAG_Citations_Cent90_PerRow THEN "10"
            WHEN CitationCount >= MAG_Citations_Cent75_PerRow THEN "25"
            WHEN CitationCount >= MAG_Citations_Median_PerRow THEN "50"
            ELSE "Other"
        END as mag_percentile_group,
        CASE
            WHEN CitationCount = 0 THEN "0"
            WHEN CitationCount / mean < 0.8 THEN "I"
            WHEN CitationCount / mean < 1.2 THEN "II"
            WHEN CitationCount / mean < 2 THEN "III"
            WHEN CitationCount / mean < 4 THEN "IV"
            WHEN CitationCount / mean < 8 THEN "V"
            ELSE "VI"
        END as mag_rci_group

    FROM doi_table_with_imputed_journal as d JOIN benchmarks_by_container_year as b on
        d.published_year = b.published_year
        AND d.container_id = b.container_id
    WHERE
        d.container_id is not null
)

SELECT
    published_year,
    school,
    COUNT(DISTINCT schools.doi) as total_outputs,
    SUM(CitationCount) as total_citations,
    COUNTIF(mag_rci_group = "0") as rci_group_0,
    COUNTIF(mag_rci_group = "I") as rci_group_I,
    COUNTIF(mag_rci_group = "II") as rci_group_II,
    COUNTIF(mag_rci_group = "III") as rci_group_III,
    COUNTIF(mag_rci_group = "IV") as rci_group_IV,
    COUNTIF(mag_rci_group = "V") as rci_group_V,
    COUNTIF(mag_rci_group = "VI") as rci_group_VI,
    COUNTIF(mag_percentile_group = "1") as mag_centile_1,
    COUNTIF(mag_percentile_group = "5") as mag_centile_5,
    COUNTIF(mag_percentile_group = "10") as mag_centile_10,
    COUNTIF(mag_percentile_group = "25") as mag_centile_25,
    COUNTIF(mag_percentile_group = "50") as mag_centile_50,
    COUNTIF(mag_percentile_group = "Other") as mag_centile_other

FROM `coki-scratch-space.curtin.combined_deduped` as schools
INNER JOIN metrics_by_doi as metrics on schools.doi=metrics.doi

GROUP BY published_year, school
ORDER BY published_year DESC, school ASC