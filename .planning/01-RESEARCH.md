# **Technical Specification and Data Inventory for the LA Metro Ridership Impact Analysis**

The longitudinal assessment of transit infrastructure investment requires a rigorous alignment of disparate datasets, particularly when evaluating the specific socio-economic and ridership outcomes of the Gold Line Foothill Extension Phase 2A. This report provides a comprehensive audit of the data landscape for the Los Angeles County Metropolitan Transportation Authority (Metro) and the associated economic indicators in the San Gabriel Valley. The period of interest, centered on the March 2016 opening, necessitates a multi-layered approach to account for the structural reconfigurations of the rail network, most notably the Regional Connector opening in June 2023, and the geographical limitations of municipal open data portals. The following analysis serves as a technical blueprint for implementing a statistical framework—specifically a Difference-in-Differences (DiD) or Synthetic Control Method—to isolate the causal impact of the extension on transit boardings and local commercial density.

## **Section 1: LA Metro Ridership Data Systems and Accessibility**

### **1a) Analysis of the Streets For All Ridership Dashboard**

The third-party platform ridership.streetsforall.org was developed as a direct response to the technical deficiencies of the official Metro ridership portal.1 As of August 22, 2025, the dashboard is fully operational and serves as a high-fidelity mirror for line-level ridership trends.1 The platform is designed to facilitate the visualization, filtering, and aggregation of monthly data, which is otherwise difficult to compare using native agency tools.2

The data procurement process on this site involves a "Download" function that exports custom selections as a Comma Separated Values (CSV) file.2 Unlike the official dashboard, which often returns static table views, Streets For All provides a processed dataset that accounts for "shakeups"—the semiannual service changes occurring in June and December.2 During these months, the platform utilizes a proration algorithm to normalize monthly averages based on the number of days before and after the service adjustment.2

The exported CSV files from this source include the following field schema:

| Column Name | Data Type | Functional Description |
| :---- | :---- | :---- |
| Year | Integer | The calendar year of the observation. |
| Month | String | The month of the observation (e.g., "January"). |
| Line Name | String | The official designation of the rail or bus line. |
| Day Group | String | Categorization of data into Weekday, Saturday, or Sunday. |
| Avg. Daily Boardings | Float | Calculated average boardings for the specified day group. |
| Line Category | String | Mode designation (e.g., "Train" or "Bus"). |

The date range available on the portal extends from 2009 to early 2025, covering the entire pre- and post-intervention window for the March 2016 Foothill Extension.2 However, it is a critical limitation to note that this dataset is primarily line-level.2 While the organization has utilized stop-level data for specific bus delay analyses, the public-facing CSV export for rail is aggregated at the line level, meaning it provides total boardings for the "Gold Line" (or "A Line") rather than for individual stations like Arcadia or Azusa.2

### **1b) Technical Audit of the OPA Metro Ridership Dashboard**

The official agency dashboard, located at opa.metro.net/MetroRidership, is an aging infrastructure built on a.NET/ASPX framework.2 This dashboard returns average daily ridership figures based on Automated Passenger Counter (APC) sensors located on trains and buses.2 The interface provides granularity for monthly timeframes, segmented by three distinct day groups: Weekday, Saturday, and Sunday.2

As of recent technical evaluations, this site is considered highly suboptimal for automated data ingestion. The platform does not offer a bulk "Download" button for the entire longitudinal history; instead, it requires users to generate individual requests per line and per time range, making comparative analysis impossible without manual scraping or cell-by-cell copying into local documents.2 The dashboard is frequently described as antiquated, and there is no documented API for direct data calls.3

The granularity available through the OPA portal is:

* Mode Level (System-wide, Rail, Bus).  
* Line Level (Individual rail lines and bus routes).  
* Day Type (Weekday, Saturday, Sunday).

Data is not natively downloadable in a structured CSV format through this interface for station-level boardings.2 Furthermore, the site has been reported as inaccessible or unstable in several research instances, indicating that it should not be the primary source for a mission-critical data pipeline.5

### **1c) Identification of Station-Level Ridership Sources**

Station-level ridership data—the most granular metric required for localized economic impact studies—is not currently published through a live, downloadable portal by LA Metro.2 However, high-quality proxies and specific academic/community datasets exist:

