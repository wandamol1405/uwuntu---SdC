#include <efi.h>
#include <efilib.h>

EFI_STATUS efi_main(EFI_HANDLE ImageHandle, EFI_SYSTEM_TABLE *SystemTable)
{
    InitializeLib(ImageHandle, SystemTable);

    Print(L"\r\n");
    Print(L"=====================================\r\n");
    Print(L"              UWUNTU                 \r\n");
    Print(L"=====================================\r\n");

    Print(L" u     u  w     w  u     u  n   n  ttttt  u     u \r\n");
    Print(L" u     u  w  w  w  u     u  nn  n    t    u     u \r\n");
    Print(L" u     u  w w w w  u     u  n n n    t    u     u \r\n");
    Print(L" u     u  ww   ww  u     u  n  nn    t    u     u \r\n");
    Print(L"  uuuu     w   w    uuuu    n   n    t     uuuuu  \r\n");

    Print(L"\r\n        >>> grupo: uwuntu <<<\r\n\r\n");

    Print(L"Iniciando entorno pre-OS...\r\n");
    Print(L"Firmware activo. Protocolos cargados.\r\n");
    Print(L"Explorando el sistema desde UEFI...\r\n\r\n");

    unsigned char code[] = {0xCC};

    if (code[0] == 0xCC)
    {
        Print(L"[OK] Breakpoint detectado (INT3)\r\n");
    }

    Print(L"\r\nEjecucion finalizada.\r\n");

    return EFI_SUCCESS;
}