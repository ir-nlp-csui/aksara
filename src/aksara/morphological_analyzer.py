from typing import List, Literal


class MorphologicalAnalyzer:
    def analyze(
        self, input_src: str,
        input_mode: Literal["f", "s"] = "s",
        is_informal: bool = False,
        sep_regex: str = None,
    ) -> List[List[tuple[str, str]]]:
        pass

    def analyze_to_file(
        self, input_src: str,
        write_path: str,
        input_mode: Literal["f", "s"] = "s",
        write_mode: Literal['a', 'w', 'x'] = 'x',
        is_informal: bool = False,
        sep_regex: str = None
    ) -> str:
        pass