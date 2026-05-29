"""Generate data catalog PDF for Japan Real Estate Explorer."""
from fpdf import FPDF
from pathlib import Path

OUTPUT = Path(__file__).resolve().parent.parent / "docs" / "data_catalog.pdf"
OUTPUT.parent.mkdir(exist_ok=True)

BLUE   = (59, 130, 246)
DARK   = (15, 23, 42)
GRAY   = (100, 116, 139)
LIGHT  = (241, 245, 249)
WHITE  = (255, 255, 255)
GREEN  = (16, 185, 129)
ORANGE = (245, 158, 11)
RED    = (239, 68, 68)
INDIGO = (79, 70, 229)
TEAL   = (16, 185, 129)
AMBER  = (245, 158, 11)


class Catalog(FPDF):
    def header(self):
        self.set_fill_color(*DARK)
        self.rect(0, 0, 210, 14, "F")
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*BLUE)
        self.set_y(4)
        self.cell(0, 6, "JAPAN REAL ESTATE EXPLORER  |  DATA CATALOG", align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "", 7)
        self.set_text_color(*GRAY)
        self.cell(0, 6, f"Page {self.page_no()}", align="C")

    def cover(self):
        self.add_page()
        self.set_fill_color(*DARK)
        self.rect(0, 0, 210, 297, "F")
        self.set_y(70)
        self.set_font("Helvetica", "B", 28)
        self.set_text_color(*WHITE)
        self.cell(0, 14, "JAPAN REAL ESTATE", align="C", new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 14, "EXPLORER", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(6)
        self.set_font("Helvetica", "", 13)
        self.set_text_color(*BLUE)
        self.cell(0, 8, "Complete Data Catalog & API Reference", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(10)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*GRAY)
        self.cell(0, 6, "All data sources, fields, coverage, and availability", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(30)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*GRAY)
        for line in [
            "MLIT Real Estate Information Library API",
            "e-Stat Government Statistics API",
            "Additional Data Sources & Roadmap",
        ]:
            self.cell(0, 7, line, align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_y(260)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 6, "Generated: May 2026", align="C")

    def section_header(self, title, subtitle="", color=None):
        if color is None:
            color = BLUE
        self.ln(4)
        self.set_fill_color(*color)
        self.rect(10, self.get_y(), 190, 10, "F")
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*WHITE)
        self.set_x(14)
        self.cell(0, 10, title)
        self.ln(10)
        if subtitle:
            self.set_font("Helvetica", "I", 7.5)
            self.set_text_color(*GRAY)
            self.set_x(10)
            self.multi_cell(190, 4.5, subtitle)
        self.ln(2)

    def subsection(self, title):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*DARK)
        self.set_fill_color(*LIGHT)
        self.set_x(10)
        self.cell(190, 7, f"  {title}", fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def field_table(self, fields):
        self.set_font("Helvetica", "B", 7.5)
        self.set_fill_color(*DARK)
        self.set_text_color(*WHITE)
        self.set_x(10)
        self.cell(42, 6, "Field", fill=True, border=0)
        self.cell(22, 6, "Type", fill=True, border=0)
        self.cell(22, 6, "Coverage", fill=True, border=0)
        self.cell(104, 6, "Description", fill=True, border=0)
        self.ln(6)
        for i, (name, ftype, cov, desc) in enumerate(fields):
            fill = i % 2 == 0
            self.set_fill_color(248, 250, 252) if fill else self.set_fill_color(*WHITE)
            self.set_text_color(*DARK)
            self.set_font("Helvetica", "B", 7)
            self.set_x(10)
            self.cell(42, 5.5, name, fill=fill, border=0)
            self.set_font("Helvetica", "", 7)
            self.set_text_color(*GRAY)
            self.cell(22, 5.5, ftype, fill=fill, border=0)
            if "100%" in cov:
                self.set_text_color(*GREEN)
            elif "0%" in cov:
                self.set_text_color(*RED)
            else:
                self.set_text_color(*ORANGE)
            self.set_font("Helvetica", "B", 7)
            self.cell(22, 5.5, cov, fill=fill, border=0)
            self.set_font("Helvetica", "", 7)
            self.set_text_color(*DARK)
            self.cell(104, 5.5, desc, fill=fill, border=0)
            self.ln(5.5)
        self.ln(3)

    def info_box(self, lines):
        self.set_x(10)
        for line in lines:
            self.set_font("Helvetica", "", 8)
            self.set_text_color(*DARK)
            self.set_x(10)
            self.multi_cell(190, 5.5, line)
        self.ln(2)

    def endpoint_block(self, code, name, period, fields, note):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*DARK)
        self.set_fill_color(*LIGHT)
        self.set_x(10)
        self.cell(190, 7, f"  {code} - {name}  |  Period: {period}", fill=True, new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "I", 7.5)
        self.set_text_color(*GRAY)
        self.set_x(14)
        self.multi_cell(186, 5, note)
        self.set_font("Helvetica", "", 7.5)
        self.set_text_color(*DARK)
        for f in fields:
            self.set_x(18)
            self.cell(4, 4.5, "-")
            self.cell(0, 4.5, f, new_x="LMARGIN", new_y="NEXT")
        self.ln(3)


