"""Stack implementation and visualization demo.

This script covers the required procedural stack API as well as an
object-oriented stack with a simple ASCII visualization.
"""

MAX_ITEMS = 10
_stack_storage: list[str] = []


def push(item: str) -> None:
    """Push an item onto the shared stack if there is capacity."""
    if len(_stack_storage) >= MAX_ITEMS:
        print(f"[warn] stack full (max {MAX_ITEMS}); skipping push of {item!r}")
        return
    _stack_storage.append(item)
    print(f"[info] pushed {item!r}")


def pop() -> str | None:
    """Pop and return the most recently pushed item."""
    if empty():
        print("[warn] stack empty; nothing to pop")
        return None
    item = _stack_storage.pop()
    print(f"[info] popped {item!r}")
    return item


def empty() -> bool:
    """Return True when the shared stack contains no items."""
    return len(_stack_storage) == 0


def peek() -> str | None:
    """Return the most recent item without removing it."""
    if empty():
        print("[warn] stack empty; nothing to peek at")
        return None
    item = _stack_storage[-1]
    print(f"[info] peeked {item!r}")
    return item


class VisualStack:
    """Stack implementation with ASCII visualization helper."""

    def __init__(self, max_items: int = MAX_ITEMS) -> None:
        self.max_items = max_items
        self._items: list[str] = []

    def push(self, item: str) -> None:
        if len(self._items) >= self.max_items:
            print(f"[warn] visual stack full (max {self.max_items}); cannot add {item!r}")
            return
        self._items.append(item)
        print(f"[visual] pushed {item!r}")

    def pop(self) -> str | None:
        if self.empty():
            print("[warn] visual stack empty; nothing to pop")
            return None
        item = self._items.pop()
        print(f"[visual] popped {item!r}")
        return item

    def peek(self) -> str | None:
        if self.empty():
            print("[warn] visual stack empty; nothing to peek at")
            return None
        item = self._items[-1]
        print(f"[visual] peeked {item!r}")
        return item

    def empty(self) -> bool:
        return len(self._items) == 0

    def render(self) -> None:
        """Print an ASCII visualization of the current stack state."""
        print("\n=== Visual Stack State ===")
        if self.empty():
            print("| (empty) |")
            print("==========================\n")
            return

        for i, item in enumerate(reversed(self._items), start=1):
            label = f"#{len(self._items) - (i - 1):02d}"
            print("+----------------------+")
            print(f"| top {label}: {item:<12} |")
        print("+----------------------+")
        print("==========================\n")


def demo_basic_stack() -> None:
    print("== Basic Stack Demo ==")
    for idx in range(1, MAX_ITEMS + 3):
        push(f"task-{idx:02d}")

    peek()

    while not empty():
        pop()

    # Attempt another pop to show the warning on an empty stack
    pop()
    print()


def demo_visual_stack() -> None:
    print("== Visual Stack Demo ==")
    visual_stack = VisualStack(max_items=5)

    for idx in range(1, 7):
        visual_stack.push(f"job-{idx:02d}")
        visual_stack.render()

    visual_stack.peek()
    visual_stack.render()

    for _ in range(3):
        visual_stack.pop()
        visual_stack.render()

    # Show empty visualization warning
    visual_stack.pop()
    visual_stack.render()
    visual_stack.pop()
    visual_stack.render()

    # Attempt to pop once more to trigger empty warning
    visual_stack.pop()
    print()


def interactive_session() -> None:
    """Interactive prompt so users can test the stack manually."""
    print("== Interactive Stack Session ==")
    stack_size_input = input("Enter maximum stack size (default 5): ").strip()
    if stack_size_input:
        try:
            max_items = int(stack_size_input)
            if max_items <= 0:
                raise ValueError
        except ValueError:
            print("[warn] invalid size input; falling back to 5")
            max_items = 5
    else:
        max_items = 5

    interactive_stack = VisualStack(max_items=max_items)
    print(
        "Commands: push <value>, pop, peek, show, quit\n"
        "Try pushing values with IDs to observe stack order."
    )

    while True:
        command = input("stack> ").strip()
        if not command:
            continue

        lower = command.lower()
        if lower in {"quit", "exit"}:
            print("[info] ending interactive session")
            break

        if lower.startswith("push"):
            parts = command.split(maxsplit=1)
            if len(parts) < 2 or not parts[1]:
                print("[warn] usage: push <value>")
                continue
            interactive_stack.push(parts[1])
            interactive_stack.render()
            continue

        if lower == "pop":
            interactive_stack.pop()
            interactive_stack.render()
            continue

        if lower == "peek":
            interactive_stack.peek()
            continue

        if lower == "show":
            interactive_stack.render()
            continue

        print("[warn] unknown command; valid commands are push/pop/peek/show/quit")


if __name__ == "__main__":
    demo_basic_stack()
    demo_visual_stack()
    run_interactive = input("Run interactive session? (y/n): ").strip().lower()
    if run_interactive.startswith("y"):
        interactive_session()
