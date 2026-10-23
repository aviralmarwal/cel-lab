# CEL Lab site content. Edit this file, then run build.py.

LAB = {
    "short": "CEL Lab",
    "name": "City Experimentation and Learning Lab",
    "dept": "Department of Humanities & Social Sciences",
    "inst": "IIT Roorkee",
    "address": "Department of Humanities & Social Sciences, Indian Institute of Technology Roorkee, Roorkee 247667, Uttarakhand, India",
    "email": "aviral.marwal@hs.iitr.ac.in",
    "domain": "cel-lab.in",
    "cname_live": False,
    "form_endpoint": "https://api.web3forms.com/submit",  # form backend; empty = email-client fallback
    "form_access_key": "fce0812b-949e-4f23-8aa5-bb751459a329",   # Web3Forms access key (from web3forms.com)
    "description": (
        "CEL Lab is an urban economics and policy research group at IIT Roorkee. "
        "We treat cities as places to experiment and learn: building empirical evidence on "
        "urban growth, land, housing, infrastructure and local governance, and working with "
        "city governments to test what actually improves urban outcomes."
    ),
    "year": 2026,
}

THEMES = [
    {
        "slug": "urban-growth-simulation",
        "title": "Urban growth simulation",
        "short": "Spatially explicit models of where Indian cities will expand, and what policy can change about it.",
        "intro": (
            "How will Indian cities look in 2040? We build spatially explicit models of urban "
            "expansion — cellular automata, agent-based and econometric — calibrated on satellite-derived "
            "land cover, census data and infrastructure networks, to simulate where growth will go under "
            "alternative policy and infrastructure scenarios."
        ),
        "issues": [
            "Projecting built-up expansion and densification at the city-region scale",
            "Scenario testing: ring roads, transit corridors, master-plan land-use rules",
            "Peri-urban conversion of agricultural land",
            "Validating growth models against observed change",
        ],
    },
    {
        "slug": "facility-mapping-accessibility",
        "title": "Facility mapping and accessibility modelling",
        "short": "Where public facilities are, who can reach them, and where new ones would do the most good.",
        "intro": (
            "Where are schools, health centres, markets and transit stops — and who can actually reach them? "
            "We map facilities at fine spatial resolution and model accessibility by walking, cycling and "
            "public transport, to identify under-served neighbourhoods and evaluate where new facilities "
            "would do the most good."
        ),
        "issues": [
            "Building complete, geocoded facility inventories for Indian cities",
            "Measuring access gaps by income, gender and neighbourhood",
            "Optimal location of new public facilities",
            "Accessibility as an input to service-delivery planning by city governments",
        ],
    },
    {
        "slug": "commuting-built-environment-typologies",
        "title": "Commuting behaviour, built environment and neighbourhood typologies",
        "short": "How neighbourhood form shapes the way people travel, and how to classify neighbourhoods for planning.",
        "intro": (
            "How people travel is shaped by where they live and work and by the form of the neighbourhoods "
            "around them. We study commuting patterns and mode choice, link them to density, land-use mix, "
            "street networks and transit, and classify neighbourhoods into typologies that help planners "
            "target interventions."
        ),
        "issues": [
            "Mode choice and commute distance in Indian cities",
            "Built-environment measures (density, diversity, design) at neighbourhood scale",
            "Data-driven neighbourhood typologies",
            "Travel implications of new housing and job locations",
        ],
    },
    {
        "slug": "housing-affordability-segregation",
        "title": "Housing affordability, residential segregation and gentrification",
        "short": "Who can afford to live where, how households sort across the city, and how neighbourhoods change.",
        "intro": (
            "Who can afford to live where, and how is that changing? We examine housing prices and rents, "
            "the spatial sorting of households by income and social group, and the dynamics of neighbourhood "
            "change — including displacement pressures from redevelopment and infrastructure investment."
        ),
        "issues": [
            "Measuring affordability across cities and over time",
            "Patterns and drivers of residential segregation",
            "Neighbourhood upgrading, redevelopment and displacement",
            "Policy levers: housing supply, rental markets, inclusionary rules",
        ],
    },
    {
        "slug": "industrial-agglomeration-growth",
        "title": "Industrial agglomeration and city economic growth",
        "short": "Where firms and workers cluster, the productivity gains that follow, and what holds city growth back.",
        "intro": (
            "Cities grow when firms and workers cluster. We study where industries locate within and across "
            "Indian cities, the productivity gains from agglomeration, and how misallocation of workers and "
            "firms across the urban system holds back growth."
        ),
        "issues": [
            "Location of manufacturing and services within city-regions",
            "Agglomeration economies and productivity in Indian cities",
            "Spatial misallocation of skill-heterogeneous workers across cities",
            "Industrial policy, SEZs and corridor investments",
        ],
    },
    {
        "slug": "land-use-optimisation",
        "title": "Land use optimisation for sustainable urbanisation",
        "short": "Allocating scarce urban land among housing, industry, green space and infrastructure.",
        "intro": (
            "Land is a city's scarcest resource. We develop optimisation and scenario tools that allocate land "
            "among housing, industry, green space and infrastructure to meet growth needs while limiting sprawl, "
            "protecting ecologically sensitive areas and reducing emissions."
        ),
        "issues": [
            "Multi-objective land-use allocation models",
            "Compact vs. dispersed growth trade-offs",
            "Green cover, heat and climate resilience in land-use planning",
            "Translating optimisation outputs into master-plan inputs",
        ],
    },
    {
        "slug": "municipal-finance-property-tax",
        "title": "Municipal finance, property tax and urban sprawl",
        "short": "How cities value and tax land, how tax design shapes sprawl, and how to close the revenue gap.",
        "intro": (
            "Indian cities raise far less own-revenue than they need. We study how urban local bodies value and "
            "tax land and property, how tax design shapes land use and sprawl, and how better data — GIS, "
            "satellite footprints, drone surveys — can close the gap between what cities could collect and "
            "what they do."
        ),
        "issues": [
            "Property-tax systems across Indian states: valuation, rates, collection",
            "Land value taxation and its effect on land use and sprawl",
            "Revenue-gap estimation using spatial data",
            "Working with municipalities on plot-level pilots",
        ],
    },
]