pdf = Catalog()
pdf.set_auto_page_break(auto=True, margin=15)

pdf.cover()

# TOC
pdf.add_page()
pdf.section_header("TABLE OF CONTENTS")
toc = [
    ("1.", "MLIT XIT001 - Transaction Prices", "ACTIVE"),
    ("2.", "MLIT Other Endpoints - Available, Not Yet Fetched", "Available with current key"),
    ("3.", "e-Stat - Government Statistics", "Key obtained, not yet fetched"),
    ("4.", "Static / Hardcoded Data (Remaining)", "Still in code"),
    ("5.", "Additional Sources - Roadmap", "Not yet integrated"),
]
for num, title, status in toc:
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*DARK)
    pdf.set_x(14)
    pdf.cell(10, 7, num)
    pdf.cell(140, 7, title)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 7, status, new_x="LMARGIN", new_y="NEXT")


# SECTION 1 - MLIT XIT001
pdf.add_page()
pdf.section_header(
    "1. MLIT XIT001 - Real Estate Transaction Prices",
    "API Key: MLIT_API_KEY  |  Status: ACTIVE  |  Endpoint: reinfolib.mlit.go.jp/ex-api/external/XIT001",
)
pdf.info_box([
    "Source: Ministry of Land, Infrastructure, Transport and Tourism",
    "Coverage: All 47 prefectures, any municipality. Data from 2005 Q3 to present (~2 quarter lag).",
    "Auth: Header 'Ocp-Apim-Subscription-Key'. Params: year, quarter, area (pref code), language=en.",
    "Note: One call per prefecture x quarter. Recommended rate: 0.4s between calls.",
])

pdf.subsection("1a. ward_transactions.parquet - Tokyo 23 Wards  (245,139 rows, 2020-2025)")
pdf.field_table([
    ("ward",             "string", "100%",  "Ward name in English (Chiyoda, Minato, etc.)"),
    ("ward_ja",          "string", "100%",  "Ward name in Japanese kanji"),
    ("property_type",    "string", "100%",  "Used Apartment / Used House / Used Commercial / Land Only"),
    ("purpose",          "string", "55.9%", "Declared use: House, Office, Shop, Other"),
    ("region",           "string", "23.6%", "Sub-zone within ward from MLIT record"),
    ("tx_year",          "int",    "100%",  "Transaction year (2020-2025)"),
    ("tx_quarter",       "int",    "100%",  "Transaction quarter (1-4)"),
    ("tx_period",        "string", "100%",  "Combined period label e.g. '2023-Q2'"),
    ("area_m2",          "float",  "100%",  "Property floor area in square meters"),
    ("layout",           "string", "100%",  "Apartment layout: 1K, 1LDK, 2LDK, etc. '-' for land/commercial"),
    ("year_built",       "int",    "90.6%", "Year the building was constructed"),
    ("building_age",     "int",    "90.6%", "Age of building at time of transaction (years)"),
    ("nearest_station",  "string", "0%",    "Nearest station - NOT provided by MLIT XIT001"),
    ("station_minutes",  "int",    "0%",    "Walk time to station - NOT provided by MLIT XIT001"),
    ("trade_price_jpy",  "int",    "100%",  "Total transaction price in Japanese Yen"),
    ("price_per_m2_jpy", "int",    "100%",  "Price per square meter in Japanese Yen"),
    ("lat",              "float",  "100%",  "Ward centroid latitude"),
    ("lon",              "float",  "100%",  "Ward centroid longitude"),
    ("district",         "string", "100%",  "MLIT DistrictName - sub-ward neighborhood (e.g. Roppongi)"),
    ("district_code",    "string", "100%",  "JIS district code (9 digits)"),
    ("structure",        "string", "0%",    "Building structure: RC, SRC, Steel, Wood - NOT returned for Tokyo"),
    ("direction",        "string", "28.9%", "Facade orientation: South, Southwest, East, etc."),
    ("renovation",       "string", "31.3%", "Renovation status: Done / Not Done"),
    ("city_planning",    "string", "96.2%", "City planning zone: Residential / Commercial / Industrial"),
    ("coverage_ratio",   "float",  "64.8%", "Maximum building footprint as % of lot area"),
    ("floor_area_ratio", "float",  "64.8%", "Maximum total floor area as % of lot area (FAR)"),
    ("frontage_m",       "float",  "21.6%", "Street frontage of the lot in meters"),
    ("breadth_m",        "float",  "28.6%", "Depth of the lot in meters"),
])

