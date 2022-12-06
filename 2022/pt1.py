#!/usr/bin/python3

def locate_start_of_packet(datastream):
    """ Finds the start_of_packet marker (first 4 non-repeating characters)
    and sends back the offset of the last character of this packet.
    >>> locate_start_of_packet("mjqjpqmgbljsphdztnvjfqwrcgsmlb")
    7
    >>> locate_start_of_packet("bvwbjplbgvbhsrlpgdmjqwftvncz")
    5
    >>> locate_start_of_packet("nppdvjthqldpwncqszvftbrmjlhg")
    6
    >>> locate_start_of_packet("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg")
    10
    >>> locate_start_of_packet("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw")
    11
    """
    for n in range(len(datastream) - 4):
        if len(set(datastream[n:n+4])) == 4:
            return n + 4
    return None

if __name__ == '__main__':
    with open("input_real", encoding="utf-8") as fd:
        print(locate_start_of_packet(fd.readline().strip()))