1. **Reddit Source (misken67):** The most reliable public source for station-level rail data in the LA region is the user misken67, who facilitates the distribution of ridership figures obtained through formal Public Records Act (PRA) requests.6 These datasets provide average weekday boardings for every station in the system, often comparing fiscal years (July 1 to June 30\) or providing "pre-pandemic" vs. "post-pandemic" benchmarks.6 These datasets are typically shared via Google Sheets links or directly in community discussions on the r/LAMetro subreddit.6  
2. **National Transit Database (NTD):** The Federal Transit Administration (FTA) maintains the NTD, which includes data for urban full reporters like LA Metro.8 While the standard monthly module (MRR) provides agency and mode-level data, it does not typically publish station-level CSVs to the general public.8 Researchers must often use the "Monthly Module Raw Data Release" found at https://www.transit.dot.gov/ntd/data-product/monthly-module-raw-data-release to find line-level totals, which can then be used to validate the station-level totals found in community reports.  
3. **Metro GIS and Developer Portal:** The site developer.metro.net/gis-data/ primarily hosts geospatial files (Shapefiles, GeoJSON) for station locations and track alignments but does not contain dynamic ridership boarding CSVs.3 The GitHub organization for the agency (LACMTA) confirms that while they possess the data internally, the public-facing "Ridership Stats Dashboard" is in "dire need of improvements" and currently lacks a direct download API for raw station data.3

### **1d) Confirmation of Line-Level Monthly Data Availability**

In the event that station-level data for specific months in the 2016–2023 period cannot be verified through community sources, it is confirmed that line-level monthly data is fully available through the National Transit Database (NTD).8

**Procurement Method for Line-Level Data:**

* **Exact URL:** https://analysis.dds.dot.ca.gov/ntd\_monthly\_ridership/.8  
* **Process:** Access the "Monthly Ridership Trends" report. Filter for "Los Angeles County Metropolitan Transportation Authority" as the Reporter.8  
* **Granularity:** Monthly "Unlinked Passenger Trips" (UPT) by mode (Light Rail).8  
* **Application:** This data is suitable for a system-wide analysis or for comparing the "Gold Line" as a whole against other control lines (e.g., the Blue or Green lines) during the 2016 treatment period.

## **Section 2: Gold Line / A Line Historical and Structural Evolution**

### **2a) Gold Line Foothill Extension Phase 2A Details**

The Foothill Extension Phase 2A officially commenced passenger service on **March 5, 2016**.11 This project extended the light rail system from its previous terminus at Sierra Madre Villa in Pasadena into the "Foothill Cities" of the San Gabriel Valley.11 The extension added 11.5 miles of double track and six new stations to the line.11

The stations added during this 2016 opening are:

1. **Arcadia** (City of Arcadia).12  
2. **Monrovia** (City of Monrovia).12  
3. **Duarte/City of Hope** (City of Duarte).12  
4. **Irwindale** (City of Irwindale).12  
5. **Azusa Downtown** (City of Azusa).12  
6. **APU/Citrus College** (City of Azusa; terminus for Phase 2A).11

### **2b) Regional Connector Impact and Data Continuity Challenges**

The opening of the Regional Connector on **June 16, 2023**, represents a fundamental rupture in the continuity of LA Metro rail data.11 This project eliminated the need for transfers at 7th Street/Metro Center and Union Station by creating three new underground stations in Downtown Los Angeles (Little Tokyo/Arts District, Historic Broadway, and Grand Avenue Arts/Bunker Hill).12

**Structural Reorganization:**

* **The Gold Line (L Line) Retirement:** The Gold Line, which previously operated as a U-shaped line from East LA through Union Station to Azusa, was discontinued as a distinct entity.11  
* **A Line Consolidation:** The northern segment of the former Gold Line (Azusa to Union Station) was merged with the former Blue Line (Long Beach to 7th St/Metro Center).11 This consolidated route is now known exclusively as the **A Line**, running from Long Beach to Azusa (and as of September 19, 2025, to Pomona).12  
* **E Line Consolidation:** The eastern segment of the former Gold Line (East LA to Union Station) was merged with the former Expo Line (Santa Monica to 7th St/Metro Center) to form the new **E Line**.12