pdf.subsection("1b. prefecture_aggregates.parquet - 47 Prefectures  (94 rows, 2024-2025)")
pdf.field_table([
    ("prefecture_code", "string", "100%", "2-digit prefecture code (01=Hokkaido ... 47=Okinawa)"),
    ("tx_year",         "int",    "100%", "Transaction year (2024 or 2025)"),
    ("median_ppm2",     "float",  "100%", "Median price per m2 across all transactions in that year"),
    ("mean_ppm2",       "float",  "100%", "Mean price per m2 (skewed by luxury outliers)"),
    ("n_transactions",  "int",    "100%", "Number of transactions used to compute the aggregate"),
])

pdf.subsection("1c. prefecture_aggregates_by_type.parquet - 47 Prefectures x Property Type  (376 rows)")
pdf.field_table([
    ("prefecture_code", "string", "100%", "2-digit prefecture code"),
    ("tx_year",         "int",    "100%", "Transaction year (2024 or 2025)"),
    ("property_type",   "string", "100%", "Used Apartment / Used House / Used Commercial / Land Only"),
    ("median_ppm2",     "float",  "100%", "Median price per m2 for that type in that year"),
    ("n_transactions",  "int",    "100%", "Transaction count for that type/year/prefecture"),
])


# SECTION 2 - MLIT Other Endpoints
pdf.add_page()
pdf.section_header(
    "2. MLIT Other Endpoints - Available, Not Yet Fetched",
    "Same MLIT_API_KEY. All available today.",
    color=INDIGO,
)
pdf.endpoint_block(
    "XCT001", "Appraised Property Valuations", "Last 5 years",
    ["Appraised value (JPY)", "Property type", "Land area (m2)", "Building area (m2)",
     "Year built", "Purpose", "Location (prefecture / municipality)", "Appraisal date"],
    "Official government appraisals - more accurate than transaction prices for land valuation.",
)
pdf.endpoint_block(
    "XPT001", "Transaction Prices - Point Data", "2005 to present",
    ["Exact latitude / longitude per transaction", "Price (JPY)", "Area (m2)",
     "Property type", "Year", "Quarter"],
    "Same as XIT001 but returns exact GPS coordinates - enables heatmaps at address level.",
)
pdf.endpoint_block(
    "XPT002", "Published Land Prices - Point Data", "1995 to present",
    ["Exact latitude / longitude", "Published land price (JPY/m2)", "Year",
     "Land use category", "Building coverage ratio", "Floor area ratio"],
    "Government benchmark land prices - published annually for key reference points nationwide.",
)
pdf.endpoint_block(
    "XKT002", "Land Use Zones", "Current",
    ["Zone type (Residential / Commercial / Industrial / Agricultural)",
     "Sub-category (e.g. Category 1 Low-rise Residential)",
     "Geometry (polygon GeoJSON)", "Municipality code"],
    "Zoning map for all of Japan. Shows what can be built where - critical for development potential.",
)
pdf.endpoint_block(
    "XKT015", "Station Boarding Statistics", "Latest available",
    ["Station name", "Daily average boardings", "Railway line",
     "Municipality code", "Latitude / longitude"],
    "Real passenger volume per station - replaces the synthetic station proximity factor in the price estimator.",
)
pdf.endpoint_block(
    "XKT016/021-029", "Disaster Risk Zones", "Current",
    ["Risk type (flood / landslide / tsunami / liquefaction / embankment)",
     "Risk level (High / Medium / Low)", "Geometry (polygon GeoJSON)", "Municipality code"],
    "Key differentiator for foreign investors unaware of Japan disaster risk geography.",
)
pdf.endpoint_block(
    "XKT001", "Urban Planning Areas", "Current",
    ["Planning area name",
     "Classification (Urbanization Promotion / Urbanization Control)",
     "Geometry", "Prefecture / municipality code"],
    "Whether an area is designated for development or restricted - affects future price appreciation.",
)
pdf.endpoint_block(
    "XIT002", "Municipal Codes Reference", "Current",
    ["Municipality code (5 digits)", "Municipality name (EN/JA)",
     "Prefecture code", "Municipality type (city / town / village)"],
    "Master reference table for all Japanese municipality codes.",
)


