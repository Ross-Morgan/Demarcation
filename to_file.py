from typing import Iterator, TypeVar

T = TypeVar("T")


def chunks(arr: list[T], chunk_size: int) -> Iterator[list[T]]:
    for i in range(0, len(arr), chunk_size):
        yield arr[i: i + chunk_size]


def format_byte(n):
    s = hex(n)[2:]

    if len(s) < 2:
        s = f"0{s}"

    return f"\\x{s}"


with open("src/demarcation/logo.py", "w+") as f:
    with open("logo.webp", "rb") as byte_stream:
        ba = list(map(format_byte, bytearray(byte_stream.read())))  # noqa

        f.write('icon_data = b"""\n')

        for chunk in chunks(ba, 16):
            f.write("".join(chunk))
            f.write("\n")

        f.write('"""\n')