**Implications for Longitudinal Analysis:** For a project assessing the 2016 extension's impact, the "Gold Line" (or "L Line" after 2020\) serves as the treatment group until June 2023\.16 Post-June 2023, the researcher must pivot to the **A Line** data to track the same physical stations (Arcadia to Azusa).16 This transition introduces a significant exogenous shock to the data: ridership on the northern portion of the A Line reportedly increased by 11.5% year-over-year following the connector's opening, partly due to the elimination of the Union Station transfer for riders heading to Downtown LA or Long Beach.19 Failure to account for the Regional Connector would likely lead to an overestimation of the 2016 extension's long-term "organic" growth by confounding it with the 2023 network effect.

### **2c) Comprehensive List of Current Metro Rail Lines for Treatment/Control Grouping**

To define accurate control groups for a statistical project, the following table lists the current Metro Rail lines, their former designations, and their historical context:

| Current Letter | Former Name | Primary Color | Opening Date | Historical Notes |
| :---- | :---- | :---- | :---- | :---- |
| **A Line** | Blue Line | Blue | 1990 | Added Foothill Extension (2016) and Regional Connector (2023).12 |
| **B Line** | Red Line | Red | 1993 | Heavy rail; North Hollywood to Union Station.12 |
| **C Line** | Green Line | Green | 1995 | Norwalk to Redondo Beach; reconfigured for LAX (2024/2025).12 |
| **D Line** | Purple Line | Purple | 1993 | Redesignated from Red Line in 2006; currently under extension to Westwood.12 |
| **E Line** | Expo Line | Aqua | 2012 | Extended to Santa Monica (2016); merged with Eastside Gold Line (2023).12 |
| **K Line** | Crenshaw/LAX | Pink | 2022 | First segments opened 2022; extended to Aviation/Century in 2024\.12 |

## **Section 3: Economic Activity and Business Data**

### **3a) LA City "Listing of Active Businesses" Data**

The City of Los Angeles provides a robust dataset for economic analysis through its Open Data portal. This dataset is maintained by the Office of Finance and contains records for all businesses registered to operate within the city.21

* **Exact CSV Download URL:** https://data.lacity.org/api/views/6rrh-rzua/rows.csv?accessType=DOWNLOAD.23  
* **Metadata Profile:**  
  * **Row Count:** Approximately 625,000 active businesses (as of February 2026 update).25  
  * **Update Interval:** Monthly.21  
* **Column Schema:**  
  * LOCATION ACCOUNT \#: Unique identifier for the business location.25  
  * BUSINESS NAME: Legal name of the business.25  
  * DBA NAME: Doing Business As name.25  
  * STREET ADDRESS, CITY, ZIP CODE: Physical location details.25  
  * LOCATION DESCRIPTION: Abbreviated address description.25  
  * MAILING ADDRESS, MAILING CITY, MAILING ZIP CODE: Correspondence address.26  
  * NAICS: Industry classification code.21  
  * PRIMARY NAICS DESCRIPTION: Industry category description.27  
  * COUNCIL DISTRICT: City of LA political boundary.25  
  * LOCATION: Latitude and longitude coordinates (Yes, included).21  
  * LOCATION START DATE: The date the business was registered or began operations (Yes, included).21

### **3b) Critical Geographical Limitation: The "SGV Gap"**

A primary obstacle for the "LA Metro Ridership Impact Analysis" is the spatial mismatch between the LA City business data and the Foothill Extension stations. The data from data.lacity.org covers **ONLY the City of Los Angeles**.21 The five cities served by the 2016 extension—Arcadia, Monrovia, Duarte, Irwindale, and Azusa—are autonomous incorporated cities in the San Gabriel Valley and are **not** part of the City of Los Angeles.29

**County-Level Data Search:** Research into the Los Angeles County open data portal (data.lacounty.gov) reveals that there is **no unified business license dataset** that covers all incorporated cities in the county.28 The County’s "TTC Business License" dataset specifically covers:

1. Unincorporated areas of the County.  
2. The contract cities of Malibu, Santa Clarita, and Westlake Village.28

Businesses in the Foothill cities (Arcadia, Azusa, etc.) are required to pay an annual business license tax to their respective municipal governments, but these cities do not currently contribute their data to a centralized, machine-readable open data portal like Socrata.32 For example, the City of Azusa requires all businesses to obtain a license prior to conducting business, but the data is managed internally by the Economic and Community Development department.34 The City of Monrovia provides a "Business License Application" but does not offer a public API or CSV of active licenses.35