# SECTION 3 - e-Stat
pdf.add_page()
pdf.section_header(
    "3. e-Stat - Government Statistics Portal",
    "API Key: ESTAT_API_KEY  |  Status: KEY OBTAINED, NOT YET FETCHED  |  api.e-stat.go.jp",
    color=TEAL,
)
pdf.info_box([
    "Source: Ministry of Internal Affairs and Communications",
    "Endpoint: https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData",
    "Auth: appId query parameter. Free, no rate limit specified.",
])

pdf.subsection("Population Census 2020  |  Dataset: 0004019304  |  Geography: 47 prefectures")
pdf.field_table([
    ("prefecture_code", "string", "100%", "2-digit code"),
    ("sex",             "string", "100%", "Total / Male / Female"),
    ("age_group",       "string", "100%", "5-year age groups (0-4, 5-9, ... 85+)"),
    ("population",      "int",    "100%", "Number of persons"),
    ("year",            "int",    "100%", "2020"),
])

pdf.subsection("Housing Survey 2023 - Vacant Dwellings (Akiya)  |  Dataset: 0004021648  |  47 prefectures")
pdf.field_table([
    ("prefecture_code", "string", "100%", "2-digit code"),
    ("vacancy_type",    "string", "100%", "For sale / For rent / Secondary / Other vacant / Total"),
    ("n_dwellings",     "int",    "100%", "Number of vacant dwellings"),
    ("vacancy_rate",    "float",  "100%", "Vacant dwellings as % of total dwelling stock"),
    ("year",            "int",    "100%", "2023"),
])

pdf.subsection("Housing Survey 2023 - Dwelling Size  |  Dataset: 0004021461  |  47 prefectures")
pdf.field_table([
    ("prefecture_code",  "string", "100%", "2-digit code"),
    ("tenure_type",      "string", "100%", "Owner-occupied / Rented"),
    ("avg_floor_area_m2","float",  "100%", "Average floor area per dwelling in m2"),
    ("avg_rooms",        "float",  "100%", "Average number of rooms per dwelling"),
    ("year",             "int",    "100%", "2023"),
])

pdf.subsection("Housing Survey 2023 - Tenure  |  Dataset: 0004021624  |  47 prefectures")
pdf.field_table([
    ("prefecture_code", "string", "100%", "2-digit code"),
    ("tenure_type",     "string", "100%", "Owner-occupied / Rented private / Public rental / Company housing"),
    ("n_dwellings",     "int",    "100%", "Number of dwellings by tenure type"),
    ("share_pct",       "float",  "100%", "Share of total dwelling stock (%)"),
    ("year",            "int",    "100%", "2023"),
])

pdf.subsection("Housing Survey 2023 - Elderly Households  |  Dataset: 0004025672  |  47 prefectures")
pdf.field_table([
    ("prefecture_code",  "string", "100%", "2-digit code"),
    ("household_type",   "string", "100%", "Single elderly / Couple both 65+ / With younger members"),
    ("n_households",     "int",    "100%", "Number of households"),
    ("barrier_free_pct", "float",  "100%", "Share of dwellings with barrier-free features (%)"),
    ("year",             "int",    "100%", "2023"),
])

pdf.subsection("Census 2020 - Employment by Industry  |  Dataset: 0003454502  |  47 prefectures")
pdf.field_table([
    ("prefecture_code",  "string", "100%", "2-digit code"),
    ("industry",         "string", "100%", "Industry category (17 groups): Manufacturing, Finance, IT, etc."),
    ("employed_persons", "int",    "100%", "Number of employed persons aged 15+"),
    ("year",             "int",    "100%", "2020"),
])


# SECTION 4 - Static Data Remaining
pdf.add_page()
pdf.section_header(
    "4. Static / Hardcoded Data (Remaining)",
    "Still in code. Population and akiya to be replaced by e-Stat.",
    color=AMBER,
)

