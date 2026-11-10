use WorldBank_Analytics
select * from [dbo].[WorldBankData]
USE WorldBank_Analytics;
GO

SELECT
    'worldbank_global_cleaned' AS Table_Name,
    COUNT(*) AS Total_Records
FROM dbo.worldbank_global_cleaned

UNION ALL

SELECT
    'WorldBankData',
    COUNT(*)
FROM dbo.WorldBankData;


select 
count(*) as total_records,
count(distinct country_code) as total_countries,
count(distinct indicator_code) as total_indocators,
min(year) as first_year,
max(year) as last_year
from [dbo].[worldbank_global_cleaned]

select 
indicator_category,
count(*) as total_records,
count(value) as available_values,
sum(case when value is null then 1 else 0 end) as missing_values
from[dbo].[worldbank_global_cleaned]
group by indicator_category
order by indicator_category

SELECT
    Country_Code,
    Year,
    Indicator_Code,
    COUNT(*) AS Duplicate_Count
FROM [dbo].[worldbank_global_cleaned]
GROUP BY Country_Code, Year, Indicator_Code
HAVING COUNT(*) > 1;



select
country_name,
count(*) as total_records,
sum(case when value is null then 1 else 0 end ) as missing_values,
count(value) as available_values,
cast(100*sum(case when value is null then 1 else 0 end)/count(*) as decimal (5,2)) as missing_percentage
from [dbo].[worldbank_global_cleaned]
GROUP BY Country_Name

ORDER BY Missing_Values DESC;
SELECT
    Indicator_Name,
    Indicator_Category,

    COUNT(*) AS Total_Records,

    COUNT(Value) AS Available_Values,

min(case when value is not null then year end ) as first_available_year,
max(case when value is not null then year end) as last_available_year,
cast(
100*count(value)/count(*) as decimal (5,2) ) as coverage_percentage
from [dbo].[worldbank_global_cleaned]
group by indicator_name,
indicator_category
order by 
coverage_percentage desc

select 
top 10
country_name,
value as gdp_growth_percentage
from[dbo].[worldbank_global_cleaned]
where
indicator_category = 'gdp growth'
and year = 2024
and value is not null
order by value desc

SELECT TOP 10
    Country_Name,
    Value AS GDP_Growth_Percentage

FROM dbo.worldbank_global_cleaned

WHERE
    Indicator_Category = 'GDP_Growth'
    AND Year = 2024
    AND Value IS NOT NULL

ORDER BY Value DESC;

select 
top 10
country_name,
round(value,2) as gdp_per_capita_usd
from [dbo].[worldbank_global_cleaned]
where indicator_category = 'gdp_per_capita'
and year = 2024
and value is not null
order by value desc

with populationcomparison as 
( 
select
country_name,
max(case
when year = 2000 then value end ) as population_2000,
max(case
when year = 2024 then value end ) as population_2024
from[dbo].[worldbank_global_cleaned]
where 
indicator_category = 'population'
and year in (2000, 2024)
group by country_name
)
select 
top 10
country_name,
round(population_2000,0) as population_2000,
round(population_2024,0) as population_2024,

round(
(population_2024-population_2000)*100/ nullif(population_2000,0),2) as population_growth_percentage
from populationcomparison
WHERE Population_2000 IS NOT NULL
  AND Population_2024 IS NOT NULL

ORDER BY Population_Growth_Percentage DESC;

9
select 
top 10 
country_name,
round(
value/1000000000000,3) as gdp_trillion_usd
from[dbo].[worldbank_global_cleaned]
where indicator_category = 'gdp_current_usd'
and year = 2024
and value is not null
order by value desc

10
select 
year ,
round(value,2) as gdp_growth_percentage
from [dbo].[worldbank_global_cleaned]
where country_name= 'India'
and indicator_category = 'gdp_growth'
and value is not null
order by year

11
select
country_name,
round(value,2) as gdp_growth_percentae
from[dbo].[worldbank_global_cleaned]
where indicator_category = 'gdp_growth'
and year = 2024
and value < 0
order by value asc

12
select 
country_name,
round(avg(value),2) as average_gdp_growth
from [dbo].[worldbank_global_cleaned]
where indicator_category = 'gdp_growth'
and value is not null
group by country_name
order by average_gdp_growth desc

13
select 
top 10
country_name,
round(value,2) as life_expextancy
from[dbo].[worldbank_global_cleaned]
where indicator_category = 'life_expectancy'
and year = 2024
and value is not null
order by value desc

14
select 
top 10
country_name,
round(value,2) as life_expextancy
from[dbo].[worldbank_global_cleaned]
where indicator_category = 'life_expectancy'
and year = 2024
and value is not null
order by value asc

