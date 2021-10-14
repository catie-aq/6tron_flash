# 6TRON Flash
Tool to flash 6TRON boards.

## Usage
```
Usage: cli.py [OPTIONS] MCU ELF

  Console script for sixtron_flash.

Options:
  -p, --probe [j-link|st-link]
  --help                        Show this message and exit.
```

## 6TRON Boards

| Board                  | Target                | JLink device  |
|------------------------|-----------------------|---------------|
| Z_Environment          | Z_ENVIRONMENT         | stm32l496rg   |
| Z_Motion               | Z_MOTION              | stm32l496rg   |
| Zest_Core_MTXDOT       | ZEST_CORE_MTXDOT      | stm32l151cc   |
| Zest_Core_STM32G474VE  | ZEST_CORE_STM32G474VE | stm32g474ve   |
| Zest_Core_STM32H753ZI  | ZEST_CORE_STM32H753ZI | STM32h753vi   |
| Zest_Core_STM32L496RG  | ZEST_CORE_STM32L496RG | stm32l496rg   |
| Zest_Core_STM32L496ZG  | ZEST_CORE_STM32L496ZG | stm32l496zg   |
| Zest_Core_STM32L4A6RG  | ZEST_CORE_STM32L4A6RG | stm32l4a6rg   |
| Zest_Core_nRF52832     | ZEST_CORE_NRF52832    | nrf52832_xxaa |