### **3c) Verified Scope Adjustment for Economic Analysis**

Based on the lack of a usable, bulk-downloadable business license dataset for the San Gabriel Valley station areas, it is confirmed that a business proximity analysis based on "active licenses" or "business start dates" is **currently impossible** using only open public data.30

**Recommendation:** The researcher should remove "Business Proximity Analysis" from the project scope or pivot to a different proxy for economic activity. An alternative viable metric is the **US Census American Community Survey (ACS) 5-year estimates**, which provide "Commute Mode Share" and "Median Household Income" at the Census Block Group level for every city in the San Gabriel Valley. This data can be retrieved using the tidycensus library (R) or census (Python) to evaluate changes in transit dependency around the new stations between the 2011–2015 (pre) and 2017–2021 (post) periods.9

## **Section 4: Metro Station Locations and GIS Data**

### **4a) GIS Data Inventory from Developer Portal**

Geospatial data for Metro stations is primarily hosted through the agency's GIS portals and mirrored in community GitHub repositories. The official developer portal (developer.metro.net/gis-data/) provides the following resources:

* **Station Location Files:** Available in **GeoJSON**, **Shapefile**, and **KML** formats.37  
* **Exact Download URL (Community-Verified):** https://github.com/datadesk/lametro-maps/blob/master/blue-line-stations.geojson (This repository is a standard source used by regional analysts to map station points).38  
* **Included Fields:**  
  * station: The name of the station (e.g., "Azusa Downtown").  
  * line: The rail line(s) serving the station.  
  * lat: Latitude coordinate.  
  * lon: Longitude coordinate.  
  * geometry: Point geometry for mapping.37

### **4b) Manual GIS Alternative**

For a project focused primarily on statistical modeling rather than complex cartography, a manually-created CSV of the six Foothill stations and their coordinates is often more efficient than processing large GeoJSON files.

| Station Name | City | Latitude | Longitude |
| :---- | :---- | :---- | :---- |
| Arcadia | Arcadia | 34.1417 | \-118.0287 |
| Monrovia | Monrovia | 34.1356 | \-118.0019 |
| Duarte/City of Hope | Duarte | 34.1311 | \-117.9712 |
| Irwindale | Irwindale | 34.1283 | \-117.9344 |
| Azusa Downtown | Azusa | 34.1360 | \-117.9068 |
| APU/Citrus College | Azusa | 34.1363 | \-117.8920 |

*Note: Coordinates in the table above are UNVERIFIED and should be manually confirmed via Google Maps or the official Metro GTFS feed prior to coding.*

## **Section 5: Data Availability Summary and Recommendations**

### **5a) Data Source Summary Table**

| Data Source | Available? | Format | Granularity | Date Range | Exact URL / Source |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **Line Ridership** | YES | CSV | Monthly | 2009–2025 | ridership.streetsforall.org 1 |
| **Station Ridership** | PARTIAL | Google Sheet | Annual | 2016–2025 | reddit.com/u/misken67 6 |
| **NTD Ridership** | YES | Excel/CSV | Monthly | 2018–2024 | transit.dot.gov/ntd 8 |
| **LA City Business** | YES | CSV | Monthly | 1997–2026 | data.lacity.org/api/views/6rrh-rzua 23 |
| **SGV Business Data** | **NO** | N/A | N/A | N/A | **UNAVAILABLE** in open portal 30 |
| **Station GIS** | YES | GeoJSON | Point | Current | github.com/datadesk/lametro-maps 38 |

### **5b) Comprehensive Recommendations for Analysis Design**

**1\. Data Selection Strategy:**

* **Utilize the National Transit Database (NTD) for line-level controls.** The NTD provides the most historically consistent monthly ridership figures.8 Use the "Light Rail" mode total as a proxy for system-wide trends to control for macro-economic factors (e.g., gas prices, employment rates).  
* **Utilize misken67 datasets for the treatment group.** To isolate the effect of the 2016 extension, the researcher must use the station-level boardings for the six Foothill stations.6 Using line-level data for the A Line would be inaccurate, as the A Line now includes the high-ridership Long Beach segment, which would drown out the Foothill signal.6

**2\. Scope Adjustments:**

