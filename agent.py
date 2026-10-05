import os
import json
import ollama
import storage

class ClinicalSchedulerAgent:
    def __init__(self):
        self.conversation_history = []

    def build_system_prompt(self):
        prompt = (
            "You are a strict automated medical clinic appointment scheduling coordinator.\n"
            "Operating Hours: 9:00 AM to 5:00 PM, Monday to Friday.\n"
            f"Available Slots: {', '.join(storage.AVAILABLE_SLOTS)}.\n\n"
            "CRITICAL PROTOCOLS:\n"
            "1. You talk directly to the patient. Respond concisely.\n"
            "2. If a patient asks for a specific slot, you MUST check if it falls within our operating hours. If they ask for any time before 9:00 AM, you MUST immediately reject it out-of-bounds.\n"
            "3. If a valid slot is requested, use the tool keyword format: [CALL_TOOL: attempt_booking(TIME)]"
        )
        
        dynamic_rules = storage.get_dynamic_rules()
        if dynamic_rules:
            prompt += "\n\n[CRITICAL CLINICAL DIRECTIVES INJECTED VIA PAST CONSTRAINTS]:\n"
            for rule in dynamic_rules:
                prompt += f"- {rule}\n"
        return prompt

    def respond(self, user_message):
        self.conversation_history.append({"role": "user", "content": user_message})
        messages = [{"role": "system", "content": self.build_system_prompt()}] + self.conversation_history
        
        response = ollama.chat(model="clinic-llama", messages=messages, options={"temperature": 0.0})
        reply = response["message"]["content"].strip()
        
        # Intercept tool-calling patterns safely
        if "[CALL_TOOL:" in reply and "attempt_booking" in reply:
            try:
                time_part = reply.split("attempt_booking(")[-1].split(")")[0].replace("'", "").replace('"', "")
                db_result = storage.attempt_booking(time_part)
                
                if not db_result["success"]:
                    reply = f"I'm sorry, but {time_part} is not available. Our operating hours are 9:00 AM to 5:00 PM, Monday to Friday. Please choose a valid slot."
                else:
                    reply = db_result["message"]
            except Exception:
                reply = "I'm sorry, but that time slot is not available. Please select from our open slots."
                
        self.conversation_history.append({"role": "assistant", "content": reply})
        return reply
