
from . import RiskPreferences, RiskPreferences2, RiskPreferences3, Demographics
from otree.api import Bot


class PlayerBot(Bot):
    def play_round(self):
        yield RiskPreferences, dict(c9_or_30at09_otherwise_minus270=1)
        yield RiskPreferences2, dict(c11_or_30at09_otherwise_minus270=2)
        yield RiskPreferences3, dict(c7_or_30at09_otherwise_minus270=3)
        yield Demographics, dict(age=20, gender="Male", full_name="John Doe", academic_degree="MSc",
                                 is_english_native_language="No", survey_optional_text="Blah")

