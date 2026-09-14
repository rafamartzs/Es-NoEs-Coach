QUESTION_SPECS = {
    1: {
        "dimension": "WHAT",
        "name": "Object with defect",
        "objective": "Precisely delimit the affected population and find the closest useful IS-NOT comparison.",
        "weak_answers": [
            "A broad product family when a specific part number is known",
            "A different part number when OK units of the same part number are available",
            "A comparison that changes many relevant conditions at once",
        ],
        "investigation_examples": [
            "Check serial/part-number traceability",
            "Find OK units inside the same affected population",
            "Compare same part number, same machine, and close production time first",
        ],
    },
    2: {
        "dimension": "WHAT",
        "name": "Defect at object",
        "objective": "Describe the defect as an observable or measurable condition, not as a presumed cause.",
        "weak_answers": [
            "Machine unstable",
            "Bad sensor",
            "Part is wrong",
        ],
        "investigation_examples": [
            "Measure the characteristic against specification",
            "Record location, size, severity, or deviation",
            "Use photos or measurement records when appropriate",
        ],
    },
    3: {
        "dimension": "WHERE",
        "name": "Geographical location",
        "objective": "Determine physical scope: plant, line, customer, area, machine, storage location, etc.",
        "weak_answers": [
            "It does not happen elsewhere, when elsewhere has not been checked",
            "Using lack of reports as proof that the failure is absent",
        ],
        "investigation_examples": [
            "Review complaints and quality records in comparable locations",
            "Check inventory and traceability by location",
        ],
    },
    4: {
        "dimension": "WHERE",
        "name": "Process location",
        "objective": "Identify where the defect is demonstrably present and distinguish generation from detection.",
        "weak_answers": [
            "The failure occurs at Station 7 because Station 7 is where it is measured",
        ],
        "investigation_examples": [
            "Inspect before and after candidate operations",
            "Use temporary measurements at upstream/downstream stations",
            "Trace selected parts through the process",
        ],
    },
    5: {
        "dimension": "WHERE",
        "name": "Location on object",
        "objective": "Localize the defect on the object: side, slot, segment, plane, surface, coordinate, region, etc.",
        "weak_answers": ["On the part", "On the commutator"],
        "investigation_examples": [
            "Create a defect map",
            "Mark photos or drawings",
            "Measure defect position relative to a datum",
        ],
    },
    6: {
        "dimension": "WHEN",
        "name": "First occurrence / observation / claim",
        "objective": "Build a time boundary: last confirmed OK -> relevant changes -> first confirmed NOK. Separate occurrence, detection, and claim dates.",
        "weak_answers": ["A few days ago", "Since the complaint date"],
        "investigation_examples": [
            "Review historical measurements and traceability",
            "Check machine events, maintenance, model changes, and scrap records",
        ],
    },
    7: {
        "dimension": "WHEN",
        "name": "Trend, repetition, rhythm of occurrence",
        "objective": "Detect temporal or sequential patterns: every N parts, startup, shift, model change, maintenance, warm-up, etc.",
        "weak_answers": ["Random"],
        "investigation_examples": [
            "Order parts by timestamp or sequence number",
            "Create a run chart",
            "Repeat the cycle under observation",
        ],
    },
    8: {
        "dimension": "WHEN",
        "name": "Life-cycle stage",
        "objective": "Determine at what life-cycle stage the defect is observed: manufacturing, test, storage, transport, customer assembly, use, aging, etc.",
        "weak_answers": [
            "Assuming the stage where the defect is detected is the stage where it was created"
        ],
        "investigation_examples": [
            "Inspect at multiple life-cycle checkpoints",
            "Compare retained samples before and after transport/assembly",
        ],
    },
    9: {
        "dimension": "WHO",
        "name": "Who observed the failure",
        "objective": "Identify who detects the failure and with what detection method/opportunity. Do not equate observer with cause.",
        "weak_answers": [
            "Operator A sees it, therefore Operator A causes it",
            "Comparing observers who use different detection methods as if detection capability were equal",
        ],
        "investigation_examples": [
            "Compare inspection method, sampling frequency, sensitivity, and criteria",
            "Verify whether multiple people can detect the same mode under the same method",
        ],
    },
    10: {
        "dimension": "HOW_MANY",
        "name": "How many objects show the failure",
        "objective": "Quantify incidence using numerator and denominator whenever possible.",
        "weak_answers": ["Many", "Several", "17 pieces without total inspected"],
        "investigation_examples": [
            "Perform sorting/containment",
            "Request customer inspection quantities",
            "Use traceability and inventory records",
        ],
    },
    11: {
        "dimension": "HOW_MANY",
        "name": "How much of the object is affected",
        "objective": "Quantify severity or extent within each object.",
        "weak_answers": ["Confusing number of NOK pieces with severity per piece"],
        "investigation_examples": [
            "Measure affected length, area, roughness, number of slots, deviation, etc.",
            "Map severity by location",
        ],
    },
    12: {
        "dimension": "HOW_MANY",
        "name": "How many defects are in the object",
        "objective": "Count distinct defect events/sites/modes within a single object.",
        "weak_answers": ["Three defects when actually three separate parts are affected"],
        "investigation_examples": [
            "Perform 100% inspection of selected units",
            "Record number and location of defects per object",
        ],
    },
    13: {
        "dimension": "HOW_MANY",
        "name": "Quantitative trend / repetition",
        "objective": "Determine how incidence or severity changes over time, sequence, lot, machine, supplier, etc.",
        "weak_answers": ["It is increasing, without data"],
        "investigation_examples": [
            "Plot NOK rate, defects per part, or severity versus time/sequence/lot",
            "Look for clusters and step changes",
        ],
    },
}
