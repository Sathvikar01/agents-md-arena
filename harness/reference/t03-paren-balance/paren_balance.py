PAIRS = {")": "(", "]": "[", "}": "{"}


def is_balanced(s: str) -> bool:
    stack = []
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif ch in PAIRS:
            if not stack or stack[-1] != PAIRS[ch]:
                return False
            stack.pop()
    return not stack
