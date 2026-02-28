import openai
import json
import os
from dotenv import load_dotenv

load_dotenv()

class MCQGenerator:
    """Generate MCQs from notes using OpenAI API"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        openai.api_key = self.api_key
    
    def generate_mcqs(self, notes_text, num_questions=5):
        """Generate MCQ questions from notes text"""
        try:
            # Create prompt for GPT
            prompt = self._create_prompt(notes_text, num_questions)
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert educator creating multiple choice questions from study notes."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            # Parse response
            content = response['choices'][0]['message']['content']
            mcqs = self._parse_mcqs(content)
            
            return mcqs
        
        except Exception as e:
            raise Exception(f"Error generating MCQs: {str(e)}")
    
    def _create_prompt(self, notes_text, num_questions):
        """Create the prompt for MCQ generation"""
        prompt = f"""Based on the following study notes, generate exactly {num_questions} multiple choice questions.

For each question:
1. Create a clear, specific question
2. Provide 4 options (A, B, C, D)
3. Indicate the correct answer
4. Provide a brief explanation for why the answer is correct

Return the response as a JSON array with the following structure:
[
  {{
    "question": "question text",
    "options": {{"A": "option A", "B": "option B", "C": "option C", "D": "option D"}},
    "correct_answer": "A",
    "explanation": "explanation text"
  }}
]

STUDY NOTES:
{notes_text}

Generate the MCQs now:"""
        return prompt
    
    def _parse_mcqs(self, response_text):
        """Parse MCQs from API response"""
        try:
            # Try to extract JSON from response
            json_start = response_text.find('[')
            json_end = response_text.rfind(']') + 1
            
            if json_start != -1 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                mcqs = json.loads(json_str)
                return mcqs
            else:
                raise ValueError("Could not find JSON in response")
        
        except json.JSONDecodeError as e:
            raise Exception(f"Error parsing MCQ JSON: {str(e)}")