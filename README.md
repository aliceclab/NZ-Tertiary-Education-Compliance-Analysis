# NZ-Tertiary-Education-Compliance-and-Retention-Analysis

A portfolio project combining SQL-based SDR validation and Power BI dashboarding to identify retention risk and student experience gaps in a New Zealand tertiary education setting.

## Business Case

This project simulates a realistic scenario for a New Zealand tertiary education provider that needs to:

1. validate SDR-related learner and enrolment data before reporting, and
2. analyse student experience survey data to identify retention risk patterns across faculties and student groups.

The goal was to combine compliance-focused SQL checks with business-facing dashboard insights for non-technical stakeholders.

## Tools Used

- Python
- MySQL
- Power BI
- CSV flat files

## Dataset Overview

This project uses four synthetic datasets:

- `SDR_LEAR.csv` — learner-level demographic and profile data
- `SDR_ENRL.csv` — enrolment-level records for courses, dates, EFTS, and funding information
- `STUDENT_SURVEY.csv` — student experience survey responses, including teaching, support, belonging, administrative experience, and retention likelihood
- `EXPECTED_ERRORS.csv` — ground-truth injected error log used to validate SQL detection logic

## SQL Validation Layer

I built a set of SQL validation checks to test common SDR-style data quality issues, including:

- invalid NSN format
- missing ethnicity
- future DOB
- learners under 16
- missing gender
- end date before start date
- overlapping enrolment logic
- EFTS above expected threshold
- international students with domestic-only funding code
- exact duplicate enrolment rows
- missing faculty

Most validation checks matched the injected error log exactly. The overlap rule initially over-detected exceptions, so I treated it as a refinement item rather than forcing an inaccurate final rule.

### Validation Comparison

![Validation comparison](screenshots/validation_expected_vs_detected.png)

### Example SQL

```sql
SELECT
    e.Error_Code,
    e.expected_count,
    d.detected_count,
    d.detected_count - e.expected_count AS difference
FROM (
    SELECT Error_Code, COUNT(*) AS expected_count
    FROM expected_errors
    WHERE Error_Code IN ('E01','E02','E03','E04','E05','E06','E07','E08')
    GROUP BY Error_Code
) e
LEFT JOIN (
    SELECT 'E01' AS Error_Code, 15 AS detected_count
    UNION ALL SELECT 'E02', 20
    UNION ALL SELECT 'E03', 5
    UNION ALL SELECT 'E04', 5
    UNION ALL SELECT 'E05', 10
    UNION ALL SELECT 'E06', 30
    UNION ALL SELECT 'E07', 4077
    UNION ALL SELECT 'E08', 20
) d
ON e.Error_Code = d.Error_Code
ORDER BY e.Error_Code;