15
with lifecomparison as 
( select
country_name,
max(case when year = 2000 then value end ) as life_expectancy_2000,
max(case when year = 2024 then value end ) as life_expectancy_2024
from[dbo].[worldbank_global_cleaned]
where 
indicator_category = 'life_expectancy'
and year in (2000,2024)
group by country_name
)
select 
top 10
country_name,
round(life_expectancy_2000,2) as life_expectancy_2000,
round(life_expectancy_2024,2) as life_expectancy_2024,
round(life_expectancy_2024-life_expectancy_2000,2) as improvement_years
from lifecomparison
WHERE Life_Expectancy_2000 IS NOT NULL
  AND Life_Expectancy_2024 IS NOT NULL

ORDER BY Improvement_Years DESC;
16
select
country_name,
round(value,2) as gdp_per_capita_usd
from[dbo].[worldbank_global_cleaned]
where country_name in ('india','china','united states')
and indicator_category = 'gdp_per_capita'
and year = 2024
order by value desc
17
select 
country_name,
round(value,2) as agricultural_gdp_percentage
from[dbo].[worldbank_global_cleaned]

where indicator_category = 'agriculture_gdp'
and year = 2024
and value is not null
order by value desc
18
SELECT TOP 10
    Country_Name,
    ROUND(Value, 2) AS Cereal_Yield_KG_Per_Hectare
FROM dbo.worldbank_global_cleaned
WHERE Indicator_Category = 'Cereal_Yield'
  AND Year = 2024
  AND Value IS NOT NULL
ORDER BY Value DESC;

19
select 
top 15 
country_name,
round(value,2) as agriculture_employment_percentage
from [dbo].[worldbank_global_cleaned]
where indicator_category = 'agriculture_employment'
and year = 2024 
and value is not null 
order by value desc

20
SELECT TOP 10
    L.Country_Name,

    ROUND(L.Value, 2) AS Life_Expectancy,

    ROUND(H.Value, 2) AS Healthcare_Expenditure_Percentage

FROM dbo.worldbank_global_cleaned L

INNER JOIN dbo.worldbank_global_cleaned H
    ON L.Country_Code = H.Country_Code
    AND L.Year = H.Year

WHERE L.Indicator_Category = 'Life_Expectancy'
  AND H.Indicator_Category = 'Health_Expenditure'
  AND L.Year = 2024
  AND L.Value IS NOT NULL
  AND H.Value IS NOT NULL

ORDER BY L.Value DESC;

21
with latestpoverty as
(
select
country_name,
year,
value,
row_number() over (
partition by country_code
order by year desc) as rn
from [dbo].[worldbank_global_cleaned]
where Indicator_Category = 'poverty_rate'
and value is not null
)
select
top 10
country_name,
year,
round(value,2) as poverty_rate_percentage
from latestpoverty
where rn =1 
order by value desc

22
select 
year,
round(value,2)as poverty_rate_percentage
from [dbo].[worldbank_global_cleaned]
where Country_name = 'india'
and Indicator_Category = 'poverty_rate'
and value is not null
order by value desc

23
select 
country_name,
count(value) as available_years,
round(avg(value),2) as average_gdp_growth,
round(stdev(value),2)as gdp_growth_volatility
from [dbo].[worldbank_global_cleaned]
where Indicator_Category= 'gdp_growth'
and value is not null
group by Country_Name
having count(value)>=15
order by gdp_growth_volatility desc

24
select 
year,
round(avg(value),2) as avergae_country_gdp_growth,
round(
max(case
when country_name = 'india'then value end ),2
) as india_gdp_growth
from [dbo].[worldbank_global_cleaned]
where Indicator_Category = 'gdp_growth'
and value is not null
group by year
order by year
25
with agriculturedata as 
(
select 
country_code,
country_name,
max(case
when indicator_category = 'agriculture_gdp'
then year end) as gdp_year,
max(case
when indicator_category = 'agriculture_gdp'
then value end) as agriculture_gdp_percentage,
max(case
when indicator_category = 'agriculture_employment'
then year end) as employment_year,
max(case
when indicator_category = 'agriculture_employment'
then value end) as Agriculture_Employment_Percentage
from [dbo].[worldbank_global_cleaned]
   WHERE Indicator_Category IN
        ('Agriculture_GDP', 'Agriculture_Employment')
      AND Value IS NOT NULL
    GROUP BY Country_Code, Country_Name
)
SELECT
    Country_Name,
    GDP_Year,
    ROUND(Agriculture_GDP_Percentage, 2)
        AS Agriculture_GDP_Percentage,
    Employment_Year,
    ROUND(Agriculture_Employment_Percentage, 2)
        AS Agriculture_Employment_Percentage
FROM AgricultureData
WHERE Agriculture_GDP_Percentage IS NOT NULL
  AND Agriculture_Employment_Percentage IS NOT NULL
ORDER BY Agriculture_GDP_Percentage DESC;  

26
SELECT
    Year,

    MAX(CASE
        WHEN Indicator_Category = 'Agriculture_GDP'
        THEN Value
    END) AS Agriculture_GDP_Percentage,

    MAX(CASE
        WHEN Indicator_Category = 'Agriculture_Employment'
        THEN Value
    END) AS Agriculture_Employment_Percentage,

    MAX(CASE
        WHEN Indicator_Category = 'Cereal_Yield'
        THEN Value
    END) AS Cereal_Yield_KG_Per_Hectare

