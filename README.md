# 6TRON Flash
Tool to flash 6TRON Boards

## Usage
```
Usage: cli.py [OPTIONS] MCU ELF

  Console script for sixtron_flash.

Options:
  -p, --probe [j-link|st-link]
  --help                        Show this message and exit.
```

## 6TRON Boards

| Target                | JLink device  |
|-----------------------|---------------|
| ZEST_CORE_STM32L4A6RG | stm32l4a6rg   |
| ZEST_CORE_STM32L496RG | stm32l496rg   |
| ZEST_CORE_STM32G474VE | stm32g474ve   |
| ZEST_CORE_MTXDOT      | stm32l496rg   |
| ZEST_CORE_nRF52832    | nrf52832_xxaa |
| Z_MOTION              | stm32l496rg   |
| Z_ENVIRONMENT         | stm32l496rg   |