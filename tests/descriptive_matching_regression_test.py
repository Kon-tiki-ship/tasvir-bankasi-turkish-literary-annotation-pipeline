from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


def load_stage_05_4_module():
    module_path = Path(__file__).resolve().parents[1] / "pipeline" / "06_00_description_category_tagging.py"
    spec = importlib.util.spec_from_file_location("stage_05_4_descriptive_tagging", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load 06_00_description_category_tagging.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def collect_reasons(profile: list[dict]) -> set[str]:
    reasons: set[str] = set()
    for block in profile:
        for reason in block.get("reasons", []):
            reasons.add(reason)
    return reasons


class DescriptiveMatchingRegressionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.stage05_4 = load_stage_05_4_module()

    def assert_no_reason(self, text: str, reason: str) -> None:
        profile = self.stage05_4.build_descriptive_profile(text)
        self.assertNotIn(reason, collect_reasons(profile), msg=f"Unexpected reason '{reason}' for: {text}")

    def assert_has_reason(self, text: str, reason: str) -> None:
        profile = self.stage05_4.build_descriptive_profile(text)
        self.assertIn(reason, collect_reasons(profile), msg=f"Missing reason '{reason}' for: {text}")

    def test_negative_cases(self) -> None:
        self.assert_no_reason("böyle bir adamdı", "boy")
        self.assert_no_reason("boynuna atkı sardı", "boy")
        self.assert_no_reason("boyunlarına baktı", "boy")
        self.assert_no_reason("boyanmış bir oyuncak vardı", "boy")

        self.assert_no_reason("karısı ağlıyordu", "kar")
        self.assert_no_reason("karımı ağlar buldum", "kar")
        self.assert_no_reason("karısına baktı", "kar")
        self.assert_no_reason("karısını gördü", "kar")
        self.assert_no_reason("kara yağız bir attı", "kar")
        self.assert_no_reason("karanlık çöktü", "kar")
        self.assert_no_reason("karar verdim", "kar")
        self.assert_no_reason("karşıya baktı", "kar")
        self.assert_no_reason("Karahisarlı olduğunu söyledi", "kar")

        self.assert_no_reason("evlatları geldi", "ev")
        self.assert_no_reason("evlilik hakkında konuştu", "ev")
        self.assert_no_reason("evvel zaman içinde", "ev")
        self.assert_no_reason("grev başladı", "ev")

        self.assert_no_reason("elektriğini kapattı", "el")
        self.assert_no_reason("güzelliğiyle dikkat çekti", "el")
        self.assert_no_reason("ellilik bir adamdı", "el")
        self.assert_no_reason("otel kapısı açıktı", "el")
        self.assert_no_reason("güzel bir gündü", "el")

        self.assert_no_reason("bari sus", "bar")
        self.assert_no_reason("barış istiyordu", "bar")
        self.assert_no_reason("ibarettir", "bar")
        self.assert_no_reason("beraber yürüdüler", "bar")

        self.assert_no_reason("gözüküyordu", "goz")
        self.assert_no_reason("gölge duvara vurdu", "gol")
        self.assert_no_reason("tutan adam sustu", "utan")

        self.assert_no_reason("altı yüz lira verdi", "yuz")
        self.assert_no_reason("yüz lira borcu vardı", "yuz")
        self.assert_no_reason("iki yüz kuruş tuttu", "yuz")

        self.assert_no_reason("yağmurluklarını astılar", "yagmur")
        self.assert_no_reason("yağmurluk giydi", "yagmur")

        self.assert_no_reason("tutturulmuş bir levhaydı", "tuttu")
        self.assert_no_reason("duvara tutturulmuştu", "tuttu")

        self.assert_no_reason("çiçek motifli bir oyuncaktı", "cicek")
        self.assert_no_reason("llmn üzerine çiçek çizilmişti", "cicek")

    def test_positive_cases(self) -> None:
        self.assert_has_reason("evde oturuyordu", "ev")
        self.assert_has_reason("eve döndü", "ev")
        self.assert_has_reason("evin kapısı açıktı", "ev")
        self.assert_has_reason("evler uzakta kaldı", "ev")

        self.assert_has_reason("elini masaya koydu", "el")
        self.assert_has_reason("eliyle işaret etti", "el")
        self.assert_has_reason("elleri titriyordu", "el")

        self.assert_has_reason("kar yerde birikmişti", "kar")
        self.assert_has_reason("karlı bir sabahtı", "kar")
        self.assert_has_reason("karda yürüdü", "kar")

        self.assert_has_reason("gölde kayık vardı", "gol")
        self.assert_has_reason("gölün kıyısında durdu", "gol")

        self.assert_has_reason("yüzü solgundu", "yuz")
        self.assert_has_reason("adamın yüzüne baktı", "yuz")
        self.assert_has_reason("gözleri parlıyordu", "goz")
        self.assert_has_reason("gözü dalmıştı", "goz")

        self.assert_has_reason("yağmur yağıyordu", "yagmur")
        self.assert_has_reason("yağmurlu bir akşamdı", "yagmur")

        self.assert_has_reason("utandı ve sustu", "utan")
        self.assert_has_reason("elini tuttu", "tuttu")

        self.assert_has_reason("barda oturdu", "bar")
        self.assert_has_reason("barın önünde bekledi", "bar")

        self.assert_has_reason("boyu uzundu", "boy")
        self.assert_has_reason("boylu poslu bir adamdı", "boy")

        self.assert_has_reason("çiçekler açmıştı", "cicek")
        self.assert_has_reason("bahçede çiçek vardı", "cicek")


if __name__ == "__main__":
    unittest.main()
