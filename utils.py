import random
from datetime import datetime, timedelta
import re
import json
import pandas as pd
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain_community.vectorstores import FAISS
from flow import verify_patient

def format_date(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    return f"{date_obj.month}..{date_obj.day}..{date_obj.year}"

def handle_confirmation(text):
    text_lower = text.lower()
    return (
        True if any(x in text_lower for x in ['yes', 'correct', 'right', 'yeah', 'yep']) 
        else False if any(x in text_lower for x in ['no', 'incorrect', 'wrong', 'nope']) 
        else None
    )

def fake_patient():
    first_names = ['John', 'Maria', 'James', 'Sarah', 'Michael']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones']
    
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    
    return {
        'first_name': first_name,
        'last_name': last_name,
        'date_of_birth': format_date((datetime.now() - timedelta(days=random.randint(6570, 29200))).strftime('%Y-%m-%d')),
        'member_number': str(random.randint(100000000, 999999999)),
        'group_number': str(random.randint(1000, 9999)),
        'insurance_provider': random.choice(['Delta Dental', 'Cigna', 'MetLife', 'Aetna', 'Guardian'])
    }

def format_speech_output(text):
    text = text.replace(' ID ', ' I..D ').replace(' id ', ' I..D ')
    text = re.sub(r'(\d{1,2})/(\d{1,2})/(\d{4})', r'\1..\2..\3', text)
    text = re.sub(r'member I..D is (\d+)', lambda m: f'member I..D is {" ".join(list(m.group(1)))}', text)
    text = re.sub(r'group number is (\d+)', lambda m: f'group number is {" ".join(list(m.group(1)))}', text)
    text = re.sub(r'\$(\d+(?:,\d{3})*(?:\.\d{2})?)', lambda m: f'$ {" ".join(list(m.group(1).replace(",", "")))}', text)
    text = re.sub(r'(\d+)%', lambda m: f'{" ".join(list(m.group(1)))} percent', text)
    return text

def get_verification_summary(verification):
    summary = {
        'collected': {},
        'missing': [],
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'status': 'incomplete'
    }
    
    for category in verification.verification_data:
        summary['collected'][category] = {}
        for field, value in verification.verification_data[category].items():
            if value is not None:
                summary['collected'][category][field] = value
            else:
                summary['missing'].append(f"{category}.{field}")
    
    if not summary['missing']:
        summary['status'] = 'complete'
    
    return summary

def initialize_correction_system():
    try:
        df = pd.read_csv("./correction_lookup.csv")
        embeddings = HuggingFaceInstructEmbeddings(
            model_name="hkunlp/instructor-base",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True}
        )
        misheard_texts = df['misheard'].tolist()
        faiss_index = FAISS.from_texts(texts=misheard_texts, embedding=embeddings)
        print("Correction system initialized successfully")
        return faiss_index, df
    except Exception as e:
        print(f"Error initializing correction system: {str(e)}")
        return None, None


def find_similar_terms(query, faiss_index, df, current_context = "patient information", threshold = 0.70):
    """Search for similar terms using FAISS index with context"""
    if not query or not query.strip():
        return None, 0
        
    try:
        similar_docs_with_scores = faiss_index.similarity_search_with_score(query, k=1)
        if similar_docs_with_scores:
            doc, score = similar_docs_with_scores[0]
            confidence = 1 / (1 + score)
            matched_row = df[df['misheard'] == doc.page_content].iloc[0]
            
            print(f"\nContext Check - Looking in: {current_context}")
            print(f"Text: '{matched_row['correction']}'")
            
            if matched_row['context'].lower() == current_context.lower():
                return {'original': query, 'correction': matched_row['correction']}, confidence
            return None, 0
                
    except Exception as e:
        print(f"Error: {str(e)}")
    return None, 0

def get_llm_correction(text: str, verification) -> dict:
    """Use LLM to suggest correction when lookup.csv doesn't have a match"""
    try:
        prompt = f"""In an insurance verification context, suggest the most likely correction for this input.
        
        Common insurance verification phrases:
        - Questions about patient info: "What is the patient's name?", "What is the date of birth?"
        - Insurance queries: "What is the member ID?", "What's the eligibility status?"
        - Coverage questions: "What's the annual maximum?", "What's the deductible?"
        
        Input: "{text}"
        
        Return JSON format:
        {{"suggestion": "corrected phrase",
          "confidence": "high/medium/low"}}
        
        Return only valid JSON, no other text."""
        
        response = verification.chat.send_message({"text": prompt})
        result = json.loads(response.text.strip())
        
        return result
            
    except Exception as e:
        print(f"Error in LLM correction: {str(e)}")
        return None

