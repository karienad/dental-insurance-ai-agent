from datetime import datetime
from llm import initialize_llm
from typing import Optional

class InsuranceVerification:
    def __init__(self, office_name, patient_data):
        self.office_name = office_name
        self.patient_data = patient_data
        self.verification_data = {
            'eligibility': {
                'status': None,
                'effective_date': None,
                'plan_type': None
            },
            'benefits': {
                'annual_maximum': None,
                'remaining_maximum': None,
                'deductible': None,
                'deductible_met': None,
                'benefit_period': None
            },
            'coverage': {
                'preventive': None,
                'basic': None,
                'major': None,
                'periodontics': None,
                'endodontics': None
            },
            'limitations': {
                'waiting_period': None,
                'frequency': None,
                'missing_tooth': None,
                'pre_authorization': None
            }
        }
        
        self.extraction_functions = {
            'eligibility': {
                'status': self.extract_status,
                'effective_date': self.extract_date,
                'plan_type': self.extract_plan_type
            },
            'benefits': {
                'annual_maximum': self.extract_amount,
                'remaining_maximum': self.extract_amount,
                'deductible': self.extract_amount,
                'deductible_met': self.extract_amount,
                'benefit_period': self.extract_period
            },
            'coverage': {
                'preventive': self.extract_percentage,
                'basic': self.extract_percentage,
                'major': self.extract_percentage,
                'periodontics': self.extract_percentage,
                'endodontics': self.extract_percentage
            },
            'limitations': {
                'waiting_period': self.extract_period,
                'frequency': self.extract_frequency,
                'missing_tooth': self.extract_boolean,
                'pre_authorization': self.extract_boolean
            }
        }
        
        self.chat = initialize_llm()

    def extract_status(self, response: str, question: str) -> Optional[str]:
        """Extract insurance status from response"""
        print(f"\nDEBUG - Status Extraction:")
        print(f"Question: '{question}'")
        print(f"Response: '{response}'")
        
        try:
            prompt = f"""Given this question and response, determine the insurance status.
            Question: "{question}"
            Response: "{response}"
            
            Return only 'Active' if patient is eligible/active/covered,
            'Inactive' if not eligible/inactive/not covered,
            or 'None' if unclear.

            Examples:
            Q. "What is the patient's current eligibility status?" A: "The patient is currently active and eligible for benefits." -> "Active"
            Q. "What is the patient's current eligibility status?" A: "The patient's coverage is active and verified." -> "Active"
            Q. "What is the patient's current eligibility status?" A: "Yes, the patient is eligible and the coverage is in force." -> "Active"
            Q. "What is the patient's current eligibility status?" A: "The patient is eligible with active coverage status." -> "Inactive"
            """
            
            llm_response = self.chat.send_message({"text": prompt})
            result = llm_response.text.strip()
            print(f"LLM status result: '{result}'")
            
            if result in ['Active', 'Inactive']:
                return result
            return None
                
        except Exception as e:
            print(f"Error extracting status: {str(e)}")
            return None


    def extract_date(self, response: str, question: str) -> Optional[str]:
        """Extract date in MM/DD/YYYY format from the response given a specific question."""
        print(f"\nDEBUG - Date Extraction:")
        print(f"Question: '{question}'")
        print(f"Response: '{response}'")

        current_year = datetime.now().year

        try:
            prompt = f"""
            Given this question and response, extract the date and convert it to MM/DD/YYYY format.
            If the response refers to 'calendar year' or 'year end', use the current year ({current_year}) to determine the date.

            Question: "{question}"
            Response: "{response}"
            
            Examples:
            Q: "What is their effective date of coverage?" A: "The coverage effective date is January 1st, {current_year}." -> "01/01/{current_year}"
            Q: "What is their effective date of coverage?" A: "Their coverage began on March 15th, {current_year}." -> "03/15/{current_year}"
            Q: "What is their effective date of coverage?" A: "The effective date shows as September 1st, {current_year - 1}." -> "09/01/{current_year - 1}"
            Q: "What is their effective date of coverage?" A: "Coverage has been effective since July 1st, {current_year}." -> "07/01/{current_year}"
            Q: "What is their effective date of coverage?" A: "Coverage has been effective since the start of the year." -> "01/01/{current_year}"
            Q: "What is their benefit period?" A: "The benefit period is calendar year, January through December." -> "12/31/{current_year}"
            Q: "What is their benefit period?" A: "Benefits run on a fiscal year, July through June." -> "06/30/{current_year + 1}"
            Q: "When did the patient's treatment start?" A: "The treatment started on May 5th, {current_year}." -> "05/05/{current_year}"
            Q: "What was the date of service?" A: "The date of service was August 20th, {current_year}." -> "08/20/{current_year}"
            """

            llm_response = self.chat.send_message({"text": prompt})
            result = llm_response.text.strip()
            print(f"LLM date result: '{result}'")

            if result == 'None':
                return None

            # Validate the response looks like a date
            parts = result.split('/')
            if len(parts) == 3 and all(p.isdigit() for p in parts):
                return result

            return None

        except Exception as e:
            print(f"Error extracting date: {str(e)}")
            return None


    def extract_amount(self, response: str, question: str) -> Optional[float]:
        """Extract monetary amount from response"""
        print(f"\nDEBUG - Amount Extraction:")
        print(f"Question: '{question}'")
        print(f"Response: '{response}'")
        
        try:
            prompt = f"""Given this question and response, extract the dollar amount.
            Question: "{question}"
            Response: "{response}"
            
            Return only the number (no $ or commas) or 'None' if no amount found.
            
            Examples:
            Q: "What is the deductible amount?" A: "fifty dollars" -> "50"
            Q: "What is their annual maximum benefit?" A: "1k" -> "1000"
            Q: "How much deductible has been met?" A: "They haven't met any of the deductible yet." -> "0"
            """
            
            llm_response = self.chat.send_message({"text": prompt})
            result = llm_response.text.strip()
            print(f"LLM amount result: '{result}'")
            
            if result == 'None':
                return None
                
            try:
                return float(result)
            except ValueError:
                return None
                
        except Exception as e:
            print(f"Error extracting amount: {str(e)}")
            return None

    def extract_percentage(self, response: str, question: str) -> Optional[int]:
        """Extract percentage from the response given a specific question."""
        print(f"\nDEBUG - Percentage Extraction:")
        print(f"Question: '{question}'")
        print(f"Response: '{response}'")

        try:
            prompt = f"""
            Given this question and response, extract the percentage and return only the number (no % symbol) or 'None' if no percentage is found.
            Interpret phrases like 'half coverage' as 50% and 'full coverage' as 100%.
            
            Question: "{question}"
            Response: "{response}"
            
            Examples:
            Q: "What is the coverage percentage for preventive services?" A: "Preventive services are covered at 100%." -> "100"
            Q: "What about basic services?" A: "Basic services are covered at 80%." -> "80"
            Q: "What is the coverage for major services?" A: "Major services are covered at 50%." -> "50"
            Q: "What's the coverage for periodontal services?" A: "Periodontal services are covered at 80%." -> "80"
            Q: "What is the coverage percentage for preventive services?" A: "Preventive services have full coverage." -> "100"
            Q: "What about basic services?" A: "Basic services have half coverage." -> "50"
            """

            llm_response = self.chat.send_message({"text": prompt})
            result = llm_response.text.strip()
            print(f"LLM percentage result: '{result}'")

            if result == 'None':
                return None

            try:
                percentage = int(result)
                if 0 <= percentage <= 100:
                    return percentage
                return None
            except ValueError:
                return None

        except Exception as e:
            print(f"Error extracting percentage: {str(e)}")
            return None


    def extract_plan_type(self, response: str, question: str) -> Optional[str]:
        """Extract insurance plan type from the response given a specific question."""
        print(f"\nDEBUG - Plan Type Extraction:")
        print(f"Question: '{question}'")
        print(f"Response: '{response}'")

        try:
            prompt = f"""
            Given this question and response, extract the insurance plan type.
            Common types include: PPO, HMO, DHMO, Indemnity, etc.
            Return only the plan type or 'None' if unclear. No other text.

            Question: "{question}"
            Response: "{response}"
            
            Examples:
            Q: "What type of plan do they have?" A: "This is a PPO plan." -> "PPO"
            Q: "What type of plan do they have?" A: "They have a DHMO plan." -> "DHMO"
            Q: "What type of plan do they have?" A: "It's an indemnity plan." -> "Indemnity"
            Q: "What type of plan do they have?" A: "The patient has a PPO Plus plan." -> "PPO Plus"
            """

            llm_response = self.chat.send_message({"text": prompt})
            result = llm_response.text.strip()
            print(f"LLM plan type result: '{result}'")

            if result == 'None':
                return None
            return result

        except Exception as e:
            print(f"Error extracting plan type: {str(e)}")
            return None


    def extract_group_number(self, response: str, question: str) -> Optional[str]:
        """Extract group number from the response given a specific question."""
        print(f"\nDEBUG - Group Number Extraction:")
        print(f"Question: '{question}'")
        print(f"Response: '{response}'")

        try:
            prompt = f"""
            Given this question and response, extract the insurance group number.
            The group number might be labeled as 'Group #', 'Group Number', or similar.
            Return only the group number or 'None' if not found. No other text.

            Question: "{question}"
            Response: "{response}"
            
            Examples:
            Q: "Could you verify their group number?" A: "The group number is 123456." -> "123456"
            Q: "Could you verify their group number?" A: "I'm showing group number 789012." -> "789012"
            Q: "Could you verify their group number?" A: "Yes, the group number is 345678." -> "345678"
            Q: "Could you verify their group number?" A: "The verified group number is 901234." -> "901234"
            """

            llm_response = self.chat.send_message({"text": prompt})
            result = llm_response.text.strip()
            print(f"LLM group number result: '{result}'")

            if result == 'None':
                return None
            return result

        except Exception as e:
            print(f"Error extracting group number: {str(e)}")
            return None


    def extract_period(self, response: str, question: str) -> Optional[str]:
        """Extract benefit or waiting period from the response given a specific question."""
        print(f"\nDEBUG - Period Extraction:")
        print(f"Question: '{question}'")
        print(f"Response: '{response}'")

        try:
            prompt = f"""
            Given this question and response, extract the time period.
            Common formats include: 'Calendar Year', 'Contract Year', '6 months', '12 months', etc.
            Return only the period or 'None' if not found. No other text.

            Question: "{question}"
            Response: "{response}"
            
            Examples:
            Q: "What is their benefit period?" A: "The benefit period is calendar year, January through December." -> "Calendar Year"
            Q: "What is their benefit period?" A: "Benefits run on a fiscal year, July through June." -> "Fiscal Year"
            Q: "What is their benefit period?" A: "It's a calendar year benefit period." -> "Calendar Year"
            Q: "What is their benefit period?" A: "The benefit period follows the calendar year." -> "Calendar Year"
            """

            llm_response = self.chat.send_message({"text": prompt})
            result = llm_response.text.strip()
            print(f"LLM period result: '{result}'")

            if result == 'None':
                return None
            return result

        except Exception as e:
            print(f"Error extracting period: {str(e)}")
            return None


    def extract_frequency(self, response: str, question: str) -> Optional[dict]:
        """Extract frequency limitations from the response given a specific question."""
        print(f"\nDEBUG - Frequency Extraction:")
        print(f"Question: '{question}'")
        print(f"Response: '{response}'")

        try:
            prompt = f"""
            Given this question and response, extract the frequency limitation for each type of service mentioned.
            Common formats include: 'Once every 6 months', '2 per year', 'Annual', etc.
            Return a dictionary with the type of service as the key and the frequency as the value. If unable to extract, return the original response as the value.

            Question: "{question}"
            Response: "{response}"
            
            Examples:
            Q: "What are the frequency limitations?" A: "Cleanings are covered twice per calendar year." -> {{"Cleanings": "twice per calendar year"}}
            Q: "What are the frequency limitations?" A: "Exams and cleanings twice per year, x-rays once every 3 years." -> {{"Exams": "twice per year", "Cleanings": "twice per year", "X-rays": "once every 3 years"}}
            Q: "What are the frequency limitations?" A: "Two cleanings per year with 6 months separation required." -> {{"Cleanings": "twice per year, 6 months separation"}}
            Q: "What are the frequency limitations?" A: "Comprehensive exams once every 3 years, routine exams twice per year." -> {{"Comprehensive exams": "once every 3 years", "Routine exams": "twice per year"}}
            """

            llm_response = self.chat.send_message({"text": prompt})
            result = llm_response.text.strip()
            print(f"LLM frequency result: '{result}'")

            if result == 'None':
                return {"Original Response": response}
            
            try:
                # Convert the string representation of a dictionary to an actual dictionary
                frequency_dict = eval(result)
                return frequency_dict
            except (SyntaxError, ValueError):
                return {"Original Response": response}

        except Exception as e:
            print(f"Error extracting frequency: {str(e)}")
            return {"Original Response": response}

    def extract_boolean(self, question: str, response: str) -> Optional[bool]:
        """Extract yes/no answer from the response given a specific question."""
        print(f"\nDEBUG - Boolean Extraction:")
        print(f"Question: '{question}'")
        print(f"Response: '{response}'")

        try:
            prompt = f"""
            Given this question and response, analyze the text to determine if it indicates a positive (yes) or negative (no) response.
            Consider common positive and negative indicators:

            Common positive indicators: yes, sure, affirmative, absolutely, of course, definitely, indeed, active, 
            eligible, covered, required, approved, confirmed, consent, positive, agree, proceed, what do you want, 
            what would you like, what would you like to do, what do you want to verify, what would you like to verify, 
            what can I help you with
            Common negative indicators: no, not, never, inactive, ineligible, not covered, not required, denied, rejected, 
            negative, disagree

            Note: Questions that ask for the next action or verification, such as 'Sure, what would you like to verify?' 
            or 'What do you want to do?' should be treated as positive (yes) responses.

            Question: "{question}"
            Response: "{response}"

            Return only one of the following: 'True' for positive, 'False' for negative, or 'None' if unclear. No other text.
            """

            llm_response = self.chat.send_message({"text": prompt})
            result = llm_response.text.strip().upper()  # Convert to uppercase for comparison

            print(f"Raw LLM response: '{llm_response.text}'")
            print(f"Cleaned result: '{result}'")

            # Check the result
            if result == 'TRUE':
                print("Returning True")
                return True
            elif result == 'FALSE':
                print("Returning False")
                return False
            else:
                print("Returning None")
                return None

        except Exception as e:
            print(f"Error in extract_boolean: {str(e)}")
            return None