#!/usr/bin/python3

def locate_start_of_message(datastream):
    """ Finds the start_of_message marker (first 14 non-repeating characters)
    and sends back the offset of the last character of this packet.
    >>> locate_start_of_message("mjqjpqmgbljsphdztnvjfqwrcgsmlb")
    19
    >>> locate_start_of_message("bvwbjplbgvbhsrlpgdmjqwftvncz")
    23
    >>> locate_start_of_message("nppdvjthqldpwncqszvftbrmjlhg")
    23
    >>> locate_start_of_message("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg")
    29
    >>> locate_start_of_message("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw")
    26
    """
    for n in range(len(datastream) - 14):
        if len(set(datastream[n:n+14])) == 14:
            return n + 14
    return None

if __name__ == '__main__':
    with open("input_real", encoding="utf-8") as fd:
        print(locate_start_of_message(fd.readline().strip()))