* **Drop Business Analysis:** Because the SGV cities do not provide open business license data, the "economic activity" part of the query cannot be satisfied with "verified facts" and "exact URLs".30  
* **Pivotal Alternative (Census Data):** Instead of business licenses, use the US Census Bureau’s "OnTheMap" (LEHD) tool or ACS Block Group data.9 LEHD data provides "Job Density" by industry near specific coordinates, which is a superior proxy for economic impact than raw business licenses and covers the entire San Gabriel Valley.

**3\. Simplest Viable Analysis Design:**

The optimal statistical project design is a **Difference-in-Differences (DiD)** model.

* **Treatment Group:** The six Foothill Extension stations (Arcadia, Monrovia, Duarte, Irwindale, Azusa Downtown, APU/Citrus College).11  
* **Control Group:** A set of comparable light rail stations that did not undergo extension in 2016 (e.g., Gold Line stations in Pasadena like Allen or Del Mar, or the Green Line).12  
* **Treatment Date:** March 5, 2016\.11  
* **Shock to Control for:** The Regional Connector opening (June 16, 2023), which fundamentally changed the A Line's appeal to long-distance commuters.15

### **5c) WHAT TO DO NEXT**

1. **Ingest Monthly NTD Data**: Download the "Monthly Module Raw Data Release" from the FTA to establish the pre-2016 and post-2016 baseline for the Light Rail mode in Los Angeles.  
2. **Scrape misken67 Reddit Reports**: Collect the station-level ridership tables for the "Gold Line North" segment (Sierra Madre Villa to APU/Citrus College) to identify the specific performance of the Phase 2A stations.  
3. **Procure Census LEHD Data**: Access onthemap.ces.census.gov and draw 0.5-mile buffers around the six Foothill station coordinates to export annual "Work Area Profile" reports, which will provide the necessary economic density data.  
4. **Implement Data Bridge for June 2023**: In the statistical code, create a transformation logic that maps pre-2023 "Gold Line" station IDs to post-2023 "A Line" station IDs to ensure longitudinal consistency across the Regional Connector opening.  
5. **Verify GIS Coordinates**: Manually confirm the station coordinates against the latest Metro GTFS feed to ensure that spatial proximity calculations (for Census or Job data) are accurate to the platform level.

#### **Works cited**

