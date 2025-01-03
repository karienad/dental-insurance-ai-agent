def verify_patient(patient_data, query):
    if not hasattr(verify_patient, 'asked_fields'):
        verify_patient.asked_fields = set()
    if not hasattr(verify_patient, 'provided_fields'):
        verify_patient.provided_fields = set()

    query = query.lower().replace('?', ',').replace(' and ', ', ').replace('please', '').strip()
    requests = [req.strip() for req in query.split(',') if req.strip()]
    
    formatted_responses = {
        'name': f"{patient_data['first_name']} {patient_data['last_name']}",
        'date_of_birth': patient_data['date_of_birth'],
        'member_id': patient_data['member_number']
    }

    if any(word in query for word in ['name', 'who is', 'patient name']):
        return f"The patient's name is {formatted_responses['name']}"
        
    response_parts = []
    for request in requests:
        if not response_parts:
            if ('date' in request or 'birth' in request or 'dob' in request):
                verify_patient.asked_fields.add('dob')
                verify_patient.provided_fields.add('dob')
                response_parts.append(f"The date of birth is {formatted_responses['date_of_birth']}")
            elif ('member' in request or 'id' in request):
                verify_patient.asked_fields.add('member_id')
                verify_patient.provided_fields.add('member_id')
                response_parts.append(f"The member I..D is {formatted_responses['member_id']}")

    if len(response_parts) > 0:
        return " ".join(response_parts)
    return "What information would you like about the patient?"


