.code16
.global _start

_start:
    xor %ax, %ax # Clear the AX register
    mov %ax, %ds # Set DS to 0
    mov $msg, %si  # Load the address of the message into SI

print:
    lodsb           # Load the byte at SI into AL and increment SI
    cmp $0, %al     # Check if the byte is null (end of string)
    je done         # If it is null, jump to done

    mov $0x0E, %ah # BIOS teletype function
    int $0x10       # Call BIOS video interrupt to print the character

    jmp print       # Repeat for the next character

done:
    hlt             # Halt the CPU

msg:
.ascii " _   _ _ _ _   _ _   _ _____ _   _ \r\n"
    .ascii "| | | | | | | | | \\ | |_   _| | | |\r\n"
    .ascii "| |_| | | | |_| | |\\  | | | | |_| |\r\n"
    .ascii " \\___/|_____|\\___/|_| \\_| |_|  \\___/ \r\n"
    .ascii "                                     \r\n"
    .ascii "Hello, World! The uwuntu group greets you! :3\0"