1. Streets for All Data/Dev Blog, accessed March 24, 2026, [https://data.streetsforall.org/](https://data.streetsforall.org/)  
2. It's hard to use LA Metro's ridership dashboard. We built a new one. \- Streets for All Data/Dev Blog, accessed March 24, 2026, [https://data.streetsforall.org/blog/ridership\_dashboard/](https://data.streetsforall.org/blog/ridership_dashboard/)  
3. LACMTA/open-data: Location of any flat data sets utilized ... \- GitHub, accessed March 24, 2026, [https://github.com/LACMTA/open-data](https://github.com/LACMTA/open-data)  
4. LA Metro's 2024 Ridership Soars to More Than 311 Million Marking Significant Growth, accessed March 24, 2026, [http://www.metro.net/about/la-metros-2024-ridership-soars-to-more-than-311-million-marking-significant-growth/](http://www.metro.net/about/la-metros-2024-ridership-soars-to-more-than-311-million-marking-significant-growth/)  
5. accessed December 31, 1969, [https://opa.metro.net/MetroRidership/](https://opa.metro.net/MetroRidership/)  
6. LA Metro 2025 Ridership by Station : r/LAMetro \- Reddit, accessed March 24, 2026, [https://www.reddit.com/r/LAMetro/comments/1nkkxnx/la\_metro\_2025\_ridership\_by\_station/](https://www.reddit.com/r/LAMetro/comments/1nkkxnx/la_metro_2025_ridership_by_station/)  
7. Metro ridership pre/post covid comparison : r/LAMetro \- Reddit, accessed March 24, 2026, [https://www.reddit.com/r/LAMetro/comments/155fj77/metro\_ridership\_prepost\_covid\_comparison/](https://www.reddit.com/r/LAMetro/comments/155fj77/metro_ridership_prepost_covid_comparison/)  
8. Los Angeles County Metropolitan Transportation Authority — NTD Monthly Ridership by RTPA \- Cal-ITP Data Analyses Portfolio, accessed March 24, 2026, [https://analysis.dds.dot.ca.gov/ntd\_monthly\_ridership/rtpa\_los-angeles-county-metropolitan-transportation-authority/00\_\_monthly\_ridership\_report\_\_rtpa\_los-angeles-county-metropolitan-transportation-authority.html](https://analysis.dds.dot.ca.gov/ntd_monthly_ridership/rtpa_los-angeles-county-metropolitan-transportation-authority/00__monthly_ridership_report__rtpa_los-angeles-county-metropolitan-transportation-authority.html)  
9. Transportation Data and Related Resources, accessed March 24, 2026, [https://metroprimaryresources.info/data/](https://metroprimaryresources.info/data/)  
10. lacmta \- Metro · GitHub, accessed March 24, 2026, [https://github.com/LACMTA](https://github.com/LACMTA)  
11. Foothill Extension \- Wikipedia, accessed March 24, 2026, [https://en.wikipedia.org/wiki/Foothill\_Extension](https://en.wikipedia.org/wiki/Foothill_Extension)  
12. List of Los Angeles Metro Rail stations \- Wikipedia, accessed March 24, 2026, [https://en.wikipedia.org/wiki/List\_of\_Los\_Angeles\_Metro\_Rail\_stations](https://en.wikipedia.org/wiki/List_of_Los_Angeles_Metro_Rail_stations)  
13. Timeline of Los Angeles Metro : r/LAMetro \- Reddit, accessed March 24, 2026, [https://www.reddit.com/r/LAMetro/comments/1lem58p/timeline\_of\_los\_angeles\_metro/](https://www.reddit.com/r/LAMetro/comments/1lem58p/timeline_of_los_angeles_metro/)  
14. Metro Gold Line Foothill Extension Phase 2A \- Kiewit Corporation, accessed March 24, 2026, [https://www.kiewit.com/projects/metro-gold-line-foothill-extension-phase-2a/](https://www.kiewit.com/projects/metro-gold-line-foothill-extension-phase-2a/)  
15. Metro Ridership Holds Strong Amid Regional Challenges, Driven by Rail Growth, Weekend Travel, Improved Safety, accessed March 24, 2026, [https://www.metro.net/about/metro-ridership-holds-strong-amid-regional-challenges-driven-by-rail-growth-weekend-travel-improved-safety/](https://www.metro.net/about/metro-ridership-holds-strong-amid-regional-challenges-driven-by-rail-growth-weekend-travel-improved-safety/)  
16. Metro Facts at a Glance \- Los Angeles, accessed March 24, 2026, [https://www.metro.net/about/facts-glance/](https://www.metro.net/about/facts-glance/)  
17. The Longest Light Rail Line On Earth, L.A. Metro's A Line, Is Opening 4 New Stations This Week \- Secret Los Angeles, accessed March 24, 2026, [https://secretlosangeles.com/los-angeles-foothill-a-line-extension-opening/](https://secretlosangeles.com/los-angeles-foothill-a-line-extension-opening/)  
18. LA Metro Officials Report Ridership Holding Strong \- Metro Magazine, accessed March 24, 2026, [https://www.metro-magazine.com/news/la-metro-officials-report-ridership-holding-strong](https://www.metro-magazine.com/news/la-metro-officials-report-ridership-holding-strong)  
19. Per Metro: A Line ridership is up 11.5% Year-Over-Year, with significant increases in DTLA and the northern portion of line : r/LAMetro \- Reddit, accessed March 24, 2026, [https://www.reddit.com/r/LAMetro/comments/1rjhz04/per\_metro\_a\_line\_ridership\_is\_up\_115\_yearoveryear/](https://www.reddit.com/r/LAMetro/comments/1rjhz04/per_metro_a_line_ridership_is_up_115_yearoveryear/)  
20. Los Angeles Metro Rail \- Wikipedia, accessed March 24, 2026, [https://en.wikipedia.org/wiki/Los\_Angeles\_Metro\_Rail](https://en.wikipedia.org/wiki/Los_Angeles_Metro_Rail)  
21. Open Data Portal Published Information \- Office of Finance \- City of Los Angeles, accessed March 24, 2026, [https://finance.lacity.gov/open-data-portal-published-information](https://finance.lacity.gov/open-data-portal-published-information)  
22. Listing of Active Businesses \- Dataset \- Catalog \- Data.gov, accessed March 24, 2026, [https://catalog.data.gov/dataset/listing-of-active-businesses](https://catalog.data.gov/dataset/listing-of-active-businesses)  
23. Downloads \- Los Angeles Open Data, accessed March 24, 2026, [https://data.lacity.org/api/views/4qmh-sz39/rows.csv?accessType=DOWNLOAD](https://data.lacity.org/api/views/4qmh-sz39/rows.csv?accessType=DOWNLOAD)  
24. Current (CSV) \- US City Open Data Census, accessed March 24, 2026, [http://us-city.census.okfn.org/api/entries.cascade.csv](http://us-city.census.okfn.org/api/entries.cascade.csv)  
25. Listing of Active Businesses | Los Angeles \- Open Data Portal, accessed March 24, 2026, [https://data.lacity.org/Administration-Finance/Listing-of-Active-Businesses/6rrh-rzua](https://data.lacity.org/Administration-Finance/Listing-of-Active-Businesses/6rrh-rzua)  
26. Listing of All Businesses | Los Angeles \- Open Data Portal, accessed March 24, 2026, [https://data.lacity.org/Administration-Finance/Listing-of-All-Businesses/r4uk-afju](https://data.lacity.org/Administration-Finance/Listing-of-All-Businesses/r4uk-afju)  
27. BSD Order | Los Angeles \- Open Data Portal, accessed March 24, 2026, [https://data.lacity.org/A-Prosperous-City/BSD-Order/5ey4-7ygp](https://data.lacity.org/A-Prosperous-City/BSD-Order/5ey4-7ygp)  
28. TTC Business License Web Portal | County of Los Angeles Open Data, accessed March 24, 2026, [https://data.lacounty.gov/pages/c9396b9baeeb46d5a65731e9cb757168](https://data.lacounty.gov/pages/c9396b9baeeb46d5a65731e9cb757168)  
29. About | San Gabriel Valley Council of Governments, accessed March 24, 2026, [https://www.sgvcog.org/about](https://www.sgvcog.org/about)  
30. TTC Business License \- Overview \- ArcGIS Online, accessed March 24, 2026, [https://lacounty.maps.arcgis.com/home/item.html?id=8256f46ea75d49a1ba7cae2c807dce1c](https://lacounty.maps.arcgis.com/home/item.html?id=8256f46ea75d49a1ba7cae2c807dce1c)  
31. Business License Commission \- LA County, accessed March 24, 2026, [https://blc.lacounty.gov/](https://blc.lacounty.gov/)  
32. Business Licenses | San Gabriel, CA \- Official Website, accessed March 24, 2026, [https://www.sangabrielcity.com/172/Business-Licenses](https://www.sangabrielcity.com/172/Business-Licenses)  
33. Business License Services \- Arcadia, CA, accessed March 24, 2026, [https://www.arcadiaca.gov/government/development\_services/business\_license/index.php](https://www.arcadiaca.gov/government/development_services/business_license/index.php)  
34. Business Licensing | Azusa, CA \- Official Website, accessed March 24, 2026, [https://www.azusaca.gov/247/Business-Licensing](https://www.azusaca.gov/247/Business-Licensing)  
35. Business License | City of Monrovia, accessed March 24, 2026, [https://www.monroviaca.gov/doing-business-here/business-licensing](https://www.monroviaca.gov/doing-business-here/business-licensing)  
36. accessed December 31, 1969, [https://developer.metro.net/gis-data/](https://developer.metro.net/gis-data/)  
37. GeoJSON \- Metro Stations Regional \- Dataset \- Catalog, accessed March 24, 2026, [https://catalog.data.gov/dataset/metro-stations-regional/resource/91596ab0-bb7b-4cb7-8045-884c1ae801ea](https://catalog.data.gov/dataset/metro-stations-regional/resource/91596ab0-bb7b-4cb7-8045-884c1ae801ea)  
38. datadesk/lametro-maps: Geospatial data from L.A. Metro's public transportation system \- GitHub, accessed March 24, 2026, [https://github.com/datadesk/lametro-maps](https://github.com/datadesk/lametro-maps)  
39. A Peek into Metro Rail Ridership Details Station-by-Station \- Streetsblog Los Angeles, accessed March 24, 2026, [https://la.streetsblog.org/2024/08/14/a-peek-into-metro-rail-ridership-details-station-by-station](https://la.streetsblog.org/2024/08/14/a-peek-into-metro-rail-ridership-details-station-by-station)