class ConversationFlowManager:
    def __init__(self, verification, patient):
        self.verification = verification
        self.patient = patient
        self.is_patient_info_phase = True
        self.verification_started = False
        self.current_category = 'eligibility'
        
        self.insurance_qa = {
            'eligibility': {
                'status': {
                    'question': "What is the patient's current eligibility status?"
                },
                'effective_date': {
                    'question': "What is the effective date of coverage?"
                },
                'plan_type': {
                    'question': "What type of plan does the patient have?"
                }
            },
            'benefits': {
                'annual_maximum': {
                    'question': "What is the annual maximum benefit?"
                },
                'remaining_maximum': {
                    'question': "What is the remaining benefit amount?"
                },
                'deductible': {
                    'question': "What is the deductible amount?"
                },
                'deductible_met': {
                    'question': "How much of the deductible has been met? Please provide dollar amount."
                },
                'benefit_period': {
                    'question': "What is the benefit period?"
                }
            },
            'coverage': {
                'preventive': {
                    'question': "What is the coverage percentage for preventive services?"
                },
                'basic': {
                    'question': "What is the coverage percentage for basic services?"
                },
                'major': {
                    'question': "What is the coverage percentage for major services?"
                },
                'periodontics': {
                    'question': "What is the coverage percentage for periodontal services?"
                },
                'endodontics': {
                    'question': "What is the coverage percentage for endodontic services?"
                }
            },
            'limitations': {
                'waiting_period': {
                    'question': "Are there any waiting periods?"
                },
                'frequency': {
                    'question': "What are the frequency limitations?"
                },
                'missing_tooth': {
                    'question': "Is there a missing tooth clause?"
                },
                'pre_authorization': {
                    'question': "Are there any pre-authorization requirements?"
                }
            }
        }
        
        self.categories_order = ['eligibility', 'benefits', 'coverage', 'limitations']

    def check_transition_state(self, text: str) -> bool:
        """Use LLM to determine conversation state and readiness to transition"""
        try:
            # First check if we have all required fields
            required_fields = {'dob', 'member_id'}
            fields_collected = (hasattr(verify_patient, 'provided_fields') and 
                            verify_patient.provided_fields >= required_fields)
            
            if not fields_collected:
                print("Cannot transition: Required fields not collected")
                return False
                
            # Check for transition phrases directly first
            transition_phrases = [
                "how may i help",
                "how can help",
                "what can i help",
                "how can i assist",
                "what else",
                "what's next",
                "ready",
                "let's proceed",
                "go ahead"
            ]
            text_lower = text.lower()
            
            # If it's a direct match with transition phrases
            if any(phrase in text_lower for phrase in transition_phrases):
                print("Transition phrase detected, proceeding to verification")
                return True
                
            # If no direct match, use LLM as backup
            prompt = f"""You must respond with ONLY 'transition' or 'continue'.
            
            Determine if this response indicates readiness to proceed with insurance verification.
            The person has already provided date of birth and member ID. Do not worry about semantic correctness
            as long as the response makes sense.            
            Common transition phrases include:
            - Offering help (e.g., "how may I help")
            - Asking what's next
            - Indicating readiness to proceed
            - Expressing availability to assist
            
            Input: {text}
            
            Respond ONLY with:
            'transition' - if they're ready to proceed
            'continue' - if they're not indicating readiness"""
            
            response = self.verification.chat.send_message({"text": prompt})
            result = response.text.strip().lower()
            result = result.replace('```', '').strip()
            
            print(f"Required fields collected: {verify_patient.provided_fields}")
            print(f"Transition check result: {result}")
            
            should_transition = result == 'transition'
            if should_transition:
                print("LLM detected transition readiness")
            
            return should_transition
                
        except Exception as e:
            print(f"Error in transition check: {str(e)}")
            return False
            
    def process_response(self, text, verification):
        print(f"\n=== DEBUG - Process Response Start ===")
        print(f"Input text: '{text}'")
        print(f"Current phase: {'Patient Info' if self.is_patient_info_phase else 'Insurance Verification'}")

        if self.is_patient_info_phase:
            if hasattr(verify_patient, 'verification_asked'):
                print("Checking verification consent")
                question = "Would you mind verifying patient insurance coverage?"
                consent = verification.extract_boolean(question, text)
                print(f"Consent: {consent}")
                
                if consent:
                    print("Consent received - starting verification")
                    delattr(verify_patient, 'verification_asked')
                    self.is_patient_info_phase = False
                    verification.verification_started = True
                    verification.conversation_manager = self  # Pass self as conversation manager
                    next_question = self.get_next_question()
                    return next_question, True
                elif consent is False:
                    verification.verification_started = False
                    return "I understand. Please let me know when you're ready to proceed.", False
            
            required_fields = {'dob', 'member_id'}
            if (hasattr(verify_patient, 'provided_fields') and 
                verify_patient.provided_fields >= required_fields):

                help_prompt = f"""Is this a phrase offering help or asking how to assist? They usually ask these after
                providing patient name, dob and member id. The sentence does not have to be semantically correct as long
                as we can interprete it as an offering of help.
                Examples:
                - "How may I help you?"
                - "What can help you with?"
                - "How can I assist?"
                
                Return only 'True' or 'False'.
                Text: {text}"""
                
                is_help_phrase = verification.chat.send_message({"text": help_prompt}).text.strip().lower() == 'true'
                print(f"Is help phrase? {is_help_phrase}")

                if is_help_phrase:
                    print("Help phrase detected - asking for verification")
                    setattr(verify_patient, 'verification_asked', True)
                    return "Would you mind verifying patient insurance coverage?", False

            patient_info_response = verify_patient(verification.patient_data, text)
            return patient_info_response, False

        # Rest of insurance verification phase stays the same
        print("\n=== DEBUG - Insurance Verification Phase ===")
        print(f"Current category: {self.current_category}")
        current_fields = self.insurance_qa[self.current_category].keys()
        
        for field in current_fields:
            if verification.verification_data[self.current_category][field] is None:
                question = self.insurance_qa[self.current_category][field]['question']
                extract_func = verification.extraction_functions[self.current_category][field]
                
                value = extract_func(text, question)
                
                if value is not None:
                    verification.verification_data[self.current_category][field] = value
                    next_question = self.get_next_question()
                    print(f"Extracted {field}: {value}")
                    if next_question:
                        return next_question, False
                    else:
                        return "Verification complete!", False

        print("=== DEBUG - Process Response End ===")
        return "I didn't quite get that. Could you rephrase?", False
                

    def get_next_question(self):
        """Get next verification question based on current state"""
        if not self.verification_started:
            self.verification_started = True
            # First question of verification
            return self.insurance_qa['eligibility']['status']['question']

        current_fields = self.insurance_qa[self.current_category].keys()
        
        # Look for next empty field in current category
        for field in current_fields:
            if self.verification.verification_data[self.current_category][field] is None:
                return self.insurance_qa[self.current_category][field]['question']

        # All fields in current category complete, move to next category
        current_index = self.categories_order.index(self.current_category)
        if current_index < len(self.categories_order) - 1:
            next_category = self.categories_order[current_index + 1]
            self.current_category = next_category
            return (
                self._get_category_intro() +
                self.insurance_qa[next_category][list(self.insurance_qa[next_category].keys())[0]]['question']
            )

        return None  # All categories complete

    def _get_category_intro(self):
        """Get introduction message for new category"""
        intros = {
            'eligibility': "Let's verify eligibility. ",
            'benefits': "Now for benefits. ",
            'coverage': "Let's check coverage percentages. ",
            'limitations': "Finally, about limitations. "
        }
        return intros.get(self.current_category, "")     
