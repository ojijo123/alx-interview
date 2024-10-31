def validUTF8(data):
    # Number of bytes remaining in the current UTF-8 character
    bytes_to_process = 0

    # Masks to determine the number of bytes in a character
    mask_1_byte = 0b10000000  # 1st bit
    mask_2_bytes = 0b11100000  # 3 leading bits
    mask_3_bytes = 0b11110000  # 4 leading bits
    mask_4_bytes = 0b11111000  # 5 leading bits
    mask_continuation = 0b11000000  # For 10xxxxxx check

    for byte in data:
        # Only keep the last 8 bits of each integer
        byte &= 0xFF

        if bytes_to_process == 0:
            # Determine the number of bytes for the current character
            if (byte & mask_1_byte) == 0:
                # 1-byte character (0xxxxxxx)
                bytes_to_process = 0
            elif (byte & mask_2_bytes) == 0b11000000:
                # 2-byte character (110xxxxx)
                bytes_to_process = 1
            elif (byte & mask_3_bytes) == 0b11100000:
                # 3-byte character (1110xxxx)
                bytes_to_process = 2
            elif (byte & mask_4_bytes) == 0b11110000:
                # 4-byte character (11110xxx)
                bytes_to_process = 3
            else:
                # Invalid start byte
                return False
        else:
            # Check if byte is a valid continuation byte (10xxxxxx)
            if (byte & mask_continuation) != 0b10000000:
                return False
            bytes_to_process -= 1

    # All characters should have been processed completely
    return bytes_to_process == 0