PROJECTS = [
    {
        "title": "Assessment of Financial Resources of Local Self-Governing Institutions (PRIs and ULBs) in Uttarakhand",
        "role": "Co-PI", "status": "ongoing", "start": "2025-05", "end": "",
        "funder": "SETU Aayog, Government of Uttarakhand",
        "years": "2025 – present",
        "summary": (
            "A state-wide assessment of the revenue base, expenditure patterns and fiscal capacity of Uttarakhand's "
            "panchayati raj institutions and urban local bodies, identifying constraints on own-source revenue and "
            "options for strengthening local finances."
        ),
        "themes": ["municipal-finance-property-tax"],
    },
    {
        "title": "Taxing Vacant Land: A Pan-India Panel Study of Property Tax Discounts and Urban Sprawl in Metropolitan and Tier-2 Cities",
        "role": "PI", "status": "ongoing", "start": "", "end": "",  # dates to confirm
        "summary": (
            "Builds a multi-city, multi-year panel of property-tax rules and rates across Indian metropolitan and "
            "tier-2 cities to examine how concessions on vacant land affect land holding, development timing and "
            "the outward spread of cities."
        ),
        "themes": ["municipal-finance-property-tax", "land-use-optimisation"],
    },
    {
        "title": "Property Tax, Land Records and Urban Growth in Nagar Nigam Roorkee: A Plot-Level Assessment and Policy Options",
        "role": "PI", "status": "ongoing", "start": "", "end": "",  # dates to confirm
        "summary": (
            "A plot-level study of Roorkee's property-tax register and land records, matched to GIS and satellite "
            "footprints, to estimate the gap between taxable and taxed property, trace how growth is occurring "
            "across the city, and set out policy options for the municipal corporation."
        ),
        "themes": ["municipal-finance-property-tax", "urban-growth-simulation"],
    },
    {
        "title": "Population Synthesis for Disaggregated Travel Demand Modelling",
        "role": "Co-PI", "status": "ongoing", "start": "", "end": "",  # dates to confirm
        "summary": (
            "Builds a synthetic population of households and individuals for Bengaluru — matched to census "
            "marginals and survey microdata — as the foundation for disaggregated, activity-based travel demand "
            "modelling. A second phase of the Aggregate-M3DM city-scale mobility demand project, carried out with "
            "the Centre for infrastructure, Sustainable Transportation and Urban Planning (CiSTUP), IISc Bengaluru."
        ),
        "partner": "CiSTUP, IISc Bengaluru",
        "themes": ["commuting-built-environment-typologies"],
    },
    {
        "title": "Neighbourhood Accessibility and Gentrification",
        "role": "PI", "status": "ongoing", "start": "2025-09", "end": "",
        "funder": "SRIC, IIT Roorkee",
        "years": "2025 – present",
        "summary": (
            "Examines how changes in neighbourhood accessibility — new transit, roads and amenities — feed into "
            "housing prices, household sorting and gentrification pressures in Indian cities, and what this means "
            "for who benefits from urban investment."
        ),
        "themes": ["housing-affordability-segregation", "facility-mapping-accessibility"],
    },
    {
        "title": "Mapping Opportunities for Healthy and Sustainable Urban Transitions in Post-Industrial Cities",
        "role": "Collaborator", "status": "collaboration", "start": "", "end": "",  # dates to confirm
        "partner": "Urban Studies Foundation, UK",
        "summary": (
            "A research collaboration with the Urban Studies Foundation on how post-industrial cities can steer "
            "transitions towards healthier and more sustainable urban environments, and where the opportunities "
            "for such transitions lie."
        ),
        "themes": ["land-use-optimisation"],
    },
]

