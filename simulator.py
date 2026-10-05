import ollama
from agent import ClinicalSchedulerAgent

class PatientSimulator:
    def simulate(self, persona_prompt):
        agent = ClinicalSchedulerAgent()
        transcript = []
        
        patient_history = [{"role": "system", "content": f"You are a human patient calling a medical clinic. Follow this exact persona instruction:\n{persona_prompt}\nSpeak only as the human patient. Do not break character. Do not repeat the agent instructions."}]
        
        agent_reply = "Hello! Welcome to our clinic scheduling assistant. How can I help you today?"
        transcript.append({"speaker": "Agent", "text": agent_reply})
        
        for turn in range(3):
            patient_history.append({"role": "assistant", "content": agent_reply})
            response = ollama.chat(model="clinic-llama", messages=patient_history, options={"temperature": 0.3})
            patient_reply = response["message"]["content"].strip()
            
            if "agent:" in patient_reply.lower():
                patient_reply = patient_reply.lower().split("agent:")[-1].strip()
            if "patient:" in patient_reply.lower():
                patient_reply = patient_reply.lower().split("patient:")[-1].strip()
                
            patient_history.append({"role": "user", "content": patient_reply})
            transcript.append({"speaker": "Patient", "text": patient_reply})
            
            agent_reply = agent.respond(patient_reply)
            transcript.append({"speaker": "Agent", "text": agent_reply})
            
            if any(word in patient_reply.lower() for word in ["bye", "thank you", "goodbye"]):
                break
        return transcript
