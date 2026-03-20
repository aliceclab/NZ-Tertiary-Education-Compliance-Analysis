-- =========================================================
-- validation_checks.sql
-- NZ Tertiary Education Compliance and Retention Analysis
-- SQL validation checks for SDR-style data quality issues
-- =========================================================

-- Use the project database
USE project3_sdr;

-- ---------------------------------------------------------
-- Row count checks
-- ---------------------------------------------------------
SELECT COUNT(*) AS learner_count
FROM sdr_lear;

SELECT COUNT(*) AS enrolment_count
FROM sdr_enrl;

SELECT COUNT(*) AS survey_response_count
FROM student_survey;

SELECT COUNT(*) AS expected_error_count
FROM expected_errors;

-- ---------------------------------------------------------
-- E01: Invalid NSN length
-- Expected: 15
-- ---------------------------------------------------------
SELECT COUNT(*) AS e01_nsn_invalid_count
FROM sdr_lear
WHERE CHAR_LENGTH(NSN) <> 10;

-- ---------------------------------------------------------
-- E02: Missing ethnicity
-- Expected: 20
-- ---------------------------------------------------------
SELECT COUNT(*) AS e02_ethnicity_missing_count
FROM sdr_lear
WHERE Ethnicity IS NULL OR TRIM(Ethnicity) = '';

-- ---------------------------------------------------------
-- E03: Future DOB
-- Expected: 5
-- Reference date: 2024-07-01
-- ---------------------------------------------------------
SELECT COUNT(*) AS e03_future_dob_count
FROM sdr_lear
WHERE DOB > '2024-07-01';

-- ---------------------------------------------------------
-- E04: Under 16 as at 2024-07-01
-- Expected: 5
-- ---------------------------------------------------------
SELECT COUNT(*) AS e04_under_16_count
FROM sdr_lear
WHERE DOB IS NOT NULL
  AND DOB <= '2024-07-01'
  AND YEAR('2024-07-01') - YEAR(DOB) < 16;

-- ---------------------------------------------------------
-- E05: Missing gender
-- Expected: 10
-- ---------------------------------------------------------
SELECT COUNT(*) AS e05_gender_missing_count
FROM sdr_lear
WHERE Gender IS NULL OR TRIM(Gender) = '';

-- ---------------------------------------------------------
-- E06: End date before start date
-- Expected: 30
-- ---------------------------------------------------------
SELECT COUNT(*) AS e06_invalid_date_range
FROM sdr_enrl
WHERE End_Date < Start_Date;

-- ---------------------------------------------------------
-- E07: Overlapping enrolments
-- Initial rule over-detected exceptions
-- Detected: 4077
-- Expected error log: 40
-- This check is retained as a refinement example
-- ---------------------------------------------------------
SELECT COUNT(*) AS e07_overlap_count
FROM (
    SELECT
        a.NSN,
        a.Course_Code,
        a.Term,
        a.Start_Date,
        a.End_Date,
        b.Course_Code AS course_b
    FROM sdr_enrl a
    JOIN sdr_enrl b
        ON a.NSN = b.NSN
       AND a.Term = b.Term
       AND a.Course_Code < b.Course_Code
       AND a.Start_Date <= b.End_Date
       AND a.End_Date >= b.Start_Date
) t;

-- ---------------------------------------------------------
-- E08: EFTS greater than 1.0
-- Expected: 20
-- ---------------------------------------------------------
SELECT COUNT(*) AS e08_efts_too_high_count
FROM sdr_enrl
WHERE EFTS > 1.0;

-- ---------------------------------------------------------
-- E09: International learners with domestic-only funding code
-- Expected: 25
-- ---------------------------------------------------------
SELECT COUNT(*) AS e09_invalid_funding_code_count
FROM sdr_enrl e
JOIN sdr_lear l
  ON e.NSN = l.NSN
WHERE l.Citizenship_Status = 'International'
  AND e.Funding_Code IN ('S01', 'S02', 'S03');

-- ---------------------------------------------------------
-- E10: Exact duplicate enrolment rows
-- Expected: 15
-- ---------------------------------------------------------
SELECT COUNT(*) AS e10_duplicate_enrolment_count
FROM (
    SELECT
        NSN,
        Course_Code,
        Faculty,
        Academic_Year,
        Term,
        Start_Date,
        End_Date,
        EFTS,
        Funding_Code,
        Completion_Status,
        Delivery_Mode,
        COUNT(*) AS duplicate_count
    FROM sdr_enrl
    GROUP BY
        NSN,
        Course_Code,
        Faculty,
        Academic_Year,
        Term,
        Start_Date,
        End_Date,
        EFTS,
        Funding_Code,
        Completion_Status,
        Delivery_Mode
    HAVING COUNT(*) > 1
) d;

-- ---------------------------------------------------------
-- E11: Missing faculty
-- Expected: 15
-- ---------------------------------------------------------
SELECT COUNT(*) AS e11_missing_faculty_count
FROM sdr_enrl
WHERE Faculty IS NULL OR TRIM(Faculty) = '';

-- ---------------------------------------------------------
-- Expected error counts from ground-truth table
-- ---------------------------------------------------------
SELECT Error_Code, COUNT(*) AS expected_count
FROM expected_errors
GROUP BY Error_Code
ORDER BY Error_Code;

-- ---------------------------------------------------------
-- Detected counts summary (E01-E08)
-- ---------------------------------------------------------
SELECT 'E01' AS Error_Code, 15 AS detected_count
UNION ALL
SELECT 'E02', 20
UNION ALL
SELECT 'E03', 5
UNION ALL
SELECT 'E04', 5
UNION ALL
SELECT 'E05', 10
UNION ALL
SELECT 'E06', 30
UNION ALL
SELECT 'E07', 4077
UNION ALL
SELECT 'E08', 20;

-- ---------------------------------------------------------
-- Validation comparison: expected vs detected
-- ---------------------------------------------------------
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

-- ---------------------------------------------------------
-- Validation comparison: expected vs detected (E09-E11)
-- ---------------------------------------------------------
SELECT
    e.Error_Code,
    e.expected_count,
    d.detected_count,
    d.detected_count - e.expected_count AS difference
FROM (
    SELECT Error_Code, COUNT(*) AS expected_count
    FROM expected_errors
    WHERE Error_Code IN ('E09','E10','E11')
    GROUP BY Error_Code
) e
LEFT JOIN (
    SELECT 'E09' AS Error_Code, 25 AS detected_count
    UNION ALL SELECT 'E10', 15
    UNION ALL SELECT 'E11', 15
) d
ON e.Error_Code = d.Error_Code
ORDER BY e.Error_Code;