FROM dbo.worldbank_global_cleaned
WHERE Country_Name = 'India'
  AND Indicator_Category IN
  (
      'Agriculture_GDP',
      'Agriculture_Employment',
      'Cereal_Yield'
  )
GROUP BY Year
ORDER BY Year;

27
select 
top 15
country_name,
round(value,2)as healthcare_expenditure_percentage
from [dbo].[worldbank_global_cleaned]
where Indicator_Category = 'health_expenditure'
and year = 2024
and value is not null
order by value desc

28
select
country_name,
year,
cast(value/1000000 as decimal(12,2))
as population_millions
from [dbo].[worldbank_global_cleaned]
where country_name in 
('india', 'china', 'united states')
and Indicator_Category = 'population'
and year in (2000,2005,2010,2020,2024)
order by year , country_name

29
WITH CountryDevelopment AS
(
    SELECT
        Country_Code,
        Country_Name,

        MAX(CASE
            WHEN Indicator_Category = 'GDP_Per_Capita'
            THEN Value
        END) AS GDP_Per_Capita,

        MAX(CASE
            WHEN Indicator_Category = 'Life_Expectancy'
            THEN Value
        END) AS Life_Expectancy

    FROM dbo.worldbank_global_cleaned
    WHERE Year = 2024
      AND Indicator_Category IN
      ('GDP_Per_Capita', 'Life_Expectancy')
    GROUP BY Country_Code, Country_Name
)
SELECT
    Country_Name,
    ROUND(GDP_Per_Capita, 2) AS GDP_Per_Capita_USD,
    ROUND(Life_Expectancy, 2) AS Life_Expectancy,

    CASE
        WHEN GDP_Per_Capita >= 30000
             AND Life_Expectancy >= 75
            THEN 'High Development Indicators'

        WHEN GDP_Per_Capita >= 10000
             AND Life_Expectancy >= 70
            THEN 'Upper-Middle Indicators'

        WHEN GDP_Per_Capita >= 3000
             AND Life_Expectancy >= 60
            THEN 'Developing Indicators'

        ELSE 'Lower Development Indicators'
    END AS Development_Category

FROM CountryDevelopment
WHERE GDP_Per_Capita IS NOT NULL
  AND Life_Expectancy IS NOT NULL
ORDER BY GDP_Per_Capita DESC;



30
WITH CountrySummary AS
(
    SELECT
        Country_Code,
        Country_Name,

        MAX(CASE
            WHEN Indicator_Category = 'GDP_Current_USD'
            THEN Value
        END) AS GDP_USD,

        MAX(CASE
            WHEN Indicator_Category = 'GDP_Growth'
            THEN Value
        END) AS GDP_Growth,

        MAX(CASE
            WHEN Indicator_Category = 'GDP_Per_Capita'
            THEN Value
        END) AS GDP_Per_Capita,

        MAX(CASE
            WHEN Indicator_Category = 'Population'
            THEN Value
        END) AS Population,

        MAX(CASE
            WHEN Indicator_Category = 'Life_Expectancy'
            THEN Value
        END) AS Life_Expectancy,

        MAX(CASE
            WHEN Indicator_Category = 'Health_Expenditure'
            THEN Value
        END) AS Healthcare_Expenditure,

        MAX(CASE
            WHEN Indicator_Category = 'Agriculture_GDP'
            THEN Value
        END) AS Agriculture_GDP,

        MAX(CASE
            WHEN Indicator_Category = 'Agriculture_Employment'
            THEN Value
        END) AS Agriculture_Employment,

        MAX(CASE
            WHEN Indicator_Category = 'Cereal_Yield'
            THEN Value
        END) AS Cereal_Yield,

        MAX(CASE
            WHEN Indicator_Category = 'Poverty_Rate'
            THEN Value
        END) AS Poverty_Rate

    FROM dbo.worldbank_global_cleaned
    WHERE Year = 2024
    GROUP BY Country_Code, Country_Name
)

SELECT
    Country_Code,
    Country_Name,

    ROUND(GDP_USD / 1000000000.0, 2)
        AS GDP_Billion_USD,

    ROUND(GDP_Growth, 2)
        AS GDP_Growth_Percentage,

    ROUND(GDP_Per_Capita, 2)
        AS GDP_Per_Capita_USD,

    CAST(Population / 1000000.0 AS DECIMAL(12,2))
        AS Population_Millions,

    ROUND(Life_Expectancy, 2)
        AS Life_Expectancy,

    ROUND(Healthcare_Expenditure, 2)
        AS Healthcare_Expenditure_Percentage,

    ROUND(Agriculture_GDP, 2)
        AS Agriculture_GDP_Percentage,

    ROUND(Agriculture_Employment, 2)
        AS Agriculture_Employment_Percentage,

    ROUND(Cereal_Yield, 2)
        AS Cereal_Yield,

    ROUND(Poverty_Rate, 2)
        AS Poverty_Rate_Percentage

FROM CountrySummary
ORDER BY GDP_USD DESC;