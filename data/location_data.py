location_data = {
    # Creates a list of countries
    # TODO: Add more countries
    "countries": {
        "United States": {
            "country_code": "US",
            "regions": {
                "Northeast": ["NY", "MA", "CT", "NJ", "PA", "RI", "VT", "NH", "ME"],
                "South": ["TX", "LA", "OK", "AR", "MS", "AL", "GA", "FL", "SC", "NC", "VA", "WV", "KY", "TN", "DC", "MD", "DE"],
                "Midwest": ["IL", "IN", "MI", "OH", "WI", "IA", "MO", "ND", "SD", "NE", "KS", "MN"],
                "West": ["CA", "OR", "WA", "NV", "ID", "MT", "WY", "CO", "NM", "AZ", "UT", "HI"]
            },
            "languages": ["English", "Spanish"],
            "timezone_ranges": ["UTC-10", "UTC-09", "UTC-08", "UTC-07", "UTC-06", "UTC-05"]
        },
        "United Kingdom": {
            "country_code": "GB",
            "regions": {
                "England": ["London", "Manchester", "Liverpool", "Birmingham"],
                "Scotland": ["Edinburgh", "Glasgow", "Aberdeen"],
                "Wales": ["Cardiff", "Newport", "Swansea"],
                "Northern Ireland": ["Belfast", "Derry", "Lisburn"]
            },
            "languages": ["English"],
            "timezone_ranges": ["UTC+00", "UTC+01"]
        },
        "Australia": {
            "country_code": "AU",
            "regions": {
                "New South Wales": ["Sydney", "Newcastle", "Wollongong"],
                "Victoria": ["Melbourne", "Geelong", "Ballarat"],
                "Queensland": ["Brisbane", "Gold Coast", "Sunshine Coast"],
                "Western Australia": ["Perth", "Fremantle", "Mandurah"]
            },
            "languages": ["English"],
            "timezone_ranges": ["UTC+8", "UTC+9", "UTC+10", "UTC+11"]
        },
        "China": {
            "country_code": "CN",
            "regions": {
                "Eastern": ["Shanghai", "Jiangsu", "Zhejiang"],
                "Southern": ["Guangdong", "Fujian", "Hainan"],
                "Northern": ["Shandong", "Henan", "Hebei", "Shanxi"],
                "Central": ["Henan", "Hubei", "Hunan"]
            },
            "languages": ["Chinese"],
            "timezone_ranges": ["UTC+8"]
        },
        "India": {
            "country_code": "IN",
            "regions": {
                "North": ["Delhi", "Uttar Pradesh", "Punjab"],
                "South": ["Karnataka", "Tamil Nadu", "Kerala"],
                "East": ["West Bengal", "Bihar", "Odisha"],
                "West": ["Maharashtra", "Gujarat", "Rajasthan"]
            },
            "languages": ["Hindi", "English", "Bengali", "Telugu", "Tamil"],
            "timezone_ranges": ["UTC+5:30"]
        },
        "Philippines": {
            "country_code": "PH",
            "regions": {
                "Luzon": ["Metro Manila", "Calabarzon", "Central Luzon"],
                "Visayas": ["Cebu", "Iloilo", "Bacolod"],
                "Mindanao": ["Davao", "Cagayan de Oro", "Zamboanga"]
            },
            "languages": ["Filipino", "English", "Cebuano", "Ilocano"],
            "timezone_ranges": ["UTC+8"]
        },
        "United Arab Emirates": {
            "country_code": "AE",
            "regions": {
                "Emirates": ["Abu Dhabi", "Dubai", "Sharjah", "Ajman", "Umm Al Quwain", "Ras Al Khaimah", "Fujairah"]
            },
            "languages": ["Arabic", "English"],
            "timezone_ranges": ["UTC+4"]
        },
        "Japan": {
            "country_code": "JP",
            "regions": {
                "Kanto": ["Tokyo", "Yokohama", "Saitama"],
                "Kansai": ["Osaka", "Kyoto", "Kobe"],
                "Chubu": ["Nagoya", "Niigata", "Shizuoka"],
                "Hokkaido": ["Sapporo", "Asahikawa", "Hakodate"]
            },
            "languages": ["Japanese"],
            "timezone_ranges": ["UTC+9"]
        },
    },
    "country_codes": {
        "US": "United States",
        "GB": "United Kingdom",
        "AU": "Australia",
        "CN": "China",
        "IN": "India",
        "PH": "Philippines",
        "AE": "United Arab Emirates",
        "JP": "Japan",
    }
}
