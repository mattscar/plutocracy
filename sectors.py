import enum

sector_dict = dict({
    'Consumer Discretionary': 0,
    'Consumer Staples': 1,
    'Energy': 2,
    'Financials': 3,
    'Health Care': 4,
    'Industrials': 5,
    'Information Technology': 6,
    'Materials': 7,
    'Real Estate': 8,
    'Telecommunication Services': 9,
    'Utilities': 10
})

with open('sp_list.txt', 'r') as infile:

    # Iterate through lines
    report_index = 0
    industry_index = 0
    sector_num = -1
    
    outfile = open('outfile.txt', 'w')
    
    lines = infile.readlines()
    for line in lines:

        # Read tokens
        name = '';
        tokens = line.split()
        for i in range(1, len(tokens)):
            if tokens[i] == 'reports':
                report_index = i
                break

        # Check if the sector has one word
        if tokens[report_index+1] in sector_dict:
            sector_num = sector_dict[tokens[report_index+1]]
            industry_index = report_index + 2

        # Check if the sector has two words
        else:
            str = tokens[report_index+1] + ' ' + tokens[report_index+2]
            if str in sector_dict:
                industry_index = report_index + 3

        # Determine the industry
        str = ''
        for i in range(industry_index, len(tokens)):
            str += tokens[i] + ' '
        str = str[:-1]
        outfile.write(str + '\n')


'''
class Industry(enum.IntEnum):
    ADVERTISING = 0
    APPAREL_RETAIL = 1
    ACCESSORIES_LUXURY = 2
    AUTO_PARTS = 3
    AUTOMOBILE = 4
    BROADCASTING = 5
    CABLE_SATELLITE = 6
    CASINOS_GAMBLING = 7
    COMPUTER_ELECTRONICS = 8
    DEPARTMENT_STORES = 9
    DISTRIBUTORS =
    GENERAL_MERCHANDISE =
    HOME_FURNISHINGS =
    HOME_IMPROVEMENT =
    HOMEBUILDING =
    HOTELS_RESORTS =
    HOUSEHOLD_APPLIANCES =
    HOUSEWARES =
    INTERNET_RETAIL =
    LEISURE =
    MOTORCYCLE =
    PUBLISHING =
    RESTAURANTS =
    SPECIALTY_STORES =
    TIRES_RUBBER =
    AGRICULTURE =
    BREWERS =
    DISTILLERS =
    DRUG_RETAIL =
    FOOD_DISTRIBUTORS =
    FOOD_RETAIL =
    HOUSEHOLD_PRODUCTS =
    HYPERMARKETS =
    PACKAGED_FOOD =
    PERSONAL_PRODUCTS =
    SOFT_DRINKS =
    TOBACCO =
    OIL_GAS_INTEGRATED =
    OIL_GAS_DRILLING =
    OIL_GAS_EQUIPMENT =
    OIL_GAS_EXPLORATION =
    OIL_GAS_REFINING =
    OIL_GAS_STORAGE =
    ASSET_MANAGEMENT =
    CONSUMER_FINANCE =
    DIVERSIFIED_BANKS =
    FINANCIAL_EXCHANGES =
    INSURANCE =
    INVESTMENT_BANKING =
    HEALTH_INSURANCE =
    MULTILINE_INSURANCE =
    MULTISECTOR_HOLDINGS =
    PROPERTY_INSURANCE =
    REGIONAL_BANKS =
    REINSURANCE =
    THRIFT_MORTGAGE =
    BIOTECHNOLOGY =
    HEALTH_CARE_DISTRIBUTORS =
    HEALTH_CARE_EQUIPMENT =
    HEALTH_CARE_FACILITIES =
    HEALTH_CARE_SERVICES =
    HEALTH_CARE_SUPPLIES =
    HEALTH_CARE_TECHNOLOGY =
    LIFE_SCIENCE_TOOLS =
    MANAGED_HEALTH_CARE =
    PHARMACEUTICALS =
    AEROSPACE_DEFENSE =
    FARM_MACHINERY =
    AIR_FREIGHT =
    AIRLINES =
    BUILDING_PRODUCTS =
    CONSTRUCTION_ENGINEERING =
    HEAVY_TRUCKS =
    DIVERSIFIED_SUPPORT =
    ELECTRICAL_EQUIPMENT =
    FACILITIES_SERVICES =
    EMPLOYMENT_SERVICES =
    INDUSTRIAL_CONGLOMERATES =
    INDUSTRIAL_MACHINERY =
    RAILROADS =
    RESEARCH_CONSULTING =
    TRADING_COMPANIES =
    TRUCKING =
    APPLICATION_SOFTWARE =
    COMMUNICATIONS_EQUIPMENT =
    DATA_PROCESSING =
    ELECTRONIC_COMPONENTS =
    ELECTRONIC_MANUFACTURING =
    HOME_ENTERTAINMENT =
    INTERNET_SOFTWARE =
    IT_CONSULTING =
    SEMICONDUCTOR_EQUIPMENT =
    SEMICONDUCTORS =
    SYSTEMS_SOFTWARE =
    STORAGE_PERIPHERALS =
    CONSTRUCTION_MATERIALS =
    COPPER =
    CHEMICALS =
    FERTILIZER_CHEMICALS =
    GOLD =
    INDUSTRIAL_GASES =
    METAL_GLASS =
    PAPER_PACKAGING =
    SPECIALTY_CHEMICALS =
    STEEL =
    HEALTH_CARE_REITS =
    HOTEL_RESORT_REITS =
    INDUSTRIAL_REITS =
    OFFICE_REITS =
    REAL_ESTATE_SERVICES =
    RESIDENTIAL_REITS =
    RETAIL_REITS =
    SPECIALIZED_REITS =
    TELECOMMUNICATION_SERVICES =
    ELECTRIC_UTILITIES =
    POWER_PRODUCERS =
    MULTI_UTILITIES =
    WATER_UTILITIES =

sector_code = 4
sector = Sector(sector_code)
print(sector)

# cast back to int
sector_code = int(sector)
print(sector_code)
'''