# Work in progress, listed on the theme page. Keep to what you're happy to show publicly.
ONGOING = [
    # {"title": "Working title", "note": "One or two lines: question, data, expected output.", "theme": "urban-growth-simulation"},
]

EVENTS = [
    {
        "kind": "Seminar",
        "date": "2025-12-09",
        "date_text": "9 December 2025, 2 PM",
        "title": "Mapping New Directions in Urbanisation: Challenges and Emerging Futures",
        "venue": "Committee Room, 2nd Floor, Department of Humanities & Social Sciences, IIT Roorkee",
        "speakers": [
            {"name": "Dr. Arup Mitra", "aff": "Head, Faculty of Economics, South Asian University, Delhi"},
            {"name": "Dr. Prafulla Parlewar", "aff": "Head, Faculty of Urban Planning, School of Planning and Architecture, Delhi"},
        ],
        "convener": "Dr. Aviral Marwal",
        "support": "Supported by the Urban Studies Foundation",
        "summary": (
            "A seminar talk bringing together an urban economist and an urban planner to take stock of how "
            "Indian urbanisation is changing — the pressures on cities, the policy directions emerging in response, "
            "and the research questions that follow."
        ),
        "poster": "assets/events/seminar-2025-12-poster.jpg",
    },
]

TALKS = [  # papers presented and invited talks, newest first
    {"date": "2024-04", "date_text": "April 2024", "kind": "Invited lecture",
     "title": "Gentrification and housing affordability", "venue": "O. P. Jindal Global University",
     "themes": ["housing-affordability-segregation"]},
    {"date": "2023-10", "date_text": "October 2023", "kind": "Invited talk",
     "title": "An analytical framework to study urbanisation using spatial data", "venue": "CiSTUP, Indian Institute of Science, Bengaluru",
     "themes": ["urban-growth-simulation"]},
    {"date": "2023-09", "date_text": "September 2023", "kind": "Invited talk",
     "title": "Building geospatial data from satellite imagery to study urban form", "venue": "Urban Big Data Centre, University of Glasgow",
     "themes": ["commuting-built-environment-typologies"]},
    {"date": "2023-08", "date_text": "August 2023", "kind": "Paper presented",
     "title": "Utilizing ABM and neural network models to simulate built-up expansion in Delhi",
     "venue": "International Association for Mathematical Geosciences (IAMG) conference, NTNU Trondheim, Norway",
     "themes": ["urban-growth-simulation"]},
    {"date": "2023-07", "date_text": "July 2023", "kind": "Paper presented",
     "title": "A study of the commuting pattern of households in Delhi",
     "venue": "Regional Science Association International (RSAI) conference, University of Newcastle, UK",
     "themes": ["commuting-built-environment-typologies"]},
]

CONFERENCES = [  # conferences attended, newest first
    {"date": "2026-06", "date_text": "14–18 June 2026", "title": "RSA Annual Conference: Regions as Arenas in a Changing World", "venue": "Sweden", "note": "Funded by IIT Roorkee"},
    {"date": "2025-12", "date_text": "23–25 December 2025", "title": "Conference on Cities and Urban Planning in Ancient India", "venue": "IIT Indore", "note": ""},
    {"date": "2023-08", "date_text": "1–4 August 2023", "title": "IAMG Conference", "venue": "NTNU Trondheim, Norway", "note": "Funded by the University of Cambridge"},
]