pdf.subsection("prefecture_data.py - Remaining hardcoded fields")
pdf.field_table([
    ("name_en / name_ja", "string", "100%", "Prefecture name EN/JA - geographic constant, OK to keep"),
    ("capital",           "string", "100%", "Capital city name - geographic constant, OK to keep"),
    ("region",            "string", "100%", "Region grouping (Kanto, Kansai...) - OK to keep"),
    ("lat / lon",         "float",  "100%", "Centroid coordinates - geographic constant, OK to keep"),
    ("is_major_metro",    "bool",   "100%", "Major metro flag - classification constant, OK to keep"),
    ("pop_2020",          "float",  "100%", "Population - REPLACE with e-Stat Census 2020"),
    ("pop_2010",          "float",  "100%", "Population 2010 - not in e-Stat API; keep or drop"),
    ("pop_change_pct",    "float",  "100%", "Derived from pop_2010/2020 - recalculate from e-Stat"),
    ("akiya_rate_2023",   "float",  "100%", "Vacancy rate 2023 - REPLACE with e-Stat Housing Survey"),
    ("akiya_rate_2018",   "float",  "100%", "Vacancy rate 2018 - not in e-Stat API; keep or drop"),
    ("akiya_rate_2013",   "float",  "100%", "Vacancy rate 2013 - not in e-Stat API; keep or drop"),
])

pdf.subsection("ward_data.py - Remaining hardcoded fields")
pdf.field_table([
    ("ja",          "string", "100%", "Ward name in Japanese - geographic constant, OK to keep"),
    ("lat / lon",   "float",  "100%", "Ward centroid coordinates - geographic constant, OK to keep"),
    ("pop",         "int",    "100%", "Ward population in thousands - could replace with e-Stat municipal"),
    ("base_price",  "int",    "100%", "Base price/m2 estimate - SUPERSEDED by real ward_transactions.parquet"),
    ("activity",    "float",  "100%", "Transaction volume weight - SUPERSEDED by real ward_transactions.parquet"),
])
pdf.set_font("Helvetica", "I", 8)
pdf.set_text_color(*GRAY)
pdf.set_x(10)
pdf.multi_cell(190, 5,
    "Note: base_price and activity in ward_data.py are now dead code since load_data() uses the real parquet. "
    "They can be safely deleted."
)


# SECTION 5 - Roadmap
pdf.add_page()
pdf.section_header(
    "5. Additional Sources - Roadmap",
    "Not yet integrated. All free.",
    color=RED,
)
roadmap = [
    ("Bank of Japan API", "free, no key", "macroeconomics.boj.or.jp",
     "Interest rate history (policy rate, mortgage rates). Explains price cycles - rates near 0 since 1999 drove the appreciation seen in XIT001 data.",
     ["Date", "Policy rate (%)", "10-year JGB yield (%)", "Average mortgage rate (%)"]),
    ("ExchangeRate-API", "free tier", "exchangerate-api.com",
     "USD/JPY, EUR/JPY, AUD/JPY rates. Critical for foreign investor audience - all prices should optionally show USD equivalent.",
     ["Date", "USD/JPY", "EUR/JPY", "AUD/JPY", "GBP/JPY", "CNY/JPY"]),
    ("MLIT XKT015 - Station Boarding Stats", "MLIT key (have it)", "reinfolib.mlit.go.jp",
     "Real daily passenger volume per station. Replaces synthetic station_minutes factor in price estimator.",
     ["Station name", "Railway line", "Daily boardings", "Lat/lon", "Municipality code"]),
    ("MLIT Disaster Risk XKT016/021-029", "MLIT key (have it)", "reinfolib.mlit.go.jp",
     "Flood, tsunami, liquefaction, landslide risk zones as GeoJSON polygons. Strong differentiator for investors.",
     ["Risk type", "Risk level (High/Med/Low)", "Polygon geometry", "Municipality"]),
    ("OpenStreetMap Overpass API", "free, no key", "overpass-api.de",
     "Points of interest: schools, hospitals, convenience stores, parks, supermarkets by ward. Enables amenity scoring.",
     ["POI name", "Category", "Lat/lon", "Ward / district"]),
    ("National Land Numerical Information", "free, no key", "nlftp.mlit.go.jp",
     "Land use rasters, elevation models, administrative boundaries. Enables terrain and land-use overlays.",
     ["Land use category", "Elevation (m)", "Grid resolution (250m or 500m)"]),
]
for name, cost, url, desc, fields in roadmap:
    pdf.endpoint_block(name, cost, url, fields, desc)

pdf.output(str(OUTPUT))
print(f"PDF generated: {OUTPUT}")
