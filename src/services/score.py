import json
from paths import ROOT_DIR

score_file_path = ROOT_DIR / "best_score.json" 
default = {'best_score':0}

class Score:
    @staticmethod
    def create_score_file_if_not_exist() -> None:
        if score_file_path.exists():
            return

        Score.update_score_file(default)

    @staticmethod
    def load_score_file() -> dict:
        with open(score_file_path, mode="r", encoding="utf-8-sig") as file:
            return json.loads(file.read())

    @staticmethod
    def get_max_score() -> int:
        Score.create_score_file_if_not_exist()
        data = Score.load_score_file()

        return data.get("best_score")

    @staticmethod
    def update_score_file(data: dict):
        with open(score_file_path, mode="w", encoding="utf-8") as file:
            json.dump(data, file)

    @staticmethod
    def update_max_score(new_score):
        data = Score.load_score_file()
        data["best_score"] = new_score
        Score.update_score_file(data)