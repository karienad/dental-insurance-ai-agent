insurance_qa = {
    'eligibility': {
        'status': {
            'question': "What is the patient's current eligibility status?",
            'sample_answers': [
                "The patient is currently active and eligible for benefits.",
                "The patient's coverage is active and verified.",
                "Yes, the patient is eligible and the coverage is in force.",
                "The patient is eligible with active coverage status."
            ]
        },
        'effective_date': {
            'question': "What is their effective date of coverage?",
            'sample_answers': [
                "The coverage effective date is January 1st, 2024.",
                "Their coverage began on March 15th, 2024.",
                "The effective date shows as September 1st, 2023.",
                "Coverage has been effective since July 1st, 2023."
            ]
        },
        'plan_type': {
            'question': "What type of plan do they have?",
            'sample_answers': [
                "This is a PPO plan.",
                "They have a DHMO plan.",
                "It's an indemnity plan.",
                "The patient has a PPO Plus plan."
            ]
        },
        'group_number': {
            'question': "Could you verify their group number?",
            'sample_answers': [
                "The group number is 123456.",
                "I'm showing group number 789012.",
                "Yes, the group number is 345678.",
                "The verified group number is 901234."
            ]
        }
    },
    'benefits': {
        'annual_maximum': {
            'question': "What is their annual maximum benefit?",
            'sample_answers': [
                "The annual maximum is $1,500.",
                "They have a $2,000 annual maximum.",
                "The yearly maximum benefit is $1,000.",
                "Their annual maximum benefit is $2,500."
            ]
        },
        'remaining_maximum': {
            'question': "What is their remaining benefit amount?",
            'sample_answers': [
                "They have $1,200 remaining of their annual maximum.",
                "The remaining benefit is $800.",
                "There is $1,850 left in benefits for this year.",
                "The patient has $950 remaining in benefits."
            ]
        },
        'deductible': {
            'question': "What is their deductible amount?",
            'sample_answers': [
                "The annual deductible is $50 per person.",
                "There's a $100 deductible.",
                "The deductible is $75 individual.",
                "They have a $150 calendar year deductible."
            ]
        },
        'deductible_met': {
            'question': "How much of the deductible has been met, please provide dollar amount?",
            'sample_answers': [
                "The deductible has been fully met for this year.",
                "$25 of the deductible has been met.",
                "They haven't met any of the deductible yet.",
                "The deductible is met with $50 satisfied."
            ]
        },
        'benefit_period': {
            'question': "What is their benefit period?",
            'sample_answers': [
                "The benefit period is calendar year, January through December.",
                "Benefits run on a fiscal year, July through June.",
                "It's a calendar year benefit period.",
                "The benefit period follows the calendar year."
            ]
        }
    },
    'coverage': {
        'preventive': {
            'question': "What is the coverage percentage for preventive services?",
            'sample_answers': [
                "Preventive services are covered at 100%.",
                "They have 100% coverage for preventive care.",
                "Preventive is covered at 80%.",
                "The plan covers preventive services at 90%."
            ]
        },
        'basic': {
            'question': "What about basic services?",
            'sample_answers': [
                "Basic services are covered at 80%.",
                "They have 70% coverage for basic procedures.",
                "Basic services are at 80% after deductible.",
                "The plan pays 75% for basic services."
            ]
        },
        'major': {
            'question': "What is the coverage for major services?",
            'sample_answers': [
                "Major services are covered at 50%.",
                "Major procedures are at 60% coverage.",
                "They have 50% coverage for major services.",
                "The plan covers 40% for major procedures."
            ]
        },
        'periodontics': {
            'question': "What's the coverage for periodontal services?",
            'sample_answers': [
                "Periodontal services are covered at 80%.",
                "Periodontics falls under major at 50%.",
                "They have 70% coverage for periodontal procedures.",
                "Periodontal treatments are covered at 60%."
            ]
        },
        'endodontics': {
            'question': "And for endodontic services?",
            'sample_answers': [
                "Endodontic procedures are covered at 80%.",
                "Root canals and other endodontic services are at 50%.",
                "Endodontics is covered at 70%.",
                "They have 80% coverage for endodontic treatments."
            ]
        }
    },
    'limitations': {
        'waiting_period': {
            'question': "Are there any waiting periods?",
            'sample_answers': [
                "There's no waiting period for any services.",
                "Yes, there's a 6-month waiting period for major services.",
                "Basic services have a 3-month waiting period, major has 12 months.",
                "The plan has a 12-month waiting period for orthodontics."
            ]
        },
        'frequency': {
            'question': "What are the frequency limitations?",
            'sample_answers': [
                "Cleanings are covered twice per calendar year.",
                "Exams and cleanings twice per year, x-rays once every 3 years.",
                "Two cleanings per year with 6 months separation required.",
                "Comprehensive exams once every 3 years, routine exams twice per year."
            ]
        },
        'missing_tooth': {
            'question': "Is there a missing tooth clause?",
            'sample_answers': [
                "Yes, there is a missing tooth exclusion.",
                "No missing tooth clause on this plan.",
                "Missing teeth are not covered if extracted prior to coverage.",
                "The plan has a 12-month missing tooth provision."
            ]
        },
        'pre_authorization': {
            'question': "Are there any pre-authorization requirements?",
            'sample_answers': [
                "Pre-auth is required for all procedures over $300.",
                "No pre-authorization required for any services.",
                "Major services require pre-authorization.",
                "Pre-authorization needed for procedures exceeding $500."
            ]
        }
    }
}