def validate_input_context(text: str, verification, faiss_index=None, correction_df=None) -> dict:
    try:
        # Get current state safely
        if hasattr(verification, 'conversation_manager'):
            verification_started = not getattr(verification.conversation_manager, 'is_patient_info_phase', True)
        else:
            verification_started = False
            
        verification_asked = hasattr(verify_patient, 'verification_asked')
        current_context = "insurance verification" if verification_started else "patient information"
        
        print(f"\nDEBUG - Validation:")
        print(f"Input text: '{text}'")
        print(f"Verification started: {verification_started}")
        print(f"Current context: {current_context}")

        # Insurance verification phase
        if verification_started and hasattr(verification, 'conversation_manager'):
            # Try to extract information FIRST before any correction
            current_category = getattr(verification.conversation_manager, 'current_category', None)
            if current_category:
                current_fields = verification.conversation_manager.insurance_qa[current_category].keys()
                current_field = None
                
                for field in current_fields:
                    if verification.verification_data[current_category][field] is None:
                        current_field = field
                        break

                if current_field:
                    current_question = verification.conversation_manager.insurance_qa[current_category][current_field]['question']
                    print(f"Current field: {current_field}")
                    print(f"Current question: {current_question}")

                    # Check if response contains extractable information
                    info_prompt = f"""Does this response contain information relevant to: {current_question}
                    Look for:
                    1. Dollar amounts for payment questions
                    2. Percentages for coverage questions
                    3. Dates for effective date/period questions
                    4. Status terms (active, eligible) for eligibility
                    5. Any numbers or terms that answer the question
                    6. Even in incomplete sentences, is the required info present?
                    
                    Return ONLY 'True' if extractable info exists, 'False' if not.
                    Text: "{text}" """
                    
                    response = verification.chat.send_message({"text": info_prompt})
                    has_info = response.text.strip().lower() == 'true'
                    print(f"Contains relevant info for {current_field}: {has_info}")
                    
                    if has_info:
                        return {"needs_correction": False, "reason": "Contains relevant information"}

                    # Only try FAISS correction if no extractable information found
                    if faiss_index is not None and correction_df is not None:
                        correction, confidence = find_similar_terms(text, faiss_index, correction_df, current_context)
                        print(f"FAISS correction found: {correction}, confidence: {confidence}")
                        
                        if correction and confidence >= 0.7:
                            return {
                                "needs_correction": True,
                                "reason": f"Insurance verification correction found: {correction['correction']}"
                            }
        
        # Patient information phase - direct FAISS correction is fine
        else:
            if faiss_index is not None and correction_df is not None:
                correction, confidence = find_similar_terms(text, faiss_index, correction_df, current_context)
                print(f"FAISS correction found: {correction}, confidence: {confidence}")
                
                if correction and confidence >= 0.7:
                    if verification_asked:
                        return {
                            "needs_correction": True,
                            "reason": f"Consent response correction found: {correction['correction']}"
                        }
                    else:
                        return {
                            "needs_correction": True,
                            "reason": f"Patient information correction found: {correction['correction']}"
                        }

        # If no valid information or correction found
        return {
            "needs_correction": False,
            "confidence_too_low": True,
            "reason": "Please repeat your response"
        }

    except Exception as e:
        print(f"Error in validation: {str(e)}")
        return {
            "needs_correction": False,
            "confidence_too_low": True,
            "reason": f"Error in validation: {str(e)}"
        }

def enhance_accent_handling(text, faiss_index, correction_df, verification, current_context="patient information"):
    """Enhanced accent handling using FAISS for corrections"""
    if not text or not text.strip():
        return {'original': text, 'corrected': text, 'needs_confirmation': False}
        
    cleaned_text = text.lower().replace('?', '').replace('please', '').strip()
    
    # Try FAISS correction
    correction, confidence = find_similar_terms(cleaned_text, faiss_index, correction_df, current_context)
    
    if correction and confidence >= 0.70:
        return {
            'original': text, 
            'corrected': correction['correction'],
            'needs_confirmation': False
        }
    
    # If no confident correction found, return original text
    return {'original': text, 'corrected': text, 'needs_confirmation': False}