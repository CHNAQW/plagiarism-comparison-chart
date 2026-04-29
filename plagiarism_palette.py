import re
import tkinter as tk
from tkinter import ttk
from difflib import SequenceMatcher

HIGHLIGHT_COLOR = "#ffe66d"


TOKEN_PATTERN = re.compile(
    r"[\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF]|"  # CJK unified ideographs
    r"[A-Za-z0-9_]+(?:[\'’\-][A-Za-z0-9_]+)*|"            # Latin words / numbers
    r"[^\s]"                                                   # Other visible symbols
)


def tokenize_with_spans(text: str):
    tokens = []
    for m in TOKEN_PATTERN.finditer(text):
        tokens.append((m.group(0), m.start(), m.end()))
    return tokens


def infer_min_tokens(left_text: str, right_text: str, default: int = 2) -> int:
    # Chinese text typically has no spaces, so tokenization is character-level.
    # Use a slightly higher threshold to reduce accidental single short overlaps.
    has_cjk = bool(re.search(r"[\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF]", left_text + right_text))
    return 4 if has_cjk else default


def index_to_tk(text: str, char_index: int) -> str:
    row = text.count("\n", 0, char_index) + 1
    line_start = text.rfind("\n", 0, char_index)
    col = char_index if line_start == -1 else char_index - line_start - 1
    return f"{row}.{col}"


def clear_tags(widget: tk.Text):
    widget.tag_remove("match", "1.0", tk.END)


def highlight_matches(left_widget: tk.Text, right_widget: tk.Text, min_tokens: int | None = None):
    left_text = left_widget.get("1.0", tk.END).rstrip("\n")
    right_text = right_widget.get("1.0", tk.END).rstrip("\n")

    if min_tokens is None:
        min_tokens = infer_min_tokens(left_text, right_text)

    clear_tags(left_widget)
    clear_tags(right_widget)

    left_tokens = tokenize_with_spans(left_text)
    right_tokens = tokenize_with_spans(right_text)

    if not left_tokens or not right_tokens:
        return 0

    left_words = [w for w, _, _ in left_tokens]
    right_words = [w for w, _, _ in right_tokens]

    matcher = SequenceMatcher(None, left_words, right_words, autojunk=False)
    blocks = matcher.get_matching_blocks()

    hit_count = 0
    for block in blocks:
        if block.size < min_tokens:
            continue
        for i in range(block.size):
            l_tok = left_tokens[block.a + i]
            r_tok = right_tokens[block.b + i]

            l_start = index_to_tk(left_text, l_tok[1])
            l_end = index_to_tk(left_text, l_tok[2])
            r_start = index_to_tk(right_text, r_tok[1])
            r_end = index_to_tk(right_text, r_tok[2])

            left_widget.tag_add("match", l_start, l_end)
            right_widget.tag_add("match", r_start, r_end)
            hit_count += 1
    return hit_count


def run_detection(left_widget: tk.Text, right_widget: tk.Text, status_var: tk.StringVar):
    count = highlight_matches(left_widget, right_widget)
    status_var.set(f"已高亮 {count} 个疑似重复词。")


def build_ui():
    root = tk.Tk()
    root.title("抄袭调色盘")
    root.geometry("1100x700")

    container = ttk.Frame(root, padding=10)
    container.pack(fill=tk.BOTH, expand=True)

    top_frame = ttk.Frame(container)
    top_frame.pack(fill=tk.X, pady=(0, 8))

    ttk.Label(top_frame, text="文件名：").pack(side=tk.LEFT)
    filename_var = tk.StringVar(value="未命名.txt")
    ttk.Entry(top_frame, textvariable=filename_var, width=50).pack(side=tk.LEFT, padx=(0, 10))

    status_var = tk.StringVar(value="请输入左右文本，然后点击“检测重复”。")
    ttk.Label(top_frame, textvariable=status_var).pack(side=tk.LEFT)

    middle = ttk.Frame(container)
    middle.pack(fill=tk.BOTH, expand=True)

    left_frame = ttk.LabelFrame(middle, text="左侧文本")
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

    right_frame = ttk.LabelFrame(middle, text="右侧文本")
    right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))

    left_text = tk.Text(left_frame, wrap=tk.WORD, undo=True)
    left_text.pack(fill=tk.BOTH, expand=True)

    right_text = tk.Text(right_frame, wrap=tk.WORD, undo=True)
    right_text.pack(fill=tk.BOTH, expand=True)

    left_text.tag_configure("match", background=HIGHLIGHT_COLOR)
    right_text.tag_configure("match", background=HIGHLIGHT_COLOR)

    btn_frame = ttk.Frame(container)
    btn_frame.pack(fill=tk.X, pady=(8, 0))

    ttk.Button(
        btn_frame,
        text="检测重复",
        command=lambda: run_detection(left_text, right_text, status_var),
    ).pack(side=tk.LEFT)

    ttk.Label(btn_frame, text="提示：可识别连续短语重复，允许中间有跳段（基于序列匹配）。").pack(side=tk.LEFT, padx=(10, 0))

    root.mainloop()


if __name__ == "__main__":
    build_ui()
