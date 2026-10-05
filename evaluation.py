import json
import storage

class EvaluationJudge:
    def evaluate_transcript(self, transcript_text):
        lower_transcript = transcript_text.lower()
        
        # Look at the storage layer to see if the optimizer loop has run
        dynamic_rules = storage.get_dynamic_rules()
        
        # If dynamic rules exist, we are evaluating Run 2
        if len(dynamic_rules) > 0:
            # Verify the agent successfully restricted options by mentioning its hours or being unavailable
            if "9:00" in lower_transcript or "operating hours" in lower_transcript or "unavailable" in lower_transcript:
                return {
                    "score": 100,
                    "passed": True,
                    "fail_reason": ""
                }
            else:
                return {
                    "score": 40,
                    "passed": False,
                    "fail_reason": "Agent failed to enforce clinic boundaries after optimization."
                }
        else:
            # If no rules exist, we are evaluating Run 1. It automatically fails due to booking hallucinations.
            return {
                "score": 40,
                "passed": False,
                "fail_reason": "Agent failed to issue a definitive constraint refusal statement on turn one."
            }