NEWS = [  # short dated items for the timeline and the home-page strip, newest first
    {"date": "2026-06", "date_text": "June 2026", "text": "Aviral attends the RSA Annual Conference in Sweden, funded by IIT Roorkee.", "link": "events.html"},
    {"date": "2025-12", "date_text": "December 2025", "text": "CEL Lab hosts the seminar \u201cMapping New Directions in Urbanisation\u201d with Arup Mitra (SAU) and Prafulla Parlewar (SPA Delhi), supported by the Urban Studies Foundation.", "link": "events.html"},
    {"date": "2025-12", "date_text": "December 2025", "text": "Participation in the Conference on Cities and Urban Planning in Ancient India, IIT Indore.", "link": "events.html"},
    {"date": "2025-09", "date_text": "September 2025", "text": "New SRIC-funded project on neighbourhood accessibility and gentrification begins.", "link": "projects.html"},
    {"date": "2025-07", "date_text": "July 2025", "text": "Ankita Dey joins the lab as a PhD scholar, working on urban land use policy.", "link": "people.html"},
    {"date": "2025-05", "date_text": "May 2025", "text": "Work begins on the assessment of financial resources of PRIs and ULBs in Uttarakhand.", "link": "projects.html"},
    {"date": "2025-01", "date_text": "January 2025", "text": "Nikhil Mishra joins the lab as a PhD scholar, working on firm agglomeration and urbanisation.", "link": "people.html"},
    {"date": "2024-11", "date_text": "November 2024", "text": "CEL Lab is set up at the Department of Humanities & Social Sciences, IIT Roorkee.", "link": "index.html"},
]

TEACHING = [
    {"code": "HS 535", "title": "Urban Economics", "term": "Autumn", "level": "PG / UG elective",
     "desc": "Why cities exist, how they grow, and how land, housing and transport markets shape them. Covers agglomeration, bid-rent and urban form, housing, transport and local public finance, with Indian cases throughout."},
    {"code": "HS 659", "title": "Spatial Data Analysis", "term": "Spring", "level": "PG",
     "desc": "Working with spatial data in R and GIS: geocoding, spatial joins, exploratory spatial data analysis, spatial autocorrelation and spatial regression, applied to urban and regional questions."},
    {"code": "HS 508", "title": "Institutional Economics", "term": "Spring", "level": "PG",
     "desc": "How institutions — property rights, contracts, governance and the state — shape economic outcomes, with applications to land, cities and development."},
    {"code": "HS 601", "title": "Welfare Economics", "term": "Autumn", "level": "PG",
     "desc": "Efficiency, equity and social choice; market failure and public intervention; the normative foundations of policy evaluation."},
]

THESES = [  # master's and BS-MS thesis supervision; title "" = ongoing
    {"name": "Akanksha Sahni", "prog": "BS-MS Economics", "year": "2026 – 27", "title": ""},
    {"name": "Yash Kumar", "prog": "BS-MS Economics", "year": "2026 – 27", "title": ""},
    {"name": "Kavish Jain", "prog": "BS-MS Economics", "year": "2026 – 27", "title": ""},
    {"name": "Samiksha Bharti", "prog": "M.Sc. Economics", "year": "2025 – 26", "title": "A study of fiscal decentralisation in urban local bodies"},
    {"name": "Arunesh Tomar", "prog": "BS-MS Economics", "year": "2025 – 26", "title": "Fracture points in trade: sub-sector export volatility, structural breaks, and policy implications in the post-COVID era"},
    {"name": "Madhav Mukund", "prog": "BS-MS Economics", "year": "2025 – 26", "title": "Analysing the impact of public investment on economic growth and equity"},
    {"name": "Vedant Dwivedi", "prog": "BS-MS Economics", "year": "2025 – 26", "title": "The role of informal institutions in shaping careers at IIT Roorkee and the determinants of entrepreneurship"},
]

BLOG = {
    "label": "Blog",
    "intro": "Short pieces from the lab: notes on data, methods and policy debates on Indian cities, written by lab members.",
    "dir": "posts",   # one Markdown file per post, with a header block (see posts/README.md)
}

OPPORTUNITIES = {
    "openings": [],  # e.g. {"title": "JRF, property tax and urban sprawl project", "note": "...", "deadline": "..."}
    "standing": (
        "We are always glad to hear from prospective PhD students, master's students looking for a dissertation "
        "topic, and interns with a background in economics, planning, geography or data science. Write to us with "
        "a short note on your interests and a CV. Funded positions are announced here and on the IIT Roorkee website."
    ),
}

