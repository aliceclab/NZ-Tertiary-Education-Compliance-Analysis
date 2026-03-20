-- =========================================================
-- business_analysis.sql
-- NZ Tertiary Education Compliance and Retention Analysis
-- Business-facing SQL analysis for retention risk
-- =========================================================

USE project3_sdr;

-- ---------------------------------------------------------
-- 1. Retention risk by faculty
-- ---------------------------------------------------------
SELECT
    Faculty,
    COUNT(*) AS response_count,
    ROUND(AVG(Retention_Likelihood), 2) AS avg_retention_likelihood
FROM student_survey
GROUP BY Faculty
ORDER BY avg_retention_likelihood ASC;

SELECT
    Faculty,
    COUNT(*) AS response_count,
    ROUND(AVG(Teaching_Score), 2) AS avg_teaching_score,
    ROUND(AVG(Support_Score), 2) AS avg_support_score,
    ROUND(AVG(Sense_of_Belonging), 2) AS avg_belonging_score,
    ROUND(AVG(Retention_Likelihood), 2) AS avg_retention_likelihood
FROM student_survey
GROUP BY Faculty
ORDER BY avg_retention_likelihood ASC;

SELECT
    Faculty,
    COUNT(*) AS total_responses,
    SUM(CASE WHEN Retention_Likelihood <= 5 THEN 1 ELSE 0 END) AS low_retention_count,
    ROUND(
        SUM(CASE WHEN Retention_Likelihood <= 5 THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS low_retention_pct
FROM student_survey
GROUP BY Faculty
ORDER BY low_retention_pct DESC;

-- ---------------------------------------------------------
-- 2. Retention risk by ethnicity
-- ---------------------------------------------------------
SELECT
    Ethnicity,
    COUNT(*) AS response_count,
    ROUND(AVG(Retention_Likelihood), 2) AS avg_retention_likelihood
FROM student_survey
GROUP BY Ethnicity
ORDER BY avg_retention_likelihood ASC;

SELECT
    Ethnicity,
    COUNT(*) AS response_count,
    ROUND(AVG(Support_Score), 2) AS avg_support_score,
    ROUND(AVG(Sense_of_Belonging), 2) AS avg_belonging_score,
    ROUND(AVG(Retention_Likelihood), 2) AS avg_retention_likelihood
FROM student_survey
GROUP BY Ethnicity
ORDER BY avg_retention_likelihood ASC;

SELECT
    Ethnicity,
    COUNT(*) AS total_responses,
    SUM(CASE WHEN Retention_Likelihood <= 5 THEN 1 ELSE 0 END) AS low_retention_count,
    ROUND(
        SUM(CASE WHEN Retention_Likelihood <= 5 THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS low_retention_pct
FROM student_survey
WHERE Ethnicity IS NOT NULL
  AND TRIM(Ethnicity) <> ''
GROUP BY Ethnicity
ORDER BY low_retention_pct DESC;

-- ---------------------------------------------------------
-- 3. Retention risk by citizenship status
-- ---------------------------------------------------------
SELECT
    Citizenship_Status,
    COUNT(*) AS response_count,
    ROUND(AVG(Teaching_Score), 2) AS avg_teaching_score,
    ROUND(AVG(Support_Score), 2) AS avg_support_score,
    ROUND(AVG(Sense_of_Belonging), 2) AS avg_belonging_score,
    ROUND(AVG(Admin_Experience), 2) AS avg_admin_score,
    ROUND(AVG(Retention_Likelihood), 2) AS avg_retention_likelihood
FROM student_survey
GROUP BY Citizenship_Status
ORDER BY avg_retention_likelihood ASC;

SELECT
    Citizenship_Status,
    COUNT(*) AS total_responses,
    SUM(CASE WHEN Retention_Likelihood <= 5 THEN 1 ELSE 0 END) AS low_retention_count,
    ROUND(
        SUM(CASE WHEN Retention_Likelihood <= 5 THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS low_retention_pct
FROM student_survey
GROUP BY Citizenship_Status
ORDER BY low_retention_pct DESC;

-- ---------------------------------------------------------
-- 4. Citizenship by year of study
-- ---------------------------------------------------------
SELECT
    Citizenship_Status,
    Year_of_Study,
    COUNT(*) AS response_count,
    ROUND(AVG(Retention_Likelihood), 2) AS avg_retention_likelihood
FROM student_survey
GROUP BY Citizenship_Status, Year_of_Study
ORDER BY Citizenship_Status, Year_of_Study;