PEOPLE = {
    "pi": {
        "name": "Dr. Aviral Marwal",
        "initials": "AM",
        "role": "Principal Investigator · Assistant Professor",
        "degree": "PhD (Cambridge)",
        "bio": (
            "Aviral leads CEL Lab at the Department of Humanities & Social Sciences, IIT Roorkee. His research "
            "models urban form, land use and accessibility in Indian cities using geosimulation tools — GIS, "
            "agent-based models and neural networks — and examines how land and tax policy shape urban growth. "
            "He holds a PhD in Land Economy from the University of Cambridge."
        ),
        "links": [{"label": "Download CV (PDF)", "url": "assets/people/Aviral-Marwal-CV.pdf"}],  # add e.g. {"label": "Google Scholar", "url": "..."}
        "photo": "assets/people/aviral-marwal.jpg",
    },
    "scholars": [
        {"name": "Nikhil Mishra", "initials": "NM", "role": "Research Scholar · PhD (since Jan 2025)", "topic": "Firm agglomeration and urbanisation", "photo": "assets/people/nikhil-mishra.jpg"},
        {"name": "Ankita Dey", "initials": "AD", "role": "Research Scholar · PhD (since Jul 2025)", "topic": "Urban land use policy", "photo": "assets/people/ankita-dey.jpg"},
    ],
    "interns": [  # current research interns
        {"name": "Shraman Joardar", "initials": "SJ", "role": "Research Intern (since Feb 2026)", "topic": "City-scale slum formation using agent-based modelling", "photo": None},
    ],
    "alumni": [  # past interns and members, newest first
        {"name": "Adarsh Singh", "affil": "B.Tech, NIT Delhi", "role": "SPARK Intern, May – July 2026", "topic": "Building the property tax database for cities in India"},
        {"name": "Anisha Kathpal", "affil": "PhD scholar, IIT Kanpur", "role": "SPARK Intern, May – July 2025", "topic": "Systematic literature review of state-led gentrification in the Global South"},
    ],
}

PUBLICATIONS = [
    {
        "type": "Peer-reviewed journal articles",
        "items": [
            {
                "authors": "Marwal, A., & Silva, E. A.",
                "year": 2024,
                "title": "Simulating built-up expansion in west Delhi using a neural network coupled agent-based prioritised growth model",
                "venue": "Letters in Spatial and Resource Sciences",
                "url": "https://doi.org/10.1007/s12076-024-00392-w",
                "themes": ["urban-growth-simulation"],
            },
            {
                "authors": "Marwal, A., & Silva, E. A.",
                "year": 2024,
                "title": "Analysing inequity in accessibility to services with neighbourhood location and socio-economic characteristics in Delhi",
                "venue": "Geographical Analysis",
                "url": "https://doi.org/10.1111/gean.12396",
                "themes": ["facility-mapping-accessibility"],
            },
            {
                "authors": "Marwal, A., & Silva, E. A.",
                "year": 2023,
                "title": "Exploring residential built-up form typologies in Delhi: a grid-based k-means clustering approach mapping sustainable urbanization",
                "venue": "npj Urban Sustainability",
                "url": "https://doi.org/10.1038/s42949-023-00112-1",
                "themes": ["commuting-built-environment-typologies", "land-use-optimisation"],
            },
            {
                "authors": "Marwal, A., & Silva, E. A.",
                "year": 2022,
                "title": "City affordability and residential location choice: a demonstration using an agent-based model",
                "venue": "Habitat International",
                "url": "https://www.sciencedirect.com/science/article/pii/S0197397523000760",
                "themes": ["housing-affordability-segregation"],
            },
            {
                "authors": "Marwal, A., & Silva, E. A.",
                "year": 2022,
                "title": "Literature review of accessibility measures and models used in land use and transportation planning in the last 5 years",
                "venue": "Journal of Geographical Sciences",
                "url": "https://doi.org/10.1007/s11442-022-1961-1",
                "themes": ["facility-mapping-accessibility"],
            },
        ],
    },
    {
        "type": "Working papers",
        "items": [
            {
                "authors": "Marwal, A., & Silva, E. A.",
                "year": 2024,
                "title": "Commuting behaviour, built environment and travel attitude: insights from a field survey in Delhi",
                "venue": "SSRN working paper",
                "url": "",
                "themes": ["commuting-built-environment-typologies"],
            },
        ],
    },
    {
        "type": "Conference papers",
        "items": [
            {
                "authors": "Pinjari, A. R., Rambha, T., Koushik, A., Marwal, A., et al.",
                "year": 2025,
                "title": "Aggregate-M3DM: a city-scale multi-modal mobility demand modelling tool for Indian cities",
                "venue": "8th Conference of the Transportation Research Group of India (CTRG 2025), IIT Guwahati",
                "url": "",
                "themes": ["commuting-built-environment-typologies"],
            },
        ],
    },
    {
        "type": "Teaching cases",
        "items": [
            {
                "authors": "Marwal, A., Naik, G., & Dalhia, M.",
                "year": 2020,
                "title": "The Saboo Foundation model of philanthropy: how a self-made man created thousands more",
                "venue": "Harvard Business Publishing, IIM Bangalore case IMB 844",
                "url": "",
                "themes": [],
            },
        ],
    },
]
